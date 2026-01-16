#!/usr/bin/env python3
"""
Full orchestration controller for Phases 0–7b

Processes all .py files in LEGACY_SCRIPTS_TO_EXAMINE, uses pre-generated
packet subdirs from Phase 0, updates End-to-End JSON in-place, and moves
PASS, FAIL, or UNKNOWN files to final destination.

Expects:
- JSON and test already seeded by batch collector + Phase 0
- Audit scripts to emit granular diagnostics
- Rewrite engine and test runner to be externally callable

Does NOT do batch collection. This script is called after batch_collector.py.
"""

import shutil, json, subprocess, sys, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/workspaces/Logos_System").resolve()
SRC = REPO / "_Dev_Resources/LEGACY_SCRIPTS_TO_EXAMINE"
PACKET_ROOT = REPO / "_Dev_Resources/AUTOMATION_ORCHESTRATOR/END_TO_END_PACKET"
PASS_DIR = REPO / "_Dev_Resources/AUTO_NORMAL_FINALS"
FAIL_DIR = REPO / "_Dev_Resources/AUTOMATION_FAIL_GROUP"
UNKNOWN_DIR = REPO / "_Dev_Resources/AUTOMATION_UNKNOWN_GROUP"

AUDITS = [
    ("phase_1_imports", "scan_imports.py"),
    ("phase_2_symbols", "scan_symbols.py"),
    ("phase_3_dependencies", "scan_dependencies.py"),
    ("phase_4_side_effects", "scan_side_effects.py"),
]
SEMANTIC = ("phase_6_semantic_audit", "scan_semantic.py")
REWRITE_SCRIPT = "phase5_rewriter.py"
TEST_SCRIPT = "run_all_tests.py"
SCHEMA_PATH = REPO / "_Dev_Resources/AUTOMATION_ORCHESTRATOR/end_to_end_schema.json"
BENIGN_REASONS = {"unresolved_to_local_path"}

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(data, path):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def run_phase(script, file, target: Path | None = None):
    target_file = target or file
    result = subprocess.run([sys.executable, str(REPO / "_Dev_Resources/Dev_Scripts/repo_tools/system_audit" / script), str(target_file)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] {script} on {target_file.name}")
        return []
    try:
        j = json.loads(result.stdout)
        return j.get(str(target_file), []) if isinstance(j, dict) else j
    except Exception:
        print(f"[WARN] JSON parse failed for {script} on {target_file.name}")
        return []


def _filter_benign(diags):
    return [d for d in diags if d.get("reason") not in BENIGN_REASONS]

def append_to_packet(file, phase, diagnostics):
    json_path = PACKET_ROOT / file.stem / f"{file.stem}.json"
    data = load_json(json_path)
    phases = data.setdefault("phases", {})
    current = phases.get(phase)

    if isinstance(current, list):
        # phase_5_rewrite_attempts
        if isinstance(diagnostics, list):
            current.extend(diagnostics)
        else:
            current.append(diagnostics)
    else:
        target = phases.setdefault(phase, {})
        if isinstance(target, dict):
            target["diagnostics"] = diagnostics
        else:
            phases[phase] = {"diagnostics": diagnostics}

    phases.update(phases)
    save_json(data, json_path)


def record_rewrite_attempt(file, attempt: int, status: str, rewrite_path: Path | None):
    json_path = PACKET_ROOT / file.stem / f"{file.stem}.json"
    data = load_json(json_path)
    arr = data.setdefault("phases", {}).setdefault("phase_5_rewrite_attempts", [])
    entry = {
        "attempt": attempt,
        "rewrite_path": str(rewrite_path) if rewrite_path else "",
        "rewrite_hash": hash_file(rewrite_path) if rewrite_path and rewrite_path.exists() else "",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
    }
    arr.append(entry)
    save_json(data, json_path)

def move_final_packet(file, outcome):
    packet_subdir = PACKET_ROOT / file.stem
    if outcome == "PASS":
        final_dir = PASS_DIR / file.stem
        final_dir.mkdir(parents=True, exist_ok=True)
        for item in packet_subdir.iterdir():
            shutil.copy2(item, final_dir / item.name)
        shutil.move(str(file), final_dir / file.name)
    elif outcome == "FAIL":
        shutil.move(str(file), FAIL_DIR / file.name)
    elif outcome == "UNKNOWN":
        shutil.move(str(file), UNKNOWN_DIR / file.name)

def main():
    limit = int(os.environ.get("ORCH_LIMIT", "0") or 0)
    files = sorted(SRC.glob("*.py"))
    if limit > 0:
        files = files[:limit]
    for file in files:
        print(f"\n[START] {file.name}")
        # Run Phases 1–4
        for phase, script in AUDITS:
            diags = run_phase(script, file)
            append_to_packet(file, phase, diags)

        # Phase 5 (Attempt 1)
        rc1 = subprocess.run([sys.executable, REPO / "_Dev_Resources/Dev_Scripts" / REWRITE_SCRIPT, str(file), "1"], capture_output=True).returncode
        packet_dir = PACKET_ROOT / file.stem
        json_path = packet_dir / f"{file.stem}.json"
        meta = load_json(json_path).get("metadata", {}) if json_path.exists() else {}
        type_name = meta.get("type_cast_name", file.stem)
        rewrite_path = packet_dir / f"{type_name}.py"
        if rc1 != 0:
            record_rewrite_attempt(file, 1, "failed", rewrite_path if rewrite_path.exists() else None)
            move_final_packet(file, "UNKNOWN")
            continue
        record_rewrite_attempt(file, 1, "complete", rewrite_path)

        # Phase 6 (Semantic Audit, one-shot)
        sem_diags = run_phase(SEMANTIC[1], file, target=rewrite_path)
        append_to_packet(file, SEMANTIC[0], sem_diags)

        # Phase 7 (Attempt 1 verification)
        verified = all(
            len(_filter_benign(run_phase(script, file, target=rewrite_path))) == 0
            for script in [a[1] for a in AUDITS]
        )
        if verified:
            # Run tests
            test_rc = subprocess.run([sys.executable, REPO / "_Dev_Resources/Dev_Scripts" / TEST_SCRIPT, str(file)]).returncode
            outcome = "PASS" if test_rc == 0 else "FAIL"
            move_final_packet(file, outcome)
            continue

        # Phase 5b (rewrite attempt 2)
        rc2 = subprocess.run([sys.executable, REPO / "_Dev_Resources/Dev_Scripts" / REWRITE_SCRIPT, str(file), "2"], capture_output=True).returncode
        rewrite_path2 = packet_dir / f"{type_name}.py"
        if rc2 != 0:
            record_rewrite_attempt(file, 2, "failed", rewrite_path2 if rewrite_path2.exists() else None)
            move_final_packet(file, "FAIL")
            continue
        record_rewrite_attempt(file, 2, "complete", rewrite_path2)

        # Phase 7b (re-verification)
        verified2 = all(
            len(_filter_benign(run_phase(script, file, target=rewrite_path2))) == 0
            for script in [a[1] for a in AUDITS]
        )
        final_outcome = "PASS" if verified2 else "FAIL"
        move_final_packet(file, final_outcome)

if __name__ == "__main__":
    main()

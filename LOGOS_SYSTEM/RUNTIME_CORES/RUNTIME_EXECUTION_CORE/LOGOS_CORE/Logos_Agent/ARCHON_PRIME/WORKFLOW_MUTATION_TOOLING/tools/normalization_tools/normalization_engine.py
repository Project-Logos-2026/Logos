# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-061
# module_name:          normalization_engine
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/normalization_engine.py
# responsibility:       Utility module: normalization engine
# runtime_stage:        utility
# execution_entry:      None
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

"""
Normalization Engine
====================
Generic pre-governance normalization pass for Python modules staged in
WORKFLOW_TARGET_PROCESSING/PROCESSING.

Pipeline stages per module:
  1. Enumerate .py files in PROCESSING
  2. Syntax validation (ast.parse)
  3. Path literal substitution (configurable PATH_SUBSTITUTIONS)
  4. Import normalization (comment out unresolvable namespace imports)
  5. Compile/runtime import test (compile() without executing side effects)
  6. Relocation: passing modules → COMPLETED; failing modules stay in PROCESSING
  7. Completion report written to COMPLETION_LOGS

Entry point: run_normalization_pass()
"""

import ast
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Directory constants ────────────────────────────────────────────────────
AP_ROOT = Path("/workspaces/ARCHON_PRIME")
PROCESSING = AP_ROOT / "WORKFLOW_TARGET_PROCESSING" / "PROCESSING"
COMPLETED = AP_ROOT / "WORKFLOW_TARGET_PROCESSING" / "COMPLETED"
COMP_LOGS = AP_ROOT / "WORKFLOW_TARGET_PROCESSING" / "COMPLETION_LOGS"
AP_OUTPUT = AP_ROOT / "SYSTEM_AUDITS_AND_REPORTS" / "PIPELINE_OUTPUTS"

COMPLETED.mkdir(parents=True, exist_ok=True)
COMP_LOGS.mkdir(parents=True, exist_ok=True)
AP_OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Path-substitution rules (ordered: most specific first) ────────────────
# Each entry is (source_literal_pattern, replacement_string).
# Add or remove entries as the source repo evolves.
PATH_SUBSTITUTIONS: list[tuple[str, str]] = [
    (
        r"/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime",
        str(AP_OUTPUT),
    ),
    (
        r"/workspaces/Logos/_Dev_Resources/STAGING/APPLICATION_FUNCTIONS",
        str(AP_ROOT / "WORKFLOW_TARGET_PROCESSING" / "INCOMING_TARGETS" / "TARGETS"),
    ),
    (
        r"/workspaces/Logos/Blueprints/reasoning",
        str(COMPLETED),
    ),
    (
        r"/workspaces/Logos/Blueprints/utils",
        str(COMPLETED),
    ),
    (
        r"/workspaces/Logos/Tools",
        str(AP_ROOT / "WORKFLOW_MUTATION_TOOLING" / "tools"),
    ),
    # Generic source repo root — must be last
    (
        r"/workspaces/Logos",
        str(AP_ROOT),
    ),
]

# ── Import prefixes that are unresolvable in this repo ───────────────────
# Matching top-level import statements are commented out rather than deleted.
UNRESOLVABLE_IMPORT_PREFIXES: tuple[str, ...] = (
    "Logos.",
    "LOGOS_SYSTEM.",
    "logos.",
)


# ═══════════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════════


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _try_parse(source: str) -> tuple[bool, str]:
    """Return (parseable, error_message)."""
    try:
        ast.parse(source)
        return True, ""
    except SyntaxError as exc:
        return False, str(exc)


def _apply_path_substitutions(source: str) -> tuple[str, list[str]]:
    """Replace path literals using PATH_SUBSTITUTIONS. Returns (source, changes)."""
    changes: list[str] = []
    for src_pattern, replacement in PATH_SUBSTITUTIONS:
        pattern = re.compile(re.escape(src_pattern))
        if pattern.search(source):
            source = pattern.sub(replacement, source)
            changes.append(f"Replaced '{src_pattern}' → '{replacement}'")
    return source, changes


def _normalize_imports(source: str) -> tuple[str, list[str]]:
    """
    Comment out import lines referencing UNRESOLVABLE_IMPORT_PREFIXES.
    Returns (source, changes).
    """
    changes: list[str] = []
    out: list[str] = []
    for line in source.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("import ", "from ")):
            module_name = ""
            if stripped.startswith("from "):
                module_name = stripped[5:].split()[0]
            elif stripped.startswith("import "):
                module_name = stripped[7:].split()[0]
            if any(module_name.startswith(pfx) for pfx in UNRESOLVABLE_IMPORT_PREFIXES):
                out.append(
                    "# [NORM] removed unresolvable import: " + line.rstrip() + "\n"
                )
                changes.append(f"Commented out: {line.strip()}")
                continue
        out.append(line)
    return "".join(out), changes


def _attempt_repair(source: str, error: str) -> tuple[str, list[str]]:
    """
    Lightweight syntax repair attempts, in order:
      1. Comment out the specific line reported by SyntaxError.
      2. Strip trailing whitespace/incomplete block at EOF.
    Returns (source, repair_notes).
    """
    repairs: list[str] = []

    match = re.search(r"line (\d+)", error)
    if match:
        lineno = int(match.group(1))
        lines = source.splitlines(keepends=True)
        if 1 <= lineno <= len(lines):
            bad_line = lines[lineno - 1]
            lines[lineno - 1] = (
                f"# [NORM-REPAIR] syntax error on original line {lineno}: {bad_line.rstrip()}\n"
            )
            candidate = "".join(lines)
            if _try_parse(candidate)[0]:
                repairs.append(
                    f"Commented out syntax-error line {lineno}: {bad_line.strip()}"
                )
                return candidate, repairs

    stripped = source.rstrip()
    if stripped != source and _try_parse(stripped + "\n")[0]:
        repairs.append("Stripped trailing whitespace/incomplete block")
        return stripped + "\n", repairs

    return source, repairs


def _compile_test(filepath: Path) -> tuple[bool, str]:
    """
    Validate the module compiles cleanly without executing side effects.
    Returns (success, error_or_empty).
    """
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        compile(source, str(filepath), "exec")
        return True, ""
    except Exception as exc:
        return False, str(exc)


# ═══════════════════════════════════════════════════════════════════════════
# Per-module normalization
# ═══════════════════════════════════════════════════════════════════════════


def normalize_module(filepath: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "module": filepath.name,
        "path": str(filepath),
        "status": "pending",
        "syntax_ok": False,
        "syntax_repaired": False,
        "path_changes": [],
        "import_changes": [],
        "repair_notes": [],
        "compile_ok": False,
        "errors": [],
        "moved_to": None,
    }

    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        record["errors"].append(f"Read error: {exc}")
        record["status"] = "failed"
        return record

    # Syntax validation
    ok, err = _try_parse(source)
    if not ok:
        source, repairs = _attempt_repair(source, err)
        record["repair_notes"].extend(repairs)
        ok, err = _try_parse(source)
        if ok:
            record["syntax_ok"] = True
            record["syntax_repaired"] = True
        else:
            record["errors"].append(f"Syntax error (unrepaired): {err}")
    else:
        record["syntax_ok"] = True

    # Path normalization
    source, path_changes = _apply_path_substitutions(source)
    record["path_changes"] = path_changes

    # Import normalization
    source, import_changes = _normalize_imports(source)
    record["import_changes"] = import_changes

    # Write normalized source back
    try:
        filepath.write_text(source, encoding="utf-8")
    except Exception as exc:
        record["errors"].append(f"Write error: {exc}")
        record["status"] = "failed"
        return record

    # Compile test
    compile_ok, compile_err = _compile_test(filepath)
    record["compile_ok"] = compile_ok
    if not compile_ok:
        record["errors"].append(f"Compile failed: {compile_err}")

    # Relocate if both syntax and compile pass
    if record["syntax_ok"] and compile_ok:
        dest = COMPLETED / filepath.name
        shutil.move(str(filepath), str(dest))
        record["moved_to"] = str(dest)
        record["status"] = "success"
    else:
        record["status"] = "failed"

    return record


# ═══════════════════════════════════════════════════════════════════════════
# Main pass
# ═══════════════════════════════════════════════════════════════════════════


def run_normalization_pass() -> dict[str, Any]:
    """
    Normalize all .py files in PROCESSING.
    Returns the summary report dict; also writes it to COMPLETION_LOGS.
    """
    print(f"\n{'='*70}")
    print("  Normalization Engine")
    print(f"  Started : {_now_iso()}")
    print(f"  Source  : {PROCESSING}")
    print(f"  Dest    : {COMPLETED}")
    print(f"{'='*70}\n")

    py_files = sorted(PROCESSING.glob("*.py"))
    total = len(py_files)
    print(f"[ENUM] {total} Python module(s) found in PROCESSING.\n")

    results: list[dict[str, Any]] = []
    success_count = repaired_count = failed_count = 0

    for idx, fp in enumerate(py_files, 1):
        print(f"[{idx:02d}/{total}] {fp.name}")
        rec = normalize_module(fp)
        results.append(rec)

        tag = "OK" if rec["status"] == "success" else "FAIL"
        repaired_tag = " [REPAIRED]" if rec.get("syntax_repaired") else ""
        print(f"        {tag}{repaired_tag}")
        for c in rec["path_changes"]:
            print(f"        PATH  : {c}")
        for c in rec["import_changes"]:
            print(f"        IMPORT: {c}")
        for e in rec["errors"]:
            print(f"        ERROR : {e}")

        if rec["status"] == "success":
            success_count += 1
        if rec.get("syntax_repaired"):
            repaired_count += 1
        if rec["status"] == "failed":
            failed_count += 1

    report: dict[str, Any] = {
        "report_id": "Normalization_Engine_Pass",
        "generated_at": _now_iso(),
        "processing_directory": str(PROCESSING),
        "completed_directory": str(COMPLETED),
        "total_modules_processed": total,
        "modules_successfully_normalized": success_count,
        "modules_repaired": repaired_count,
        "modules_failed": failed_count,
        "pass_criteria_met": failed_count == 0,
        "modules": results,
    }

    report_path = COMP_LOGS / "normalization_engine_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\n{'='*70}")
    print("  NORMALIZATION PASS COMPLETE")
    print(f"  Processed : {total}")
    print(f"  Passed    : {success_count}")
    print(f"  Repaired  : {repaired_count}")
    print(f"  Failed    : {failed_count}")
    print(f"  Report    : {report_path}")
    print(f"{'='*70}\n")

    return report


if __name__ == "__main__":
    run_normalization_pass()

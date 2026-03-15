#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-020
# module_name:          reorganize
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/reorganize.py
# responsibility:       Mutation module: reorganize
# runtime_stage:        repair
# execution_entry:      None
# allowed_targets:      ["WORKFLOW_TARGET_PROCESSING/PROCESSING"]
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
ARCHON PRIME — APPLICATION_FUNCTIONS Categorical Reorganization
Move-only pass; no code edits, no deletions, no import modifications.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: reorganize.py
tool_category: Migration
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python reorganize.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import json
import shutil
import sys
from pathlib import Path

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json

        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


# ── Constants ────────────────────────────────────────────────────────────────
REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
TOOLS_DIR = REPO_ROOT / "Tools"
APP_FUNC_DIR = REPO_ROOT / "_Dev_Resources/STAGING/APPLICATION_FUNCTIONS"
BLUEPRINTS_DIR = REPO_ROOT / "Blueprints"

CATEGORIES = ["reasoning", "agent", "utility", "semantic", "safety", "math"]

PACKET_FILE = TOOLS_DIR / "module_packets.json"
REPORT_FILE = APP_FUNC_DIR / "reorganization_report.json"

# ── Step 1 — Load packet data ─────────────────────────────────────────────────
print("=" * 60)
print("ARCHON PRIME — APPLICATION_FUNCTIONS Reorganization")
print("=" * 60)
print()
print("=== STEP 1: LOAD CLASSIFICATION ARTIFACTS ===")

with open(PACKET_FILE) as f:
    packets: list[dict] = json.load(f)

print(f"  Packets loaded: {len(packets)}")

# ── Step 2 — Build module-stem → category map ────────────────────────────────
print()
print("=== STEP 2: BUILD MODULE → CATEGORY MAP ===")

# module stem → classification
stem_to_category: dict[str, str] = {}
# module stem → recorded relative file path (for external detection)
stem_to_recorded_paths: dict[str, list[str]] = {}

for pkt in packets:
    cls = pkt["classification"]
    for stem, fpath in zip(
        pkt.get("modules", []), pkt.get("file_paths", []), strict=False
    ):
        stem_to_category[stem] = cls
        stem_to_recorded_paths.setdefault(stem, []).append(fpath)

print(f"  Module stems mapped: {len(stem_to_category)}")

# ── Step 3 — Ensure category directories exist ───────────────────────────────
print()
print("=== STEP 3: CREATE CATEGORY DIRECTORIES ===")

for cat in CATEGORIES:
    d = APP_FUNC_DIR / cat
    if not d.exists():
        d.mkdir(parents=True)
        print(f"  Created: {d.relative_to(REPO_ROOT)}")
    else:
        print(f"  Exists:  {d.relative_to(REPO_ROOT)}")

# ── Step 4 — Scan APPLICATION_FUNCTIONS tree ──────────────────────────────────
print()
print("=== STEP 4: SCAN APPLICATION_FUNCTIONS ===")

all_py_files = sorted(APP_FUNC_DIR.rglob("*.py"))
print(f"  Python files found: {len(all_py_files)}")

# ── Step 5 — Execute moves with rollback support ─────────────────────────────
print()
print("=== STEP 5: CLASSIFY AND MOVE MODULES ===")

moves_performed: list[dict] = []
skipped_already_correct: int = 0
skipped_no_classification: list[str] = []
rollback_log: list[tuple[Path, Path]] = []  # (new_path, original_path)


def rollback_all() -> None:
    print("  ROLLBACK: restoring moved files …")
    for new_p, orig_p in reversed(rollback_log):
        try:
            orig_p.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(new_p), str(orig_p))
            print(f"    Restored: {orig_p.relative_to(REPO_ROOT)}")
        except Exception as rb_err:
            print(f"    ROLLBACK FAILED for {new_p}: {rb_err}")


for py_file in all_py_files:
    stem = py_file.stem
    category = stem_to_category.get(stem)

    if category is None:
        skipped_no_classification.append(str(py_file.relative_to(REPO_ROOT)))
        continue

    target_dir = APP_FUNC_DIR / category
    target_path = target_dir / py_file.name

    # Already in the correct category directory?
    try:
        py_file.relative_to(target_dir)
        skipped_already_correct += 1
        continue
    except ValueError:
        pass  # not inside target_dir — needs moving

    # Ensure no collision at destination
    if target_path.exists() and target_path.resolve() != py_file.resolve():
        print(f"  COLLISION: {py_file.name} already exists in {category}/ — skipping")
        skipped_no_classification.append(str(py_file.relative_to(REPO_ROOT)))
        continue

    try:
        original_path = py_file
        shutil.move(str(py_file), str(target_path))
        rollback_log.append((target_path, original_path))
        moves_performed.append(
            {
                "module": py_file.name,
                "from": str(original_path.relative_to(REPO_ROOT)),
                "to": str(target_path.relative_to(REPO_ROOT)),
            }
        )
        print(f"  MOVE: {py_file.name:45s} → {category}/")
    except Exception as e:
        print(f"  ERROR moving {py_file}: {e}")
        rollback_all()
        failure_report = {
            "status": "FAILED",
            "error": str(e),
            "failed_file": str(py_file),
            "moves_before_failure": len(moves_performed),
        }
        fail_path = APP_FUNC_DIR / "reorganization_failure.json"
        with open(fail_path, "w") as ff:
            json.dump(failure_report, ff, indent=2)
        print(f"  Failure report written to: {fail_path}")
        sys.exit(1)

# ── Step 6 — External Blueprints detection ────────────────────────────────────
print()
print("=== STEP 6: EXTERNAL BLUEPRINT DETECTION ===")

external_blueprint_stems: list[str] = []
for stem, paths in stem_to_recorded_paths.items():
    for rpath in paths:
        if rpath.startswith("Blueprints"):
            external_blueprint_stems.append(stem)
            break

external_blueprint_count = len(external_blueprint_stems)
print(f"  External blueprint modules (not moved): {external_blueprint_count}")

# ── Step 7 — Category counts in final layout ──────────────────────────────────
print()
print("=== STEP 7: FINAL CATEGORY COUNTS ===")

category_counts: dict[str, int] = {}
for cat in CATEGORIES:
    count = len(list((APP_FUNC_DIR / cat).glob("*.py")))
    category_counts[cat] = count
    print(f"  {cat:12s}: {count} modules")

# ── Step 8 — Write report ─────────────────────────────────────────────────────
print()
print("=== STEP 8: WRITE REPORT ===")

report = {
    "modules_scanned": len(all_py_files),
    "moves_performed": len(moves_performed),
    "skipped_already_correct": skipped_already_correct,
    "skipped_no_classification": len(skipped_no_classification),
    "external_blueprint_modules": external_blueprint_count,
    "category_counts": category_counts,
    "moves": moves_performed,
    "no_classification": skipped_no_classification,
}

with open(REPORT_FILE, "w") as rf:
    json.dump(report, rf, indent=2)

print(f"  Written: {REPORT_FILE.relative_to(REPO_ROOT)}")

# ── Step 9 — Validation ───────────────────────────────────────────────────────
print()
print("=== STEP 9: VALIDATION ===")

final_files = list(APP_FUNC_DIR.rglob("*.py"))
final_filenames = {f.name for f in final_files}
original_filenames = {f.name for f in all_py_files}

deleted = original_filenames - final_filenames
renamed = set()  # move-only, filenames preserved by design

if deleted:
    print(f"  WARNING: {len(deleted)} filenames disappeared: {deleted}")
else:
    print("  No files deleted. ✓")

if len(final_filenames) >= len(original_filenames):
    print(f"  File count OK: {len(original_filenames)} → {len(final_files)} ✓")
else:
    print(f"  WARNING: count dropped {len(original_filenames)} → {len(final_files)}")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("REORGANIZATION COMPLETE")
print(f"  Modules scanned:         {len(all_py_files)}")
print(f"  Moves performed:         {len(moves_performed)}")
print(f"  Already correct:         {skipped_already_correct}")
print(f"  No classification found: {len(skipped_no_classification)}")
print(f"  External blueprint mods: {external_blueprint_count}")
print("=" * 60)

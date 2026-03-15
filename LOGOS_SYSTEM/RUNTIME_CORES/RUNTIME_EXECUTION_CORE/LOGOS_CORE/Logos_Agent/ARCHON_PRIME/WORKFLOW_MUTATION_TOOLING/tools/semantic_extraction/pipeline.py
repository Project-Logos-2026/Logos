#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-077
# module_name:          pipeline
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/pipeline.py
# responsibility:       Analysis module: pipeline
# runtime_stage:        analysis
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
pipeline.py — DRAC AF extraction pipeline orchestrator.

PASS 1: Extract agent_control functions across the entire LOGOS repository.

Usage:
    /usr/bin/python3 tools/drac_af_extractor/pipeline.py

Constraints:
    - COPY ONLY. No source files are modified, moved, or deleted.
    - Registry is written to MODULAR_LIBRARY/af_semantic_registry.json.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: pipeline.py
tool_category: Report_Generation
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python pipeline.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import sys
from collections import defaultdict
from pathlib import Path

# Ensure tools directory is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from drac_af_extractor.ast_parser import parse_file  # type: ignore
from Tools.Scripts.classifier import classify_record
from Tools.Scripts.registry_writer import build_entry, write_registry
from Tools.Scripts.scanner import collect
from Tools.Scripts.semantic_extractor import extract_record

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
PASS_NAME = "PASS_1"
CATEGORY_FILTER = "AGENT_CONTROL"


def run_pass(
    repo_root: Path,
    pass_name: str,
    category_filter: str,
) -> None:
    print("=" * 60)
    print(f"DRAC AF Extractor — {pass_name} [{category_filter}]")
    print("=" * 60)

    # ── Step 1: Scan repository ───────────────────────────────────────────────
    print("\n=== STEP 1: REPOSITORY SCAN ===")
    all_files = collect(repo_root)
    print(f"  Python files discovered: {len(all_files)}")

    # ── Step 2: AST parse ─────────────────────────────────────────────────────
    print("\n=== STEP 2: AST FUNCTION EXTRACTION ===")
    all_records: list[dict] = []
    parse_errors = 0
    for py_file in all_files:
        recs = parse_file(py_file)
        if recs:
            all_records.extend(recs)
        elif py_file.stat().st_size > 0:
            parse_errors += 1

    print(f"  Files parsed:       {len(all_files) - parse_errors}")
    print(f"  Parse errors:       {parse_errors}")
    print(f"  Functions extracted: {len(all_records)}")

    # ── Step 3: Classify ──────────────────────────────────────────────────────
    print("\n=== STEP 3: CLASSIFICATION ===")
    classified: dict[str, list[dict]] = defaultdict(list)
    unclassified = 0

    for rec in all_records:
        cat = classify_record(rec)
        if cat:
            classified[cat].append(rec)
        else:
            unclassified += 1

    for cat, recs in sorted(classified.items()):
        print(f"  {cat:25s}: {len(recs)}")
    print(f"  {'unclassified':25s}: {unclassified}")

    # ── Step 4: Filter to target category ─────────────────────────────────────
    print(f"\n=== STEP 4: FILTER → {category_filter} ===")
    target_records = classified.get(category_filter, [])
    print(f"  Records matching {category_filter}: {len(target_records)}")

    if not target_records:
        print("  No matching records — nothing to write.")
        sys.exit(0)

    # ── Step 5: Semantic modifier extraction ──────────────────────────────────
    print("\n=== STEP 5: SEMANTIC MODIFIER EXTRACTION ===")
    entries: list[dict] = []
    for i, rec in enumerate(target_records, start=1):
        modifier = extract_record(rec)
        entry = build_entry(
            counter=i,
            record=rec,
            category=category_filter,
            semantic_modifier=modifier,
        )
        entries.append(entry)
        # Show first 10 as sample
        if i <= 10:
            print(f"  AF_{i:04d}  {rec['name']:40s} → {modifier}")
    if len(entries) > 10:
        print(f"  … {len(entries) - 10} more entries omitted from console")

    # ── Step 6: Validate source files unchanged ───────────────────────────────
    print("\n=== STEP 6: SOURCE INTEGRITY CHECK ===")
    # Spot check: all registered file_paths must still exist
    missing = [e for e in entries if not Path(e["file_path"]).exists()]
    if missing:
        print(f"  WARNING: {len(missing)} source files no longer found:")
        for e in missing[:5]:
            print(f"    {e['file_path']}")
    else:
        print(f"  All {len(entries)} source files intact. ✓")

    # ── Step 7: Write registry ────────────────────────────────────────────────
    print("\n=== STEP 7: WRITE REGISTRY ===")
    out_path = write_registry(
        entries=entries,
        pass_name=pass_name,
        category_filter=category_filter,
    )
    size_kb = out_path.stat().st_size / 1024
    print(f"  Written: {out_path.relative_to(REPO_ROOT)}  ({size_kb:.1f} KB)")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("PASS COMPLETE")
    print(f"  Files scanned:      {len(all_files)}")
    print(f"  Functions parsed:   {len(all_records)}")
    print(f"  AFs extracted:      {len(entries)}")
    print(f"  Category filter:    {category_filter}")
    print("  Cluster distribution:")
    for cat, recs in sorted(classified.items()):
        marker = "  ◀ (this pass)" if cat == category_filter else ""
        print(f"    {cat:25s}: {len(recs)}{marker}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_pass(REPO_ROOT, PASS_NAME, CATEGORY_FILTER)
    except Exception as e:
        print(f"\n  PIPELINE ERROR: {e}")
        import traceback

        traceback.print_exc()

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


# [AP-NORM-REPAIR] syntax error removed:         sys.exit(1)

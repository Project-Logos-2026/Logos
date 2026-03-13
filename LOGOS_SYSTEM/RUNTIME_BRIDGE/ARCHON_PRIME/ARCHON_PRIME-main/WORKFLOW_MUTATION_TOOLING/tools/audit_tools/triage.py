#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-047
# module_name:          triage
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/triage.py
# responsibility:       Inspection module: triage
# runtime_stage:        audit
# execution_entry:      run
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
ARCHON PRIME — Legacy Module Triage and Extraction
Classifies, moves, deduplicates, and cleans up staging modules.
Writes JSON reports and markdown summary.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: triage.py
tool_category: Repo_Audit
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python triage.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import difflib
import json
import shutil
from collections import defaultdict
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


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

SOURCE_DIR = Path(
    "/workspaces/ARCHON_PRIME/WORKFLOW_TARGET_PROCESSING/INCOMING_TARGETS/TARGETS"
)
DEST_REASON = Path("/workspaces/ARCHON_PRIME/WORKFLOW_TARGET_PROCESSING/COMPLETED")
DEST_UTILS = Path("/workspaces/ARCHON_PRIME/WORKFLOW_TARGET_PROCESSING/COMPLETED")
TOOLS_DIR = Path("/workspaces/ARCHON_PRIME/WORKFLOW_MUTATION_TOOLING/tools")

EXCLUDE_STEMS = {"test", "audit", "nexus", "boot"}

REASONING_SIGNALS = {
    "infer",
    "deduce",
    "abduct",
    "reason",
    "logic",
    "proof",
    "evaluate",
    "semantic",
    "ontology",
    "privation",
    "fractal",
    "pxl",
    "conscious",
    "cognition",
    "agent",
    "bayesian",
    "probability",
    "predict",
    "analysis",
    "transformer",
    "translation",
}

UTILITY_SIGNALS = {
    "schema",
    "config",
    "loader",
    "registry",
    "adapter",
    "parser",
    "serializer",
    "logging",
    "filesystem",
    "wrapper",
    "helper",
    "tools",
    "utility",
}

# Similarity threshold for duplicate detection
SIMILARITY_THRESHOLD = 0.90

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------


def should_exclude(path: Path) -> bool:
    stem = path.stem.lower()
    return any(e in stem for e in EXCLUDE_STEMS)


def read_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def try_parse(source: str, path: Path):
    try:
        return ast.parse(source, filename=str(path))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# STEP 3 — STUB DETECTION
# ---------------------------------------------------------------------------


def is_stub(path: Path, source: str, tree) -> tuple[bool, str]:
    """Return (is_stub, reason)."""
    stripped = source.strip()

    # Empty file
    if not stripped:
        return True, "empty file"

    # Only comments / docstrings — no code
    non_comment_lines = [
        ln
        for ln in stripped.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not non_comment_lines:
        return True, "only comment lines"

    if tree is None:
        # Can't parse — not a stub, partial content
        return False, ""

    # Collect all function and class defs
    functions = [
        n
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    if not functions and not classes:
        # Check if there are any expressions (non-trivial)
        expressions = [
            n
            for n in ast.walk(tree)
            if isinstance(
                n, (ast.Assign, ast.AnnAssign, ast.Expr, ast.Import, ast.ImportFrom)
            )
        ]
        if len(expressions) <= 3:
            return True, "no callables and minimal content"

    # Check if ALL function bodies are only pass / NotImplementedError / docstring
    stub_bodies = 0
    for fn in functions:
        body_nodes = [n for n in fn.body if not isinstance(n, ast.Expr)]
        if not body_nodes:
            stub_bodies += 1
            continue
        all_pass = all(isinstance(n, ast.Pass) for n in body_nodes)
        all_raise = all(
            isinstance(n, ast.Raise)
            and (
                n.exc is None
                or (
                    isinstance(n.exc, ast.Call)
                    and isinstance(n.exc.func, ast.Name)
                    and n.exc.func.id == "NotImplementedError"
                )
            )
            for n in body_nodes
        )
        if all_pass or all_raise:
            stub_bodies += 1

    if functions and stub_bodies == len(functions):
        return (
            True,
            f"all {len(functions)} function(s) are stub bodies (pass/NotImplementedError)",
        )

    # Check for explicit NotImplementedError at module level
    for node in ast.walk(tree):
        if isinstance(node, ast.Raise) and node.exc:
            if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                if node.exc.func.id == "NotImplementedError":
                    if not functions and not classes:
                        return (
                            True,
                            "module-level NotImplementedError with no callables",
                        )

    return False, ""


# ---------------------------------------------------------------------------
# STEP 4+5 — CLASSIFICATION
# ---------------------------------------------------------------------------


def score_signals(text: str, signals: set) -> int:
    lower = text.lower()
    return sum(1 for s in signals if s in lower)


def classify_module(path: Path, source: str, tree) -> str:
    """Returns 'REASONING', 'UTILITY', or 'UNCLASSIFIED'."""
    combined = path.stem.lower() + " " + source[:3000].lower()

    r_score = score_signals(combined, REASONING_SIGNALS)
    u_score = score_signals(combined, UTILITY_SIGNALS)

    if r_score == 0 and u_score == 0:
        return "UNCLASSIFIED"
    if r_score >= u_score:
        return "REASONING"
    return "UTILITY"


# ---------------------------------------------------------------------------
# STEP 6 — DUPLICATE DETECTION
# ---------------------------------------------------------------------------


def function_names(tree) -> frozenset:
    if tree is None:
        return frozenset()
    return frozenset(
        n.name
        for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )


def line_similarity(src_a: str, src_b: str) -> float:
    lines_a = src_a.splitlines()
    lines_b = src_b.splitlines()
    matcher = difflib.SequenceMatcher(None, lines_a, lines_b)
    return matcher.ratio()


def find_duplicates(classified: list[dict]) -> list[dict]:
    """
    Within each destination group (REASONING / UTILITY), compare pairs.
    Return list of duplicates to delete (keep the longer/more complete version).
    """
    by_class = defaultdict(list)
    for entry in classified:
        by_class[entry["classification"]].append(entry)

    to_delete = []
    seen_pairs = set()

    for _, entries in by_class.items():
        for i, a in enumerate(entries):
            for j, b in enumerate(entries):
                if i >= j:
                    continue
                pair_key = tuple(sorted([a["path"], b["path"]]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                # Compare function name sets
                fn_a = a["function_names"]
                fn_b = b["function_names"]
                if not fn_a and not fn_b:
                    continue

                # Jaccard similarity of function names
                if fn_a or fn_b:
                    union = fn_a | fn_b
                    intersect = fn_a & fn_b
                    fn_sim = len(intersect) / len(union) if union else 0.0
                else:
                    fn_sim = 0.0

                # Line similarity (only if function sim is high enough to be worth computing)
                line_sim = 0.0
                if fn_sim > 0.6:
                    line_sim = line_similarity(a["source"], b["source"])

                is_dup = (
                    fn_sim >= SIMILARITY_THRESHOLD or line_sim >= SIMILARITY_THRESHOLD
                )

                if is_dup:
                    # Keep the longer (more complete) file
                    victim = a if len(a["source"]) <= len(b["source"]) else b
                    keeper = b if victim is a else a
                    to_delete.append(
                        {
                            "path": victim["path"],
                            "reason": "duplicate",
                            "duplicate_of": keeper["path"],
                            "fn_similarity": round(fn_sim, 3),
                            "line_similarity": round(line_sim, 3),
                        }
                    )

    return to_delete


# ---------------------------------------------------------------------------
# STEP 7 — STUB detection for empty __init__.py
# ---------------------------------------------------------------------------


def is_empty_init(path: Path, source: str) -> bool:
    if path.name != "__init__.py":
        return False
    stripped = source.strip()
    if not stripped:
        return True
    # Only comments/docstrings
    non_comment = [
        ln
        for ln in stripped.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    # Check if the only non-comment content is a docstring
    if not non_comment:
        return True
    # Strip triple-quoted docstring content
    # Parse and see if there are any actual imports or definitions
    tree = try_parse(source, path)
    if tree is None:
        return False
    for node in tree.body:
        if not isinstance(node, ast.Expr):
            return False
    return True


# ---------------------------------------------------------------------------
# SAFE MOVE with collision handling
# ---------------------------------------------------------------------------


def safe_move(src: Path, dest_dir: Path) -> Path:
    dest = dest_dir / src.name
    if dest.exists():
        # Avoid collision: prefix with source subdirectory name
        subdir = src.parent.name
        dest = dest_dir / f"{subdir}__{src.name}"
    shutil.move(str(src), str(dest))
    return dest


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------


def run():
    print("=" * 60)
    print("ARCHON PRIME — Legacy Module Triage and Extraction")
    print("=" * 60)

    # Step 1 — Create directories
    print("\n=== STEP 1: DIRECTORY PREPARATION ===")
    DEST_REASON.mkdir(parents=True, exist_ok=True)
    DEST_UTILS.mkdir(parents=True, exist_ok=True)
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  {DEST_REASON}")
    print(f"  {DEST_UTILS}")

    # Step 2 — Module scan
    print("\n=== STEP 2: MODULE SCAN ===")
    all_py = sorted(SOURCE_DIR.rglob("*.py"))
    all_py = [p for p in all_py if "__pycache__" not in p.parts]
    candidates = [p for p in all_py if not should_exclude(p)]
    excluded = [p for p in all_py if should_exclude(p)]
    print(f"  Total Python files: {len(all_py)}")
    print(f"  Excluded (test/audit/nexus/boot): {len(excluded)}")
    print(f"  Candidates: {len(candidates)}")

    # Steps 3+4+5 — Stub detection + classification
    print("\n=== STEPS 3–5: STUB DETECTION + CLASSIFICATION ===")

    classified = []
    stubs = []
    empty_inits = []
    unclassified_kept = []

    for p in candidates:
        source = read_source(p)
        tree = try_parse(source, p)

        # Empty init check first
        if is_empty_init(p, source):
            empty_inits.append(
                {
                    "path": str(p.relative_to(SOURCE_DIR)),
                    "absolute": str(p),
                    "reason": "empty __init__.py",
                }
            )
            continue

        # Stub check
        stub_flag, stub_reason = is_stub(p, source, tree)
        if stub_flag:
            stubs.append(
                {
                    "path": str(p.relative_to(SOURCE_DIR)),
                    "absolute": str(p),
                    "reason": stub_reason,
                }
            )
            continue

        # Classify
        cls = classify_module(p, source, tree)
        fn_names = function_names(tree)

        entry = {
            "path": str(p.relative_to(SOURCE_DIR)),
            "absolute": str(p),
            "classification": cls,
            "source": source,
            "function_names": fn_names,
            "size_bytes": len(source.encode("utf-8")),
            "line_count": len(source.splitlines()),
        }

        if cls in ("REASONING", "UTILITY"):
            classified.append(entry)
        else:
            # UNCLASSIFIED — keep but don't move
            unclassified_kept.append(entry)

    print(f"  Empty __init__.py files: {len(empty_inits)}")
    print(f"  Stub modules: {len(stubs)}")
    reasoning_entries = [e for e in classified if e["classification"] == "REASONING"]
    utility_entries = [e for e in classified if e["classification"] == "UTILITY"]
    print(f"  REASONING modules: {len(reasoning_entries)}")
    print(f"  UTILITY modules:   {len(utility_entries)}")
    print(f"  UNCLASSIFIED (not moved): {len(unclassified_kept)}")

    # Step 6 — Duplicate detection (before moving)
    print("\n=== STEP 6: DUPLICATE DETECTION ===")
    duplicates = find_duplicates(classified)
    dup_paths = {d["path"] for d in duplicates}
    print(f"  Duplicates detected: {len(duplicates)}")

    # Remove duplicates from classified before moving
    classified_deduped = [e for e in classified if e["path"] not in dup_paths]
    reasoning_move = [
        e for e in classified_deduped if e["classification"] == "REASONING"
    ]
    utility_move = [e for e in classified_deduped if e["classification"] == "UTILITY"]

    # Step 4 — Move reasoning modules
    print("\n=== STEP 4: MOVING REASONING MODULES ===")
    reasoning_moved = []
    for entry in reasoning_move:
        src_path = Path(entry["absolute"])
        dest_path = safe_move(src_path, DEST_REASON)
        reasoning_moved.append(
            {
                "module_name": src_path.name,
                "source_path": entry["path"],
                "destination_path": str(
                    dest_path.relative_to(Path("/workspaces/ARCHON_PRIME"))
                ),
                "size_bytes": entry["size_bytes"],
                "line_count": entry["line_count"],
            }
        )
    print(f"  Moved: {len(reasoning_moved)}")

    # Step 5 — Move utility modules
    print("\n=== STEP 5: MOVING UTILITY MODULES ===")
    utility_moved = []
    for entry in utility_move:
        src_path = Path(entry["absolute"])
        if not src_path.exists():
            continue  # already moved (edge case)
        dest_path = safe_move(src_path, DEST_UTILS)
        utility_moved.append(
            {
                "module_name": src_path.name,
                "source_path": entry["path"],
                "destination_path": str(
                    dest_path.relative_to(Path("/workspaces/ARCHON_PRIME"))
                ),
                "size_bytes": entry["size_bytes"],
                "line_count": entry["line_count"],
            }
        )
    print(f"  Moved: {len(utility_moved)}")

    # Step 7 — Cleanup pass
    print("\n=== STEP 7: CLEANUP PASS ===")
    deleted_records = []

    # Delete stubs
    for s in stubs:
        p = Path(s["absolute"])
        if p.exists():
            p.unlink()
            deleted_records.append(
                {
                    "path": s["path"],
                    "reason": s["reason"],
                    "category": "stub",
                }
            )

    # Delete empty inits
    for ei in empty_inits:
        p = Path(ei["absolute"])
        if p.exists():
            p.unlink()
            deleted_records.append(
                {
                    "path": ei["path"],
                    "reason": "empty __init__.py",
                    "category": "empty_init",
                }
            )

    # Delete duplicate victims
    for dup in duplicates:
        p = Path(dup["absolute"]) if "absolute" in dup else SOURCE_DIR / dup["path"]
        if p.exists():
            p.unlink()
            deleted_records.append(
                {
                    "path": dup["path"],
                    "reason": f"duplicate of {dup['duplicate_of']} (fn_sim={dup['fn_similarity']},"
                    f" line_sim={dup['line_similarity']})",
                    "category": "duplicate",
                }
            )

    # Delete __pycache__ directories
    pycache_count = 0
    for pycache_dir in SOURCE_DIR.rglob("__pycache__"):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir)
            pycache_count += 1
    print(f"  __pycache__ directories removed: {pycache_count}")

    # Delete *.pyc files
    pyc_count = 0
    for pyc in SOURCE_DIR.rglob("*.pyc"):
        try:
            pyc.unlink()
            pyc_count += 1
        except Exception:
            pass
    print(f"  *.pyc files removed: {pyc_count}")

    print(f"  Stub/duplicate/empty file records: {len(deleted_records)}")

    # Step 8 — Write JSON reports
    print("\n=== STEP 8: WRITING JSON REPORTS ===")

    summary = {
        "generated": "2026-03-10",
        "source_directory": str(SOURCE_DIR),
        "total_python_files_found": len(all_py),
        "excluded_by_rule": len(excluded),
        "candidates_scanned": len(candidates),
        "stubs_detected": len(stubs),
        "empty_inits_detected": len(empty_inits),
        "duplicates_detected": len(duplicates),
        "reasoning_modules_moved": len(reasoning_moved),
        "utility_modules_moved": len(utility_moved),
        "modules_deleted": len(deleted_records),
        "pycache_dirs_removed": pycache_count,
        "pyc_files_removed": pyc_count,
        "unclassified_remaining": len(unclassified_kept),
    }

    (TOOLS_DIR / "module_extraction_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("  module_extraction_summary.json")

    (TOOLS_DIR / "reasoning_modules_moved.json").write_text(
        json.dumps(reasoning_moved, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  reasoning_modules_moved.json ({len(reasoning_moved)} entries)")

    (TOOLS_DIR / "utility_modules_moved.json").write_text(
        json.dumps(utility_moved, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  utility_modules_moved.json ({len(utility_moved)} entries)")

    deleted_out = deleted_records + [
        {
            "path": str(p.relative_to(SOURCE_DIR)),
            "reason": "excluded by rule",
            "category": "excluded",
        }
        for p in excluded
    ]
    (TOOLS_DIR / "modules_deleted.json").write_text(
        json.dumps(deleted_out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  modules_deleted.json ({len(deleted_out)} entries)")

    # Step 9 — Final report
    print("\n=== STEP 9: FINAL REPORT ===")
    _write_report(
        summary,
        reasoning_moved,
        utility_moved,
        deleted_records,
        duplicates,
        unclassified_kept,
        excluded,
    )

    print("\n" + "=" * 60)
    print("TRIAGE COMPLETE")
    print(f"  Reasoning extracted: {len(reasoning_moved)}")
    print(f"  Utility extracted:   {len(utility_moved)}")
    print(f"  Files deleted:       {len(deleted_records)}")
    print(f"  Duplicates removed:  {len(duplicates)}")
    print("=" * 60)


def _write_report(
    summary,
    reasoning_moved,
    utility_moved,
    deleted_records,
    duplicates,
    unclassified_kept,
    excluded,
):
    stub_count = sum(1 for d in deleted_records if d["category"] == "stub")
    empty_count = sum(1 for d in deleted_records if d["category"] == "empty_init")
    dup_count = sum(1 for d in deleted_records if d["category"] == "duplicate")

    # Top reasoning modules by line count
    top_reasoning = sorted(reasoning_moved, key=lambda x: -x["line_count"])[:10]
    top_utility = sorted(utility_moved, key=lambda x: -x["line_count"])[:10]

    lines = [
        "# ARCHON PRIME — Module Triage Report",
        "**Generated:** 2026-03-10  ",
        "**Source:** `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`  ",
        "**Destinations:** `Blueprints/reasoning`, `Blueprints/utils`  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Python files scanned | {summary['total_python_files_found']} |",
        f"| Excluded by rule (test/audit/nexus/boot) | {summary['excluded_by_rule']} |",
        f"| Candidates analyzed | {summary['candidates_scanned']} |",
        f"| **Reasoning modules extracted** | **{summary['reasoning_modules_moved']}** |",
        f"| **Utility modules extracted** | **{summary['utility_modules_moved']}** |",
        f"| Stub modules deleted | {stub_count} |",
        f"| Empty `__init__.py` deleted | {empty_count} |",
        f"| Duplicates removed | {dup_count} |",
        f"| Total files deleted | {summary['modules_deleted']} |",
        f"| `__pycache__` directories removed | {summary['pycache_dirs_removed']} |",
        f"| `*.pyc` files removed | {summary['pyc_files_removed']} |",
        f"| Unclassified (remaining in source) | {summary['unclassified_remaining']} |",
        "",
        "---",
        "",
        "## Reasoning Modules Extracted",
        f"**Destination:** `Blueprints/reasoning/`  **Total:** {len(reasoning_moved)}",
        "",
        "| Module | Lines | Source |",
        "|--------|-------|--------|",
    ]
    for m in top_reasoning:
        lines.append(
            f"| `{m['module_name']}` | {m['line_count']} | `{m['source_path']}` |"
        )
    if len(reasoning_moved) > 10:
        lines.append(
            f"| _(+{len(reasoning_moved) - 10} more — see `reasoning_modules_moved.json`)_ | | |"
        )

    lines += [
        "",
        "---",
        "",
        "## Utility Modules Extracted",
        f"**Destination:** `Blueprints/utils/`  **Total:** {len(utility_moved)}",
        "",
        "| Module | Lines | Source |",
        "|--------|-------|--------|",
    ]
    for m in top_utility:
        lines.append(
            f"| `{m['module_name']}` | {m['line_count']} | `{m['source_path']}` |"
        )
    if len(utility_moved) > 10:
        lines.append(
            f"| _(+{len(utility_moved) - 10} more — see `utility_modules_moved.json`)_ | | |"
        )

    lines += [
        "",
        "---",
        "",
        "## Duplicates Removed",
        f"**Total:** {len(duplicates)}",
        "",
        "| Victim Module | Kept As | Fn Similarity | Line Similarity |",
        "|--------------|---------|--------------|----------------|",
    ]
    for d in duplicates[:20]:
        victim = Path(d["path"]).name
        keeper = Path(d["duplicate_of"]).name
        lines.append(
            f"| `{victim}` | `{keeper}` | {d['fn_similarity']} | {d['line_similarity']} |"
        )
    if len(duplicates) > 20:
        lines.append(
            f"_+{len(duplicates) - 20} more duplicates — see `modules_deleted.json`_"
        )

    lines += [
        "",
        "---",
        "",
        "## Stub Deletions",
        f"**Total:** {stub_count + empty_count}",
        "",
        "| Module | Reason |",
        "|--------|--------|",
    ]
    for d in deleted_records:
        if d["category"] in ("stub", "empty_init"):
            lines.append(f"| `{Path(d['path']).name}` | {d['reason']} |")

    lines += [
        "",
        "---",
        "",
        "## Output Artifacts",
        "",
        "| File | Description |",
        "|------|-------------|",
        "| `Tools/module_extraction_summary.json` | Aggregate metrics |",
        "| `Tools/reasoning_modules_moved.json` | All reasoning modules with source/dest paths |",
        "| `Tools/utility_modules_moved.json` | All utility modules with source/dest paths |",
        "| `Tools/modules_deleted.json` | All deleted files with deletion reason |",
        "| `Tools/module_triage_report.md` | This report |",
        "",
        "---",
        "",
        "## Governance Note",
        "",
        "No changes were made to the live runtime stack (`LOGOS_SYSTEM/`, `STARTUP/`).  ",
        "All operations were scoped to `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`.  ",
        "Extracted modules in `Blueprints/reasoning/` and `Blueprints/utils/` are candidates;",
        "integration into live subsystems requires a separate governance-approved pass.",
    ]

    report = "\n".join(lines)
    (TOOLS_DIR / "module_triage_report.md").write_text(report, encoding="utf-8")
    print(f"  Written: {TOOLS_DIR / 'module_triage_report.md'}")


if __name__ == "__main__":
    run()

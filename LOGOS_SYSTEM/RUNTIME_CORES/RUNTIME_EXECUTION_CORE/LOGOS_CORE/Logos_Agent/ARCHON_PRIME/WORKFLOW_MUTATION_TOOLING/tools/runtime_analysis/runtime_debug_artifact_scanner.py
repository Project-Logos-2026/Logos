# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-068
# module_name:          runtime_debug_artifact_scanner
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/runtime_analysis/runtime_debug_artifact_scanner.py
# responsibility:       Analysis module: runtime debug artifact scanner
# runtime_stage:        validation
# execution_entry:      main
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
RUNTIME_TOOL_METADATA
---------------------

tool_name: runtime_debug_artifact_scanner.py
tool_category: Runtime_Diagnostics
tool_subcategory: debug_artifact_detection

purpose:
Scans specified directories for debug artifacts: print() calls, TODO comments,
and bare assert statements. Compares against an optional stored inventory to
report delta (new artifacts introduced since last scan).

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python runtime_debug_artifact_scanner.py --scan-dirs STARTUP LOGOS_SYSTEM

output_artifacts:
debug_artifact_scan.json

dependencies:
ast, pathlib, json, argparse, re

safety_classification:
READ_ONLY
"""

import argparse
import json
import re
from pathlib import Path

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


PATTERNS = {
    "print_call": re.compile(r"\bprint\s*\("),
    "todo_comment": re.compile(r"#.*\bTODO\b", re.IGNORECASE),
    "bare_assert": re.compile(r"^\s*assert\b"),
}


def scan_file(filepath: Path, repo_root: Path) -> dict:
    """Scan a single file for debug artifacts."""
    findings: dict[str, list[int]] = {k: [] for k in PATTERNS}
    try:
        lines = filepath.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {
            "path": str(filepath.relative_to(repo_root)),
            "error": "unreadable",
            **{k: [] for k in PATTERNS},
        }

    for i, line in enumerate(lines, start=1):
        for artifact, pattern in PATTERNS.items():
            if pattern.search(line):
                findings[artifact].append(i)

    total = sum(len(v) for v in findings.values())
    return {
        "path": str(filepath.relative_to(repo_root)),
        "total_artifacts": total,
        **findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scanner for runtime debug artifacts (print, TODO, assert)."
    )
    parser.add_argument(
        "--scan-dirs",
        nargs="+",
        required=True,
        help="One or more directories to scan, relative to repo root.",
    )
    parser.add_argument(
        "--inventory",
        default=None,
        help="Optional path to a previous scan JSON for delta comparison.",
    )
    parser.add_argument(
        "--pattern",
        nargs="*",
        choices=list(PATTERNS.keys()),
        default=list(PATTERNS.keys()),
        help="Artifact types to search for (default: all).",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/ARCHON_PRIME",
        help="Repository root (default: /workspaces/ARCHON_PRIME).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    active_patterns = {k: v for k, v in PATTERNS.items() if k in args.pattern}

    files: list[Path] = []
    for scan_dir in args.scan_dirs:
        target = repo_root / scan_dir
        if not target.exists():
            print(f"  WARNING: scan dir not found: {target}")
            continue
        files.extend(sorted(target.rglob("*.py")))

    print(f"Scanning {len(files)} files for: {', '.join(active_patterns)}")

    results = []
    for f in files:
        rec = scan_file(f, repo_root)
        if rec.get("total_artifacts", 0) > 0:
            results.append(rec)

    # Delta comparison
    delta = None
    if args.inventory:
        try:
            prev = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
            prev_paths = {r["path"] for r in prev.get("findings", [])}
            curr_paths = {r["path"] for r in results}
            delta = {
                "new_files": sorted(curr_paths - prev_paths),
                "resolved_files": sorted(prev_paths - curr_paths),
            }
        except Exception as exc:
            delta = {"error": str(exc)}  # type: ignore[dict-item]

    total_artifacts = sum(r.get("total_artifacts", 0) for r in results)
    report = {
        "tool": "runtime_debug_artifact_scanner",
        "scan_dirs": args.scan_dirs,
        "files_with_artifacts": len(results),
        "total_artifacts": total_artifacts,
        "delta": delta,
        "findings": results,
    }
    write_report("debug_artifact_scan.json", report)
    print(
        f"Files with artifacts: {len(results)} | Total artifact instances: {total_artifacts}"
    )


if __name__ == "__main__":
    main()

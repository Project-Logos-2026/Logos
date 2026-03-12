"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: module_root_existence_checker.py
tool_category: Architecture_Validation
tool_subcategory: module_root_verification

purpose:
Takes a set of declared import root prefixes (from a classification or
violation report) and verifies whether each root actually exists as a
directory or __init__.py-bearing package on disk. Reports missing roots.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python module_root_existence_checker.py --input _Reports/import_violation_classification.json

output_artifacts:
module_root_existence.json

dependencies:
json, argparse, pathlib

safety_classification:
READ_ONLY
"""

import json
import argparse
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def check_root(root_name: str, scan_dirs: list[Path]) -> dict:
    """Check whether root_name resolves to a directory in any of scan_dirs."""
    candidates = []
    for base in scan_dirs:
        candidate = base / root_name
        if candidate.exists():
            has_init = (candidate / "__init__.py").exists()
            candidates.append({"path": str(candidate), "has_init": has_init})

    return {
        "root": root_name,
        "exists": bool(candidates),
        "locations": candidates,
    }


def extract_roots(data: dict) -> list[str]:
    """Extract root prefix names from various report formats."""
    # Try classification format: data["classification"]["by_root_prefix"]
    if "classification" in data:
        return list(data["classification"].get("by_root_prefix", {}).keys())
    # Try grouping format: data["groups"]
    if "groups" in data:
        return list(data["groups"].keys())
    # Try flat list of violations
    if "violations" in data:
        roots = set()
        for v in data["violations"]:
            module = v.get("module", "") or v.get("imported", "") or ""
            if module:
                roots.add(module.split(".")[0])
        return sorted(roots)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify that import root modules actually exist on disk."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to classification or grouping report JSON.",
    )
    parser.add_argument(
        "--scan-dirs",
        nargs="*",
        default=["/workspaces/Logos"],
        help="Base directories to search for roots (default: repo root).",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/Logos",
        help="Repository root (default: /workspaces/Logos).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    input_path = Path(args.input) if Path(args.input).is_absolute() else repo_root / args.input

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        raise SystemExit(1)

    scan_dirs = [Path(d).resolve() for d in args.scan_dirs]
    data = json.loads(input_path.read_text(encoding="utf-8"))
    roots = extract_roots(data)

    if not roots:
        print("WARNING: No root prefixes found in input file.")

    print(f"Checking {len(roots)} root prefixes against {len(scan_dirs)} search dir(s)...")
    results = [check_root(r, scan_dirs) for r in roots]

    present = [r for r in results if r["exists"]]
    missing = [r for r in results if not r["exists"]]

    report = {
        "tool": "module_root_existence_checker",
        "input": str(input_path),
        "total_roots_checked": len(roots),
        "present": len(present),
        "missing": len(missing),
        "results": results,
    }
    write_report("module_root_existence.json", report)
    print(f"Present: {len(present)} | Missing: {len(missing)}")
    if missing:
        print("  Missing roots:")
        for m in missing:
            print(f"    {m['root']}")


if __name__ == "__main__":
    main()

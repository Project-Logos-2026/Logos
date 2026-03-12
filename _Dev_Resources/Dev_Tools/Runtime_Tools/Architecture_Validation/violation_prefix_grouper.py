"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: violation_prefix_grouper.py
tool_category: Architecture_Validation
tool_subcategory: violation_prefix_grouping

purpose:
Groups import violations by N-segment prefix depth. Produces a distribution
report showing violation counts at each segment depth, identifying the
most impactful prefix patterns.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python violation_prefix_grouper.py --input _Reports/Import_Linter_Report.json --prefix-depth 3

output_artifacts:
violation_prefix_groups.json

dependencies:
json, argparse, pathlib, collections

safety_classification:
READ_ONLY
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def group_by_prefix_depth(violations: list[dict], depth: int) -> dict:
    """Group violations by a prefix of exactly `depth` dot-separated segments."""
    groups: dict[str, dict] = defaultdict(lambda: {"count": 0, "unique_files": set(), "sample_modules": []})

    for v in violations:
        module = v.get("module", "") or v.get("imported", "") or v.get("import", "") or ""
        file_ = v.get("file", "") or v.get("source_file", "") or ""
        parts = module.split(".")
        prefix = ".".join(parts[:depth]) if module else "unknown"

        groups[prefix]["count"] += 1
        if file_:
            groups[prefix]["unique_files"].add(file_)
        if len(groups[prefix]["sample_modules"]) < 3 and module not in groups[prefix]["sample_modules"]:
            groups[prefix]["sample_modules"].append(module)

    return {
        k: {
            "count": v["count"],
            "unique_files": len(v["unique_files"]),
            "sample_modules": v["sample_modules"],
        }
        for k, v in sorted(groups.items(), key=lambda x: -x[1]["count"])
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Group import violations by N-segment prefix depth."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to linter report JSON (relative to repo root or absolute).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override output filename (default: violation_prefix_groups.json).",
    )
    parser.add_argument(
        "--prefix-depth",
        type=int,
        default=3,
        help="Number of dot-segments to group by (default: 3).",
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

    data = json.loads(input_path.read_text(encoding="utf-8"))
    violations = data.get("violations", [])
    if not violations and isinstance(data, list):
        violations = data

    print(f"Grouping {len(violations)} violations at prefix depth={args.prefix_depth}...")
    groups = group_by_prefix_depth(violations, args.prefix_depth)

    report = {
        "tool": "violation_prefix_grouper",
        "input": str(input_path),
        "total_violations": len(violations),
        "prefix_depth": args.prefix_depth,
        "distinct_groups": len(groups),
        "groups": groups,
    }
    output_name = args.output or "violation_prefix_groups.json"
    write_report(output_name, report)
    print(f"Distinct {args.prefix_depth}-segment groups: {len(groups)}")
    for prefix, info in list(groups.items())[:10]:
        print(f"  {prefix}: {info['count']} violations")


if __name__ == "__main__":
    main()

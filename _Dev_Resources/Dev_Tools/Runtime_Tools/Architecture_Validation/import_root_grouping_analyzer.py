"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: import_root_grouping_analyzer.py
tool_category: Architecture_Validation
tool_subcategory: import_root_analysis

purpose:
Groups import violations from a linter report by root module prefix and
ranks by occurrence frequency. Accepts parameterized input path.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python import_root_grouping_analyzer.py --input _Reports/Import_Linter_Report.json

output_artifacts:
import_root_grouping.json

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


def group_by_root(violations: list[dict]) -> dict:
    """Group violations by the root (first segment) of the imported module."""
    groups: dict[str, dict] = defaultdict(lambda: {"count": 0, "files": set(), "samples": []})

    for v in violations:
        module = v.get("module", "") or v.get("imported", "") or v.get("import", "") or ""
        file_ = v.get("file", "") or v.get("source_file", "") or ""
        root = module.split(".")[0] if module else "unknown"

        groups[root]["count"] += 1
        if file_:
            groups[root]["files"].add(file_)
        if len(groups[root]["samples"]) < 5:
            groups[root]["samples"].append({"module": module, "file": file_})

    # Serialize
    result = {}
    for root, data in sorted(groups.items(), key=lambda x: -x[1]["count"]):
        result[root] = {
            "count": data["count"],
            "unique_files": len(data["files"]),
            "samples": data["samples"],
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Group import violations by root module prefix."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to linter report JSON (relative to repo root or absolute).",
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

    print(f"Grouping {len(violations)} violations by root prefix...")
    groups = group_by_root(violations)

    report = {
        "tool": "import_root_grouping_analyzer",
        "input": str(input_path),
        "total_violations": len(violations),
        "distinct_roots": len(groups),
        "groups": groups,
    }
    write_report("import_root_grouping.json", report)
    print(f"Distinct root prefixes: {len(groups)}")
    for root, info in list(groups.items())[:10]:
        print(f"  {root}: {info['count']} violations across {info['unique_files']} files")


if __name__ == "__main__":
    main()

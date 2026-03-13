# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-054
# module_name:          import_root_grouping_analyzer
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/import_analysis/import_root_grouping_analyzer.py
# responsibility:       Analysis module: import root grouping analyzer
# runtime_stage:        analysis
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

import argparse
import json
from collections import defaultdict
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


def group_by_root(violations: list[dict]) -> dict:
    """Group violations by the root (first segment) of the imported module."""
    groups: dict[str, dict] = defaultdict(
        lambda: {"count": 0, "files": set(), "samples": []}
    )

    for v in violations:
        module = (
            v.get("module", "") or v.get("imported", "") or v.get("import", "") or ""
        )
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
        default="/workspaces/ARCHON_PRIME",
        help="Repository root (default: /workspaces/ARCHON_PRIME).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    input_path = (
        Path(args.input) if Path(args.input).is_absolute() else repo_root / args.input
    )

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
        print(
            f"  {root}: {info['count']} violations across {info['unique_files']} files"
        )


if __name__ == "__main__":
    main()

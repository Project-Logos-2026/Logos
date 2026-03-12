"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: import_violation_classifier.py
tool_category: Architecture_Validation
tool_subcategory: import_linter_analysis

purpose:
Loads a linter artifact (Import_Linter_Report.json) and classifies each
violation by module root prefix, rule ID, and occurrence frequency.
Parameterizable via --input to accept any linter report.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python import_violation_classifier.py --input _Reports/Import_Linter_Report.json

output_artifacts:
import_violation_classification.json

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


def classify_violations(violations: list[dict]) -> dict:
    """Group violations by rule ID and by the root prefix of the imported module."""
    by_rule: dict[str, list] = defaultdict(list)
    by_prefix: dict[str, int] = defaultdict(int)
    by_file: dict[str, int] = defaultdict(int)

    for v in violations:
        rule = v.get("rule", "unknown")
        module = v.get("module", "") or v.get("imported", "") or ""
        file_ = v.get("file", "") or v.get("source_file", "") or ""

        by_rule[rule].append(v)
        root = module.split(".")[0] if module else "unknown"
        by_prefix[root] += 1
        if file_:
            by_file[file_] += 1

    return {
        "by_rule": {k: len(v) for k, v in by_rule.items()},
        "by_root_prefix": dict(sorted(by_prefix.items(), key=lambda x: -x[1])),
        "by_file": dict(sorted(by_file.items(), key=lambda x: -x[1])[:50]),
        "rule_details": {k: v for k, v in by_rule.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify import violations from a linter report by rule and prefix."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to Import_Linter_Report.json (relative to repo root or absolute).",
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
    if not violations and "violations" not in data:
        # Try flat list format
        violations = data if isinstance(data, list) else []

    print(f"Classifying {len(violations)} violations from: {input_path.name}")
    classification = classify_violations(violations)

    report = {
        "tool": "import_violation_classifier",
        "input": str(input_path),
        "total_violations": len(violations),
        "classification": classification,
    }
    write_report("import_violation_classification.json", report)
    print(f"Rules found: {list(classification['by_rule'].keys())}")
    print(f"Distinct root prefixes: {len(classification['by_root_prefix'])}")


if __name__ == "__main__":
    main()

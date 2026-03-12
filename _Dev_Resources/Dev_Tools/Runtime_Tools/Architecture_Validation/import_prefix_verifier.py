"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: import_prefix_verifier.py
tool_category: Architecture_Validation
tool_subcategory: import_prefix_analysis

purpose:
Reads a linter violation report and extracts the distribution of literal
import prefixes up to a configurable segment depth. Counts occurrences per
prefix to identify the most common non-canonical import patterns.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python import_prefix_verifier.py --input _Reports/Import_Linter_Report.json --max-segments 4

output_artifacts:
import_prefix_verification.json

dependencies:
json, argparse, pathlib, collections

safety_classification:
READ_ONLY
"""

import json
import argparse
from pathlib import Path
from collections import Counter

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def extract_prefix_distribution(violations: list[dict], max_segments: int) -> dict:
    """Build prefix frequency tables from 1 to max_segments depth."""
    distribution: dict[int, dict[str, int]] = {}

    for depth in range(1, max_segments + 1):
        counter: Counter = Counter()
        for v in violations:
            module = v.get("module", "") or v.get("imported", "") or v.get("import", "") or ""
            parts = module.split(".")
            prefix = ".".join(parts[:depth]) if len(parts) >= depth else module
            if prefix:
                counter[prefix] += 1
        distribution[depth] = dict(counter.most_common())

    return distribution


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract and count literal import prefixes from a linter violation report."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to linter report JSON (relative to repo root or absolute).",
    )
    parser.add_argument(
        "--max-segments",
        type=int,
        default=4,
        help="Maximum prefix depth in segments (default: 4).",
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

    print(f"Extracting prefixes (up to {args.max_segments} segments) from {len(violations)} violations...")
    distribution = extract_prefix_distribution(violations, args.max_segments)

    report = {
        "tool": "import_prefix_verifier",
        "input": str(input_path),
        "total_violations": len(violations),
        "max_segments": args.max_segments,
        "prefix_distribution": {str(k): v for k, v in distribution.items()},
    }
    write_report("import_prefix_verification.json", report)

    for depth, prefixes in distribution.items():
        top = list(prefixes.items())[:5]
        print(f"  Depth {depth} — top prefixes: {top}")


if __name__ == "__main__":
    main()

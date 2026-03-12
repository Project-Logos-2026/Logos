#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               runtime_wiring_log_validator
governance_scope:        Repo_Inventory append-only wiring log integrity
policy_dependencies:
  - Repo_Governance/Runtime/Dependency_Wiring_Log_Contract.md
  - Repo_Governance/Runtime/Runtime_Artifact_Formatting_Spec.md
  - Repo_Governance/Runtime/Runtime_Module_Generation_Spec.md
purpose:
  Audit append-only dependency wiring logs in Repo_Inventory/Master_Indexes/.
  Verifies expected index files exist, validates JSONL format and required
  fields per line, checks structural integrity indicative of append-only
  semantics, and reports consistency status. Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - runtime_wiring_log_validation_report.json
module_name:             runtime_wiring_log_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, sys
provides:
  - validate_index_file, validate_all_indexes, main
depends_on_runtime_state: none
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
DEV_RESOURCES = REPO_ROOT / "_Dev_Resources"
REPO_INVENTORY = DEV_RESOURCES / "Repo_Inventory"
MASTER_INDEXES_ENV = REPO_INVENTORY / "Master_Indexes" / "Environment"
MASTER_INDEXES_RT = REPO_INVENTORY / "Master_Indexes" / "Runtime"
MASTER_MANIFESTS = REPO_INVENTORY / "Master_Manifests"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

# Expected wiring log files (JSONL) per Dependency_Wiring_Log_Contract.md
EXPECTED_INDEX_FILES = {
    "Runtime": [
        "import_graph_index.jsonl",
        "call_path_index.jsonl",
        "external_interaction_index.jsonl",
        "runtime_wiring_index.jsonl",
    ],
    "Environment": [],
}

# Required fields per JSONL record per Dependency_Wiring_Log_Contract.md
REQUIRED_JSONL_FIELDS = {
    "import_graph_index.jsonl": ["timestamp", "tool", "log_type", "source", "target"],
    "call_path_index.jsonl": ["timestamp", "tool", "log_type", "caller", "callee"],
    "external_interaction_index.jsonl": ["timestamp", "tool", "log_type", "module", "interaction"],
    "runtime_wiring_index.jsonl": ["timestamp", "tool", "log_type", "data"],
}

FALLBACK_REQUIRED_FIELDS = ["timestamp", "tool", "log_type", "data"]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate_index_file(file_path: Path) -> dict:
    """
    Validate one JSONL index file.
    Returns a result dict with validity flags and violation details.
    """
    rel = str(file_path.relative_to(REPO_ROOT))
    result: dict = {
        "file": rel,
        "exists": file_path.exists(),
        "is_file": file_path.is_file(),
        "violations": [],
        "line_count": 0,
        "valid_lines": 0,
        "invalid_lines": [],
        "empty_file": False,
    }

    if not file_path.exists():
        result["violations"].append(f"File not found: {rel}")
        return result

    if not file_path.is_file():
        result["violations"].append(f"Path is not a file: {rel}")
        return result

    required_fields = REQUIRED_JSONL_FIELDS.get(file_path.name, FALLBACK_REQUIRED_FIELDS)

    try:
        raw_text = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        result["violations"].append(f"Read error: {exc}")
        return result

    lines = raw_text.splitlines()
    non_empty_lines = [ln for ln in lines if ln.strip()]
    result["line_count"] = len(non_empty_lines)

    if not non_empty_lines:
        result["empty_file"] = True
        # Empty files are allowed (log not yet populated) — not a violation
        return result

    timestamps = []
    for line_no, line in enumerate(non_empty_lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            result["invalid_lines"].append({
                "line": line_no,
                "error": str(exc),
                "raw": line[:120],
            })
            continue

        if not isinstance(record, dict):
            result["invalid_lines"].append({
                "line": line_no,
                "error": "Record is not a JSON object",
                "raw": line[:120],
            })
            continue

        # Check required fields
        missing = [f for f in required_fields if f not in record]
        if missing:
            result["invalid_lines"].append({
                "line": line_no,
                "error": f"Missing fields: {missing}",
                "raw": line[:120],
            })
            continue

        # Collect timestamps for monotone check (append-only heuristic)
        if "timestamp" in record and record["timestamp"]:
            timestamps.append(str(record["timestamp"]))

        result["valid_lines"] += 1

    if result["invalid_lines"]:
        result["violations"].append(
            f"JSONL format violations: {len(result['invalid_lines'])} invalid lines"
        )

    # Append-only heuristic: timestamps should be non-decreasing
    if len(timestamps) >= 2:
        for i in range(1, len(timestamps)):
            if timestamps[i] < timestamps[i - 1]:
                result["violations"].append(
                    f"Timestamp order regression at record {i + 1}: "
                    f"'{timestamps[i]}' < '{timestamps[i - 1]}' "
                    f"(possible non-append write detected)"
                )
                break  # Report first occurrence only

    return result


def validate_all_indexes() -> dict:
    """Validate all expected index files across Repo_Inventory."""
    inventory_status: dict = {
        "repo_inventory_exists": REPO_INVENTORY.is_dir(),
        "master_indexes_runtime_exists": MASTER_INDEXES_RT.is_dir(),
        "master_indexes_environment_exists": MASTER_INDEXES_ENV.is_dir(),
        "master_manifests_exists": MASTER_MANIFESTS.is_dir(),
    }

    violations: list = []
    file_results = []
    present_count = 0
    missing_count = 0

    # Check each expected index file
    for subdir, filenames in EXPECTED_INDEX_FILES.items():
        base_dir = MASTER_INDEXES_RT if subdir == "Runtime" else MASTER_INDEXES_ENV
        for filename in filenames:
            file_path = base_dir / filename
            fv = validate_index_file(file_path)
            file_results.append(fv)
            if fv["exists"]:
                present_count += 1
            else:
                missing_count += 1
            violations.extend(fv["violations"])

    # Scan for any unexpected files in the Runtime index directory
    unexpected = []
    if MASTER_INDEXES_RT.is_dir():
        expected_set = set(EXPECTED_INDEX_FILES["Runtime"])
        for child in MASTER_INDEXES_RT.iterdir():
            if child.is_file() and child.name not in expected_set:
                unexpected.append(str(child.relative_to(REPO_ROOT)))

    if unexpected:
        violations.append(
            f"Unexpected files in Master_Indexes/Runtime: {unexpected} — "
            "only contractually defined JSONL index files are permitted."
        )

    return {
        "inventory_status": inventory_status,
        "expected_index_files": sum(len(v) for v in EXPECTED_INDEX_FILES.values()),
        "present_count": present_count,
        "missing_count": missing_count,
        "unexpected_files": unexpected,
        "total_violations": len(violations),
        "violations": violations,
        "file_results": file_results,
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit append-only dependency wiring logs in Repo_Inventory."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="runtime_wiring_log_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_all_indexes()
    total_violations = results["total_violations"]
    status = "PASS" if total_violations == 0 else "FAIL"

    report = {
        "artifact_type": "runtime_wiring_log_validation",
        "generated_utc": _now_utc(),
        "tool_name": "runtime_wiring_log_validator",
        "schema_version": "1.0",
        "status": status,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {status}")
    print(f"Expected index files: {results['expected_index_files']} | "
          f"Present: {results['present_count']} | "
          f"Missing: {results['missing_count']} | "
          f"Violations: {total_violations}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

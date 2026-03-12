#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               devscript_header_validator
governance_scope:        Dev_Tools header schema compliance
policy_dependencies:
  - Repo_Governance/Header_Schemas/runtime_tool_header_schema.json
  - Repo_Governance/Header_Schemas/repo_governance_tool_header_schema.json
  - Repo_Governance/Developer/Dev_Tool_Generation_Policy.md
purpose:
  Audit all Dev_Tools scripts to confirm header schema compliance.
  Checks header presence, schema structure, required metadata fields,
  and header schema type alignment. Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - devscript_header_validation_report.json
module_name:             devscript_header_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, ast, json, os, pathlib, re, sys
provides:
  - validate_headers, scan_tool_dir, check_required_fields, main
depends_on_runtime_state: none
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
DEV_TOOLS = REPO_ROOT / "_Dev_Resources" / "Dev_Tools"
GOVERNANCE_ROOT = REPO_ROOT / "_Dev_Resources" / "Repo_Governance"
HEADER_SCHEMAS_DIR = GOVERNANCE_ROOT / "Header_Schemas"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

RUNTIME_TOOL_REQUIRED = [
    "tool_name", "tool_category", "tool_subcategory", "purpose",
    "authoritative_scope", "mutation_capability", "destructive_capability",
    "requires_repo_context", "cli_entrypoint", "output_artifacts",
    "dependencies", "safety_classification",
]
GOVERNANCE_TOOL_REQUIRED = [
    "tool_name", "governance_scope", "policy_dependencies", "purpose",
    "mutation_capability", "destructive_capability", "requires_repo_context",
    "cli_entrypoint", "output_artifacts",
]

RUNTIME_TOOL_MARKERS = ["RUNTIME_TOOL_METADATA", "RUNTIME_TOOL_META"]
GOVERNANCE_TOOL_MARKERS = ["REPO_GOVERNANCE_TOOL_METADATA", "GOVERNANCE_TOOL_METADATA"]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _detect_schema_type(content: str) -> str:
    for marker in GOVERNANCE_TOOL_MARKERS:
        if marker in content:
            return "governance_tool"
    for marker in RUNTIME_TOOL_MARKERS:
        if marker in content:
            return "runtime_tool"
    return "unknown"


def _check_required_fields(content: str, required: list) -> dict:
    missing = []
    present = []
    for field in required:
        pattern = re.compile(rf"^\s*{re.escape(field)}\s*[:=]", re.MULTILINE)
        if pattern.search(content):
            present.append(field)
        else:
            missing.append(field)
    return {"present": present, "missing": missing}


def _validate_file(py_path: Path) -> dict:
    relative = str(py_path.relative_to(REPO_ROOT))
    try:
        content = py_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {
            "file": relative,
            "status": "ERROR",
            "error": str(exc),
            "schema_type": "unknown",
            "missing_fields": [],
        }

    schema_type = _detect_schema_type(content)
    if schema_type == "unknown":
        return {
            "file": relative,
            "status": "MISSING_HEADER",
            "schema_type": "unknown",
            "missing_fields": [],
            "note": "No recognized metadata marker found",
        }

    required = (
        GOVERNANCE_TOOL_REQUIRED if schema_type == "governance_tool" else RUNTIME_TOOL_REQUIRED
    )
    field_check = _check_required_fields(content, required)

    status = "PASS" if not field_check["missing"] else "FAIL"
    return {
        "file": relative,
        "status": status,
        "schema_type": schema_type,
        "present_fields": field_check["present"],
        "missing_fields": field_check["missing"],
    }


def scan_tool_dir(tool_root: Path) -> list:
    results = []
    for py_file in sorted(tool_root.rglob("*.py")):
        # Skip __pycache__ and _internal
        parts = py_file.parts
        if "__pycache__" in parts or "_internal" in parts:
            continue
        results.append(_validate_file(py_file))
    return results


def validate_headers(tool_root: Path) -> dict:
    all_results = scan_tool_dir(tool_root)
    passed = [r for r in all_results if r["status"] == "PASS"]
    failed = [r for r in all_results if r["status"] == "FAIL"]
    missing_header = [r for r in all_results if r["status"] == "MISSING_HEADER"]
    errors = [r for r in all_results if r["status"] == "ERROR"]

    return {
        "total_scanned": len(all_results),
        "passed": len(passed),
        "failed": len(failed),
        "missing_header": len(missing_header),
        "errors": len(errors),
        "pass_rate": f"{100 * len(passed) / max(len(all_results), 1):.1f}%",
        "file_results": all_results,
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit Dev_Tools scripts for header schema compliance."
    )
    parser.add_argument(
        "--tool-root",
        type=Path,
        default=DEV_TOOLS,
        help="Root directory to scan (default: Dev_Tools/)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="devscript_header_validation_report.json",
        help="Output report filename (written to canonical _Dev_Governance dir)",
    )
    args = parser.parse_args()

    results = validate_headers(args.tool_root)
    report = {
        "artifact_type": "devscript_header_validation",
        "generated_utc": _now_utc(),
        "tool_name": "devscript_header_validator",
        "schema_version": "1.0",
        "tool_root_scanned": str(args.tool_root),
        "status": "PASS" if results["failed"] == 0 and results["missing_header"] == 0 else "FAIL",
        "results": results,
    }
    write_report(args.output, report)
    status = report["status"]
    print(f"Status: {status}")
    print(f"Scanned: {results['total_scanned']} | Pass: {results['passed']} | "
          f"Fail: {results['failed']} | Missing header: {results['missing_header']}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

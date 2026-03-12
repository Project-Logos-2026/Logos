#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               governance_contract_validator
governance_scope:        Repo_Governance policy compliance across repository
policy_dependencies:
  - Repo_Governance/Runtime/Naming_Convention_Enforcement.md
  - Repo_Governance/Runtime/Abbreviation_Usage_Policy.md
  - Repo_Governance/Runtime/Runtime_Module_Generation_Spec.md
  - Repo_Governance/Header_Schemas/runtime_module_header_schema.json
purpose:
  Audit the repository for compliance with Repo_Governance policies.
  Checks naming conventions, abbreviation usage patterns, header schema
  usage, and runtime module generation rules. Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - governance_contract_validation_report.json
module_name:             governance_contract_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, ast, json, os, pathlib, re, sys
provides:
  - check_naming_conventions, check_abbreviation_patterns,
    check_module_headers, validate_contract, main
depends_on_runtime_state: none
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
DEV_RESOURCES = REPO_ROOT / "_Dev_Resources"
GOVERNANCE_ROOT = DEV_RESOURCES / "Repo_Governance"
ABBREVIATIONS_JSON = GOVERNANCE_ROOT / "Runtime" / "Abbreviations.json"
LOGOS_SYSTEM = REPO_ROOT / "LOGOS_SYSTEM"
DEV_TOOLS = DEV_RESOURCES / "Dev_Tools"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

# Regex for Title_Case_With_Underscores (allows ALL-CAPS segments)
TITLE_CASE_PATTERN = re.compile(r"^([A-Z][A-Za-z0-9]*_?)+[A-Z][A-Za-z0-9]*$|^[A-Z][A-Za-z0-9]*$")
# Pattern to detect lowercase-only or camelCase filenames
INVALID_MODULE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*\.py$")
CAMEL_CASE_PATTERN = re.compile(r"^[a-z][A-Za-z0-9]*\.py$")

# Known valid exception patterns (stdlib-like, dunder files)
EXEMPT_FILENAMES = {"__init__.py", "__main__.py", "conftest.py"}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_abbreviations() -> "dict | list":
    try:
        with open(ABBREVIATIONS_JSON, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def check_naming_conventions(scan_root: Path, scope_label: str) -> dict:
    """Check Python files for Title_Case_With_Underscores naming compliance."""
    violations = []
    compliant = []

    for py_file in sorted(scan_root.rglob("*.py")):
        parts = py_file.parts
        if "__pycache__" in parts:
            continue
        fname = py_file.name
        if fname in EXEMPT_FILENAMES:
            compliant.append(str(py_file.relative_to(REPO_ROOT)))
            continue

        # Check: snake_case (all lowercase) is a violation for source modules
        if INVALID_MODULE_PATTERN.match(fname):
            violations.append({
                "file": str(py_file.relative_to(REPO_ROOT)),
                "issue": "LOWERCASE_SNAKE_CASE_FILENAME",
                "actual": fname,
                "expected_pattern": "Title_Case_With_Underscores",
                "severity": "WARNING",
            })
        else:
            compliant.append(str(py_file.relative_to(REPO_ROOT)))

    return {
        "scope": scope_label,
        "total_scanned": len(violations) + len(compliant),
        "compliant_count": len(compliant),
        "violation_count": len(violations),
        "violations": violations,
    }


def check_abbreviation_patterns(file_content: str, file_rel: str, abbrev_keys: set) -> list:
    """Scan a file for ALL-CAPS tokens and flag those not in the abbreviation registry."""
    # Extract tokens that look like abbreviations (2+ consecutive uppercase letters)
    all_caps_pattern = re.compile(r"\b([A-Z]{2,})\b")
    tokens = set(all_caps_pattern.findall(file_content))

    # Common Python/system keywords to ignore
    ignore = {
        "PASS", "FAIL", "TRUE", "FALSE", "NONE", "ERROR", "OK", "NOT",
        "AND", "OR", "IF", "IN", "IS", "AS", "NO", "ID", "API",
        "UTF", "JSON", "AST", "CLI", "UTC", "ISO", "SDK", "URL",
        "TCP", "UDP", "HTTP", "HTTPS", "SMTP", "PATH", "OS", "IO",
        "READ", "WRITE", "DIR", "FILE", "LOG", "LEN", "MAX", "MIN",
        "KEY", "VAL", "STR", "INT", "DICT", "LIST", "SET", "BOOL",
    }
    missing_from_registry = []
    for token in sorted(tokens):
        if token in ignore:
            continue
        if token not in abbrev_keys:
            missing_from_registry.append(token)

    return missing_from_registry


def check_module_headers(scan_root: Path, required_marker: str) -> dict:
    """Check Python modules in scan_root for presence of the required header marker."""
    missing_headers = []
    present = []

    for py_file in sorted(scan_root.rglob("*.py")):
        parts = py_file.parts
        if "__pycache__" in parts or "_internal" in parts:
            continue
        if py_file.name in EXEMPT_FILENAMES:
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(py_file.relative_to(REPO_ROOT))
        if required_marker in content:
            present.append(rel)
        else:
            missing_headers.append(rel)

    return {
        "marker_checked": required_marker,
        "files_with_header": len(present),
        "files_missing_header": len(missing_headers),
        "missing": missing_headers,
    }


def validate_contract(
    check_naming: bool = True,
    check_headers: bool = True,
    check_abbreviations: bool = True,
    sample_limit: int = 50,
) -> dict:
    abbrev_data = _load_abbreviations()
    # Build set of registered abbreviation keys (may be list or dict)
    if isinstance(abbrev_data, dict):
        abbrev_keys = set(abbrev_data.keys())
    elif isinstance(abbrev_data, list):
        abbrev_keys = {
            entry.get("abbreviation", entry.get("key", ""))
            for entry in abbrev_data
            if isinstance(entry, dict)
        }
    else:
        abbrev_keys = set()

    results = {}

    # Naming conventions: scan Dev_Tools and LOGOS_SYSTEM
    if check_naming:
        results["naming_conventions"] = {
            "dev_tools": check_naming_conventions(DEV_TOOLS, "Dev_Tools"),
            "logos_system": check_naming_conventions(LOGOS_SYSTEM, "LOGOS_SYSTEM")
            if LOGOS_SYSTEM.is_dir()
            else {"scope": "LOGOS_SYSTEM", "status": "SKIPPED", "reason": "directory not found"},
        }

    # Header compliance: Runtime_Tools should have RUNTIME_TOOL_METADATA
    if check_headers:
        rt_root = DEV_TOOLS / "Runtime_Tools"
        gov_root = DEV_TOOLS / "Repo_Governance_Tools"
        results["header_compliance"] = {
            "runtime_tools_marker": check_module_headers(rt_root, "RUNTIME_TOOL_METADATA"),
            "governance_tools_marker": check_module_headers(gov_root, "REPO_GOVERNANCE_TOOL_METADATA"),
        }

    # Abbreviation usage: sample Dev_Tools files
    if check_abbreviations:
        abbrev_findings = []
        py_files = sorted(DEV_TOOLS.rglob("*.py"))[:sample_limit]
        for py_file in py_files:
            if "__pycache__" in py_file.parts:
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
            except Exception:
                continue
            rel = str(py_file.relative_to(REPO_ROOT))
            missing = check_abbreviation_patterns(content, rel, abbrev_keys)
            if missing:
                abbrev_findings.append({
                    "file": rel,
                    "unregistered_tokens": missing,
                })
        results["abbreviation_usage"] = {
            "files_sampled": len(py_files),
            "files_with_unregistered_tokens": len(abbrev_findings),
            "note": "Unregistered tokens are not necessarily violations; they require architect review.",
            "findings": abbrev_findings,
        }

    total_naming_violations = sum(
        r.get("violation_count", 0)
        for r in results.get("naming_conventions", {}).values()
        if isinstance(r, dict)
    )
    total_header_missing = sum(
        r.get("files_missing_header", 0)
        for r in results.get("header_compliance", {}).values()
        if isinstance(r, dict)
    )

    results["summary"] = {
        "total_naming_violations": total_naming_violations,
        "total_missing_headers": total_header_missing,
        "abbreviation_registry_loaded": len(abbrev_keys) > 0,
        "abbreviation_registry_size": len(abbrev_keys),
    }
    return results


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit repo for Repo_Governance policy compliance."
    )
    parser.add_argument("--skip-naming", action="store_true", help="Skip naming convention check")
    parser.add_argument("--skip-headers", action="store_true", help="Skip header compliance check")
    parser.add_argument("--skip-abbreviations", action="store_true", help="Skip abbreviation check")
    parser.add_argument("--sample-limit", type=int, default=50, help="Max files for abbreviation scan")
    parser.add_argument(
        "--output",
        type=str,
        default="governance_contract_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_contract(
        check_naming=not args.skip_naming,
        check_headers=not args.skip_headers,
        check_abbreviations=not args.skip_abbreviations,
        sample_limit=args.sample_limit,
    )
    summary = results.get("summary", {})
    status = "PASS" if summary.get("total_missing_headers", 0) == 0 else "PARTIAL"
    report = {
        "artifact_type": "governance_contract_validation",
        "generated_utc": _now_utc(),
        "tool_name": "governance_contract_validator",
        "schema_version": "1.0",
        "status": status,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {status}")
    print(f"Naming violations: {summary.get('total_naming_violations', 'N/A')} | "
          f"Missing headers: {summary.get('total_missing_headers', 'N/A')} | "
          f"Abbreviation registry size: {summary.get('abbreviation_registry_size', 'N/A')}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               repo_policy_enforcer
governance_scope:        Consolidated governance compliance aggregation
policy_dependencies:
  - Repo_Governance/Developer/Dev_Environment_Rules.md
  - Repo_Governance/Developer/Dev_Resources_Directory_Contract.md
  - Repo_Governance/Developer/Dev_Tool_Generation_Policy.md
  - Repo_Governance/Developer/Dev_Resources_Freeze_Protocol.md
  - Repo_Governance/Developer/Directory_Creation_Authorization_Rules.md
  - Repo_Governance/Runtime/Naming_Convention_Enforcement.md
  - Repo_Governance/Runtime/Abbreviation_Usage_Policy.md
purpose:
  Aggregate audit results from all governance validators and produce a
  consolidated governance compliance report. Composes results from
  devscript_header_validator, directory_structure_validator,
  governance_contract_validator, and tool_registry_validator.
  Read-only aggregator. Does not mutate the repository.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - consolidated_governance_compliance_report.json
module_name:             repo_policy_enforcer
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AGGREGATOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, subprocess, sys
provides:
  - run_validator, aggregate_results, main
depends_on_runtime_state: none
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
TOOLS_DIR = REPO_ROOT / "_Dev_Resources" / "Dev_Tools" / "Repo_Governance_Tools"
PYTHON = sys.executable

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

VALIDATORS = [
    {
        "tool": "devscript_header_validator",
        "script": "devscript_header_validator.py",
        "output": "devscript_header_validation_report.json",
        "description": "Header schema compliance audit",
    },
    {
        "tool": "directory_structure_validator",
        "script": "directory_structure_validator.py",
        "output": "directory_structure_validation_report.json",
        "description": "Dev_Resources directory contract audit",
    },
    {
        "tool": "governance_contract_validator",
        "script": "governance_contract_validator.py",
        "output": "governance_contract_validation_report.json",
        "description": "Repo_Governance policy compliance audit",
    },
    {
        "tool": "tool_registry_validator",
        "script": "tool_registry_validator.py",
        "output": "tool_registry_validation_report.json",
        "description": "Tool_Index registry consistency audit",
    },
    {
        "tool": "dev_resources_freeze_validator",
        "script": "dev_resources_freeze_validator.py",
        "output": "dev_resources_freeze_validation_report.json",
        "description": "Dev_Resources freeze compliance audit",
    },
    {
        "tool": "abbreviation_registry_validator",
        "script": "abbreviation_registry_validator.py",
        "output": "abbreviation_registry_validation_report.json",
        "description": "Abbreviation registry usage audit",
    },
    {
        "tool": "runtime_wiring_log_validator",
        "script": "runtime_wiring_log_validator.py",
        "output": "runtime_wiring_log_validation_report.json",
        "description": "Repo_Inventory dependency log integrity audit",
    },
]


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_validator(config: dict, timeout: int = 120) -> dict:
    """Invoke a validator subprocess and capture its result."""
    script_path = TOOLS_DIR / config["script"]
    if not script_path.is_file():
        return {
            "tool": config["tool"],
            "description": config["description"],
            "status": "SKIPPED",
            "reason": f"Script not found: {script_path}",
            "report_output": None,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
        }

    cmd = [PYTHON, str(script_path), "--output", config["output"]]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
        exit_code = result.returncode
        status = "PASS" if exit_code == 0 else "FAIL"
    except subprocess.TimeoutExpired:
        return {
            "tool": config["tool"],
            "description": config["description"],
            "status": "ERROR",
            "reason": f"Timeout after {timeout}s",
            "report_output": None,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
        }
    except Exception as exc:
        return {
            "tool": config["tool"],
            "description": config["description"],
            "status": "ERROR",
            "reason": str(exc),
            "report_output": None,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
        }

    # Try to load the generated sub-report
    report_path = OUTPUT_ROOT / config["output"]
    sub_report = None
    if report_path.is_file():
        try:
            with open(report_path, encoding="utf-8") as fh:
                sub_report = json.load(fh)
        except Exception:
            sub_report = None

    return {
        "tool": config["tool"],
        "description": config["description"],
        "status": status,
        "exit_code": exit_code,
        "report_output": config["output"],
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()[:500] if result.stderr else "",
        "sub_report_status": sub_report.get("status") if sub_report else None,
    }


def aggregate_results(validators: list, timeout: int) -> dict:
    run_results = []
    for config in validators:
        print(f"  Running: {config['tool']}...")
        res = run_validator(config, timeout=timeout)
        run_results.append(res)
        print(f"    -> {res['status']}")

    passed = [r for r in run_results if r["status"] == "PASS"]
    failed = [r for r in run_results if r["status"] == "FAIL"]
    skipped = [r for r in run_results if r["status"] == "SKIPPED"]
    errors = [r for r in run_results if r["status"] == "ERROR"]

    overall = "PASS" if not failed and not errors else "FAIL"
    return {
        "overall": overall,
        "total_validators": len(validators),
        "passed": len(passed),
        "failed": len(failed),
        "skipped": len(skipped),
        "errors": len(errors),
        "validator_results": run_results,
        "failed_tools": [r["tool"] for r in failed],
        "error_tools": [r["tool"] for r in errors],
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate all governance validator results into a consolidated compliance report."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout per validator in seconds (default: 120)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="consolidated_governance_compliance_report.json",
        help="Output report filename",
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        default=[],
        help="Tool names to skip",
    )
    args = parser.parse_args()

    validators_to_run = [v for v in VALIDATORS if v["tool"] not in args.skip]
    print(f"Running {len(validators_to_run)} governance validators...")
    results = aggregate_results(validators_to_run, timeout=args.timeout)

    report = {
        "artifact_type": "consolidated_governance_compliance",
        "generated_utc": _now_utc(),
        "tool_name": "repo_policy_enforcer",
        "schema_version": "1.0",
        "status": results["overall"],
        "results": results,
    }
    write_report(args.output, report)
    print(f"\nOverall Status: {results['overall']}")
    print(f"Pass: {results['passed']} | Fail: {results['failed']} | "
          f"Skip: {results['skipped']} | Error: {results['errors']}")
    if results["failed_tools"]:
        print(f"Failed: {results['failed_tools']}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if results["overall"] == "PASS" else 1)


if __name__ == "__main__":
    main()

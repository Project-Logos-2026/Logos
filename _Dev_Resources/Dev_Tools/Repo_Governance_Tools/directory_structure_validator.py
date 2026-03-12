#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               directory_structure_validator
governance_scope:        Dev_Resources canonical directory layout compliance
policy_dependencies:
  - Repo_Governance/Developer/Dev_Resources_Directory_Contract.md
  - Repo_Governance/Developer/Directory_Creation_Authorization_Rules.md
  - Repo_Governance/Developer/Dev_Resources_Freeze_Protocol.md
purpose:
  Validate the Dev_Resources directory contract. Checks that the canonical
  directory layout is intact, no unauthorized directories have been created,
  and all required directories are present. Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - directory_structure_validation_report.json
module_name:             directory_structure_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, sys
provides:
  - validate_structure, check_required_dirs, check_unauthorized_dirs,
    check_immutable_skeleton, main
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

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

# Required directories that MUST exist
REQUIRED_DIRS = [
    "_Dev_Resources/Dev_Tools",
    "_Dev_Resources/Dev_Tools/Archive",
    "_Dev_Resources/Dev_Tools/Archive/P1-5",
    "_Dev_Resources/Dev_Tools/Archive/RGE",
    "_Dev_Resources/Dev_Tools/Repo_Governance_Tools",
    "_Dev_Resources/Dev_Tools/Runtime_Tools",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Architecture_Validation",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Code_Extraction",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Dependency_Analysis",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Dev_Utilities",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Migration",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Repo_Audit",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Report_Generation",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Runtime_Diagnostics",
    "_Dev_Resources/Dev_Tools/Runtime_Tools/Static_Analysis",
    "_Dev_Resources/Processing_Center",
    "_Dev_Resources/Processing_Center/BLUEPRINTS",
    "_Dev_Resources/Processing_Center/STAGING",
    "_Dev_Resources/Processing_Center/STAGING/In_Process",
    "_Dev_Resources/Processing_Center/STAGING/In_Process/EXTRACT_LOGIC",
    "_Dev_Resources/Processing_Center/STAGING/In_Process/KEEP_VERIFY",
    "_Dev_Resources/Processing_Center/STAGING/In_Process/NORMALIZE_INTGRATE",
    "_Dev_Resources/Processing_Center/STAGING/Inspection_Targets",
    "_Dev_Resources/Processing_Center/STAGING/Post_Processing",
    "_Dev_Resources/Processing_Center/STAGING/Pre-Processing",
    "_Dev_Resources/Repo_Governance",
    "_Dev_Resources/Repo_Governance/Developer",
    "_Dev_Resources/Repo_Governance/Header_Schemas",
    "_Dev_Resources/Repo_Governance/Runtime",
    "_Dev_Resources/Repo_Inventory",
    "_Dev_Resources/Repo_Inventory/Master_Indexes",
    "_Dev_Resources/Repo_Inventory/Master_Indexes/Environment",
    "_Dev_Resources/Repo_Inventory/Master_Indexes/Runtime",
    "_Dev_Resources/Repo_Inventory/Master_Manifests",
    "_Dev_Resources/Tool_Index",
]

# Directories that must not be renamed or deleted (skeleton immutable)
IMMUTABLE_SKELETON = [
    "_Dev_Resources/Processing_Center",
    "_Dev_Resources/Processing_Center/BLUEPRINTS",
    "_Dev_Resources/Processing_Center/STAGING",
    "_Dev_Resources/Processing_Center/STAGING/In_Process",
    "_Dev_Resources/Processing_Center/STAGING/Inspection_Targets",
    "_Dev_Resources/Processing_Center/STAGING/Post_Processing",
    "_Dev_Resources/Processing_Center/STAGING/Pre-Processing",
]

# Tier 1 hard-frozen dirs (no file changes permitted except by exception)
HARD_FROZEN = [
    "_Dev_Resources/Repo_Governance/Header_Schemas",
    "_Dev_Resources/Dev_Tools/Archive/P1-5",
    "_Dev_Resources/Dev_Tools/Archive/RGE",
]

# Authorized top-level subdirectories of _Dev_Resources
AUTHORIZED_TOP_LEVEL = {
    "Dev_Tools", "Processing_Center", "Repo_Governance",
    "Repo_Inventory", "Tool_Index", "QUARANTINE", "__pycache__",
}

# Authorized Runtime_Tools subcategory directories
AUTHORIZED_RUNTIME_SUBCATS = {
    "Architecture_Validation", "Code_Extraction", "Dependency_Analysis",
    "Dev_Utilities", "Migration", "Repo_Audit", "Report_Generation",
    "Runtime_Diagnostics", "Static_Analysis", "__pycache__",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def check_required_dirs() -> dict:
    missing = []
    present = []
    for rel in REQUIRED_DIRS:
        full = REPO_ROOT / rel
        if full.is_dir():
            present.append(rel)
        else:
            missing.append(rel)
    return {"present": present, "missing": missing, "missing_count": len(missing)}


def check_immutable_skeleton() -> dict:
    violations = []
    intact = []
    for rel in IMMUTABLE_SKELETON:
        full = REPO_ROOT / rel
        if full.is_dir():
            intact.append(rel)
        else:
            violations.append({"path": rel, "issue": "DIRECTORY_MISSING_OR_RENAMED", "severity": "ERROR"})
    return {"intact": intact, "violations": violations, "violation_count": len(violations)}


def check_hard_frozen() -> list:
    results = []
    for rel in HARD_FROZEN:
        full = REPO_ROOT / rel
        results.append({
            "path": rel,
            "exists": full.is_dir(),
            "status": "INTACT" if full.is_dir() else "MISSING",
        })
    return results


def check_unauthorized_dirs() -> list:
    """Find directories under _Dev_Resources that are not in the authorized map."""
    unauthorized = []

    # Check top-level children of _Dev_Resources
    if not DEV_RESOURCES.is_dir():
        return [{"path": "_Dev_Resources", "issue": "ROOT_MISSING"}]

    for child in sorted(DEV_RESOURCES.iterdir()):
        if not child.is_dir():
            continue
        if child.name not in AUTHORIZED_TOP_LEVEL:
            unauthorized.append({
                "path": str(child.relative_to(REPO_ROOT)),
                "issue": "UNAUTHORIZED_TOP_LEVEL_DIRECTORY",
                "severity": "ERROR",
            })

    # Check Runtime_Tools subcategories
    rt_root = DEV_RESOURCES / "Dev_Tools" / "Runtime_Tools"
    if rt_root.is_dir():
        for child in sorted(rt_root.iterdir()):
            if child.is_dir() and child.name not in AUTHORIZED_RUNTIME_SUBCATS:
                unauthorized.append({
                    "path": str(child.relative_to(REPO_ROOT)),
                    "issue": "UNAUTHORIZED_RUNTIME_TOOLS_SUBCATEGORY",
                    "severity": "WARNING",
                })

    # Check Processing_Center/BLUEPRINTS for unexpected subdirectories added at top level of STAGING
    # (new dirs inside STAGING subdirs are allowed as MUTABLE CONTENTS; only STAGING direct children are locked)
    staging_root = DEV_RESOURCES / "Processing_Center" / "STAGING"
    authorized_staging_children = {
        "In_Process", "Inspection_Targets", "Post_Processing", "Pre-Processing",
    }
    if staging_root.is_dir():
        for child in sorted(staging_root.iterdir()):
            if child.is_dir() and child.name not in authorized_staging_children:
                unauthorized.append({
                    "path": str(child.relative_to(REPO_ROOT)),
                    "issue": "UNAUTHORIZED_STAGING_SUBDIRECTORY",
                    "severity": "WARNING",
                })

    return unauthorized


def validate_structure() -> dict:
    required_check = check_required_dirs()
    skeleton_check = check_immutable_skeleton()
    unauthorized = check_unauthorized_dirs()
    frozen_check = check_hard_frozen()

    errors = (
        required_check["missing_count"]
        + skeleton_check["violation_count"]
        + len([u for u in unauthorized if u.get("severity") == "ERROR"])
    )

    return {
        "required_directories": required_check,
        "immutable_skeleton": skeleton_check,
        "hard_frozen_dirs": frozen_check,
        "unauthorized_directories": unauthorized,
        "unauthorized_count": len(unauthorized),
        "total_errors": errors,
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Dev_Resources canonical directory structure."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="directory_structure_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_structure()
    status = "PASS" if results["total_errors"] == 0 else "FAIL"
    report = {
        "artifact_type": "directory_structure_validation",
        "generated_utc": _now_utc(),
        "tool_name": "directory_structure_validator",
        "schema_version": "1.0",
        "status": status,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {status}")
    print(f"Required dirs missing: {results['required_directories']['missing_count']} | "
          f"Skeleton violations: {results['immutable_skeleton']['violation_count']} | "
          f"Unauthorized dirs: {results['unauthorized_count']}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

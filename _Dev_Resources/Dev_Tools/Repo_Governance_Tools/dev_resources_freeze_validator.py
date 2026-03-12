#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               dev_resources_freeze_validator
governance_scope:        Dev_Resources freeze compliance enforcement
policy_dependencies:
  - Repo_Governance/Developer/Dev_Resources_Freeze_Protocol.md
  - Repo_Governance/Developer/Dev_Resources_Directory_Contract.md
  - Repo_Governance/Developer/Directory_Creation_Authorization_Rules.md
purpose:
  Audit Dev_Resources freeze compliance. Verifies that immutable directories
  have not been renamed or removed, no unauthorized directory creation has
  occurred, and Processing_Center skeleton exceptions are correctly honored.
  Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - dev_resources_freeze_validation_report.json
module_name:             dev_resources_freeze_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, sys
provides:
  - check_tier1_frozen, check_tier2_skeleton, check_coq_exclusion_zones,
    check_processing_center_exceptions, validate_freeze, main
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

# Tier 1 — Hard Frozen (must exist as directories)
TIER1_FROZEN = [
    "_Dev_Resources/Repo_Governance/Header_Schemas",
    "_Dev_Resources/Dev_Tools/Archive/P1-5",
    "_Dev_Resources/Dev_Tools/Archive/RGE",
]

# Tier 2 — Skeleton Frozen (directory must exist; files inside may change)
TIER2_SKELETON = [
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
]

# Coq Extended Exclusion (must exist and be untouched)
COQ_EXCLUSION_ZONES = [
    "STARTUP/PXL_Gate",
    "STARTUP/Runtime_Compiler",
]

# Authorized mutable areas inside Processing_Center
# (BLUEPRINTS/* and STAGING/* contents may change, but top-level dirs may not)
AUTHORIZED_MUTABLE_UNDER_PC = {
    # BLUEPRINTS subdirs (authorized original 13)
    "ARP", "CSP", "DRAC", "EMP", "Epistemic_Artifacts", "I2",
    "Logos_Core", "MSPC", "MTP", "P1-5", "RGE", "SCP", "SOP",
    # STAGING subdirs (authorized original 4)
    "In_Process", "Inspection_Targets", "Post_Processing", "Pre-Processing",
}

# Authorized top-level entries under _Dev_Resources
AUTHORIZED_DEV_RESOURCES_TOP = {
    "Dev_Tools", "Processing_Center", "Repo_Governance",
    "Repo_Inventory", "Tool_Index", "QUARANTINE", "__pycache__",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def check_tier1_frozen() -> dict:
    """Verify Tier 1 hard-frozen directories still exist."""
    results = []
    violations = []
    for rel in TIER1_FROZEN:
        full = REPO_ROOT / rel
        exists = full.is_dir()
        entry = {
            "path": rel,
            "tier": 1,
            "exists": exists,
            "status": "INTACT" if exists else "VIOLATION",
        }
        results.append(entry)
        if not exists:
            violations.append({
                "path": rel,
                "issue": "TIER1_FROZEN_DIR_MISSING_OR_RENAMED",
                "severity": "ERROR",
            })
    return {"dirs": results, "violations": violations, "violation_count": len(violations)}


def check_tier2_skeleton() -> dict:
    """Verify Tier 2 skeleton directories still exist."""
    results = []
    violations = []
    for rel in TIER2_SKELETON:
        full = REPO_ROOT / rel
        exists = full.is_dir()
        entry = {
            "path": rel,
            "tier": 2,
            "exists": exists,
            "status": "INTACT" if exists else "VIOLATION",
        }
        results.append(entry)
        if not exists:
            violations.append({
                "path": rel,
                "issue": "TIER2_SKELETON_DIR_MISSING_OR_RENAMED",
                "severity": "ERROR",
            })
    return {"dirs": results, "violations": violations, "violation_count": len(violations)}


def check_coq_exclusion_zones() -> dict:
    """Verify Coq exclusion zone directories exist (they must never be removed)."""
    results = []
    violations = []
    for rel in COQ_EXCLUSION_ZONES:
        full = REPO_ROOT / rel
        exists = full.is_dir()
        entry = {
            "path": rel,
            "exists": exists,
            "status": "INTACT" if exists else "VIOLATION",
        }
        results.append(entry)
        if not exists:
            violations.append({
                "path": rel,
                "issue": "COQ_EXCLUSION_ZONE_DIR_MISSING",
                "severity": "CRITICAL",
            })
    return {"dirs": results, "violations": violations, "violation_count": len(violations)}


def check_processing_center_exceptions() -> dict:
    """
    Verify Processing_Center exceptions are honored:
    - BLUEPRINTS/* and STAGING/* contents may change (files inside allowed)
    - But no NEW top-level directories inside BLUEPRINTS or STAGING at the immediate child level
      that are not in the authorized set.
    """
    violations = []
    ok = []

    blueprints = REPO_ROOT / "_Dev_Resources" / "Processing_Center" / "BLUEPRINTS"
    staging = REPO_ROOT / "_Dev_Resources" / "Processing_Center" / "STAGING"

    for parent_dir, label in [(blueprints, "BLUEPRINTS"), (staging, "STAGING")]:
        if not parent_dir.is_dir():
            continue
        for child in sorted(parent_dir.iterdir()):
            if not child.is_dir():
                continue
            child_name = child.name
            rel = str(child.relative_to(REPO_ROOT))
            if child_name in AUTHORIZED_MUTABLE_UNDER_PC:
                ok.append({"path": rel, "status": "AUTHORIZED"})
            else:
                violations.append({
                    "path": rel,
                    "issue": f"UNAUTHORIZED_SUBDIR_UNDER_{label}",
                    "severity": "WARNING",
                })

    return {
        "authorized_subdirs": ok,
        "unauthorized_subdirs": violations,
        "unauthorized_count": len(violations),
    }


def check_unauthorized_top_level() -> list:
    """Check for unauthorized top-level directories under _Dev_Resources."""
    violations = []
    if not DEV_RESOURCES.is_dir():
        return [{"issue": "_Dev_Resources missing", "severity": "CRITICAL"}]
    for child in sorted(DEV_RESOURCES.iterdir()):
        if child.is_dir() and child.name not in AUTHORIZED_DEV_RESOURCES_TOP:
            violations.append({
                "path": str(child.relative_to(REPO_ROOT)),
                "issue": "UNAUTHORIZED_TOP_LEVEL_DIRECTORY_IN_DEV_RESOURCES",
                "severity": "ERROR",
            })
    return violations


def validate_freeze() -> dict:
    tier1 = check_tier1_frozen()
    tier2 = check_tier2_skeleton()
    coq = check_coq_exclusion_zones()
    pc_exceptions = check_processing_center_exceptions()
    unauthorized_top = check_unauthorized_top_level()

    total_violations = (
        tier1["violation_count"]
        + tier2["violation_count"]
        + coq["violation_count"]
        + pc_exceptions["unauthorized_count"]
        + len([u for u in unauthorized_top if u.get("severity") == "ERROR"])
    )

    return {
        "tier1_frozen": tier1,
        "tier2_skeleton": tier2,
        "coq_exclusion_zones": coq,
        "processing_center_exceptions": pc_exceptions,
        "unauthorized_top_level": unauthorized_top,
        "total_violations": total_violations,
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit Dev_Resources freeze compliance."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="dev_resources_freeze_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_freeze()
    status = "PASS" if results["total_violations"] == 0 else "FAIL"
    report = {
        "artifact_type": "dev_resources_freeze_validation",
        "generated_utc": _now_utc(),
        "tool_name": "dev_resources_freeze_validator",
        "schema_version": "1.0",
        "status": status,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {status}")
    print(f"Tier1 violations: {results['tier1_frozen']['violation_count']} | "
          f"Tier2 violations: {results['tier2_skeleton']['violation_count']} | "
          f"Coq zone violations: {results['coq_exclusion_zones']['violation_count']} | "
          f"Unauthorized dirs: {len(results['unauthorized_top_level'])}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

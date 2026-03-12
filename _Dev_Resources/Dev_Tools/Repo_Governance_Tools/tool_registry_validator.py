#!/usr/bin/env python3
"""
REPO_GOVERNANCE_TOOL_METADATA
------------------------------
tool_name:               tool_registry_validator
governance_scope:        Tool_Index registry consistency
policy_dependencies:
  - Repo_Governance/Developer/Dev_Tool_Generation_Policy.md
  - Tool_Index/dev_tool_registry.json
  - Tool_Index/dev_tool_capability_index.json
  - Tool_Index/destructive_tools_index.json
purpose:
  Validate Tool_Index registry consistency. Checks that tool paths
  exist on disk, registry entries match filesystem, capability index
  alignment is correct, and destructive tool classification is accurate.
  Read-only auditor.
mutation_capability:     false
destructive_capability:  false
requires_repo_context:   true
cli_entrypoint:          main
output_artifacts:
  - tool_registry_validation_report.json
module_name:             tool_registry_validator
runtime_layer:           GOVERNANCE_ENFORCEMENT
role:                    AUDITOR
boot_phase:              N/A
failure_mode:            FAIL_CLOSED
expected_imports:
  - argparse, json, os, pathlib, sys
provides:
  - validate_registry, check_paths_exist, check_capability_alignment,
    check_destructive_classification, main
depends_on_runtime_state: none
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/workspaces/Logos")
OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/_Dev_Governance")
TOOL_INDEX = REPO_ROOT / "_Dev_Resources" / "Tool_Index"
DEV_TOOLS = REPO_ROOT / "_Dev_Resources" / "Dev_Tools"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> tuple:
    """Load JSON file; return (data, error_str). error_str is None on success."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh), None
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except json.JSONDecodeError as exc:
        return None, f"JSON decode error in {path}: {exc}"


def check_paths_exist(registry_entries: list) -> list:
    """For each registry entry, verify the script_path resolves to a real file."""
    results = []
    for entry in registry_entries:
        tool_name = entry.get("tool_name", "<unnamed>")
        script_path_str = entry.get("script_path", "")
        # script_path may be relative to canonical_root or Dev_Tools
        # Try resolutions in order of likelihood
        candidates = [
            DEV_TOOLS / "Runtime_Tools" / script_path_str,
            DEV_TOOLS / script_path_str,
            REPO_ROOT / script_path_str,
            REPO_ROOT / "_Dev_Resources" / script_path_str,
        ]
        # Also resolve the basename against the full Dev_Tools tree
        basename = Path(script_path_str).name
        found = None
        for c in candidates:
            if c.is_file():
                found = str(c.relative_to(REPO_ROOT))
                break
        if found is None:
            # Search by filename across Dev_Tools
            matches = list(DEV_TOOLS.rglob(basename)) if basename else []
            if matches:
                found = str(matches[0].relative_to(REPO_ROOT))
                status = "FOUND_BY_NAME"
            else:
                status = "NOT_FOUND"
        else:
            status = "FOUND"

        results.append({
            "tool_name": tool_name,
            "script_path": script_path_str,
            "resolved_path": found,
            "exists": status in ("FOUND", "FOUND_BY_NAME"),
            "status": status,
        })
    return results


def check_capability_alignment(registry_entries: list, capability_data: dict) -> list:
    """Cross-check that tools in registry appear in capability index."""
    issues = []
    if capability_data is None:
        return [{"issue": "capability_index_unavailable"}]

    index_tools = set()
    for category_info in capability_data.get("category_summary", {}).values():
        for t in category_info.get("tools", []):
            index_tools.add(t)
    # Also walk tool_capabilities if present
    for entry in capability_data.get("tool_capabilities", []):
        index_tools.add(entry.get("tool_name", ""))

    for entry in registry_entries:
        tool_name = entry.get("tool_name", "")
        if tool_name and tool_name not in index_tools:
            issues.append({
                "tool_name": tool_name,
                "issue": "NOT_IN_CAPABILITY_INDEX",
                "severity": "WARNING",
            })
    return issues


def check_destructive_classification(
    registry_entries: list, destructive_index_data: dict
) -> list:
    """Verify tools flagged destructive in registry appear in the destructive index."""
    issues = []
    if destructive_index_data is None:
        return [{"issue": "destructive_index_unavailable"}]

    destructive_listed = set()
    for entry in destructive_index_data.get("destructive_tools", []):
        destructive_listed.add(entry.get("tool_name", ""))
    # Also handle flat list format
    if isinstance(destructive_index_data.get("tools"), list):
        for t in destructive_index_data["tools"]:
            destructive_listed.add(t if isinstance(t, str) else t.get("tool_name", ""))

    for entry in registry_entries:
        tool_name = entry.get("tool_name", "")
        is_destructive = entry.get("destructive_capability_flag", False)
        in_index = tool_name in destructive_listed
        if is_destructive and not in_index:
            issues.append({
                "tool_name": tool_name,
                "issue": "DESTRUCTIVE_FLAG_SET_BUT_NOT_IN_DESTRUCTIVE_INDEX",
                "severity": "ERROR",
            })
        elif not is_destructive and in_index:
            issues.append({
                "tool_name": tool_name,
                "issue": "IN_DESTRUCTIVE_INDEX_BUT_FLAG_NOT_SET",
                "severity": "WARNING",
            })
    return issues


def validate_registry() -> dict:
    registry, err = _load_json(TOOL_INDEX / "dev_tool_registry.json")
    capability, cap_err = _load_json(TOOL_INDEX / "dev_tool_capability_index.json")
    d_index, d_err = _load_json(TOOL_INDEX / "destructive_tools_index.json")

    load_errors = []
    if err:
        load_errors.append({"file": "dev_tool_registry.json", "error": err})
    if cap_err:
        load_errors.append({"file": "dev_tool_capability_index.json", "error": cap_err})
    if d_err:
        load_errors.append({"file": "destructive_tools_index.json", "error": d_err})

    entries = registry.get("entries", []) if registry else []

    path_results = check_paths_exist(entries)
    capability_issues = check_capability_alignment(entries, capability)
    destructive_issues = check_destructive_classification(entries, d_index)

    missing_paths = [r for r in path_results if not r["exists"]]
    all_issues = capability_issues + destructive_issues
    errors = [i for i in all_issues if i.get("severity") == "ERROR"]

    return {
        "registry_entries_total": len(entries),
        "path_check": {
            "total": len(path_results),
            "found": len([r for r in path_results if r["exists"]]),
            "not_found": len(missing_paths),
            "missing": missing_paths,
            "results": path_results,
        },
        "capability_alignment": {
            "issues": capability_issues,
            "issue_count": len(capability_issues),
        },
        "destructive_classification": {
            "issues": destructive_issues,
            "issue_count": len(destructive_issues),
        },
        "load_errors": load_errors,
        "error_count": len(errors) + len(load_errors),
    }


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Tool_Index registry consistency."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tool_registry_validation_report.json",
        help="Output report filename",
    )
    args = parser.parse_args()

    results = validate_registry()
    overall = "PASS" if results["error_count"] == 0 and len(results["path_check"]["missing"]) == 0 else "FAIL"
    report = {
        "artifact_type": "tool_registry_validation",
        "generated_utc": _now_utc(),
        "tool_name": "tool_registry_validator",
        "schema_version": "1.0",
        "status": overall,
        "results": results,
    }
    write_report(args.output, report)
    print(f"Status: {overall}")
    print(f"Registry entries: {results['registry_entries_total']} | "
          f"Paths missing: {results['path_check']['not_found']} | "
          f"Issues: {results['error_count']}")
    print(f"Report: {OUTPUT_ROOT / args.output}")
    sys.exit(0 if overall == "PASS" else 1)


if __name__ == "__main__":
    main()

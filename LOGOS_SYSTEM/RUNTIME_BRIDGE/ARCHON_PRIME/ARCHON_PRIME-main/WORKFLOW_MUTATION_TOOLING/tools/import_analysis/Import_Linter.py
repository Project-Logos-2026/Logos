#!/usr/bin/env python3
# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-050
# module_name:          Import_Linter
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/import_analysis/Import_Linter.py
# responsibility:       Analysis module: Import Linter
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
LOGOS Static Import Enforcement Linter
Branch: pre-import-repair-stabilization

Scans all Python files under STARTUP/ and LOGOS_SYSTEM/ for import violations.
"""
"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: Import_Linter.py
tool_category: Repo_Audit
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python Import_Linter.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import os
import sys
from pathlib import Path

# Rule definitions
ALLOWED_ROOT = "LOGOS_SYSTEM"
FORBIDDEN_ROOTS = [
    "Logos_System",
    "LOGOS_AGI",
    "intelligence",
    "mathematics",
    "protocols",
]
BARE_PREFIXES = [
    "Synthetic_Cognition_Protocol",
    "Advanced_Reasoning_Protocol",
    "Multi_Process_Signal_Compiler",
    "I1_Agent",
    "I2_Agent",
    "I3_Agent",
]
PROHIBITED_PATTERNS = [
    "sys.path.append",
    "sys.path.insert",
    "import *",
    "importlib.import_module",
]
PROHIBITED_NET_MODULES = ["requests", "httpx", "urllib"]

SCAN_DIRS = ["STARTUP", "LOGOS_SYSTEM"]


# Track violations in structured form
violations_by_rule = {f"Rule {i+1}": [] for i in range(4)}
violation_records = []
files_scanned = set()


# Helper: check if path contains /mathematics/
def is_mathematics_path(path):
    return "/mathematics/" in str(path).replace(os.sep, "/")


def scan_file(file_path):
    # DRAC exclusion: skip files in Dynamic_Reconstruction_Adaptive_Compilation_Protocol
    if "Dynamic_Reconstruction_Adaptive_Compilation_Protocol" in str(file_path):
        return
    rel_path = os.path.relpath(file_path)
    files_scanned.add(rel_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception:
        return
    try:
        tree = ast.parse(source, filename=str(file_path))
    except Exception:
        return
    # Rule 1 & 2 & 3: Import checks
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name
                # Rule 1: Only LOGOS_SYSTEM allowed as internal root
                if not mod.startswith(ALLOWED_ROOT):
                    # Rule 2: Forbidden roots
                    if any(mod.startswith(root) for root in FORBIDDEN_ROOTS):
                        violations_by_rule["Rule 2"].append(
                            (rel_path, node.lineno, mod)
                        )
                        violation_records.append(
                            {
                                "rule": "Rule_2",
                                "file": rel_path,
                                "line": node.lineno,
                                "import": mod,
                            }
                        )
                    # Rule 3: Bare prefix
                    elif any(mod.startswith(prefix) for prefix in BARE_PREFIXES):
                        violations_by_rule["Rule 3"].append(
                            (rel_path, node.lineno, mod)
                        )
                        violation_records.append(
                            {
                                "rule": "Rule_3",
                                "file": rel_path,
                                "line": node.lineno,
                                "import": mod,
                            }
                        )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            # Rule 1: Only LOGOS_SYSTEM allowed as internal root
            if mod and not mod.startswith(ALLOWED_ROOT):
                # Rule 2: Forbidden roots
                if any(mod.startswith(root) for root in FORBIDDEN_ROOTS):
                    violations_by_rule["Rule 2"].append((rel_path, node.lineno, mod))
                    violation_records.append(
                        {
                            "rule": "Rule_2",
                            "file": rel_path,
                            "line": node.lineno,
                            "import": mod,
                        }
                    )
                # Rule 3: Bare prefix
                elif any(mod.startswith(prefix) for prefix in BARE_PREFIXES):
                    violations_by_rule["Rule 3"].append((rel_path, node.lineno, mod))
                    violation_records.append(
                        {
                            "rule": "Rule_3",
                            "file": rel_path,
                            "line": node.lineno,
                            "import": mod,
                        }
                    )
            # Rule 4: import *
            if node.names and any(alias.name == "*" for alias in node.names):
                violations_by_rule["Rule 4"].append((rel_path, node.lineno, "import *"))
                violation_records.append(
                    {
                        "rule": "Rule_4",
                        "file": rel_path,
                        "line": node.lineno,
                        "import": "import *",
                    }
                )
    # Rule 4: Prohibited patterns in source
    for pattern in PROHIBITED_PATTERNS:
        idx = source.find(pattern)
        if idx != -1:
            # Find line number
            line_num = source[:idx].count("\n") + 1
            violations_by_rule["Rule 4"].append((rel_path, line_num, pattern))
            violation_records.append(
                {
                    "rule": "Rule_4",
                    "file": rel_path,
                    "line": line_num,
                    "import": pattern,
                }
            )
    # Rule 4: Prohibited net modules in /mathematics/
    if is_mathematics_path(file_path):
        for netmod in PROHIBITED_NET_MODULES:
            for pattern in [f"import {netmod}", f"from {netmod} import"]:
                idx = source.find(pattern)
                if idx != -1:
                    line_num = source[:idx].count("\n") + 1
                    violations_by_rule["Rule 4"].append(
                        (rel_path, line_num, f"network import: {netmod}")
                    )
                    violation_records.append(
                        {
                            "rule": "Rule_4",
                            "file": rel_path,
                            "line": line_num,
                            "import": f"network import: {netmod}",
                        }
                    )


def main():
    py_files = []
    for scan_dir in SCAN_DIRS:
        for root, _, files in os.walk(scan_dir):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))
    for file_path in py_files:
        scan_file(file_path)

    total_violations = len(violation_records)
    violations_by_rule_count = {
        k.replace(" ", "_"): len(v) for k, v in violations_by_rule.items()
    }

    # Prepare JSON report
    report = {
        "summary": {
            "total_files_scanned": len(files_scanned),
            "total_violations": total_violations,
            "violations_by_rule": violations_by_rule_count,
        },
        "violations": violation_records,
    }

    # Write JSON report
    reports_dir = Path("_Reports")
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / "Import_Linter_Report.json"
    import json

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Print short summary
    print(f"Total violations: {total_violations}")
    for rule, count in violations_by_rule_count.items():
        print(f"  {rule}: {count}")

    if total_violations > 0:
        sys.exit(1)
    else:
        print("No import violations found.")
        sys.exit(0)


if __name__ == "__main__":
    main()

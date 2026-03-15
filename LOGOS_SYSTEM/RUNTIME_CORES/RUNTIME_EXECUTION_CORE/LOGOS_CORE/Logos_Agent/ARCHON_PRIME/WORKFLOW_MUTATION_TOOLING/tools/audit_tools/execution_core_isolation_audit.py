# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-028
# module_name:          execution_core_isolation_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/execution_core_isolation_audit.py
# responsibility:       Inspection module: execution core isolation audit
# runtime_stage:        audit
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
RUNTIME_TOOL_METADATA
---------------------

tool_name: execution_core_isolation_audit.py
tool_category: Architecture_Validation
tool_subcategory: isolation_boundary_verification

purpose:
Verifies that modules under LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE
do not import from forbidden boundary-violating modules. Reports any boundary
violations found via static AST analysis.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python execution_core_isolation_audit.py --include-root LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE

output_artifacts:
execution_core_isolation_audit.json

dependencies:
ast, pathlib, json, argparse

safety_classification:
READ_ONLY
"""

import argparse
import ast
import json
from pathlib import Path

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def get_imports(filepath: Path) -> list[str]:
    """Return all imported module strings from a Python file."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Execution core isolation auditor — detects forbidden imports crossing the RUNTIME_EXECUTION_CORE boundary."
    )
    parser.add_argument(
        "--include-root",
        required=True,
        help="The isolated core directory to audit, relative to repo root.",
    )
    parser.add_argument(
        "--roots",
        nargs="*",
        default=[],
        help="Additional entry-point paths to trace (optional).",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=["__pycache__"],
        help="Directory name patterns to exclude.",
    )
    parser.add_argument(
        "--forbidden-prefixes",
        nargs="*",
        default=["STAGING", "_Dev_Resources", "test_", "legacy"],
        help="Import prefixes considered boundary violations.",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/ARCHON_PRIME",
        help="Repository root (default: /workspaces/ARCHON_PRIME).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    core_root = repo_root / args.include_root

    if not core_root.exists():
        print(f"ERROR: Include root not found: {core_root}")
        raise SystemExit(1)

    py_files = [
        f
        for f in sorted(core_root.rglob("*.py"))
        if not any(exc in str(f) for exc in args.exclude)
    ]
    print(f"Auditing {len(py_files)} modules in: {args.include_root}")

    violations = []
    clean = []
    for fpath in py_files:
        imports = get_imports(fpath)
        bad = [
            imp
            for imp in imports
            if any(imp.startswith(prefix) for prefix in args.forbidden_prefixes)
        ]
        record = {
            "path": str(fpath.relative_to(repo_root)),
            "all_imports": imports,
            "violations": bad,
        }
        if bad:
            violations.append(record)
        else:
            clean.append(str(fpath.relative_to(repo_root)))

    status = "PASS" if not violations else "FAIL"
    report = {
        "tool": "execution_core_isolation_audit",
        "include_root": args.include_root,
        "forbidden_prefixes": args.forbidden_prefixes,
        "status": status,
        "total_modules": len(py_files),
        "violations_count": len(violations),
        "clean_count": len(clean),
        "violations": violations,
    }
    write_report("execution_core_isolation_audit.json", report)
    print(f"Status: {status} | Violations: {len(violations)} | Clean: {len(clean)}")


if __name__ == "__main__":
    main()

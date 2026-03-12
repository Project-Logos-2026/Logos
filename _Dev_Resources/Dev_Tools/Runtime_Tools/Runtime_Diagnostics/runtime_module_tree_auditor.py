"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: runtime_module_tree_auditor.py
tool_category: Runtime_Diagnostics
tool_subcategory: module_tree_analysis

purpose:
AST-based inventory of any module subtree. Extracts module names, class
definitions, function definitions, line counts, and import dependencies.
Parameterizable via --module-root to audit any LOGOS_SYSTEM subsystem.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python runtime_module_tree_auditor.py --module-root LOGOS_SYSTEM/RUNTIME_BRIDGE

output_artifacts:
module_tree_audit.json

dependencies:
ast, pathlib, json, argparse

safety_classification:
READ_ONLY
"""

import ast
import json
import argparse
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data: dict) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def audit_module(filepath: Path, repo_root: Path) -> dict:
    """Extract classes, functions, imports, and LOC from a single .py file."""
    record: dict = {
        "path": str(filepath.relative_to(repo_root)),
        "loc": 0,
        "classes": [],
        "functions": [],
        "imports": [],
        "parse_error": None,
    }
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        record["loc"] = source.count("\n") + 1
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError as exc:
        record["parse_error"] = str(exc)
        return record

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            record["classes"].append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            record["functions"].append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                record["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                record["imports"].append(node.module)

    return record


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AST-based module tree auditor for any LOGOS_SYSTEM subsystem."
    )
    parser.add_argument(
        "--module-root",
        required=True,
        help="Subdirectory to audit, relative to repo root.",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/Logos",
        help="Repository root (default: /workspaces/Logos).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    module_root = repo_root / args.module_root

    if not module_root.exists():
        print(f"ERROR: Module root not found: {module_root}")
        raise SystemExit(1)

    py_files = sorted(module_root.rglob("*.py"))
    print(f"Auditing {len(py_files)} Python files under: {module_root.relative_to(repo_root)}")

    modules = [audit_module(f, repo_root) for f in py_files]

    total_loc = sum(m["loc"] for m in modules)
    total_classes = sum(len(m["classes"]) for m in modules)
    total_functions = sum(len(m["functions"]) for m in modules)
    parse_errors = [m["path"] for m in modules if m["parse_error"]]

    report = {
        "tool": "runtime_module_tree_auditor",
        "module_root": args.module_root,
        "summary": {
            "total_modules": len(modules),
            "total_loc": total_loc,
            "total_classes": total_classes,
            "total_functions": total_functions,
            "parse_errors": len(parse_errors),
        },
        "parse_error_files": parse_errors,
        "modules": modules,
    }
    write_report("module_tree_audit.json", report)
    print(f"Modules: {len(modules)} | LOC: {total_loc} | Classes: {total_classes} | Functions: {total_functions}")


if __name__ == "__main__":
    main()

# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-072
# module_name:          ast_parser
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/semantic_extraction/ast_parser.py
# responsibility:       Analysis module: ast parser
# runtime_stage:        analysis
# execution_entry:      None
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
ast_parser.py — AST-based function extraction from Python source files.
Extracts: function name, docstring, signature, imports, body summary.
"""

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: ast_parser.py
tool_category: Static_Analysis
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python ast_parser.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
from pathlib import Path
from typing import Any

OUTPUT_ROOT = Path(
    "/workspaces/ARCHON_PRIME/SYSTEM_AUDITS_AND_REPORTS/PIPELINE_OUTPUTS"
)
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json

        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


def _imports_from_tree(tree: ast.Module) -> list[str]:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                imports.append(f"{mod}.{alias.name}" if mod else alias.name)
    return sorted(set(imports))


def _build_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = []
    func_args = node.args
    for arg in func_args.args:
        args.append(arg.arg)
    for arg in func_args.kwonlyargs:
        args.append(arg.arg)
    if func_args.vararg:
        args.append(f"*{func_args.vararg.arg}")
    if func_args.kwarg:
        args.append(f"**{func_args.kwarg.arg}")
    return f"{node.name}({', '.join(args)})"


def _body_summary(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Return a compact summary of what the function body does."""
    calls: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                calls.append(child.func.id)
            elif isinstance(child.func, ast.Attribute):
                calls.append(child.func.attr)
    # Deduplicate preserving order
    seen: set[str] = set()
    unique = [c for c in calls if not (c in seen or seen.add(c))]  # type: ignore[func-returns-value]
    return ", ".join(unique[:10]) if unique else ""


def parse_file(path: Path) -> list[dict[str, Any]]:
    """
    Parse a Python file and return a list of function records.
    Each record contains: name, docstring, signature, imports, body_calls, file_path.
    Returns an empty list on syntax error.
    """
    try:
        src = path.read_text(errors="replace")
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        return []

    imports = _imports_from_tree(tree)
    records: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # Skip private/dunder helpers
        if node.name.startswith("__") and node.name.endswith("__"):
            continue
        doc = ast.get_docstring(node) or ""
        records.append(
            {
                "name": node.name,
                "docstring": doc[:500],
                "signature": _build_signature(node),
                "imports": imports,
                "body_calls": _body_summary(node),
                "file_path": str(path),
                "lineno": node.lineno,
            }
        )

    return records

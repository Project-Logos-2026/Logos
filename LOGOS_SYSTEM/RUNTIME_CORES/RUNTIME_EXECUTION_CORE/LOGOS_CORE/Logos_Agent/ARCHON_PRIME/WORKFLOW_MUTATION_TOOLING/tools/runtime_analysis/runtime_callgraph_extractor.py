# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-067
# module_name:          runtime_callgraph_extractor
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/runtime_analysis/runtime_callgraph_extractor.py
# responsibility:       Analysis module: runtime callgraph extractor
# runtime_stage:        validation
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

tool_name: runtime_callgraph_extractor.py
tool_category: Runtime_Diagnostics
tool_subcategory: call_graph_analysis

purpose:
AST scan of entrypoint modules to build a static dependency/call graph.
Captures all Import and ImportFrom statements reachable from the specified
entry points and writes the dependency map to JSON.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python runtime_callgraph_extractor.py --roots STARTUP/START_LOGOS.py

output_artifacts:
runtime_callgraph.json

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


def extract_imports(filepath: Path) -> list[str]:
    """Return all imported module names from a single Python file."""
    imports = []
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, OSError):
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def build_callgraph(roots: list[Path], repo_root: Path) -> dict:
    """
    Walk AST from each entry-point file, following discovered .py paths
    within the repo to build a dependency adjacency map.
    """
    visited: set[str] = set()
    graph: dict[str, list[str]] = {}
    queue: list[Path] = list(roots)

    while queue:
        current = queue.pop(0)
        key = str(current.relative_to(repo_root))
        if key in visited:
            continue
        visited.add(key)

        imports = extract_imports(current)
        graph[key] = imports

        # Attempt to resolve imports to local files for further traversal
        for mod in imports:
            candidate = repo_root / mod.replace(".", "/")
            py_candidate = candidate.with_suffix(".py")
            init_candidate = candidate / "__init__.py"
            for path in (py_candidate, init_candidate):
                if path.exists():
                    rel = str(path.relative_to(repo_root))
                    if rel not in visited:
                        queue.append(path)

    return graph


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Static AST call-graph extractor for LOGOS_SYSTEM entry points."
    )
    parser.add_argument(
        "--roots",
        nargs="+",
        required=True,
        help="One or more entry-point .py files relative to repo root.",
    )
    parser.add_argument(
        "--repo-root",
        default="/workspaces/ARCHON_PRIME",
        help="Repository root (default: /workspaces/ARCHON_PRIME).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    root_paths = [repo_root / r for r in args.roots]

    missing = [str(p) for p in root_paths if not p.exists()]
    if missing:
        print(f"ERROR: Entry-point files not found: {missing}")
        raise SystemExit(1)

    print(f"Building callgraph from {len(root_paths)} root(s)...")
    graph = build_callgraph(root_paths, repo_root)

    report = {
        "tool": "runtime_callgraph_extractor",
        "roots": [str(p.relative_to(repo_root)) for p in root_paths],
        "total_modules_visited": len(graph),
        "callgraph": graph,
    }
    write_report("runtime_callgraph.json", report)
    print(f"Total modules visited: {len(graph)}")


if __name__ == "__main__":
    main()

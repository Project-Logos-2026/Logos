"""
Phase 2B — Deterministic Canonical Root Prefix Expansion
AST-based import rewrite for protocol roots.
"""
import ast
import os
import json
from pathlib import Path
from typing import List, Dict, Any

PREFIX_MAP = {
    "Advanced_Reasoning_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol",
    "Synthetic_Cognition_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol",
    "Multi_Process_Signal_Compiler": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler",
    "System_Operations_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol"
}

EXCLUDE_SUBTREE = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"

REPORT_PATH = Path("_Reports/Phase_2B_Mutation_Report.json")

class ImportRewriter(ast.NodeTransformer):
    def __init__(self, prefix_map: Dict[str, str]):
        self.prefix_map = prefix_map
        self.rewrites = []

    def visit_Import(self, node):
        new_names = []
        for alias in node.names:
            for prefix, repl in self.prefix_map.items():
                if alias.name == prefix:
                    new_name = repl
                    self.rewrites.append((node.lineno, f"import {alias.name}", f"import {new_name}"))
                    alias = ast.alias(name=new_name, asname=alias.asname)
            new_names.append(alias)
        node.names = new_names
        return node

    def visit_ImportFrom(self, node):
        if node.module:
            for prefix, repl in self.prefix_map.items():
                if node.module == prefix:
                    self.rewrites.append((node.lineno, f"from {node.module} import ...", f"from {repl} import ..."))
                    node.module = repl
        return node

def should_exclude(path: Path) -> bool:
    return EXCLUDE_SUBTREE in str(path)

def find_py_files(root_dirs: List[str]) -> List[Path]:
    py_files = []
    for root_dir in root_dirs:
        for dirpath, dirs, files in os.walk(root_dir):
            if EXCLUDE_SUBTREE in dirpath:
                continue
            for f in files:
                if f.endswith(".py"):
                    py_files.append(Path(dirpath) / f)
    return py_files

def main():
    scan_dirs = ["STARTUP", "LOGOS_SYSTEM"]
    py_files = find_py_files(scan_dirs)
    total_files_modified = 0
    total_imports_rewritten = 0
    detailed = []
    for file in py_files:
        with open(file, "r", encoding="utf-8") as f:
            src = f.read()
        try:
            tree = ast.parse(src)
        except Exception:
            continue
        rewriter = ImportRewriter(PREFIX_MAP)
        rewriter.visit(tree)
        if not rewriter.rewrites:
            continue
        total_files_modified += 1
        total_imports_rewritten += len(rewriter.rewrites)
        for lineno, original, rewritten in rewriter.rewrites:
            detailed.append({
                "file": str(file),
                "line": lineno,
                "original": original,
                "rewritten": rewritten
            })
        # Write back mutated code, preserving formatting
        import astor
        new_src = astor.to_source(tree)
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_src)
    report = {
        "total_files_modified": total_files_modified,
        "total_imports_rewritten": total_imports_rewritten,
        "rewrites": detailed
    }
    REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Phase 2B mutation complete. Files modified: {total_files_modified}, Imports rewritten: {total_imports_rewritten}")

if __name__ == "__main__":
    main()

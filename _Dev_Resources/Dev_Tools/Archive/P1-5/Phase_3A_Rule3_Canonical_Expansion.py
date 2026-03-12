# Phase_3A_Rule3_Canonical_Expansion.py
"""
Deterministic AST-based import rewrite for Rule_3 canonical expansion.
Expands bare-prefix imports to full LOGOS_SYSTEM paths per canonical map.
Excludes DRAC subtree and non-targeted directories.
"""
import ast
import os
import json
from typing import List, Dict

CANONICAL_PREFIX_MAP = {
    "Synthetic_Cognition_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol",
    "Advanced_Reasoning_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Advanced_Reasoning_Protocol",
    "Multi_Process_Signal_Compiler": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler",
    "System_Operations_Protocol": "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol",
}

EXCLUDE_PATH_FRAGMENT = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
TARGET_ROOTS = ["STARTUP", "LOGOS_SYSTEM"]

REPORT_PATH = "_Reports/Phase_3A_Rule3_Canonical_Expansion_Report.json"

rewrite_records: List[Dict] = []
total_files_modified = 0
total_imports_rewritten = 0


def should_exclude(path: str) -> bool:
    return EXCLUDE_PATH_FRAGMENT in path

def is_target_file(path: str) -> bool:
    return any(path.startswith(root + os.sep) for root in TARGET_ROOTS) and path.endswith(".py")

def expand_imports_in_file(filepath: str) -> int:
    global total_files_modified, total_imports_rewritten
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=filepath)
    modified = False
    rewrites = []
    class ImportRewriter(ast.NodeTransformer):
        def visit_Import(self, node):
            for alias in node.names:
                for bare, canon in CANONICAL_PREFIX_MAP.items():
                    if alias.name == bare or alias.name.startswith(bare + "."):
                        new_name = canon + alias.name[len(bare):]
                        rewrites.append({
                            "file": filepath,
                            "original": alias.name,
                            "rewritten": new_name,
                            "line": node.lineno
                        })
                        alias.name = new_name
                        nonlocal modified
                        modified = True
                        break
            return node
        def visit_ImportFrom(self, node):
            if node.module:
                for bare, canon in CANONICAL_PREFIX_MAP.items():
                    if node.module == bare or node.module.startswith(bare + "."):
                        new_mod = canon + node.module[len(bare):]
                        rewrites.append({
                            "file": filepath,
                            "original": node.module,
                            "rewritten": new_mod,
                            "line": node.lineno
                        })
                        node.module = new_mod
                        nonlocal modified
                        modified = True
                        break
            return node
    rewriter = ImportRewriter()
    new_tree = rewriter.visit(tree)
    if modified:
        total_files_modified += 1
        total_imports_rewritten += len(rewrites)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ast.unparse(new_tree))
        rewrite_records.extend(rewrites)
        return len(rewrites)
    return 0

def main():
    for root, dirs, files in os.walk("."):
        for fname in files:
            rel_path = os.path.relpath(os.path.join(root, fname), ".")
            if not is_target_file(rel_path):
                continue
            if should_exclude(rel_path):
                continue
            expand_imports_in_file(rel_path)
    report = {
        "phase": "Phase_3A_Rule3_Canonical_Expansion",
        "total_files_modified": total_files_modified,
        "total_imports_rewritten": total_imports_rewritten,
        "rewrite_records": rewrite_records
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()

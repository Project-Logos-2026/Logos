"""
PHASE_2D_CANONICAL_ROOT_EXPANSION
Rewrite all Rule_2 legacy roots to fully canonical runtime paths using AST-based rewriting.
"""
import os
import json
import ast
from pathlib import Path

EXECUTION_BASE = "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE"
OPERATIONS_BASE = "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE"
EXCLUDE = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
BRANCH = "pre-import-repair-stabilization"

REPORT_PATH = Path("_Reports/Phase_2D_Canonical_Expansion_Mutation_Report.json")

# Canonicalization rules

def canonicalize(module: str) -> str:
    if module.startswith("Logos_System."):
        return "LOGOS_SYSTEM." + module[len("Logos_System."):]
    if module.startswith("Logos_System_Rebuild."):
        return "LOGOS_SYSTEM." + module[len("Logos_System_Rebuild."):]
    if module.startswith("LOGOS_AGI."):
        return EXECUTION_BASE + "." + module[len("LOGOS_AGI."):]
    if module.startswith("intelligence."):
        return EXECUTION_BASE + ".Synthetic_Cognition_Protocol." + module[len("intelligence."):]
    if module.startswith("mathematics."):
        return EXECUTION_BASE + ".Synthetic_Cognition_Protocol.SCP_Core.MVS_System.MVS_Core.mathematics." + module[len("mathematics."):]
    return module

class CanonicalImportRewriter(ast.NodeTransformer):
    def __init__(self):
        self.rewrites = []
        self.lines = None

    def visit_Import(self, node):
        for alias in node.names:
            orig = alias.name
            new = canonicalize(orig)
            if new != orig:
                self.rewrites.append((node.lineno, f"import {orig}", f"import {new}"))
                alias.name = new
        return node

    def visit_ImportFrom(self, node):
        if node.module:
            orig = node.module
            new = canonicalize(orig)
            if new != orig:
                self.rewrites.append((node.lineno, f"from {orig} import ...", f"from {new} import ..."))
                node.module = new
        return node

def should_exclude(path: Path) -> bool:
    return EXCLUDE in str(path)

def find_py_files(root_dirs):
    py_files = []
    for root_dir in root_dirs:
        for dirpath, dirs, files in os.walk(root_dir):
            if EXCLUDE in dirpath:
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
    rewrite_records = []
    for file in py_files:
        with open(file, "r", encoding="utf-8") as f:
            src = f.read()
        try:
            tree = ast.parse(src)
        except Exception:
            continue
        rewriter = CanonicalImportRewriter()
        rewriter.visit(tree)
        if not rewriter.rewrites:
            continue
        total_files_modified += 1
        total_imports_rewritten += len(rewriter.rewrites)
        for lineno, original, rewritten in rewriter.rewrites:
            rewrite_records.append({
                "file": str(file),
                "original": original,
                "rewritten": rewritten,
                "line": lineno
            })
        import astor
        new_src = astor.to_source(tree)
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_src)
    report = {
        "phase": "Phase_2D_Canonical_Root_Expansion",
        "branch": BRANCH,
        "total_files_modified": total_files_modified,
        "total_imports_rewritten": total_imports_rewritten,
        "rewrite_records": rewrite_records,
        "excluded_directory": EXCLUDE
    }
    REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Phase 2D canonical root expansion complete. Files modified: {total_files_modified}, Imports rewritten: {total_imports_rewritten}")

if __name__ == "__main__":
    main()

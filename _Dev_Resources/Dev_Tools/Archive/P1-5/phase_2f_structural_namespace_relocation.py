"""
PHASE_2F_STRUCTURAL_NAMESPACE_RELOCATION
Collapse legacy ghost namespaces into canonical on-disk runtime paths using AST-based rewriting.
"""
import os
import json
import ast
from pathlib import Path

EXCLUDE = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
REPORT_PATH = Path("_Reports/Phase_2F_Structural_Relocation_Mutation_Report.json")

# Canonical relocation map logic

def relocate(module: str) -> str:
    # 1. System_Stack collapse
    if module.startswith("Logos_System.System_Stack.Logos_Protocol"):
        return module.replace(
            "Logos_System.System_Stack.Logos_Protocol",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol",
            1)
    if module.startswith("Logos_System.System_Stack.Synthetic_Cognition_Protocol"):
        return module.replace(
            "Logos_System.System_Stack.Synthetic_Cognition_Protocol",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol",
            1)
    if module.startswith("Logos_System.System_Stack.System_Operations_Protocol"):
        return module.replace(
            "Logos_System.System_Stack.System_Operations_Protocol",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol",
            1)
    if module.startswith("Logos_System.System_Entry_Point"):
        return module.replace(
            "Logos_System.System_Entry_Point",
            "LOGOS_SYSTEM.STARTUP",
            1)
    # 2. LOGOS_AGI collapse
    if module.startswith("LOGOS_AGI."):
        rest = module[len("LOGOS_AGI."):]
        if rest.startswith("System_Operations_Protocol"):
            return "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol" + rest[len("System_Operations_Protocol"):]
        else:
            return "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE." + rest
    # 3. intelligence collapse
    if module.startswith("intelligence.trinity"):
        return module.replace(
            "intelligence.trinity",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.trinity",
            1)
    if module.startswith("intelligence.iel_domains"):
        return module.replace(
            "intelligence.iel_domains",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.iel_domains",
            1)
    if module.startswith("intelligence.uip"):
        return module.replace(
            "intelligence.uip",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.uip",
            1)
    # 4. mathematics collapse
    if module.startswith("mathematics."):
        return module.replace(
            "mathematics.",
            "LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.MVS_System.MVS_Core.mathematics.",
            1)
    return module

class RelocationRewriter(ast.NodeTransformer):
    def __init__(self):
        self.rewrites = []

    def visit_Import(self, node):
        for alias in node.names:
            orig = alias.name
            new = relocate(orig)
            if new != orig:
                self.rewrites.append((node.lineno, f"import {orig}", f"import {new}"))
                alias.name = new
        return node

    def visit_ImportFrom(self, node):
        if node.module:
            orig = node.module
            new = relocate(orig)
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
    scan_dirs = ["STARTUP", "LOGOS_SYSTEM/RUNTIME_CORES", "LOGOS_SYSTEM/RUNTIME_BRIDGE"]
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
        rewriter = RelocationRewriter()
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
        "phase": "Phase_2F_Structural_Namespace_Relocation",
        "total_files_modified": total_files_modified,
        "total_imports_rewritten": total_imports_rewritten,
        "rewrite_records": rewrite_records,
        "excluded_directory": EXCLUDE
    }
    REPORT_PATH.parent.mkdir(exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Phase 2F structural relocation complete. Files modified: {total_files_modified}, Imports rewritten: {total_imports_rewritten}")

if __name__ == "__main__":
    main()

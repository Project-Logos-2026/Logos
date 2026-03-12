import ast
import os
import json
from pathlib import Path

ALLOWED_ROOT = "LOGOS_SYSTEM"
LEGACY_ROOT = "Logos_System"
EXCLUDE_DIR = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
SCAN_DIRS = ["STARTUP", "LOGOS_SYSTEM"]

files_modified = []
rewrite_records = []

class ImportRootNormalizer(ast.NodeTransformer):
    def __init__(self, file_path):
        self.file_path = file_path
        self.local_rewrites = []

    def visit_Import(self, node):
        for alias in node.names:
            parts = alias.name.split(".")
            if parts and parts[0] == LEGACY_ROOT:
                original = alias.name
                parts[0] = ALLOWED_ROOT
                alias.name = ".".join(parts)
                self.local_rewrites.append({
                    "type": "import",
                    "original": original,
                    "rewritten": alias.name,
                    "line": node.lineno
                })
        return node

    def visit_ImportFrom(self, node):
        if node.module:
            parts = node.module.split(".")
            if parts and parts[0] == LEGACY_ROOT:
                original = node.module
                parts[0] = ALLOWED_ROOT
                node.module = ".".join(parts)
                self.local_rewrites.append({
                    "type": "from",
                    "original": original,
                    "rewritten": node.module,
                    "line": node.lineno
                })
        return node

def should_exclude(path):
    return EXCLUDE_DIR in str(path)

def process_file(path):
    try:
        source = Path(path).read_text(encoding="utf-8")
    except Exception:
        return

    try:
        tree = ast.parse(source)
    except Exception:
        return

    normalizer = ImportRootNormalizer(path)
    new_tree = normalizer.visit(tree)

    if normalizer.local_rewrites:
        new_source = ast.unparse(new_tree)

        Path(path).write_text(new_source, encoding="utf-8")

        files_modified.append(str(path))
        rewrite_records.extend([
            {
                "file": str(path),
                **entry
            }
            for entry in normalizer.local_rewrites
        ])

def main():
    for scan_dir in SCAN_DIRS:
        for root, _, files in os.walk(scan_dir):
            if should_exclude(root):
                continue
            for file in files:
                if file.endswith(".py"):
                    process_file(os.path.join(root, file))

    report = {
        "phase": "Phase_2A_AST_Canonical_Root_Normalization",
        "total_files_modified": len(set(files_modified)),
        "total_imports_rewritten": len(rewrite_records),
        "files_modified": list(set(files_modified)),
        "rewrite_records": rewrite_records,
        "excluded_directory": EXCLUDE_DIR
    }

    reports_dir = Path("_Reports")
    reports_dir.mkdir(exist_ok=True)

    with open(reports_dir / "Phase_2A_AST_Mutation_Report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("Phase 2A AST normalization complete.")
    print("Files modified:", len(set(files_modified)))
    print("Imports rewritten:", len(rewrite_records))

if __name__ == "__main__":
    main()

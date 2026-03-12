"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: repo_structure_export.py
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
python repo_structure_export.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import os
import json
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}

directories = []
python_files = []
imports = []

for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
    # Prune ignored directories in-place
    dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

    rel_dir = os.path.relpath(dirpath, REPO_ROOT)
    if rel_dir != ".":
        directories.append(rel_dir)

    for filename in filenames:
        if filename.endswith(".py"):
            rel_file = os.path.relpath(os.path.join(dirpath, filename), REPO_ROOT)
            python_files.append(rel_file)

            abs_file = os.path.join(dirpath, filename)
            try:
                with open(abs_file, "r", encoding="utf-8", errors="replace") as f:
                    for line_number, line in enumerate(f, start=1):
                        stripped = line.strip()
                        if stripped.startswith("import ") or stripped.startswith("from "):
                            imports.append({
                                "file": rel_file,
                                "line_number": line_number,
                                "import_statement": stripped,
                            })
            except OSError:
                pass

tree_path = os.path.join(REPO_ROOT, "repo_directory_tree.json")
files_path = os.path.join(REPO_ROOT, "repo_python_files.json")
imports_path = os.path.join(REPO_ROOT, "repo_imports.json")

with open(tree_path, "w", encoding="utf-8") as f:
    json.dump({"directories": directories}, f, indent=2)

with open(files_path, "w", encoding="utf-8") as f:
    json.dump({"python_files": python_files}, f, indent=2)

with open(imports_path, "w", encoding="utf-8") as f:
    json.dump({"imports": imports}, f, indent=2)

print(f"repo_directory_tree.json -> {tree_path}")
print(f"repo_python_files.json  -> {files_path}")
print(f"repo_imports.json       -> {imports_path}")
print("All three artifacts written successfully.")

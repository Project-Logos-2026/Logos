# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-064
# module_name:          repo_structure_export
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/repo_structure_export.py
# responsibility:       Inspection module: repo structure export
# runtime_stage:        inspection
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

import json
import os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
}

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
                        if stripped.startswith("import ") or stripped.startswith(
                            "from "
                        ):
                            imports.append(
                                {
                                    "file": rel_file,
                                    "line_number": line_number,
                                    "import_statement": stripped,
                                }
                            )
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

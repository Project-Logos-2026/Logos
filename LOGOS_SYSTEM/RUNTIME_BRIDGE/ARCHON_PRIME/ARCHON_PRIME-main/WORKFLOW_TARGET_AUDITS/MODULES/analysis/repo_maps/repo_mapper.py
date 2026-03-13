# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-086
# module_name:          repo_mapper
# subsystem:            audit_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_TARGET_AUDITS/MODULES/analysis/repo_maps/repo_mapper.py
# responsibility:       Analysis module: repo mapper
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

import ast
import hashlib
import json
import os
from pathlib import Path

REPO_ROOT = Path(".").resolve()

OUTPUT_DIR = REPO_ROOT / "AUDIT_SYSTEM" / "analysis" / "repo_maps"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def build_directory_tree():
    tree = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        rel = os.path.relpath(root, REPO_ROOT)
        tree[rel] = {"dirs": sorted(dirs), "files": sorted(files)}
    return tree


def collect_python_files():
    py_files = []
    for root, _, files in os.walk(REPO_ROOT):
        for f in files:
            if f.endswith(".py"):
                p = Path(root) / f
                rel = os.path.relpath(p, REPO_ROOT)
                py_files.append(
                    {"path": rel, "size": p.stat().st_size, "hash": hash_file(p)}
                )
    return py_files


def extract_imports(file_path):
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception:
        pass
    return sorted(set(imports))


def build_module_index(py_files):
    modules = []
    for f in py_files:
        full = REPO_ROOT / f["path"]
        name = f["path"].replace("/", ".").replace(".py", "")
        imports = extract_imports(full)

        modules.append({"module": name, "file": f["path"], "imports": imports})
    return modules


print("ARCHON_PRIME AUDIT START")

directory_tree = build_directory_tree()
python_files = collect_python_files()
module_index = build_module_index(python_files)

with open(OUTPUT_DIR / "repo_directory_tree.json", "w") as f:
    json.dump(directory_tree, f, indent=2)

with open(OUTPUT_DIR / "repo_python_files.json", "w") as f:
    json.dump(python_files, f, indent=2)

with open(OUTPUT_DIR / "module_index.json", "w") as f:
    json.dump(module_index, f, indent=2)

print("ARCHON_PRIME AUDIT COMPLETE")
print("Artifacts written to:", OUTPUT_DIR)

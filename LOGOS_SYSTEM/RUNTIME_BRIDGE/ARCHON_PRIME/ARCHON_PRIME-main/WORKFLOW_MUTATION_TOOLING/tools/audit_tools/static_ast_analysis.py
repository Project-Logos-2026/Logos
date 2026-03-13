# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-045
# module_name:          static_ast_analysis
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/static_ast_analysis.py
# responsibility:       Inspection module: static ast analysis
# runtime_stage:        audit
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

# Static AST analysis script for Logos repository
# This script will be used to extract module path, file path, and static imports for each Python file in the repo.
# It will output the results to _Reports/FULL_STATIC_IMPORT_GRAPH.json and _Reports/LAYER_CLASSIFIED_GRAPH.json

"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: static_ast_analysis.py
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
python static_ast_analysis.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import ast
import json
from pathlib import Path

# Layer classification rules (prefixes)
LAYER_RULES = [
    ("LOGOS_SYSTEM/RUNTIME_CORES/", "runtime_core"),
    ("LOGOS_SYSTEM/RUNTIME_BRIDGE/", "runtime_bridge"),
    ("LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/", "governance_enforcement"),
    ("LOGOS_SYSTEM/System_Entry_Point/", "system_entry_point"),
    ("LOGOS_SYSTEM/", "logos_system"),
    ("STARTUP/", "startup"),
    ("_Governance/", "governance"),
    ("_Dev_Resources/", "dev_resources"),
    ("_Reports/", "reports"),
]

REPO_ROOT = Path("/workspaces/ARCHON_PRIME")
REPORTS_DIR = REPO_ROOT / "_Reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Load the list of all user Python files (already filtered)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from python_file_list import PYTHON_FILE_LIST

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


# Helper: convert file path to module path (dot notation)
def file_to_module_path(file_path: Path) -> str:
    rel_path = file_path.relative_to(REPO_ROOT)
    parts = list(rel_path.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-3]  # strip .py
    return ".".join(parts)


# Helper: classify by layer
def classify_layer(file_path: Path) -> str:
    rel_path = str(file_path.relative_to(REPO_ROOT))
    for prefix, layer in LAYER_RULES:
        if rel_path.startswith(prefix):
            return layer
    return "other"


# Helper: extract static imports from a Python file
def extract_imports(file_path: Path):
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=str(file_path))
        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    imports.add(n.module.split(".")[0])
    except Exception as e:
        imports.add(f"__ERROR__:{e}")
    return sorted(imports)


# Main analysis
def main():
    full_graph = []
    for file_path_str in PYTHON_FILE_LIST:
        file_path = Path(file_path_str)
        module_path = file_to_module_path(file_path)
        rel_path = str(file_path.relative_to(REPO_ROOT))
        imports = extract_imports(file_path)
        full_graph.append(
            {"module_path": module_path, "file_path": rel_path, "imports": imports}
        )
    # Write full static import graph
    with open(
        REPORTS_DIR / "FULL_STATIC_IMPORT_GRAPH.json", "w", encoding="utf-8"
    ) as f:
        json.dump(full_graph, f, indent=2)
    # Layer classification
    layer_graph = []
    for entry in full_graph:
        layer = classify_layer(REPO_ROOT / entry["file_path"])
        layer_graph.append({**entry, "layer": layer})
    with open(REPORTS_DIR / "LAYER_CLASSIFIED_GRAPH.json", "w", encoding="utf-8") as f:
        json.dump(layer_graph, f, indent=2)
    print(
        f"Static analysis complete. Modules: {len(full_graph)}. Output written to _Reports/."
    )


if __name__ == "__main__":
    main()

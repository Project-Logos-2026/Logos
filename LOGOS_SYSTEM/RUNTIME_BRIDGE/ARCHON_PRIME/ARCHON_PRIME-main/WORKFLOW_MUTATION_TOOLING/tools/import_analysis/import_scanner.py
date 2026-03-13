# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-055
# module_name:          import_scanner
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/import_analysis/import_scanner.py
# responsibility:       Analysis module: import scanner
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
import json
from pathlib import Path


def extract_imports(file):
    imports = []
    try:
        tree = ast.parse(open(file).read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            if isinstance(node, ast.ImportFrom):
                imports.append(node.module)
    except Exception:
        pass
    return imports


def scan():
    result = {}
    for p in Path(".").rglob("*.py"):
        result[str(p)] = extract_imports(p)
    json.dump(result, open("logs/import_map.json", "w"), indent=2)


if __name__ == "__main__":
    scan()

# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-065
# module_name:          dependency_graph
# subsystem:            mutation_tooling
# module_role:          analysis
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/runtime_analysis/dependency_graph.py
# responsibility:       Analysis module: dependency graph
# runtime_stage:        validation
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

IMPORT_FILE = "logs/import_map.json"


def build_graph():
    data = json.load(open(IMPORT_FILE))
    graph = {}
    for module, imports in data.items():
        graph[module] = imports
    json.dump(graph, open("logs/dependency_graph.json", "w"), indent=2)


if __name__ == "__main__":
    build_graph()

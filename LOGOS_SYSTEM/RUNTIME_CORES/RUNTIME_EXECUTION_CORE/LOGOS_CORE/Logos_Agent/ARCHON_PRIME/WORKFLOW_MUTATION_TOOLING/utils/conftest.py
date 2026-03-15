# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-080
# module_name:          conftest
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/utils/conftest.py
# responsibility:       Utility module: conftest
# runtime_stage:        utility
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

import pytest

EXTERNAL_PATH_FRAGMENTS = [
    "External_Enhancements",
    "ML_Wrapper",
    "NLP_Wrapper",
    "Visualization_Wrapper",
    "Graph_Wrapper",
]


def pytest_collection_modifyitems(config, items):
    for item in items:
        path_str = str(item.fspath)
        if any(fragment in path_str for fragment in EXTERNAL_PATH_FRAGMENTS):
            item.add_marker(pytest.mark.external_wrapper)

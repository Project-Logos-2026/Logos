# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-060
# module_name:          header_validator
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/header_validator.py
# responsibility:       Utility module: header validator
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

import json
from pathlib import Path


def check_headers():
    missing = []
    for p in Path(".").rglob("*.py"):
        text = open(p).read().strip()
        if not text.startswith("#"):
            missing.append(str(p))
    json.dump(missing, open("logs/header_violations.json", "w"), indent=2)


if __name__ == "__main__":
    check_headers()

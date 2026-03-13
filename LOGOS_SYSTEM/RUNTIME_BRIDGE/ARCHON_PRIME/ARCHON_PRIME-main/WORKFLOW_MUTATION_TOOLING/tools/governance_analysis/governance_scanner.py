# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-049
# module_name:          governance_scanner
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/governance_analysis/governance_scanner.py
# responsibility:       Inspection module: governance scanner
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
from pathlib import Path


def scan():
    gov = []
    for p in Path(".").rglob("*governance*.py"):
        gov.append(str(p))
    json.dump(gov, open("logs/governance_modules.json", "w"), indent=2)


if __name__ == "__main__":
    scan()

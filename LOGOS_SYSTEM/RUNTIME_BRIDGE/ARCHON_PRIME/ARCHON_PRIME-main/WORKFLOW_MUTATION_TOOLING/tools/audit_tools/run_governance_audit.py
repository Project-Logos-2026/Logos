# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-042
# module_name:          run_governance_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/run_governance_audit.py
# responsibility:       Inspection module: run governance audit
# runtime_stage:        audit
# execution_entry:      run
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

import sys

import governance_contract_audit
import governance_coverage_map
import governance_module_audit


def run(target):

    governance_contract_audit.run(target)

    governance_module_audit.run(target)

    governance_coverage_map.run(target)


if __name__ == "__main__":

    target = sys.argv[1]

    run(target)

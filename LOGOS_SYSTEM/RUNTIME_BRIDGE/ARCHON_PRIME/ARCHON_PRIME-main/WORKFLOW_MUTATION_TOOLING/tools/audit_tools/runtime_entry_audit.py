# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-043
# module_name:          runtime_entry_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/runtime_entry_audit.py
# responsibility:       Inspection module: runtime entry audit
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

from pathlib import Path

from audit_utils import generate_id, write_log


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        text = open(p).read()

        if "__main__" in text:

            issues.append(
                {
                    "id": generate_id(str(p)),
                    "file": str(p),
                    "issue": "runtime_entrypoint",
                }
            )

    write_log("runtime_entry_audit", target, "runtime_entrypoint", issues)

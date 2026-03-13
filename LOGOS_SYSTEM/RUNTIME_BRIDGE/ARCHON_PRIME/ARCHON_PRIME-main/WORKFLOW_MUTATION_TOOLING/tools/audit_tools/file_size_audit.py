# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-030
# module_name:          file_size_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/file_size_audit.py
# responsibility:       Inspection module: file size audit
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

        size = p.stat().st_size

        if size > 50000:

            issues.append(
                {
                    "id": generate_id(str(p)),
                    "file": str(p),
                    "size_bytes": size,
                    "issue": "oversized_module",
                }
            )

    write_log("file_size_audit", target, "oversized_module", issues)

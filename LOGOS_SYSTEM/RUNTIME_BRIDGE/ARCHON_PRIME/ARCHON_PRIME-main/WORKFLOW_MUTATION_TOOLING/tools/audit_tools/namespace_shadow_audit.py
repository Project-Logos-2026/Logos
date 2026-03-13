# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-037
# module_name:          namespace_shadow_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/namespace_shadow_audit.py
# responsibility:       Inspection module: namespace shadow audit
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

    names = {}
    issues = []

    for p in Path(target).rglob("*.py"):

        name = p.stem

        if name in names:

            issues.append(
                {
                    "id": generate_id(name),
                    "module": name,
                    "file_a": names[name],
                    "file_b": str(p),
                    "issue": "namespace_shadow",
                }
            )

        else:
            names[name] = str(p)

    write_log("namespace_shadow_audit", target, "namespace_shadow", issues)

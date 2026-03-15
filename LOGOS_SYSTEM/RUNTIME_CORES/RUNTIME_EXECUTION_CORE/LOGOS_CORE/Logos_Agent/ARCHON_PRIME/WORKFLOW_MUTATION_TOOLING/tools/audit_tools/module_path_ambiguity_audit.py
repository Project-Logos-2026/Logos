# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-036
# module_name:          module_path_ambiguity_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/module_path_ambiguity_audit.py
# responsibility:       Inspection module: module path ambiguity audit
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

    modules = {}
    issues = []

    for p in Path(target).rglob("*.py"):

        short = p.stem

        if short in modules:

            issues.append(
                {
                    "id": generate_id(short),
                    "module": short,
                    "file_a": modules[short],
                    "file_b": str(p),
                    "issue": "module_path_ambiguity",
                }
            )

        else:
            modules[short] = str(p)

    write_log("module_path_ambiguity_audit", target, "module_path_ambiguity", issues)

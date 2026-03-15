# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-033
# module_name:          governance_module_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/governance_module_audit.py
# responsibility:       Inspection module: governance module audit
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

KEYWORDS = [
    "governance",
    "contract",
    "enforce",
    "validate",
    "policy",
    "rule",
    "constraint",
]


def run(target):

    issues = []

    for p in Path(target).rglob("*.py"):

        try:

            text = open(p).read().lower()

            for k in KEYWORDS:

                if k in text:

                    issues.append(
                        {
                            "id": generate_id(str(p) + k),
                            "module": str(p),
                            "keyword": k,
                            "issue": "governance_module",
                        }
                    )

                    break

        except Exception:
            pass

    write_log("governance_module_audit", target, "governance_module", issues)

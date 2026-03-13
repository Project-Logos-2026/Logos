# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-031
# module_name:          governance_contract_audit
# subsystem:            mutation_tooling
# module_role:          inspection
# canonical_path:       WORKFLOW_MUTATION_TOOLING/tools/audit_tools/governance_contract_audit.py
# responsibility:       Inspection module: governance contract audit
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

GOV_TERMS = [
    "governance",
    "contract",
    "policy",
    "protocol",
    "rule",
    "constraint",
    "spec",
    "design",
]


def run(target):

    issues = []

    for p in Path(target).rglob("*"):

        if p.suffix.lower() in [".md", ".txt", ".yaml", ".yml", ".json"]:

            try:

                text = open(p).read().lower()

                for term in GOV_TERMS:

                    if term in text:

                        issues.append(
                            {
                                "id": generate_id(str(p) + term),
                                "artifact": str(p),
                                "governance_term": term,
                                "issue": "governance_contract",
                            }
                        )

                        break

            except Exception:
                pass

    write_log("governance_contract_audit", target, "governance_contract", issues)

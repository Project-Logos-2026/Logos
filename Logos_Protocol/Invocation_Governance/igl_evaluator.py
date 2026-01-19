"""
Invocation Governance Evaluator — NON-EXECUTABLE

Evaluates hypothetical invocation permissibility.
Does NOT invoke protocols.
Does NOT recommend invocation.
"""

from typing import Dict, List

def assess_invocation(pmte_record: Dict, invocation_context: Dict) -> Dict:
    blocking: List[str] = []
    required: List[str] = []

    # PMTE prerequisite
    if pmte_record.get("classification") != "CONDITIONALLY_ADMISSIBLE":
        blocking.append("pmte_forbidden")

    # Authority & persistence checks
    if invocation_context.get("persistence") != "none":
        blocking.append("persistence_risk")

    if invocation_context.get("revocability") != "immediate":
        blocking.append("revocation_insufficient")

    if invocation_context.get("frequency") != "single_step":
        blocking.append("repetition_risk")

    # Compositional ambiguity
    if invocation_context.get("compositional_context"):
        blocking.append("composition_risk")

    if blocking:
        risk_class = "DENIED"
    else:
        risk_class = "STRICTLY_CONSTRAINED"
        required.extend([
            "single_step_only",
            "immediate_revocation",
            "no_persistence",
            "non_composable",
        ])

    return {
        "protocol_id": pmte_record.get("protocol_id", "UNKNOWN"),
        "invocation_risk_class": risk_class,
        "blocking_factors": blocking,
        "required_constraints": required,
        "rationale": "IGL hypothetical assessment only. No invocation permitted.",
        "final_state": "DISCARDED",
    }

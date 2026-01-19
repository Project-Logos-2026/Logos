"""
PMTE Evaluator — NON-EXECUTABLE

This module evaluates protocol artifacts as inert data.
It MUST NOT import, invoke, simulate, or interact with any tool.
"""

from typing import Dict, List

MUST_NEVER_CATEGORIES = [
    "ontological_privation",
    "epistemic_privation",
    "axiological_privation",
    "unauthorized_agency",
    "governance_breach",
]

def evaluate_protocol_artifact(artifact: Dict) -> Dict:
    violations: List[str] = []

    # Fail-closed structural checks
    if artifact.get("execution_surface") != "none":
        violations.append("unauthorized_agency")

    io = artifact.get("io_surface", {})
    if any(io.get(k) for k in ("filesystem", "network", "device")):
        violations.append("governance_breach")

    if not artifact.get("declared_purpose"):
        violations.append("epistemic_privation")

    classification = "CONDITIONALLY_ADMISSIBLE" if not violations else "FORBIDDEN"

    return {
        "protocol_id": artifact.get("protocol_id", "UNKNOWN"),
        "classification": classification,
        "violations": violations,
        "rationale": "PMTE evaluative classification only. No execution permitted.",
        "final_state": "DISCARDED",
    }

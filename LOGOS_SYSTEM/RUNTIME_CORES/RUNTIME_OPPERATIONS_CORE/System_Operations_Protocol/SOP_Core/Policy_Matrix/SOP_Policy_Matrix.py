"""
SOP Policy Matrix
Expanded with metadata and phase validation
Fail-Closed
"""


class SOPPolicyMatrix:

    ALLOWED_PHASES = ["Phase_1", "Phase_5"]

    @staticmethod
    def evaluate(request: dict):

        required_fields = [
            "Core_Block_ID",
            "Overlays",
            "Phase",
            "Trust_Level",
        ]

        for field in required_fields:
            if field not in request:
                raise RuntimeError(
                    f"[FAIL-CLOSED] Missing policy field: {field}"
                )

        if request["Trust_Level"] == "ZERO_TRUST_CLASSIFIED":
            raise RuntimeError("[FAIL-CLOSED] Zero-trust request blocked.")

        if request["Phase"] not in SOPPolicyMatrix.ALLOWED_PHASES:
            raise RuntimeError(
                f"[FAIL-CLOSED] Phase not allowed: {request['Phase']}"
            )

        return {
            "phase_validated": request["Phase"],
            "trust_level": request["Trust_Level"],
        }

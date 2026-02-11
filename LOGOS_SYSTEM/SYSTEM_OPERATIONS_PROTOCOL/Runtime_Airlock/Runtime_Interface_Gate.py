"""
SOP Runtime Interface Gate
Phase 4: DRAC Orchestration Bound
Fail-Closed
"""

from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.DRAC_Integration.DRAC_Handshake import (
    DRACHandshake,
)
from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.DRAC_Integration.DRAC_Orchestration_Bridge import (
    DRACOrchestrationBridge,
)
from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.Audit_Spine.Audit_Logger import (
    AuditLogger,
)


class RuntimeInterfaceGate:

    @staticmethod
    def forward_request(smp: dict):

        # Expect policy-ready structure inside SMP payload
        if "payload" not in smp:
            raise RuntimeError("[FAIL-CLOSED] SMP missing payload.")

        payload = smp["payload"]

        required_fields = [
            "Core_Block_ID",
            "Overlays",
            "Phase",
            "Trust_Level",
        ]

        for field in required_fields:
            if field not in payload:
                raise RuntimeError(
                    f"[FAIL-CLOSED] Payload missing required field: {field}"
                )

        # Step 1: Authorization
        authorization = DRACHandshake.authorize(payload)

        # Step 2: Build compile intent (snapshot manifest)
        compile_intent = DRACOrchestrationBridge.build_compile_intent(authorization)

        # Step 3: Audit full decision chain
        AuditLogger.log(
            {
                "event": "DRAC_COMPILE_INTENT_CREATED",
                "core": compile_intent["core"],
                "phase": compile_intent["phase"],
                "trust_level": compile_intent["trust_level"],
                "manifest_snapshot_hash": compile_intent[
                    "manifest_snapshot_hash"
                ],
                "status": "READY_FOR_DRAC_PIPELINE",
            }
        )

        return {
            "status": "READY_FOR_DRAC_PIPELINE",
            "trace": smp.get("hash", "UNKNOWN"),
            "compile_intent": compile_intent,
        }

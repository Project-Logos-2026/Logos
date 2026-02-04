"""
MODULE: reference_monitor
PHASE: Phase-E (Execution Grounding)
PURPOSE:
- Centralized governance enforcement
"""

import time
from typing import Any, Dict, List

from Logos_System.System_Stack.System_Operations_Protocol.governance.pxl_client import (
    PXLClient,
)


class ProofGateError(Exception):
    """Raised when proof gate fails."""


class KernelHashMismatchError(ProofGateError):
    """Raised when kernel hash does not match expected."""


class ReferenceMonitor:
    def __init__(self, config_path: str | None = None):
        # config_path is retained for compatibility; Phase-E ignores the payload.
        self.client = PXLClient()
        self.decisions: List[Dict[str, Any]] = []
        self.expected_kernel_hash = "DEADBEEF"
        self.audit_log_path = None
        self.config_path = config_path

    def evaluate(self, action: Dict[str, Any]) -> Dict[str, Any]:
        decision = self.client.prove(action)
        record = {
            "timestamp": time.time(),
            "action": action,
            "decision": decision,
        }
        self.decisions.append(record)
        return decision

    def require_proof_token(self, obligation: str, provenance: Any = None) -> Dict[str, Any]:
        result = self.client.prove_box(obligation)
        if not result.get("ok", False):
            raise ProofGateError(result.get("reason", "proof denied"))
        return {"proof_id": result.get("id"), "kernel_hash": result.get("kernel_hash")}

    def health_check(self) -> Dict[str, Any]:
        return {
            "reference_monitor": "ok",
            "expected_kernel_hash": self.expected_kernel_hash,
            "pxl_server": self.client.health(),
            "audit_log_path": self.audit_log_path,
        }

    def evaluate_modal_proposition(self, *args, **kwargs) -> Dict[str, Any]:
        return {"ok": True, "result": "stub"}

    def evaluate_iel_proposition(self, *args, **kwargs) -> Dict[str, Any]:
        return {"ok": True, "result": "stub"}

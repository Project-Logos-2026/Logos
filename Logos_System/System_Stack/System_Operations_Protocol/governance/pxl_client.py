"""
MODULE: pxl_client
PHASE: Phase-E (Execution Grounding)
PURPOSE:
- Provide conservative governance signals
"""

import time
from typing import Any, Dict


class PXLClient:
    def __init__(self, *args, **kwargs):
        # Retain args for backwards compatibility even though Phase-E ignores them.
        self.args = args
        self.kwargs = kwargs

    def health(self) -> Dict[str, Any]:
        return {
            "status": "DEGRADED",
            "timestamp": time.time(),
            "notes": "Phase-E execution grounding active; optional capabilities disabled",
        }

    def health_check(self) -> Dict[str, Any]:
        # Alias for callers expecting the legacy interface.
        return self.health()

    def prove(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(action, dict):
            return {"allowed": False, "reason": "invalid action format"}

        if action.get("type") in {"ACTIVATION_EXECUTION", "AGENT_EXECUTE"}:
            return {"allowed": True, "reason": "Phase-E activation allowed"}

        return {"allowed": False, "reason": "action not permitted in Phase-E"}

    def prove_box(self, obligation: Any, *args, **kwargs) -> Dict[str, Any]:
        # Compatibility shim: wrap prove() to match earlier prover response shape.
        decision = self.prove({"type": obligation} if isinstance(obligation, str) else {})
        allowed = decision.get("allowed", False)
        return {
            "ok": allowed,
            "id": "phase-e-proof",
            "kernel_hash": "DEADBEEF",
            "goal": obligation if isinstance(obligation, str) else "",
            "latency_ms": 0,
            "reason": decision.get("reason", ""),
        }

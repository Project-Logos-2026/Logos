"""
MODULE: Logos_Agent.runtime
PHASE: Phase-G (Agent Deployment)
PURPOSE:
- Deploy a concrete, governed Logos Agent
- Single-action execution only
- Policy-first, fail-closed
NON-GOALS:
- No autonomy
- No loops
- No self-planning
"""

from typing import Any, Dict

from Logos_System.System_Stack.System_Operations_Protocol.governance.reference_monitor import (
    ReferenceMonitor,
)
from Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Agent_Integration.coordinator import (
    coordinate,
)
from Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Agent_Integration.dispatch import (
    dispatch,
)


class LogosAgentRuntime:
    def __init__(self, agent_id: str):
        if not isinstance(agent_id, str) or not agent_id:
            raise ValueError("agent_id must be a non-empty string")

        self.agent_id = agent_id
        self.governance = ReferenceMonitor()

    # -----------------------------
    # Public API
    # -----------------------------
    def receive(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accept a single execution request.
        Fail-closed on any invalidity or denial.
        """
        if not isinstance(request, dict):
            return self._deny("invalid request format")

        if "attestation" not in request:
            return self._deny("missing attestation")

        action = {
            "type": "AGENT_EXECUTE",
            "agent_id": self.agent_id,
            "request": request,
        }

        decision = self.governance.evaluate(action)
        if not decision.get("allowed"):
            return {
                "status": "DENIED",
                "reason": decision.get("reason", "unspecified"),
            }

        # Execute exactly one activation under Phase-E constraints
        audit = coordinate(request)
        result = dispatch({"agent_id": self.agent_id, "audit": audit})

        return {
            "status": "EXECUTED",
            "commit_id": result.get("commit_id"),
        }

    # -----------------------------
    # Helpers
    # -----------------------------
    def _deny(self, reason: str) -> Dict[str, Any]:
        return {"status": "DENIED", "reason": reason}

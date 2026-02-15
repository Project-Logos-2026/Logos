# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: runtime
runtime_layer: inferred
role: Runtime module
responsibility: Provides runtime logic for LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/runtime.py.
agent_binding: Logos_Agent
protocol_binding: None
runtime_classification: runtime_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/runtime.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

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

from LOGOS_SYSTEM.System_Stack.System_Operations_Protocol.governance.reference_monitor import (
    ReferenceMonitor,
)
from LOGOS_SYSTEM.System_Stack.Logos_Protocol.Activation_Sequencer.Agent_Integration.coordinator import (
    coordinate,
)
from LOGOS_SYSTEM.System_Stack.Logos_Protocol.Activation_Sequencer.Agent_Integration.dispatch import (
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

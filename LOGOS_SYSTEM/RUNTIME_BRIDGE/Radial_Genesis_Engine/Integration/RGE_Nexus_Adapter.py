# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: RGE_Nexus_Adapter
runtime_layer: rge_integration
role: Nexus boundary adapter
responsibility: Wraps RGERuntime as a NexusParticipant for StandardNexus registration. Never constructs internal components. Never registers itself. Never modifies Nexus. Fail-closed on all error paths.
agent_binding: None
protocol_binding: None
runtime_classification: integration_adapter
boot_phase: Phase-A-Integration
expected_imports: [Controller.RGE_Bootstrap.RGERuntime, LP_Nexus.Logos_Protocol_Nexus.NexusParticipant, LP_Nexus.Logos_Protocol_Nexus.StatePacket]
provides: [RGENexusAdapter]
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: "All exceptions caught in execute_tick. No rethrow. No partial state. On failure, tick completes silently with no topology recommendation."
rewrite_provenance:
  source: Phase_A_Controlled_Runtime_Entry
  rewrite_phase: Phase_A_Integration
  rewrite_timestamp: 2026-02-21T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import time
from typing import Any, Dict, List, Optional

from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.RGE_Bootstrap import (
    RGERuntime,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    NexusParticipant,
    StatePacket,
)


_ADAPTER_PARTICIPANT_ID = "rge_topology_advisor"


class RGENexusAdapter(NexusParticipant):

    participant_id: str = _ADAPTER_PARTICIPANT_ID

    def __init__(self, rge_runtime: RGERuntime) -> None:
        self._rge = rge_runtime
        self._handle: Any = None
        self._last_result: Optional[Dict[str, Any]] = None
        self._received_packets: List[StatePacket] = []

    def register(self, nexus_handle: Any) -> None:
        self._handle = nexus_handle

    def receive_state(self, packet: StatePacket) -> None:
        self._received_packets.append(packet)

    def execute_tick(self, context: Dict[str, Any]) -> None:
        try:
            telemetry_input = self._extract_telemetry_input(context)

            self._rge.inject_telemetry(
                task_id=telemetry_input["task_id"],
                tick_id=telemetry_input["tick_id"],
                constraints=telemetry_input["constraints"],
                mesh_output=telemetry_input.get("mesh_output"),
                protocol_telemetry=telemetry_input.get("protocol_telemetry"),
                hysteresis_key=telemetry_input.get("hysteresis_key"),
                recursion_telemetry=telemetry_input.get("recursion_telemetry"),
            )

            self._rge.evaluate()

            result = self._rge.select()

            self._last_result = result

        except Exception:
            self._last_result = None
            return

        self._received_packets.clear()

    def project_state(self) -> Optional[StatePacket]:
        if self._last_result is None:
            return None

        if not self._last_result.get("selected", False):
            return None

        print("RGE ADVISORY:", self._last_result)  # TEMPORARY AUDIT PRINT

        return StatePacket(
            source_id=self.participant_id,
            payload={
                "type": "rge_topology_recommendation",
                "content": self._last_result,
            },
            timestamp=time.time(),
            causal_intent="topology_advisory",
        )

    def _extract_telemetry_input(self, context: Dict[str, Any]) -> Dict[str, Any]:
        tick_id = str(context.get("tick_id", ""))
        task_id = str(context.get("task_id", ""))
        constraints = context.get("constraints", [])
        mesh_output = context.get("mesh_output", None)
        protocol_telemetry = context.get("protocol_telemetry", None)
        hysteresis_key = context.get("hysteresis_key", None)
        recursion_telemetry = context.get("recursion_telemetry", None)

        return {
            "task_id": task_id,
            "tick_id": tick_id,
            "constraints": constraints,
            "mesh_output": mesh_output,
            "protocol_telemetry": protocol_telemetry,
            "hysteresis_key": hysteresis_key,
            "recursion_telemetry": recursion_telemetry,
        }

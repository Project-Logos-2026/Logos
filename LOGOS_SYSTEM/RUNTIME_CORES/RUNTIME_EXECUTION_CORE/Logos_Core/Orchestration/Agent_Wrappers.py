# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

from enum import Enum
from typing import Dict, Any, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    NexusParticipant,
    StatePacket,
    NexusHandle,
)


class SMPRoutingState(Enum):
    RECEIVED = 1
    ANALYZED = 2
    PROMOTED = 3
    RESOLVED = 4
    HALTED = 5


class AgentParticipantBase(NexusParticipant):
    def __init__(
        self,
        agent_name: str,
        session_id: str,
        logos_agent_id: str,
        protocol_binding: str,
    ) -> None:
        from typing import List
        self.agent_name = agent_name
        self.session_id = session_id
        self.logos_agent_id = logos_agent_id
        self.protocol_binding = protocol_binding
        self._nexus_handle: Optional[NexusHandle] = None
        self._last_projection: Optional[StatePacket] = None
        self._received_packets: List[StatePacket] = []

    def register(self, nexus_handle: NexusHandle) -> None:
        self._nexus_handle = nexus_handle

    def receive_state(self, packet: StatePacket) -> None:
        self._received_packets.append(packet)
        self._on_receive(packet)

    def execute_tick(self, context: Dict[str, Any]) -> None:
        result = self._on_tick(context)
        projection = self._project()
        self._last_projection = projection
        self._received_packets.clear()

    def project_state(self) -> Optional[StatePacket]:
        return self._last_projection

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        raise NotImplementedError

    def _on_receive(self, packet: StatePacket) -> None:
        pass

    def _project(self) -> Optional[StatePacket]:
        return None


class I1AgentParticipant(AgentParticipantBase):
    participant_id = "agent_i1"

    def __init__(self, session_id: str, logos_agent_id: str, scp_orchestrator) -> None:
        super().__init__("I1", session_id, logos_agent_id, "SCP")
        self._scp_orchestrator = scp_orchestrator

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        smp = context.get("smp")
        if smp is not None:
            aa = self._scp_orchestrator.analyze(smp)
            return {"agent": "I1", "status": "analyzed", "aa_id": aa.aa_id, "aa_type": aa.aa_type}
        return {"agent": "I1", "status": "idle"}

    def _project(self) -> Optional[StatePacket]:
        return None


class I2AgentParticipant(AgentParticipantBase):
    participant_id = "agent_i2"

    def __init__(self, session_id: str, logos_agent_id: str, uwm_reader, canonical_store) -> None:
        super().__init__("I2", session_id, logos_agent_id, "MTP")
        self._uwm_reader = uwm_reader
        self._canonical_store = canonical_store

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        csmp_id = context.get("csmp_id")
        if csmp_id is not None:
            csmp = self._canonical_store.get(csmp_id)
            if csmp:
                rendered_output = csmp.payload.get("input", "")
                return {"agent": "I2", "status": "rendered", "rendered_output": rendered_output}
        return {"agent": "I2", "status": "idle"}

    def _project(self) -> Optional[StatePacket]:
        return None


class I3AgentParticipant(AgentParticipantBase):
    participant_id = "agent_i3"

    def __init__(self, session_id: str, logos_agent_id: str) -> None:
        super().__init__("I3", session_id, logos_agent_id, "ARP")

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        task = context.get("task", {})
        return {
            "agent": "I3",
            "status": "delegated",
            "arp_delegation": "deterministic_placeholder",
            "session_id": self.session_id,
            "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
        }

    def _project(self) -> Optional[StatePacket]:
        return None


class LogosAgentParticipant(AgentParticipantBase):
    participant_id = "agent_logos"

    def __init__(
        self,
        session_id: str,
        logos_agent_id: str,
        smp_store,
        uwm_reader,
        scp_orchestrator,
        promotion_evaluator,
        canonical_producer,
        canonical_store,
    ) -> None:
        super().__init__("LOGOS", session_id, logos_agent_id, "Logos_Protocol")
        self._smp_store = smp_store
        self._uwm_reader = uwm_reader
        self._scp_orchestrator = scp_orchestrator
        self._promotion_evaluator = promotion_evaluator
        self._canonical_producer = canonical_producer
        self._canonical_store = canonical_store
        self.routing_state = SMPRoutingState.RECEIVED
        self._current_smp_id: Optional[str] = None
        self._csmp_id: Optional[str] = None
        self._halt_reason: Optional[str] = None
        self._tick_result: Dict[str, Any] = {"status": "in_progress"}

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet, validate_task
        if "packet" in context:
            validate_route_packet(context["packet"])
        task = context.get("task", {})
        if isinstance(task, dict) and task:
            validate_task(task)
        if self.routing_state == SMPRoutingState.RECEIVED:
            payload = {
                "input": task.get("input", "") if isinstance(task, dict) else "",
                "task": task,
            }
            smp = self._smp_store.create_smp(
                smp_type="input_task",
                payload=payload,
                session_id=self.session_id,
                source="logos_agent",
            )
            self._current_smp_id = smp.header.smp_id
            self.routing_state = SMPRoutingState.ANALYZED
            result: Dict[str, Any] = {"status": "in_progress", "routing_state": "ANALYZED"}
        elif self.routing_state == SMPRoutingState.ANALYZED:
            smp = self._smp_store.get_smp(self._current_smp_id)
            aa = self._scp_orchestrator.analyze(smp)
            self._smp_store.append_aa(self._current_smp_id, "I1AA", "I1", aa.content)
            self._smp_store.promote_classification(self._current_smp_id, "provisional")
            self.routing_state = SMPRoutingState.PROMOTED
            result = {"status": "in_progress", "routing_state": "PROMOTED"}
        elif self.routing_state == SMPRoutingState.PROMOTED:
            smp = self._smp_store.get_smp(self._current_smp_id)
            i2_aa_content = {
                "rendered_output": f"Resolved: {smp.payload.get('input', '')}",
                "session_id": self.session_id,
            }
            self._smp_store.append_aa(self._current_smp_id, "I2AA", "I2", i2_aa_content)
            i3_aa_content = {
                "arp_delegation": "deterministic_placeholder",
                "session_id": self.session_id,
                "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
            }
            self._smp_store.append_aa(self._current_smp_id, "I3AA", "I3", i3_aa_content)
            eval_result = self._promotion_evaluator.evaluate_for_canonical(self._current_smp_id)
            if eval_result.eligible:
                aas = self._uwm_reader.get_aas_for_smp(
                    self._current_smp_id, requester_role="logos_agent"
                )
                smp = self._smp_store.get_smp(self._current_smp_id)
                csmp = self._canonical_producer.produce(smp, aas)
                self._canonical_store.store(csmp)
                self._csmp_id = csmp.header.smp_id
                self.routing_state = SMPRoutingState.RESOLVED
                result = {"status": "in_progress", "routing_state": "RESOLVED"}
            else:
                self._halt_reason = f"promotion_ineligible:{eval_result.missing_requirements}"
                self.routing_state = SMPRoutingState.HALTED
                result = {
                    "status": "halted",
                    "halt_reason": self._halt_reason,
                    "smp_id": self._current_smp_id,
                }
        elif self.routing_state == SMPRoutingState.RESOLVED:
            csmp = self._canonical_store.get(self._csmp_id)
            rendered_output = csmp.payload.get("input", "") if csmp else ""
            result = {
                "status": "completed",
                "smp_id": self._current_smp_id,
                "csmp_id": self._csmp_id,
                "classification": "canonical",
                "rendered_output": rendered_output,
            }
        elif self.routing_state == SMPRoutingState.HALTED:
            result = {
                "status": "halted",
                "halt_reason": self._halt_reason or "routing_halted",
                "smp_id": self._current_smp_id,
            }
        else:
            result = {"status": "halted", "halt_reason": "unknown_routing_state"}
        self._tick_result = result
        return result

    def _project(self) -> Optional[StatePacket]:
        return None

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

from typing import Dict, Any, Optional
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    NexusParticipant,
    StatePacket,
    NexusHandle,
)


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

    def __init__(
        self,
        session_id: str,
        logos_agent_id: str,
        smp_store,
        uwm_read_api,
        scp_orchestrator,
        promotion_evaluator,
        canonical_smp_producer,
        csp_canonical_store,
        mtp_nexus,
        arp_compiler,
    ) -> None:
        super().__init__("I1", session_id, logos_agent_id, "SCP")
        self._smp_store = smp_store
        self._uwm_read_api = uwm_read_api
        self._scp_orchestrator = scp_orchestrator
        self._promotion_evaluator = promotion_evaluator
        self._canonical_smp_producer = canonical_smp_producer
        self._csp_canonical_store = csp_canonical_store
        self._mtp_nexus = mtp_nexus
        self._arp_compiler = arp_compiler

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        smp_id = context.get("smp_id")
        if not smp_id:
            return {"agent": "I1", "status": "stub_tick"}
        aas = self._uwm_read_api.get_aas_for_smp(smp_id, requester_role="logos_agent")
        for aa in aas:
            aa_type = aa.get("aa_type") if isinstance(aa, dict) else getattr(aa, "aa_type", None)
            source = aa.get("source_agent") if isinstance(aa, dict) else getattr(aa, "source_agent", None)
            if aa_type == "I1AA" or source == "I1":
                return {"agent": "I1", "status": "already_present", "smp_id": smp_id}
        smp = self._smp_store.get_smp(smp_id)
        aa = self._scp_orchestrator.analyze(smp)
        self._smp_store.append_aa(smp_id, "I1AA", "I1", aa.content)
        return {"agent": "I1", "status": "appended", "smp_id": smp_id}

    def _project(self) -> Optional[StatePacket]:
        return None


class I2AgentParticipant(AgentParticipantBase):
    participant_id = "agent_i2"

    def __init__(
        self,
        session_id: str,
        logos_agent_id: str,
        smp_store,
        uwm_read_api,
        scp_orchestrator,
        promotion_evaluator,
        canonical_smp_producer,
        csp_canonical_store,
        mtp_nexus,
        arp_compiler,
    ) -> None:
        super().__init__("I2", session_id, logos_agent_id, "MTP")
        self._smp_store = smp_store
        self._uwm_read_api = uwm_read_api
        self._uwm_reader = uwm_read_api  # compat alias for existing _on_tick
        self._scp_orchestrator = scp_orchestrator
        self._promotion_evaluator = promotion_evaluator
        self._canonical_smp_producer = canonical_smp_producer
        self._csp_canonical_store = csp_canonical_store
        self._canonical_store = csp_canonical_store  # compat alias for existing _on_tick
        self._mtp_nexus = mtp_nexus
        self._arp_compiler = arp_compiler

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        smp_id = context.get("smp_id")
        if not smp_id:
            return {"agent": "I2", "status": "stub_tick"}
        aas = self._uwm_read_api.get_aas_for_smp(smp_id, requester_role="logos_agent")
        for aa in aas:
            aa_type = aa.get("aa_type") if isinstance(aa, dict) else getattr(aa, "aa_type", None)
            source = aa.get("source_agent") if isinstance(aa, dict) else getattr(aa, "source_agent", None)
            if aa_type == "I2AA" or source == "I2":
                return {"agent": "I2", "status": "already_present", "smp_id": smp_id}
        smp = self._smp_store.get_smp(smp_id)
        i2_content = {"rendered_output": f"Resolved: {smp.payload.get('input', '')}", "session_id": self.session_id}
        self._smp_store.append_aa(smp_id, "I2AA", "I2", i2_content)
        return {"agent": "I2", "status": "appended", "smp_id": smp_id}

    def _project(self) -> Optional[StatePacket]:
        return None


class I3AgentParticipant(AgentParticipantBase):
    participant_id = "agent_i3"

    def __init__(
        self,
        session_id: str,
        logos_agent_id: str,
        smp_store,
        uwm_read_api,
        scp_orchestrator,
        promotion_evaluator,
        canonical_smp_producer,
        csp_canonical_store,
        mtp_nexus,
        arp_compiler,
    ) -> None:
        super().__init__("I3", session_id, logos_agent_id, "ARP")
        self._smp_store = smp_store
        self._uwm_read_api = uwm_read_api
        self._scp_orchestrator = scp_orchestrator
        self._promotion_evaluator = promotion_evaluator
        self._canonical_smp_producer = canonical_smp_producer
        self._csp_canonical_store = csp_canonical_store
        self._mtp_nexus = mtp_nexus
        self._arp_compiler = arp_compiler

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet
        if "packet" in context:
            validate_route_packet(context["packet"])
        smp_id = context.get("smp_id")
        if not smp_id:
            return {"agent": "I3", "status": "stub_tick"}
        aas = self._uwm_read_api.get_aas_for_smp(smp_id, requester_role="logos_agent")
        for aa in aas:
            aa_type = aa.get("aa_type") if isinstance(aa, dict) else getattr(aa, "aa_type", None)
            source = aa.get("source_agent") if isinstance(aa, dict) else getattr(aa, "source_agent", None)
            if aa_type == "I3AA" or source == "I3":
                return {"agent": "I3", "status": "already_present", "smp_id": smp_id}
        i3_content = {"arp_delegation": "deterministic_placeholder", "session_id": self.session_id}
        self._smp_store.append_aa(smp_id, "I3AA", "I3", i3_content)
        return {"agent": "I3", "status": "appended", "smp_id": smp_id}

    def _project(self) -> Optional[StatePacket]:
        return None


class LogosAgentParticipant(AgentParticipantBase):
    participant_id = "agent_logos"

    def __init__(
        self,
        session_id: str,
        logos_agent_id: str,
        smp_store,
        uwm_read_api,
        scp_orchestrator,
        promotion_evaluator,
        canonical_smp_producer,
        csp_canonical_store,
        mtp_nexus,
        arp_compiler,
    ) -> None:
        super().__init__("LOGOS", session_id, logos_agent_id, "Logos_Protocol")
        self._smp_store = smp_store
        self._uwm_read_api = uwm_read_api
        self._uwm_reader = uwm_read_api  # compat alias for existing _on_tick
        self._scp_orchestrator = scp_orchestrator
        self._promotion_evaluator = promotion_evaluator
        self._canonical_smp_producer = canonical_smp_producer
        self._canonical_producer = canonical_smp_producer  # compat alias for existing _on_tick
        self._csp_canonical_store = csp_canonical_store
        self._canonical_store = csp_canonical_store  # compat alias for existing _on_tick
        self._mtp_nexus = mtp_nexus
        self._arp_compiler = arp_compiler
        self._current_smp_id: Optional[str] = None
        self._csmp_id: Optional[str] = None
        self._routing_state: str = "INIT"

    def _on_tick(self, context: Dict[str, Any]) -> Dict[str, Any]:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_route_packet, validate_task
        if "packet" in context:
            validate_route_packet(context["packet"])
        if self._routing_state == "INIT":
            task = context.get("task", {})
            if isinstance(task, dict) and task:
                validate_task(task)
            smp = self._smp_store.create_smp(
                smp_type="input_task",
                payload={"input": task.get("input", "") if isinstance(task, dict) else "", "task": task},
                session_id=self.session_id,
                source="logos_agent",
            )
            self._current_smp_id = smp.header.smp_id
            self._routing_state = "SMP_CREATED"
            return {"agent": "LOGOS", "status": "in_progress", "smp_id": self._current_smp_id}
        elif self._routing_state == "SMP_CREATED":
            smp = self._smp_store.get_smp(self._current_smp_id)
            aa = self._scp_orchestrator.analyze(smp)
            self._smp_store.append_aa(self._current_smp_id, aa.aa_type, "I1", aa.content)
            self._smp_store.promote_classification(self._current_smp_id, "provisional")
            self._routing_state = "I1_COMPLETE"
            return {
                "agent": "LOGOS",
                "status": "in_progress",
                "routing_state": "I1_COMPLETE",
                "smp_id": self._current_smp_id,
            }
        elif self._routing_state == "I1_COMPLETE":
            smp = self._smp_store.get_smp(self._current_smp_id)
            i3_aa_content = {
                "arp_delegation": "deterministic_placeholder",
                "session_id": self.session_id,
            }
            self._smp_store.append_aa(self._current_smp_id, "I3AA", "I3", i3_aa_content)
            self._routing_state = "I3_COMPLETE"
            return {
                "agent": "LOGOS",
                "status": "in_progress",
                "routing_state": "I3_COMPLETE",
                "smp_id": self._current_smp_id,
            }
        elif self._routing_state == "I3_COMPLETE":
            smp = self._smp_store.get_smp(self._current_smp_id)
            i2_aa_content = {
                "rendered_output": f"Resolved: {smp.payload.get('input', '')}",
                "session_id": self.session_id,
            }
            self._smp_store.append_aa(self._current_smp_id, "I2AA", "I2", i2_aa_content)
            self._routing_state = "I2_COMPLETE"
            return {
                "agent": "LOGOS",
                "status": "in_progress",
                "routing_state": "I2_COMPLETE",
                "smp_id": self._current_smp_id,
            }
        elif self._routing_state == "I2_COMPLETE":
            eval_result = self._promotion_evaluator.evaluate_for_canonical(self._current_smp_id)
            if eval_result.eligible:
                self._routing_state = "RESOLVED_PENDING"
                return {
                    "agent": "LOGOS",
                    "status": "in_progress",
                    "routing_state": "RESOLVED_PENDING",
                    "smp_id": self._current_smp_id,
                }
            else:
                self._routing_state = "HALTED"
                return {
                    "agent": "LOGOS",
                    "status": "halted",
                    "halt_reason": f"promotion_ineligible:{eval_result.missing_requirements}",
                    "smp_id": self._current_smp_id,
                }
        elif self._routing_state == "RESOLVED_PENDING":
            aas = self._uwm_reader.get_aas_for_smp(
                self._current_smp_id, requester_role="logos_agent"
            )
            smp = self._smp_store.get_smp(self._current_smp_id)
            csmp = self._canonical_smp_producer.produce(smp, aas)
            self._canonical_store.store(csmp)
            self._csmp_id = csmp.header.smp_id
            self._routing_state = "RESOLVED"
            return {
                "agent": "LOGOS",
                "status": "completed",
                "smp_id": self._current_smp_id,
                "csmp_id": self._csmp_id,
                "classification": "canonical",
                "rendered_output": smp.payload.get("input", ""),
            }
        return {"agent": "LOGOS", "status": "stub_tick"}

    def _project(self) -> Optional[StatePacket]:
        return None

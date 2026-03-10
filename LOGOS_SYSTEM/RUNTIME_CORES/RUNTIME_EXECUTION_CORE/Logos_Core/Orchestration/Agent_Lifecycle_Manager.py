from enum import Enum

class LifecycleState(Enum):
    INITIALIZED = "INITIALIZED"
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    HALTED = "HALTED"

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

from typing import Dict, Any
from .Agent_Wrappers import (
    I1AgentParticipant,
    I2AgentParticipant,
    I3AgentParticipant,
    LogosAgentParticipant,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    NexusParticipant,
)
from logos.imports.protocols import SMPStore
from logos.imports.protocols import UWMReadAPI
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.SCP_Orchestrator import SCPOrchestrator
from logos.imports.protocols import PromotionEvaluator
from logos.imports.protocols import CanonicalSMPProducer
from logos.imports.protocols import CSPCanonicalStore


class LifecycleHalt(Exception):
    pass


class AgentLifecycleManager:
    def _transition_state(self, participant_id: str, new_state: LifecycleState) -> None:
        current_state = self._participant_states.get(participant_id)
        legal = {
            LifecycleState.INITIALIZED: LifecycleState.REGISTERED,
            LifecycleState.REGISTERED: LifecycleState.ACTIVE,
            LifecycleState.ACTIVE: LifecycleState.HALTED,
        }
        if current_state is None:
            # Only allow INITIALIZED as first state
            if new_state != LifecycleState.INITIALIZED:
                raise LifecycleHalt(f"Illegal initial state for {participant_id}: {new_state}")
        else:
            if legal.get(current_state) != new_state:
                raise LifecycleHalt(f"Illegal transition for {participant_id}: {current_state} -> {new_state}")
        self._participant_states[participant_id] = new_state

    def __init__(self, startup_context: Dict[str, Any]) -> None:
        if not isinstance(startup_context, dict):
            raise LifecycleHalt("Invalid startup_context")

        if startup_context.get("status") != "LOGOS_AGENT_READY":
            raise LifecycleHalt("Startup status invalid")

        identity = startup_context.get("logos_identity")
        if not isinstance(identity, dict):
            raise LifecycleHalt("Missing logos_identity")

        logos_agent_id = identity.get("logos_agent_id")
        session_id = identity.get("session_id")

        if not logos_agent_id or not isinstance(logos_agent_id, str):
            raise LifecycleHalt("Invalid logos_agent_id")

        if not session_id or not isinstance(session_id, str):
            raise LifecycleHalt("Invalid session_id")

        plan = startup_context.get("agent_orchestration_plan")
        if not isinstance(plan, dict):
            raise LifecycleHalt("Missing agent_orchestration_plan")

        self._startup_context = startup_context
        self._logos_agent_id = logos_agent_id
        self._session_id = session_id
        self._plan = plan
        self._participants: Dict[str, NexusParticipant] = {}
        self._activated = False
        self._participant_states: Dict[str, LifecycleState] = {}

    def activate(self) -> Dict[str, NexusParticipant]:
        try:
            smp_store = SMPStore()
            uwm_read_api = UWMReadAPI(smp_store)
            scp_orchestrator = SCPOrchestrator()
            promotion_evaluator = PromotionEvaluator(uwm_read_api)
            canonical_smp_producer = CanonicalSMPProducer()
            csp_canonical_store = CSPCanonicalStore()
            mtp_nexus = None  # stub — not activated in P3.1
            arp_compiler = None  # stub — not activated in P3.1
            _shared = (
                smp_store,
                uwm_read_api,
                scp_orchestrator,
                promotion_evaluator,
                canonical_smp_producer,
                csp_canonical_store,
                mtp_nexus,
                arp_compiler,
            )
            i1 = I1AgentParticipant(self._session_id, self._logos_agent_id, *_shared)
            i2 = I2AgentParticipant(self._session_id, self._logos_agent_id, *_shared)
            i3 = I3AgentParticipant(self._session_id, self._logos_agent_id, *_shared)
            logos = LogosAgentParticipant(self._session_id, self._logos_agent_id, *_shared)
        except Exception as e:
            raise LifecycleHalt(f"Agent construction failed: {e}")

        self._participants = {
            "agent_i1": i1,
            "agent_i2": i2,
            "agent_i3": i3,
            "agent_logos": logos,
        }
        # Set INITIALIZED and transition to REGISTERED
        for pid in self._participants:
            self._transition_state(pid, LifecycleState.INITIALIZED)
            self._transition_state(pid, LifecycleState.REGISTERED)
        self._activated = True  # Legacy guard
        return self._participants

    def get_session_id(self) -> str:
        return self._session_id

    def get_logos_agent_id(self) -> str:
        return self._logos_agent_id

    def get_participants(self) -> Dict[str, NexusParticipant]:
        for pid in self._participants:
            if self._participant_states.get(pid) != LifecycleState.REGISTERED:
                raise LifecycleHalt(f"Participant {pid} not in REGISTERED state")
        return self._participants

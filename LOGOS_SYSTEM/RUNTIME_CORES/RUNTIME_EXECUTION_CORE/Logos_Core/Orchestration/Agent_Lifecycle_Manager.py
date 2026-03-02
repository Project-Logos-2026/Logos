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


class LifecycleHalt(Exception):
    pass


class AgentLifecycleManager:
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

    def activate(self) -> Dict[str, NexusParticipant]:
        try:
            i1 = I1AgentParticipant(self._session_id, self._logos_agent_id)
            i2 = I2AgentParticipant(self._session_id, self._logos_agent_id)
            i3 = I3AgentParticipant(self._session_id, self._logos_agent_id)
            logos = LogosAgentParticipant(self._session_id, self._logos_agent_id)
        except Exception as e:
            raise LifecycleHalt(f"Agent construction failed: {e}")

        self._participants = {
            "agent_i1": i1,
            "agent_i2": i2,
            "agent_i3": i3,
            "agent_logos": logos,
        }

        self._activated = True
        return self._participants

    def get_session_id(self) -> str:
        return self._session_id

    def get_logos_agent_id(self) -> str:
        return self._logos_agent_id

    def get_participants(self) -> Dict[str, NexusParticipant]:
        if not self._activated:
            raise LifecycleHalt("activate() not yet called")
        return self._participants

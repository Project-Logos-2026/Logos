# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

from typing import Dict, Any, Optional, Protocol
import sys

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Agent_Lifecycle_Manager import (
    AgentLifecycleManager,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Nexus_Factory import (
    NexusFactory,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    StandardNexus,
)


# ----------------------------------------
# TaskSource / OutputSink Contracts
# ----------------------------------------

class TaskSource(Protocol):
    def get_task(self) -> Optional[Dict[str, Any]]:
        ...


class OutputSink(Protocol):
    def emit(self, result: Dict[str, Any]) -> None:
        ...


class StdinTaskSource:
    def get_task(self) -> Optional[Dict[str, Any]]:
        import json
        try:
            line = sys.stdin.readline()
            if not line:
                return None
            obj = None
            try:
                obj = json.loads(line.strip())
            except Exception:
                return None
            if not isinstance(obj, dict):
                return None
            return obj
        except Exception:
            return None


class StdoutOutputSink:
    def emit(self, result: Dict[str, Any]) -> None:
        import json
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": "Non-dict result emitted"}))


class SingleTaskSource:
    def __init__(self, task: Dict[str, Any]) -> None:
        self._task = task
        self._used = False

    def get_task(self) -> Optional[Dict[str, Any]]:
        if self._used:
            return None
        self._used = True
        return self._task


# ----------------------------------------
# RuntimeLoop
# ----------------------------------------

class RuntimeLoop:

    def __init__(
        self,
        startup_context: Dict[str, Any],
        task_source: Optional[TaskSource] = None,
        output_sink: Optional[OutputSink] = None,
    ) -> None:

        self._startup_context = startup_context
        self._task_source = task_source or StdinTaskSource()
        self._output_sink = output_sink or StdoutOutputSink()

        # Activate agents
        self._alm = AgentLifecycleManager(startup_context)
        participants = self._alm.activate()

        # Build LP Nexus
        self._nexus: StandardNexus = NexusFactory.build_lp_nexus(participants)

        self._running = False

    # ----------------------------------------
    # Blocking main loop
    # ----------------------------------------

    def run(self) -> None:
        self._running = True

        while self._running:
            task = self._task_source.get_task()
            if task is None:
                break

            result = self._execute_tick(task)
            self._output_sink.emit(result)

    # ----------------------------------------
    # Single tick execution
    # ----------------------------------------

    def run_single(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return self._execute_tick(task)

    # ----------------------------------------
    # Tick execution contract
    # ----------------------------------------

    def _execute_tick(self, task: Dict[str, Any]) -> Dict[str, Any]:

        try:
            causal_intent = task.get("input") if isinstance(task, dict) else None
            self._nexus.tick(causal_intent)

            result = {
                "status": "TICK_COMPLETE",
                "session_id": self._alm.get_session_id(),
                "logos_agent_id": self._alm.get_logos_agent_id(),
                "task": task,
                "participants": list(self._alm.get_participants().keys()),
                "mre_state": "UNKNOWN",  # P1 scope placeholder
                "constraints_applied": False,
                "ms_pipeline_invoked": False,
                "error": None,
            }

            return result

        except Exception as e:
            return {
                "status": "TICK_FAILED",
                "session_id": self._alm.get_session_id(),
                "logos_agent_id": self._alm.get_logos_agent_id(),
                "task": task,
                "participants": [],
                "mre_state": "ERROR",
                "constraints_applied": False,
                "ms_pipeline_invoked": False,
                "error": str(e),
            }

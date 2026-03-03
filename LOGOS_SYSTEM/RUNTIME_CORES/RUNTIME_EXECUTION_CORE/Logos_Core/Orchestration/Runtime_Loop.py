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
    LifecycleState,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Nexus_Factory import (
    NexusFactory,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    StandardNexus,
)
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Agent_Wrappers import (
    LogosAgentParticipant,
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
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Boundary_Validators import validate_startup_context
        validate_startup_context(startup_context)
        self._startup_context = startup_context
        self._task_source = task_source or StdinTaskSource()
        self._output_sink = output_sink or StdoutOutputSink()
        self._alm = AgentLifecycleManager(startup_context)
        participants = self._alm.activate()
        self._participants = participants
        self._nexus: StandardNexus = NexusFactory.build_lp_nexus(participants)
        self._running = False
        self._first_tick = True
        self._initial_participant_ids = sorted(participants.keys())
        self._integration_wired = False

    # ----------------------------------------
    # Blocking main loop
    # ----------------------------------------

    def run(self) -> None:
        self._running = True

        while self._running:
            task = self._task_source.get_task()
            if task is None:
                break

            result = self._process_task(task)
            self._output_sink.emit(result)

    # ----------------------------------------
    # Single tick execution
    # ----------------------------------------

    def run_single(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return self._process_task(task)

    # ----------------------------------------
    # Multi-tick task processing
    # ----------------------------------------

    def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # REM-04: Integration hook — fail-closed until RGE/MSPC artifacts implemented
        integration_error = self._attempt_rge_mspc_wiring()
        if integration_error is not None:
            return {
                "tick_id": 0,
                "session_id": self._alm.get_session_id(),
                "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
                "status": "halted",
                "rendered_output": None,
                "smp_id": None,
                "csmp_id": None,
                "classification": None,
                "halt_reason": integration_error,
            }
        tick_counter = 0
        while tick_counter < 50:
            result = self._execute_tick(task, tick_counter)
            if result.get("status") in {"completed", "halted"}:
                return result
            tick_counter += 1
        return {
            "tick_id": tick_counter,
            "session_id": self._alm.get_session_id(),
            "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
            "status": "halted",
            "rendered_output": None,
            "smp_id": None,
            "csmp_id": None,
            "classification": None,
            "halt_reason": "max_ticks_exceeded",
        }

    # ----------------------------------------
    # REM-04: RGE ↔ MSPC Integration Wiring
    # ----------------------------------------

    def _attempt_rge_mspc_wiring(self) -> Optional[str]:
        """
        Attempts one-time RGE ↔ MSPC participant registration.

        Returns None on success (wiring complete).
        Returns a deterministic error string on failure (fail-closed).

        NotImplementedError from stub builders is treated as a hard halt,
        not a silent skip. Integration is mandatory once builders are present.

        Authority: LOGOS_V1_P3_Integration_Wiring_Spec.md §3
        """
        if self._integration_wired:
            return None
        try:
            rge_adapter = NexusFactory.build_rge_adapter(None)
            topology_provider = NexusFactory.build_topology_provider()
            mspc_pipeline = NexusFactory.build_mspc_pipeline(None)

            # Collect new participants with deterministic ordering
            new_participants = {
                rge_adapter.participant_id: rge_adapter,
                topology_provider.participant_id: topology_provider,
                mspc_pipeline.participant_id: mspc_pipeline,
            }

            # Register into ALM lifecycle, then nexus — in sorted order
            for pid in sorted(new_participants.keys()):
                if pid in self._participants:
                    raise RuntimeError(
                        f"LifecycleSymmetryHalt: Duplicate participant_id '{pid}' during REM-04 wiring"
                    )
                self._participants[pid] = new_participants[pid]
                self._alm._participant_states[pid] = LifecycleState.REGISTERED
                self._nexus.register_participant(new_participants[pid])

            # Expand registry freeze to include integration participants
            self._initial_participant_ids = sorted(self._participants.keys())

            self._integration_wired = True
            return None
        except NotImplementedError as e:
            return f"REM-04 integration artifacts not implemented: {e}"

    # ----------------------------------------
    # Tick execution contract
    # ----------------------------------------

    def _execute_tick(self, task: Dict[str, Any], tick_id: int) -> Dict[str, Any]:
        try:
            # Freeze registry and enforce sorted order
            current_ids = sorted(self._participants.keys())
            if current_ids != self._initial_participant_ids:
                raise RuntimeError("RuntimeActivationHalt: Participant registry mutated during tick")
            # Enforce nexus/ALM registry symmetry
            nexus_ids = sorted(self._nexus.participants.keys())
            if nexus_ids != current_ids:
                raise RuntimeError("LifecycleSymmetryHalt: Nexus registry diverged from ALM registry")
            # First tick: transition REGISTERED -> ACTIVE
            if self._first_tick:
                for pid in current_ids:
                    self._alm._transition_state(pid, LifecycleState.ACTIVE)
                self._first_tick = False
            # Enforce all ACTIVE before tick
            for pid in current_ids:
                if self._alm._participant_states.get(pid) != LifecycleState.ACTIVE:
                    raise RuntimeError(f"LifecycleHalt: Participant {pid} not ACTIVE before tick")
            causal_intent = task.get("input") if isinstance(task, dict) else None
            self._nexus.tick(causal_intent, task_context={"task": task})
            logos_participant = self._participants.get("agent_logos")
            if isinstance(logos_participant, LogosAgentParticipant):
                raw = logos_participant._tick_result
                return {
                    "tick_id": tick_id,
                    "session_id": self._alm.get_session_id(),
                    "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
                    "status": raw.get("status"),
                    "rendered_output": raw.get("rendered_output"),
                    "smp_id": raw.get("smp_id"),
                    "csmp_id": raw.get("csmp_id"),
                    "classification": raw.get("classification"),
                    "halt_reason": raw.get("halt_reason"),
                }
            return {
                "tick_id": tick_id,
                "session_id": self._alm.get_session_id(),
                "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
                "status": "no_output",
                "rendered_output": None,
                "smp_id": None,
                "csmp_id": None,
                "classification": None,
                "halt_reason": None,
            }
        except Exception as e:
            return {
                "tick_id": tick_id,
                "session_id": self._alm.get_session_id(),
                "task_id": task.get("task_id", "") if isinstance(task, dict) else "",
                "status": "halted",
                "rendered_output": None,
                "smp_id": None,
                "csmp_id": None,
                "classification": None,
                "halt_reason": str(e),
            }
    def halt(self) -> None:
        # Transition all ACTIVE participants to HALTED
        for pid in self._initial_participant_ids:
            if self._alm._participant_states.get(pid) == LifecycleState.ACTIVE:
                self._alm._transition_state(pid, LifecycleState.HALTED)
        self._running = False

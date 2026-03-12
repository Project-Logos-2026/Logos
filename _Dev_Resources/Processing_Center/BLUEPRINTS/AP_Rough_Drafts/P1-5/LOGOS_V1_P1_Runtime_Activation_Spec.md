# LOGOS V1 — Phase P1: Runtime Activation Design Specification

**Document ID:** `LOGOS-V1-P1-RUNTIME-ACTIVATION`
**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires human governance ratification
**Parent:** `LOGOS_V1_Operational_Readiness_Blueprint.md`
**Phase:** P1 (first development phase, post-M6)
**Date:** 2026-03-01

---

## 0. Cross-Reference Index

This document is cited as `LOGOS-V1-P1` in all downstream artifacts.

| Reference ID | Section | Description |
|---|---|---|
| P1.1 | §3 | Agent Lifecycle Manager |
| P1.2 | §4 | Nexus Construction Factory |
| P1.3 | §5 | Main Tick Loop |
| P1.4 | §6 | Startup-to-Runtime Handoff |
| P1-IF-01 | §2.1 | NexusParticipant interface contract |
| P1-IF-02 | §2.2 | StandardNexus tick contract |
| P1-IF-03 | §2.3 | Startup output contract |
| P1-IF-04 | §2.4 | Orchestration plan contract |
| P1-IF-05 | §3.4 | Agent wrapper interface contract |
| P1-IF-06 | §5.3 | RuntimeLoop public interface |
| P1-IF-07 | §5.5 | Tick result contract |

---

## 1. Problem Statement

The LOGOS startup chain is fully operational. It executes:

```
START_LOGOS()
  → environment verification
  → Lock-and-Key (dual-site LEM admission)
  → start_logos_agent() (session envelope)
  → discharge_lem() (LOGOS agent identity)
  → prepare_agent_orchestration() (declarative binding plan)
  → return {"status": "LOGOS_AGENT_READY", ...}
```

**The chain terminates here.** `RUN_LOGOS_SYSTEM()` in `STARTUP/LOGOS_SYSTEM.py` returns a dict to `START_LOGOS.py`, which does nothing further. The operational logger is closed. No agents are instantiated. No Nexus is constructed. No tick loop runs. No task can be processed.

P1 bridges this gap. After P1, LOGOS can accept a task, execute a governed tick, and produce output.

---

## 2. Existing Contracts (Verified from Repository)

These are the exact interfaces P1 must consume and implement against. Every method signature, field name, and dataclass is taken directly from canonical repo modules.

### 2.1 NexusParticipant Interface (P1-IF-01)

**Source:** Defined identically in LP_Nexus, SCP_Nexus, ARP_Nexus, CSP_Nexus, SOP_Nexus, DRAC_Nexus, EMP_Nexus. The canonical import path for P1 is from LP_Nexus.

**Import:**
```python
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus import (
    NexusParticipant,
    StatePacket,
    NexusHandle,
)
```

**Interface:**
```python
class NexusParticipant:
    participant_id: str  # class attribute, must be set

    def register(self, nexus_handle: NexusHandle) -> None:
        """Called by Nexus during registration. Store handle for emit()."""
        raise NotImplementedError

    def receive_state(self, packet: StatePacket) -> None:
        """Called by Nexus to deliver routed StatePackets from other participants."""
        raise NotImplementedError

    def execute_tick(self, context: Dict[str, Any]) -> None:
        """Called by Nexus during tick execution. Context contains tick_id, causal_intent, and MRE state."""
        raise NotImplementedError

    def project_state(self) -> Optional[StatePacket]:
        """Called by Nexus after all execute_tick calls. Return a StatePacket or None."""
        raise NotImplementedError
```

**StatePacket:**
```python
@dataclass(frozen=True)
class StatePacket:
    source_id: str
    payload: Dict[str, Any]
    timestamp: float
    causal_intent: Optional[str] = None
```

**NexusHandle:**
```python
class NexusHandle:
    def emit(self, payload: Dict[str, Any], causal_intent: Optional[str] = None) -> None:
        """Emit a StatePacket into the Nexus inbox. Applies provisional proof tagging on egress."""
```

**Mesh constraint on emit payloads:** All emitted payloads MUST contain `"type"` and `"content"` keys or they will be rejected by MeshEnforcer/IonMeshEnforcer.

**Reference implementation:** `RGENexusAdapter` in `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/RGE_Nexus_Adapter.py` — the only existing NexusParticipant implementation in the repo.

### 2.2 StandardNexus Tick Contract (P1-IF-02)

**Source:** `LP_Nexus/Logos_Protocol_Nexus.py`

**Constructor (LP Nexus variant):**
```python
class StandardNexus:
    def __init__(self, mesh: MeshEnforcer, mre_governor: MREGovernor):
```

**Note:** The EMP Nexus uses a four-argument constructor `(mesh, mre_governor, pre_gate, post_gate)`. LP Nexus uses two arguments. P1 uses the LP Nexus.

**Registration:**
```python
def register_participant(self, participant: NexusParticipant) -> None:
    # Requires participant.participant_id to be set
    # Raises NexusViolation on missing or duplicate participant_id
    # Creates NexusHandle and calls participant.register(handle)
```

**Tick execution sequence (exact order from repo):**
```
nexus.tick(causal_intent=None)
  1. tick_counter += 1
  2. Snapshot inbox (swap to empty list)
  3. Route inbound packets to all participants (except source)
  4. For each participant in sorted(participants.keys()):
     a. context = mre.pre_execute(pid)  → raises MREHalt if RED
     b. context.update({"tick_id": tick_id, ...})
     c. participant.execute_tick(context)
     d. mre.post_execute(pid)  → raises MREHalt if RED
  5. Collect project_state() from all participants
  6. Apply provisional proof tagging to projections
  7. Mesh-validate projections
  8. Route projections to all participants (except source)
```

**Critical implication for participant_id naming:** Participants execute in `sorted()` order. This means lexicographic ASCII ordering of `participant_id` strings determines execution sequence within a tick. The M6 blueprint relies on this for ensuring RGE executes before MSPC.

### 2.3 Startup Output Contract (P1-IF-03)

**Source:** `STARTUP/LOGOS_SYSTEM.py`, function `RUN_LOGOS_SYSTEM()`

The startup chain returns this exact structure:

```python
{
    "status": "LOGOS_AGENT_READY",
    "logos_identity": {
        "status": "LEM_DISCHARGED",
        "session_id": str,              # universal session ID from Lock-and-Key
        "logos_agent_id": str,           # "LOGOS:{session_id}"
        "issued_agents": {},             # empty dict (stub)
        "issued_protocols": {},          # empty dict (stub)
        "authority": {},                 # empty dict (stub)
    },
    "logos_session": {
        "status": "LOGOS_SESSION_ESTABLISHED",
        "session_id": str,
        "verified_context": dict,        # full verified context from startup
        "execution": "FORBIDDEN",        # session envelope is non-executing
    },
    "constructive_compile_output": {
        "logos_agent_id": str,
        "universal_session_id": str,
        "prepared_bindings": {
            "issued_agents": {},
            "issued_protocols": {},
            "authority": {},
        },
    },
    "agent_orchestration_plan": {
        "logos_agent_id": str,
        "universal_session_id": str,
        "agents_planned": ["I1", "I2", "I3"],
        "protocols_planned": ["SCP", "ARP", "MTP"],
        "execution": "FORBIDDEN",
        "phase": "Phase-E",
        "status": "ORCHESTRATION_PLAN_PREPARED",
    },
}
```

**Key fields P1 consumes:**
- `logos_identity.logos_agent_id` — root identity for all downstream authority
- `logos_identity.session_id` — universal session ID for all participants
- `agent_orchestration_plan.agents_planned` — which agents to instantiate
- `agent_orchestration_plan.protocols_planned` — which protocols to bind

### 2.4 Orchestration Plan Contract (P1-IF-04)

**Source:** `agent_orchestration.py`

The orchestration plan is declarative. It says WHAT should be bound, not HOW. P1 is the first module that converts this declarative plan into runtime reality.

**Binding rules (from `Runtime_Spine_Lock_And_Key_Execution_Contract.json`):**
- SCP → I1 (exclusive, no shared access)
- MTP → I2 (exclusive, no shared access)
- ARP → I3 (exclusive, no shared access)
- Logos Protocol → Logos Agent (exclusive)
- CSP → shared substrate (all authorized agents, no escalation)
- SOP → airlocked (session_id + logos_agent_id only, no agent access)

---

## 3. P1.1 — Agent Lifecycle Manager

### 3.1 Purpose

Consumes the `LOGOS_AGENT_READY` output and constructs runtime agent wrappers that implement `NexusParticipant`. After `AgentLifecycleManager.activate()`, all agents exist as registerable participants.

### 3.2 File Location

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Agent_Lifecycle_Manager.py
```

### 3.3 Class Definition

```python
class AgentLifecycleManager:

    def __init__(self, startup_context: Dict[str, Any]) -> None:
        """
        Accepts the full LOGOS_AGENT_READY dict from RUN_LOGOS_SYSTEM().

        Validates:
        - startup_context["status"] == "LOGOS_AGENT_READY"
        - logos_agent_id is present and non-empty
        - session_id is present and non-empty
        - agent_orchestration_plan is present and well-formed

        Raises:
        - LifecycleHalt on any validation failure
        """

    def activate(self) -> Dict[str, NexusParticipant]:
        """
        Constructs agent wrappers from the orchestration plan.

        Returns dict mapping participant_id → NexusParticipant instance:
        {
            "agent_i1": I1AgentParticipant,
            "agent_i2": I2AgentParticipant,
            "agent_i3": I3AgentParticipant,
            "agent_logos": LogosAgentParticipant,
        }

        Does NOT register participants with any Nexus.
        Does NOT start any tick execution.
        Does NOT activate any protocol.

        Raises:
        - LifecycleHalt on construction failure
        """

    def get_session_id(self) -> str:
        """Returns the universal session ID."""

    def get_logos_agent_id(self) -> str:
        """Returns the LOGOS agent identity string."""

    def get_participants(self) -> Dict[str, NexusParticipant]:
        """Returns the constructed participants. Raises if activate() not called."""
```

### 3.4 Agent Wrapper Interface (P1-IF-05)

Each agent wrapper implements `NexusParticipant` and delegates to existing agent tool libraries. The wrapper holds identity, protocol binding, and session context. The wrapper does NOT contain reasoning logic.

**Base class:**

```python
class AgentParticipantBase(NexusParticipant):
    """
    Base class for all agent wrappers.

    Subclasses MUST set:
    - participant_id (class or instance attribute)
    - protocol_binding (str or None)

    Subclasses MUST implement:
    - _on_tick(context) → called during execute_tick
    - _on_receive(packet) → called during receive_state
    - _project() → called during project_state, returns payload dict or None
    """

    def __init__(
        self,
        agent_name: str,
        session_id: str,
        logos_agent_id: str,
        protocol_binding: Optional[str],
    ) -> None:
        self._agent_name = agent_name
        self._session_id = session_id
        self._logos_agent_id = logos_agent_id
        self._protocol_binding = protocol_binding
        self._handle: Optional[NexusHandle] = None
        self._received_packets: List[StatePacket] = []
        self._last_tick_result: Optional[Dict[str, Any]] = None

    def register(self, nexus_handle: NexusHandle) -> None:
        self._handle = nexus_handle

    def receive_state(self, packet: StatePacket) -> None:
        self._received_packets.append(packet)

    def execute_tick(self, context: Dict[str, Any]) -> None:
        try:
            self._last_tick_result = self._on_tick(context)
        except Exception:
            self._last_tick_result = None
        self._received_packets.clear()

    def project_state(self) -> Optional[StatePacket]:
        projection = self._project()
        if projection is None:
            return None
        return StatePacket(
            source_id=self.participant_id,
            payload=projection,
            timestamp=time.time(),
            causal_intent=f"{self._agent_name}_tick_projection",
        )

    # --- Subclass hooks ---
    def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def _on_receive(self, packet: StatePacket) -> None:
        pass  # default: buffer in _received_packets

    def _project(self) -> Optional[Dict[str, Any]]:
        return None  # default: no projection
```

### 3.5 Concrete Agent Wrappers

**participant_id naming convention:** All agent participant IDs use the prefix `"agent_"` followed by the lowercase agent name. This guarantees they sort AFTER the RGE adapter (`"rge_topology_advisor"`) is not necessarily desired — see §3.6 for ordering analysis.

#### 3.5.1 LogosAgentParticipant

```python
class LogosAgentParticipant(AgentParticipantBase):
    participant_id: str = "agent_logos"

    def __init__(self, session_id: str, logos_agent_id: str) -> None:
        super().__init__(
            agent_name="Logos",
            session_id=session_id,
            logos_agent_id=logos_agent_id,
            protocol_binding="Logos_Protocol",
        )
        self._task_queue: List[Dict[str, Any]] = []
        self._routing_table: Dict[str, str] = {}  # smp_id → target_agent

    def enqueue_task(self, task: Dict[str, Any]) -> None:
        """External entry point: submit a task to the Logos Agent for processing."""
        self._task_queue.append(task)

    def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Logos Agent tick responsibilities:
        1. If task_queue is non-empty, create SMP from next task
        2. Evaluate routing: which agent should process this SMP?
        3. Evaluate promotion readiness for completed SMPs
        4. Route resolved SMPs to MTP for externalization
        """
        # V1 stub: pull task, create minimal SMP dict, route to I1
        # Full implementation in P2/P3
        if not self._task_queue:
            return None
        task = self._task_queue.pop(0)
        return {
            "type": "logos_task_dispatch",
            "content": {
                "task": task,
                "action": "route_to_i1",
                "session_id": self._session_id,
            },
        }

    def _project(self) -> Optional[Dict[str, Any]]:
        if self._last_tick_result is None:
            return None
        return self._last_tick_result
```

**Authority:** LogosAgentParticipant is the ONLY participant that may:
- Create SMPs
- Route SMPs to other agents
- Evaluate promotion readiness
- Authorize MTP externalization

No other agent wrapper may perform these operations. This is enforced by convention in V1 and by governance gates in later phases.

#### 3.5.2 I1AgentParticipant

```python
class I1AgentParticipant(AgentParticipantBase):
    participant_id: str = "agent_i1"

    def __init__(self, session_id: str, logos_agent_id: str) -> None:
        super().__init__(
            agent_name="I1",
            session_id=session_id,
            logos_agent_id=logos_agent_id,
            protocol_binding="SCP",
        )

    def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        I1 tick responsibilities:
        1. Check received packets for SMP routed to SCP
        2. If present, run SCP analysis (MVS/BDN) via existing adapters
        3. Produce I1AA and emit via handle
        """
        # V1 stub: acknowledge received SMPs, produce placeholder I1AA
        # Full implementation wires to:
        #   - smp_intake.load_smp()
        #   - analysis_runner.run_analysis()
        #   - i1aa_binder.I1AABinder.bind()
        for packet in self._received_packets:
            if packet.payload.get("type") == "logos_task_dispatch":
                return {
                    "type": "i1_analysis_result",
                    "content": {
                        "agent": "I1",
                        "status": "stub_complete",
                        "session_id": self._session_id,
                    },
                }
        return None
```

#### 3.5.3 I2AgentParticipant

```python
class I2AgentParticipant(AgentParticipantBase):
    participant_id: str = "agent_i2"

    def __init__(self, session_id: str, logos_agent_id: str) -> None:
        super().__init__(
            agent_name="I2",
            session_id=session_id,
            logos_agent_id=logos_agent_id,
            protocol_binding="MTP",
        )

    def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        I2 tick responsibilities:
        1. Check received packets for SMP routed to MTP
        2. If present, run MTP egress pipeline
        3. Produce I2AA (egress critique) and rendered NL output
        """
        # V1 stub: acknowledge, produce placeholder
        # Full implementation wires to:
        #   - MTPNexus.process(smp_payload)
        #   - I2EgressCritique.critique()
        return None
```

#### 3.5.4 I3AgentParticipant

```python
class I3AgentParticipant(AgentParticipantBase):
    participant_id: str = "agent_i3"

    def __init__(self, session_id: str, logos_agent_id: str) -> None:
        super().__init__(
            agent_name="I3",
            session_id=session_id,
            logos_agent_id=logos_agent_id,
            protocol_binding="ARP",
        )

    def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        I3 tick responsibilities:
        1. Check received packets for SMP routed to ARP
        2. If present, run ARP compiler
        3. Produce I3AA and emit
        """
        # V1 stub: acknowledge, produce placeholder
        # Full implementation wires to:
        #   - ARPCompilerCore.compile(aaced_packet, context)
        return None
```

### 3.6 Participant Execution Order Analysis

The LP Nexus executes participants in `sorted(participants.keys())` order. Given the participant IDs defined above plus the existing RGE adapter:

```
Sorted execution order:
  1. "agent_i1"
  2. "agent_i2"
  3. "agent_i3"
  4. "agent_logos"
  5. "rge_topology_advisor"
```

**Analysis:**
- `agent_logos` executes AFTER `agent_i1`, `agent_i2`, `agent_i3`. This means Logos Agent can read projected state from all sub-agents in the SAME tick (via receive_state on the next tick's inbound routing). However, within a single tick, agents communicate only via the shared context dict, NOT via StatePackets. StatePackets from one tick are routed at the START of the next tick.
- `rge_topology_advisor` executes LAST. This is correct: RGE reads task constraints from context, evaluates topology, and its projection is available for MSPC in the next tick.

**Governance question for ratification:** Should Logos Agent execute FIRST (prefix `"aaa_logos"` or similar) to dispatch tasks before sub-agents execute? Or should Logos Agent execute AFTER sub-agents to collect results?

**Recommendation:** For V1, Logos Agent executes after sub-agents. This allows a single-tick pattern where:
1. Logos routes an SMP to I1 (via StatePacket emitted in tick N)
2. I1 receives and processes it in tick N+1
3. Logos reads I1's projection in tick N+2

Multi-tick processing is the natural pattern. Single-tick "same-tick routing" requires shared context injection, which is the M6 pattern for RGE constraints but should not be generalized to agent-to-agent communication.

### 3.7 Files Created

| File | Purpose |
|---|---|
| `Logos_Core/Orchestration/Agent_Lifecycle_Manager.py` | Manager class |
| `Logos_Core/Orchestration/Agent_Wrappers.py` | Base class + 4 concrete wrappers |
| `Logos_Core/Orchestration/__init__.py` | Package initializer (may already exist from M6B) |

### 3.8 Verification

```bash
# File exists
test -f "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Agent_Lifecycle_Manager.py"

# Clean import
python3 -c "from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Agent_Lifecycle_Manager import AgentLifecycleManager; print('OK')"

# Construction from mock startup context
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Agent_Lifecycle_Manager import AgentLifecycleManager
ctx = {
    'status': 'LOGOS_AGENT_READY',
    'logos_identity': {'logos_agent_id': 'LOGOS:test', 'session_id': 'test'},
    'logos_session': {'session_id': 'test'},
    'constructive_compile_output': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'prepared_bindings': {}},
    'agent_orchestration_plan': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'agents_planned': ['I1','I2','I3'], 'protocols_planned': ['SCP','ARP','MTP'], 'execution': 'FORBIDDEN', 'phase': 'Phase-E', 'status': 'ORCHESTRATION_PLAN_PREPARED'},
}
mgr = AgentLifecycleManager(ctx)
participants = mgr.activate()
assert len(participants) == 4
assert 'agent_logos' in participants
assert 'agent_i1' in participants
assert 'agent_i2' in participants
assert 'agent_i3' in participants
print('ALL PASS')
"
```

### 3.9 Phase Lock

```
_Governance/Phase_Locks/Phase_P1_1_Agent_Lifecycle_Manager_Lock.json
```

---

## 4. P1.2 — Nexus Construction Factory

### 4.1 Purpose

Constructs the LP Nexus instance with MeshEnforcer and MREGovernor, then registers all agent participants and the RGE adapter. After `NexusFactory.build()`, the Nexus is ready to tick.

### 4.2 File Location

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Nexus_Factory.py
```

### 4.3 Class Definition

```python
class NexusFactory:

    @staticmethod
    def build_lp_nexus(
        participants: Dict[str, NexusParticipant],
        rge_adapter: Optional[NexusParticipant] = None,
        mre_config: Optional[Dict[str, Any]] = None,
    ) -> StandardNexus:
        """
        Constructs and populates the primary LP Nexus.

        Parameters:
        - participants: dict from AgentLifecycleManager.activate()
        - rge_adapter: optional RGENexusAdapter (constructed externally with RGERuntime)
        - mre_config: optional MRE parameters (defaults provided)

        Construction sequence:
        1. Create MeshEnforcer
        2. Create MeteredReasoningEnforcer with config
        3. Create MREGovernor wrapping MRE
        4. Create StandardNexus(mesh, mre_governor)
        5. Register each participant from participants dict
        6. Register rge_adapter if provided
        7. Return nexus

        Raises:
        - NexusViolation on registration failure
        """

    @staticmethod
    def build_rge_adapter() -> Optional[NexusParticipant]:
        """
        Attempts to construct RGENexusAdapter.

        Construction:
        1. Import RGERuntime from RGE_Bootstrap
        2. Construct RGERuntime()
        3. Wrap in RGENexusAdapter(rge_runtime)
        4. Return adapter

        On ImportError or construction failure:
        - Return None (RGE is advisory; system operates without it)
        - Log warning
        """

    @staticmethod
    def build_topology_provider():
        """
        Constructs TopologyContextProvider from M6B.

        Returns:
        - TopologyContextProvider instance

        This is the pure data holder bridging RGE output to MSPC.
        """

    @staticmethod
    def build_mspc_pipeline(topology_provider) -> Optional[Any]:
        """
        Attempts to construct MSPCPipeline with topology_provider as runtime_ref.

        On ImportError or construction failure:
        - Return None (MSPC can be wired later)
        - Log warning
        """
```

### 4.4 MRE Default Configuration

```python
DEFAULT_MRE_CONFIG = {
    "mre_level": 0.5,
    "max_iterations": 1000,
    "max_time_seconds": 10.0,
}
```

These defaults are conservative. The LP Nexus MRE instance governs ALL participants (agents + RGE). If any participant exceeds iteration or time limits, MRE transitions to RED and raises MREHalt.

### 4.5 LP Nexus MRE Variant

**Problem:** The LP Nexus `StandardNexus` constructor takes `MREGovernor(mre)` where `mre` must implement `pre_tick(pid) -> dict` and `post_tick(pid) -> dict`. But the standalone `MeteredReasoningEnforcer` in `ARP_Core/metered_reasoning_enforcer.py` implements `update(output_signature)`, `should_continue()`, and `telemetry_snapshot()` — a different interface.

**Resolution:** Each Nexus defines its own `MREGovernor` class that wraps `MeteredReasoningEnforcer` with `pre_tick` / `post_tick` adaptation. The LP Nexus already has this:

```python
class MREGovernor:
    def __init__(self, mre):
        self.mre = mre

    def pre_execute(self, participant_id: str) -> Dict[str, Any]:
        decision = self.mre.pre_tick(participant_id)
        if decision["state"] == "RED":
            raise MREHalt(f"MRE HALT (pre): {participant_id}")
        return decision

    def post_execute(self, participant_id: str) -> None:
        decision = self.mre.post_tick(participant_id)
        if decision["state"] == "RED":
            raise MREHalt(f"MRE HALT (post): {participant_id}")
```

**This means the LP Nexus MRE expects `pre_tick(pid)` and `post_tick(pid)`, not the `update()`/`should_continue()` interface.** The NexusFactory must provide an MRE implementation with this interface. This may require a thin adapter or a V1-specific MRE implementation that tracks per-participant iteration counts and returns `{"state": "GREEN"}` / `{"state": "RED"}` dicts.

### 4.6 V1 MRE Adapter

```python
class V1MREAdapter:
    """
    Minimal MRE for V1 that tracks per-participant tick counts.
    Returns GREEN until max_ticks_per_participant is exceeded.
    """

    def __init__(self, max_ticks_per_participant: int = 1000) -> None:
        self._max = max_ticks_per_participant
        self._counts: Dict[str, int] = {}

    def pre_tick(self, participant_id: str) -> Dict[str, Any]:
        count = self._counts.get(participant_id, 0)
        if count >= self._max:
            return {"state": "RED", "participant_id": participant_id, "ticks": count}
        return {"state": "GREEN", "participant_id": participant_id, "ticks": count}

    def post_tick(self, participant_id: str) -> Dict[str, Any]:
        self._counts[participant_id] = self._counts.get(participant_id, 0) + 1
        return {"state": "GREEN", "participant_id": participant_id}
```

### 4.7 Construction Sequence

```python
# Inside NexusFactory.build_lp_nexus():

mesh = MeshEnforcer()
mre = V1MREAdapter(max_ticks_per_participant=mre_config.get("max_iterations", 1000))
mre_governor = MREGovernor(mre)
nexus = StandardNexus(mesh=mesh, mre_governor=mre_governor)

for pid in sorted(participants.keys()):
    nexus.register_participant(participants[pid])

if rge_adapter is not None:
    nexus.register_participant(rge_adapter)

return nexus
```

### 4.8 Files Created

| File | Purpose |
|---|---|
| `Logos_Core/Orchestration/Nexus_Factory.py` | Factory class + V1MREAdapter |

### 4.9 Verification

```bash
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Nexus_Factory import NexusFactory
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Agent_Lifecycle_Manager import AgentLifecycleManager

ctx = {
    'status': 'LOGOS_AGENT_READY',
    'logos_identity': {'logos_agent_id': 'LOGOS:test', 'session_id': 'test'},
    'logos_session': {'session_id': 'test'},
    'constructive_compile_output': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'prepared_bindings': {}},
    'agent_orchestration_plan': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'agents_planned': ['I1','I2','I3'], 'protocols_planned': ['SCP','ARP','MTP'], 'execution': 'FORBIDDEN', 'phase': 'Phase-E', 'status': 'ORCHESTRATION_PLAN_PREPARED'},
}
mgr = AgentLifecycleManager(ctx)
participants = mgr.activate()

nexus = NexusFactory.build_lp_nexus(participants, rge_adapter=None)
assert len(nexus.participants) == 4
assert nexus.tick_counter == 0
nexus.tick()
assert nexus.tick_counter == 1
print('ALL PASS')
"
```

### 4.10 Phase Lock

```
_Governance/Phase_Locks/Phase_P1_2_Nexus_Factory_Lock.json
```

---

## 5. P1.3 — Main Tick Loop

### 5.1 Purpose

The main execution loop. Receives tasks, executes governed ticks, routes output. This is the module that makes LOGOS run.

### 5.2 File Location

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Runtime_Loop.py
```

### 5.3 Public Interface (P1-IF-06)

```python
class RuntimeLoop:

    def __init__(
        self,
        startup_context: Dict[str, Any],
        task_source: Optional[TaskSource] = None,
        output_sink: Optional[OutputSink] = None,
    ) -> None:
        """
        Constructs the runtime from startup context.

        Internal construction:
        1. AgentLifecycleManager(startup_context)
        2. AgentLifecycleManager.activate()
        3. NexusFactory.build_rge_adapter() (optional)
        4. NexusFactory.build_topology_provider()
        5. NexusFactory.build_lp_nexus(participants, rge_adapter)
        6. NexusFactory.build_mspc_pipeline(topology_provider) (optional)
        7. DeclaredConstraintProvider() from M6A
        8. Store all components

        Raises:
        - RuntimeActivationHalt on any construction failure
        """

    def run(self) -> None:
        """
        Main execution loop. Blocks until termination.

        Loop:
        1. Pull next task from task_source (blocks if empty)
        2. Build task_context (task_id, tick_id, declared_constraints)
        3. Execute orchestration tick (M6 Task C sequence)
        4. Route output to output_sink
        5. Check for halt conditions
        6. Repeat

        Termination:
        - task_source signals end-of-input
        - Halt propagation from Nexus tick (MREHalt, NexusViolation)
        - External shutdown signal (SIGTERM/SIGINT)
        - Explicit halt from Logos Agent

        On termination:
        - Close operational logger
        - Emit session closure audit event
        """

    def run_single(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task synchronously. For testing and CLI mode.

        Returns tick result dict (P1-IF-07).

        Does NOT enter the main loop.
        """
```

### 5.4 Task and Output Interfaces

```python
class TaskSource:
    """Abstract interface for task ingestion."""

    def next_task(self) -> Optional[Dict[str, Any]]:
        """Return next task dict or None to signal end-of-input."""
        raise NotImplementedError

    def has_tasks(self) -> bool:
        raise NotImplementedError


class StdinTaskSource(TaskSource):
    """V1 default: reads JSON task objects from stdin, one per line."""

    def next_task(self) -> Optional[Dict[str, Any]]:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line.strip())

    def has_tasks(self) -> bool:
        return True  # stdin blocks


class SingleTaskSource(TaskSource):
    """For testing: provides exactly one task."""

    def __init__(self, task: Dict[str, Any]) -> None:
        self._task = task
        self._consumed = False

    def next_task(self) -> Optional[Dict[str, Any]]:
        if self._consumed:
            return None
        self._consumed = True
        return self._task

    def has_tasks(self) -> bool:
        return not self._consumed


class OutputSink:
    """Abstract interface for output delivery."""

    def emit(self, result: Dict[str, Any]) -> None:
        raise NotImplementedError


class StdoutOutputSink(OutputSink):
    """V1 default: writes JSON result to stdout."""

    def emit(self, result: Dict[str, Any]) -> None:
        print(json.dumps(result, indent=2))
```

### 5.5 Tick Result Contract (P1-IF-07)

Each tick produces a result dict:

```python
{
    "tick_id": int,
    "session_id": str,
    "task_id": str,                     # from task input
    "status": str,                       # "completed" | "halted" | "no_output"
    "rge_result": Optional[Dict],        # topology selection (if RGE active)
    "mspc_result": Optional[Dict],       # compilation result (if MSPC active)
    "agent_projections": Dict[str, Any], # participant_id → projection payload
    "rendered_output": Optional[str],    # NL text from MTP (if pipeline wired)
    "halt_reason": Optional[str],        # set if status == "halted"
}
```

### 5.6 Tick Execution Sequence (V1)

```python
def _execute_tick(self, task: Dict[str, Any]) -> Dict[str, Any]:

    task_id = task.get("task_id", str(uuid.uuid4()))

    # 1. Submit task to Logos Agent
    self._logos_participant.enqueue_task(task)

    # 2. Derive constraints
    constraints = self._constraint_provider.get_constraints_for_tick(task)

    # 3. Build task context for Nexus tick
    task_context = {
        "task_id": task_id,
        "constraints": constraints,
        "session_id": self._session_id,
    }

    # 4. Execute LP Nexus tick (M6 Task C integration if MSPC active)
    #    If M6 wiring is complete:
    #      a. nexus.tick() — all participants execute, RGE produces topology
    #      b. Read RGE result from adapter
    #      c. topology_provider.set_topology(rge_result)
    #      d. mspc_pipeline.execute_tick() — receives topology context
    #      e. topology_provider.clear()
    #    If M6 wiring is NOT complete (no MSPC):
    #      a. nexus.tick() — agents execute only

    try:
        self._nexus.tick(causal_intent=f"task:{task_id}")
    except MREHalt as e:
        return self._halt_result(task_id, f"MRE halt: {e}")
    except NexusViolation as e:
        return self._halt_result(task_id, f"Nexus violation: {e}")
    except MeshRejection as e:
        return self._halt_result(task_id, f"Mesh rejection: {e}")

    # 5. Read RGE result (if adapter present)
    rge_result = None
    if self._rge_adapter is not None:
        rge_result = self._rge_adapter.get_last_result()

    # 6. Topology handoff (if M6 wired)
    if self._topology_provider is not None and rge_result is not None:
        self._topology_provider.set_topology(rge_result)

    # 7. MSPC tick (if pipeline constructed)
    mspc_result = None
    if self._mspc_pipeline is not None:
        try:
            mspc_result = self._mspc_pipeline.execute_tick()
        except Exception as e:
            mspc_result = {"halted": True, "reason": str(e)}

    # 8. Clear topology context (unconditional)
    if self._topology_provider is not None:
        self._topology_provider.clear()

    # 9. Collect projections
    projections = {}
    for pid, participant in self._nexus.participants.items():
        proj = participant.project_state()
        if proj is not None:
            projections[pid] = proj.payload

    # 10. Check for MSPC halt
    if mspc_result and mspc_result.get("halted"):
        return self._halt_result(task_id, f"MSPC halt: {mspc_result.get('reason')}")

    # 11. Build result
    return {
        "tick_id": self._nexus.tick_counter,
        "session_id": self._session_id,
        "task_id": task_id,
        "status": "completed",
        "rge_result": rge_result,
        "mspc_result": mspc_result,
        "agent_projections": projections,
        "rendered_output": None,  # MTP wiring in P3
        "halt_reason": None,
    }
```

### 5.7 Halt Propagation Rules

| Source | Condition | Behavior |
|---|---|---|
| MREHalt | Any participant exceeds MRE limits | Tick aborts, result status = "halted" |
| NexusViolation | Registration or structural failure | Tick aborts, result status = "halted" |
| MeshRejection | Malformed StatePacket | Tick aborts, result status = "halted" |
| MSPC halt | `mspc_result["halted"] == True` | Tick completes but result status = "halted" |
| RGE not selected | `rge_result["selected"] == False` | NOT a halt. Normal mode-gated behavior. Topology provider stores None. |
| Telemetry failure | Zero-triad from empty constraints | NOT a halt. RGE uses default topology. |
| Task source exhaustion | `next_task()` returns None | Loop terminates cleanly. |

### 5.8 Signal Handling

```python
import signal

def _setup_signal_handlers(self) -> None:
    signal.signal(signal.SIGTERM, self._shutdown_handler)
    signal.signal(signal.SIGINT, self._shutdown_handler)

def _shutdown_handler(self, signum, frame) -> None:
    self._running = False
```

### 5.9 Files Created

| File | Purpose |
|---|---|
| `Logos_Core/Orchestration/Runtime_Loop.py` | RuntimeLoop + TaskSource + OutputSink |

### 5.10 Verification

```bash
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Runtime_Loop import RuntimeLoop, SingleTaskSource, StdoutOutputSink

# Build minimal startup context
ctx = {
    'status': 'LOGOS_AGENT_READY',
    'logos_identity': {'logos_agent_id': 'LOGOS:test', 'session_id': 'test'},
    'logos_session': {'session_id': 'test'},
    'constructive_compile_output': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'prepared_bindings': {}},
    'agent_orchestration_plan': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'agents_planned': ['I1','I2','I3'], 'protocols_planned': ['SCP','ARP','MTP'], 'execution': 'FORBIDDEN', 'phase': 'Phase-E', 'status': 'ORCHESTRATION_PLAN_PREPARED'},
}

loop = RuntimeLoop(ctx)
result = loop.run_single({'task_id': 'test-001', 'input': 'hello world'})
assert result['status'] in ('completed', 'no_output')
assert result['session_id'] == 'test'
assert result['task_id'] == 'test-001'
print('ALL PASS')
"
```

### 5.11 Phase Lock

```
_Governance/Phase_Locks/Phase_P1_3_Runtime_Loop_Lock.json
```

---

## 6. P1.4 — Startup-to-Runtime Handoff

### 6.1 Purpose

Modify the existing startup chain to call `RuntimeLoop.run()` after producing `LOGOS_AGENT_READY`, instead of returning and terminating.

### 6.2 Modified Files

#### 6.2.1 `STARTUP/LOGOS_SYSTEM.py`

**Current terminal code (lines ~190-200):**
```python
    result = {
        "status": "LOGOS_AGENT_READY",
        "logos_identity": logos_identity,
        "logos_session": logos_session,
        "constructive_compile_output": constructive_compile_output,
        "agent_orchestration_plan": orchestration_plan,
    }
    operational_logger.status(Channel.STARTUP, "agent_orchestration_complete")
    operational_logger.close()
    return result
```

**Modified code:**
```python
    result = {
        "status": "LOGOS_AGENT_READY",
        "logos_identity": logos_identity,
        "logos_session": logos_session,
        "constructive_compile_output": constructive_compile_output,
        "agent_orchestration_plan": orchestration_plan,
    }
    operational_logger.status(Channel.STARTUP, "agent_orchestration_complete")

    # ---- P1.4: Runtime Activation Handoff ----
    if mode == "headless":
        operational_logger.status(Channel.STARTUP, "runtime_activation_begin")
        try:
            from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Runtime_Loop import (
                RuntimeLoop,
                StdinTaskSource,
                StdoutOutputSink,
            )
            runtime = RuntimeLoop(
                startup_context=result,
                task_source=StdinTaskSource(),
                output_sink=StdoutOutputSink(),
            )
            runtime.run()
        except Exception as exc:
            operational_logger.halt(
                Channel.STARTUP,
                f"Runtime activation failed: {exc}",
                error_type="RuntimeActivationHalt",
                error_detail=str(exc),
            )
            raise RuntimeHalt(f"Runtime activation failed: {exc}")
        finally:
            operational_logger.status(Channel.STARTUP, "runtime_terminated")
            operational_logger.close()
    else:
        # Interactive mode: return for GUI consumption
        operational_logger.close()
        return result
```

**Key design decisions:**
- Runtime import is deferred (inside the `if` block) to avoid importing P1 modules at LOGOS_SYSTEM load time. This preserves the startup chain's existing import graph.
- Headless mode enters the runtime loop. Interactive mode returns the dict for GUI consumption (preserving existing behavior).
- The operational logger is NOT closed before runtime activation. It remains open for the duration of the runtime loop. The `finally` block closes it on termination.

#### 6.2.2 `STARTUP/START_LOGOS.py`

**Current behavior:** Calls `RUN_LOGOS_SYSTEM()` and receives the returned dict. In headless mode with P1.4, `RUN_LOGOS_SYSTEM()` will block inside the runtime loop and only return on termination or in interactive mode.

**No changes needed** if `START_LOGOS.py` simply calls `RUN_LOGOS_SYSTEM()` and exits. The blocking behavior in headless mode is intentional — the process stays alive as long as the runtime loop runs.

### 6.3 Backward Compatibility

| Scenario | Before P1.4 | After P1.4 |
|---|---|---|
| Headless mode | Returns `LOGOS_AGENT_READY` dict, exits | Enters runtime loop, blocks, exits on termination |
| Interactive mode | Returns dict, launches GUI | Returns dict, launches GUI (unchanged) |
| Diagnostic mode | Returns dict | Returns dict (unchanged) |
| Import only | No execution | No execution (unchanged) |

### 6.4 Verification

```bash
# Verify headless mode enters runtime (test with immediate EOF on stdin)
echo '{}' | python3 -c "
import sys; sys.path.insert(0, '.')
from STARTUP.START_LOGOS import main
# This will process one empty task and exit when stdin is exhausted
"

# Verify interactive mode still returns dict
python3 -c "
from STARTUP.LOGOS_SYSTEM import RUN_LOGOS_SYSTEM
result = RUN_LOGOS_SYSTEM(mode='interactive')
assert result['status'] == 'LOGOS_AGENT_READY'
print('INTERACTIVE MODE: PASS')
"
```

### 6.5 Phase Lock

```
_Governance/Phase_Locks/Phase_P1_4_Startup_Handoff_Lock.json
```

---

## 7. Dependency Graph (P1 Internal)

```
P1.1 Agent Lifecycle Manager
  │
  ▼
P1.2 Nexus Construction Factory (requires P1.1 participants)
  │
  ▼
P1.3 Main Tick Loop (requires P1.1 + P1.2 + M6 artifacts)
  │
  ▼
P1.4 Startup Handoff (requires P1.3)
```

Strictly sequential. No parallelism within P1.

---

## 8. Complete File Manifest

### New Files (4-5)

| File | Path | Purpose |
|---|---|---|
| Agent_Lifecycle_Manager.py | `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/` | Agent construction from orchestration plan |
| Agent_Wrappers.py | `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/` | Base class + 4 concrete NexusParticipant wrappers |
| Nexus_Factory.py | `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/` | LP Nexus construction + V1MREAdapter |
| Runtime_Loop.py | `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/` | Main tick loop + TaskSource/OutputSink |
| `__init__.py` | `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/` | Package initializer (may already exist from M6B) |

### Modified Files (1-2)

| File | Change |
|---|---|
| `STARTUP/LOGOS_SYSTEM.py` | Add runtime activation handoff after `LOGOS_AGENT_READY` |
| `STARTUP/START_LOGOS.py` | Potentially no change needed (verify blocking behavior) |

### Dependencies (Consumed, Not Modified)

| Module | Import Purpose |
|---|---|
| `LP_Nexus/Logos_Protocol_Nexus.py` | NexusParticipant, StatePacket, NexusHandle, StandardNexus, MeshEnforcer, MREGovernor |
| `RGE_Nexus_Adapter.py` | RGENexusAdapter (optional) |
| `RGE_Bootstrap.py` | RGERuntime (optional, for RGE adapter construction) |
| `Topology_Context_Provider.py` | TopologyContextProvider (from M6B) |
| `Task_Constraint_Provider.py` | DeclaredConstraintProvider (from M6A) |
| `MSPC_Pipeline.py` | MSPCPipeline (optional) |

---

## 9. Governance Invariants Preserved

| Invariant | How P1 Preserves It |
|---|---|
| Deny-by-default | Agent wrappers have no authority by default. Only LogosAgentParticipant may route SMPs. |
| Fail-closed | All tick execution is wrapped in try/except. Any exception produces a halt result, never degraded operation. |
| No implicit authority escalation | Agent wrappers delegate to tool libraries. No wrapper contains governance logic. |
| No audit readback | Operational logger writes only. No component reads audit logs. |
| No hidden persistent state | All runtime state is session-scoped. RuntimeLoop holds ephemeral state only. |
| Deterministic tick ordering | LP Nexus executes participants in sorted(participant_id) order. Order is deterministic from participant_id naming. |
| RGE advisory only | RGE adapter participates in Nexus ticks but its topology recommendation is advisory. Logos Agent may ignore it. |
| Single-tick temporal boundary | No cross-tick state leakage. Topology provider is cleared unconditionally at tick boundary. |

---

## 10. Open Questions Requiring Human Decision

1. **Logos Agent execution position:** Should `agent_logos` execute before or after sub-agents? Current naming puts it 4th of 5. Alternative: rename to `aaa_logos_orchestrator` for first-position execution.

2. **Multi-tick vs single-task mode:** Should V1 default to processing one task and exiting, or looping until stdin is exhausted? Recommendation: loop until EOF (Unix pipeline compatible).

3. **RGE optionality:** If RGE import fails (missing dependencies), should the system halt or continue without topology advice? Recommendation: continue without (advisory-only degradation).

4. **MRE strictness:** V1 MRE adapter is permissive (1000 ticks per participant). Should this be tighter for safety? Recommendation: keep permissive for V1, tighten in P4 hardening.

---

## 11. GPT Prompt Generation Instructions

P1 implementation should be executed as 4 sequential GPT → VS Code prompts:

**Prompt 1:** P1.1 — Create Agent_Lifecycle_Manager.py and Agent_Wrappers.py. Run verification. Write phase lock.

**Prompt 2:** P1.2 — Create Nexus_Factory.py. Run verification (depends on P1.1 artifacts). Write phase lock.

**Prompt 3:** P1.3 — Create Runtime_Loop.py. Run verification (depends on P1.1 + P1.2). Write phase lock.

**Prompt 4:** P1.4 — Modify STARTUP/LOGOS_SYSTEM.py. Run verification. Write phase lock. Write P1 closure lock.

Each prompt is self-contained after its predecessor is committed.

---

END OF P1 SPECIFICATION

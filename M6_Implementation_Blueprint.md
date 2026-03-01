# M6 Implementation Blueprint and Roadmap

**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires governance ratification before implementation
**Pipeline Position:** Claude (this document) → GPT (VS Code prompt generation) → VS Code (repo mutation) → GitHub (canonical state)
**Date:** 2026-02-28

---

## 0. How to Read This Document

This blueprint defines the complete M6 implementation scope for closing the RGE ↔ MSPC integration loop. It is structured as a sequential task list (A → B → C), each containing everything GPT needs to produce a targeted VS Code prompt. Each task specifies exact files, exact changes, verification commands, and a phase lock artifact.

GPT should produce one VS Code prompt per task. Tasks execute in strict order. No task may begin until the prior task's phase lock is committed.

---

## 1. System State (Verified by Repo Inspection)

### 1.1 What Already Exists

**RGENexusAdapter** (`LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/RGE_Nexus_Adapter.py`):
- Wraps `RGERuntime` as a `NexusParticipant`
- `participant_id = "rge_topology_advisor"`
- `execute_tick(context)` already calls:
  1. `_extract_telemetry_input(context)` — reads `constraints`, `task_id`, `tick_id`, `mesh_output`, `protocol_telemetry`, `hysteresis_key`, `recursion_telemetry` from context dict
  2. `self._rge.inject_telemetry(...)` — assembles telemetry snapshot
  3. `self._rge.evaluate()` — scores all 192 configurations
  4. `self._rge.select()` — applies hysteresis, emits topology advice to Router
  5. Stores result in `self._last_result`
- `project_state()` emits `StatePacket` with `type: "rge_topology_recommendation"` containing topology snapshot
- Fail-closed: exceptions caught, `_last_result` set to `None`

**Logos Protocol Nexus** (`LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py`):
- `tick()` executes participants in `sorted(self.participants.keys())` order
- Context built from `self.mre.pre_execute(pid)` plus `tick_id` and `causal_intent`
- `_route(inbound)` runs BEFORE participant execution (routes prior-tick packets only)
- Participants cannot communicate within the same tick via StatePackets — only via shared context

**MSPC Pipeline** (`LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Multi_Process_Signal_Compiler/MSCP_Protocol/MSPC_Pipeline.py`):
- `_stage_compilation()` probes `self._runtime_ref.get_topology_context()` if method exists
- Passes result as `topology_context` to `IncrementalCompiler.compile_batch()`
- `__init__()` accepts `runtime_ref: Optional[Any]`
- Handles `None` topology context gracefully

**Task_Triad_Derivation** (`LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Core/Task_Triad_Derivation.py`):
- `Constraint` dataclass: `constraint_id`, `framing_tags: FrozenSet[str]`, `weight`, `critical`
- `derive_triad(constraints: List[Constraint]) -> TriadDerivationResult` — deterministic classification
- Already imported by `RGE_Bootstrap.py`

**Telemetry_Producer** (two locations):
- `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Core/Telemetry_Producer.py` — canonical assembly function `assemble_telemetry()`
- `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Telemetry_Production/Telemetry_Producer.py` — parallel copy (same function, different import path; used by `RGE_Bootstrap`)

**Logos_Telemetry_Integration_Point** (`LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/Logos_Telemetry_Integration_Point.py`):
- Status: `DESIGN_ONLY`
- Defines mixin pattern for telemetry injection
- Documents lexicographic ordering constraint

### 1.2 What Does NOT Exist

1. **Constraint ingress seam** — no module produces `List[Constraint]` from a task context at tick time
2. **Context injection** — the LP Nexus `tick()` method does not accept external task-level data; context is built internally from MRE
3. **Topology context provider** — no bridge object connects RGE selection output to MSPC's `runtime_ref.get_topology_context()`
4. **MSPC tick triggering** — no orchestration code calls `MSPCPipeline.execute_tick()` after the LP Nexus tick completes
5. **Tick boundary cleanup** — no code clears the topology context provider between ticks

### 1.3 Critical Architectural Constraint

The LP Nexus `tick()` loop routes inbound packets BEFORE executing participants. Participants cannot exchange data within the same tick via StatePackets. The only intra-tick data path is the `context` dict passed to `execute_tick()`.

This means: constraints must enter the RGE adapter's `execute_tick(context)` via the context dict, not via a prior participant's StatePacket emission. The context is currently built from `mre.pre_execute(pid)` + tick metadata. Constraints must be injected into this context before the tick loop begins.

---

## 2. Revised Task Definitions

The original spec (Phase_6_Integration_Closure_Spec.md) defined three tasks. Based on repo inspection, Task A is revised. Tasks B and C are confirmed.

### Summary

| Task | Description | New Files | Modified Files |
|------|-------------|-----------|----------------|
| A | Constraint Ingress + Context Injection | 1 | 1-2 |
| B | Topology Context Provider | 1 | 1 |
| C | Orchestration Tick Binding + Cleanup | 0 | 1-2 |

---

## 3. Task A — Constraint Ingress and Context Injection

### 3.1 Objective

Create the constraint ingress seam and ensure constraints reach the RGE adapter's `execute_tick(context)` via the LP Nexus tick context.

### 3.2 Why Not a Separate Telemetry Participant

The original spec proposed a "Logos Telemetry Participant" that assembles telemetry before RGE executes. This is unnecessary because:

- `RGENexusAdapter.execute_tick()` already calls `inject_telemetry()` → `evaluate()` → `select()` internally
- `inject_telemetry()` already calls `assemble_telemetry()` which calls `derive_triad()`
- The full telemetry → triad → scoring → selection pipeline is already wired inside the adapter

What is missing is getting constraints INTO the adapter's tick context, not assembling telemetry from constraints (that part works).

### 3.3 Deliverables

**D-A1: TaskConstraintProvider module**

New file. Minimal interface + pass-through implementation.

```
Path: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Telemetry_Production/Task_Constraint_Provider.py
```

Contents:

```python
from typing import Any, Dict, List, Protocol
from LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Core.Task_Triad_Derivation import Constraint

class ConstraintProvider(Protocol):
    def get_constraints_for_tick(self, task_context: Dict[str, Any]) -> List[Constraint]: ...

class DeclaredConstraintProvider:
    """
    Pass-through provider: reads pre-declared constraints from task_context.
    M6 implementation. Future phases may replace with governance-inference provider.
    """
    CONTEXT_KEY: str = "declared_constraints"

    def get_constraints_for_tick(self, task_context: Dict[str, Any]) -> List[Constraint]:
        raw = task_context.get(self.CONTEXT_KEY, [])
        if isinstance(raw, list):
            return [c for c in raw if isinstance(c, Constraint)]
        return []
```

Requirements:
- Canonical header per `Runtime_Module_Header_Contract.json`
- `DESIGN_ONLY` status until governance ratification (but structurally complete)
- Fail-closed: returns empty list on malformed input (triggers zero-triad → default topology)
- No inference, no NLP, no governance expansion

**D-A2: LP Nexus context injection**

Modify LP Nexus to accept optional tick-level task context that gets merged into each participant's `execute_tick(context)` dict.

File: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py`

Change: Add `task_context` parameter to `tick()` method.

Current signature:
```python
def tick(self, causal_intent: Optional[str] = None) -> None:
```

New signature:
```python
def tick(self, causal_intent: Optional[str] = None, task_context: Optional[Dict[str, Any]] = None) -> None:
```

Inside the tick loop, merge task_context into each participant's context:
```python
context = self.mre.pre_execute(pid)
context.update({"tick_id": tick_id, "causal_intent": causal_intent})
if task_context is not None:
    context.update(task_context)
participant.execute_tick(context)
```

This is backward-compatible: existing callers pass no task_context, context is unchanged. New callers can inject constraints, task_id, mesh_output, etc.

### 3.4 Constraints

- LP Nexus `tick()` signature change must be backward-compatible (Optional parameter with None default)
- No modification to `RGENexusAdapter` — it already reads constraints from context
- No modification to MRE governor
- No modification to RGE internals
- The `task_context` dict is read-only within the tick — no participant may mutate it

### 3.5 Verification

```bash
# 1. New file exists and has canonical header
test -f "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Telemetry_Production/Task_Constraint_Provider.py"

# 2. LP Nexus tick() accepts task_context parameter
grep -n "def tick" "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py" | grep "task_context"

# 3. Context merging present in tick loop
grep -n "task_context" "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py"

# 4. Backward compatibility: existing tick() calls don't break (no required new args)
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Telemetry_Production.Task_Constraint_Provider import DeclaredConstraintProvider, Constraint
p = DeclaredConstraintProvider()
# Empty context returns empty list
assert p.get_constraints_for_tick({}) == []
# Malformed input returns empty list
assert p.get_constraints_for_tick({'declared_constraints': 'not_a_list'}) == []
# Valid input passes through
c = Constraint(constraint_id='test', framing_tags=frozenset({'goal'}))
assert p.get_constraints_for_tick({'declared_constraints': [c]}) == [c]
print('Task A verification: PASS')
"
```

### 3.6 Phase Lock

```
Path: _Governance/Phase_Locks/Phase_M6A_Constraint_Ingress_Lock.json
```

```json
{
  "phase": "M6A",
  "title": "Constraint Ingress and Context Injection",
  "status": "LOCKED",
  "new_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Telemetry_Production/Task_Constraint_Provider.py"
  ],
  "modified_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py"
  ],
  "rge_modified": false,
  "mspc_modified": false,
  "backward_compatible": true,
  "governance_compliance_verified": true
}
```

---

## 4. Task B — Topology Context Provider

### 4.1 Objective

Create a bridge object that receives RGE's topology selection result and exposes it to MSPC via the existing `get_topology_context()` probe in `_stage_compilation()`.

### 4.2 Deliverables

**D-B1: TopologyContextProvider module**

New file.

```
Path: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py
```

Contents:

```python
from typing import Any, Dict, Optional

class TopologyContextProvider:
    """
    Bridge between RGE topology selection and MSPC compilation context.
    
    Written by orchestration layer after RGE selects.
    Read by MSPC via get_topology_context() during _stage_compilation().
    
    Single-tick lifecycle:
      1. Orchestration calls set_topology() with RGE selection result
      2. MSPC calls get_topology_context() during compilation
      3. Orchestration calls clear() at tick boundary
    
    No persistence across ticks. No cross-component coupling.
    RGE does not write here directly. Orchestration mediates.
    """

    def __init__(self) -> None:
        self._current_context: Optional[Dict[str, Any]] = None

    def set_topology(self, rge_result: Dict[str, Any]) -> None:
        if rge_result is None:
            self._current_context = None
            return
        if not rge_result.get("selected", False):
            self._current_context = None
            return
        self._current_context = rge_result.get("topology")

    def get_topology_context(self) -> Optional[Dict[str, Any]]:
        return self._current_context

    def clear(self) -> None:
        self._current_context = None
```

Requirements:
- Canonical header per `Runtime_Module_Header_Contract.json`
- `get_topology_context()` matches the method name probed by MSPC's `_stage_compilation()`
- Returns `None` when RGE was mode-gated, overridden, or no selection occurred
- `clear()` called at tick boundary by orchestration layer
- No imports from RGE or MSPC (pure data holder)

**D-B2: Wire as MSPC runtime_ref**

Locate the site where `MSPCPipeline` is constructed. Pass the `TopologyContextProvider` instance as `runtime_ref`.

The construction site must be identified during implementation. Search for:
```bash
grep -rn "MSPCPipeline(" LOGOS_SYSTEM/
```

If no construction site exists yet (MSPC may not be instantiated in the current codebase), document where it should be constructed and defer wiring to Task C.

### 4.3 Constraints

- No modification to `MSPC_Pipeline.py` — the existing `runtime_ref` / `get_topology_context()` probe is sufficient
- No modification to RGE — the orchestration layer reads `RGENexusAdapter._last_result` or the projected StatePacket
- No RGE → MSPC import path created
- TopologyContextProvider has zero imports from either RGE or MSPC packages
- `set_topology()` is idempotent — calling twice overwrites

### 4.4 Verification

```bash
# 1. New file exists
test -f "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py"

# 2. Method name matches MSPC probe
grep -n "get_topology_context" "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py"
grep -n "get_topology_context" "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Multi_Process_Signal_Compiler/MSCP_Protocol/MSPC_Pipeline.py"

# 3. Functional test
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Topology_Context_Provider import TopologyContextProvider

tcp = TopologyContextProvider()

# No topology set
assert tcp.get_topology_context() is None

# Mode-gated result
tcp.set_topology({'selected': False, 'reason': 'mode_gated'})
assert tcp.get_topology_context() is None

# Valid selection
tcp.set_topology({'selected': True, 'topology': {'rotation_index': 3, 'agent_assignments': {'a': 'SCP'}}})
assert tcp.get_topology_context() == {'rotation_index': 3, 'agent_assignments': {'a': 'SCP'}}

# Clear at tick boundary
tcp.clear()
assert tcp.get_topology_context() is None

print('Task B verification: PASS')
"
```

### 4.5 Phase Lock

```
Path: _Governance/Phase_Locks/Phase_M6B_Topology_Context_Provider_Lock.json
```

```json
{
  "phase": "M6B",
  "title": "Topology Context Provider",
  "status": "LOCKED",
  "new_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py"
  ],
  "modified_files": [],
  "mspc_pipeline_modified": false,
  "rge_modified": false,
  "no_rge_mspc_import_path": true,
  "governance_compliance_verified": true
}
```

---

## 5. Task C — Orchestration Tick Binding

### 5.1 Objective

Implement the per-tick orchestration sequence that binds constraint ingress, LP Nexus tick (containing RGE), topology context handoff, and MSPC tick into a single governed execution cycle.

### 5.2 The Tick Sequence

```
TICK N:

  1. Orchestration layer constructs task_context:
     - task_id, tick_id
     - declared_constraints: List[Constraint] (via DeclaredConstraintProvider or direct)
     - mesh_output (optional)
     - protocol_telemetry (optional)

  2. Orchestration calls nexus.tick(task_context=task_context):
     - LP Nexus routes prior-tick inbound packets
     - LP Nexus merges task_context into each participant's context
     - Participants execute in sorted order:
       a. "rge_topology_advisor" (RGENexusAdapter):
          → reads constraints from context
          → inject_telemetry → evaluate → select
          → stores result in _last_result
          → emits topology advice to Epistemic_Library_Router

  3. Orchestration reads RGE result:
     - From RGENexusAdapter._last_result (direct reference)
     - OR from RGENexusAdapter.project_state() (StatePacket)
     - Calls topology_context_provider.set_topology(result)

  4. Orchestration calls mspc_pipeline.execute_tick():
     - _stage_ingress drains signals
     - _stage_compilation probes get_topology_context() → receives Step 3 topology
     - _stage_emission / _stage_publication complete

  5. Orchestration calls topology_context_provider.clear()
     - Prevents stale topology leakage to tick N+1

TICK N COMPLETE
```

### 5.3 Implementation Site

This orchestration logic must live in the Logos Agent orchestration layer. The exact file depends on the current orchestration structure. Search for:

```bash
# Find where nexus.tick() is currently called
grep -rn "\.tick(" LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/
grep -rn "\.tick(" LOGOS_SYSTEM/System_Entry_Point/Agent_Orchestration/
grep -rn "\.tick(" STARTUP/
```

If no orchestration loop currently exists that calls `nexus.tick()`, the implementation must create a minimal orchestration function. Suggested location:

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Tick_Orchestrator.py
```

This function is the integration glue. It does not own authority — it sequences existing components.

### 5.4 Orchestration Function Shape

```python
def execute_orchestration_tick(
    nexus: LogosProtocolNexus,
    rge_adapter: RGENexusAdapter,
    mspc_pipeline: MSPCPipeline,
    topology_provider: TopologyContextProvider,
    constraint_provider: ConstraintProvider,
    task_context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Execute one complete orchestration tick.
    Sequences: constraint derivation → Nexus tick → topology handoff → MSPC tick → cleanup.
    """
    # 1. Derive constraints
    constraints = constraint_provider.get_constraints_for_tick(task_context)
    
    # 2. Build tick context
    tick_context = {
        "task_id": task_context.get("task_id", ""),
        "constraints": constraints,
        "mesh_output": task_context.get("mesh_output"),
        "protocol_telemetry": task_context.get("protocol_telemetry"),
        "hysteresis_key": task_context.get("hysteresis_key"),
        "recursion_telemetry": task_context.get("recursion_telemetry"),
    }
    
    # 3. Execute LP Nexus tick (includes RGE participant)
    nexus.tick(task_context=tick_context)
    
    # 4. Hand off topology to provider
    rge_result = rge_adapter._last_result
    topology_provider.set_topology(rge_result)
    
    # 5. Execute MSPC tick
    mspc_result = mspc_pipeline.execute_tick()
    
    # 6. Cleanup
    topology_provider.clear()
    
    # 7. Return tick summary
    return {
        "rge_selected": rge_result.get("selected", False) if rge_result else False,
        "mspc_halted": mspc_result.halted if mspc_result else False,
        "mspc_artifacts_emitted": mspc_result.artifacts_emitted if mspc_result else 0,
    }
```

This is pseudocode for structural reference. The actual implementation must:
- Include canonical header
- Include try/except with fail-closed semantics on orchestration failure
- NOT catch MSPC halts silently — propagate them
- NOT modify any participant internals
- NOT create new authority surfaces

### 5.5 Accessing RGE Result

Two options for Step 3 → Step 4 handoff:

**Option A — Direct reference:** The orchestration function holds a reference to `rge_adapter` and reads `rge_adapter._last_result` after `nexus.tick()` completes. This is direct but accesses a private attribute.

**Option B — Public accessor:** Add a `get_last_result() -> Optional[Dict[str, Any]]` method to `RGENexusAdapter`. This is cleaner but modifies the adapter.

Recommendation: Option B. One-line addition to `RGE_Nexus_Adapter.py`:

```python
def get_last_result(self) -> Optional[Dict[str, Any]]:
    return self._last_result
```

This is the only modification to an existing RGE file in M6.

### 5.6 MSPC Construction

If `MSPCPipeline` is not yet constructed anywhere in the codebase, Task C must include constructing it with the `TopologyContextProvider` as `runtime_ref`. Search:

```bash
grep -rn "MSPCPipeline(" LOGOS_SYSTEM/ STARTUP/
```

If no construction exists, the orchestration function or a session initialization module must build the pipeline. This may require resolving MSPC dependencies (ingress, registry, resolver, graph, compiler, emitter, subscription API, telemetry, audit log). Document what is available and what must be stubbed.

### 5.7 Halt Propagation

- `MSPCPipeline.execute_tick()` returns `PipelineTickResult` with `halted: bool`
- If `halted` is True, the orchestration function must propagate this (raise, return error, or signal upstream)
- RGE `{"selected": False}` is NOT a halt — it is normal mode-gated behavior
- Telemetry assembly failure → zero-triad → default topology → NOT a halt
- Orchestration function failure → fail-closed → halt

### 5.8 Constraints

- No modification to `MSPC_Pipeline.py` stages
- No modification to `RGERuntime` or `RGE_Bootstrap.py`
- Minimal modification to `RGE_Nexus_Adapter.py` (public accessor only, if Option B)
- No new governance authority
- No cross-tick state retention
- Topology context cleared at every tick boundary, unconditionally

### 5.9 Verification

```bash
# 1. Orchestration file exists
# (path depends on implementation — verify after creation)

# 2. RGE adapter has public accessor (if Option B chosen)
grep -n "get_last_result" "LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/RGE_Nexus_Adapter.py"

# 3. Topology provider clear() called unconditionally in orchestration
# (manual code review — grep for "clear()" in orchestration file)

# 4. Integration test (conceptual — may require stubs for MSPC dependencies)
# Execute one tick with non-trivial constraints
# Verify RGE produces non-default topology
# Verify MSPC receives non-None topology_context
# Verify topology_context is None after tick completes (cleared)
```

### 5.10 Phase Lock

```
Path: _Governance/Phase_Locks/Phase_M6C_Orchestration_Tick_Binding_Lock.json
```

```json
{
  "phase": "M6C",
  "title": "Orchestration Tick Binding",
  "status": "LOCKED",
  "new_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Tick_Orchestrator.py"
  ],
  "modified_files": [
    "LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/RGE_Nexus_Adapter.py"
  ],
  "rge_internals_modified": false,
  "mspc_pipeline_modified": false,
  "cross_tick_state": false,
  "halt_propagation_implemented": true,
  "governance_compliance_verified": true
}
```

---

## 6. M6 Closure

After Tasks A, B, and C are locked:

### 6.1 Final Phase Lock

```
Path: _Governance/Phase_Locks/Phase_M6_Integration_Closure_Lock.json
```

```json
{
  "phase": "M6",
  "title": "RGE ↔ MSPC Integration Closure",
  "status": "LOCKED",
  "sub_phases": ["M6A", "M6B", "M6C"],
  "integration_loop_complete": true,
  "tick_sequence": [
    "constraint_ingress",
    "nexus_tick_with_rge",
    "topology_handoff",
    "mspc_tick",
    "cleanup"
  ],
  "new_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Telemetry_Production/Task_Constraint_Provider.py",
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Topology_Context_Provider.py",
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Tick_Orchestrator.py"
  ],
  "modified_files": [
    "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Protocol/LP_Nexus/Logos_Protocol_Nexus.py",
    "LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/Integration/RGE_Nexus_Adapter.py"
  ],
  "rge_internals_modified": false,
  "mspc_pipeline_modified": false,
  "phase_5_frozen_artifacts_preserved": true,
  "phase_7_frozen_artifacts_preserved": true,
  "governance_invariants_preserved": {
    "rge_advisory_only": true,
    "no_rge_mspc_direct_coupling": true,
    "telemetry_immutable_within_tick": true,
    "no_cross_tick_feedback": true,
    "no_canonical_promotion": true,
    "fail_closed": true,
    "deny_by_default": true
  }
}
```

### 6.2 Known Debt (Post-M6)

Items explicitly out of M6 scope, tracked for future work:

1. **Governance-inferred constraints (Path 2):** Replace `DeclaredConstraintProvider` with inference from active Phase contracts, SMP pipeline state, and governance rules. Separate workstream.

2. **MSPC full construction:** If MSPC Pipeline is not yet instantiated in the codebase, Task C may produce a partial binding with stubs. Full MSPC session initialization is a prerequisite for live integration testing.

3. **RGE temporary prints:** Three `TEMPORARY AUDIT PRINT` statements remain in `RGE_Bootstrap.py`, plus prints in `Hysteresis_Governor.py`, `RGE_Nexus_Adapter.py`, and `Logos_Protocol_Nexus.py` (`TICK ORDER ->`). These are outside M6 scope but should be addressed in the broader 695-print cleanup (M6-print or Phase 2).

4. **Logos_Telemetry_Integration_Point status:** This file remains `DESIGN_ONLY`. With the revised Task A approach (context injection rather than separate participant), this file's role may need to be updated or deprecated. Decision deferred.

5. **End-to-end integration test:** A full tick with real constraints → real RGE scoring → real MSPC compilation requires all MSPC dependencies to be instantiated. This is a test infrastructure item, not an M6 blocker.

---

## 7. Governance Invariant Checklist (Binding)

| Invariant | Source | M6 Status |
|-----------|--------|:---------:|
| RGE subordination — advisory only | RGE_Subordination_Declaration.md | Preserved |
| No RGE → MSPC direct communication | Phase_6_Integration_Closure_Spec §4.4 | Preserved — TopologyContextProvider mediates |
| Telemetry immutability within tick | Constraint_Taxonomy_Spec §7.3 | Preserved — snapshot produced once, read-only |
| No cross-tick feedback | Constraint_Taxonomy_Spec §7.3 | Preserved — provider.clear() at tick boundary |
| No canonical promotion | Phase_7_Step_1_Governance_Addendum §6 | Preserved — RGE advice remains non-canonical |
| MSPC invariants | MSPC_Pipeline.py header | Preserved — topology_context is compilation input, not state mutation |
| Fail-closed on uncertainty | Governance_Log_Spec_v1 §3 | Preserved — zero-triad → default topology, MSPC halt → propagate |
| Deny-by-default | Core governance invariant | Preserved — no new authority surfaces |
| Runtime Module Header Contract | _Governance/Contracts/ | Required on all new files |
| Phase 5 freeze | PHASE_5_STEP_4_COMPLETION_AND_CLOSEOUT | Preserved — no NL externalization changes |
| Phase 7 freeze | Phase_7_Step_3_Integration_Exit | Preserved — no RGE router wiring changes |

---

## 8. GPT Prompt Generation Instructions

For each task, GPT should produce a single VS Code prompt that:

1. Begins with a constraint block (what MUST and MUST NOT happen)
2. Creates new files with canonical headers
3. Modifies existing files with minimal, targeted edits
4. Runs verification commands
5. Writes the sub-phase lock artifact
6. Reports results

Prompt sequencing:
- **Prompt 1:** Task A (constraint ingress + context injection)
- **Prompt 2:** Task B (topology context provider) — only after M6A lock is committed
- **Prompt 3:** Task C (orchestration binding) — only after M6B lock is committed
- **Prompt 4:** M6 closure lock — only after M6C lock is committed

Each prompt must be self-contained. No prompt may assume state from a prior prompt beyond the existence of committed artifacts.

---

END OF BLUEPRINT

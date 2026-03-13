# LOGOS V1 — Phase P4: Hardening & Validation Design Specification

**Document ID:** `LOGOS-V1-P4-HARDENING-VALIDATION`
**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires human governance ratification
**Parent:** `LOGOS_V1_Operational_Readiness_Blueprint.md`
**Depends On:** `LOGOS-V1-P3-INTEGRATION-WIRING` (P3.1 minimum — end-to-end pipeline functional)
**Phase:** P4 (fourth development phase)
**Date:** 2026-03-01

---

## 0. Cross-Reference Index

| Reference ID | Section | Description |
|---|---|---|
| P4.1 | §2 | V1 Test Suite |
| P4.2 | §3 | MRE Tightening |
| P4.3 | §4 | Error Handling & Halt Propagation |
| P4.4 | §5 | Governance Contract Enforcement |
| P4.5 | §6 | Operational Logging Coverage |
| P4.6 | §7 | Boundary Validation |

---

## 1. Phase Overview

P4 hardens the integrated system produced by P3. No new features. No new subsystems. P4 adds tests, tightens safety margins, improves error handling, and validates that governance invariants hold under adversarial and degenerate conditions.

**Prerequisite:** P3.1 complete (end-to-end SMP pipeline functional).

**Post-condition:** The system is demonstrably correct under normal operation, gracefully halts under adversarial conditions, and maintains all governance invariants at every execution boundary.

| Workstream | What It Does | Blocking for V1? |
|---|---|---|
| P4.1 Test Suite | Comprehensive automated tests | YES |
| P4.2 MRE Tightening | Replace permissive V1 limits with production values | YES |
| P4.3 Error Handling | Harden all try/except, validate halt propagation | YES |
| P4.4 Governance Enforcement | Wire SOP tools to runtime | NO (deferrable) |
| P4.5 Logging Coverage | Ensure all critical paths emit audit events | NO (deferrable) |
| P4.6 Boundary Validation | Validate every cross-layer contract | YES |

---

## 2. P4.1 — V1 Test Suite

### 2.1 Test Architecture

The V1 test suite is organized in three tiers matching the existing Phase-8 convention:

**Tier 1 — Unit Tests:** Individual component correctness in isolation. No cross-component dependencies. Mock all external interfaces.

**Tier 2 — Integration Tests:** Cross-component contracts. Verify that wired interfaces produce expected results. Limited mocking (only for optional subsystems).

**Tier 3 — End-to-End Tests:** Full pipeline from task submission to NL output. No mocking. Exercises the entire tick sequence.

### 2.2 Test Location

```
LOGOS_SYSTEM/TEST_SUITE/
├── V1/
│   ├── tier1_unit/
│   │   ├── test_smp_schema.py
│   │   ├── test_smp_store.py
│   │   ├── test_aa_catalog.py
│   │   ├── test_classification_tracker.py
│   │   ├── test_uwm_access_control.py
│   │   ├── test_scp_orchestrator.py
│   │   ├── test_promotion_evaluator.py
│   │   ├── test_canonical_smp_producer.py
│   │   ├── test_csp_canonical_store.py
│   │   ├── test_agent_wrappers.py
│   │   ├── test_agent_lifecycle_manager.py
│   │   ├── test_nexus_factory.py
│   │   ├── test_runtime_loop.py
│   │   ├── test_smp_routing_state.py
│   │   └── test_v1_mre_adapter.py
│   ├── tier2_integration/
│   │   ├── test_uwm_smp_lifecycle.py
│   │   ├── test_i1_scp_pipeline.py
│   │   ├── test_i2_mtp_pipeline.py
│   │   ├── test_i3_arp_pipeline.py
│   │   ├── test_logos_routing_statemachine.py
│   │   ├── test_nexus_tick_ordering.py
│   │   ├── test_promotion_full_cycle.py
│   │   ├── test_rge_mspc_topology_handoff.py
│   │   └── test_mre_halt_propagation.py
│   ├── tier3_e2e/
│   │   ├── test_single_task_pipeline.py
│   │   ├── test_multi_task_sequential.py
│   │   ├── test_task_with_stub_engines.py
│   │   ├── test_task_halt_on_budget.py
│   │   └── test_task_rejected_smp.py
│   ├── conftest.py
│   └── run_v1_suite.py
```

### 2.3 Tier 1 — Unit Test Specifications

**test_smp_schema.py:**
- Valid SMP construction succeeds
- Missing privation metadata raises SMPValidationError
- Empty payload accepted (valid edge case)
- Payload with executable content rejected (embedded code detection)
- SMP ID format enforced ("SMP:{hash}")
- Classification state must be in allowed set
- content_hash matches payload

**test_smp_store.py:**
- Create SMP, verify in store
- Get SMP by ID returns correct SMP
- Get nonexistent SMP returns None
- Duplicate SMP ID rejected
- SMP count accurate after creates
- Classification state mutated only via promote/reject (not direct assignment)

**test_aa_catalog.py:**
- Append AA to existing SMP succeeds
- Append AA to nonexistent SMP raises error
- Append AA to canonical SMP raises error
- AA hash computed correctly
- AA count increments on append
- AAs ordered by creation_timestamp

**test_classification_tracker.py:**
- conditional → provisional: valid
- conditional → canonical: valid (skip allowed)
- provisional → canonical: valid
- Any → rejected: valid (except canonical)
- canonical → anything: invalid (terminal)
- rejected → anything: invalid (terminal)
- conditional → conditional: invalid (no self-transition)
- regression (provisional → conditional): invalid

**test_uwm_access_control.py:**
- logos_agent reads all SMPs
- agent_i1 reads only SMPs with matching routing
- Unrecognized role returns None (deny-by-default)
- Provenance verification failure returns None

**test_scp_orchestrator.py:**
- Analyze with stub adapters produces I1AA
- I1AA bound to correct SMP ID
- Analysis exception produces rejection AA (fail-closed)
- Batch analysis preserves order

**test_promotion_evaluator.py:**
- No AAs: not eligible for provisional
- One AA: eligible for provisional
- I1+I2+I3 AAs: eligible for canonical
- Missing I3AA: not eligible for canonical
- Conflict AAs: not eligible

**test_canonical_smp_producer.py:**
- Produces C-SMP with "C-SMP:" prefix
- C-SMP classification_state is "canonical"
- C-SMP payload matches source
- C-SMP append_artifacts frozen
- C-SMP has full derivation lineage

**test_agent_wrappers.py:**
- Each wrapper implements all 4 NexusParticipant methods
- LogosAgent creates SMP from task
- LogosAgent routes to correct agent based on state
- I1 reads SMP, calls SCP, writes I1AA
- I2 reads SMP, calls MTP, writes I2AA
- I3 reads SMP, calls ARP, writes I3AA
- Wrappers handle missing optional engines gracefully

**test_agent_lifecycle_manager.py:**
- Constructs 4 participants from startup context
- Participant IDs match expected sorted order
- Invalid startup context raises activation error
- UWM and subsystem references injected correctly

**test_nexus_factory.py:**
- Builds LP Nexus with participants
- Participants registered in sorted order
- MRE adapter constructed with correct limits
- RGE adapter registration is optional (None accepted)
- Mesh enforcer rejects malformed packets

**test_runtime_loop.py:**
- Construction from valid startup context succeeds
- Construction from invalid context raises halt
- run_single processes one task
- Signal handler sets running flag to False

**test_smp_routing_state.py:**
- All transitions in ROUTING_TRANSITIONS are valid
- No transition from RESOLVED
- No transition from REJECTED
- Full lifecycle: CREATED → I1_PENDING → I1_COMPLETE → I3_PENDING → I3_COMPLETE → I2_PENDING → I2_COMPLETE → RESOLVED

**test_v1_mre_adapter.py:**
- pre_tick returns GREEN below limit
- pre_tick returns RED at limit
- post_tick increments counter
- Multiple participants tracked independently

### 2.4 Tier 2 — Integration Test Specifications

**test_uwm_smp_lifecycle.py:**
- Create SMP → append I1AA → append I3AA → append I2AA → promote to provisional → promote to canonical. Verify all state at each step. Verify canonical SMP closed to further AAs.

**test_i1_scp_pipeline.py:**
- Construct I1AgentParticipant with real UWM and SCP orchestrator. Send route packet. Verify I1AA appears in UWM. Verify response packet emitted.

**test_i2_mtp_pipeline.py:**
- Same pattern with I2 and MTP (stub engines). Verify I2AA with rendered_text.

**test_i3_arp_pipeline.py:**
- Same pattern with I3 and ARP (stub compiler). Verify I3AA.

**test_logos_routing_statemachine.py:**
- Submit task to LogosAgent. Simulate tick sequence (inject agent response packets). Verify routing state transitions. Verify promotion triggers at I2_COMPLETE. Verify output projection contains rendered_text.

**test_nexus_tick_ordering.py:**
- Register 5 participants with known IDs. Execute tick. Verify execute_tick called in lexicographic ID order. Verify SOP observer (if registered) executes last.

**test_promotion_full_cycle.py:**
- Full promotion from conditional through canonical with real UWM, real evaluator, real producer, real CSP store. Verify C-SMP in CSP store. Verify source SMP classification updated. Verify source SMP still accessible in UWM.

**test_rge_mspc_topology_handoff.py:**
- Construct RGE adapter (if importable) and MSPC runtime (if importable). Execute tick. Verify topology context set on MSPC. Verify topology cleared after MSPC tick.

**test_mre_halt_propagation.py:**
- Set MRE limit to 3 ticks per participant. Run 4 ticks. Verify MREHalt raised on tick 4. Verify tick result status is "halted". Verify runtime loop terminates cleanly.

### 2.5 Tier 3 — End-to-End Test Specifications

**test_single_task_pipeline.py:**
- Submit one task via SingleTaskSource. Run RuntimeLoop.run_single(). Verify result has status "completed" or "halted" (either is valid in V1 with stub engines). Verify result has task_id matching input. Verify rendered_output is non-empty string (even if stub).

**test_multi_task_sequential.py:**
- Submit 3 tasks. Verify each produces a result. Verify task ordering preserved. Verify UWM contains 3 SMPs. Verify CSP contains 0-3 C-SMPs (depending on promotion outcomes).

**test_task_with_stub_engines.py:**
- Run with all optional engines absent (no MTP, no ARP, no RGE, no MSPC). Verify system still completes. Verify stub output produced. This is the minimum viable V1 configuration.

**test_task_halt_on_budget.py:**
- Set tick budget to 5. Submit task. Verify result status is "halted" with reason containing "budget". Verify no infinite loop.

**test_task_rejected_smp.py:**
- Construct scenario where promotion fails (e.g., force conflict AA). Verify SMP ends in REJECTED state. Verify output still produced (with rejection metadata).

### 2.6 Test Infrastructure

**conftest.py:**
```python
import pytest

@pytest.fixture
def mock_startup_context():
    """Minimal valid LOGOS_AGENT_READY dict for testing."""
    return {
        "status": "LOGOS_AGENT_READY",
        "logos_identity": {
            "logos_agent_id": "LOGOS:test-001",
            "session_id": "test-session-001",
        },
        "logos_session": {"session_id": "test-session-001"},
        "constructive_compile_output": {
            "logos_agent_id": "LOGOS:test-001",
            "universal_session_id": "test-session-001",
            "prepared_bindings": {},
        },
        "agent_orchestration_plan": {
            "logos_agent_id": "LOGOS:test-001",
            "universal_session_id": "test-session-001",
            "agents_planned": ["I1", "I2", "I3"],
            "protocols_planned": ["SCP", "ARP", "MTP"],
            "execution": "FORBIDDEN",
            "phase": "Phase-E",
            "status": "ORCHESTRATION_PLAN_PREPARED",
        },
    }

@pytest.fixture
def mock_task():
    """Minimal valid task dict."""
    return {
        "task_id": "test-task-001",
        "input": "What is the nature of truth?",
    }
```

**run_v1_suite.py:**
```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "LOGOS_SYSTEM/TEST_SUITE/V1/", "-v", "--tb=short"],
    capture_output=True, text=True,
)
print(result.stdout)
print(result.stderr)
sys.exit(result.returncode)
```

### 2.7 Target Test Count

| Tier | Estimated Tests | Pass Requirement |
|---|---|---|
| Tier 1 | 80-120 | 100% (all must pass) |
| Tier 2 | 30-50 | 100% (all must pass) |
| Tier 3 | 5-10 | 100% (all must pass) |
| Total | 115-180 | 100% green suite |

### 2.8 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_1_V1_Test_Suite_Lock.json
```

---

## 3. P4.2 — MRE Tightening

### 3.1 Problem Statement

P1 introduced `V1MREAdapter` with a permissive 1000-tick-per-participant limit. This was necessary for initial development. With the end-to-end pipeline functional, the MRE limits must be tightened to prevent runaway execution.

Additionally, the standalone `MeteredReasoningEnforcer` (in ARP_Core) tracks iteration count, time bounds, novelty rate, and repetition rate. The `V1MREAdapter` tracks only tick count. The two systems must be reconciled.

### 3.2 Existing MRE Implementations

| Component | Location | Interface | Tracks |
|---|---|---|---|
| `MeteredReasoningEnforcer` | `ARP_Core/metered_reasoning_enforcer.py` | `update()`, `should_continue()`, `telemetry_snapshot()` | iterations, time, novelty, repetition |
| `V1MREAdapter` | P1.2 Nexus_Factory.py | `pre_tick(pid)`, `post_tick(pid)` | tick count per participant |
| `MREGovernor` | Every Nexus file | `pre_execute(pid)`, `post_execute(pid)` | delegates to wrapped MRE |

### 3.3 Reconciled MRE Architecture

Replace `V1MREAdapter` with `ProductionMREAdapter` that wraps `MeteredReasoningEnforcer` per participant:

```python
class ProductionMREAdapter:
    """
    Production MRE adapter for LP Nexus.
    Creates one MeteredReasoningEnforcer per participant.
    Delegates to the full MRE implementation for tick/time/novelty enforcement.
    """

    def __init__(
        self,
        max_ticks_per_participant: int = 100,
        max_time_per_participant: float = 30.0,
        mre_level: float = 0.5,
    ) -> None:
        self._max_ticks = max_ticks_per_participant
        self._max_time = max_time_per_participant
        self._mre_level = mre_level
        self._enforcers: Dict[str, MeteredReasoningEnforcer] = {}

    def _get_enforcer(self, pid: str) -> MeteredReasoningEnforcer:
        if pid not in self._enforcers:
            self._enforcers[pid] = MeteredReasoningEnforcer(
                mre_level=self._mre_level,
                max_iterations=self._max_ticks,
                max_time_seconds=self._max_time,
            )
        return self._enforcers[pid]

    def pre_tick(self, pid: str) -> Dict[str, Any]:
        enforcer = self._get_enforcer(pid)
        if not enforcer.should_continue():
            return {"state": "RED"}
        return {"state": "GREEN"}

    def post_tick(self, pid: str) -> Dict[str, Any]:
        enforcer = self._get_enforcer(pid)
        output_sig = f"{pid}:tick:{enforcer.iterations}"
        enforcer.update(output_sig)
        state = enforcer.evaluate_state()
        return {"state": state}

    def telemetry(self) -> Dict[str, Dict[str, Any]]:
        return {pid: e.telemetry_snapshot() for pid, e in self._enforcers.items()}
```

### 3.4 Production Limits

| Parameter | V1 Development | V1 Production | Rationale |
|---|---|---|---|
| max_ticks_per_participant | 1000 | 100 | Single task needs ~7 ticks. 100 provides 14x headroom. |
| max_time_per_participant | None | 30.0s | Prevent indefinite blocking per agent per session. |
| mre_level | N/A | 0.5 | Moderate sensitivity. RED on >50% repetition rate. |
| tick_budget_per_task | 50 | 50 | No change (already reasonable). |

### 3.5 MRE Reset Between Tasks

When `RuntimeLoop._process_task()` completes, the MRE enforcers for all participants should be reset for the next task. Otherwise, tick counts accumulate across tasks and early exhaustion occurs.

```python
# In RuntimeLoop._process_task(), after result:
self._mre_adapter.reset()

# In ProductionMREAdapter:
def reset(self) -> None:
    """Reset all per-participant enforcers for next task."""
    self._enforcers.clear()
```

### 3.6 MRE Telemetry Emission

After each task, emit MRE telemetry to the operational logger:

```python
# In RuntimeLoop._process_task(), before reset:
telemetry = self._mre_adapter.telemetry()
self._logger.log(
    Channel.PROTOCOL,
    Severity.TRACE,
    "mre_telemetry",
    optional={"task_id": task_id, "mre_snapshot": telemetry},
)
```

### 3.7 File Changes

| File | Change |
|---|---|
| `Nexus_Factory.py` (P1.2) | Replace V1MREAdapter with ProductionMREAdapter |
| `Runtime_Loop.py` (P1.3) | Add MRE reset between tasks, telemetry emission |

### 3.8 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_2_MRE_Tightening_Lock.json
```

---

## 4. P4.3 — Error Handling & Halt Propagation

### 4.1 Error Taxonomy

Every error in the V1 runtime falls into exactly one of these categories:

| Category | Response | Severity |
|---|---|---|
| **MRE Halt** | Tick aborts, task halted | HALT |
| **Mesh Rejection** | Packet dropped, tick continues | ERROR |
| **Nexus Violation** | Tick aborts, task halted | HALT |
| **SMP Validation Error** | Operation rejected, caller receives error | ERROR |
| **Classification Error** | Operation rejected, caller receives error | ERROR |
| **AA Append Error** | Operation rejected, caller receives error | ERROR |
| **MTP Pipeline Failure** | I2 produces stub output, task continues | WARN |
| **ARP Compiler Failure** | I3 produces stub output, task continues | WARN |
| **RGE Import Failure** | RGE disabled, task continues without topology | WARN |
| **MSPC Boot Failure** | MSPC disabled, task continues without compilation | WARN |
| **Import Error** | Module unavailable, feature degraded | WARN |
| **Startup Halt** | System does not start | HALT |
| **Runtime Activation Halt** | System started but runtime loop failed to construct | HALT |
| **Tick Budget Exhaustion** | Task halted after max ticks | HALT |
| **Signal (SIGTERM/SIGINT)** | Runtime loop terminates cleanly | STATUS |

### 4.2 Halt Propagation Verification

Every halt source must produce a result with `status: "halted"` and a non-empty `halt_reason`. The following table traces each halt from origin to output:

| Halt Source | Where Caught | Result Field | halt_reason Format |
|---|---|---|---|
| MREHalt | StandardNexus.tick() | tick result | `"MRE HALT (pre/post): {participant_id}"` |
| MeshRejection | StandardNexus._route_inbound() | logged, packet dropped | Not a halt (degraded) |
| NexusViolation | RuntimeLoop._execute_tick() | tick result | `"Nexus violation: {detail}"` |
| RuntimeActivationHalt | RuntimeLoop.__init__() | raised to caller | `"Runtime activation failed: {detail}"` |
| TickBudgetExhaustion | RuntimeLoop._process_task() | tick result | `"Tick budget exhausted ({N} ticks)"` |
| SIGTERM | RuntimeLoop.run() | clean shutdown | `"Signal received"` |

### 4.3 Try/Except Audit

Every `try/except` in P1-P3 code must be audited against these rules:

**Rule 1: No bare except.** Every except must catch a specific exception class.

**Rule 2: No silent swallow.** Every except must either log the error or propagate it. `pass` in an except block is forbidden.

**Rule 3: Fail-closed default.** If the correct response to an error is unclear, halt. Never degrade silently.

**Rule 4: Error context.** Every logged error must include: module path, tick_id (if in tick context), error type, and error detail.

### 4.4 Hardening Checklist

Each of the following must be verified:

```
[ ] RuntimeLoop.__init__: all construction failures raise RuntimeActivationHalt
[ ] RuntimeLoop._execute_tick: nexus.tick() wrapped, all exceptions produce halted result
[ ] RuntimeLoop._process_task: tick budget enforced, no infinite loop possible
[ ] RuntimeLoop.run: signal handler tested, clean shutdown verified
[ ] AgentLifecycleManager.activate: construction failures raise descriptive errors
[ ] LogosAgent._on_tick: routing state machine handles all states, no unreachable branches
[ ] LogosAgent._evaluate_and_resolve: promotion failure produces REJECTED, not exception
[ ] I1._on_tick: SCP failure produces rejection AA, not propagated exception
[ ] I2._on_tick: MTP failure produces stub output, not propagated exception
[ ] I3._on_tick: ARP failure produces stub output, not propagated exception
[ ] NexusFactory: all import failures produce None (optional) or raise (required)
[ ] UWM create_smp: validation failure raises SMPCreationError
[ ] UWM append_aa: canonical SMP check enforced
[ ] UWM promote: monotonic ladder enforced, regression raises ClassificationError
[ ] MRE pre_tick: RED state raises MREHalt via MREGovernor
[ ] MeshEnforcer: malformed packets raise MeshRejection
```

### 4.5 File Changes

No new files. Modifications to all P1-P3 files where try/except blocks exist.

### 4.6 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_3_Error_Handling_Lock.json
```

---

## 5. P4.4 — Governance Contract Enforcement

### 5.1 Problem Statement

SOP has governance enforcement tools built but unwired:

- `InvariantEnforcer` — validates DRAC assembly invariants via SHA-256 attestation
- `Invariant_Drift_Detector` — detects mutation of invariant files (stub, needs governance decisions)
- `SMP_Policy_Validator` — validates SMP hash integrity and origin classification
- `Governance_Validator` — validates governance schema conformance (stub)
- `Phase_Enforcer` — validates execution phase boundaries (stub)

### 5.2 V1 Enforcement Scope

Not all SOP tools need to be wired for V1. The minimum enforcement set:

**Wire for V1:**

1. **InvariantEnforcer.enforce()** — Call during RuntimeLoop construction (after startup, before first tick). Validates DRAC assembly invariants are unmodified. Failure halts runtime.

2. **SMPPolicyValidator.validate_smp()** — Call during UWM `create_smp()`. Validates SMP hash integrity before storage. Failure rejects SMP creation.

3. **Protocol binding validation** — Verify at construction time that I1↔SCP, I2↔MTP, I3↔ARP bindings match `Runtime_Spine_Lock_And_Key_Execution_Contract.json`. Failure halts activation.

**Defer to V1.1:**

4. Invariant_Drift_Detector (requires governance routing decisions)
5. Governance_Validator (stub, needs schema)
6. Phase_Enforcer (stub, needs boundary model)

### 5.3 Wiring Points

**InvariantEnforcer → RuntimeLoop:**

```python
# In RuntimeLoop.__init__(), before nexus construction:
try:
    from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol.SOP_Tools.Governance_Control.Invariant_Enforcer import InvariantEnforcer
    InvariantEnforcer.enforce()
except Exception as exc:
    raise RuntimeActivationHalt(f"Invariant enforcement failed: {exc}")
```

**SMPPolicyValidator → UWM:**

```python
# In UWMWriteAPI.create_smp(), after SMP construction:
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.System_Operations_Protocol.SOP_Tools.Governance_Control.SMP_Policy_Validator import SMPPolicyValidator

smp_dict = {
    "origin": source,
    "payload": payload,
    "hash": smp.provenance.content_hash,
    "phase": "runtime",
}
SMPPolicyValidator.validate_smp(smp_dict)
```

**Binding validation → AgentLifecycleManager:**

```python
# In AgentLifecycleManager.activate(), after participant construction:
REQUIRED_BINDINGS = {
    "agent_i1": "SCP",
    "agent_i2": "MTP",
    "agent_i3": "ARP",
    "agent_logos": "Logos_Protocol",
}

for pid, participant in participants.items():
    expected = REQUIRED_BINDINGS.get(pid)
    actual = getattr(participant, "_protocol_binding", None)
    if expected and actual != expected:
        raise RuntimeActivationHalt(
            f"Binding violation: {pid} bound to {actual}, expected {expected}"
        )
```

### 5.4 File Changes

| File | Change |
|---|---|
| `Runtime_Loop.py` | Add InvariantEnforcer call in constructor |
| `SMP_Store.py` (P2.1) | Add SMPPolicyValidator call in create_smp |
| `Agent_Lifecycle_Manager.py` (P1.1) | Add binding validation in activate |

### 5.5 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_4_Governance_Enforcement_Lock.json
```

---

## 6. P4.5 — Operational Logging Coverage

### 6.1 Problem Statement

The `Operational_Logger` is fully built with Channel, Severity, and JSONL output. It is wired during startup (13 log points in `LOGOS_SYSTEM.py`). It is not wired during runtime.

### 6.2 Required Logging Points

Every log call follows the same pattern:

```python
self._logger.log(channel, severity, message, optional={...})
```

Or the convenience methods: `self._logger.status(channel, message)`, `self._logger.halt(channel, message, ...)`.

| Location | Channel | Severity | Message | Optional Fields |
|---|---|---|---|---|
| RuntimeLoop construction success | STARTUP | STATUS | `"runtime_loop_constructed"` | session_id |
| RuntimeLoop construction failure | STARTUP | HALT | `"runtime_activation_failed"` | error_type, error_detail |
| Task received | AGENT | STATUS | `"task_received"` | task_id |
| SMP created | MEMORY | STATUS | `"smp_created"` | smp_id, smp_type |
| AA appended | MEMORY | STATUS | `"aa_appended"` | aa_id, aa_type, bound_smp_id |
| Classification promoted | MEMORY | STATUS | `"classification_promoted"` | smp_id, from_state, to_state |
| I1 analysis complete | PROTOCOL | STATUS | `"i1_analysis_complete"` | smp_id |
| I2 rendering complete | PROTOCOL | STATUS | `"i2_rendering_complete"` | smp_id, pipeline_status |
| I3 reasoning complete | PROTOCOL | STATUS | `"i3_reasoning_complete"` | smp_id |
| C-SMP produced | MEMORY | STATUS | `"csmp_produced"` | csmp_id, source_smp_id |
| Task completed | AGENT | STATUS | `"task_completed"` | task_id, status, tick_count |
| Task halted | AGENT | HALT | `"task_halted"` | task_id, halt_reason, tick_count |
| MRE RED state | GOVERNANCE | WARN | `"mre_red_state"` | participant_id, tick_count |
| MRE telemetry | PROTOCOL | TRACE | `"mre_telemetry"` | task_id, snapshot |
| Mesh rejection | GOVERNANCE | ERROR | `"mesh_rejection"` | participant_id, reason |
| Tick completed | PROTOCOL | TRACE | `"tick_completed"` | tick_id, participants_executed |
| Runtime terminated | STARTUP | STATUS | `"runtime_terminated"` | session_id, total_ticks |
| InvariantEnforcer pass | GOVERNANCE | STATUS | `"invariant_enforcement_pass"` | hash |
| InvariantEnforcer fail | GOVERNANCE | HALT | `"invariant_enforcement_fail"` | error_detail |

### 6.3 Logger Injection

The operational logger is created in `LOGOS_SYSTEM.py` and should be passed through to the RuntimeLoop via the startup context dict. RuntimeLoop distributes it to subsystems:

```python
# In RuntimeLoop.__init__():
self._logger = self._build_logger(startup_context)

# In AgentLifecycleManager.activate():
# Each agent wrapper receives logger reference for AA/SMP log points

# In UWMWriteAPI constructor:
# Logger reference for SMP/AA creation logging
```

### 6.4 File Changes

| File | Change |
|---|---|
| `Runtime_Loop.py` | Add 8 log points (task received, completed, halted, tick, MRE, terminated, invariant) |
| `Agent_Wrappers.py` | Add 3 log points (I1/I2/I3 completion) |
| `SMP_Store.py` | Add 3 log points (create, append_aa, promote) |
| `CSP_Canonical_Store.py` | Add 1 log point (csmp_produced) |
| `Nexus_Factory.py` | Add 1 log point (mesh_rejection, if observable) |

### 6.5 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_5_Logging_Coverage_Lock.json
```

---

## 7. P4.6 — Boundary Validation

### 7.1 Problem Statement

The V1 system has 7 cross-layer boundaries where contracts can be violated at runtime. P4.6 adds runtime assertions at each boundary.

### 7.2 Boundary Inventory

**Boundary 1: Startup → Runtime**
Contract: `LOGOS_AGENT_READY` dict shape (P1-IF-03)
Validation point: `RuntimeLoop.__init__()`, `AgentLifecycleManager.__init__()`
Assertion: all required keys present, session_id is string, logos_agent_id is string

**Boundary 2: Task → SMP**
Contract: task dict → SMP (P3-IF-01)
Validation point: `LogosAgent._create_smp_from_task()`
Assertion: task has `task_id` and `input` keys

**Boundary 3: SMP → Agent Routing**
Contract: StatePacket routing protocol (P3-IF-02)
Validation point: each agent `_on_tick()` method
Assertion: received packet has `type` and `content.smp_id` fields

**Boundary 4: Agent → UWM Write**
Contract: AA append rules (P2-IF-02, P2-IF-04)
Validation point: `UWMWriteAPI.append_aa()`
Assertion: bound SMP exists, SMP not canonical, AA type valid

**Boundary 5: UWM → Promotion**
Contract: promotion criteria (P2-IF-06)
Validation point: `PromotionEvaluator.evaluate_for_canonical()`
Assertion: all required AA types checked, classification state checked

**Boundary 6: MTP → Output**
Contract: EgressPipelineResult (P3-IF-04)
Validation point: I2 `_on_tick()` after MTP call
Assertion: result has `status`, `emitted_text()` callable

**Boundary 7: RuntimeLoop → OutputSink**
Contract: tick result shape (P1-IF-07)
Validation point: `RuntimeLoop._process_task()` before emit
Assertion: result has all 9 required fields

### 7.3 Validation Implementation

Each boundary gets a validation function that raises a descriptive error on violation:

```python
def validate_startup_context(ctx: Dict[str, Any]) -> None:
    """Validate LOGOS_AGENT_READY dict shape."""
    required_keys = ["status", "logos_identity", "logos_session",
                     "constructive_compile_output", "agent_orchestration_plan"]
    for key in required_keys:
        if key not in ctx:
            raise RuntimeActivationHalt(f"Missing startup context key: {key}")
    if ctx["status"] != "LOGOS_AGENT_READY":
        raise RuntimeActivationHalt(f"Invalid startup status: {ctx['status']}")
    identity = ctx["logos_identity"]
    if not isinstance(identity.get("logos_agent_id"), str):
        raise RuntimeActivationHalt("logos_agent_id must be string")
    if not isinstance(identity.get("session_id"), str):
        raise RuntimeActivationHalt("session_id must be string")


def validate_task(task: Dict[str, Any]) -> None:
    """Validate task dict shape."""
    if "task_id" not in task:
        raise ValueError("Task missing required field: task_id")
    if "input" not in task:
        raise ValueError("Task missing required field: input")


def validate_route_packet(packet_payload: Dict[str, Any]) -> None:
    """Validate routing StatePacket payload."""
    if "type" not in packet_payload:
        raise ValueError("Route packet missing type")
    if "content" not in packet_payload:
        raise ValueError("Route packet missing content")
    if "smp_id" not in packet_payload["content"]:
        raise ValueError("Route packet content missing smp_id")


def validate_tick_result(result: Dict[str, Any]) -> None:
    """Validate tick result against P1-IF-07."""
    required = ["tick_id", "session_id", "task_id", "status"]
    for key in required:
        if key not in result:
            raise ValueError(f"Tick result missing required field: {key}")
    if result["status"] not in ("completed", "halted", "no_output"):
        raise ValueError(f"Invalid tick result status: {result['status']}")
```

### 7.4 File Manifest

| File | Path | Purpose |
|---|---|---|
| Boundary_Validators.py | `Logos_Core/Orchestration/` | All 7 boundary validation functions |

### 7.5 Phase Lock

```
_Governance/Phase_Locks/Phase_P4_6_Boundary_Validation_Lock.json
```

---

## 8. Dependency Graph (P4 Internal)

```
P3.1 (SMP Pipeline) ──→ P4.1 Test Suite (requires functional pipeline)
                    ├──→ P4.2 MRE Tightening (requires functional pipeline)
                    ├──→ P4.3 Error Handling (requires all code paths)
                    ├──→ P4.4 Governance Enforcement (independent after P3.1)
                    ├──→ P4.5 Logging Coverage (independent after P3.1)
                    └──→ P4.6 Boundary Validation (independent after P3.1)
```

All P4 workstreams can proceed in parallel once P3.1 is complete. P4.1 depends on all other P4 workstreams being in progress (tests validate hardened behavior), so P4.1 should be written last but can start with Tier 1 tests immediately.

Recommended execution order:
1. P4.6 Boundary Validation (small, foundational)
2. P4.3 Error Handling (audit existing code)
3. P4.2 MRE Tightening (mechanical replacement)
4. P4.4 Governance Enforcement (3 wiring points)
5. P4.5 Logging Coverage (mechanical addition)
6. P4.1 Test Suite (comprehensive, written against hardened system)

---

## 9. Complete File Manifest (All P4 Workstreams)

### New Files (15-20+)

| File | Workstream | Path |
|---|---|---|
| Boundary_Validators.py | P4.6 | `Logos_Core/Orchestration/` |
| test_smp_schema.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_smp_store.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_aa_catalog.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_classification_tracker.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_uwm_access_control.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_scp_orchestrator.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_promotion_evaluator.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_canonical_smp_producer.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_agent_wrappers.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_agent_lifecycle_manager.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_nexus_factory.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_runtime_loop.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_smp_routing_state.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| test_v1_mre_adapter.py | P4.1 | `TEST_SUITE/V1/tier1_unit/` |
| 9 tier2 test files | P4.1 | `TEST_SUITE/V1/tier2_integration/` |
| 5 tier3 test files | P4.1 | `TEST_SUITE/V1/tier3_e2e/` |
| conftest.py | P4.1 | `TEST_SUITE/V1/` |
| run_v1_suite.py | P4.1 | `TEST_SUITE/V1/` |

### Modified Files (8-12)

| File | Workstream | Change |
|---|---|---|
| `Nexus_Factory.py` | P4.2 | Replace V1MREAdapter with ProductionMREAdapter |
| `Runtime_Loop.py` | P4.2, P4.3, P4.4, P4.5 | MRE reset + telemetry, error audit, InvariantEnforcer, 8 log points |
| `Agent_Wrappers.py` | P4.3, P4.5 | Error handling audit, 3 log points |
| `Agent_Lifecycle_Manager.py` | P4.4 | Binding validation |
| `SMP_Store.py` | P4.4, P4.5 | SMPPolicyValidator, 3 log points |
| `AA_Catalog.py` | P4.3 | Error handling audit |
| `Classification_Tracker.py` | P4.3 | Error handling audit |
| `CSP_Canonical_Store.py` | P4.5 | 1 log point |

---

## 10. GPT Prompt Generation Instructions

**Prompt 1 (P4.6):** Create Boundary_Validators.py. Integrate validation calls into RuntimeLoop, AgentLifecycleManager, LogosAgent, agent wrappers. Run import test.

**Prompt 2 (P4.3):** Audit all try/except blocks in P1-P3 files. Apply 4 rules (no bare except, no silent swallow, fail-closed default, error context). Run existing tests.

**Prompt 3 (P4.2):** Create ProductionMREAdapter. Replace V1MREAdapter in Nexus_Factory.py. Add MRE reset and telemetry to RuntimeLoop. Run MRE tests.

**Prompt 4 (P4.4):** Wire InvariantEnforcer, SMPPolicyValidator, binding validation. Run existing tests.

**Prompt 5 (P4.5):** Add all logging points. Verify logger injection path. Run full pipeline and inspect JSONL output.

**Prompt 6 (P4.1):** Create full test suite. Run all tiers. Target: 100% pass rate, 115+ tests.

---

## 11. V1 Acceptance Criteria

After P4 completion, V1 is accepted if and only if:

1. **Test suite green:** All Tier 1, 2, 3 tests pass (100%).
2. **Governance invariants hold:** InvariantEnforcer passes, binding validation passes, SMP hash integrity validated.
3. **Halt propagation verified:** Every halt source produces a halted result with reason.
4. **MRE enforced:** Production limits active, no participant exceeds 100 ticks or 30 seconds.
5. **Logging complete:** All 19 logging points emit to JSONL. Log file parseable. No missing channels.
6. **Boundary contracts validated:** All 7 boundaries checked at runtime. Invalid inputs produce descriptive errors.
7. **End-to-end functional:** A task submitted to stdin produces governed NL on stdout.
8. **Stub degradation graceful:** With all optional engines absent, system still completes with stub output.

---

END OF P4 SPECIFICATION

# LOGOS V1 — P3.2 Orchestration Wiring Blueprint

**Status:** DESIGN_ONLY  
**Execution Authority:** NONE  
**Purpose:** Governance review artifact prior to P3.2 runtime mutation.  
**Date:** 2026-03-04  
**Phase:** P3.2 — Nexus-Mediated Orchestration Migration  

---

## 1. HEADER

This document is a pre-execution governance artifact. It describes the intended architectural transition from centralized SMP lifecycle execution inside `LogosAgentParticipant` to Nexus-mediated multi-participant orchestration.

No runtime code changes may be made until this artifact has been reviewed and approved. The document is append-only and must not be modified once execution begins.

---

## 2. CURRENT SYSTEM STATE

### P3.1 Implementation Summary

The SMP lifecycle is currently executed entirely inside `LogosAgentParticipant._on_tick()` via an internal string-based routing state machine.

**Current routing states:**

```
INIT
SMP_CREATED
I1_COMPLETE
I3_COMPLETE
I2_COMPLETE
RESOLVED_PENDING
RESOLVED
HALTED
```

**Current runtime flow:**

```
RuntimeLoop
    ↓
NexusFactory (MRE enforcement)
    ↓
Nexus
    ↓
LogosAgentParticipant
    ↓
    [internal: SMP creation]
    [internal: SCP analysis → I1AA append]
    [internal: ARP delegation → I3AA append]
    [internal: MTP render → I2AA append]
    [internal: PromotionEvaluator gate]
    [internal: Canonical SMP production]
    ↓
output
```

### Participant Status

| Participant | Class | Current State |
|---|---|---|
| `agent_logos` | `LogosAgentParticipant` | Active — executes full pipeline internally |
| `agent_i1` | `I1AgentParticipant` | Registered — stubbed (`stub_tick`) |
| `agent_i2` | `I2AgentParticipant` | Registered — stubbed (`stub_tick`) |
| `agent_i3` | `I3AgentParticipant` | Registered — stubbed (`stub_tick`) |

I1, I2, and I3 participants are registered in the Nexus but produce no AA output and perform no real work. All agent-phase logic is simulated inside `LogosAgentParticipant`.

### Audit Finding

The P3 Integration Wiring Spec (`BLUEPRINTS/LOGOS_V1_P3_Integration_Wiring_Spec.md`) requires orchestration to be distributed across participants via Nexus coordination. The current state collapses all agent authority into a single participant, which violates the distributed orchestration contract and creates a routing mismatch against blueprint-defined states.

---

## 3. TARGET ARCHITECTURE (P3.2)

### Required Runtime Flow

```
RuntimeLoop
    ↓
NexusFactory (MRE enforcement)
    ↓
Nexus
    ↓ (StatePacket routing)
    ├── I1AgentParticipant   → SCP analysis → I1AA append → project packet
    ├── I3AgentParticipant   → ARP delegation → I3AA append → project packet
    ├── I2AgentParticipant   → MTP render → I2AA append → project packet
    └── LogosAgentParticipant → promotion gate → canonical production → output
```

### Key Architectural Properties

- Each participant acts on an SMP when routed to it by Nexus
- Each participant projects a `StatePacket` signaling the next routing destination
- Nexus enforces deterministic tick ordering via MRE tick governor
- `LogosAgentParticipant` retains authority over SMP creation, promotion evaluation, and canonical production
- No participant writes to the canonical store except `LogosAgentParticipant`
- No AA is appended after canonicalization

---

## 4. PARTICIPANT RESPONSIBILITY MATRIX

### LogosAgentParticipant

| Responsibility | Description |
|---|---|
| SMP creation | Creates `input_task` SMP from task context on first tick |
| Promotion evaluation | Calls `PromotionEvaluator.evaluate_for_canonical()` after all AAs present |
| Canonical SMP production | Calls `CanonicalSMPProducer.produce()` on eligible path |
| Canonical store write | Calls `CSPCanonicalStore.store()` — only participant with write authority |
| Final output emission | Returns `completed` result with `smp_id`, `csmp_id`, `classification`, `rendered_output` |
| HALTED output | Returns `halted` result with `halt_reason` on ineligible path |

### I1AgentParticipant

| Responsibility | Description |
|---|---|
| SCP analysis | Calls `SCPOrchestrator.analyze(smp)` |
| I1AA generation | Appends `I1AA` via `SMPStore.append_aa()` |
| Routing projection | Projects `StatePacket` with signal `route_to_i3` |

### I3AgentParticipant

| Responsibility | Description |
|---|---|
| ARP delegation | Produces deterministic ARP delegation content |
| I3AA generation | Appends `I3AA` via `SMPStore.append_aa()` |
| Routing projection | Projects `StatePacket` with signal `route_to_i2` |

### I2AgentParticipant

| Responsibility | Description |
|---|---|
| MTP rendering | Produces rendered output from SMP payload |
| I2AA generation | Appends `I2AA` via `SMPStore.append_aa()` |
| Routing projection | Projects `StatePacket` with signal `route_to_logos` |

---

## 5. LIFECYCLE TRANSITION (P3.2)

The following defines the distributed tick-by-tick lifecycle after P3.2 migration is complete.

### Tick 1 — LogosAgentParticipant (SMP Bootstrap)

```
Input:  task context
Action: create_smp(smp_type="input_task", ...)
        store smp_id
        project StatePacket(signal="route_to_i1", smp_id=...)
Output: {"status": "in_progress", "smp_id": ...}
```

### Tick 2 — I1AgentParticipant (SCP Analysis)

```
Input:  StatePacket(signal="route_to_i1")
Action: smp = smp_store.get_smp(smp_id)
        aa  = scp_orchestrator.analyze(smp)
        smp_store.append_aa(smp_id, aa.aa_type, "I1", aa.content)
        smp_store.promote_classification(smp_id, "provisional")
        project StatePacket(signal="route_to_i3", smp_id=...)
Output: {"agent": "I1", "status": "analyzed", "aa_id": ..., "aa_type": ...}
```

### Tick 3 — I3AgentParticipant (ARP Delegation)

```
Input:  StatePacket(signal="route_to_i3")
Action: i3_content = {"arp_delegation": "deterministic_placeholder", "session_id": ...}
        smp_store.append_aa(smp_id, "I3AA", "I3", i3_content)
        project StatePacket(signal="route_to_i2", smp_id=...)
Output: {"agent": "I3", "status": "delegated", ...}
```

### Tick 4 — I2AgentParticipant (MTP Render)

```
Input:  StatePacket(signal="route_to_i2")
Action: smp = smp_store.get_smp(smp_id)
        i2_content = {"rendered_output": f"Resolved: {smp.payload['input']}", "session_id": ...}
        smp_store.append_aa(smp_id, "I2AA", "I2", i2_content)
        project StatePacket(signal="route_to_logos", smp_id=...)
Output: {"agent": "I2", "status": "rendered", "rendered_output": ...}
```

### Tick 5 — LogosAgentParticipant (Promotion Evaluation)

```
Input:  StatePacket(signal="route_to_logos")
Action: eval_result = promotion_evaluator.evaluate_for_canonical(smp_id)
        if eligible  → routing_state = "RESOLVED_PENDING"
        if ineligible → routing_state = "HALTED"
Output (eligible):   {"status": "in_progress", "routing_state": "RESOLVED_PENDING", ...}
Output (ineligible): {"status": "halted", "halt_reason": ..., ...}
```

### Tick 6 — LogosAgentParticipant (Canonical Production)

```
Input:  routing_state == "RESOLVED_PENDING"
Action: aas  = uwm_reader.get_aas_for_smp(smp_id, requester_role="logos_agent")
        smp  = smp_store.get_smp(smp_id)
        csmp = canonical_smp_producer.produce(smp, aas)
        canonical_store.store(csmp)
        csmp_id = csmp.header.smp_id
        routing_state = "RESOLVED"
Output: {"status": "completed", "smp_id": ..., "csmp_id": ...,
         "classification": "canonical", "rendered_output": ...}
```

---

## 6. STATEPACKET ROUTING CONTRACT

Each participant that is not the terminal node must project a `StatePacket` encoding the next routing destination. The Nexus reads these projections to determine which participant receives the next tick.

### Defined Routing Signals

| Signal | Produced by | Consumed by |
|---|---|---|
| `route_to_i1` | `LogosAgentParticipant` (tick 1) | `I1AgentParticipant` |
| `route_to_i3` | `I1AgentParticipant` (tick 2) | `I3AgentParticipant` |
| `route_to_i2` | `I3AgentParticipant` (tick 3) | `I2AgentParticipant` |
| `route_to_logos` | `I2AgentParticipant` (tick 4) | `LogosAgentParticipant` |

### StatePacket Minimum Schema

```python
StatePacket(
    source_agent_id: str,       # participant_id of projecting agent
    routing_signal: str,        # one of the signals above
    smp_id: str,                # current SMP being processed
    payload: Dict[str, Any],    # optional additional context
)
```

Packets are immutable once projected. No participant may modify a received packet.

---

## 7. MIGRATION STRATEGY

Migration proceeds in six locked stages. No stage may begin until the prior stage passes validation. Each stage is a standalone atomic change.

### Stage 1 — Dual-Path Bootstrap

Enable each I-participant to perform its own AA generation while the `LogosAgent` internal state machine remains as fallback. Both paths produce identical SMP state.

**Blast radius:** I1, I2, I3 `_on_tick()` only.  
**Validation:** I-participants produce correct AAs; LogosAgent fallback unchanged.

### Stage 2 — I1 Logic Migration

Remove the I1 simulation branch from `LogosAgentParticipant._on_tick()`. Replace with a `route_to_i1` projection. `I1AgentParticipant` now solely responsible for `I1AA`.

**Blast radius:** `I1AgentParticipant._on_tick()`, `LogosAgentParticipant._on_tick()`.  
**Validation:** I1AA still present, `provisional` classification still promoted.

### Stage 3 — I3 Logic Migration

Remove the I3 simulation branch from `LogosAgentParticipant._on_tick()`. Replace with `route_to_i3` projection from I1. `I3AgentParticipant` now solely responsible for `I3AA`.

**Blast radius:** `I3AgentParticipant._on_tick()`.  
**Validation:** I3AA still present after tick 3.

### Stage 4 — I2 Logic Migration

Remove the I2 simulation branch from `LogosAgentParticipant._on_tick()`. Replace with `route_to_i2` projection from I3. `I2AgentParticipant` now solely responsible for `I2AA`.

**Blast radius:** `I2AgentParticipant._on_tick()`.  
**Validation:** I2AA still present; rendered output correct.

### Stage 5 — LogosAgent State Machine Reduction

Remove all internal routing state strings beyond `RESOLVED_PENDING`, `RESOLVED`, and `HALTED` from `LogosAgentParticipant`. The SMP_CREATED / I1_COMPLETE / I3_COMPLETE / I2_COMPLETE states are now owned by their respective participants.

**Blast radius:** `LogosAgentParticipant.__init__` and `_on_tick()`.  
**Validation:** LogosAgent only handles evaluation and canonicalization ticks.

### Stage 6 — Nexus Routing Enforcement

Enable `StatePacket` projection and consumption in the Nexus. Wire `project_state()` returns from each participant into Nexus routing logic. Confirm MRE tick governor continues to enforce tick budget.

**Blast radius:** `Logos_Protocol_Nexus.py`, participant `_project()` methods.  
**Validation:** Full 6-tick round-trip produces identical output to P3.1 baseline.

---

## 8. GOVERNANCE INVARIANTS

The following invariants must remain intact throughout all migration stages. Any stage that would violate an invariant is a governance halt condition.

| Invariant | Description |
|---|---|
| Append-only AA model | AAs may only be appended, never modified or removed |
| No AA writes after canonicalization | Once `RESOLVED`, no further `append_aa` calls permitted |
| PromotionEvaluator gate unchanged | `evaluate_for_canonical()` call signature and semantics must not change |
| Canonical store exclusivity | Only `LogosAgentParticipant` may call `canonical_store.store()` |
| Canonical SMP immutability | Once stored, a CSMP may not be modified |
| Deterministic tick ordering | Tick sequence must remain `I1 → I3 → I2 → Logos` |
| MRE tick governor enforcement | `NexusFactory` tick budget enforcement must remain active |
| RuntimeLoop tick budget | `RuntimeLoop` max tick count must not be altered |
| No SMP mutation after canonicalization | SMP payload is frozen once CSMP is written |

---

## 9. NON-GOALS

P3.2 explicitly does NOT:

- Modify DRAC (Deliberate Reasoning Audit Chain)
- Modify MSPC (Multi-Step Planning Controller)
- Modify SOP (System Orchestration Protocol)
- Modify `AgentLifecycleManager` lifecycle transitions or state machine
- Introduce new reasoning logic or inference capability
- Change canonical classification rules or CSMP schema
- Modify `RuntimeLoop` tick driver or budget enforcement
- Add new subsystem imports or dependencies beyond those injected in P3.1
- Change the `NexusParticipant` interface contract
- Alter governance enforcement at `_Governance/` or `Boundary_Validators`

---

## 10. SUCCESS CRITERIA

P3.2 is considered complete when all of the following are verified:

1. `LogosAgentParticipant._on_tick()` no longer contains I1, I2, or I3 simulation branches
2. `I1AgentParticipant._on_tick()` performs SCP analysis and appends `I1AA`
3. `I3AgentParticipant._on_tick()` appends `I3AA` with deterministic ARP content
4. `I2AgentParticipant._on_tick()` appends `I2AA` with rendered output
5. Each I-participant projects a `StatePacket` encoding the next routing destination
6. Nexus routes between participants using projected `StatePacket` signals
7. `RuntimeLoop` drives tick progression without modification
8. Canonical SMP production remains gated by `PromotionEvaluator`
9. Ineligible path still results in `HALTED` with `halt_reason`
10. Full 6-tick eligible run produces `completed` result with `csmp_id` and `rendered_output`
11. P3 audit routing mismatch finding is resolved
12. `py_compile` clean on all modified files
13. All existing P3.1 behavioral tests continue to pass

---

*Document status: DESIGN_ONLY. No runtime code may be modified based on this artifact until execution authority is explicitly granted.*

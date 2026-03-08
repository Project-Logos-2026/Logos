# Logos Core Design Specification v1

## Governance Header

| Field | Value |
|---|---|
| Artifact Type | Design Specification |
| Authority | Canonical |
| Subsystem | Logos Core |
| Tier | 0 (Foundation) |
| Version | 1.0.0 |
| Status | Active |
| Depends On | None (root dependency) |
| Depended On By | All runtime subsystems |
| RGE Integration | RGE_Design_Specification_v3.md §8.4 |
| Mutability | Controlled (version-gated amendments only) |

---

## 1. Purpose and Scope

### 1.1 Subsystem Identity

Logos Core is the sovereign center of the LOGOS runtime. It is the unified substrate from which all runtime authority originates. It is not a peer subsystem alongside the three agent-protocol pairs (I1↔SCP, I2↔MTP, I3↔ARP). It is the fixed reference frame that governs them.

### 1.2 Architectural Position

The LOGOS runtime geometry places three agent-protocol pairs at equidistant positions around a central axis. Logos Core occupies that axis. The Radial Genesis Engine (RGE) operates on the three peripheral pairs as its domain — evaluating, scoring, and recommending topology configurations across those pairs. Logos Core is the entity that receives RGE's advisory output and decides whether to accept, reject, or override it.

If Logos Core were decomposed into a separate agent-protocol pair, it would simultaneously be a member of the evaluated set and the evaluator of that set. This breaks the geometry and introduces a self-referential authority loop that violates fail-closed governance. The unification eliminates this structural defect.

### 1.3 Scope of This Specification

This specification defines the complete operational surface of Logos Core:

- Tick lifecycle model
- Activation sequencing (Phase-G ordering)
- SMP pipeline architecture
- Unified Working Memory (UWM) schema and access control
- Protocol routing framework
- PXL gate interface
- Telemetry production contract
- Nexus participation model
- Sovereign authority model (mutation gates, identity issuance, UWM write authority)
- Agent orchestration and AA governance
- Governance mode parameterization (P1/P2 extension point)
- RGE integration surface
- Downstream subsystem integration matrix

### 1.4 What This Specification Does Not Cover

- Internal implementation of I1, I2, I3, SCP, MTP, or ARP (covered by their respective design specs)
- RGE internal scoring, selection, or hysteresis logic (covered by RGE_Design_Specification_v3.md)
- Phase 5 Natural Language Externalization (covered by externalization schemas)
- IEL Foundations and mathematical resources (static reference library, not runtime logic)
- Coq/PXL proof corpus internals (covered by EMP design spec)

---

## 2. Canonical Directory Structure

### 2.1 Root Location

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/
```

### 2.2 Internal Layout

```
Logos_Core/
├── __init__.py
├── Logos_Agents/
│   ├── __init__.py
│   └── Logos_Agent/
│       └── runtime.py
└── Logos_Protocol/
    ├── __init__.py
    ├── LP_Core/
    │   ├── Activation_Sequencer/
    │   ├── Agent_Integration/
    │   │   ├── I1/ (I1.py, scp_pipeline/)
    │   │   ├── I2/ (I2.py, mtp_pipeline/)
    │   │   ├── I3/ (I3.py, arp_cycle/)
    │   │   └── types.py
    │   ├── Agent_Orchestration/
    │   │   ├── agent_orchestration.py
    │   │   ├── agent_planner.py
    │   │   ├── coordinator.py
    │   │   ├── dispatch.py
    │   │   └── test_determinism.py
    │   └── Identity_Generator/
    │       ├── agent_identity.py
    │       ├── attestation.py
    │       ├── audit_and_emit.py
    │       ├── commitment_ledger.py
    │       ├── consciousness_safety_adapter.py
    │       ├── identity_loader.py
    │       ├── persist_identity.py
    │       └── schemas.py
    ├── LP_Nexus/
    │   ├── __init__.py
    │   └── Logos_Protocol_Nexus.py
    ├── LP_Tools/
    │   └── Recursion_Grounding/
    │       ├── Phase_E_Tick_Engine.py
    │       └── recursion_identity_runtime.py
    ├── Runtime_Operations/
    │   ├── Orchestration/
    │   └── tests/
    └── Logos_Agent_Resources/
        ├── Cognition_Normalized/
        ├── IEL_Foundations/ (static reference; not runtime)
        ├── math_categories/ (static reference; not runtime)
        └── privation_library.json
```

### 2.3 Boundary Declaration

Everything under `Logos_Core/` is within Logos Core's authority boundary. No external subsystem may directly import from, write to, or modify modules within this tree except through the interfaces defined in this specification.

---

## 3. Tick Lifecycle Model

### 3.1 Dual-Phase Architecture

Each tick executes in two phases. This model aligns with RGE_Design_Specification_v3.md §4 (Dual-Phase Tick Lifecycle).

**Phase A — Governance and Configuration (Pre-Cognitive)**

This phase establishes the invariant frame for the tick. No cognitive work occurs.

| Step | Responsibility | Description |
|---|---|---|
| A.1 | Logos Core | Receive tick context from Nexus via `execute_tick(context)` |
| A.2 | Logos Core | Evaluate governance mode (P1 active / P2 passive) from tick context |
| A.3 | Logos Core | Validate PXL gate status; halt if proof state is invalid |
| A.4 | Logos Core | Receive RGE StatePacket from prior tick's projection (if available) |
| A.5 | Logos Core | Accept, reject, or override RGE topology recommendation |
| A.6 | Logos Core | Resolve Activation Topology Map (ATM) for this tick |
| A.7 | Logos Core | Bind agent activation priorities per ATM |
| A.8 | Logos Core | Emit tick governance header to audit trail |

**Phase B — Cognitive Execution (Agent Processing)**

This phase executes the cognitive work. Agent ordering follows the ATM resolved in Phase A.

| Step | Responsibility | Description |
|---|---|---|
| B.1 | Logos Core | Determine task source: external input (P1) or internal work order (P2) |
| B.2 | Logos Core | Classify task constraints and derive telemetry triad t(x) |
| B.3 | Logos Core | Inject telemetry into SMP and route to primary agent |
| B.4 | Primary Agent | Execute protocol-specific processing via bound pipeline |
| B.5 | Secondary Agent | Execute protocol-specific processing if multi-agent tick |
| B.6 | Tertiary Agent | Execute protocol-specific processing if tri-agent tick |
| B.7 | Logos Core | Collect Append Artifacts (AAs) from agent processing |
| B.8 | Logos Core | Evaluate AA acceptance/rejection per governance rules |
| B.9 | Logos Core | Write accepted AAs to UWM (sole write authority) |
| B.10 | Logos Core | Compute commutation residuals and stability scalars |
| B.11 | Logos Core | Assemble TelemetrySnapshot and project to RGE |
| B.12 | Logos Core | Emit tick completion record to audit trail |

### 3.2 Tick Boundary Invariants

The following invariants must hold at every tick boundary:

- **INV-TL-01:** No cognitive work occurs during Phase A.
- **INV-TL-02:** No governance reconfiguration occurs during Phase B.
- **INV-TL-03:** The ATM resolved in A.6 is immutable for the duration of Phase B.
- **INV-TL-04:** Agent execution order in Phase B is determined solely by the ATM.
- **INV-TL-05:** If Phase A fails at any step, the tick halts. No Phase B execution occurs.
- **INV-TL-06:** If Phase B fails at any step, partial results are discarded. UWM state reverts to pre-tick state.
- **INV-TL-07:** TelemetrySnapshot (B.11) is assembled from this tick's data only; no cross-tick accumulation.

### 3.3 Multi-Tick Processing

The 7-tick cognitive lifecycle defined in prior architecture documents maps onto this model as follows. Each tick is a complete Phase A → Phase B cycle. The lifecycle's seven stages (intake, classification, primary processing, secondary processing, tertiary processing, synthesis, output) each occupy one tick. The ATM may differ between ticks — RGE topology recommendations are re-evaluated at each tick boundary.

Cross-tick state is carried exclusively through UWM. Agents do not retain state between ticks. The SMP created at intake (tick 1) accumulates AAs across subsequent ticks until the lifecycle completes at output (tick 7).

---

## 4. Activation Sequencing (Phase-G Ordering)

### 4.1 Bootstrap Sequence

Session activation follows the Phase-G ordering protocol. This is a strict total order with no parallel execution permitted.

| Phase | Action | Precondition |
|---|---|---|
| G.0 | PXL gate validation | None (first action) |
| G.1 | Lock-and-Key verification | G.0 pass |
| G.2 | Universal Session ID issuance | G.1 pass |
| G.3 | Logos Core identity establishment | G.2 pass |
| G.4 | Agent ID issuance (I1, I2, I3) | G.3 pass |
| G.5 | Protocol binding (I1↔SCP, I2↔MTP, I3↔ARP) | G.4 pass |
| G.6 | RGE initialization (default topology) | G.5 pass |
| G.7 | UWM initialization | G.6 pass |
| G.8 | Session ready | G.7 pass |

### 4.2 Sequencing Invariants

- **INV-AS-01:** Phase-G ordering is a strict total order. No phase may execute before its precondition phase completes successfully.
- **INV-AS-02:** Failure at any phase halts the bootstrap. The session does not partially activate.
- **INV-AS-03:** Lock-and-Key verification (G.1) confirms the dual-compile proof status from STARTUP/PXL_Gate.
- **INV-AS-04:** Agent IDs are issued in deterministic order: I1 first, I2 second, I3 third.
- **INV-AS-05:** Protocol binding at G.5 establishes the identity-to-protocol mapping. This mapping defines which protocol internals each agent may access. The mapping is immutable for the session lifetime.
- **INV-AS-06:** RGE initialization at G.6 sets the default activation topology. This is the starting configuration; RGE may recommend changes at subsequent tick boundaries.
- **INV-AS-07:** The distinction between protocol *binding* (immutable, G.5) and activation *priority* (mutable via ATM per tick) is fundamental. Binding defines scope; priority defines ordering. RGE modifies priority, never binding.

### 4.3 Binding vs. Priority Distinction

This distinction requires explicit definition because governance artifacts predating the Logos Core unification may conflate them.

**Binding** (immutable per session): I1 can only access SCP internals. I2 can only access MTP internals. I3 can only access ARP internals. No agent may access another agent's protocol internals. This is the Lock-and-Key invariant.

**Priority** (mutable per tick via ATM): For a given task, which agent executes first (primary), second (secondary), and third (tertiary). RGE recommends priority ordering based on topology scoring. Logos Core accepts or overrides.

An agent's `AuthorityScope` is defined by binding. An agent's `ActivationOrder` is defined by priority. Changing priority does not expand scope. This is why RGE-mediated dynamic orchestration does not violate the A1 Non-Escalation principle.

---

## 5. SMP Pipeline Architecture

### 5.1 SMP Lifecycle

A Semantic Message Packet (SMP) is the fundamental unit of work in the LOGOS runtime. Its lifecycle spans the 7-tick cognitive cycle.

| Stage | Tick | Action | Authority |
|---|---|---|---|
| Creation | 1 | SMP created with task payload, governance header, empty AA catalog | Logos Core |
| Classification | 2 | Task constraints classified, triad derived, SMP tagged | Logos Core |
| Primary Processing | 3 | Primary agent processes SMP, generates AAs | Agent (propose) / Logos Core (accept/reject) |
| Secondary Processing | 4 | Secondary agent processes SMP, generates AAs | Agent (propose) / Logos Core (accept/reject) |
| Tertiary Processing | 5 | Tertiary agent processes SMP, generates AAs | Agent (propose) / Logos Core (accept/reject) |
| Synthesis | 6 | Cross-agent AA integration, coherence validation | Logos Core |
| Output | 7 | Final SMP state written to UWM, externalization triggered | Logos Core |

### 5.2 SMP Schema (Required Fields)

| Field | Type | Authority | Mutability |
|---|---|---|---|
| `smp_id` | UUID | Logos Core (creation) | Immutable |
| `session_id` | UUID | Logos Core (from G.2) | Immutable |
| `tick_created` | int | Logos Core | Immutable |
| `task_payload` | dict | External (P1) or Internal (P2) | Immutable after creation |
| `governance_header` | GovernanceHeader | Logos Core | Immutable |
| `constraint_classification` | ConstraintClassification | Logos Core (tick 2) | Immutable after classification |
| `triad` | Triad(c_E, c_G, c_T) | Logos Core (tick 2) | Immutable after derivation |
| `aa_catalog` | List[AppendArtifact] | Logos Core (append-only) | Append-only |
| `classification_status` | ClassificationLadder | Logos Core | Monotonic (can only advance) |
| `lineage` | List[LineageRecord] | Logos Core | Append-only |

### 5.3 SMP Invariants

- **INV-SMP-01:** SMP payload is immutable after creation. No agent or subsystem may modify the original task.
- **INV-SMP-02:** AA catalog is append-only. Entries are never removed or modified.
- **INV-SMP-03:** Only Logos Core may append to the AA catalog. Agents propose AAs; Logos Core validates and appends.
- **INV-SMP-04:** Classification status is monotonic. An SMP may only advance along the classification ladder, never regress.
- **INV-SMP-05:** Every SMP state transition is recorded in the lineage field with tick number, agent ID, and action type.
- **INV-SMP-06:** An SMP with no governance header is invalid and must be rejected at creation.

---

## 6. Unified Working Memory (UWM)

### 6.1 Purpose

UWM is the sole persistent state surface for the LOGOS runtime within a session. All cross-tick state is held in UWM. All agent-visible state is mediated through UWM.

### 6.2 Access Control Model

| Actor | Read | Write | Scope |
|---|---|---|---|
| Logos Core | Full | Full | All UWM state |
| I1 | Mediated | None | SCP-relevant state only |
| I2 | Mediated | None | MTP-relevant state only |
| I3 | Mediated | None | ARP-relevant state only |
| RGE | Projection only | None | StatePacket via Nexus |
| SOP | Observability only | None | Metrics and telemetry |
| All others | None | None | No access |

### 6.3 Write Authority Chain

All UWM writes follow this chain:

1. Agent proposes AA via its pipeline
2. AA routed to Logos Core via protocol routing
3. Logos Core validates AA against governance rules
4. Logos Core validates AA against SMP schema
5. Logos Core validates write bounds (rate limiting, size limits)
6. Logos Core acquires write authorization token (time-bounded, 5s expiry)
7. Logos Core executes atomic write
8. Logos Core emits write audit event
9. On failure at any step: write rejected, UWM unchanged, rejection logged

### 6.4 UWM Invariants

- **INV-UWM-01:** Logos Core is the sole entity with UWM write permission. No exception.
- **INV-UWM-02:** Agent reads are mediated: each agent sees only the state relevant to its protocol binding.
- **INV-UWM-03:** All writes are atomic. A partial write that fails mid-execution rolls back completely.
- **INV-UWM-04:** All writes produce audit events. A write without an audit event is a governance violation.
- **INV-UWM-05:** Write authorization tokens expire after 5 seconds. An expired token cannot authorize a write.
- **INV-UWM-06:** UWM state at tick boundary N is the complete input for tick N+1. No other state source exists.

---

## 7. Protocol Routing Framework

### 7.1 Routing Model

Logos Core mediates all inter-agent and agent-to-protocol communication. There is no direct agent-to-agent communication channel.

```
I1 ──→ Logos Core ──→ I2
         ↕
I3 ──→ Logos Core ──→ SCP/MTP/ARP (via bound pipelines)
```

### 7.2 Routing Rules

- **RR-01:** Agent-to-agent messages are routed through Logos Core. The sending agent does not know the destination agent's identity.
- **RR-02:** Agent-to-protocol messages are routed through Logos Core to the agent's bound protocol only. Cross-protocol routing is blocked.
- **RR-03:** Protocol output (AAs) routes back through Logos Core for governance validation before UWM write.
- **RR-04:** RGE topology advisories are received by Logos Core via Nexus state projection, not via the agent routing channel.
- **RR-05:** SOP telemetry is emitted by Logos Core to the observability surface. SOP data never enters the cognitive routing path.

### 7.3 Routing and ATM Interaction

The ATM determines activation *order*, not routing *paths*. All routing paths pass through Logos Core regardless of which agent is primary. The ATM only affects the sequence in which agents are invoked during Phase B of a tick.

---

## 8. PXL Gate Interface

### 8.1 Purpose

The PXL (Protopraxic Logic) gate is the proof-gated execution boundary. It enforces the safety-first principle: admissibility must be established before reasoning is permitted.

### 8.2 Interface Contract

| Method | Input | Output | Semantics |
|---|---|---|---|
| `validate_proof_status()` | session context | `ProofStatus` (VALID / INVALID / DEGRADED) | Checks STARTUP/PXL_Gate compilation state |
| `check_admissibility(smp)` | SMP reference | `AdmissibilityResult` (ADMITTED / DENIED / DEFERRED) | Evaluates whether SMP processing is permitted |
| `verify_lock_and_key()` | dual-compile hash | `bool` | Confirms LEM discharge and bijection proof status |

### 8.3 PXL Gate Invariants

- **INV-PXL-01:** `validate_proof_status()` is the first call in Phase-G bootstrap (G.0). If it returns INVALID, bootstrap halts.
- **INV-PXL-02:** `check_admissibility()` is called before any SMP enters the cognitive pipeline. DENIED halts processing for that SMP.
- **INV-PXL-03:** DEGRADED proof status permits continued operation with restricted capabilities (specific restrictions TBD per degradation mode ladder).
- **INV-PXL-04:** The PXL gate never caches results across ticks. Each check is evaluated fresh.
- **INV-PXL-05:** PXL gate logic is stateless. It reads proof state; it does not produce or modify proofs.

---

## 9. Telemetry Production Contract

### 9.1 Purpose

Logos Core is the sole producer of the telemetry that feeds RGE's scoring pipeline. This section defines what Logos Core computes, when it computes it, and the exact data contract for the output.

### 9.2 Production Chain

The telemetry production chain executes during Phase B of each tick, specifically at steps B.2 (triad derivation), B.10 (residuals and scalars), and B.11 (snapshot assembly).

```
Task arrival
  → Constraint enumeration from task + governance context
    → extract_triad(task) → normalize → Triad(c_E, c_G, c_T)
  → MESH commutation validation
    → commutation residuals R_j per protocol-axis pair
  → Protocol telemetry aggregation
    → stability scalars S_j per protocol-axis pair
  → Assemble TelemetrySnapshot
    → Project to RGE via Nexus state projection
```

### 9.3 TelemetrySnapshot Schema

This schema is the canonical interface between Logos Core (producer) and RGE (consumer). It aligns with RGE_Design_Specification_v3.md §3.2.

| Field | Type | Bounds | Producer |
|---|---|---|---|
| `triad` | Triad(c_E, c_G, c_T) | Each component ∈ [0, 1]; sum = 1.0 | Logos Core (B.2) |
| `raw_constraint_counts` | dict[str, int] | Non-negative integers | Logos Core (B.2) |
| `commutation_residuals` | dict[str, float] | Per-protocol-axis; ≥ 0.0 | Logos Core (B.10) |
| `stability_scalars` | dict[str, float] | Per-protocol-axis; ∈ [0, 1] | Logos Core (B.10) |
| `coupling_weights` | dict[str, float] | Pairwise; ∈ [0, 1] | Logos Core (B.10) |
| `tick_number` | int | Monotonically increasing | Logos Core |
| `session_id` | UUID | Matches session | Logos Core |
| `timestamp` | ISO-8601 | Wall clock | Logos Core |

### 9.4 Telemetry Invariants

- **INV-TEL-01:** TelemetrySnapshot is a frozen (immutable) dataclass. Once assembled, it cannot be modified.
- **INV-TEL-02:** TelemetrySnapshot is per-tick. It contains data from the current tick only.
- **INV-TEL-03:** If triad derivation fails, the snapshot is not assembled. RGE receives no input for that tick and retains prior topology (hysteresis).
- **INV-TEL-04:** Commutation residuals and stability scalars are computed after agent processing completes (B.10), not before.
- **INV-TEL-05:** The telemetry production chain is not optional. Every tick that completes Phase B must produce a TelemetrySnapshot.

---

## 10. Nexus Participation Model

### 10.1 Participant Identity

Logos Core participates in the StandardNexus tick loop as a registered `NexusParticipant`. Its `participant_id` determines execution order within the Nexus tick (alphabetical sort on string keys).

### 10.2 Interface

| Method | Semantics |
|---|---|
| `execute_tick(context)` | Receives tick context from Nexus. Executes Phase A → Phase B. Returns nothing. |
| `project_state()` | Returns the current tick's TelemetrySnapshot for consumption by other Nexus participants (primarily RGE). |
| `get_participant_id()` | Returns the string identifier used for tick ordering. |

### 10.3 Ordering Consideration

RGE must execute after Logos Core within the same Nexus tick so that RGE can consume the TelemetrySnapshot produced by Logos Core's `project_state()`. This is controlled by `participant_id` string ordering. If Logos Core's ID sorts before RGE's ID, the ordering is correct.

### 10.4 Nexus Invariants

- **INV-NX-01:** Logos Core's `execute_tick()` is the sole entry point for tick processing. No other path into the cognitive loop exists.
- **INV-NX-02:** `project_state()` returns an immutable snapshot. The caller cannot modify Logos Core state through this interface.
- **INV-NX-03:** If `execute_tick()` throws, the Nexus must handle the failure per its own error policy. Logos Core does not retry.

---

## 11. Sovereign Authority Model

### 11.1 Principle

Logos Core holds absolute authority within the LOGOS runtime. This authority is not delegated, shared, or negotiable. It is the architectural equivalent of a constitutional sovereign: it defines the rules under which all other entities operate.

### 11.2 Authority Enumeration

| Authority | Description | Delegation |
|---|---|---|
| UWM Write | Sole entity permitted to write to UWM | Never delegated |
| Identity Issuance | Issues session IDs, agent IDs, protocol binding tokens | Never delegated |
| AA Acceptance | Decides which proposed AAs are written to UWM | Never delegated |
| Topology Decision | Accepts, rejects, or overrides RGE topology recommendations | Never delegated |
| Task Admission | Decides whether an SMP enters the cognitive pipeline | Never delegated |
| Agent Lifecycle | Creates, suspends, and terminates agent instances | Never delegated |
| Governance Mode | Determines P1/P2 mode for each tick | Never delegated |
| Audit Emission | Produces governance audit records | Never delegated |

### 11.3 What Agents May Do

Agents (I1, I2, I3) are evaluative entities. They may:

- Receive mediated read access to UWM state within their protocol scope
- Execute processing logic within their bound protocol
- Propose AAs as output of their processing
- Request state access via protocol routing

Agents may not:

- Write to UWM directly
- Communicate with other agents directly
- Access protocol internals outside their binding
- Override or influence Logos Core's authority decisions
- Retain state between ticks

### 11.4 What RGE May Do

RGE is an advisory subsystem. It may:

- Receive TelemetrySnapshot via Nexus state projection
- Score topology configurations
- Recommend a topology via StatePacket

RGE may not:

- Write to UWM
- Modify the ATM directly
- Override Logos Core's topology decision
- Access agent state or SMP content
- Influence governance mode

### 11.5 Authority Invariants

- **INV-AUTH-01:** No entity other than Logos Core may write to UWM. Violation is a critical governance failure.
- **INV-AUTH-02:** No entity other than Logos Core may issue identity tokens. Violation is a critical governance failure.
- **INV-AUTH-03:** Expanding any component's authority scope beyond what is defined in this specification is a structural violation, not a configuration choice.
- **INV-AUTH-04:** Authority cannot be acquired by proximity, frequency, or emergent behavior. Authority is assigned by this specification and enforced by mutation gates.

---

## 12. Agent Orchestration and AA Governance

### 12.1 Orchestration Model

Agent orchestration follows the ATM resolved in Phase A of each tick. The ATM assigns three roles:

| Role | Description |
|---|---|
| Primary | First agent to process the SMP. Receives initial task context. |
| Secondary | Second agent. Receives SMP with primary agent's accepted AAs. |
| Tertiary | Third agent. Receives SMP with primary and secondary AAs. |

Not all ticks require all three agents. Simple tasks may complete with primary-only processing. The ATM determines how many agents participate.

### 12.2 AA Validation Pipeline

When an agent proposes an AA:

1. AA must conform to AA_CORE schema (required fields: `aa_id`, `source_agent_id`, `source_protocol`, `tick_number`, `payload`, `governance_tag`)
2. AA must reference a valid, active SMP
3. AA's `source_agent_id` must match the currently executing agent
4. AA's `source_protocol` must match the agent's bound protocol
5. AA payload must pass protocol-specific validation rules
6. AA must not duplicate an existing AA in the SMP's catalog (content-hash check)
7. Logos Core issues accept or reject decision
8. Accepted AAs are appended to SMP's AA catalog and written to UWM
9. Rejected AAs are logged with rejection reason; agent is notified

### 12.3 AA Invariants

- **INV-AA-01:** An AA without a valid `source_agent_id` matching the executing agent is rejected unconditionally.
- **INV-AA-02:** An AA referencing a protocol other than the agent's bound protocol is rejected unconditionally.
- **INV-AA-03:** AA acceptance does not imply correctness. It implies governance compliance. Semantic validity is the agent's responsibility.
- **INV-AA-04:** Rejected AAs are never silently dropped. Every rejection produces an audit event with a machine-readable reason code.

---

## 13. Identity Management

### 13.1 Identity Hierarchy

| Identity | Issued By | Lifetime | Format |
|---|---|---|---|
| Universal Session ID | Logos Core (G.2) | Session | UUID v4 |
| Logos Core Identity | Logos Core (G.3) | Session | Deterministic from session ID |
| Agent ID (I1) | Logos Core (G.4) | Session | Deterministic from session ID + ordinal |
| Agent ID (I2) | Logos Core (G.4) | Session | Deterministic from session ID + ordinal |
| Agent ID (I3) | Logos Core (G.4) | Session | Deterministic from session ID + ordinal |
| Protocol Binding Token | Logos Core (G.5) | Session | Hash of agent ID + protocol ID |
| Write Authorization Token | Logos Core (per write) | 5 seconds | Nonce + timestamp |

### 13.2 Identity Invariants

- **INV-ID-01:** All identity tokens are deterministic given the session ID and issuance ordinal. Two sessions with the same seed produce identical identity hierarchies.
- **INV-ID-02:** Agent IDs are issued in strict order: I1, I2, I3. No other ordering is permitted.
- **INV-ID-03:** Protocol binding tokens are one-to-one. One agent binds to exactly one protocol. One protocol binds to exactly one agent.
- **INV-ID-04:** Identity issuance is a Phase-G operation only. No new identities are issued after G.5.
- **INV-ID-05:** Write authorization tokens are single-use. A token consumed by one write cannot authorize another.

---

## 14. Governance Mode Parameterization

### 14.1 Design Intent

The governance mode determines the authority profile active for a given tick. This is the structural accommodation for the potential P1/P2 runtime distinction.

### 14.2 Mode Definitions

**P1 Mode (Active Runtime — User Input Present)**

- Task source: external input only
- Authority model: full deny-by-default
- No autonomous task generation
- No internal work order processing
- All governance gates enforced at maximum strictness

**P2 Mode (Passive Runtime — System Active, No User Input)**

- Task source: internal work orders permitted
- Authority model: same mutation gates, same fail-closed semantics
- Task intake surface accepts internally generated work orders
- Governance gate strictness: unchanged for mutation, write, and identity operations
- Relaxation scope: task *source* constraint only; authority *mechanism* unchanged

### 14.3 Mode Resolution

Governance mode is resolved at Phase A, step A.2 of each tick. The mode is determined by the tick context received from Nexus. The resolution logic is:

- If tick context contains external input: P1 mode
- If tick context contains no external input and session is in passive state: P2 mode
- If tick context is ambiguous: P1 mode (fail-closed to stricter mode)

### 14.4 Mode Invariants

- **INV-GM-01:** Governance mode is resolved once per tick and is immutable for that tick.
- **INV-GM-02:** P2 mode does not expand any entity's authority scope. It only changes the permitted task source.
- **INV-GM-03:** The default mode is P1. A tick that cannot determine its mode operates in P1.
- **INV-GM-04:** Mode transitions (P1→P2, P2→P1) occur only at tick boundaries.

### 14.5 Deferred Design Note

The specific mechanics of P2 internal work order generation, validation, and scheduling are not defined in this specification. This section establishes the structural hook. A P2 Operations Addendum will define the specifics when the P2 runtime design is finalized. Until that addendum exists, Logos Core operates exclusively in P1 mode.

---

## 15. RGE Integration Surface

### 15.1 Cross-Reference

This section defines Logos Core's side of the integration contract specified in RGE_Design_Specification_v3.md §8.4. Both specifications must remain mutually consistent.

### 15.2 Logos Core → RGE (Telemetry Production)

| Data | Source | Channel | Frequency |
|---|---|---|---|
| TelemetrySnapshot | Logos Core Phase B.11 | Nexus `project_state()` | Every completed tick |

Logos Core produces; RGE consumes. The channel is the Nexus state projection mechanism. Logos Core does not call RGE directly.

### 15.3 RGE → Logos Core (Topology Advisory)

| Data | Source | Channel | Frequency |
|---|---|---|---|
| StatePacket | RGE `project_state()` | Nexus state projection | Every RGE tick |

RGE produces; Logos Core consumes at Phase A.4 of the next tick. The StatePacket contains a topology recommendation (which agent-protocol pair should be primary, secondary, tertiary).

### 15.4 Logos Core Decision Authority

Upon receiving a StatePacket:

1. Logos Core validates the StatePacket schema
2. Logos Core evaluates the recommendation against governance constraints
3. Logos Core applies hysteresis threshold (minimum score delta required to change topology)
4. Logos Core issues one of three decisions:
   - **ACCEPT:** Apply recommended topology as the ATM for the next tick
   - **REJECT:** Retain current topology; log rejection reason
   - **OVERRIDE:** Apply a different topology determined by governance logic; log override reason

### 15.5 RGE Integration Invariants

- **INV-RGE-01:** Logos Core never calls RGE methods directly. Communication is exclusively via Nexus state projection.
- **INV-RGE-02:** RGE's StatePacket is advisory. Logos Core is never obligated to accept it.
- **INV-RGE-03:** If no StatePacket is available (RGE failure, first tick, etc.), Logos Core uses the default topology.
- **INV-RGE-04:** Logos Core's topology decision is final and unappealable within a tick.
- **INV-RGE-05:** RGE does not know whether its recommendation was accepted. It receives the next TelemetrySnapshot regardless of the decision.

---

## 16. Downstream Subsystem Integration Matrix

This matrix defines how each downstream subsystem interacts with Logos Core. It is the Logos Core perspective; each subsystem's own design spec will define the reverse perspective.

| Subsystem | Reads From Logos Core | Writes To Logos Core | Channel | Frequency |
|---|---|---|---|---|
| I1 | Mediated UWM (SCP scope) | AA proposals | Protocol routing | Per-tick (when activated) |
| I2 | Mediated UWM (MTP scope) | AA proposals | Protocol routing | Per-tick (when activated) |
| I3 | Mediated UWM (ARP scope) | AA proposals | Protocol routing | Per-tick (when activated) |
| SCP | Task context via I1 pipeline | Processing results via I1 AAs | Agent integration layer | Per-tick (when I1 activated) |
| MTP | Task context via I2 pipeline | Processing results via I2 AAs | Agent integration layer | Per-tick (when I2 activated) |
| ARP | Task context via I3 pipeline | Processing results via I3 AAs | Agent integration layer | Per-tick (when I3 activated) |
| RGE | TelemetrySnapshot | StatePacket (advisory) | Nexus state projection | Every tick |
| CSP | Cognitive state queries | State updates (via Logos Core write) | Logos Core internal | Per-tick |
| SOP | Observability metrics | None | Telemetry emission | Per-tick |
| DRAC | Session reconstruction data | Compilation results | Session bootstrap | Per-session |
| EMP | Proof queries | Proof results | PXL gate interface | On-demand |
| MSPC | Compilation routing context | Compiled artifacts (via AA) | Protocol routing | Per-tick |

---

## 17. Governance Reconciliation Appendix

### 17.1 Purpose

The unification of Logos Agent and Logos Protocol into Logos Core is an architectural shift that postdates several governance artifacts. This appendix identifies every known governance artifact that assumes the decomposed (pre-unification) model and requires reconciliation.

### 17.2 Reconciliation is Downstream

This appendix flags discrepancies. It does not modify governance artifacts. Reconciliation is a separate work unit to be executed after this specification is approved.

### 17.3 Known Stale References

| Artifact / Location | Stale Assumption | Required Update |
|---|---|---|
| `_Governance/Alpha_Series/` phase definitions | May reference "Logos Agent" and "Logos Protocol" as separate phase participants | Consolidate to "Logos Core" |
| `_Governance/Contracts/` interface contracts | May define separate interface contracts for Logos Agent and Logos Protocol | Merge into unified Logos Core interface contract |
| `_Governance/Autonomy/A1_Non_Escalation/` | References agent authority scope in terms of the decomposed model | Update to reference unified authority model per §11 |
| `_Governance/Contracts/DRAC_*` registries | `Default_Bindings_Registry.json` and `Core_Interface_Registry.json` may reference Logos Agent as a discrete binding target | Update to reference Logos Core |
| Multi-Tick Invariants | May assume stable topology with Logos Agent as a fixed participant | Update to acknowledge ATM-driven topology per §3 |
| SMP Pipeline Governance | `mandatory_pass_lenses` may reference SCP specifically as epistemic verifier assuming static binding | Update to reference ATM-resolved primary agent |
| Runtime Subsystem Completeness Matrix | Lists Logos Agent and Logos Protocol as separate Tier 1 entries | Collapse to single Logos Core entry at Tier 0 |
| Prior session artifacts referencing "Octafolium" | Dated terminology | Replace with "RGE" per naming convention update |

### 17.4 Reconciliation Priority

The reconciliation should be executed in this order:

1. Runtime Subsystem Completeness Matrix update (unblocks downstream spec campaign)
2. Interface contracts (unblocks Tier 1 specs: CSP, SOP)
3. Alpha_Series phase definitions (governance consistency)
4. DRAC registries (unblocks DRAC design spec)
5. Remaining artifacts (lower urgency)

---

## 18. Implementation Status and Gap Analysis

### 18.1 Implemented (Confirmed in Repo)

| Component | Location | Status |
|---|---|---|
| Directory structure | `Logos_Core/` | Complete |
| Agent integration stubs | `LP_Core/Agent_Integration/I1,I2,I3` | Stub — pipeline_runner.py exists, logic TBD |
| Agent orchestration modules | `LP_Core/Agent_Orchestration/` | Partial — agent_orchestration.py, coordinator.py, dispatch.py exist |
| Identity generator | `LP_Core/Identity_Generator/` | Partial — schemas and attestation exist; runtime issuance TBD |
| Logos Protocol Nexus | `LP_Nexus/Logos_Protocol_Nexus.py` | Exists; integration status TBD |
| Phase-E Tick Engine | `LP_Tools/Recursion_Grounding/Phase_E_Tick_Engine.py` | Exists |
| Logos Agent runtime | `Logos_Agents/Logos_Agent/runtime.py` | Exists; authority model TBD |
| Agent resources | `Logos_Agent_Resources/` | Static reference library; complete for current scope |

### 18.2 Not Implemented (Spec'd Here, Build Required)

| Component | Spec Section | Priority | Dependency |
|---|---|---|---|
| Dual-phase tick lifecycle | §3 | P0 | None |
| Phase-G bootstrap sequencer | §4 | P0 | PXL gate |
| SMP creation and lifecycle manager | §5 | P0 | Tick lifecycle |
| UWM access control and write gates | §6 | P0 | Identity management |
| Protocol routing enforcement | §7 | P0 | Agent integration |
| PXL gate interface implementation | §8 | P0 | EMP subsystem |
| Telemetry production chain | §9 | P1 | RGE integration |
| Mutation authority enforcement | §11 | P0 | UWM access control |
| AA validation pipeline | §12 | P0 | SMP lifecycle |
| Governance mode resolver | §14 | P2 | Tick lifecycle |

### 18.3 Critical Path

The implementation critical path for Logos Core is:

```
PXL Gate Interface (§8)
  → Phase-G Bootstrap (§4)
    → Identity Management (§13)
      → UWM Access Control (§6)
        → SMP Lifecycle (§5)
          → Protocol Routing (§7)
            → Tick Lifecycle (§3)
              → AA Validation (§12)
                → Agent Orchestration (§12)
                  → Telemetry Production (§9)
```

---

## 19. Invariant Summary

All invariants defined in this specification, collected for reference.

### Tick Lifecycle (§3)
- INV-TL-01 through INV-TL-07

### Activation Sequencing (§4)
- INV-AS-01 through INV-AS-07

### SMP Pipeline (§5)
- INV-SMP-01 through INV-SMP-06

### UWM (§6)
- INV-UWM-01 through INV-UWM-06

### PXL Gate (§8)
- INV-PXL-01 through INV-PXL-05

### Telemetry (§9)
- INV-TEL-01 through INV-TEL-05

### Nexus (§10)
- INV-NX-01 through INV-NX-03

### Authority (§11)
- INV-AUTH-01 through INV-AUTH-04

### AA Governance (§12)
- INV-AA-01 through INV-AA-04

### Identity (§13)
- INV-ID-01 through INV-ID-05

### Governance Mode (§14)
- INV-GM-01 through INV-GM-04

### RGE Integration (§15)
- INV-RGE-01 through INV-RGE-05

**Total: 46 invariants**

---

## 20. Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-03-06 | Initial specification. Defines unified Logos Core as Tier 0 subsystem absorbing former Logos Agent and Logos Protocol scope. |

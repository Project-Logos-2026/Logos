# Cognitive State Protocol (CSP) Design Specification v1

## Governance Header

| Field | Value |
|---|---|
| Artifact Type | Design Specification |
| Authority | Canonical |
| Subsystem | Cognitive State Protocol (CSP) |
| Tier | 1 |
| Version | 1.0.0 |
| Status | Active |
| Division | Operations |
| Depends On | Logos Core (Tier 0) |
| Depended On By | I1 (via SCP axis), I2, I3 (mediated read access) |
| RGE Integration | RGE_Design_Specification_v3.md §8.4 |
| Upstream Spec | Logos_Core_Design_Specification_v1.md |
| Mutability | Controlled (version-gated amendments only) |

---

## 1. Purpose and Scope

### 1.1 Subsystem Identity

CSP is the cognitive state substrate of the LOGOS runtime. It manages memory, world modeling, and belief state on the operations side of the domain boundary. It provides the persistent cognitive context that agents query for memory retrieval and context grounding.

### 1.2 Architectural Position

CSP resides in the operations domain (`RUNTIME_OPPERATIONS_CORE`). It cannot command execution, invoke ticks, or mutate execution-side state. It receives state snapshots from the execution domain via the Runtime Bridge and maintains the operations-side representation of cognitive state.

Within the RGE geometry, CSP occupies a protocol position paired with SCP on the CSP-SCP axis. This axis enables deep abstract recursion over memory to find existing axioms or memories that structurally ground current analysis. CSP provides the memory substrate; SCP provides the synthetic cognition machinery that recurses over it.

### 1.3 Domain Boundary Significance

CSP is operations-side. Logos Core's UWM (§6 of Logos Core spec) is execution-side. These are not the same thing despite both managing state:

- **Logos Core UWM:** Execution-side, tick-scoped, write-gated by Logos Core, agents interact with it via mediated access during cognitive processing.
- **CSP State Surface:** Operations-side, session-scoped, synchronized from execution via Runtime Bridge snapshots, provides persistent memory and world model context.

The relationship is: Logos Core UWM is the authoritative tick-level working memory. CSP maintains the broader cognitive context (long-term memory, world model, belief state) that informs but does not control tick-level processing. Execution-side agents access CSP-managed state through Logos Core mediation, not by direct CSP import.

### 1.4 Scope of This Specification

This specification defines:

- Memory subsystem architecture
- World modeling framework
- Belief state management
- CSP Nexus participation model
- State synchronization contract (Runtime Bridge interface)
- Agent query interface (mediated through Logos Core)
- RGE integration surface (CSP-SCP axis context)
- Governance boundaries

### 1.5 What This Specification Does Not Cover

- Execution-side UWM access control (covered by Logos Core spec §6)
- SCP internal processing logic (covered by SCP design spec, Tier 3)
- Runtime Bridge internal transport (infrastructure, not protocol-specific)
- DRAC session reconstruction (covered by DRAC design spec, Tier 2)

---

## 2. Canonical Directory Structure

### 2.1 Root Location

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/Cognitive_State_Protocol/
```

### 2.2 Internal Layout

```
Cognitive_State_Protocol/
├── CSP_Core/
│   ├── __init__.py
│   ├── Memory/
│   │   ├── __init__.py
│   │   ├── Logos_Memory_Nexus.py
│   │   ├── Memory_Access_Point.py
│   │   ├── Memory_Recall_Integration.py
│   │   └── Memory_State_Persistence.py
│   └── Unified_Working_Memory/
│       ├── __init__.py
│       └── World_Modeling/
│           ├── __init__.py
│           ├── PXL_World_Model.py
│           ├── commitment_ledger.py
│           └── world_model.py
├── CSP_Documentation/
│   ├── __init__.py
│   ├── GOVERNANCE_SCOPE.md
│   ├── MANIFEST.md
│   ├── METADATA.json
│   ├── ORDER_OF_OPERATIONS.md
│   ├── RUNTIME_ROLE.md
│   └── STACK_POSITION.md
└── CSP_Nexus/
    └── CSP_Nexus.py
```

### 2.3 Naming Note

The `Unified_Working_Memory` directory name within CSP predates the Logos Core unification. This is CSP's operations-side world modeling layer, not the execution-side UWM governed by Logos Core. A future normalization pass may rename this directory to avoid confusion. Until then, the distinction defined in §1.3 is authoritative.

---

## 3. Memory Subsystem

### 3.1 Purpose

The Memory subsystem provides structured access to persistent cognitive context: episodic memory, semantic memory, and retrieval mechanisms. It is the substrate that agents query when they need historical context, prior reasoning results, or established axioms.

### 3.2 Module Responsibilities

| Module | Responsibility |
|---|---|
| `Logos_Memory_Nexus.py` | Central coordination point for memory operations. Routes memory queries, manages memory lifecycle, integrates with CSP Nexus tick loop. |
| `Memory_Access_Point.py` | Public interface for memory queries. All external access to CSP memory routes through this module. Enforces access control and query validation. |
| `Memory_Recall_Integration.py` | Retrieval logic for memory queries. Implements recall strategies (exact match, similarity, temporal proximity). Returns structured recall results. |
| `Memory_State_Persistence.py` | Persistence layer for memory state across session boundaries. Manages serialization, deserialization, and integrity verification of persisted memory. |

### 3.3 Memory Access Model

| Actor | Access | Channel |
|---|---|---|
| Logos Core | Full read | Runtime Bridge → CSP_Nexus → Memory_Access_Point |
| I1 (via Logos Core) | Scoped read (SCP-relevant memory) | Logos Core mediation → Runtime Bridge → Memory_Access_Point |
| I2 (via Logos Core) | Scoped read (MTP-relevant memory) | Logos Core mediation → Runtime Bridge → Memory_Access_Point |
| I3 (via Logos Core) | Scoped read (ARP-relevant memory) | Logos Core mediation → Runtime Bridge → Memory_Access_Point |
| SOP | Observability only | SOP metrics channel |
| DRAC | Session reconstruction data | DRAC reconstruction interface |
| All others | None | No access |

### 3.4 Memory Invariants

- **INV-MEM-01:** All memory access is mediated. No execution-side entity imports CSP modules directly.
- **INV-MEM-02:** Memory writes are append-only for episodic content. Existing memories are never modified.
- **INV-MEM-03:** Memory recall results are read-only snapshots. The caller cannot modify CSP state through a recall result.
- **INV-MEM-04:** Memory queries that fail return empty results, not errors. Fail-silent on retrieval, fail-closed on corruption.
- **INV-MEM-05:** Memory_State_Persistence verifies integrity on load. Corrupted persistence data is rejected, not repaired.

---

## 4. World Modeling Framework

### 4.1 Purpose

The World Modeling subsystem maintains a structured representation of the system's understanding of its operational context. This includes the PXL-grounded world model, commitment tracking, and belief-state coherence.

### 4.2 Module Responsibilities

| Module | Responsibility |
|---|---|
| `world_model.py` | Core world model data structure. Maintains the current state of world knowledge as a structured, queryable representation. |
| `PXL_World_Model.py` | PXL-grounded subset of the world model. Contains only world-state propositions that have been formally verified through the PXL proof system. Provides the formally trusted knowledge base. |
| `commitment_ledger.py` | Tracks active commitments — propositions, goals, or obligations the system has committed to. Commitments are append-only and cannot be silently retracted. |

### 4.3 World Model Layers

The world model operates in two layers:

**Verified Layer (PXL_World_Model):** Contains only propositions with corresponding PXL proof status of VERIFIED_PXL or higher. This layer is the formally trusted knowledge base. Agents may rely on its contents without additional verification.

**Working Layer (world_model):** Contains all world-state propositions including unverified, provisional, and verified. This layer is the complete picture. Agents querying this layer must treat unverified propositions accordingly.

### 4.4 World Model Invariants

- **INV-WM-01:** The verified layer is a strict subset of the working layer. Every proposition in PXL_World_Model exists in world_model.
- **INV-WM-02:** Propositions may only be promoted from working to verified layer when EMP confirms PXL proof status ≥ VERIFIED_PXL.
- **INV-WM-03:** Propositions are never demoted from verified to working. If a proof is invalidated, the proposition is removed from the verified layer entirely.
- **INV-WM-04:** Commitment ledger entries are append-only. Retraction requires a new explicit retraction entry, not deletion of the original.
- **INV-WM-05:** World model state is session-scoped. Cross-session persistence is handled by Memory_State_Persistence, not by the world model directly.

---

## 5. Belief State Management

### 5.1 Purpose

Belief state tracks the system's epistemic posture: what it believes, with what confidence, and on what basis. This is distinct from the world model (which tracks propositions about the world) and from memory (which tracks historical context).

### 5.2 Belief State Structure

| Component | Description |
|---|---|
| Active Beliefs | Propositions currently held as true, with associated evidence chains |
| Suspended Beliefs | Propositions held as possible but not confirmed, pending further evidence |
| Retracted Beliefs | Propositions previously held but explicitly retracted, with retraction justification |
| Confidence Scores | Bounded [0, 1] confidence for each active belief, derived from evidence strength |

### 5.3 Belief State Invariants

- **INV-BS-01:** Every active belief has a non-empty evidence chain. A belief without evidence is invalid.
- **INV-BS-02:** Confidence scores are monotonically derived from evidence. Manual confidence overrides are prohibited.
- **INV-BS-03:** Belief retraction produces an explicit retraction record. Beliefs are never silently removed.
- **INV-BS-04:** Belief state queries return the current state as a read-only snapshot. Mutations to belief state occur only through the CSP internal update pipeline.
- **INV-BS-05:** Belief state is synchronized to the execution domain via Runtime Bridge at tick boundaries. The execution domain sees the belief state as of the most recent synchronization.

---

## 6. CSP Nexus Participation Model

### 6.1 Participant Identity

CSP participates in the operations-side tick loop via `CSP_Nexus.py`. CSP_Nexus implements the StandardNexus pattern: registration, deterministic tick ordering, structural constraint enforcement, and MRE gating.

### 6.2 Tick Responsibilities

Each CSP Nexus tick:

1. Receive execution-side state snapshot from Runtime Bridge
2. Update memory indices from snapshot deltas
3. Refresh world model with new propositions from accepted AAs
4. Update belief state based on new evidence
5. Process pending memory queries from execution-side mediation queue
6. Emit CSP telemetry to SOP observability channel
7. Project current cognitive state summary for bridge consumption

### 6.3 Nexus Invariants

- **INV-CN-01:** CSP Nexus tick execution is operations-side only. It never invokes execution-side methods.
- **INV-CN-02:** CSP Nexus processes one snapshot per tick. Multiple snapshots in the queue are processed in order without skipping.
- **INV-CN-03:** If no snapshot is available, CSP Nexus tick completes with no state changes (idempotent no-op).
- **INV-CN-04:** CSP Nexus tick failures do not propagate to execution. A failed CSP tick means the execution domain operates with stale cognitive context.

---

## 7. State Synchronization Contract

### 7.1 Direction

```
Execution Domain (Logos Core) ──→ Runtime Bridge ──→ CSP (Operations)
```

This flow is unidirectional for state data. CSP receives snapshots; it does not push state to execution.

### 7.2 Query Mediation (Reverse Direction)

```
Agent (Execution) → Logos Core → Runtime Bridge → CSP Memory_Access_Point → result → Runtime Bridge → Logos Core → Agent
```

Query results flow back through the same mediated path. The agent never holds a reference to CSP internals.

### 7.3 Snapshot Schema

| Field | Type | Description |
|---|---|---|
| `tick_number` | int | Tick that produced this snapshot |
| `session_id` | UUID | Session identifier |
| `accepted_aas` | List[AA_Summary] | AAs accepted in this tick (for world model update) |
| `smp_state_deltas` | List[SMP_Delta] | SMP state changes in this tick |
| `telemetry_summary` | TelemetrySummary | Condensed telemetry for CSP indexing |
| `timestamp` | ISO-8601 | Snapshot creation time |

### 7.4 Synchronization Invariants

- **INV-SYNC-01:** Snapshots are delivered in tick order. Out-of-order delivery is a bridge violation.
- **INV-SYNC-02:** Snapshots are immutable. CSP cannot modify a snapshot after receipt.
- **INV-SYNC-03:** Missing snapshots are not retried. CSP operates with the latest available state.
- **INV-SYNC-04:** The synchronization channel carries no authority. Snapshot receipt does not authorize CSP to perform any action on the execution domain.

---

## 8. RGE Integration Surface

### 8.1 CSP-SCP Axis

In the RGE geometry, CSP and SCP form a paired axis. This pairing reflects a functional relationship: SCP performs synthetic cognition (recursive analysis, pattern extraction), and CSP provides the memory and world-model substrate that SCP recurses over.

### 8.2 RGE Relevance

When RGE evaluates topology configurations, the CSP-SCP axis represents the system's capacity for memory-grounded analysis. A topology that prioritizes I1 (SCP-bound) as primary simultaneously increases the relevance of CSP as the memory provider for that processing pass.

CSP does not directly interact with RGE. The relevance is structural: RGE's topology decisions affect how heavily CSP's memory surface is utilized in a given tick.

### 8.3 Telemetry Contribution

CSP does not produce telemetry that feeds RGE scoring directly. The telemetry production chain is Logos Core's responsibility (Logos Core spec §9). However, CSP-derived metrics (memory load, recall latency, world model size) may be included in future telemetry extensions. This is a deferred integration point.

---

## 9. Governance Boundaries

### 9.1 CSP May

- Maintain operations-side cognitive state (memory, world model, belief state)
- Respond to mediated memory queries from execution-side agents
- Update internal state from execution-side snapshots received via Runtime Bridge
- Emit telemetry to SOP observability channel
- Participate in DRAC session reconstruction by providing cognitive state for serialization

### 9.2 CSP May Not

- Write to execution-side UWM (Logos Core spec INV-UWM-01)
- Command or invoke execution-side ticks
- Directly communicate with agents (all communication is Logos Core-mediated)
- Modify execution-side SMP content
- Override or influence Logos Core authority decisions
- Access protocol internals (SCP, MTP, ARP) directly

### 9.3 Governance Invariants

- **INV-GOV-01:** CSP is non-authoritative. It provides state; it does not make decisions.
- **INV-GOV-02:** CSP's outputs are advisory context, not binding instructions.
- **INV-GOV-03:** CSP failure degrades cognitive context quality but does not halt execution. The system continues with stale context.
- **INV-GOV-04:** CSP operates within the operations domain boundary. Cross-domain imports are prohibited.

---

## 10. Implementation Status and Gap Analysis

### 10.1 Implemented (Confirmed in Repo)

| Component | Location | Status |
|---|---|---|
| Directory structure | `Cognitive_State_Protocol/` | Complete |
| Memory subsystem | `CSP_Core/Memory/` | 4 modules present; implementation depth TBD |
| World modeling | `CSP_Core/Unified_Working_Memory/World_Modeling/` | 3 modules present including PXL_World_Model |
| CSP Nexus | `CSP_Nexus/CSP_Nexus.py` | Present; Nexus integration status TBD |
| Documentation | `CSP_Documentation/` | 6 documents present including GOVERNANCE_SCOPE and RUNTIME_ROLE |

### 10.2 Not Implemented (Spec'd Here, Build Required)

| Component | Spec Section | Priority | Dependency |
|---|---|---|---|
| Belief state management | §5 | P1 | Memory subsystem |
| State synchronization from Runtime Bridge | §7 | P0 | Runtime Bridge, Logos Core telemetry |
| Query mediation interface | §7.2 | P0 | Logos Core protocol routing |
| Snapshot processing pipeline | §6.2 | P1 | State synchronization |
| UWM naming reconciliation | §2.3 | P2 | None (documentation task) |

### 10.3 Critical Path

```
State Synchronization Contract (§7)
  → Snapshot Processing Pipeline (§6.2)
    → Memory Update from Snapshots (§3)
      → World Model Refresh (§4)
        → Belief State Update (§5)
          → Query Mediation Interface (§7.2)
```

---

## 11. Invariant Summary

| Domain | Invariants | Count |
|---|---|---|
| Memory (§3) | INV-MEM-01 through INV-MEM-05 | 5 |
| World Model (§4) | INV-WM-01 through INV-WM-05 | 5 |
| Belief State (§5) | INV-BS-01 through INV-BS-05 | 5 |
| CSP Nexus (§6) | INV-CN-01 through INV-CN-04 | 4 |
| Synchronization (§7) | INV-SYNC-01 through INV-SYNC-04 | 4 |
| Governance (§9) | INV-GOV-01 through INV-GOV-04 | 4 |

**Total: 27 invariants**

---

## 12. Version History

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-03-06 | Initial specification. Defines CSP as Tier 1 operations-side cognitive state substrate with explicit domain boundary separation from execution-side UWM. |

# LOGOS Epistemic Artifact (EA) System — Design Specification

**Version**: 1.0.0
**Status**: DRAFT
**Date**: 2026-03-05
**Authority**: LOGOS V1 Architecture
**Scope**: Runtime EA lifecycle, storage, governance, and protocol integration
**Spec Type**: Non-executable design artifact

---

## 1. Overview

The Epistemic Artifact (EA) system defines the formal abstraction governing how structured epistemic objects are created, modified, classified, persisted, and consumed across the LOGOS runtime.

An EA is the composite of a Structured Meaning Packet (SMP) and its associated Append Artifact (AA) Catalog:

```
EA = SMP + AA Catalog
```

The SMP carries the structured semantic content. The AA Catalog carries the append-only epistemic metadata that accumulates as the EA moves through the cognitive processing pipeline. Together they constitute the atomic epistemic unit of the LOGOS runtime — the indivisible container for all meaning that enters, flows through, and exits the system.

The EA system does not introduce new runtime surfaces. It formalizes the relationship between existing components (SMP_Schema, SMP_Store, AA_Catalog, Classification_Tracker, UWM_Access_Control, Promotion_Evaluator, Canonical_SMP_Producer, CSP_Canonical_Store) under a single conceptual and governance model.

No protocol, agent, or subsystem may interact with epistemic content outside the EA abstraction. All epistemic reads and writes transit through the EA system's governed interfaces.

---

## 2. Terminology

**EA (Epistemic Artifact)**: The composite runtime object consisting of one SMP and its associated AA Catalog. The fundamental unit of epistemic content in LOGOS.

**SMP (Structured Meaning Packet)**: The immutable-after-sealing data structure carrying structured semantic content through the runtime. Defined by SMP_Schema.py.

**AA (Append Artifact)**: An atomic, append-only metadata record attached to an SMP. Each AA records a discrete epistemic contribution from a specific protocol or agent action.

**AA Catalog**: The ordered, append-only collection of AAs associated with a single SMP. Managed by the AA_Catalog module and stored within the SMP's `append_artifacts` field.

**Classification State**: The epistemic maturity of an EA, drawn from the monotonic ladder: `rejected`, `conditional`, `provisional`, `canonical`.

**Canonical SMP (C-SMP)**: An EA that has been promoted to the `canonical` classification state by the CSP Promotion pipeline and is stored in the CSP Canonical Store. Identified by the `C-SMP:` prefix on its identity field.

**Sealing**: The governance event after which an SMP's core fields (identity, type, provenance, temporal_context, payload) become immutable. Sealing occurs at SMP creation time. Post-sealing modification is restricted to AA attachment and classification promotion.

**UWM (Unified Working Memory)**: The session-scoped, in-memory storage layer for all active EAs. The authoritative epistemic memory domain of the runtime.

**Promotion**: The governed transition of an EA from `provisional` to `canonical` classification, producing a C-SMP and persisting it to the CSP Canonical Store.

**Content Hash**: SHA-256 hash computed over the SMP's content fields at creation time. Used for integrity verification. Recomputed at canonicalization to cover the full AA chain.

---

## 3. EA Conceptual Model

### 3.1 Composition

An EA is not a separate data structure stored alongside or instead of an SMP. An EA is the SMP viewed together with its AA Catalog as a single governed epistemic unit. The SMP_Schema dataclass and SMP_Store remain the authoritative storage representations. The EA abstraction is a governance and lifecycle concept, not a new class or table.

```
EA
├── SMP (sealed core)
│   ├── identity          (string, immutable, unique)
│   ├── type              (string, immutable, declarative category)
│   ├── provenance        (dict, immutable, structured envelope)
│   ├── temporal_context  (dict, immutable, time metadata)
│   ├── status_confidence (dict, mutable via classification only)
│   ├── classification    (enum, mutable via monotonic promotion only)
│   ├── privation         (dict, immutable, redaction/quarantine flags)
│   ├── payload           (dict, immutable, bounded inert content)
│   └── content_hash      (string, computed at creation, recomputed at canonicalization)
│
└── AA Catalog (append-only)
    ├── AA[0]  (first attached artifact)
    ├── AA[1]  (second attached artifact)
    └── AA[n]  (nth attached artifact, n monotonically increasing)
```

### 3.2 Identity Model

Every EA is uniquely identified by its SMP identity field, which is assigned at creation and is immutable thereafter. The identity follows the format `SMP:<session_id>:<sequence>` for working SMPs and `C-SMP:<session_id>:<sequence>` for canonical SMPs. No two EAs within a session or across the canonical store may share an identity.

#### 3.2.1 Forward Compatibility Guidance (V1.1+)

The V1 identity format (`SMP:<session_id>:<sequence>`, `C-SMP:<session_id>:<sequence>`) is accepted and sufficient for V1, which operates under a single-session, single-agent-cluster assumption where session_id uniqueness is guaranteed by the RuntimeLoop.

For V1.1+ contexts involving multi-session persistence, distributed agent clusters, or cross-session canonical store federation, the recommended future-safe identity format is:

```
SMP:<agent_id>:<session_id>:<sequence>
C-SMP:<agent_id>:<session_id>:<sequence>
```

Where `agent_id` identifies the originating Logos Agent instance. This eliminates identity collision across independent sessions or agent deployments sharing a canonical store.

This is forward compatibility guidance only. It is NOT a V1 requirement. V1 implementations MUST use the two-part format. Migration to the three-part format, if adopted, would be a V1.1 schema revision governed by the standard phase lock process.

### 3.3 Immutability Boundaries

The EA model enforces two distinct immutability regimes:

**Hard immutability** (post-sealing, no exceptions): identity, type, provenance, temporal_context, privation, payload. These fields are set at creation and never modified.

**Governed mutability** (append-only or monotonic-only): classification (monotonic ladder transitions only), append_artifacts (append-only AA attachment), content_hash (recomputed only at canonicalization).

No field on a sealed SMP may be deleted. No AA may be removed from the catalog. No classification may move backward (except to `rejected`, which is terminal).

### 3.4 Inertness Constraint

EAs are inert. They carry no executable content, no scheduling directives, no continuation tokens, no embedded code, and no template references that would cause runtime behavior. An EA is a passive data structure that is acted upon by protocols and agents. It never acts on its own behalf.

---

## 4. SMP Architecture

### 4.1 Schema Definition

The SMP schema is defined in `SMP_Schema.py` at:
```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/
  Cognitive_State_Protocol/CSP_Core/Unified_Working_Memory/SMP_Schema.py
```

The SMP is implemented as a Python dataclass with the following canonical fields:

| Field | Type | Mutability | Description |
|-------|------|------------|-------------|
| `identity` | `str` | Immutable | Unique identifier, format `SMP:<session>:<seq>` |
| `type` | `str` | Immutable | Declarative category (observation, plan_fragment, audit_event) |
| `provenance` | `dict` | Immutable | Structured provenance envelope (creator, source, chain_of_custody) |
| `temporal_context` | `dict` | Immutable | Time metadata (created_at, session_tick) |
| `status_confidence` | `dict` | Governed | Status and confidence bounds |
| `classification` | `str` | Monotonic | One of: rejected, conditional, provisional, canonical |
| `privation` | `dict` | Immutable | Redaction and quarantine flags |
| `append_artifacts` | `list` | Append-only | Ordered AA catalog |
| `payload` | `dict` | Immutable | Structured, bounded, inert content |
| `content_hash` | `str` | Recomputed at canonicalization | SHA-256 of content fields |

### 4.2 SMP Prohibitions

The following content is prohibited within any SMP field. Violation triggers immediate rejection (fail-closed):

- Executable code or references to executable modules
- Scheduling or continuation directives
- Self-referential autonomy markers
- Embedded templates or template identifiers
- Unbounded or streaming payloads
- References to mutable external state

### 4.3 SMP Creation

SMPs are created exclusively through `SMPStore.create_smp()`. The creation process:

1. Validates all required fields are present and well-typed.
2. Validates payload conforms to inertness constraints.
3. Validates provenance envelope is complete.
4. Assigns identity using session-scoped sequence.
5. Sets initial classification to `conditional`.
6. Computes SHA-256 content_hash over (identity + type + provenance + payload).
7. Initializes empty `append_artifacts` list.
8. Seals the SMP. Core fields are immutable from this point.
9. Stores the SMP in the UWM session-scoped store.

Creation requires a valid `WriteAuthorization` traceable to the Logos Agent. Sub-agents cannot directly invoke `create_smp()`.

### 4.4 SMP Retrieval

SMPs are retrieved through `UWMReadAPI`, which enforces role-based access control. The access control model:

- **Logos Agent**: Full read access to all SMPs and AAs in the session.
- **I1 (SCP)**: Read access to SMPs routed to SCP for analysis. Cannot read SMPs assigned to other agents.
- **I2 (MTP)**: Read access to SMPs routed for rendering. Cannot read working SMPs pre-routing.
- **I3 (ARP)**: Read access to SMPs routed for reasoning. Cannot read SMPs assigned to other agents.
- **Unrecognized roles**: No access (deny-by-default, returns None).

---

## 5. AA Catalog Architecture

### 5.1 Append Artifact Schema

An AA is implemented as a Python dataclass (`AppendArtifact` in SMP_Schema.py) with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `aa_id` | `str` | Unique identifier within the SMP's AA catalog |
| `aa_type` | `str` | Artifact type (analysis_result, reasoning_output, rendering_directive, promotion_record, governance_annotation) |
| `producer` | `str` | Identifier of the producing agent or protocol |
| `produced_at` | `str` | ISO-8601 timestamp of creation |
| `content` | `dict` | Structured, inert artifact content |
| `content_hash` | `str` | SHA-256 hash of the AA content |

### 5.2 AA Types

The EA system defines a closed set of AA types:

**`analysis_result`** (I1AA): Produced by I1 via the SCP Orchestrator. Contains structured analysis output from MVS/BDN processing. This is the initial epistemic contribution that begins SMP enrichment.

**`reasoning_output`** (I3AA): Produced by I3 via the ARP pipeline. Contains formal reasoning results, proof fragments, constraint evaluations.

**`rendering_directive`** (I2AA): Produced by I2 via MTP. Contains natural language rendering instructions and rendered output.

**`promotion_record`**: Produced by the CSP Promotion pipeline. Records the evaluation result and transition rationale when classification changes.

**`governance_annotation`**: Produced by governance enforcement modules. Records constraint violations, boundary enforcement actions, or audit markers.

No AA type outside this set may be introduced without a governance schema revision.

### 5.3 AA Attachment

AAs are attached to SMPs exclusively through `SMPStore.append_aa()`. The attachment process:

1. Validates the target SMP exists and is not in `canonical` or `rejected` state.
2. Validates the AA conforms to the AppendArtifact schema.
3. Calls `validate_agent_write_boundary()` to enforce that the write originates from an authorized context.
4. Computes AA content_hash.
5. Appends the AA to the SMP's `append_artifacts` list.
6. Records the AA hash in the SMP's aa_hashes integrity chain.

Canonical SMPs are immutable — no AA may be attached after canonicalization. Rejected SMPs are terminal — no AA may be attached after rejection.

### 5.4 AA Catalog Integrity

The AA Catalog maintains an ordered integrity structure over all attached AAs. Two levels of integrity are defined:

**Minimum V1 (current implementation)**: A flat list of independent AA content hashes. Each AA's content_hash is computed as `SHA-256(canonical_serialization(AA_content))` and appended to the SMP's `aa_hashes` list at attachment time. The canonical serialization is the deterministic JSON serialization of the AA's `content` field with sorted keys and no whitespace. This provides:

- Ordering proof: the position of a hash in the list corresponds to AA attachment order.
- Per-AA integrity: any modification to an individual AA's content produces a hash mismatch.
- Completeness check: `len(aa_hashes) == len(append_artifacts)` must hold at all times.

**Target integrity (governance clarification for V1 hardening or V1.1)**: A true chained commitment hash where each element commits to all prior elements, preserving both content integrity and ordering in a single verifiable chain:

```
H_0 = SHA-256(canonical_serialization(AA_0.content))
H_n = SHA-256(H_{n-1} || canonical_serialization(AA_n.content))
```

Where `||` denotes byte concatenation. Under this model, the final hash `H_n` commits to the exact content and order of all AAs in the catalog. Verification requires replaying the chain from `H_0`. Any insertion, deletion, reordering, or content modification at any position invalidates all subsequent hashes.

The transition from flat list to chained commitment does not require new modules or classes. It requires a change to the hash computation within `SMPStore.append_aa()` and a corresponding update to the C-SMP hash recomputation in `CanonicalSMPProducer.produce()`. This transition is classified as a governance-driven hardening change, not a refactor.

### 5.5 AA Catalog Integration

The AA_Catalog module (`AA_Catalog.py`) provides indexed lookup and query capabilities over the AA collection. In the current implementation, SMPStore manages AAs directly via its internal `_aas` dictionary. The EA specification requires that AA_Catalog be integrated as the authoritative index over AA collections, providing:

- Lookup by aa_id.
- Lookup by aa_type (all analysis_results, all reasoning_outputs, etc.).
- Lookup by producer (all AAs from I1, all AAs from I3, etc.).
- Ordered iteration in attachment sequence.

This integration is documented as REM-09 in the V1 compliance audit and is required for EA system completeness.

---

## 6. EA Lifecycle

The EA lifecycle describes the governed sequence of states an EA transits from creation to terminal state. Every EA follows this lifecycle without exception.

### 6.1 Lifecycle Phases

```
CREATION → ENRICHMENT → EVALUATION → PROMOTION/REJECTION → TERMINAL
```

**Phase 1 — Creation**: The Logos Agent creates an SMP via SMPStore.create_smp() in response to a task input or internal routing decision. The SMP is sealed with classification `conditional`. The EA now exists in UWM.

**Phase 2 — Enrichment**: The SMP is routed through the agent pipeline via the SMP routing state machine in the Logos Agent. Each agent attaches AAs as it processes the SMP:
- I1 (SCP): Attaches `analysis_result` AAs via SCPOrchestrator.analyze().
- I3 (ARP): Attaches `reasoning_output` AAs via the ARP pipeline.
- I2 (MTP): Attaches `rendering_directive` AAs via MTP processing.
Each AA attachment is governed by write boundary validation.

**Phase 3 — Evaluation**: The PromotionEvaluator examines the enriched EA (SMP + all attached AAs) and determines whether it qualifies for promotion from `provisional` to `canonical`. Evaluation criteria include AA completeness, confidence thresholds, and governance compliance.

**Phase 4 — Promotion or Rejection**: Based on the evaluation result:
- **Promotion**: The CanonicalSMPProducer creates a C-SMP with the `C-SMP:` prefix, canonical classification, updated chain_of_custody, and recomputed content_hash. The C-SMP is stored in CSPCanonicalStore.
- **Rejection**: The classification is set to `rejected`. A `governance_annotation` AA is attached recording the rejection rationale. The EA becomes terminal.

**Phase 5 — Terminal**: The EA is in its final state. Canonical EAs are available in the CSP Canonical Store for downstream consumption (DRAC, World Modeling). Rejected EAs remain in UWM for audit purposes but are not promoted or further enriched.

### 6.2 Classification State Machine

```
                    ┌───────────┐
        creation    │conditional│
                    └─────┬─────┘
                          │ (enrichment begins)
                          ▼
                    ┌───────────┐
                    │provisional│
                    └─────┬─────┘
                         / \
            (promote)   /   \   (reject)
                       ▼     ▼
              ┌──────────┐ ┌────────┐
              │ canonical │ │rejected│
              └──────────┘ └────────┘
              (terminal)   (terminal)
```

**Transition rules** (enforced by Classification_Tracker):
- `conditional` → `provisional`: Allowed when at least one AA has been attached.
- `provisional` → `canonical`: Allowed only via PromotionEvaluator approval.
- `provisional` → `rejected`: Allowed at any point during evaluation.
- `conditional` → `rejected`: Allowed (e.g., boundary validation failure).
- `canonical` → (anything): Forbidden. Canonical is terminal.
- `rejected` → (anything): Forbidden. Rejected is terminal.
- All backward transitions (canonical → provisional, provisional → conditional): Forbidden.

The monotonic ladder invariant is enforced by `Classification_Tracker.validate_transition()`. Any attempt to violate the ladder raises immediately (fail-closed).

### 6.3 Tick-Aligned Processing

EA lifecycle progression is aligned with the RuntimeLoop tick cycle. Each tick may advance one or more EAs through their lifecycle phases:

- **Tick N**: SMP created, routed to I1. I1 attaches analysis_result AA.
- **Tick N+1**: SMP routed to I3. I3 attaches reasoning_output AA.
- **Tick N+2**: SMP routed to I2. I2 attaches rendering_directive AA.
- **Tick N+3**: Promotion evaluation. SMP promoted or rejected.

The exact tick mapping depends on the SMP routing state machine in the Logos Agent. The maximum tick budget per task is 50 (enforced by RuntimeLoop).

---

## 7. Agent Interaction Model

### 7.1 Authority Hierarchy

The LOGOS agent hierarchy enforces strict write authority over EAs:

**Logos Agent (Runtime Sovereign)**: The only entity authorized to write to UWM. All SMP creation, AA attachment, and classification updates are mediated through the Logos Agent. The Logos Agent operates the SMP routing state machine that determines which sub-agent processes an EA at each tick.

**I1 (SCP Agent)**: Proposes analysis_result AAs. Cannot write to UWM directly. Proposals are submitted to the Logos Agent, which validates and persists them.

**I2 (MTP Agent)**: Proposes rendering_directive AAs. Same write restriction as I1.

**I3 (ARP Agent)**: Proposes reasoning_output AAs. Same write restriction as I1.

### 7.2 SMP Routing State Machine

The Logos Agent maintains an `SMPRoutingState` for each active SMP, tracking which processing stages have been completed:

```
SMPRoutingState:
  smp_id: str
  current_stage: enum (INTAKE, SCP_ANALYSIS, ARP_REASONING, MTP_RENDERING, EVALUATION, RESOLVED)
  stages_completed: list[str]
  tick_entered: int
  tick_budget_remaining: int
```

The routing state machine governs which agent receives the SMP at each tick. The Logos Agent inspects the routing state, dispatches the SMP to the appropriate sub-agent, receives the proposed AA, validates it, and persists it to UWM.

### 7.3 Agent-EA Interactions by Protocol

| Agent | Protocol | AA Type Produced | EA Fields Read | EA Fields Written |
|-------|----------|------------------|----------------|-------------------|
| Logos | CSP (orchestration) | promotion_record, governance_annotation | All fields | classification, append_artifacts |
| I1 | SCP | analysis_result | identity, type, payload, provenance | append_artifacts (via Logos) |
| I2 | MTP | rendering_directive | identity, payload, append_artifacts (prior AAs) | append_artifacts (via Logos) |
| I3 | ARP | reasoning_output | identity, payload, append_artifacts (prior AAs) | append_artifacts (via Logos) |

### 7.4 Sub-Agent Proposal Protocol

When a sub-agent produces an AA, the interaction follows this governed sequence:

1. Sub-agent receives SMP reference via `_on_tick()` dispatch.
2. Sub-agent reads permitted SMP fields via UWMReadAPI.
3. Sub-agent performs protocol-specific processing (SCP analysis, ARP reasoning, MTP rendering).
4. Sub-agent constructs an AppendArtifact with its results.
5. Sub-agent returns the proposed AA to the Logos Agent via the tick result.
6. Logos Agent validates the AA (schema, write boundary, inertness).
7. Logos Agent calls `SMPStore.append_aa()` to persist the AA.
8. Logos Agent advances the SMP routing state.

At no point does a sub-agent call SMPStore directly. The Logos Agent is the sole write path.

---

## 8. Governance Invariants

The EA system enforces the following invariants unconditionally. Violation of any invariant triggers an immediate halt or rejection (fail-closed). No invariant may be relaxed by configuration, feature flag, or runtime condition.

### 8.1 Structural Invariants

**EA-INV-01 — SMP Immutability After Sealing**: Once an SMP is created and sealed, its core fields (identity, type, provenance, temporal_context, privation, payload) are immutable. No runtime path may modify these fields.

**EA-INV-02 — AA Append-Only**: AAs may only be appended to the AA Catalog. No AA may be modified, reordered, or removed after attachment. The AA Catalog is a monotonically growing, ordered collection.

**EA-INV-03 — Monotonic Classification Ladder**: Classification transitions must follow the monotonic ladder. No backward transitions are permitted except to `rejected` (which is terminal). Enforced by Classification_Tracker.validate_transition().

**EA-INV-04 — Canonical Immutability**: Once an EA reaches `canonical` classification, no further modifications of any kind are permitted — no AA attachment, no classification change, no field mutation.

**EA-INV-05 — Rejected Terminal**: Once an EA reaches `rejected` classification, no further enrichment or promotion is permitted. The EA remains in UWM for audit but is inert.

### 8.2 Authority Invariants

**EA-INV-06 — Logos Agent Write Exclusivity**: Only the Logos Agent may invoke SMPStore.create_smp(), SMPStore.append_aa(), and SMPStore.promote_classification(). Sub-agents propose; the Logos Agent persists.

**EA-INV-07 — Deny-By-Default Read Access**: UWMReadAPI returns None for any role not explicitly granted access. Unrecognized roles receive no data.

**EA-INV-08 — Write Boundary Enforcement**: Every AA attachment invokes validate_agent_write_boundary() before persistence. Invalid write attempts are rejected immediately.

### 8.3 Integrity Invariants

**EA-INV-09 — Content Hash Integrity**: Every SMP has a SHA-256 content_hash computed at creation. Every AA has a content_hash computed at attachment. The canonical SMP recomputes a covering hash over the full EA (SMP + all AAs).

**EA-INV-10 — No Hidden Persistent State**: All EA state is session-scoped and stored in-memory within UWM. No EA state persists to disk, database, or external storage during runtime. Canonical SMPs in CSPCanonicalStore are also session-scoped in V1.

**EA-INV-11 — Deterministic Processing Order**: EAs are processed in deterministic tick order. The LP Nexus executes participants in sorted(participant_id) order. AA attachment order within a tick is deterministic.

### 8.4 Content Invariants

**EA-INV-12 — Inertness**: No EA may contain executable content, scheduling directives, continuation tokens, or self-referential autonomy markers. Violation results in immediate rejection at creation time.

**EA-INV-13 — Single Canonical Authority**: No duplicate EA identities may exist within a session or across the canonical store. Identity collision is a governance violation.

---

## 9. Storage Model (UWM)

### 9.1 Memory Domain Architecture

LOGOS maintains three strictly separated memory domains. The EA system operates exclusively within the first:

**Epistemic Memory (UWM/SMP)**: Session-scoped, in-memory. All active EAs reside here. Writes mediated by the Logos Agent only. Sub-agents may read (with access control) but never write.

**Operational Memory (SOP)**: Runtime telemetry and observability data. Non-semantic. Readable by the Logos Agent. Not part of the EA system. No SOP data may flow into UWM. No EA data may be derived from SOP readings.

**Historical Record (SYSTEM_AUDIT_LOGS)**: Immutable, append-only, out-of-runtime audit trail. Not readable by the runtime. EA lifecycle events may be logged here but the logs never feed back into EA processing.

**Forbidden cross-domain flows**:
- SOP → UWM (forbidden)
- AUDIT → SOP (forbidden)
- AUDIT → Runtime (forbidden)
- UWM → AUDIT (direct write forbidden; logging adapter only)

### 9.2 UWM Storage Components

The UWM storage layer for EAs consists of:

**SMPStore**: The primary EA storage manager. Maintains an in-memory dictionary of SMP identity → SMP object. Provides create_smp(), get_smp(), append_aa(), promote_classification(). All operations are governed and fail-closed.

**AA_Catalog**: The indexed AA lookup layer. Provides retrieval by aa_id, aa_type, and producer. Must be integrated with SMPStore (see §5.5).

**UWMReadAPI**: The read-access gateway. Enforces role-based access control per §4.4. Returns None on unauthorized access (deny-by-default).

**Classification_Tracker**: The monotonic ladder enforcer. Validates all classification transitions. Rejects invalid transitions immediately.

**UWM_Access_Control**: The access policy layer. Defines which roles may read which SMP fields and which AAs.

### 9.3 Canonical Store

The CSP Canonical Store (`CSP_Canonical_Store.py`) provides persistent-within-session storage for promoted C-SMPs. It is separate from the working UWM store:

- C-SMPs are stored by their canonical identity (`C-SMP:` prefixed).
- C-SMPs are fully immutable — no field modification, no AA attachment.
- The canonical store is read-only to all components except the CanonicalSMPProducer during promotion.
- DRAC and World Modeling read from the canonical store.

### 9.4 Session Scoping

All UWM state is session-scoped. When a session ends, all working EAs and canonical EAs are discarded. LOGOS does not assume persistence of epistemic state between sessions. Each session reconstructs its working memory from task inputs and dynamic session construction.

---

## 10. Promotion and Classification

### 10.1 Promotion Pipeline

The CSP Promotion pipeline transforms a working EA into a canonical EA. The pipeline consists of three components at:

```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/
  Cognitive_State_Protocol/CSP_Core/
    Promotion_Evaluator.py
    Canonical_SMP_Producer.py
    CSP_Canonical_Store.py
```

### 10.2 Promotion Evaluation

The PromotionEvaluator examines a provisional EA and determines canonicalization eligibility. Evaluation criteria:

- **AA Completeness**: The EA must have at least one analysis_result AA (from I1/SCP). Additional AAs from I3/ARP and I2/MTP are evaluated per task requirements.
- **Confidence Threshold**: The status_confidence bounds must meet the minimum threshold for canonical classification.
- **Governance Compliance**: All governance invariants (§8) must hold. Any invariant violation disqualifies the EA.
- **Hash Integrity**: The content_hash must verify against the current SMP content. The AA hash chain must be complete and consistent.

The evaluator returns a binary result: PROMOTE or REJECT. There is no partial promotion.

### 10.3 Canonical SMP Production

When the evaluator approves promotion, the CanonicalSMPProducer creates the C-SMP:

1. Copies the source SMP's sealed core fields.
2. Sets identity to `C-SMP:<session>:<seq>`.
3. Sets classification to `canonical`.
4. Appends `canonical_producer` to the chain_of_custody in provenance.
5. Attaches a `promotion_record` AA documenting the promotion decision.
6. Recomputes content_hash over the full C-SMP (core fields + all AAs).
7. Stores the C-SMP in CSPCanonicalStore.

The source SMP in UWM is not modified or deleted. It remains as the working record.

### 10.4 Classification Transition Log

Every classification transition produces a `promotion_record` or `governance_annotation` AA recording:

- Previous classification state.
- New classification state.
- Transition rationale.
- Evaluator identity.
- Tick at which the transition occurred.

This provides a complete audit trail of all classification decisions within the EA's AA Catalog.

---

## 11. Runtime Protocol Interactions

The EA system interacts with all eight Octafolium protocols. This section defines each interaction boundary.

### 11.1 SCP (Synthetic Cognition Protocol)

**Role**: Primary analysis protocol. Produces the initial epistemic enrichment of an EA.

**Interaction**: When I1 receives an SMP via tick dispatch, the SCPOrchestrator.analyze() method processes the SMP's payload using MVS and BDN subsystem adapters. The result is an `analysis_result` AA containing structured analysis output. I1 returns this AA to the Logos Agent for attachment.

**EA Fields Consumed**: identity, type, payload, provenance.
**EA Fields Produced**: analysis_result AA (via append).

### 11.2 ARP (Advanced Reasoning Protocol)

**Role**: Formal reasoning and proof generation over EA content.

**Interaction**: When I3 receives an SMP, the ARP pipeline processes the payload and any prior AAs (particularly analysis_results from SCP) to produce formal reasoning outputs. The result is a `reasoning_output` AA.

**EA Fields Consumed**: identity, payload, append_artifacts.
**EA Fields Produced**: reasoning_output AA (via append).

### 11.3 MTP (Meaning Translation Protocol)

**Role**: Natural language rendering of EA content for external consumption.

**Interaction**: When I2 receives an SMP, MTP processes the payload and accumulated AAs to produce a human-readable rendering. The result is a `rendering_directive` AA containing the rendered natural language output.

**EA Fields Consumed**: identity, payload, append_artifacts.
**EA Fields Produced**: rendering_directive AA (via append).

### 11.4 CSP (Cognitive State Protocol)

**Role**: EA lifecycle governance, promotion pipeline, canonical storage.

**Interaction**: CSP owns the promotion pipeline (PromotionEvaluator, CanonicalSMPProducer, CSPCanonicalStore). It also owns UWM, where all working EAs reside. CSP defines the classification state machine and enforces the monotonic ladder. The Logos Agent interacts with CSP components to manage EA lifecycle transitions.

**EA Fields Consumed**: All fields (for evaluation).
**EA Fields Produced**: promotion_record AA, classification state transitions.

### 11.5 EMP (Epistemic Monitoring Protocol)

**Role**: Epistemic state assessment and proof status tracking.

**Interaction**: EMP examines EAs to assess their epistemic status — whether claims within the EA are proven, unproven, contradicted, or underdetermined. EMP reads EA content (SMP payload + AAs) and may produce `governance_annotation` AAs recording epistemic assessments. In V1, EMP operates with basic proof_state checking. Full Coq verification integration is deferred to V1.1.

**EA Fields Consumed**: identity, payload, append_artifacts (particularly reasoning_output AAs).
**EA Fields Produced**: governance_annotation AA (epistemic status assessment).

### 11.6 MSPC (Multi-Process Signal Compiler)

**Role**: Coherence evaluation across concurrent EA processing signals.

**Interaction**: MSPC operates at the tick level, consuming topology information from the RGE (Radial Genesis Engine) and evaluating signal coherence across participants. MSPC does not directly modify EAs. Instead, MSPC coherence results inform the Logos Agent's routing decisions. If MSPC detects incoherence, the Logos Agent may attach a `governance_annotation` AA recording the incoherence finding.

**EA Fields Consumed**: None directly (operates on topology signals).
**EA Fields Produced**: Indirectly via governance_annotation AA if incoherence detected.

### 11.7 SOP (System Operations Protocol)

**Role**: Runtime observability and telemetry.

**Interaction**: SOP observes EA lifecycle events (creation, AA attachment, classification transitions, promotion, rejection) and writes them to operational logs. SOP is write-only — it does not read from the operational log, and no EA data may be derived from SOP observations. EA lifecycle events are emitted to SOP via the operational logger.

**EA Fields Consumed**: identity, classification (for logging).
**EA Fields Produced**: None. SOP operates in the operational memory domain, not the epistemic domain.

### 11.8 DRAC (Dynamic Reconstruction Adaptive Compilation Protocol)

**Role**: Downstream consumer of canonical EAs for session artifact assembly.

**Interaction**: DRAC reads C-SMPs from the CSP Canonical Store to incorporate canonical epistemic content into session artifacts. DRAC does not modify EAs. DRAC's consumption of EAs is read-only and occurs after canonicalization. See §12 for details.

**EA Fields Consumed**: All fields of C-SMPs (read-only from Canonical Store).
**EA Fields Produced**: None (DRAC produces session artifacts, not EAs).

---

## 12. DRAC Integration

### 12.1 Consumption Model

DRAC consumes canonical EAs (C-SMPs) from the CSP Canonical Store as inputs to its session artifact assembly process. DRAC does not interact with working (non-canonical) EAs in UWM.

The consumption flow:

1. DRAC queries CSPCanonicalStore for C-SMPs matching its assembly criteria.
2. DRAC reads the full C-SMP including all attached AAs.
3. DRAC extracts semantic content from payload and AA content fields.
4. DRAC incorporates this content into its session artifact structure.
5. DRAC never writes back to the canonical store or UWM.

### 12.2 DRAC-EA Boundary

DRAC operates under the following constraints relative to the EA system:

- DRAC may read any field of a C-SMP.
- DRAC may not modify any C-SMP field.
- DRAC may not attach AAs to C-SMPs.
- DRAC may not change C-SMP classification.
- DRAC may not promote or reject EAs.
- DRAC's internal session artifacts are not EAs — they are DRAC-domain objects governed by DRAC invariants, not EA invariants.

### 12.3 V1 Deferral

In V1, DRAC Assembler (P2.4) is deferred. The EA-DRAC integration pathway is specified here for architectural completeness. The `build_drac_adapter()` factory method and DRAC session artifact assembly are V1.1 deliverables. The C-SMP → DRAC read path does not require EA system modifications.

---

## 13. Security and Integrity Constraints

### 13.1 Write Authority Chain

Every EA write operation must be traceable to the Logos Agent through an unbroken authority chain:

```
Task Input → Logos Agent → SMPStore.create_smp() → SMP created
Sub-Agent Proposal → Logos Agent → SMPStore.append_aa() → AA attached
Promotion Decision → Logos Agent → SMPStore.promote_classification() → Classification updated
```

No shortcut paths exist. No sub-agent may bypass the Logos Agent to write to UWM.

### 13.2 Hash Integrity Verification

The EA system supports integrity verification at two levels:

**SMP-level**: The content_hash on each SMP is computed at creation over the immutable core fields. At any point, the hash can be recomputed and compared to detect tampering.

**AA-level**: Each AA has its own content_hash computed at attachment. The SMP's aa_hashes list provides an ordered integrity chain over all attached AAs.

**C-SMP-level**: At canonicalization, a new content_hash is computed covering the full EA (core fields + all AAs), providing a single integrity anchor for the canonical artifact.

### 13.3 Boundary Validation

The Boundary_Validators module provides five validators relevant to the EA system:

- `validate_startup_context()`: Ensures the runtime context is well-formed before any EA can be created.
- `validate_task()`: Ensures task input meets EA-compatible structure requirements.
- `validate_route_packet()`: Ensures SMP routing packets are well-formed.
- `validate_tick_result()`: Ensures tick results conform to the P1-IF-07 contract.
- `validate_agent_write_boundary()`: Ensures AA attachment requests originate from authorized contexts.

All validators are fail-closed — they raise on any violation.

---

## 14. Failure Modes

The EA system is designed fail-closed. Every failure mode results in explicit rejection, halt, or degraded operation with governance annotation. No silent fallback or implicit recovery is permitted.

### 14.1 Creation Failures

| Failure | Response |
|---------|----------|
| Missing required SMP field | Reject creation, raise validation error |
| Payload contains executable content | Reject creation, raise inertness violation |
| Invalid provenance envelope | Reject creation, raise provenance error |
| Identity collision | Reject creation, raise uniqueness violation |
| Write authorization missing | Reject creation, raise authority violation |

### 14.2 AA Attachment Failures

| Failure | Response |
|---------|----------|
| Target SMP not found | Reject attachment, raise lookup error |
| Target SMP is canonical | Reject attachment, raise immutability violation |
| Target SMP is rejected | Reject attachment, raise terminal state error |
| AA schema violation | Reject attachment, raise validation error |
| Write boundary violation | Reject attachment, raise authority error |

### 14.3 Classification Failures

| Failure | Response |
|---------|----------|
| Invalid transition (backward) | Reject transition, raise monotonic ladder violation |
| Promotion evaluation failure | Set classification to rejected, attach governance_annotation AA |
| Hash integrity mismatch | Reject promotion, attach governance_annotation AA |

### 14.4 Runtime Failures

| Failure | Response |
|---------|----------|
| Tick budget exhaustion (50 max) | Halt task processing, attach governance_annotation to active EA |
| MRE budget exhaustion | Halt participant, attach governance_annotation |
| Sub-agent timeout | Skip AA proposal, Logos Agent attaches governance_annotation |

---

## 15. Observability and Auditing

### 15.1 EA Lifecycle Events

The following EA lifecycle events are emitted to the SOP operational logger:

| Event | Trigger | Data Logged |
|-------|---------|-------------|
| `ea_created` | SMPStore.create_smp() | smp_id, type, classification, tick |
| `aa_attached` | SMPStore.append_aa() | smp_id, aa_id, aa_type, producer, tick |
| `classification_changed` | SMPStore.promote_classification() | smp_id, old_classification, new_classification, tick |
| `promotion_evaluated` | PromotionEvaluator.evaluate() | smp_id, result (PROMOTE/REJECT), rationale, tick |
| `csmp_produced` | CanonicalSMPProducer.produce() | csmp_id, source_smp_id, tick |
| `ea_rejected` | Classification → rejected | smp_id, rejection_reason, tick |

### 15.2 Audit Trail Properties

EA lifecycle audit events maintain the following properties:

- **Write-only**: SOP receives events but never feeds them back into EA processing.
- **No readback**: No runtime component reads from the operational log. The no_audit_readback invariant is absolute.
- **Ordered**: Events are logged in tick-sequential order within a session.
- **Complete**: Every state transition produces a log event. No silent transitions.

### 15.3 Operational Logger Integration

The operational logger is injected into RuntimeLoop at construction time and propagated to agent wrappers and UWM components. Per P4.5, 19 logging points are required across 5 files. EA-specific log points fall within this allocation:

- RuntimeLoop: EA creation event, tick-level EA state summary.
- Agent_Wrappers: AA proposal submission, AA attachment confirmation.
- SMP_Store: create_smp(), append_aa(), promote_classification() events.
- CSP_Canonical_Store: C-SMP production event.

---

## 16. Implementation Notes

### 16.1 Current Implementation Status

Based on the V1 P1-P4 compliance audit (2026-03-03), the EA system's implementation status:

**Implemented and compliant**:
- SMP_Schema.py (SMP dataclass with all required fields)
- SMP_Store.py (create_smp, append_aa, promote_classification with hash integrity)
- Classification_Tracker.py (monotonic ladder enforcement)
- UWM_Access_Control.py (UWMReadAPI with role-based access)
- Promotion_Evaluator.py, Canonical_SMP_Producer.py, CSP_Canonical_Store.py (promotion pipeline)
- Boundary_Validators.py (all 7 validators including validate_agent_write_boundary)

**Implemented with issues**:
- UWM `__init__.py` has duplicate class definitions (REM-06)
- AA_Catalog.py exists but is not integrated into SMPStore (REM-09)

**Not yet implemented (blocked by P3.1)**:
- SMP routing state machine in Logos Agent
- Sub-agent AA proposal protocol via _on_tick()
- Multi-tick EA lifecycle processing via _process_task()
- UWM/SCP/CSP/MTP/ARP injection into agent constructors
- Operational logging points (P4.5)

### 16.2 Integration Sequencing

The EA system becomes fully operational when the following remediations are completed in order:

1. **REM-01 (P3.1)**: Implement SMP Pipeline — agent wrappers with subsystem delegation, SMP routing state machine, multi-tick processing. This is the critical path blocker.
2. **REM-02**: Fix tick result schema to P1-IF-07 — enables proper EA state reporting per tick.
3. **REM-06**: Clean UWM `__init__.py` — removes duplicate definitions that could cause import ambiguity.
4. **REM-09**: Integrate AA_Catalog into SMPStore — enables indexed AA lookup per §5.5.
5. **REM-07**: Add operational logging points — enables EA lifecycle observability per §15.

### 16.3 Canonical File Locations

| Component | Path |
|-----------|------|
| SMP_Schema.py | `CSP_Core/Unified_Working_Memory/SMP_Schema.py` |
| SMP_Store.py | `CSP_Core/Unified_Working_Memory/SMP_Store.py` |
| AA_Catalog.py | `CSP_Core/Unified_Working_Memory/AA_Catalog.py` |
| Classification_Tracker.py | `CSP_Core/Unified_Working_Memory/Classification_Tracker.py` |
| UWM_Access_Control.py | `CSP_Core/Unified_Working_Memory/UWM_Access_Control.py` |
| Promotion_Evaluator.py | `CSP_Core/Promotion_Evaluator.py` |
| Canonical_SMP_Producer.py | `CSP_Core/Canonical_SMP_Producer.py` |
| CSP_Canonical_Store.py | `CSP_Core/CSP_Canonical_Store.py` |
| Boundary_Validators.py | `Logos_Core/Orchestration/Boundary_Validators.py` |
| Agent_Wrappers.py | `Logos_Core/Orchestration/Agent_Wrappers.py` |
| Agent_Lifecycle_Manager.py | `Logos_Core/Orchestration/Agent_Lifecycle_Manager.py` |
| Runtime_Loop.py | `Logos_Core/Orchestration/Runtime_Loop.py` |
| Nexus_Factory.py | `Logos_Core/Orchestration/Nexus_Factory.py` |

All paths are relative to:
```
LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/
```

### 16.4 World Modeling Integration

The World Modeling subsystem (`World_Modeling/world_model.py`, `PXL_World_Model.py`, `commitment_ledger.py`) within UWM provides the semantic grounding context against which EAs are evaluated. World Modeling does not modify EAs directly. Instead:

- The PXL World Model provides the axiomatic baseline against which SCP analysis and ARP reasoning operate.
- The Commitment Ledger tracks semantic commitments derived from canonical EAs.
- The World Model provides context that informs PromotionEvaluator decisions.

World Modeling reads from canonical EAs and task context. It does not write to EAs.

### 16.5 Design Constraints

This specification introduces no new Python classes, no new files, and no new import paths. The EA abstraction is realized through the existing component set. The only implementation changes required are:

- Integration of AA_Catalog into SMPStore (wiring change, not new component).
- Cleanup of UWM `__init__.py` duplicates (code quality fix, not new component).
- Completion of P3.1 agent wiring (already specified in P3 blueprint, not new architecture).

No architectural contradictions are introduced. No major refactoring is required.

---

*End of specification.*

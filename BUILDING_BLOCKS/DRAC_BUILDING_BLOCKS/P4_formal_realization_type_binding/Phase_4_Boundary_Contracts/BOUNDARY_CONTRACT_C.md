# BOUNDARY_CONTRACT_C.md
Boundary: Persistence Gate
Status: CANONICAL | DESIGN-ONLY
Authority: None (Specification Only)
Execution: STRICTLY FORBIDDEN
Phase: Phase 4 Closure Artifact
Scope: Defines the persistence gate boundary between DR–AC and mutation_gates

---

## Semantic Synopsis (GPT Handoff)

This artifact formally defines Boundary Contract C — the Persistence Gate
between the DR–AC artifact_cataloger stage (Stage 8) and the mutation_gates
persistence enforcement infrastructure. It specifies the gate-mediated
write contract, what may be persisted, what is forbidden, failure semantics
(REJECT, not HALT), and explicit non-capabilities. This is the sole
persistence boundary in the DR–AC pipeline. GPT should treat this as the
authoritative specification for DR–AC's persistence contract.

---

## 1. Boundary Identity

**Name:** Boundary C — Persistence Gate

**Purpose:** Mediate DR–AC's conditional write authority through
mutation_gates without granting autonomous persistence, ungoverned writes,
or authority escalation.

**Participants:**
- **Persistence Proposer (DR–AC side):**
  - artifact_cataloger (Stage 8)
- **Persistence Enforcer (Infrastructure side):**
  - mutation_gates (existing LOGOS persistence governance)

**Intent:** Stage 8 may propose artifacts for persistence. mutation_gates
decides whether to allow or reject. Stage 8 never writes autonomously.

---

## 2. Boundary Specification

### 2.1 What May Cross the Boundary (Permitted)

#### From DR–AC to mutation_gates (Proposal Direction)
- Persistence Proposal containing:
  - Artifact Candidate (the artifact to persist)
  - Metadata Set (three non-semantic fields only):
    - input_class
    - constraint_set
    - effectiveness_signal

#### From mutation_gates to DR–AC (Decision Direction)
- Gate Decision: ALLOW | REJECT
- No additional metadata, reasoning, or partial results
- No modification of the proposed artifact

### 2.2 What Is Forbidden (Prohibited)

#### DR–AC May NOT
- Write without an explicit ALLOW from mutation_gates
- Retry a rejected proposal
- Submit a modified version of a rejected artifact
- Inspect mutation gate internals or decision logic
- Override or bypass a REJECT decision
- Persist anything outside the Persistence Proposal structure
- Persist session-ephemeral state directly
- Write across user boundaries

#### mutation_gates May NOT
- Modify artifact content
- Grant DR–AC autonomous write authority
- Execute DR–AC stage logic
- Return partial, probabilistic, or conditional results
- Persist proposals for audit purposes (observability concerns are
  separate)

---

## 3. Stage 8 → mutation_gates Gate Contract

### 3.1 Conditional Execution Preconditions

Stage 8 executes ONLY if:
- Stage 5 Decision Outcome was ADAPT or GENERATE-NEW
- Stage 7 (output delivery) is complete

If Stage 5 Decision Outcome was REUSE, Stage 8 does not execute.

### 3.2 Persistence Proposal Structure

Stage 8 submits a Persistence Proposal containing:

**Artifact Candidate:**
- The specific artifact produced by Stage 6
- Either a newly generated artifact (GENERATE-NEW) or an adapted copy
  (ADAPT)
- Unmodified by Stage 8

**Metadata Set (Exactly Three Fields):**
- **input_class:** Determined at Stage 5; non-semantic classification
- **constraint_set:** Governance context from Stage 3; non-semantic
  constraint profile
- **effectiveness_signal:** From Calibration Signal Aggregate; non-
  semantic observable indicator

No additional metadata may be attached.

### 3.3 Gate Decision Semantics

mutation_gates returns exactly one of:
- **ALLOW:** Persistence is permitted
- **REJECT:** Persistence is not permitted

The conditions under which REJECT is returned are defined by
mutation_gates logic (Autonomy_Policies enforcement), not by DR–AC.

### 3.4 Response Handling

**On ALLOW:**
- Artifact is persisted to user's Curated Artifact store
- Recall Object is created (or updated) in user's Recall index
- Both writes are user-scoped; no cross-boundary writes
- Adapted artifacts persist as distinct entries; source artifact
  unmodified

**On REJECT:**
- Artifact is NOT persisted
- No Recall Object is created
- No writes occur
- No retry, no fallback, no escalation

**Regardless of ALLOW or REJECT:**
- Session-Ephemeral Compilation is discarded
- All un-attached Calibration Signals are discarded
- All session-local state is discarded

### 3.5 Traceability

Declared in:
- STAGE_8_ARTIFACT_CATALOGER_TYPE_SCHEMA.md
- LOGOS_Reconstruction_Scaffolding_Design.md — Section 4, Section 7
- LOGOS_DR_AC_Invariant_Specification.md — G3, G5, G6, G7

---

## 4. Failure Semantics (REJECT, Not HALT)

### 4.1 Critical Distinction

Stage 8's failure mode is **REJECT**, not HALT.

**REJECT means:**
- The artifact is not persisted
- The session has already completed output delivery (Stage 7)
- Delivered output stands unaffected
- This artifact will not be available for future sessions

**REJECT does NOT mean:**
- The session failed
- The output was invalid
- The user did not receive a response

### 4.2 On REJECT

**Preserved:**
- The delivered output (immutable; delivery completed at Stage 7)

**Discarded:**
- The artifact candidate
- The session Calibration Signal aggregate (not attached to any
  persisted Recall Object)
- The Session-Ephemeral Compilation
- All session-local state

**Forbidden:**
- Retry of the rejected proposal
- Fallback to a modified proposal
- Escalation
- Persistence through any mechanism other than mutation_gates

### 4.3 Traceability

REJECT semantics declared in:
- LOGOS_DR_AC_artifact_cataloger_Formalization.md — Section 6
- LOGOS_DR_AC_Invariant_Specification.md — Stage 8 HALT Semantics
- PHASES_1_3_AUDITS.md — Stage 8 failure semantics

---

## 5. Authority Boundaries

### 5.1 DR–AC Authority at This Boundary

DR–AC holds **conditional write authority** at Boundary C.

"Conditional" means:
- Write authority exists only when mutation_gates returns ALLOW
- No autonomous writes
- No writes outside the declared Persistence Scope
- No writes without explicit gate approval

Stage 8 may:
- Submit Persistence Proposals
- Receive Gate Decisions
- Write when ALLOW is received
- Discard when REJECT is received

Stage 8 may NOT:
- Write without ALLOW
- Retry after REJECT
- Escalate authority
- Bypass mutation_gates

### 5.2 mutation_gates Authority at This Boundary

mutation_gates holds **persistence enforcement authority** at Boundary C.

It may:
- Evaluate Persistence Proposals against Autonomy_Policies
- Return ALLOW or REJECT
- Enforce policy without DR–AC inspection or challenge

It may NOT:
- Modify artifact content
- Grant DR–AC autonomous write authority
- Execute DR–AC logic
- Return conditional or partial approvals

---

## 6. Persistence Scope (Authority Bounds)

### 6.1 What May Be Persisted

When mutation_gates returns ALLOW, Stage 8 may write to exactly two
locations:

**Target 1 — User's Curated Artifact Store:**
- The Artifact Candidate (elevated from ephemeral to persisted scope)
- User-scoped; no cross-boundary writes

**Target 2 — User's Recall Index:**
- A new Recall Object indexing the persisted artifact
- Indexed by the three metadata fields
- User-scoped; no cross-boundary writes

### 6.2 Constraints on Writes

**On ADAPT:**
- The persisted artifact is a distinct entry
- The source artifact and its Recall Object are not modified
- The two entries are independent

**On GENERATE-NEW:**
- A new artifact and a new Recall Object are created
- No existing entries are modified

**Always:**
- No existing Curated Artifact or Recall Object is overwritten, modified,
  or deleted by this module
- Recall Objects are created or left unchanged; never updated to modify
  existing index fields

### 6.3 What May NOT Be Persisted

- Session-Ephemeral Compilation (directly; only the Artifact Candidate
  component is persisted)
- Calibration Signals (as independent state; only as the
  effectiveness_signal metadata field)
- Any governance validation results
- Any pipeline state or metadata
- Any content from rejected proposals

---

## 7. Explicit Non-Capabilities

### 7.1 DR–AC at Boundary C
- Cannot write without an explicit ALLOW from mutation_gates
- Cannot retry a rejected proposal
- Cannot modify, overwrite, or delete existing Curated Artifacts or
  Recall Objects
- Cannot modify the source artifact when cataloging an adaptation
- Cannot attach metadata fields beyond the declared three
- Cannot persist session-ephemeral state directly
- Cannot learn, score, or rank artifacts
- Cannot modify semantic content
- Cannot access observability or audit domain data (G8)
- Cannot execute when Stage 5 decision was REUSE
- Cannot cause HALT (failure mode is REJECT and discard)
- Cannot inspect, interpret, or challenge mutation gate reasoning

### 7.2 mutation_gates at Boundary C
- Cannot modify artifact content
- Cannot grant DR–AC autonomous write authority
- Cannot execute DR–AC stage logic
- Cannot return partial or conditional approvals
- Cannot persist proposals for governance purposes (observability is
  separate)

---

## 8. Boundary Isolation Properties

### 8.1 No Authority Escalation

Querying mutation_gates does not grant DR–AC additional authority.
Write authority is conditional and gate-mediated. It does not exceed
what mutation_gates explicitly permits per proposal.

### 8.2 No Autonomous Persistence

DR–AC never writes autonomously. Every write requires explicit ALLOW.
No fallback, no degraded mode, no alternative persistence pathway.

### 8.3 No Cross-User Writes

All writes are user-scoped. Stage 8 cannot write across user boundaries.

### 8.4 No Governance Bypass

There is no mechanism to bypass, override, or circumvent mutation_gates.
REJECT is final and unappealable within the pipeline.

### 8.5 G6 Enforcement

Stage 8 is the sole persistence point (G6). No other stage creates
durable state. This boundary is the only location where ephemeral content
becomes persistent.

---

## 9. Traceability to Phase 2/3

Boundary C is explicitly declared in:
- LOGOS_Reconstruction_Scaffolding_Design.md — Section 7 (Boundary with
  Existing Infrastructure)
- LOGOS_DR_AC_Invariant_Specification.md — G3 (Non-mutation prior to
  governance approval), G5 (Recall index writable only at Stage 8), G6
  (Single persistence gate), G7 (Monotonic authority)
- PHASES_1_3_AUDITS.md — Stage 8 audit findings

---

## 10. Relationship to Other Boundaries

Boundary C is distinct from:
- **Boundary A** (Governance Query Interface): Stages 3/4 → Safety_Gates
- **Boundary B** (Output Delivery Handoff): Stage 6 → MTP

Boundary C concerns persistence only.
It does not involve governance validation or output delivery.

---

## 11. Closing Declaration

Boundary Contract C defines the Persistence Gate between DR–AC and
mutation_gates.

This boundary:
- Permits gate-mediated writes only
- Forbids autonomous persistence, authority escalation, or governance
  bypass
- Enforces conditional write authority absolutely
- Maintains isolation between DR–AC and persistence infrastructure
- Is the sole persistence point in the DR–AC pipeline (G6)

This boundary is design-only. Implementation requires explicit Phase 5
authorization.

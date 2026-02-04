# STAGE_5_REUSE_DECISION_TYPE_SCHEMA.md
Stage: reuse_decision
Status: DESIGN-ONLY | NON-EXECUTABLE
Artifact Class: Type Schema (A5)
Grounding: PHASE_4_GROUNDING_RULE.md compliant
Note: Stage 5 Type Schema was PARTIAL in gap ledger. This artifact extracts
and formalizes the inline type declarations from Phase 3 into a standalone
Phase 4 Type Schema.

---

## Semantic Synopsis (GPT Handoff)

This is the Phase 4 Type Schema for reuse_decision (Stage 5). It defines
four inputs — Current Input, Recall Index, Constraint Set, and Overlaid
Surface (forward-referenced to Stage 4) — and one output: Decision Result.
Decision Result is a composite type containing a Decision Outcome
(enumerated: REUSE, ADAPT, GENERATE-NEW) and a conditional Artifact
Pointer (present when outcome is REUSE or ADAPT; absent when
GENERATE-NEW). The Decision Result carries a pipeline-gating property:
its outcome determines whether Stage 8 executes. This is a structural
property of the decision type — it does not constitute write authority
for Stage 5. Stage 5's authority is None (read-only) per Phase 3.
The tasking prompt characterized this as "the first stage with non-zero
authority" — that characterization does not match Phase 3 source material.
Authority in the LOGOS architecture denotes write capability; Stage 5 has
none. The downstream gating effect belongs to the Decision Result type.
G5 (Recall index read-only) is the primary safety-critical invariant at
this stage. Two elements are Phase 4 derivations (Decision Result as a
composite output type, and Constraint Set as a standalone type). All other
elements trace directly to Phase 2/3 declarations. GPT should treat this
as a standalone type definition ready for Interface Contract completion
coupling and Realization Constraints for Stage 5.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Component Name | reuse_decision |
| Stage Number | 5 |
| Pipeline Role | Classification and selection boundary; sole decision-producing stage |
| Primary Function | Classify input; query Recall index; return exactly one decision (REUSE, ADAPT, or GENERATE-NEW) with conditional artifact pointer |
| Authority | None (read-only) |

---

## 2. Structural Fields

### Required Fields

- current_input [INPUT]
  Type: Current Input
  Description: The raw input received by the pipeline for this session.
  Consumed for classification purposes only. Classification is determined
  by structural dimensions (type and constraint profile), not by semantic
  interpretation of content.

- recall_index [INPUT]
  Type: Recall Index
  Description: The read-only, queryable index of the user's Recall Objects.
  Derived from Recall Objects loaded at Stage 2. Queried against classified
  input dimensions to locate candidate artifacts. Must not be mutated,
  scored, or ranked during pipeline execution. G5 enforced.

- constraint_set [INPUT]
  Type: Constraint Set
  Description: The governance constraint profile active for this session.
  Established at Stage 3 via governance validation. Defines compatibility
  requirements that candidate artifacts must satisfy. Read-only; does not
  change during Stage 5 processing.

- overlaid_surface [INPUT]
  Type: Overlaid Surface
  Description: The baseline-plus-overlay output from Stage 4. Defines the
  artifact eligibility boundary — only artifacts present in this surface
  may be selected by REUSE or ADAPT decisions.

  Forward Reference: Overlaid Surface
  Definition artifact: STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md
  Expected phase: Phase 4

- reuse_decision [OUTPUT]
  Type: Decision Result
  Description: The single decision returned by this stage. Contains the
  Decision Outcome (enumerated) and a conditional Artifact Pointer.
  Exactly one Decision Result is produced per invocation, or the stage
  HALTs. The decision is fully traceable to input_class and constraint_set
  — no other factors determine the outcome.

### Optional Fields

None. No optional fields are declared or justified by Phase 2/3
source material.

---

## 3. Nullability Rules

| Field | Nullability | Rationale |
|-------|-------------|-----------|
| current_input | NON-NULL | Classification cannot proceed without input |
| recall_index | NON-NULL | The index must exist; empty index is structurally valid but null is not |
| constraint_set | NON-NULL | Governance constraint profile is required for compatibility evaluation |
| overlaid_surface | NON-NULL | Received from Stage 4; defines eligible artifact set |
| reuse_decision | NON-NULL | Exactly one Decision Result is produced, or the stage HALTs |

---

## 4. Subordinate Type Definitions

### Current Input

Structural definition: The raw input to be classified. Opaque from
Stage 5's perspective — classification is determined by structural
dimensions (type profile and constraint profile), not by semantic
interpretation. Contains no logic, authority, or mutable state.

### Recall Index

Structural definition: A read-only, queryable collection of Recall Objects
derived from the Loaded Profile produced by Stage 2. Organized for lookup
by the three indexed dimensions declared on Recall Objects: input_class,
constraint_set, and effectiveness_signal. Supports candidate location only.
Must not be mutated, scored, or ranked during pipeline execution.

Contains:
- Recall Objects (zero or more)

Forward Reference: Recall Object
Definition artifact: STAGE_2_PROFILE_LOADER_TYPE_SCHEMA.md
Expected phase: Phase 4

Constraint: G5 — Recall index is read-only during pipeline execution.

### Constraint Set

Structural definition: The governance constraint profile active for this
session. Established by Stage 3 governance validation. Defines the
compatibility requirements that candidate artifacts must satisfy for
selection. Shared indexing dimension with Recall Objects — artifacts are
indexed by constraint_set and must be evaluated against this same profile
for compatibility.

### Overlaid Surface

Forward Reference: Overlaid Surface
Definition artifact: STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Defines the artifact eligibility boundary — only
artifacts present in this surface may be selected by REUSE or ADAPT.

### Decision Result

Structural definition: The single composite output of Stage 5. Contains
a Decision Outcome and a conditional Artifact Pointer. Exactly one
Decision Result is produced per invocation.

Fields:
- outcome: Decision Outcome (NON-NULL)
- artifact_pointer: Artifact Pointer (NULLABLE — present when outcome
  is REUSE or ADAPT; absent when outcome is GENERATE-NEW)

Pipeline-gating property: If outcome is ADAPT or GENERATE-NEW, Stage 8
(artifact_cataloger) executes post-delivery. If outcome is REUSE, Stage 8
does not execute. This is a structural property of the Decision Result
type. It does not constitute write authority for Stage 5 — Stage 5's
authority remains None (read-only) per Phase 3.

### Decision Outcome

Structural definition: Enumerated type representing the three admissible
pipeline decisions. Exactly one value is selected per invocation.
Outcomes are evaluated in priority order; the first satisfied outcome
is selected.

Enumerated values (priority order):

- REUSE: An existing Curated Artifact is selected for direct use without
  modification. Selection criteria (all must hold):
  - Artifact's indexed input_class matches the classified current input
  - Artifact's indexed constraint_set is compatible with active Constraint Set
  - Artifact is present in the Overlaid Surface

- ADAPT: An existing Curated Artifact is selected as source for
  surface-level modification. Selection criteria (all must hold):
  - Artifact partially matches the classified input_class
  - Required modification is limited to expression parameters or routing —
    not to semantic content or invariant profile
  - Artifact is present in the Overlaid Surface

- GENERATE-NEW: No existing artifact satisfies REUSE or ADAPT criteria.
  Selection criteria (all must hold):
  - No artifact in Recall Index matches under REUSE criteria
  - No artifact in Recall Index satisfies ADAPT partial-match and
    surface-modification constraints

### Artifact Pointer

Structural definition: A reference to a specific Curated Artifact within
the Overlaid Surface. Present only when Decision Outcome is REUSE or
ADAPT. The referenced artifact must be present in the Overlaid Surface.

When REUSE: references the selected artifact for direct binding at
Stage 6. No copy is made; no modification occurs.

When ADAPT: references the source artifact for surface-level modification
at Stage 6. The source artifact itself is not modified — Stage 6 produces
a distinct copy.

When GENERATE-NEW: no Artifact Pointer is produced.

---

## 5. Carried-Forward Invariants

| Invariant | Statement | Source |
|-----------|-----------|--------|
| G5 — Recall index read-only | The Recall index is not mutated, scored, or ranked during pipeline execution. No scoring or ranking state is modified. | LOGOS_DR_AC_Invariant_Specification.md — G5; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.3 |
| Exactly one decision | Exactly one Decision Result is returned per invocation. Multiple decisions are structurally impossible. | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants |
| Decision traceability | The decision is fully traceable to input_class and constraint_set. No other factors determine the outcome. | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 7 |
| Compound HALT condition | HALT occurs if and only if input classification is ambiguous AND no REUSE candidate exists. Both conditions must hold simultaneously. Ambiguous classification with an existing REUSE candidate resolves by selection. Unambiguous classification without a REUSE candidate proceeds to ADAPT or GENERATE-NEW. | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 HALT Semantics; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 6 |
| No intermediate state persistence | No intermediate state is persisted — including input classifications, candidate sets, or intermediate decisions. G6 enforced. | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.3; LOGOS_DR_AC_Invariant_Specification.md — G6 |
| Source artifact immutability on ADAPT | If decision is ADAPT, the source artifact referenced by Artifact Pointer is not modified. Stage 6 produces a distinct copy. | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |

---

## 6. Explicit Non-Capabilities

The reuse_decision type and its subordinate types:

- Do NOT hold write authority of any kind
- Do NOT mutate the Recall index or any scoring or ranking state within it
- Do NOT persist any state — including input classifications, candidate sets,
  or intermediate decisions
- Do NOT produce more than one decision per invocation
- Do NOT continue when input classification is ambiguous and no REUSE
  candidate exists
- Do NOT interpret semantic content — classification is by structural
  dimensions only
- Do NOT access or modify Canonical Primitives
- Do NOT access observability or audit domain data (G8)
- Do NOT override or bypass governance validation results from Stages 3 or 4
- Do NOT introduce semantic content not present in the Overlaid Surface or baseline

---

## 7. Traceability Table

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|
| current_input (field) | TRACE | Declared as Stage 5 input ("Current input") in Phase 2; declared as input_raw in Phase 3 formalization | LOGOS_DR_AC_Design_Specification.md — Stage 5, Input; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1 |
| Current Input (subordinate type) | TRACE | Declared as input_raw in Phase 3 formalization; structural role as classification source declared in Phase 3 Section 1 | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 1; Section 2.1 |
| recall_index (field) | TRACE | Declared as Stage 5 input in Phase 2 and Phase 3 | LOGOS_DR_AC_Design_Specification.md — Stage 5, Input; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1 |
| Recall Index (subordinate type) | TRACE | Declared as recall_index in Phase 3; read-only and queryable per G5; indexed dimensions declared on Recall Objects in Phase 2 | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1; LOGOS_DR_AC_Invariant_Specification.md — G5 |
| Recall Object (forward ref) | TRACE | Defined in Stage 2 Type Schema; composes the Recall Index | STAGE_2_PROFILE_LOADER_TYPE_SCHEMA.md — Section 4 |
| constraint_set (field) | TRACE | Declared as Stage 5 input in Phase 3 formalization | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1 |
| Constraint Set (subordinate type) | DERIVE | Phase 3 declares constraint_set as an input with source "Governance context (established at Stage 3)" but does not define it as a standalone structural type. Defined as the governance constraint profile per the decision criteria declarations and shared indexing dimension with Recall Objects. This is a Phase 4 derivation. | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1; LOGOS_DR_AC_Design_Specification.md — Section 4.1 |
| overlaid_surface (field) | TRACE | Declared as Stage 5 input ("overlaid artifact set") in Phase 2 and Phase 3 | LOGOS_DR_AC_Design_Specification.md — Stage 5, Input; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.1 |
| Overlaid Surface (forward ref) | TRACE | Defined in Stage 4 Type Schema; received as input | STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md — Section 4 |
| reuse_decision (field) | TRACE | Declared as Stage 5 output in Phase 2 and Phase 3 | LOGOS_DR_AC_Design_Specification.md — Stage 5, Output; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.2 |
| Decision Result (subordinate type) | DERIVE | Phase 3 declares two separate outputs (Decision and Artifact pointer) with explicit conditional relationship. Composing them into a single typed output object is required to represent the conditional pointer-presence constraint as a structural property. This is a Phase 4 derivation. | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.2 |
| Decision Outcome (subordinate type) | TRACE | Three enumerated values and selection criteria explicitly declared in Phase 2 Section 4 and Phase 3 Section 5 | LOGOS_DR_AC_Design_Specification.md — Section 4; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| REUSE criteria | TRACE | Explicitly declared | LOGOS_DR_AC_Design_Specification.md — Section 4.1; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| ADAPT criteria | TRACE | Explicitly declared | LOGOS_DR_AC_Design_Specification.md — Section 4.2; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| GENERATE-NEW criteria | TRACE | Explicitly declared | LOGOS_DR_AC_Design_Specification.md — Section 4.3; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| Priority-order selection rule | TRACE | "Applied in order. The first satisfied outcome is selected." | LOGOS_DR_AC_Design_Specification.md — Section 4 |
| Artifact Pointer (subordinate type) | TRACE | Declared as artifact_ref in Phase 3; presence conditions (REUSE or ADAPT) and absence condition (GENERATE-NEW) explicitly declared | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.2; Section 5 |
| Pipeline-gating property | TRACE | Stage 8 conditional execution determined by Stage 5 outcome — explicitly declared in Phase 2 | LOGOS_DR_AC_Design_Specification.md — Stage 8 |
| Authority: None | TRACE | Explicitly declared in Phase 3 formalization header and Section 2.3 | LOGOS_DR_AC_reuse_decision_Formalization.md — Header; Section 2.3 |
| G5 carry-forward | TRACE | G5 explicitly enforced at Stage 5 | LOGOS_DR_AC_Invariant_Specification.md — G5; PHASES_1_3_AUDITS.md — Stage 5 |
| Exactly one decision | TRACE | Explicitly declared in post-invariants | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants |
| Decision traceability | TRACE | Explicitly declared in post-invariants and invariant traceability table | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 7 |
| Compound HALT condition | TRACE | Explicitly declared; both conditions required simultaneously | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 HALT Semantics; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 6 |
| No intermediate persistence | TRACE | Explicitly declared in Phase 3 Section 2.3; G6 enforced | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.3; LOGOS_DR_AC_Invariant_Specification.md — G6 |
| Source artifact immutability on ADAPT | TRACE | Explicitly declared in Phase 3 post-invariants and decision semantics | LOGOS_DR_AC_Invariant_Specification.md — Stage 5 Post-Invariants; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| Non-capability: no write authority | TRACE | Explicitly declared in Phase 3 header and Section 2.3 | LOGOS_DR_AC_reuse_decision_Formalization.md — Header; Section 2.3 |
| Non-capability: no Recall index mutation | TRACE | G5; Phase 3 Section 2.3 | LOGOS_DR_AC_Invariant_Specification.md — G5; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.3 |
| Non-capability: no state persistence | TRACE | Phase 3 Section 2.3; G6 | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 2.3; LOGOS_DR_AC_Invariant_Specification.md — G6 |
| Non-capability: no semantic interpretation | TRACE | Phase 3 Section 1: "classifies inputs and matches classifications against an existing index" | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 1 |
| Non-capability: no audit domain access | TRACE | G8; Phase 3 Non-Capabilities | LOGOS_DR_AC_Invariant_Specification.md — G8; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 8 |
| Non-capability: no governance override | TRACE | Explicitly declared in Phase 3 Non-Capabilities | LOGOS_DR_AC_reuse_decision_Formalization.md — Section 8 |

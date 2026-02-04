# STAGE_2_PROFILE_LOADER_TYPE_SCHEMA.md
Stage: profile_loader
Status: DESIGN-ONLY | NON-EXECUTABLE
Artifact Class: Type Schema (A5)
Grounding: PHASE_4_GROUNDING_RULE.md compliant

---

## Semantic Synopsis (GPT Handoff)

This is the Phase 4 Type Schema for profile_loader (Stage 2). It defines
the input type (User Identifier), the nullable source type (User Profile
Source), and the output type (Loaded Profile). Loaded Profile is
structurally defined as containing only Recall Objects and Calibration
Signal Aggregates — empty is valid. The semantic purity gate function
of this stage is represented structurally through the permitted-content
constraint on User Profile Source, not procedurally. All fields and types
are grounded in Phase 2 (LOGOS_DR_AC_Design_Specification.md) and Phase 3
(profile_loader formalization / LOGOS_DR_AC_Invariant_Specification.md).
One input field and one subordinate type are Phase 4 derivations, explicitly
labeled and justified. It belongs to the Orchestration layer. It respects
G2 (Non-semantic profile purity). GPT should treat this as a standalone type
definition ready for coupling to Phase 4 Interface Contract completion and
Realization Constraints for Stage 2.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Component Name | profile_loader |
| Stage Number | 2 |
| Pipeline Role | Semantic purity gate for user-scoped continuity data |
| Primary Function | Load user profile; validate non-semantic purity; produce Loaded Profile or empty default |

---

## 2. Structural Fields

### Required Fields

- user_identifier [INPUT]
  Type: User Identifier
  Description: Scoped, non-semantic identifier used to locate the
  user's profile data. Contains no semantic payload. Does not itself
  constitute profile content.

- loaded_profile [OUTPUT]
  Type: Loaded Profile
  Description: The validated profile output. Contains only Recall
  Objects and Calibration Signal Aggregates. Structurally empty when
  source is missing, unreadable, or absent. Empty is valid — it is
  the safe default, not a failure state.

### Nullable Fields

- user_profile_source [INPUT]
  Type: User Profile Source
  Nullability: NULLABLE
  Description: The raw profile data located via user_identifier. Null
  when the profile is missing or unreadable. When present, structurally
  permitted to contain only Recall Objects and Calibration Signal
  Aggregates. Any other content category constitutes semantic
  contamination and triggers HALT. Failure semantics are covered by
  Phase 3 Interface Contract carry-forward.

### Optional Fields

None. No optional fields are declared or justified by Phase 2/3
source material.

---

## 3. Nullability Rules

| Field | Nullability | Rationale |
|-------|-------------|-----------|
| user_identifier | NON-NULL | Stage cannot attempt profile location without a scoped identifier |
| user_profile_source | NULLABLE | Missing or unreadable profile is the safe default for new users; not a failure |
| loaded_profile | NON-NULL | Output is always produced — either populated or empty; HALT is the only alternative to production |

---

## 4. Subordinate Type Definitions

### User Identifier

Structural definition: Opaque, scoped, non-semantic identifier.
No internal fields. Serves exclusively as a location key for
user-scoped profile data. Does not carry semantic content, authority,
or configuration.

### User Profile Source

Structural definition: Raw profile data container. When present,
structurally permitted to contain only elements of type Recall Object
and elements of type Calibration Signal Aggregate — no other content
categories are permitted. Any content not belonging to these two
categories constitutes semantic contamination. When null, the stage
produces an empty Loaded Profile via safe-default path.

Permitted element types:
- Recall Object (zero or more)
- Calibration Signal Aggregate (zero or more)

Violation category:
- Semantic content: any content not classifiable as a Recall Object
  or Calibration Signal Aggregate. Presence triggers HALT.

### Loaded Profile

Structural definition: Validated profile output. Contains only
elements that have passed the purity constraint declared on
User Profile Source. Structurally empty (zero Recall Objects, zero
Calibration Signal Aggregates) is valid — this is the output
produced when User Profile Source is null or when the user has no
prior continuity data.

Contains:
- Recall Objects: zero or more
- Calibration Signal Aggregates: zero or more

### Recall Object

Structural definition: Metadata-indexed reference to a Curated
Artifact. User-scoped. Contains no artifact logic — only routing
information needed to locate, evaluate, and select an artifact.
Indexed by three dimensions:
- input_class (non-semantic classification)
- constraint_set (governance constraint profile)
- effectiveness_signal (non-semantic observable indicator)

### Calibration Signal Aggregate

Structural definition: Aggregated non-semantic feedback indicators
accumulated across prior sessions and attached as metadata to Recall
Objects. Encodes observable, bounded properties only:
- input class frequency
- artifact activation count
- routing path outcomes

Does not encode meaning, truth, or belief. Persists only in
attached form on Recall Objects — not as independent state.

---

## 5. Carried-Forward Invariants

| Invariant | Statement | Source |
|-----------|-----------|--------|
| G2 — Non-semantic profile purity | User profiles contain only non-semantic data. No stage writes semantic content into a user profile. | LOGOS_DR_AC_Invariant_Specification.md — G2 |
| Stage 2 Post-Invariant: profile contents | Profile contains only Recall Objects and Calibration Signal aggregates. No semantic content exists in the loaded profile. | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |
| Stage 2 Post-Invariant: safe default | If profile is missing or unreadable, pipeline continues with an empty profile. This is the safe default, not a failure. | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |

---

## 6. Explicit Non-Capabilities

The profile_loader type and its subordinate types:

- Do NOT write to the user profile or modify any profile data
- Do NOT treat any profile content as truth, axiom, or belief
- Do NOT query governance or Safety_Gates
- Do NOT produce output other than Loaded Profile
- Do NOT continue execution when semantic content is detected in profile
- Do NOT modify, score, rank, or persist Recall Objects or Calibration Signal Aggregates
- Do NOT carry authority of any kind
- Do NOT provide fallback or degraded output on semantic contamination

---

## 7. Traceability Table

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|
| user_identifier (field) | TRACE | Direct declaration as Stage 2 input | LOGOS_DR_AC_Design_Specification.md — Stage 2, Input |
| User Identifier (subordinate type) | DERIVE | Phase 2 declares input as "User identifier (scoped, non-semantic)" but does not specify internal structure. Defined as opaque location key per declaration. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 2, Input |
| user_profile_source (field) | DERIVE | Phase 2 declares "The user profile is loaded" and "If the profile is missing or unreadable, the pipeline continues with an empty profile." Structurally representing the raw source as a nullable input is required to model the safe-default path. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 2, Description; Stage 2, Boundary |
| User Profile Source (subordinate type) | TRACE | Permitted-content constraint and violation category derived directly from Phase 2 boundary declaration and Phase 3 purity gate definition | LOGOS_DR_AC_Design_Specification.md — Stage 2, Boundary; LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |
| loaded_profile (field) | TRACE | Direct declaration as Stage 2 output | LOGOS_DR_AC_Design_Specification.md — Stage 2, Output |
| Loaded Profile (subordinate type) | TRACE | Structurally defined by Phase 2 output declaration and Phase 3 post-invariants: contains only Recall Objects and Calibration Signal aggregates; empty is valid | LOGOS_DR_AC_Design_Specification.md — Stage 2, Output; LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |
| Recall Object (subordinate type) | TRACE | Defined in Phase 2 as a core conceptual object; structure declared in Section 1.3 | LOGOS_DR_AC_Design_Specification.md — Section 1.3 |
| Calibration Signal Aggregate (subordinate type) | TRACE | Defined in Phase 2 as a core conceptual object; structure declared in Section 1.4 | LOGOS_DR_AC_Design_Specification.md — Section 1.4 |
| G2 carry-forward | TRACE | G2 explicitly enforced at Stage 2 per Phase 3 formalization | LOGOS_DR_AC_Invariant_Specification.md — G2; PHASES_1_3_AUDITS.md — Stage 2 |
| Stage 2 Post-Invariant: profile contents | TRACE | Direct declaration in Invariant Specification | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |
| Stage 2 Post-Invariant: safe default | TRACE | Direct declaration in Invariant Specification | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 Post-Invariants |
| Non-capability: no writes | TRACE | Authority declared as None (read-only) in Phase 3 formalization | PHASES_1_3_AUDITS.md — Stage 2 |
| Non-capability: no truth treatment | TRACE | Phase 2 boundary + Phase 3 HALT semantics: semantic content is governance violation | LOGOS_DR_AC_Design_Specification.md — Stage 2, Boundary; LOGOS_DR_AC_Invariant_Specification.md — Stage 2 HALT Semantics |
| Non-capability: no governance querying | TRACE | Explicitly stated in Phase 3 formalization | PHASES_1_3_AUDITS.md — Stage 2 |
| Non-capability: no continuation on semantic contamination | TRACE | HALT semantics are terminal; forbidden to continue with semantic content | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 HALT Semantics |
| Non-capability: no modification of Recall Objects or Calibration Signals | TRACE | Authority declared as None (read-only); no write capability | PHASES_1_3_AUDITS.md — Stage 2 |
| Non-capability: no fallback on contamination | TRACE | HALT is terminal; no fallback or degraded continuation permitted | LOGOS_DR_AC_Invariant_Specification.md — Stage 2 HALT Semantics |

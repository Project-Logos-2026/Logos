# STAGE_1_SESSION_INIT_TYPE_SCHEMA.md
Stage: session_init
Status: DESIGN-ONLY | NON-EXECUTABLE
Artifact Class: Type Schema (A5)
Supersedes: Prior ungrounded session_init Type Schema (discarded)
Grounding: PHASE_4_GROUNDING_RULE.md compliant

---

## Semantic Synopsis (GPT Handoff)

This is the Phase 4 Type Schema for session_init (Stage 1). It defines
the input type (Session Trigger), the output type (Clean Session State),
and the subordinate type (Residual State Surface) that structurally
defines what "clean" means. All fields and types are grounded in Phase 2
(LOGOS_DR_AC_Design_Specification.md) and Phase 3 (session_init
formalization / LOGOS_DR_AC_Invariant_Specification.md). No fields are
invented; one subordinate type is a Phase 4 derivation, explicitly
labeled and justified. It belongs to the Orchestration layer. It
respects G1 (Ephemerality). GPT should treat this as a standalone type
definition ready for coupling to Phase 4 Interface Contract completion
and Realization Constraints for Stage 1.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Component Name | session_init |
| Stage Number | 1 |
| Pipeline Role | Anti-contamination entry gate; pipeline entry point |
| Primary Function | Detect and reject residual state; produce clean session state |

---

## 2. Structural Fields

### Required Fields

- session_trigger [INPUT]
  Type: Session Trigger
  Description: The event that initiates the DR–AC pipeline. Serves as
  the invocation signal. Contains no semantic payload.

- clean_session_state [OUTPUT]
  Type: Clean Session State
  Description: The confirmed absence of all residual state categories.
  Produced only when residual check passes. Structurally empty by
  definition.

### Optional Fields

None. No optional fields are declared or justified by Phase 2/3
source material.

---

## 3. Nullability Rules

| Field | Nullability | Rationale |
|-------|-------------|-----------|
| session_trigger | NON-NULL | Pipeline cannot begin without an invocation signal |
| clean_session_state | NON-NULL | Output is either produced (clean) or the stage HALTs; no intermediate state is valid |

---

## 4. Subordinate Type Definitions

### Session Trigger

Structural definition: Opaque event marker. No internal fields.
Signals pipeline invocation only. Does not carry data, configuration,
or identity. Its presence is the sole input to session_init.

### Clean Session State

Structural definition: The confirmed absence of all categories
enumerated in Residual State Surface. This type has no fields. Its
structure is defined entirely by what it excludes. A Clean Session
State object exists if and only if every category in Residual State
Surface has been verified absent.

### Residual State Surface

Structural definition: The enumerated set of state categories that
must all be verified absent before Clean Session State can be declared.
Derived directly from Phase 2 and Phase 3 declarations of what
constitutes residual state.

Categories:

- compiled_surface: Any active Session-Ephemeral Compilation
  persisting from a prior session.

- active_bindings: Any live stage bindings persisting from a prior
  session.

- prior_session_residual: Any other carried state from a prior session
  not covered by the above categories.

All three categories must be absent. Presence of any one triggers HALT.
Failure semantics are covered by Phase 3 Interface Contract
carry-forward; they are not re-authored here.

---

## 5. Carried-Forward Invariants

| Invariant | Statement | Source |
|-----------|-----------|--------|
| G1 — Ephemerality | Enforced at session boundary. No state from prior sessions may persist into the new session. | LOGOS_DR_AC_Invariant_Specification.md — G1; Phase 3 session_init formalization |
| Stage 1 Post-Invariant | Session state is clean: no compiled surface, no active bindings, no residual from any prior session. | LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |

---

## 6. Explicit Non-Capabilities

The session_init type and its subordinate types:

- Do NOT authorize execution of any kind
- Do NOT carry mutable state
- Do NOT produce identity, metadata, or configuration
- Do NOT persist beyond the session boundary
- Do NOT perform governance querying, user-data access, or writes
- Do NOT provide fallback or degraded-state output

---

## 7. Traceability Table

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|
| session_trigger (field) | TRACE | Direct declaration as Stage 1 input | LOGOS_DR_AC_Design_Specification.md — Stage 1, Input |
| Session Trigger (subordinate type) | DERIVE | Phase 2 declares the input as "session trigger (new session event)" but does not specify internal structure. Defined as opaque event marker per pipeline role. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 1, Input |
| clean_session_state (field) | TRACE | Direct declaration as Stage 1 output | LOGOS_DR_AC_Design_Specification.md — Stage 1, Output |
| Clean Session State (subordinate type) | TRACE | Structurally defined by Phase 2 and Phase 3 as the absence of residual state | LOGOS_DR_AC_Design_Specification.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| Residual State Surface (subordinate type) | TRACE | Categories derived directly from Phase 2/3 declarations of what constitutes non-clean state | LOGOS_DR_AC_Design_Specification.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| compiled_surface (category) | TRACE | Explicitly named in Phase 2 and Phase 3 as a residual state category | LOGOS_DR_AC_Design_Specification.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| active_bindings (category) | TRACE | Explicitly named in Phase 2 and Phase 3 as a residual state category | LOGOS_DR_AC_Design_Specification.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| prior_session_residual (category) | TRACE | Explicitly named in Phase 2 and Phase 3 as a residual state category | LOGOS_DR_AC_Design_Specification.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| G1 carry-forward | TRACE | G1 explicitly enforced at Stage 1 per Phase 3 formalization | PHASES_1_3_AUDITS.md — Stage 1; LOGOS_DR_AC_Invariant_Specification.md — G1 |
| Stage 1 Post-Invariant carry-forward | TRACE | Direct declaration in Invariant Specification | LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| Non-capability: no execution authority | TRACE | Authority declared as None in Phase 3 formalization | PHASES_1_3_AUDITS.md — Stage 1 |
| Non-capability: no mutable state | TRACE | Post-invariant requires clean (empty) state | LOGOS_DR_AC_Invariant_Specification.md — Stage 1 Post-Invariants |
| Non-capability: no identity/metadata | DERIVE | Stage 1 output is clean state only; no identity or metadata output is declared in Phase 2/3. This non-capability is a Phase 4 derivation from the absence of any such declaration. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 1 |
| Non-capability: no persistence | TRACE | G1 Ephemerality enforced at session boundary | LOGOS_DR_AC_Invariant_Specification.md — G1 |
| Non-capability: no governance querying | TRACE | Explicitly stated in Phase 3 formalization | PHASES_1_3_AUDITS.md — Stage 1 |
| Non-capability: no fallback output | TRACE | HALT semantics are terminal; no fallback permitted | LOGOS_DR_AC_Invariant_Specification.md — Stage 1 HALT Semantics |

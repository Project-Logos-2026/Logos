# CROSS_STAGE_BINDING_MAP.md
Status: CANONICAL | DESIGN-ONLY
Authority: None (Specification Only)
Execution: STRICTLY FORBIDDEN
Phase: Phase 4 Closure Artifact
Scope: Defines type bindings between DR–AC pipeline stages

---

## Semantic Synopsis (GPT Handoff)

This artifact explicitly defines how Stage outputs bind to downstream
Stage inputs throughout the DR–AC pipeline. It eliminates interpretive
gaps between Type Schemas by declaring exact type-to-type mappings at
each stage transition. No new types are introduced. All bindings trace
directly to existing Phase 4 Type Schemas. GPT should treat this as the
authoritative reference for inter-stage type flow.

---

## 1. Purpose

This document defines the complete set of type bindings between DR–AC
pipeline stages. For each stage transition (1→2, 2→3, 3→4, 4→5, 5→6,
6→8), it specifies:
- Which output types from the producer stage bind to which input types
  in the consumer stage
- The exact type names as defined in Phase 4 Type Schemas
- Directionality (producer → consumer)
- Explicit non-bindings (what is NOT passed forward)

Stage 7 (MTP / Interface_Layer handoff) is explicitly excluded — it is
owned by existing infrastructure outside DR–AC scope.

---

## 2. Binding Notation

Each binding is declared using the following structure:

**Producer Stage [STAGE_N] → Consumer Stage [STAGE_M]**
- Producer Output Type → Consumer Input Type
- Non-Bindings: (types that do NOT flow forward)

Type names are exact matches to Phase 4 Type Schema definitions.

---

## 3. Stage 1 → Stage 2 Binding

**Producer: session_init [STAGE_1]**
**Consumer: profile_loader [STAGE_2]**

### Bindings
- Clean Session State → (implicit precondition; Stage 2 requires clean
  state but does not receive it as an explicit input type)

### Non-Bindings
- Session Trigger (consumed by Stage 1; not passed forward)

### Notes
Stage 1's output is a postcondition (clean session state confirmed) rather
than a typed data object. Stage 2 depends on this postcondition being
satisfied but does not receive Clean Session State as an input field.

---

## 4. Stage 2 → Stage 3 Binding

**Producer: profile_loader [STAGE_2]**
**Consumer: baseline_assembler [STAGE_3]**

### Bindings
- Loaded Profile → (held in pipeline context; not a direct Stage 3 input,
  but required for Stage 5)

### Non-Bindings
- User Identifier (consumed by Stage 2; not passed forward)
- User Profile Source (consumed by Stage 2; not passed forward)

### Notes
Stage 2's primary output (Loaded Profile) is not a direct input to Stage 3.
It is held in pipeline context and consumed by Stage 5 (reuse_decision).
Stage 3 operates independently of user-specific data.

---

## 5. Stage 3 → Stage 4 Binding

**Producer: baseline_assembler [STAGE_3]**
**Consumer: artifact_overlay [STAGE_4]**

### Bindings
- Validated Baseline → validated_baseline [INPUT]

### Non-Bindings
- Canonical Primitive Set (internal to Stage 3; not passed as a distinct
  object; its contents are embedded in Validated Baseline)
- Governance Validation Result (consumed by Stage 3; not passed forward)

### Notes
Stage 4 receives the Validated Baseline, which contains the governance-
validated Canonical Primitives. The baseline is passed unmodified.

---

## 6. Stage 4 → Stage 5 Binding

**Producer: artifact_overlay [STAGE_4]**
**Consumer: reuse_decision [STAGE_5]**

### Bindings
- Overlaid Surface → overlaid_surface [INPUT]

### Additional Inputs to Stage 5 (Not from Stage 4)
- Loaded Profile (from Stage 2; held in pipeline context)
  → Provides Recall Index for Stage 5
- Current Input (from pipeline entry)
  → current_input [INPUT]

### Non-Bindings
- Validated Baseline (passed through Stage 4 unmodified; becomes input
  to Stage 6, not Stage 5)

### Notes
Stage 5 receives the Overlaid Surface from Stage 4. It also receives
the Recall Index (derived from Stage 2's Loaded Profile) and the
Current Input (from pipeline entry). Stage 5 does not receive the
Validated Baseline directly.

---

## 7. Stage 5 → Stage 6 Binding

**Producer: reuse_decision [STAGE_5]**
**Consumer: compilation [STAGE_6]**

### Bindings
- Decision Result → decision_result [INPUT]

### Additional Inputs to Stage 6 (Not from Stage 5)
- Validated Baseline (from Stage 3; held in pipeline context)
  → validated_baseline [INPUT]
- Overlaid Surface (from Stage 4; held in pipeline context)
  → overlaid_surface [INPUT]

### Non-Bindings
- Current Input (consumed by Stage 5; not passed to Stage 6)
- Recall Index (queried by Stage 5; not passed to Stage 6)
- Constraint Set (queried by Stage 5; not passed to Stage 6)

### Notes
Stage 6 is the convergence point. It receives:
- Decision Result from Stage 5
- Validated Baseline from Stage 3 (held in pipeline context)
- Overlaid Surface from Stage 4 (held in pipeline context)

These three inputs are assembled into the Session-Ephemeral Compilation.

---

## 8. Stage 6 → Stage 7 Binding (Out of Scope)

**Producer: compilation [STAGE_6]**
**Consumer: MTP / Interface_Layer [STAGE_7]**

### Status
Stage 7 is owned by existing infrastructure outside DR–AC scope.
The binding contract is Boundary B (Output Delivery Handoff).
This binding is NOT defined in this document.

### What is Known
- Stage 6 produces: Session-Ephemeral Compilation
- Stage 7 receives: (external contract; not specified here)
- Stage 7 produces: delivered output to user

See BOUNDARY_CONTRACT_B.md for the formal boundary specification.

---

## 9. Stage 6 → Stage 8 Binding (Conditional)

**Producer: compilation [STAGE_6]**
**Consumer: artifact_cataloger [STAGE_8]**

### Conditional Execution
Stage 8 executes ONLY if:
- Stage 5 Decision Outcome was ADAPT or GENERATE-NEW
- Stage 7 (output delivery) is complete

If Stage 5 Decision Outcome was REUSE, Stage 8 does not execute.

### Bindings (When Stage 8 Executes)
- Artifact Candidate (extracted from Session-Ephemeral Compilation)
  → artifact_candidate [INPUT]

### Additional Inputs to Stage 8 (Not from Stage 6)
- Decision Result (from Stage 5; held in pipeline context)
  → stage_5_decision [INPUT] (precondition check only)
- Calibration Signal Aggregate (accumulated during session)
  → calibration_aggregate [INPUT]

### Non-Bindings
- Session-Ephemeral Compilation (not passed in its entirety; only the
  Artifact Candidate component is extracted and submitted to Stage 8)

### Notes
Stage 8 does not receive the full Session-Ephemeral Compilation. It
receives the Artifact Candidate — the specific artifact produced by
Stage 6 that is eligible for cataloging (new or adapted artifact only).

---

## 10. Stage 5 → Stage 8 Binding (Precondition Check)

**Producer: reuse_decision [STAGE_5]**
**Consumer: artifact_cataloger [STAGE_8]**

### Bindings
- Decision Result → stage_5_decision [INPUT]

### Purpose
Stage 8 receives the Decision Result from Stage 5 for precondition
checking only. It confirms that the Decision Outcome is ADAPT or
GENERATE-NEW before proceeding. It does not re-evaluate or modify
the decision.

### Non-Bindings
- All other Stage 5 inputs and internal state (not passed to Stage 8)

---

## 11. Pipeline Context vs Direct Bindings

Some types flow through pipeline context rather than as direct stage-to-
stage bindings:

### Types Held in Pipeline Context
- **Loaded Profile** (Stage 2 output)
  → Consumed by Stage 5
  → Not a direct input to Stages 3 or 4

- **Validated Baseline** (Stage 3 output)
  → Consumed by Stage 4 (direct)
  → Consumed by Stage 6 (held in context after Stage 4)

- **Overlaid Surface** (Stage 4 output)
  → Consumed by Stage 5 (direct)
  → Consumed by Stage 6 (held in context after Stage 5)

- **Decision Result** (Stage 5 output)
  → Consumed by Stage 6 (direct)
  → Consumed by Stage 8 (held in context after Stage 6)

### Rationale
Multi-stage dependencies require some outputs to be held in pipeline
context rather than passed in linear sequence. This is a structural
property of the pipeline, not a deviation from fail-closed semantics.

---

## 12. Summary Table

| Transition | Producer Output | Consumer Input | Direct Binding | Context Held |
|------------|-----------------|----------------|----------------|--------------|
| 1 → 2 | Clean Session State | (postcondition) | No | No |
| 2 → 3 | Loaded Profile | (none) | No | Yes (for Stage 5) |
| 3 → 4 | Validated Baseline | validated_baseline | Yes | Yes (for Stage 6) |
| 4 → 5 | Overlaid Surface | overlaid_surface | Yes | Yes (for Stage 6) |
| 5 → 6 | Decision Result | decision_result | Yes | Yes (for Stage 8) |
| 6 → 7 | Session-Ephemeral Compilation | (external) | — | — |
| 6 → 8 | Artifact Candidate | artifact_candidate | Yes | No |
| 5 → 8 | Decision Result | stage_5_decision | Yes | (already held) |

---

## 13. Non-Introduced Types

This document introduces NO new types.
All type names reference existing Phase 4 Type Schema definitions.

---

## 14. Closing Declaration

This document defines the complete set of type bindings between DR–AC
pipeline stages. All bindings trace to Phase 4 Type Schemas. No gaps
remain.

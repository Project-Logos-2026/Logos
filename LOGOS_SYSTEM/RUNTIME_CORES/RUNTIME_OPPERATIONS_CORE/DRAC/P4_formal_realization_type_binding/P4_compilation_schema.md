# STAGE_6_COMPILATION_TYPE_SCHEMA.md
Stage: compilation
Status: DESIGN-ONLY | NON-EXECUTABLE
Artifact Class: Type Schema (A5)
Grounding: PHASE_4_GROUNDING_RULE.md compliant

---

## Semantic Synopsis (GPT Handoff)

This is the Phase 4 Type Schema for compilation (Stage 6). It is the
pipeline's convergence point and the location of the anti-hallucination
boundary. It defines three inputs — Validated Baseline (forward-referenced
to Stage 3), Overlaid Surface (forward-referenced to Stage 4), and Decision
Result (forward-referenced to Stage 5) — and one output: Session-Ephemeral
Compilation. The schema's primary structural feature is the Assembly Case
type: a three-case enumerated structure (REUSE, ADAPT, GENERATE-NEW) that
determines the assembly mode and its output properties. Each case is
structurally distinct in what it produces and what downstream effects it
carries. The semantic traceability constraint is represented as a structural
property on the output type — every element of the Session-Ephemeral
Compilation must be traceable to either the Validated Baseline or an
individually validated Curated Artifact from the Overlaid Surface.
Violation of this constraint constitutes untraceable semantic content and
triggers HALT. This is the strongest safety property in the DR–AC pipeline
(anti-hallucination gate). Authority is None (read-only; assembly-only).
Two elements are Phase 4 derivations (Assembly Case as a composite type
encoding the decision-to-assembly mapping, and the Traceability Constraint
as a structural property on the output). All other elements trace directly
to Phase 2/3 declarations. GPT should treat this as ready for Interface
Contract completion coupling and Realization Constraints for Stage 6.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Component Name | compilation |
| Stage Number | 6 |
| Pipeline Role | Convergence point; anti-hallucination gate |
| Primary Function | Assemble Session-Ephemeral Compilation from baseline, overlay, and decision outcome; enforce semantic traceability; produce compilation or HALT |
| Authority | None (read-only; assembly-only) |

---

## 2. Structural Fields

### Required Fields

- validated_baseline [INPUT]
  Type: Validated Baseline
  Description: The governance-validated baseline from Stage 3. Provides
  the deterministic foundation into which all assembly cases operate.
  Received unmodified.

  Forward Reference: Validated Baseline
  Definition artifact: STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md
  Expected phase: Phase 4

- overlaid_surface [INPUT]
  Type: Overlaid Surface
  Description: The baseline-plus-overlay output from Stage 4. Provides
  the complete set of individually validated Curated Artifacts eligible
  for binding or adaptation. Defines the traceable artifact boundary —
  only content from this surface or the baseline may appear in the output.

  Forward Reference: Overlaid Surface
  Definition artifact: STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md
  Expected phase: Phase 4

- decision_result [INPUT]
  Type: Decision Result
  Description: The single decision output from Stage 5. Determines the
  assembly case. Contains a Decision Outcome (REUSE, ADAPT, or
  GENERATE-NEW) and a conditional Artifact Pointer (present for REUSE
  and ADAPT; absent for GENERATE-NEW). Stage 6 does not re-evaluate
  the decision — it receives it and assembles accordingly.

  Forward Reference: Decision Result
  Definition artifact: STAGE_5_REUSE_DECISION_TYPE_SCHEMA.md
  Expected phase: Phase 4

- session_ephemeral_compilation [OUTPUT]
  Type: Session-Ephemeral Compilation
  Description: The fully assembled runtime surface for this session.
  Structurally complete, internally consistent, and semantically
  traceable. Never persisted — exists only for the duration of the
  session. Produced only when all three HALT conditions are absent.
  Failure semantics are covered by Phase 3 Interface Contract
  carry-forward.

### Optional Fields

None. No optional fields are declared or justified by Phase 2/3
source material.

---

## 3. Nullability Rules

| Field | Nullability | Rationale |
|-------|-------------|-----------|
| validated_baseline | NON-NULL | Assembly requires the baseline as foundation |
| overlaid_surface | NON-NULL | Received from Stage 4; defines the traceable artifact boundary |
| decision_result | NON-NULL | Assembly case is determined by the decision; cannot proceed without it |
| session_ephemeral_compilation | NON-NULL | Output is either produced (all checks pass) or the stage HALTs; no partial compilation is valid |

---

## 4. Subordinate Type Definitions

### Validated Baseline

Forward Reference: Validated Baseline
Definition artifact: STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Received as input; provides the deterministic
foundation for all assembly cases.

### Overlaid Surface

Forward Reference: Overlaid Surface
Definition artifact: STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Received as input; defines the set of traceable
Curated Artifacts available for binding or adaptation.

### Decision Result

Forward Reference: Decision Result
Definition artifact: STAGE_5_REUSE_DECISION_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Received as input; determines which Assembly Case
applies.

### Assembly Case

Structural definition: A three-case enumerated type that maps the
Decision Outcome to specific assembly behavior and output properties.
Exactly one case applies per invocation, determined by the Decision
Outcome in the received Decision Result. Each case is structurally
distinct in what it contributes to the Session-Ephemeral Compilation
and what downstream effects it carries.

Cases:

- REUSE
  Applies when: Decision Outcome is REUSE.
  Assembly behavior: The artifact referenced by the Artifact Pointer
  is bound into the compilation unmodified. No copy is produced. No
  modification occurs.
  Downstream effect: Stage 8 does not execute. The bound artifact
  already exists in persisted form.
  Output contribution: Validated Baseline + the referenced artifact,
  bound unmodified.

- ADAPT
  Applies when: Decision Outcome is ADAPT.
  Assembly behavior: A distinct copy of the artifact referenced by
  the Artifact Pointer is produced. Surface-level modifications are
  applied to the copy. The source artifact is not modified. The
  modification is limited to expression parameters or routing — not
  to semantic content or invariant profile.
  Downstream effect: Stage 8 executes post-delivery; the adapted
  copy is subject to cataloging.
  Output contribution: Validated Baseline + the adapted copy (a new,
  independent artifact).

- GENERATE-NEW
  Applies when: Decision Outcome is GENERATE-NEW.
  Assembly behavior: A new artifact is produced from the current
  baseline and input. No existing artifact is referenced or modified.
  Downstream effect: Stage 8 executes post-delivery; the new artifact
  is subject to cataloging.
  Output contribution: Validated Baseline + the new artifact.

### Session-Ephemeral Compilation

Structural definition: The fully assembled runtime surface for this
session. Composed from the Validated Baseline and the output of the
applicable Assembly Case. Exists only for the duration of the session
— never persisted directly. Discarded at session end.

Structural constraints:
- Structurally complete: all components required by the Assembly Case
  are present
- Internally consistent: no internal contradictions between components
- Semantically traceable: every element of semantic content is traceable
  to either the Validated Baseline or a Curated Artifact present in the
  Overlaid Surface (Traceability Constraint — see below)

Contains:
- Validated Baseline content (unmodified)
- Assembly Case output (one of: bound artifact, adapted copy, or
  new artifact)

### Traceability Constraint

Structural definition: The semantic content boundary enforced on the
Session-Ephemeral Compilation. This is the anti-hallucination gate
of the DR–AC pipeline.

Rule: Every element of semantic content in the Session-Ephemeral
Compilation must be traceable to one of two sources:
- The Validated Baseline, OR
- A Curated Artifact individually validated and present in the
  Overlaid Surface

Violation: Any semantic content that cannot be traced to either source
constitutes untraceable semantic content. This triggers HALT.

This constraint applies uniformly across all three Assembly Cases.
It does not matter whether the content originates from a bound
artifact, an adapted copy, or a newly produced artifact — the
traceability requirement is absolute.

---

## 5. Carried-Forward Invariants

| Invariant | Statement | Source |
|-----------|-----------|--------|
| G1 — Ephemerality | Session-Ephemeral Compilation is never persisted directly. Only artifacts that pass through Stage 8's mutation gate persist. | LOGOS_DR_AC_Invariant_Specification.md — G1 |
| G4 — Canonical Primitive immutability | No Canonical Primitive within the baseline is written, overwritten, or shadowed by any assembly operation. | LOGOS_DR_AC_Invariant_Specification.md — G4 |
| Semantic traceability (anti-hallucination) | All semantic content in the compilation is traceable to baseline or validated artifacts. Untraceable content triggers HALT. This is the strongest safety property in the DR–AC formalization set. | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants; PHASES_1_3_AUDITS.md — Stage 6; Section 4.D |
| Structural completeness | Session-Ephemeral Compilation is structurally complete. Incompleteness triggers HALT. | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| Internal consistency | Compilation is internally consistent. Internal inconsistency triggers HALT. | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| ADAPT produces distinct copy | If Assembly Case is ADAPT, the output is a distinct copy. The source artifact referenced by the Artifact Pointer is unmodified. | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants |
| Three-case separation | The three assembly cases are explicitly and structurally separated. No case bleeds into another. | PHASES_1_3_AUDITS.md — Stage 6; LOGOS_DR_AC_Design_Specification.md — Stage 6 |

---

## 6. Explicit Non-Capabilities

The compilation type and its subordinate types:

- Do NOT hold write authority of any kind
- Do NOT persist the Session-Ephemeral Compilation or any component of it
- Do NOT modify the Validated Baseline or any Canonical Primitive within it
- Do NOT modify the source artifact on ADAPT (produces distinct copy only)
- Do NOT introduce semantic content not traceable to baseline or validated artifacts
- Do NOT continue when compilation is structurally incomplete
- Do NOT continue when compilation is internally inconsistent
- Do NOT continue when untraceable semantic content is detected
- Do NOT re-evaluate or override the Decision Result from Stage 5
- Do NOT produce more than one compilation per invocation
- Do NOT access observability or audit domain data (G8)

---

## 7. Traceability Table

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|
| validated_baseline (field) | TRACE | Direct declaration as Stage 6 input ("Baseline") | LOGOS_DR_AC_Design_Specification.md — Stage 6, Input |
| Validated Baseline (forward ref) | TRACE | Defined in Stage 3 Type Schema; received as input | STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md — Section 4 |
| overlaid_surface (field) | TRACE | Direct declaration as Stage 6 input ("overlay") | LOGOS_DR_AC_Design_Specification.md — Stage 6, Input |
| Overlaid Surface (forward ref) | TRACE | Defined in Stage 4 Type Schema; received as input | STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md — Section 4 |
| decision_result (field) | TRACE | Direct declaration as Stage 6 input ("Stage 5 decision outcome") | LOGOS_DR_AC_Design_Specification.md — Stage 6, Input |
| Decision Result (forward ref) | TRACE | Defined in Stage 5 Type Schema; received as input | STAGE_5_REUSE_DECISION_TYPE_SCHEMA.md — Section 4 |
| session_ephemeral_compilation (field) | TRACE | Direct declaration as Stage 6 output | LOGOS_DR_AC_Design_Specification.md — Stage 6, Output |
| Session-Ephemeral Compilation (subordinate type) | TRACE | Defined in Phase 2 as a core conceptual object (Section 1.5); properties declared in Phase 3 post-invariants | LOGOS_DR_AC_Design_Specification.md — Section 1.5; LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants |
| Assembly Case (subordinate type) | DERIVE | Phase 2 and Phase 3 declare three explicitly separated assembly behaviors driven by the Stage 5 decision. Composing them into a single enumerated type that maps decision outcome to assembly behavior and output properties is required to represent the three-case structure as a typed design artifact. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 6; PHASES_1_3_AUDITS.md — Stage 6 |
| REUSE case | TRACE | Explicitly declared: bind artifact unmodified; Stage 8 does not run | LOGOS_DR_AC_Design_Specification.md — Stage 6; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| ADAPT case | TRACE | Explicitly declared: distinct copy, surface-only modification, source unmodified, Stage 8 catalogs copy | LOGOS_DR_AC_Design_Specification.md — Stage 6; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5; LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants |
| GENERATE-NEW case | TRACE | Explicitly declared: new artifact from baseline and input; Stage 8 catalogs it | LOGOS_DR_AC_Design_Specification.md — Stage 6; LOGOS_DR_AC_reuse_decision_Formalization.md — Section 5 |
| Traceability Constraint (subordinate type) | DERIVE | Phase 2 declares the traceability invariant ("must not introduce semantic content not present in baseline or validated artifacts") and Phase 3 declares HALT on untraceable content. Representing this as a structural constraint type on the output is required to model the anti-hallucination gate without execution semantics. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 6, Boundary; LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants; Stage 6 HALT Semantics |
| G1 carry-forward | TRACE | Compilation is ephemeral; never persisted directly | LOGOS_DR_AC_Invariant_Specification.md — G1 |
| G4 carry-forward | TRACE | Canonical Primitives unmodified through assembly | LOGOS_DR_AC_Invariant_Specification.md — G4 |
| Anti-hallucination gate | TRACE | Stage 6 Condition C: untraceable semantic content ⇒ HALT — explicitly declared as the strongest safety property | PHASES_1_3_AUDITS.md — Stage 6; Section 4.D; LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| Structural completeness HALT | TRACE | Explicitly declared as HALT trigger | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| Internal consistency HALT | TRACE | Explicitly declared as HALT trigger | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| ADAPT distinct copy | TRACE | Explicitly declared in post-invariants: adaptation is a distinct copy; source unmodified | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants |
| Three-case separation | TRACE | Explicitly declared: "Three-case assembly explicitly separated" | PHASES_1_3_AUDITS.md — Stage 6 |
| Non-capability: no writes | TRACE | Authority declared as None (read-only; assembly-only) | PHASES_1_3_AUDITS.md — Stage 6 |
| Non-capability: no persistence | TRACE | G1 — ephemeral; never persisted | LOGOS_DR_AC_Invariant_Specification.md — G1 |
| Non-capability: no baseline modification | TRACE | G4 — Canonical Primitive immutability | LOGOS_DR_AC_Invariant_Specification.md — G4 |
| Non-capability: no source modification on ADAPT | TRACE | Post-invariant: source unmodified; distinct copy produced | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 Post-Invariants |
| Non-capability: no untraceable content | TRACE | Anti-hallucination gate — HALT on violation | LOGOS_DR_AC_Invariant_Specification.md — Stage 6 HALT Semantics |
| Non-capability: no decision override | TRACE | Stage 6 receives and assembles per decision; does not re-evaluate | LOGOS_DR_AC_Design_Specification.md — Stage 6 |
| Non-capability: no audit domain access | TRACE | G8 | LOGOS_DR_AC_Invariant_Specification.md — G8 |

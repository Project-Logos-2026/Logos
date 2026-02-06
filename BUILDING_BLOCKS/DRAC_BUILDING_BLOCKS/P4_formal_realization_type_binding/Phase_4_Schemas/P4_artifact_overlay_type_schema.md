# STAGE_4_ARTIFACT_OVERLAY_TYPE_SCHEMA.md
Stage: artifact_overlay
Status: DESIGN-ONLY | NON-EXECUTABLE
Artifact Class: Type Schema (A5)
Grounding: PHASE_4_GROUNDING_RULE.md compliant

---

## Semantic Synopsis (GPT Handoff)

This is the Phase 4 Type Schema for artifact_overlay (Stage 4). It is the
first stage where user-specific variation enters the pipeline. It defines
two inputs: Validated Baseline (forward-referenced to Stage 3) and Recall
Objects (forward-referenced to Stage 2), which structurally locate the
Curated Artifacts eligible for overlay. The output is Overlaid Surface —
the baseline with zero or more validated Curated Artifacts additively
layered on top. The schema's structural complexity centers on two
constraints: (1) additive-only overlay — the baseline is never modified,
overwritten, or shadowed, and (2) per-artifact governance validation,
scoped narrower than Stage 3. Stage 4 validates against only two targets
(Denial_Invariants, Design_Only_Declarations); Phase_Definitions is
explicitly excluded because it is a session-level gate handled at Stage 3.
Empty Recall Object set is a valid safe default. HALT occurs only when
candidates existed and all individually failed validation. Two elements
are Phase 4 derivations (Recall Object Set as a collection type, and
Per-Artifact Validation Scope as a structural representation of per-artifact
governance per design-only posture). All other elements trace to Phase 2/3.
GPT should treat this as ready for Interface Contract completion coupling
and Realization Constraints for Stage 4.

---

## 1. Identity

| Field | Value |
|-------|-------|
| Component Name | artifact_overlay |
| Stage Number | 4 |
| Pipeline Role | First lawful point of user-specific variation; additive overlay |
| Primary Function | Overlay user-specific Curated Artifacts onto baseline via per-artifact governance validation; produce Overlaid Surface or HALT |

---

## 2. Structural Fields

### Required Fields

- validated_baseline [INPUT]
  Type: Validated Baseline
  Description: The governance-validated baseline received from Stage 3.
  Passed through unmodified into the Overlaid Surface. No baseline
  content may be overwritten or shadowed by overlay artifacts. No
  re-validation occurs at this stage.

  Forward Reference: Validated Baseline
  Definition artifact: STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md
  Expected phase: Phase 4

- recall_objects [INPUT]
  Type: Recall Object Set
  Description: The set of Recall Objects loaded via Stage 2. Each Recall
  Object structurally locates one Curated Artifact eligible for overlay
  consideration. The set may be structurally empty (zero elements) — this
  is the safe default when the user has no prior continuity data. An empty
  set produces an Overlaid Surface containing only the Validated Baseline;
  it does not trigger HALT.

- overlaid_surface [OUTPUT]
  Type: Overlaid Surface
  Description: The baseline with zero or more validated Curated Artifacts
  additively overlaid. Produced when: (a) recall_objects is empty, or
  (b) at least one Curated Artifact located by recall_objects passes
  Per-Artifact Validation Scope. Not produced when recall_objects is
  non-empty and all located Curated Artifacts fail validation — stage
  HALTs in that case. Failure semantics are covered by Phase 3 Interface
  Contract carry-forward.

### Optional Fields

None. No optional fields are declared or justified by Phase 2/3
source material.

---

## 3. Nullability Rules

| Field | Nullability | Rationale |
|-------|-------------|-----------|
| validated_baseline | NON-NULL | Overlay operates on the baseline; received from Stage 3 |
| recall_objects | NON-NULL | The set itself must exist; empty set is structurally valid but null is not — empty and absent are distinct states |
| overlaid_surface | NON-NULL | Output is either produced (empty set or at least one PASS) or the stage HALTs; no partial or degraded output is valid |

---

## 4. Subordinate Type Definitions

### Validated Baseline

Forward Reference: Validated Baseline
Definition artifact: STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Received as input from Stage 3; passed through
unmodified into Overlaid Surface.

### Recall Object Set

Structural definition: An unordered collection of Recall Objects from
the Loaded Profile produced by Stage 2. Each element locates one
Curated Artifact eligible for overlay consideration. The set may be
structurally empty — this is the safe default, not a failure state.

Contains:
- Recall Objects (zero or more)

### Recall Object

Forward Reference: Recall Object
Definition artifact: STAGE_2_PROFILE_LOADER_TYPE_SCHEMA.md
Expected phase: Phase 4

Not redefined here. Each Recall Object structurally locates one
Curated Artifact via its indexed dimensions (input_class,
constraint_set, effectiveness_signal).

### Curated Artifact

Structural definition: A user-scoped artifact previously cataloged
via Stage 8 (artifact_cataloger). Located by a Recall Object for
overlay consideration at this stage. Contains no execution logic.
Carries only content traceable to prior baseline or Stage 4–validated
overlay operations. Subject to Per-Artifact Validation Scope before
inclusion in the Overlaid Surface.

### Per-Artifact Validation Scope

Structural definition: Declares the governance targets applicable to
each Curated Artifact at Stage 4. This is a narrower scope than Stage
3's session-level validation — two targets only.

Targets (enumerated, exhaustive for Stage 4):
- Denial_Invariants
- Design_Only_Declarations

Explicitly excluded from Stage 4 scope:
- Phase_Definitions (session-level gate; handled at Stage 3)

Resolution per artifact:
- PASS: artifact passes validation against both targets
- FAIL: artifact fails validation against either target, OR Safety_Gates
  is unreachable for either target (unreachability is treated as FAIL)

Aggregate semantics:
- If recall_objects is empty: no validation occurs; output produced
  (baseline only)
- If recall_objects is non-empty and at least one located Curated
  Artifact resolves PASS: output produced (baseline + all PASS artifacts)
- If recall_objects is non-empty and all located Curated Artifacts
  resolve FAIL: stage HALTs

Failure semantics for the HALT case are covered by Phase 3 Interface
Contract carry-forward.

### Overlaid Surface

Structural definition: The complete output of Stage 4. Contains the
Validated Baseline (unmodified, in its entirety) plus zero or more
Curated Artifacts that individually passed Per-Artifact Validation
Scope.

Structural constraints:
- Additive-only: no element of the Validated Baseline is removed,
  overwritten, or shadowed
- Each overlay artifact is independent of other overlay artifacts
- Contains no content not traceable to the Validated Baseline or to
  individually validated Curated Artifacts

Contains:
- Validated Baseline (unmodified, complete)
- Validated Overlay Artifacts (zero or more Curated Artifacts that
  passed Per-Artifact Validation Scope)

---

## 5. Carried-Forward Invariants

| Invariant | Statement | Source |
|-----------|-----------|--------|
| Additive-only overlay | Overlay artifacts are added on top of the baseline. No baseline content may be overwritten or shadowed. | LOGOS_DR_AC_Invariant_Specification.md — Stage 4; PHASES_1_3_AUDITS.md — Stage 4 |
| Per-artifact governance validation | Each Curated Artifact is validated independently against Denial_Invariants and Design_Only_Declarations. Phase_Definitions is excluded (session-level gate at Stage 3). | LOGOS_DR_AC_Invariant_Specification.md — Stage 4; PHASES_1_3_AUDITS.md — Stage 4 |
| Empty set is safe default | An empty Recall Object set (and therefore zero candidate Curated Artifacts) produces output (baseline only). It is not a failure condition. | LOGOS_DR_AC_Invariant_Specification.md — Stage 4 Post-Invariants; PHASES_1_3_AUDITS.md — Stage 4 |
| Failed artifacts are session-scoped | Artifacts that fail validation are skipped for this session only. Their presence in the user profile is unchanged — removal is a Stage 8 concern. | LOGOS_DR_AC_Invariant_Specification.md — Stage 4 Post-Invariants |

---

## 6. Explicit Non-Capabilities

The artifact_overlay type and its subordinate types:

- Do NOT write to any external store or persist any state
- Do NOT overwrite, shadow, or modify any content in the Validated Baseline
- Do NOT continue when candidates existed and all failed validation
- Do NOT validate at session level — validation is per-artifact only
- Do NOT validate against Phase_Definitions (explicitly excluded from Stage 4 scope)
- Do NOT interpret the semantic content of Curated Artifacts
- Do NOT remove failed artifacts from the user profile (session-scoped skip only)
- Do NOT carry authority of any kind
- Do NOT provide fallback, partial, or degraded output on all-failed condition
- Do NOT query governance independently — validation scope is represented structurally

---

## 7. Traceability Table

| Element | Grounding | Justification | Source |
|---------|-----------|---------------|--------|
| validated_baseline (field) | TRACE | Direct declaration as Stage 4 input (baseline received from Stage 3) | LOGOS_DR_AC_Design_Specification.md — Stage 4, Input |
| Validated Baseline (forward ref) | TRACE | Defined in Stage 3 Type Schema; received unmodified as Stage 4 input | STAGE_3_BASELINE_ASSEMBLER_TYPE_SCHEMA.md — Section 4 |
| recall_objects (field) | TRACE | Direct declaration as Stage 4 input ("loaded Recall Objects") | LOGOS_DR_AC_Design_Specification.md — Stage 4, Input |
| Recall Object Set (subordinate type) | DERIVE | Phase 2 declares "loaded Recall Objects" as Stage 4 input but does not define the collection-level type. Defined as the unordered set of Recall Objects from the Loaded Profile. This is a Phase 4 derivation. | LOGOS_DR_AC_Design_Specification.md — Stage 4, Input |
| Recall Object (forward ref) | TRACE | Defined in Stage 2 Type Schema; each element locates a Curated Artifact | STAGE_2_PROFILE_LOADER_TYPE_SCHEMA.md — Section 4 |
| Curated Artifact (subordinate type) | TRACE | Defined in Phase 2 as a core conceptual object; Section 1.2 | LOGOS_DR_AC_Design_Specification.md — Section 1.2 |
| Per-Artifact Validation Scope (subordinate type) | DERIVE | Phase 3 declares per-artifact governance validation with specific target scoping and aggregate semantics. Representing this as a discrete structural type is required to model the per-artifact validation function without runtime semantics. This is a Phase 4 derivation. | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Denial_Invariants (target) | TRACE | Explicitly declared as a per-artifact Safety_Gates validation target for Stage 4 | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Design_Only_Declarations (target) | TRACE | Explicitly declared as a per-artifact Safety_Gates validation target for Stage 4 | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Phase_Definitions (explicit exclusion) | TRACE | Explicitly excluded from Stage 4 scope; session-level gate handled at Stage 3 | PHASES_1_3_AUDITS.md — Stage 4 |
| Aggregate HALT semantics | TRACE | HALT only when candidates existed and all failed — explicitly declared | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 HALT Semantics |
| overlaid_surface (field) | TRACE | Direct declaration as Stage 4 output | LOGOS_DR_AC_Design_Specification.md — Stage 4, Output |
| Overlaid Surface (subordinate type) | TRACE | Additive-only constraint, composition rules, and traceability constraint declared explicitly in Phase 2 and Phase 3 | LOGOS_DR_AC_Design_Specification.md — Stage 4, Output; PHASES_1_3_AUDITS.md — Stage 4 |
| Invariant: additive-only overlay | TRACE | Cannot overwrite or shadow baseline — explicitly declared | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Invariant: per-artifact validation | TRACE | Per-artifact validation against two targets, Phase_Definitions excluded — explicitly declared | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Invariant: empty set safe default | TRACE | Empty Recall Object set produces output (baseline only); not failure — explicitly declared | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 Post-Invariants |
| Invariant: failed artifacts session-scoped | TRACE | Failed artifacts skipped for session only; profile unchanged — explicitly declared | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 Post-Invariants |
| Non-capability: no writes | TRACE | Authority declared as None (read-only; governance-queried per artifact) | PHASES_1_3_AUDITS.md — Stage 4 |
| Non-capability: no baseline modification | TRACE | Additive-only constraint; baseline passed through unmodified | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 |
| Non-capability: no session-level validation | TRACE | Validation is per-artifact; granularity explicitly declared | PHASES_1_3_AUDITS.md — Stage 4 |
| Non-capability: no Phase_Definitions validation | TRACE | Explicitly excluded; session-level gate at Stage 3 | PHASES_1_3_AUDITS.md — Stage 4 |
| Non-capability: no profile modification | TRACE | Failed artifacts remain in profile; removal is Stage 8 concern | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 Post-Invariants |
| Non-capability: no continuation on all-failed | TRACE | HALT is terminal when candidates existed and all failed | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 HALT Semantics |
| Non-capability: no fallback output | TRACE | HALT is terminal; no fallback or degraded output permitted | PHASES_1_3_AUDITS.md — Stage 4; LOGOS_DR_AC_Invariant_Specification.md — Stage 4 HALT Semantics |
| Non-capability: no independent governance querying | DERIVE | Stage 4 is declared governance-queried per artifact, but the Type Schema models validation scope structurally rather than as an active query, per Phase 4's design-only posture (A9). This is a Phase 4 derivation. | PHASE_4_BLUEPRINT_AND_CHECKLIST.md — A9; PHASES_1_3_AUDITS.md — Stage 4 |

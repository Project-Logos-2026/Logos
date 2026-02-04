# Reconstruction Pipeline — Semantic Invariants & Correctness Conditions
**LOGOS | Phase 2: Prototype | Design-Only | Non-Executable | Authoritative**

---

## 1. Per-Stage Invariant Specification

### Stage 1 — session_init

**Pre-invariants:** None. Stage 1 is the pipeline entry point; no prior state is assumed.

**Post-invariants:**
- Session state is clean: no compiled surface, no active bindings, no residual from any prior session.

**HALT semantics:**
- Trigger: residual state detected.
- Preserved: nothing. The session has not yet begun.
- Discarded: all residual state.
- Forbidden: continuation into Stage 2 under any conditions.

---

### Stage 2 — profile_loader

**Pre-invariants:**
- Stage 1 post-invariants hold (session state is clean).

**Post-invariants:**
- User profile is loaded.
- Profile contains only Recall Objects and Calibration Signal aggregates.
- No semantic content exists in the loaded profile.
- If profile is missing or unreadable: pipeline continues with an empty profile. This is the safe default, not a failure.

**HALT semantics:**
- Trigger: semantic content detected in profile.
- Preserved: clean session state from Stage 1.
- Discarded: the contaminated profile data.
- Forbidden: continuation with any semantic content from the profile; treating any profile content as truth.

---

### Stage 3 — baseline_assembler

**Pre-invariants:**
- Stage 2 post-invariants hold (profile is loaded or empty).
- Safety_Gates are reachable and queryable.

**Post-invariants:**
- Canonical Primitives are loaded unmodified.
- All required governance gates have returned PASS (Phase_Definitions, Denial_Invariants, Design_Only_Declarations).
- A validated baseline exists.
- The baseline is identical to what any other user or session would produce under the same governance context.

**HALT semantics:**
- Trigger: any governance gate returns FAIL, or Safety_Gates are unreachable.
- Preserved: clean session state, loaded or empty profile.
- Discarded: any partially assembled baseline.
- Forbidden: continuation without full governance validation; any modification to Canonical Primitives.

---

### Stage 4 — artifact_overlay

**Pre-invariants:**
- Stage 3 post-invariants hold (validated baseline exists).
- User profile with Recall Objects is available (may be empty).
- Safety_Gates are queryable for per-artifact validation.

**Post-invariants:**
- If Curated Artifacts were available for overlay: at least one has survived validation and been applied.
- Overlay is strictly additive. No Canonical Primitive has been overwritten or shadowed.
- Every overlaid artifact has been individually validated against current governance.
- Artifacts that failed validation have been skipped for this session. Their presence in the user profile is unchanged (removal is a Stage 8 concern).

**HALT semantics:**
- Trigger: Curated Artifacts were available for overlay, and all of them failed validation.
- Preserved: validated baseline, loaded profile including failed artifacts.
- Discarded: all candidate artifacts that failed validation, for this session only.
- Forbidden: overlay that overwrites or shadows any baseline content; continuation with zero valid artifacts when candidates existed.

---

### Stage 5 — reuse_decision

**Pre-invariants:**
- Stage 4 post-invariants hold (baseline + overlay available; possibly baseline-only).
- Recall index is loaded and queryable.
- Current input has been received.

**Post-invariants:**
- Input has been classified: input class is determined and unambiguous.
- Exactly one decision has been returned: REUSE, ADAPT, or GENERATE-NEW.
- If REUSE: a valid pointer to the selected artifact exists.
- Recall index has not been mutated. No scoring or ranking state has been modified.

**HALT semantics:**
- Trigger: input classification is ambiguous AND no REUSE candidate exists.
- Preserved: baseline + overlay, loaded profile, Recall index (unmutated).
- Discarded: the ambiguous input classification.
- Forbidden: proceeding with an unresolved classification; any mutation to the Recall index during the query.

---

### Stage 6 — compilation

**Pre-invariants:**
- Stage 5 post-invariants hold (decision returned, classification resolved).
- If REUSE: selected artifact pointer is valid.
- If ADAPT: source artifact is available and unmodified.
- If GENERATE-NEW: generation is authorized by the pipeline decision.

**Post-invariants:**
- Session-Ephemeral Compilation is structurally complete.
- Compilation introduces no semantic content not present in baseline or validated artifacts.
- Compilation is internally consistent.
- If ADAPT: the adaptation is a distinct copy. The source artifact is unmodified.

**HALT semantics:**
- Trigger: compilation is incomplete, internally inconsistent, or contains semantic content not traceable to baseline or validated artifacts.
- Preserved: baseline, overlay result, Stage 5 decision.
- Discarded: the incomplete or invalid compilation.
- Forbidden: proceeding to output delivery with an invalid compilation; introducing untraceable semantic content.

---

### Stage 7 — [MTP / Interface_Layer handoff]

Stage 7 is owned by existing infrastructure. The scaffolding does not define its internal invariants or HALT semantics. The following are stated from the pipeline boundary only.

**Pre-invariants (boundary):**
- Stage 6 post-invariants hold (compilation is complete and valid).

**Post-invariants (boundary):**
- Output has been delivered.
- No persistent state has been created or mutated during delivery.
- Output does not imply intent, agency, or persistence.

**HALT semantics:** Not defined by this scaffolding. Delivery failure handling belongs to MTP.

---

### Stage 8 — artifact_cataloger

Executes conditionally: only if Stage 5 returned ADAPT or GENERATE-NEW.

**Pre-invariants:**
- Stage 5 decision was ADAPT or GENERATE-NEW.
- Output delivery (Stage 7) is complete.
- Mutation gate is reachable and queryable.

**Post-invariants:**
- If mutation gate returned ALLOW: artifact is persisted with metadata attached; Recall Object is created or updated.
- If mutation gate returned REJECT: artifact is not persisted.
- Session-ephemeral state is fully discarded regardless of cataloging outcome.
- All Calibration Signals not attached to a persisted Recall Object are discarded.

**HALT semantics:**
- Stage 8 does not HALT the session. The session has already completed output delivery.
- Preserved: the delivered output (immutable at this point).
- Discarded: Session-Ephemeral Compilation, un-persisted artifacts, un-attached Calibration Signals — all discarded whether cataloging succeeds or fails.
- Forbidden: persisting any object without passing mutation gate; persisting session-ephemeral state directly.

---

## 2. Global Invariants

Must hold across the entire pipeline at all times. No stage may violate them.

**G1 — Ephemerality.** Session-Ephemeral Compilations are never persisted. Only artifacts that pass through Stage 8's mutation gate persist.

**G2 — Non-semantic profile purity.** User profiles contain only non-semantic data. No stage writes semantic content into a user profile.

**G3 — Non-mutation prior to governance approval.** No persistent state is mutated before passing through the appropriate governance gate: Safety_Gates for validation (Stages 3–4), mutation_gates for persistence (Stage 8).

**G4 — Canonical Primitive immutability.** Canonical Primitives are loaded at Stage 3 and never written, overwritten, or shadowed by any subsequent stage.

**G5 — Recall index read-only during pipeline execution.** Queryable at Stage 5. Writable only at Stage 8, only through mutation_gates. No other stage may read or write it.

**G6 — Single persistence gate.** Stage 8 is the sole persistence point. No other stage creates durable state.

**G7 — Monotonic authority.** Authority does not escalate through the pipeline. Stages 1–6 hold no write authority. Stage 8 holds write authority only as mediated by mutation_gates.

**G8 — No audit domain interaction.** No stage queries, reads, or writes SYSTEM_AUDIT_LOGS. The pipeline has no pathway into or out of the observability domain.

---

## 3. Invariant Classification

### Epistemic
Concern: knowledge, uncertainty, and classification correctness.

- G2 — profile must not function as a knowledge source
- Stage 5 pre-invariant — input classification must be unambiguous before a decision is returned
- Stage 6 post-invariant — all semantic content in the compilation is traceable; no hallucination surface exists

### Structural
Concern: pipeline order, dependencies, and conditional execution.

- Strict sequential dependency: no stage begins until its predecessor returns non-HALT
- G6 — single persistence gate
- Stage 8 conditional execution: fires only on ADAPT or GENERATE-NEW
- Stage 7 boundary: internal invariants and HALT semantics belong to MTP, not the scaffolding

### Governance-Derived
Concern: authority, permission, and constraint enforcement.

- Stage 3 — governance gate validation (Phase_Definitions, Denial_Invariants, Design_Only_Declarations)
- Stage 4 — per-artifact validation against current governance
- Stage 8 — mutation gate mediation
- G3 — non-mutation prior to governance approval
- G4 — Canonical Primitive immutability (derives from Baseline Canon)
- G7 — monotonic authority (derives from Autonomy_Policies)

### Safety-Critical
Concern: fail-closed behavior, no fallback, no escalation.

- HALT at every transition is terminal: no fallback, no degraded continuation, no escalation
- G1 — ephemerality prevents unintended persistence
- G5 — Recall index read-only during execution prevents covert state mutation
- G7 — monotonic authority prevents implicit escalation
- G8 — no audit domain interaction preserves memory domain separation

---

## 4. Scaffolding Correction Record

One invariant required correction to maintain consistency with the DR/AC Design Specification during this phase.

**Correction:** Stage 4 → Stage 5 HALT condition in the Reconstruction Scaffolding.

**Prior condition:** "At least one artifact survives overlay validation."

**Problem:** This condition would HALT a new user with an empty profile. Zero artifacts were available, so zero survived. This contradicts the DR/AC Specification, which establishes an empty profile as the safe default, not a failure.

**Corrected condition:** Stage 4 HALTs only when Curated Artifacts were available for overlay and all of them failed validation. An empty candidate set proceeds to Stage 5 with a baseline-only compilation.

**Scope:** Correction applies to the fail-closed transition table in the Reconstruction Scaffolding. The Scaffolding should be updated to reflect this correction before formalization.

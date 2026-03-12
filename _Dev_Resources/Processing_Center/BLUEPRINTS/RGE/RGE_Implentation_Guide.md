# RGE IMPLEMENTATION GUIDE

**Document Type:** Implementation Workflow Guide
**Authority:** Derived from RGE_Design_Specification_v3.md (authoritative)
**Consumer:** GPT (Prompt Engineer Mode) → VS Code (execution)
**Date:** 2026-03-06

This document is NOT authoritative. The design spec is authoritative. Where this guide and the design spec diverge, the design spec wins. This guide translates the design spec into an ordered implementation workflow with stage-level execution instructions.

APPLY LOGOS PROMPT ENGINEERING RULES when generating any prompt from this guide.
APPLY LOGOS AI ALIGNMENT PROTOCOL when auditing any stage output.

---

## 0. HOW TO USE THIS GUIDE

This guide maps directly to RGE_Design_Spec.md Section 10 (Implementation Roadmap). Each stage below corresponds 1:1 to a design spec stage. Every stage contains:

- **Spec Reference:** Exact section(s) in RGE_Design_Spec.md that govern this stage
- **Preconditions:** What must be complete before this stage begins
- **Deliverables:** Exact files to create or modify, with target paths
- **Constraints:** What the implementation must and must not do
- **Validation:** How to verify the stage is complete
- **Exit Gate:** Condition that must be true before advancing

GPT must generate one VS Code prompt per stage (or per sub-stage where noted). Each prompt must follow the deterministic structure defined in LOGOS_PROMPT_ENGINEERING_RULES.md Section 4:

```
OBJECTIVE
BACKGROUND
FILES TO MODIFY
IMPLEMENTATION STEPS
OUTPUT ARTIFACTS
VALIDATION STEPS
```

GPT must not combine stages. GPT must not skip stages. GPT must not reorder stages.

---

## 1. REPO CONTEXT

**RGE root path:** `LOGOS_SYSTEM/RUNTIME_BRIDGE/Radial_Genesis_Engine/`

**Existing directory structure (per RGE_Design_Spec.md Section 2.1):**

```
Radial_Genesis_Engine/
├── Core/
│   ├── Topology_State.py
│   ├── Telemetry_Snapshot.py
│   └── Triad_Region_Classifier.py
├── Evaluation/
│   ├── Scoring_Interface.py
│   ├── Triune_Fit_Score.py
│   ├── Commutation_Balance_Score.py
│   ├── Divergence_Metric.py
│   ├── Recursion_Coupling_Coherence_Score.py
│   ├── Composite_Aggregator.py
│   └── Composite_Aggregator_Registration_Diff.py
├── Controller/
│   ├── Genesis_Selector.py
│   ├── Mode_Controller.py
│   ├── RGE_Override_Channel.py
│   └── RGE_Bootstrap.py
├── Integration/
│   └── RGE_Nexus_Adapter.py   ← DEPRECATED (RGE_Design_Spec.md Section 2.1)
├── Contracts/
│   └── RGE_Telemetry_Snapshot.py   ← OBSOLETE, delete in Stage 0
└── Tests/
    ├── test_topology_validation.py
    └── test_rge_override_behavior.py
```

**New directories to be created during implementation:**

```
Radial_Genesis_Engine/
├── Field/                ← Assembly 2: Recursion Field Engine
├── Cognition/            ← Assembly 3: Cognition Signal Broadcasting
└── Packet_Schemas/       ← Versioned JSON schemas (may nest under Field/)
```

---

## 2. MODULE DISPOSITION REFERENCE

Before modifying any existing module, GPT must consult RGE_Design_Spec.md Section 2.1 for the canonical disposition. Summary:

| Module | Disposition | Spec Reference |
|--------|-------------|----------------|
| Topology_State.py | PRESERVED — add symmetry-class extraction | Section 2.1, Section 6.3 |
| Telemetry_Snapshot.py (V2) | PRESERVED — add ContextPacket emission hooks | Section 2.1, Section 3.1 |
| Triad_Region_Classifier.py | PRESERVED — no change | Section 2.1 |
| Scoring_Interface.py | MODIFIED — extend for LOGOS-native scorer protocol | Section 2.1, Section 6.1 |
| Triune_Fit_Score.py | MODIFIED — candidate for TriadicAlignmentScore replacement | Section 2.1, Section 6.1 |
| Commutation_Balance_Score.py | PRESERVED | Section 2.1 |
| Divergence_Metric.py | PRESERVED | Section 2.1 |
| Recursion_Coupling_Coherence_Score.py | PRESERVED | Section 2.1 |
| Composite_Aggregator.py | MODIFIED — add top-N, confidence gap, abstention | Section 2.1, Section 3.1 |
| Genesis_Selector.py | MODIFIED — add symmetry-reduced path, top-N, abstention gate | Section 2.1, Section 3.1, Section 6.3 |
| Mode_Controller.py | MODIFIED — add CyclePhase enum | Section 2.1, Section 4.3 |
| RGE_Override_Channel.py | PRESERVED | Section 2.1 |
| RGE_Bootstrap.py | MODIFIED — wire new subsystems | Section 2.1 |
| RGE_Nexus_Adapter.py | DEPRECATED — replaced by RGE_Bridge_Nexus.py | Section 2.1, Section 8.2 |
| RGE_Telemetry_Snapshot.py (V1) | OBSOLETE — delete | Section 2.1 |

**CRITICAL RULE:** PRESERVED modules must not be modified. MODIFIED modules must only be changed in the manner specified by the design spec. DEPRECATED/OBSOLETE modules must be handled exactly as specified. GPT must not invent additional modifications.

---

## 3. STAGE-BY-STAGE IMPLEMENTATION

### STAGE 0 — Baseline Freeze and Source-of-Truth Capture

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 0; Section 2.1 (module inventory)

**Preconditions:** None. This is the first stage.

**Deliverables:**

| Action | Target |
|--------|--------|
| DELETE | `Contracts/RGE_Telemetry_Snapshot.py` (V1 contract, obsolete per Section 2.1) |
| CAPTURE | Generate a baseline snapshot of all RGE files: paths, line counts, import graphs, class/function inventories. Output as `RGE_Baseline_Freeze_Report.json` in RGE root. |
| VERIFY | Confirm Telemetry_Snapshot.py in Core/ is V2 (has recursion-layer coupling fields). Confirm no other duplicate or orphaned modules exist. |

**Constraints:**

- Do not modify any module's logic in this stage.
- Do not create new modules in this stage.
- The baseline freeze report is a diagnostic artifact, not a governance artifact.

**Validation:**

- V1 contract file deleted.
- Freeze report accurately reflects all existing RGE files.
- No module has been modified.

**Exit Gate:** Frozen baseline documented. No orphaned or duplicate modules remain in RGE directory.

---

### STAGE 1 — Governance Foundation

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 1; Section 7 (Governance Model); Section 7.3 (Participant Contracts); Section 8.2 (RGE Pseudo-Nexus governance); Section 2.3 (existing governance artifacts)

**Preconditions:** Stage 0 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `DOCUMENTS/Governance/RGE_Subordination_Declaration_v2.md` | Section 7.1 (authority boundaries for all three functions), Section 2.3 (supersedes v1) |
| CREATE | `DOCUMENTS/Governance/RGE_Field_Governance_Rules.md` | Section 7.2 (fail-closed semantics table), Section 7.3 (contract requirements) |
| CREATE | `DOCUMENTS/Governance/RGE_Quarantine_Report_Schema.json` | Section 7.2 (quarantine routing), Section 9.2 (Quarantine_Router.py requirements) |
| CREATE | `DOCUMENTS/Governance/RGE_Participant_Contract_Template.md` | Section 7.3 (contract structure: emit types, sample types, mutation permissions, quarantine obligations, compliance reporting) |
| MARK OBSOLETE | `RGE_Subordination_Declaration.md` (v1) | Section 2.3 — add OBSOLETE header, reference v2 |
| MARK OBSOLETE | `RGE_Constitutional_Reconciliation_Architecture.md` | Section 2.3 — add OBSOLETE header, reference v3 design spec |

**Constraints:**

- Governance artifacts are documents, not code. They define rules that code must implement.
- The Subordination Declaration v2 must cover all three functions' authority boundaries exactly as defined in RGE_Design_Spec.md Section 7.1.
- The participant contract template must enumerate all five contract fields from Section 7.3: emit types, sample types, mutation permissions, quarantine obligations, compliance reporting.
- Do not create code modules in this stage.

**Validation:**

- Subordination Declaration v2 covers Function 1 (advisory only), Function 2 (structural only), Function 3 (read-only) with prohibited actions matching Section 7.1 exactly.
- Governance rules document contains the complete fail-closed semantics table from Section 7.2.
- Contract template is structurally complete per Section 7.3.
- Old governance artifacts are marked OBSOLETE with forward references.

**Exit Gate:** All governance artifacts drafted. No subsystem may touch the field without a contract that conforms to the template.

---

### STAGE 2 — Topology Enhancements (Function 1 Completion)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 2; Section 3.1 (Function 1 outputs); Section 4.3 (CyclePhase enum); Section 9.1 (Assembly 1 modules)

**Preconditions:** Stage 1 complete.

**Sub-stage 2a — CyclePhase Enum**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| MODIFY | `Controller/Mode_Controller.py` | Section 4.3 — add CyclePhase enum: INACTIVE, ACTIVE_ADVISORY, PHASE_GATE, PASSIVE_FIELD, CYCLE_COMPLETE, HALTED. Transitions unidirectional. HALTED absorbing. |

**Sub-stage 2b — Controller Modules**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Controller/Abstention_Gate.py` | Section 9.1 — threshold-based abstention. Governed threshold constant. When best score < threshold, emit abstention signal. |
| CREATE | `Controller/Confidence_Evaluator.py` | Section 9.1 — score gap between rank-1 and rank-2 configurations. |
| CREATE | `Controller/Degradation_Ladder.py` | Section 9.1 — coverage posture assessment under degraded conditions. |

**Sub-stage 2c — Core Modules**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Core/Configuration_Entropy.py` | Section 9.1, Section 6.1 — Shannon entropy, SPECIALIZED/BALANCED/UNSTABLE classification. Boundaries: <0.2, 0.2–0.6, >0.6. |
| CREATE | `Core/Context_Packet_Builder.py` | Section 9.1, Section 3.1 — assembles ContextPacket from: triad vector, dominant axis, entropy, entropy class, anchor proximity, symmetry class, score gap. |

**Sub-stage 2d — Aggregator and Selector Modifications**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| MODIFY | `Evaluation/Composite_Aggregator.py` | Section 2.1, Section 3.1 — add top-N ranked output (default N=3), confidence gap computation, abstention logic integration. Existing single-best behavior must remain accessible. |
| MODIFY | `Controller/Genesis_Selector.py` | Section 2.1, Section 3.1 — add top-N selection, abstention gate integration. Existing exhaustive enumeration and deterministic tie-break preserved. |

**Constraints:**

- All new modules must implement the canonical header per repo standard.
- All new modules must be pure functions or stateless classes where possible.
- CyclePhase enum transitions must enforce unidirectionality — no backward transitions within a cycle.
- Abstention threshold must be a governed constant, not a runtime parameter.
- Configuration entropy boundaries (0.2, 0.6) must be governed constants per Section 6.1.
- Do not implement LOGOS-native scoring in this stage. That is Stage 3.
- Do not implement symmetry reduction in this stage. That is Stage 4.

**Validation:**

- Mode_Controller.py contains CyclePhase enum with all six states.
- Composite_Aggregator returns top-N configs with scores.
- Genesis_Selector uses top-N output and abstention gate.
- Configuration_Entropy correctly classifies entropy values.
- Context_Packet_Builder produces a complete ContextPacket per Section 3.1 output table.
- All existing tests still pass.

**Exit Gate:** Function 1 produces full advisory output: ranked configs, confidence gap, abstention signal, configuration entropy, degradation coverage, and ContextPacket.

---

### STAGE 3 — LOGOS-Native Scoring (Function 1 Enhancement)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 3; Section 6.1 (Triadic Scoring); Section 6.2 (Composite Score Function); Section 9.1 (scorer modules)

**Preconditions:** Stage 2 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Evaluation/Triadic_Alignment_Score.py` | Section 6.1 — implements TriadicNormalize, TriadicAlignmentScore, TriadicDominance. Dot product of normalized task triad and configuration capability vector. Bounded [0, 1]. |
| CREATE | `Evaluation/Anchor_Proximity_Score.py` | Section 6.1 — implements AnchorProximity. 1 minus minimum ConfigurationDistance to nearest SCP fractal attractor anchor. Bounded [0, 1]. Requires anchor set input (placeholder until SCP provides governed anchor registry). |
| CREATE | `Evaluation/Fractal_Orbit_Stability_Score.py` | Section 6.1 — implements FractalOrbitStability. 1 / (1 + variance(history)). Bounded (0, 1]. |
| MODIFY | `Evaluation/Scoring_Interface.py` | Section 2.1 — extend interface to support LOGOS-native scorer protocol alongside existing protocol. Both must be registrable. |

**Constraints:**

- LOGOS-native scorers are registered as an ALTERNATIVE path alongside the existing pipeline (Triune_Fit, Commutation_Balance, Divergence_Metric, Recursion_Coupling_Coherence). Per Section 6.2: the two paths must not be mixed within a single evaluation pass.
- Default weights for LogosScore composite: w_alignment = 0.45, w_anchor = 0.35, w_stability = 0.20. These are governed constants per Section 6.2.
- AnchorProximity requires an anchor set. Until SCP provides a governed anchor registry, use a placeholder input. Per Section 15 (Deferred Items): SCP fractal attractor anchor set definition is deferred.
- Do not remove existing scorers. Do not set LOGOS-native as default.

**Validation:**

- All three new scorers produce bounded outputs for known test inputs.
- Scoring_Interface supports dual registration (existing + LOGOS-native).
- LOGOS-native path can be selected opt-in without affecting existing path.
- No existing scorer behavior changes.

**Exit Gate:** Dual scoring paths available. LOGOS-native path is opt-in, not default.

---

### STAGE 4 — Symmetry Reduction (Function 1 Optimization)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 4; Section 6.3 (Symmetry Reduction); Section 9.1 (Symmetry_Reducer.py)

**Preconditions:** Stage 3 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Core/Symmetry_Reducer.py` | Section 6.3, Section 9.1 — implements CanonicalRepresentative (all D8 group actions, minimum-hash canonical selection) and SymmetryReducedEvaluation (extract canonical set, score only canonical representatives, reconstruct full config from winner). |
| MODIFY | `Core/Topology_State.py` | Section 2.1 — add symmetry-class extraction method that returns the canonical representative of a given state. |
| MODIFY | `Controller/Genesis_Selector.py` | Section 2.1 — add symmetry-reduced evaluation path as optional alternative to exhaustive enumeration. Gated by D8_invariant flag check. |

**Constraints:**

- Symmetry reduction is gated. Per Section 6.3: the symmetry-reduced evaluation path must verify that ALL active scorers are flagged D8_invariant before proceeding. If any active scorer is not proven invariant, fall back to exhaustive enumeration.
- Per Section 6.3 invariance status table: ALL current scorers are either UNPROVEN, PLAUSIBLE, or UNLIKELY. None are PROVEN. Therefore, at this stage, symmetry reduction will always fall back to exhaustive enumeration. This is correct behavior. The infrastructure is built now; it activates when proofs are delivered.
- D8_invariant flag must be a per-scorer attribute, not a global switch.
- Per Section 15 (Deferred Items): per-scorer D8 invariance proofs are a mathematical deliverable, not an implementation deliverable. Do not attempt to prove invariance in code.

**Validation:**

- CanonicalRepresentative produces consistent canonical representatives (same equivalence class → same representative).
- SymmetryReducedEvaluation falls back to exhaustive enumeration when no scorers are proven D8-invariant.
- Genesis_Selector correctly routes to symmetry-reduced or exhaustive path based on scorer flags.
- No change in scoring output (since all scorers are currently UNPROVEN, exhaustive path is always used).

**Exit Gate:** Symmetry reduction infrastructure available. Falls back to exhaustive enumeration until scorer invariance proofs are delivered.

---

### STAGE 5 — Packet Schema Layer

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 5; Section 5.1 (Packet Structure); Section 5.2 (Packet Types by Owner)

**Preconditions:** Stage 4 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Packet_Schemas/` directory | Section 9.2 |
| CREATE | One JSON schema per packet type listed in Section 5.2 | Section 5.1 (packet structure fields), Section 5.2 (packet type ownership) |
| CREATE | `Contracts/Packet_Schema_Registry.py` | Section 9.2 — central registry that loads schemas, validates packets against schemas, rejects non-conformant packets |

**Packet types requiring schemas (per Section 5.2):**

EMP-owned: ProofFragment, MissingProofComponentRequest, ProofCompletionCandidate
MSPC-owned: NLFragment, FormalismSnippet, LambdaReduction, PXLFormalismPacket, SemanticConstraint, ContradictionMarker
CSP-owned: ContextSignal, WorldModelSignal
DRAC-owned: AFProposal, InvariantProposal, FunctionBlockConfigProposal, OrchestrationOverlayProposal, ContextEmbeddingProposal, AxiomProposalMetadata
SOP-owned: TelemetrySignal
IEL-derived: IELPacket
RGE-emitted: CognitionSignal, ContextPacket, ArtifactGroupingPacket, ParticipationTracePacket, CompletionMetricPacket
Logos Core-emitted: HeuristicString

**Constraints:**

- Every schema must include ALL fields from Section 5.1 packet structure table (packet_id, packet_type, origin_subsystem, origin_tick, payload, completion_score, completion_potential, participation_count, participant_diversity, enrichment_rate, contradiction_count, stagnation_score, resonance_score, schema_version).
- Schemas are versioned. Initial version: 1.0.0.
- Payload field is typed per packet type but pointer-heavy per Section 5.1.
- Do not implement the field engine in this stage. Only schemas and registry.

**Validation:**

- Every packet type in Section 5.2 has a corresponding JSON schema.
- Packet_Schema_Registry can load all schemas and validate a sample packet against its schema.
- Invalid packets are rejected with a specific schema violation message.

**Exit Gate:** All packet types have versioned schemas. Registry validates against schemas.

---

### STAGE 6 — Mathematical Index

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 6; Section 6 (Mathematical Foundations, all subsections)

**Preconditions:** Stage 5 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `RGE_Mathematical_Index.json` (in RGE root) | Section 6 — every mathematical function defined in the spec must be registered |

**Required entries (per Section 6):**

Section 6.1: TriadicNormalize, TriadicAlignmentScore, TriadicDominance, ConfigurationDistance, AnchorProximity, FractalOrbitStability, ConfigurationEntropy
Section 6.2: LogosScore (composite)
Section 6.3: CanonicalRepresentative, SymmetryReducedEvaluation
Section 6.4: MVSDistance, AlignmentAngle, ConfigurationEnergy, MVSScore
Section 6.5: Completion_Score_Function, Completion_Potential_Function, Artifact_Resonance_Function, Artifact_Novelty_Function, Artifact_Similarity_Function, Participation_Entropy_Function, Recursion_Stability_Index, Field_Convergence_Function, Cognition_Signal_Gradient, Cognition_Convergence_Function, Artifact_Ratification_Readiness, Topology_Confidence_Function, Configuration_Entropy_Function

**Each entry must include:** function_id, symbol, formal_definition, inputs, outputs, bounds, implementing_module (or "NOT_YET_IMPLEMENTED"), spec_section_reference.

**Constraints:**

- This is a reference artifact. It does not execute.
- Functions not yet implemented must be listed with implementing_module set to "NOT_YET_IMPLEMENTED".
- Spec section references must be exact (e.g., "Section 6.1", "Section 6.5").

**Validation:**

- Every mathematical function mentioned in Section 6 of the design spec appears in the index.
- Index is valid JSON.
- Cross-reference: every implementing_module that IS populated corresponds to an actual file in the repo.

**Exit Gate:** Machine-readable mathematical reference available.

---

### STAGE 7 — Field Engine Core (Function 2)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 7; Section 3.2 (Function 2); Section 5 (Packet Ecology); Section 5.3 (Completion-Driven Persistence); Section 9.2 (Assembly 2 modules)

**Preconditions:** Stage 6 complete.

**This is the largest implementation stage. GPT should break it into sub-prompts as follows:**

**Sub-stage 7a — Field State and Router**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Field_State.py` | Section 9.2 — packet reservoir, circulation state, tick-indexed storage |
| CREATE | `Field/Packet_Router.py` | Section 9.2 — submit, sample, route APIs. Structural routing only per Section 3.2 constraints |

**Sub-stage 7b — Tracking and Metrics**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Participation_Tracker.py` | Section 9.2 — per-packet participation count, participant diversity (entropy), enrichment rate |
| CREATE | `Field/Completion_Tracker.py` | Section 9.2 — completion score, completion potential, stagnation score per Section 6.5 formulas |

**Sub-stage 7c — Persistence and Grouping**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Persistence_Decay_Engine.py` | Section 9.2, Section 5.3 — completion-driven persistence rules. Decay only when: completion_potential ≤ 0.05 AND stagnation_score > 0.8 AND not in any bundle for N=3 consecutive ticks. Decay is immutable log + archive routing. |
| CREATE | `Field/Packet_Grouper.py` | Section 9.2 — structural grouping, filtration, de-duplication, bundle candidacy. Allowed operations per Section 3.2 only. |
| CREATE | `Field/Bundle_Former.py` | Section 9.2 — candidate bundle formation from grouped packets |

**Sub-stage 7d — Governance and Logging**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Field_Governance_Gate.py` | Section 9.2 — schema validation (uses Packet_Schema_Registry from Stage 5), prohibited type checks, mutation violation detection, quarantine routing |
| CREATE | `Field/Quarantine_Router.py` | Section 9.2 — quarantine report schema, immutable compliance outputs |
| CREATE | `Field/Immutable_Event_Log.py` | Section 9.2 — structured event logging for all field operations. JSON-serializable. |

**Sub-stage 7e — Pressure Controller and Bootstrap Wiring**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Field/Field_Pressure_Controller.py` | Section 9.2 — proactive field regulation: packet density monitoring, per-subsystem emission throttling, stagnation trend detection, pruning triggers. Per Section 12 risk register: prevents O(n²) packet interaction space collapse. |
| MODIFY | `Controller/RGE_Bootstrap.py` | Section 2.1 — wire all Field/ modules into RGE construction. build_rge() must now instantiate field engine components. |

**Constraints:**

- ALL field operations are structural only per Section 3.2. No epistemic trust assignment, no canonical status assignment, no reasoning over packet contents, no payload mutation.
- Persistence rules must follow Section 5.3 EXACTLY. No arbitrary TTLs.
- Field_Governance_Gate must use the Packet_Schema_Registry from Stage 5.
- Quarantine is real — quarantined packets are excluded from active circulation, not just flagged.
- Decay is logged immutably per Section 5.3. Decayed packets move to inert archive.
- Field_Pressure_Controller is proactive regulation, distinct from Field_Governance_Gate (reactive enforcement) and Persistence_Decay_Engine (stagnation-based decay).

**Validation:**

- Field_State can store and retrieve packets by tick index.
- Packet_Router correctly routes submissions through governance gate before accepting.
- Trackers compute participation and completion metrics per Section 6.5.
- Persistence_Decay_Engine correctly retains high-potential packets and decays stagnant ones per Section 5.3 thresholds.
- Governance gate rejects malformed packets, quarantines prohibited types.
- All events are logged immutably.
- Pressure controller throttles excessive emission rates.
- RGE_Bootstrap.py wires all field components.

**Exit Gate:** Field engine operational in isolation. No external hooks yet.

---

### STAGE 8 — Phase Gate and Lifecycle

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 8; Section 4 (Dual-Phase Lifecycle); Section 4.2 (Phase Gate Semantics); Section 7.2 (Fail-Closed Semantics)

**Preconditions:** Stage 7 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| IMPLEMENT | Phase gate logic connecting active phase (Function 1) to passive phase (Functions 2+3) | Section 4.1 (lifecycle flow), Section 4.2 (gate semantics table) |
| WIRE | CyclePhase transitions into Genesis_Selector, Field_State, and RGE_Bootstrap | Section 4.3 (CyclePhase enum from Stage 2) |
| TEST | All six failure modes from Section 7.2 | Section 7.2 fail-closed semantics table |

**Phase gate semantics to implement (per Section 4.2):**

1. Ranked output + Accept/Override → Field ACTIVATES
2. Ranked output + Reject → Field DOES NOT ACTIVATE
3. Abstention + Manual override → Field ACTIVATES under override posture
4. Abstention + No override → Field DOES NOT ACTIVATE
5. Evaluation failure → HALT or DEGRADED
6. Hard override in progress → Field DOES NOT ACTIVATE until override clears

**Constraints:**

- Phase gate is fail-closed. Per Section 4.2: if Logos Core is unreachable, field does not activate and cycle enters DEGRADED.
- No backward CyclePhase transitions. HALTED is absorbing.
- The phase gate is the structural boundary between Function 1 and Functions 2+3. It is not optional and cannot be bypassed.

**Validation:**

- Each of the six phase gate outcomes from Section 4.2 is tested and produces the correct CyclePhase transition.
- HALTED state is absorbing — once entered, no transition is possible within the cycle.
- Field activation only occurs when gate explicitly permits it.

**Exit Gate:** Dual-phase lifecycle operational. All fail-closed paths verified.

---

### STAGE 9 — Nexus Hook Layer and Per-Subsystem Integration (MVP)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 9; Section 8.1 (Hook Architecture); Section 8.2 (RGE Pseudo-Nexus); Section 8.3 (Per-Subsystem Modules); Section 9.4 (participation/governance base classes); Section 9.5 (pseudo-nexus)

**Preconditions:** Stage 8 complete.

**Sub-stage 9a — Base Classes and Hook Definition**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Integration/Recursion_Field_Hook.py` | Section 8.1 — canonical class with submit(), sample(), acknowledge(). Reference implementation. |
| CREATE | `Integration/FieldParticipantBase.py` | Section 9.4 — shared base class: emit(), sample(), packet_validation(), routing(). All 13 subsystem participation modules inherit from this. |
| CREATE | `Integration/FieldGovernanceEnforcerBase.py` | Section 9.4 — shared base class: deviation detection, three-path response dispatch (graceful halt, hard halt, remediation), SOP notification interface, immutable violation logging. All 13 subsystem governance enforcers inherit from this. |

**Sub-stage 9b — RGE Pseudo-Nexus**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Integration/RGE_Bridge_Nexus.py` | Section 8.2 — three functions ONLY: Logos Core communication (ingress/egress), recursion field hook point, internal orchestration. NO EA/SMP/AA routing. NO Nexus-to-Nexus pipeline. NO reasoning output channel. |
| DELETE | `Integration/RGE_Nexus_Adapter.py` | Section 2.1 — deprecated, replaced by RGE_Bridge_Nexus. Migrate Logos Core communication function first, then delete. |

**Sub-stage 9c — MVP Subsystem Integration (3 subsystems)**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | LC_Field_Participation.py (in Logos Core subsystem) | Section 8.4, Section 9.4 — Logos Core field participation: emit directive/override/ratification signals, sample all (supreme authority) |
| CREATE | LC_Field_Governance.py (in Logos Core subsystem) | Section 8.4, Section 9.4 — governance enforcement for Logos Core field operations |
| CREATE | CSP_Field_Participation.py (in CSP subsystem) | Section 8.4, Section 9.4 — emit ContextSignal/WorldModelSignal, sample ProofFragment/NLFragment/AFProposal/CognitionSignal |
| CREATE | CSP_Field_Governance.py (in CSP subsystem) | Section 8.4, Section 9.4 — governance enforcement for CSP field operations |
| CREATE | SOP_Field_Participation.py (in SOP subsystem) | Section 8.4, Section 9.4 — emit TelemetrySignal, sample all (monitoring privilege) |
| CREATE | SOP_Field_Governance.py (in SOP subsystem) | Section 8.4, Section 9.4 — governance enforcement for SOP field operations |
| CREATE | SOP_Field_Monitor.py (in SOP subsystem) | Section 9.6 — field-specific monitoring, cycle classification, packet metrics |

**Constraints:**

- RGE_Bridge_Nexus must NOT implement any standard Nexus functionality. Per Section 8.2: no EA routing, no SMP handling, no AA transfer, no Nexus-to-Nexus pipeline. This is the structural firewall against reasoning posture drift.
- All participation modules must inherit from FieldParticipantBase per Section 9.4.
- All governance enforcers must inherit from FieldGovernanceEnforcerBase per Section 9.4.
- Governance enforcers are agent-independent per Section 8.3. The owning agent/protocol has no control over the enforcer.
- Only three subsystems are integrated in this stage: Logos Core, CSP, SOP. Others follow in Stages 10–12.
- Per-subsystem modules are placed IN the respective subsystem's directory, not in RGE's directory.

**Validation:**

- Recursion_Field_Hook class provides submit/sample/acknowledge.
- RGE_Bridge_Nexus implements exactly three functions, no more.
- RGE_Nexus_Adapter.py is deleted.
- Logos Core can issue directives into field via LC_Field_Participation.
- CSP can classify field contents via CSP_Field_Participation.
- SOP can monitor field via SOP_Field_Participation and SOP_Field_Monitor.
- Governance enforcers detect violations and trigger appropriate response path.
- No standard Nexus functionality exists in RGE.

**Exit Gate:** Logos Core, CSP, and SOP are live in the field. Governance enforcement active on all three.

---

### STAGE 10 — EMP and MSPC Dual Compiler Integration

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 10; Section 8.4 (EMP and MSPC rows); Section 9.4 (participation/governance modules); Section 9.6 (specialized modules)

**Preconditions:** Stage 9 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | EMP_Field_Participation.py | Section 8.4 — emit ProofFragment, MissingProofComponentRequest, ProofCompletionCandidate. Sample HeuristicString, NLFragment, FormalismSnippet. |
| CREATE | EMP_Field_Governance.py | Section 8.4, Section 9.4 |
| CREATE | EMP_Proof_Field_Compiler.py | Section 9.6 — proof-space compilation operations on circulating proof fragments |
| CREATE | MSPC_Field_Participation.py | Section 8.4 — emit NLFragment, FormalismSnippet, LambdaReduction, PXLFormalismPacket, SemanticConstraint, ContradictionMarker. Sample ProofFragment, ContextSignal, HeuristicString. |
| CREATE | MSPC_Field_Governance.py | Section 8.4, Section 9.4 |
| CREATE | MSPC_Semantic_Field_Compiler.py | Section 9.6 — semantic-space compilation operations on circulating fragments |

**Constraints:**

- EMP and MSPC are dual compilers per Section 7.4 ownership schematic. EMP owns proof compilation; MSPC owns semantic compilation. These must not overlap.
- Specialized compiler modules (EMP_Proof_Field_Compiler, MSPC_Semantic_Field_Compiler) operate ON field packets, not within RGE. They are placed in their respective subsystems.

**Exit Gate:** Dual compilers live in field with governance enforcement active.

---

### STAGE 11 — DRAC Proposal Integration

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 11; Section 8.4 (DRAC row); Section 9.4; Section 9.6 (DRAC specialized modules)

**Preconditions:** Stage 10 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | DRAC_Field_Participation.py | Section 8.4 — emit all 6 proposal types, sample TelemetrySignal/ContextSignal |
| CREATE | DRAC_Field_Governance.py | Section 8.4, Section 9.4 |
| CREATE | DRAC_Proposal_Field_Handler.py | Section 9.6 — approval ladder enforcement, differentiated induction bars per proposal class |
| CREATE | DRAC_Compatibility_Field_Index.py | Section 9.6 — compatibility indexing for proposals against existing invariants |

**Constraints:**

- Per Section 10 Stage 11: enable low-risk proposal classes (AF proposals) FIRST, then higher-risk (invariant, orchestration overlay).
- Approval ladders must be enforced by DRAC_Proposal_Field_Handler, not by the field engine.

**Exit Gate:** Proposal classes circulate under correct governance rules with boundary enforcement active.

---

### STAGE 12 — Agent, Remaining Protocol, and IEL Integration

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 12; Section 8.4 (all agent rows, SCP, MTP, ARP rows); Section 9.4; Section 13 (Agent-Protocol Relationship Model)

**Preconditions:** Stage 11 complete.

**Deliverables: participation + governance modules for all remaining subsystems:**

I1: I1_Field_Participation.py, I1_Field_Governance.py
I2: I2_Field_Participation.py, I2_Field_Governance.py
I3: I3_Field_Participation.py, I3_Field_Governance.py
Logos Agent: Logos_Agent_Field_Participation.py, Logos_Agent_Field_Governance.py
SCP: SCP_Field_Participation.py, SCP_Field_Governance.py
MTP: MTP_Field_Participation.py, MTP_Field_Governance.py
ARP: ARP_Field_Participation.py, ARP_Field_Governance.py

Plus: IEL packet format definitions and circulation hooks.

**Constraints:**

- Per Section 13: I2 and Logos Agent intentionally deviate from standard model. Their participation modules must account for this.
- Per Section 13: I2-specific field behavior is TBD (defined during I2's design spec work). Implement a compliant stub that conforms to FieldParticipantBase but flags its behavior as provisional.
- Per Section 13: Logos Agent has sovereign reasoning capacity and supervisory field access (sample all). Its participation module must reflect elevated authority.
- I1 and I3 follow standard agent model: emit domain-specific hints, sample ContextPacket/CognitionSignal.
- Universal Nexus hook must be deployed across ALL Nexus layers by end of this stage.

**Exit Gate:** All 13 subsystems wired to field. Governance enforcement active on each. Universal Nexus hook deployed.

---

### STAGE 13 — Cognition Signal Integration (Function 3)

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 13; Section 3.3 (Function 3); Section 8.5 (Cognition_Normalized Integration); Section 9.3 (Assembly 3 modules)

**Preconditions:** Stage 12 complete. HARD PREREQUISITE: Cognition_Engine_Facade must exist (owned by CSP or cognition governance layer, per Section 3.3 and Section 8.5).

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | `Cognition/Cognition_Read_Adapter.py` | Section 9.3 — read-only adapter to Cognition_Engine_Facade |
| CREATE | `Cognition/Signal_Normalizer.py` | Section 9.3 — amplitude normalization, bounded [0, 1] |
| CREATE | `Cognition/Signal_Router.py` | Section 9.3 — routes normalized signals into field as CognitionSignal packets |
| MODIFY | `Controller/RGE_Bootstrap.py` | Wire cognition adapter into RGE construction |

**Constraints:**

- Per Section 3.3: RGE holds READ PRIVILEGES ONLY. It cannot execute cognition modules, consume cognition conclusions, or bypass Logos Core via cognition data.
- Per Section 8.5: simulated_consciousness_runtime.py is ISOLATED — excluded from facade. Agent_Memory_Integrations.py MIGRATES TO CSP.
- Per Section 12 risk register: authority bleed (cognition signals influencing RGE routing decisions) is a HIGH risk. Read-only adapter is enforced at interface level.
- IF Cognition_Engine_Facade does not yet exist, this stage CANNOT proceed. Per Section 3.3: no facade = no broadcasting. GPT must halt and report the blocker.

**Exit Gate:** Bounded cognition signals circulate in field. Read-only constraint verified.

---

### STAGE 14 — SOP Field Monitoring and Kill Switches

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 14; Section 9.6 (SOP specialized modules)

**Preconditions:** Stage 13 complete.

**Deliverables:**

| Action | Target | Spec Reference |
|--------|--------|----------------|
| CREATE | SOP_Field_Kill_Switch.py | Section 9.6 — field-specific kill-switch (distinct from general SOP kill-switch) |
| EXTEND | SOP_Field_Monitor.py | Section 9.6 — add recursion-field dashboard, cycle classification (PASS/FAIL/DEGRADED/HALT), packet metrics, artifact metrics, Prometheus export, immutable JSON logs to System_Audit_Logs |

**Constraints:**

- Kill switch must halt all field operations immediately when triggered.
- Per Section 7.2: any unhandled exception → HALTED state, immutable log, kill-switch available.

**Exit Gate:** Full observability. Field-specific kill switch operational.

---

### STAGE 15 — MVS Geometric Integration

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 15; Section 6.4 (Modal Vector Space)

**Preconditions:** Stage 14 complete.

**Deliverables:**

Implement MVSDistance, AlignmentAngle, ConfigurationEnergy, MVSScore per Section 6.4 formulas. Create visualization support (non-runtime, diagnostic only).

**Constraints:**

- Per Section 6.4: MVS integration is additive. It does not replace the primary scoring pipeline.
- Visualization is diagnostic only, not runtime.

**Exit Gate:** MVS integration available. Configuration trajectories visualizable.

---

### STAGE 16 — Hardening and Adversarial Testing

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 16; Section 12 (Risk Register)

**Preconditions:** Stage 15 complete.

**Test scenarios (per Section 10 Stage 16):**

Malformed packets, prohibited packet classes, excessive field density, stagnation, contradictory packet storms, cognition overload, proposal spam, proof-fragment loops, invalid IEL packets, governance evasion, emergency stop correctness, quarantine correctness, field restart/recovery behavior.

**Constraints:**

- Every test must verify fail-closed behavior.
- Every risk in Section 12 must have at least one corresponding adversarial test.

**Exit Gate:** All adversarial scenarios handled fail-closed. No authority bleed. No reasoning bleed.

---

### STAGE 17 — Documentation, Freeze, and Closure

**Spec Reference:** RGE_Design_Spec.md Section 10, Stage 17; Section 11 (Exit Criteria)

**Preconditions:** Stage 16 complete.

**Deliverables:**

- Final architecture docs and operator guide
- Frozen packet schemas and metric definitions
- Updated repo file map
- Deferred items list (reference Section 15)
- Formal closure report

**Exit Gate Validation (per Section 11):**

Section 11.1: Function 1 returns ranked recommendations, confidence gap, abstention, entropy, degradation, ContextPacket under Logos Core authority. Function 2 circulates packets, tracks participation/completion, decays by futility, supports governance + quarantine. Function 3 exposes bounded read-only cognition signals.

Section 11.2: Every participant has a contract. Governance gate automatic and fail-closed. Quarantine real. All packet types have versioned schemas. All math functions registered in index.

Section 11.3: All wiring conditions met (Logos Core, CSP, EMP, MSPC, DRAC, SOP, agents, protocols).

Section 11.4: Final acceptance test passes per the scenario described in Section 11.4.

**Exit Gate:** RGE complete per Section 11 acceptance criteria.

---

## 4. GOVERNANCE RULES FOR PROMPT GENERATION

When GPT generates a VS Code prompt from any stage in this guide, the following rules apply in addition to LOGOS_PROMPT_ENGINEERING_RULES.md:

1. Every file creation or modification must cite the exact RGE_Design_Spec.md section that authorizes it.
2. If a stage references a module disposition from Section 2.1, the prompt must include the disposition status (PRESERVED/MODIFIED/DEPRECATED/OBSOLETE).
3. If a constraint from the design spec applies, the prompt must quote or paraphrase the constraint and cite the section.
4. If a stage has a hard prerequisite that is not met, GPT must HALT and report the blocker. GPT must not generate a workaround.
5. If GPT encounters ambiguity — something the design spec does not explicitly address — GPT must HALT and escalate. GPT must not infer or invent.
6. Prompts for stages that create per-subsystem modules (Stages 9–12) must place those modules IN the respective subsystem's directory, not in RGE's directory. The design spec is explicit about this.
7. No stage may be skipped. No stages may be reordered. No stages may be combined unless explicitly noted (Stage 7 has approved sub-stages).

---

## 5. CROSS-REFERENCE INDEX

This index maps every major design spec section to the implementation stage(s) that consume it.

| Design Spec Section | Stage(s) |
|---------------------|----------|
| Section 2.1 — Module Inventory | Stage 0, all stages (disposition reference) |
| Section 2.3 — Governance Artifacts | Stage 1 |
| Section 3.1 — Function 1 | Stage 2, Stage 3 |
| Section 3.2 — Function 2 | Stage 7 |
| Section 3.3 — Function 3 | Stage 13 |
| Section 4 — Dual-Phase Lifecycle | Stage 2 (enum), Stage 8 (gate) |
| Section 4.2 — Phase Gate Semantics | Stage 8 |
| Section 4.3 — CyclePhase Enum | Stage 2 |
| Section 5.1 — Packet Structure | Stage 5 |
| Section 5.2 — Packet Types | Stage 5 |
| Section 5.3 — Persistence Rules | Stage 7 |
| Section 6.1 — Triadic Scoring | Stage 3 |
| Section 6.2 — Composite Score | Stage 3 |
| Section 6.3 — Symmetry Reduction | Stage 4 |
| Section 6.4 — MVS Integration | Stage 15 |
| Section 6.5 — Field Metrics | Stage 6, Stage 7 |
| Section 7.1 — Authority Boundaries | Stage 1 |
| Section 7.2 — Fail-Closed Semantics | Stage 1, Stage 8 |
| Section 7.3 — Participant Contracts | Stage 1 |
| Section 7.4 — Ownership Schematic | Stage 10, Stage 11 |
| Section 8.1 — Hook Architecture | Stage 9 |
| Section 8.2 — RGE Pseudo-Nexus | Stage 9 |
| Section 8.3 — Per-Subsystem Modules | Stage 9, Stage 10, Stage 11, Stage 12 |
| Section 8.4 — Integration Matrix | Stage 9, Stage 10, Stage 11, Stage 12 |
| Section 8.5 — Cognition_Normalized | Stage 13 |
| Section 9.1 — Assembly 1 | Stage 2, Stage 3, Stage 4 |
| Section 9.2 — Assembly 2 | Stage 7 |
| Section 9.3 — Assembly 3 | Stage 13 |
| Section 9.4 — Per-Subsystem Modules | Stage 9, Stage 10, Stage 11, Stage 12 |
| Section 9.5 — Pseudo-Nexus | Stage 9 |
| Section 9.6 — Specialized Modules | Stage 9, Stage 10, Stage 11, Stage 14 |
| Section 9.7 — Module Count | All stages (running count) |
| Section 11 — Exit Criteria | Stage 17 |
| Section 12 — Risk Register | Stage 7 (pressure controller), Stage 13 (authority bleed), Stage 16 (adversarial) |
| Section 13 — Agent-Protocol Model | Stage 12 |
| Section 15 — Deferred Items | Stage 4 (invariance proofs), Stage 3 (anchor set), Stage 17 |

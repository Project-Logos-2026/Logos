# EMP Native Coq Proof Engine — Blueprint and Roadmap

**Filename:** EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
**Target Path:** LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/Epistemic_Monitoring_Protocol/Documentation/
**Status:** DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
**Authority:** Logos Agent (design approval required before implementation)
**Supersedes:** None (extends existing EMP governance scope)
**Depends On:** PXL_Gate Coq baseline, EMP_Core, EMP_Nexus, MSPC Protocol, Octafolium architecture

---

## 1. Purpose and Scope

This document defines the design blueprint and sequential build roadmap for transforming the Epistemic Monitoring Protocol (EMP) from its current stub implementation into a native Coq proof engine with secondary capabilities as a search engine, inference tool, and abstraction engine.

EMP is an existing P2 (priority-two) protocol in the LOGOS runtime. Its canonical function is to enrich Structured Meaning Packets (SMPs) with Append Artifacts (AAs) through iterative proof synthesis, template derivation, and cumulative bivalence forcing. EMP proof artifacts are required for SMP canonicalization per the Shared AA Schema Appendix.

This document is design-only. It does not authorize implementation by itself.

---

## 2. Current State Assessment

### 2.1 EMP_Core: EMP_Meta_Reasoner.py

Current implementation is a 14-line stub:

- `EMP_Meta_Reasoner.__init__(budget)` — initializes reasoning budget counter
- `EMP_Meta_Reasoner._use(n=1)` — increments step counter, raises `ReasoningBudgetExceeded` on overflow
- `EMP_Meta_Reasoner.analyze(artifact)` — checks `artifact["proof_state"] == "complete"`, assigns `epistemic_state` as either `canonical_candidate` or `provisional`, records `reasoning_steps_used`

No Coq integration. No proof verification. No search or inference capability. Classification is binary and shallow.

### 2.2 EMP_Nexus: EMP_Nexus.py

Fully operational Standard Nexus implementation:

- `PreProcessGate` — structural admissibility check (payload must be dict)
- `PostProcessGate` — egress tagging via `_apply_provisional_proof_tagging`
- `MeshEnforcer` — validates payload is dict with `content` key
- `MREGovernor` — pre/post tick gating via Metered Reasoning Enforcer
- `StandardNexus` — participant registration, deterministic tick orchestration, state routing
- `NexusHandle` — restricted emit interface for participants
- `NexusParticipant` — abstract interface (register, receive_state, execute_tick, project_state)

Provisional proof tagging scans for PXL-related keywords (`pxl`, `proof`, `axiom`, `wff`) and attaches `PROVISIONAL_PROOF_TAG` with status `PROVISIONAL`, disclaimer `Requires EMP compilation`, and confidence uplift of `0.05`.

### 2.3 EMP Governance Scope (Repo-Authoritative)

Permissions:
- Apply bounded epistemic tagging
- Register participants and route packets via Nexus
- Enforce mesh constraints and MRE gating

Prohibitions:
- No agent reasoning or inference
- No authority expansion or capability grants
- No SOP mutation or external execution

Enforcement points: PreProcessGate, PostProcessGate, MeshEnforcer, MREGovernor

Non-authority declaration: This protocol does not confer or expand authority.

### 2.4 EMP-to-SOP Contract

- Advisory only
- No mutation
- MRE enforced

### 2.5 PXL Coq Baseline (Available Infrastructure)

The PXL_Gate contains a complete Coq project:

- 60 `.v` source files across `src/`, `src/baseline/`, `src/modal/`, `src/option_b/`, `src/tests/`, `src/ui/`
- `_CoqProject` loadpath: `-Q src PXL`
- Core modules: PXL_Definitions, PXL_Kernel_Axioms, PXLv3, PXL_Modal_Axioms_Semantic
- Baseline proofs: 32+ operational proof modules including PXL_Bridge_Proofs, PXL_Global_Bijection, PXL_Trinitarian_Optimization, PXL_OmniProofs
- Semantic modal kernel: 17-axiom profile compiled end-to-end (PXL_Semantic_Profile_Suite.v)
- S5 Kripke semantics: full modal layer (PXL_Modal_Semantic_Kripke.v)
- jsCoq WebAssembly: working browser-based Coq verification
- Zero-admits on critical theorems: `safety_gate`, `global_bijection`

### 2.6 MSPC Protocol (Newly Delivered, Standalone)

23-file protocol package at `LOGOS_SYSTEM/Runtime_Protocols/MSPC/` with five subdirectories:

- Signals/ — signal definition and routing
- Compilation/ — multi-signal compilation
- Resolution/ — conflict resolution
- Contracts/ — protocol contracts
- Diagnostics/ — runtime diagnostics

MSPC is the designated runtime coherence witness for EMP under the Octafolium architecture. MSPC guarantees every formal derivation is simultaneously expressible in natural language, mathematics, lambda calculus, and PXL formalism. This enables EMP to operate unairlocked as a live reasoning component.

---

## 3. Architectural Design

### 3.1 Core Principle (Non-Negotiable)

EMP remains a non-reasoning, non-assertive protocol. Proof verification is mechanical, not epistemic. EMP does not interpret, decide, or infer. It compiles, verifies, indexes, and tags. All outputs are AAs bound to SMPs. EMP never promotes SMPs; it emits promotion-support AAs that Logos evaluates.

### 3.2 Transformation Scope

EMP transforms from:
- Binary stub classifier (`complete` → `canonical_candidate`, else → `provisional`)

To:
- Native Coq proof verification engine
- Proof-state indexer and search engine
- Template derivation tool
- Abstraction pattern extractor
- Bivalence forcing mechanism

All within existing governance scope. No new authority. No new permissions beyond what GOVERNANCE_SCOPE.md already permits.

### 3.3 Module Architecture

```
Epistemic_Monitoring_Protocol/
├── EMP_Core/
│   ├── EMP_Meta_Reasoner.py          [REPLACE — Coq-backed proof classifier]
│   ├── EMP_Coq_Bridge.py             [NEW — Coq process management]
│   ├── EMP_Proof_Index.py            [NEW — proof state indexing and search]
│   ├── EMP_Template_Engine.py        [NEW — template derivation from proofs]
│   └── EMP_Abstraction_Engine.py     [NEW — pattern extraction and generalization]
├── EMP_Nexus/
│   ├── EMP_Nexus.py                  [MODIFY — enhanced PostProcessGate with Coq results]
│   ├── Library_Manifest.py           [PRESERVE]
│   └── EMP_MSPC_Witness.py           [NEW — MSPC coherence witness integration]
├── EMP_Documentation/
│   ├── EMP_TO_SOP_CONTRACT_SCHEMA.md [PRESERVE]
│   └── EMP_PROOF_RESULT_SCHEMA.md    [NEW — structured proof output format]
└── Documentation/
    ├── GOVERNANCE_SCOPE.md            [PRESERVE — no governance changes]
    ├── MANIFEST.md                    [UPDATE — add new files]
    ├── METADATA.json                  [UPDATE — ready_for_deployment status]
    ├── ORDER_OF_OPERATIONS.md         [UPDATE — add Coq verification flow]
    ├── RUNTIME_ROLE.md                [UPDATE — reflect enhanced capabilities]
    └── STACK_POSITION.md              [UPDATE — add PXL_Gate dependency]
```

### 3.4 EMP_Coq_Bridge — Coq Process Manager

Responsibilities:
- Manage Coq subprocess lifecycle (coqc, coqtop, or jsCoq WebAssembly)
- Submit `.v` content for compilation
- Parse and structure Coq output (success, error, admits, axiom dependencies)
- Enforce compilation timeout (reasoning budget maps to wall-clock limit)
- Maintain loadpath configuration matching `_CoqProject` semantics

Interface:
```
EMP_Coq_Bridge.verify(coq_source: str) -> CoqVerificationResult
EMP_Coq_Bridge.check_theorem(theorem_name: str, file_path: str) -> TheoremStatus
EMP_Coq_Bridge.get_axiom_footprint(file_path: str) -> List[str]
EMP_Coq_Bridge.compile_file(file_path: str) -> CompilationResult
```

CoqVerificationResult schema:
```
{
  "verified": bool,
  "admits_count": int,
  "axiom_dependencies": List[str],
  "proof_steps": int,
  "compilation_time_ms": int,
  "error_message": Optional[str],
  "vo_artifact_hash": Optional[str]
}
```

Fail-closed semantics: any Coq subprocess failure, timeout, or parse error returns `verified: false` with error details. No partial success states.

Environment selection order:
1. Native coqc (if available on system PATH)
2. jsCoq WebAssembly (browser/Node.js environments)
3. Fail-closed with `"error_message": "No Coq environment available"`

### 3.5 EMP_Meta_Reasoner (Replacement)

The replacement Meta Reasoner delegates to EMP_Coq_Bridge for actual verification while preserving the existing budget enforcement interface.

Enhanced classification states (monotonic, ordered):
```
UNVERIFIED        — no proof attempted
PROVISIONAL       — proof attempted, incomplete or admitted
PARTIAL           — proof compiles but contains admits
VERIFIED_AXIOMATIC — proof compiles, zero admits, but uses non-PXL axioms
VERIFIED_PXL      — proof compiles, zero admits, all axioms in PXL kernel
CANONICAL_CANDIDATE — VERIFIED_PXL + MSPC coherence witness PASS
```

Classification rules:
- `UNVERIFIED` → default state for all artifacts without proof content
- `PROVISIONAL` → Coq compilation fails or proof contains `Admitted.`
- `PARTIAL` → Coq compiles, but `admits_count > 0`
- `VERIFIED_AXIOMATIC` → Coq compiles, `admits_count == 0`, axiom footprint exceeds PXL kernel
- `VERIFIED_PXL` → Coq compiles, `admits_count == 0`, all axioms in PXL kernel set
- `CANONICAL_CANDIDATE` → `VERIFIED_PXL` + MSPC coherence witness returns `COHERENT`

No artifact may skip classification levels. Budget enforcement remains: `ReasoningBudgetExceeded` halts classification at current state.

### 3.6 EMP_Proof_Index — Search Engine

Maintains an in-session index of all verified proofs, their dependency graphs, axiom footprints, and theorem signatures.

Capabilities:
- **Theorem search** — find proofs by name, axiom usage, or structural pattern
- **Dependency graph traversal** — map which theorems depend on which
- **Axiom footprint analysis** — identify minimal axiom sets for any theorem
- **Proof gap detection** — find theorems referenced but not yet proven
- **Completeness mapping** — percentage of PXL kernel covered by verified proofs

Interface:
```
EMP_Proof_Index.index_file(file_path: str, verification_result: CoqVerificationResult)
EMP_Proof_Index.search(query: str) -> List[ProofEntry]
EMP_Proof_Index.get_dependency_graph(theorem_name: str) -> DependencyGraph
EMP_Proof_Index.get_axiom_footprint(theorem_name: str) -> List[str]
EMP_Proof_Index.find_gaps() -> List[UnprovenReference]
EMP_Proof_Index.coverage_report() -> CoverageReport
```

Index is session-scoped. Rebuilt on each session via DRAC reconstruction. No persistent state.

### 3.7 EMP_Template_Engine — Template Derivation

Extracts reusable proof templates from verified proofs for downstream compilation layers.

Capabilities:
- **Pattern extraction** — identify recurring proof structures (modus ponens chains, induction patterns, case analysis structures)
- **Template generation** — produce parameterized proof skeletons from verified examples
- **Template validation** — verify that template instantiation preserves proof validity
- **Template catalog** — session-scoped registry of available templates

Interface:
```
EMP_Template_Engine.extract_templates(verified_proofs: List[ProofEntry]) -> List[ProofTemplate]
EMP_Template_Engine.instantiate(template: ProofTemplate, params: Dict) -> str
EMP_Template_Engine.validate_instantiation(instance: str) -> CoqVerificationResult
EMP_Template_Engine.catalog() -> List[ProofTemplate]
```

Templates are non-authoritative derived artifacts per Phase-3.1 Derived Policy Compiler Charter. All templates bind to source proofs via cryptographic hash. Any mismatch between template and source triggers DENY.

### 3.8 EMP_Abstraction_Engine — Inference and Generalization

Mechanical abstraction operations on verified proofs. Not inference in the epistemic sense — structural pattern operations only.

Capabilities:
- **Generalization** — propose more general versions of specific theorems by identifying substitutable parameters
- **Lemma suggestion** — identify intermediate lemmas that would simplify complex proofs
- **Cross-module pattern mining** — find common proof structures across the PXL baseline
- **Complexity analysis** — measure proof complexity (depth, branching, axiom count)

Interface:
```
EMP_Abstraction_Engine.generalize(theorem: ProofEntry) -> List[GeneralizationCandidate]
EMP_Abstraction_Engine.suggest_lemmas(goal: str) -> List[LemmaCandidate]
EMP_Abstraction_Engine.mine_patterns(proofs: List[ProofEntry]) -> List[ProofPattern]
EMP_Abstraction_Engine.complexity(theorem: ProofEntry) -> ComplexityReport
```

All candidates are tagged `UNVERIFIED` until passed through EMP_Coq_Bridge. Candidates that fail verification are discarded, not stored.

### 3.9 EMP_MSPC_Witness — Coherence Gate

Integration point between EMP and MSPC under the Octafolium architecture.

The MSPC coherence witness operates on the I2 axis. For any EMP derivation to achieve `CANONICAL_CANDIDATE` status, it must satisfy simultaneous expressibility across four modalities:

1. Natural language — the derivation can be stated in governed NL
2. Mathematics — the derivation has a valid mathematical representation
3. Lambda calculus — the derivation has a lambda-calculus encoding
4. PXL formalism — the derivation compiles in PXL Coq

MSPC does not validate proof correctness (that is EMP's domain). MSPC validates that the proof is coherent across representational modalities. If any modality fails expressibility, MSPC returns `INCOHERENT` and EMP classification halts at `VERIFIED_PXL`.

Interface:
```
EMP_MSPC_Witness.request_coherence_check(derivation: VerifiedDerivation) -> CoherenceResult
EMP_MSPC_Witness.get_modality_status(derivation_id: str) -> Dict[str, ModalityStatus]
```

CoherenceResult schema:
```
{
  "coherent": bool,
  "modality_results": {
    "natural_language": {"expressible": bool, "representation": Optional[str]},
    "mathematics": {"expressible": bool, "representation": Optional[str]},
    "lambda_calculus": {"expressible": bool, "representation": Optional[str]},
    "pxl_formal": {"expressible": bool, "representation": Optional[str]}
  },
  "incoherence_reason": Optional[str]
}
```

Communication path: EMP → Logos Agent → MSPC → Logos Agent → EMP. No direct protocol-to-protocol communication.

### 3.10 EMP_PROOF_RESULT_SCHEMA — Structured Output Format

Every EMP proof verification produces a structured AA conforming to:

```
{
  "aa_type": "ProtocolAA",
  "originating_entity": "EMP",
  "aa_fields": {
    "proof_result": {
      "classification": "<UNVERIFIED|PROVISIONAL|PARTIAL|VERIFIED_AXIOMATIC|VERIFIED_PXL|CANONICAL_CANDIDATE>",
      "coq_verification": CoqVerificationResult,
      "mspc_coherence": Optional[CoherenceResult],
      "axiom_footprint": List[str],
      "dependency_graph_hash": str,
      "template_derivations": List[str],
      "budget_consumed": int,
      "budget_remaining": int
    }
  }
}
```

All AAs conform to the Shared AA Schema Appendix. No deviation.

### 3.11 Enhanced PostProcessGate

The existing `_apply_provisional_proof_tagging` function is replaced with Coq-backed tagging:

Current behavior (keyword scan):
- Scans payload for PXL-related keywords
- Attaches `PROVISIONAL_PROOF_TAG` with static confidence uplift of 0.05

Enhanced behavior (Coq-verified):
- If payload contains proof content, routes to EMP_Coq_Bridge for verification
- Attaches `EMP_PROOF_RESULT` AA with full classification and verification data
- Confidence uplift is graduated by classification level:
  - UNVERIFIED: 0.00
  - PROVISIONAL: 0.02
  - PARTIAL: 0.05
  - VERIFIED_AXIOMATIC: 0.10
  - VERIFIED_PXL: 0.15
  - CANONICAL_CANDIDATE: 0.20
- Fails closed: any verification error returns UNVERIFIED with 0.00 uplift

Backward compatibility: payloads without proof content continue through unchanged. The keyword scan remains as a fast-path detector to avoid unnecessary Coq invocations.

---

## 4. Governance Compliance

### 4.1 No Governance Changes Required

All new capabilities fall within existing EMP governance scope:
- "Apply bounded epistemic tagging" — Coq verification is mechanized tagging, not reasoning
- "Register participants and route packets via Nexus" — unchanged
- "Enforce mesh constraints and MRE gating" — unchanged

### 4.2 Prohibitions Preserved

- No agent reasoning or inference — EMP delegates to Coq (mechanical) and MSPC (coherence check via Logos Agent routing). EMP itself performs zero inference.
- No authority expansion — EMP_PROOF_RESULT AAs are non-authoritative. Logos Agent alone evaluates them for promotion decisions.
- No SOP mutation — EMP-to-SOP contract remains advisory-only, one-way, MRE enforced.
- No external execution — Coq subprocess is a verification tool, not an execution environment. No Coq-compiled artifacts are executed at runtime.

### 4.3 Phase-3.1 Compliance

All template derivations and abstraction outputs are:
- Deterministic and reproducible from source proofs
- Bound to source via cryptographic hash
- Non-authoritative mirrors subordinate to `.v` source files
- Subject to proof-of-equivalence requirement (template instantiation must re-verify)

### 4.4 Runtime Artifact Ingress Compliance

All EMP outputs entering downstream systems satisfy:
- Unique Artifact ID (AA hash)
- Emitting Protocol ID (EMP)
- Emission Timestamp
- Version Identifier
- Cryptographic Hash
- Declared Artifact Class (ProtocolAA)
- Declared Ingress Target
- Phase Compatibility Marker

---

## 5. Dependency Map

```
EMP_Coq_Bridge
  ← PXL_Gate/coq/ (_CoqProject, .v files, .vo artifacts)
  ← coqc | jsCoq WebAssembly runtime

EMP_Meta_Reasoner (replacement)
  ← EMP_Coq_Bridge
  ← EMP_MSPC_Witness (for CANONICAL_CANDIDATE classification)

EMP_Proof_Index
  ← EMP_Coq_Bridge (verification results)
  ← PXL_Gate/coq/src/ (file listing)

EMP_Template_Engine
  ← EMP_Proof_Index (verified proofs as input)
  ← EMP_Coq_Bridge (template validation)

EMP_Abstraction_Engine
  ← EMP_Proof_Index (proofs and patterns)
  ← EMP_Coq_Bridge (candidate verification)

EMP_MSPC_Witness
  ← MSPC Protocol (via Logos Agent routing)
  ← EMP_Coq_Bridge (derivation data)

EMP_Nexus (enhanced PostProcessGate)
  ← EMP_Meta_Reasoner (classification)
  ← EMP_Coq_Bridge (verification results)
```

No circular dependencies. All information flows are acyclic.

---

## 6. Build Roadmap

### Phase E1: Coq Bridge Foundation
**Duration estimate:** 3-5 days
**Deliverables:**
- EMP_Coq_Bridge.py — complete module
- Coq subprocess wrapper with timeout enforcement
- Output parser for coqc compilation results
- Loadpath configuration matching PXL_Gate _CoqProject
- Integration test: verify `pxl_excluded_middle` theorem via bridge

**Dependencies:** PXL_Gate Coq infrastructure must be accessible at known path
**Validation:** Bridge successfully compiles PXL_Semantic_Profile_Suite.v and returns structured result with correct admits count (0) and axiom list
**Governance gate:** None (internal tooling, no runtime surface)

### Phase E2: Meta Reasoner Replacement
**Duration estimate:** 2-3 days
**Deliverables:**
- EMP_Meta_Reasoner.py — replacement module preserving existing interface
- Six-tier classification state machine
- Budget enforcement mapped to Coq compilation timeout
- EMP_PROOF_RESULT_SCHEMA.md — structured output format

**Dependencies:** Phase E1 complete
**Validation:** Meta Reasoner correctly classifies a known-good proof (PXL_Bridge_Proofs.v → VERIFIED_PXL), a proof with admits (any `Admitted.` file → PARTIAL), and an invalid proof (synthetic error → PROVISIONAL)
**Governance gate:** None (replaces stub with mechanical equivalent)

### Phase E3: Proof Index and Search
**Duration estimate:** 3-4 days
**Deliverables:**
- EMP_Proof_Index.py — complete module
- Theorem name index, axiom footprint index, dependency graph builder
- Search interface (name, axiom, pattern queries)
- Coverage report generator
- Gap detection for unproven references

**Dependencies:** Phase E2 complete
**Validation:** Index all 60 PXL_Gate .v files. Search for `pxl_excluded_middle` returns correct entry. Dependency graph for `PXL_OmniProofs.v` correctly reflects import chain. Gap detection identifies any `Parameter` or `Axiom` declarations without corresponding proofs.
**Governance gate:** None (read-only index, no authority)

### Phase E4: Enhanced PostProcessGate
**Duration estimate:** 1-2 days
**Deliverables:**
- Modified EMP_Nexus.py PostProcessGate with Coq-backed tagging
- Graduated confidence uplift by classification tier
- Backward-compatible keyword fast-path for non-proof payloads
- Updated ORDER_OF_OPERATIONS.md

**Dependencies:** Phase E2 complete
**Validation:** Packets with proof content receive Coq-verified tags. Packets without proof content pass through unchanged. Budget exhaustion fails closed to UNVERIFIED.
**Governance gate:** Logos Agent review of modified Nexus behavior (existing governance, no scope change)

### Phase E5: Template Engine
**Duration estimate:** 3-4 days
**Deliverables:**
- EMP_Template_Engine.py — complete module
- Pattern extraction from verified proofs
- Parameterized template generation
- Template validation via re-verification
- Session-scoped template catalog

**Dependencies:** Phase E3 complete
**Validation:** Extract template from `mequiv_reflexive` proof pattern. Instantiate with different proposition. Re-verify instantiation compiles. Catalog correctly lists available templates.
**Governance gate:** Phase-3.1 compliance check — all templates carry source hash binding

### Phase E6: Abstraction Engine
**Duration estimate:** 3-4 days
**Deliverables:**
- EMP_Abstraction_Engine.py — complete module
- Theorem generalization (parameter substitution detection)
- Lemma suggestion (proof decomposition analysis)
- Cross-module pattern mining
- Complexity metrics

**Dependencies:** Phase E3 complete (E5 optional but beneficial)
**Validation:** Generalize `coherence_I1` to parameterized form. Suggest intermediate lemma for `global_bijection`. Mine patterns across baseline — identify modus ponens and case analysis frequencies. All candidates tagged UNVERIFIED until re-verified.
**Governance gate:** None (all outputs non-authoritative, discarded on verification failure)

### Phase E7: MSPC Coherence Witness Integration
**Duration estimate:** 2-3 days
**Deliverables:**
- EMP_MSPC_Witness.py — complete module
- Coherence request protocol (EMP → Logos Agent → MSPC → Logos Agent → EMP)
- Four-modality expressibility check interface
- CANONICAL_CANDIDATE gating logic in Meta Reasoner
- Updated STACK_POSITION.md with MSPC dependency

**Dependencies:** Phase E2 complete + MSPC Protocol operational
**Validation:** Submit verified PXL proof through witness. MSPC returns coherence result. Meta Reasoner promotes to CANONICAL_CANDIDATE only on COHERENT response. INCOHERENT response halts at VERIFIED_PXL.
**Governance gate:** Logos Agent must approve MSPC routing path (new inter-protocol communication via sovereign routing)

### Phase E8: Documentation and Manifest Updates
**Duration estimate:** 1 day
**Deliverables:**
- Updated MANIFEST.md — all new files listed
- Updated METADATA.json — `ready_for_deployment: true` (conditional on all phases passing)
- Updated RUNTIME_ROLE.md — reflect enhanced capabilities
- Updated GOVERNANCE_SCOPE.md — no scope changes, but explicit confirmation that Coq verification falls within "bounded epistemic tagging"
- Updated STACK_POSITION.md — PXL_Gate and MSPC dependencies declared

**Dependencies:** All prior phases complete
**Validation:** All documentation cross-references are consistent. MANIFEST inventory matches actual file listing.
**Governance gate:** Final audit — documentation-only

---

## 7. Total Effort and Critical Path

**Estimated total duration:** 18-26 days

**Critical path:** E1 → E2 → E3 → E5/E6 (parallel) → E7 → E8

**Phase E4 is independent** after E2 and can run in parallel with E3.

**Phase E7 is gated** on MSPC Protocol being operational. If MSPC is not ready, E7 defers and the system operates without CANONICAL_CANDIDATE classification (halts at VERIFIED_PXL maximum).

**Minimum viable capability:** Phases E1 + E2 + E4 deliver Coq-backed proof verification in the Nexus pipeline. This replaces the keyword-scanning stub with real verification in approximately 6-10 days.

---

## 8. Clever Use Cases Beyond Design Intent

### 8.1 Type-Driven Development Aid

Use EMP_Coq_Bridge to validate API contracts expressed as Coq type signatures. If a proposed interface change violates an existing type relationship, Coq rejects the compilation. This provides formal contract verification without runtime overhead.

### 8.2 Logical Consistency Auditing

Submit governance rules expressed in PXL as Coq propositions. If any governance artifacts contain contradictory requirements, Coq will fail to compile a consistency proof. This catches governance drift mechanically.

### 8.3 Semantic Version Control

Track logical implications of `.v` file changes. If a commit modifies an axiom, EMP_Proof_Index can immediately identify all downstream theorems affected. This is a semantic diff, not a textual diff.

### 8.4 Interactive Proof Assistant (jsCoq Path)

In browser environments via jsCoq WebAssembly, EMP provides real-time proof development feedback. Each keystroke can trigger incremental verification, enabling collaborative proof construction with immediate error localization.

### 8.5 Axiom Minimality Auditing

EMP_Abstraction_Engine can identify axioms that are never used in any verified proof, axioms that could be derived from other axioms (redundancy), and proofs that use more axioms than necessary. This supports ongoing PXL kernel refinement.

### 8.6 Cross-Domain Coherence Validation (via MSPC)

With MSPC as coherence witness, EMP can verify not just formal correctness but representational completeness — ensuring the formal system never outruns its ability to be explained, taught, or communicated. This is a unique capability arising from the Octafolium dual-compiler architecture.

---

## 9. Open Design Questions (Requiring Human Authority)

### 9.1 Coq Environment Path

Where does the Coq binary (coqc) or jsCoq runtime live relative to the LOGOS repository root? DRAC session reconstruction needs to know how to locate or provision the Coq environment.

### 9.2 Budget-to-Timeout Mapping

The existing `budget` parameter in EMP_Meta_Reasoner is an integer step count. How should this map to Coq compilation timeouts? Proposed: 1 budget unit = 1 second wall-clock for Coq subprocess. Requires explicit approval.

### 9.3 Proof Content Detection

The current keyword scan (`pxl`, `proof`, `axiom`, `wff`) is the fast-path trigger for Coq verification. Should this be replaced with a structural detector (e.g., presence of `.v` content or PXL formal syntax) to reduce false positives?

### 9.4 MSPC Operational Readiness

Phase E7 depends on MSPC being operational. What is the current MSPC build status and when will it be available for integration testing?

### 9.5 PXL Kernel Axiom Set

The VERIFIED_PXL classification requires all axioms to be in the "PXL kernel set." What is the canonical, exhaustive list of PXL kernel axioms? Currently inferred from PXLv3_SemanticModal.v but requires explicit declaration.

---

## 10. Relationship to Octafolium Architecture

Under the Octafolium rosette topology, EMP occupies one of the eight protocol positions on the perimeter. Its designated axis pairs it with MSPC through I2 mediation.

The EMP-MSPC coherence loop:
1. I2 + fractal TRI-CORE explores abstraction space, finds candidate claims
2. Ship to MSPC — formalize in NL + math + lambda + PXL simultaneously
3. Ship to EMP — CONC compiler works across three formal axes, produces multi-layer artifacts
4. Back to I2 — mediate via privation gating + bridge principle + Trinitarian optimization
5. Back to MSPC — diff comparison of what changed in the I2→EMP→I2 loop
6. Loop closes — MSPC validates whether the transformation was coherent

This forms a self-validating reasoning closure. EMP does not need temporal airlocking (pre/post isolation) because MSPC provides real-time semantic coherence witnessing. I2's native properties (privation gating, bridge principle, Trinitarian optimization) are part of the computation, not external constraints.

The enhanced EMP described in this blueprint is designed to fully support this loop at the proof verification layer. Phase E7 (MSPC Witness Integration) is the specific implementation point.

---

## 11. Success Criteria

- EMP_Coq_Bridge successfully compiles all 60 PXL_Gate .v files with correct structured output
- EMP_Meta_Reasoner correctly classifies proofs across all six tiers with no false promotions
- EMP_Proof_Index indexes the full PXL baseline and returns correct search results
- PostProcessGate produces Coq-verified AAs conforming to Shared AA Schema Appendix
- All EMP outputs fail closed on any error condition
- No governance regressions (all prohibitions preserved)
- MSPC coherence witness correctly gates CANONICAL_CANDIDATE status (Phase E7)
- Budget enforcement prevents unbounded Coq compilation
- Total build effort within 18-26 day estimate
- All new modules carry canonical headers per repo standard

---

## 12. Explicit Non-Goals

- No new governance artifacts or gates
- No new protocols (MSPC is separately defined)
- No external NLP libraries
- No probabilistic inference
- No autonomous reasoning in EMP
- No semantic reinterpretation of proof content
- No modification of SMP payloads
- No direct protocol-to-protocol communication (all routing via Logos Agent)
- No persistent state across sessions (index rebuilds per DRAC reconstruction)
- No modification of PXL_Gate .v source files

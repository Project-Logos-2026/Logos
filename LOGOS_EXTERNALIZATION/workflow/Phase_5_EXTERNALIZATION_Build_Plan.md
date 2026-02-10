# LOGOS Natural Language Externalization — Authoritative Build Plan

**Status:** Design-Only (Authoritative)
**Scope:** Complete NL externalization core — Layers 1 through 4
**Authority:** Conceptual design reference for downstream implementation
**Pipeline Position:** Claude (concept) → GPT (prompt engineering) → VS Code (mutation) → GitHub (canonical state)

---

## 1. Governing Premise

Natural language in LOGOS is a compile artifact. It is produced by a deterministic compiler operating over formally governed semantic inputs. It is not generated, inferred, or negotiated. It is rendered.

The externalization system does not participate in meaning, sequencing, approval, or audit. It receives a resolved semantic state and projects it into language. The projection is non-authoritative, replaceable, and validated against the formal artifacts it describes — never the reverse.

This build plan defines the complete construction of that projection system across four compositional layers, from atomic rendering units through multi-statement discourse assembly.

---

## 2. Architectural Foundation

### 2.1 What the Compiler Receives

The upstream system produces a **Resolved Output Packet** containing a closed set of inputs:

| Field | Source | Role |
|---|---|---|
| Meaning_State_Reference | Meaning Layer (SP + SR + SI) | Identifies what is true |
| Applied_Transformation_ID | Sequencing (TT-01 through TT-10, or null) | Identifies what changed |
| Arithmetic / Mathematical Expression | Ground truth checksum (L2) | Machine-verifiable truth |
| PXL Formalization | Formal proof artifact (L3) | Authority |
| Proof / Compile Status | PXL Gate | Epistemic status |
| Sequencing Termination Reason | Sequencing specification | Why processing halted |
| Audit_Record_Reference | Audit system | Traceability |

Missing any element halts externalization. This is fail-closed by contract.

### 2.2 What the Compiler Produces

The compiler emits:

- **Natural Language Surface Output** (L1) — one or more rendered sentences
- **Artifact Linkage Metadata** — references tying each NL clause to its L2/L3 sources
- **Consistency Declaration** — machine-readable attestation that NL was derived from, and validated against, authoritative artifacts

### 2.3 Directionality

The externalization boundary is read-only and non-causal. No signal propagates inward from rendering to meaning, sequencing, or audit. Authority decreases monotonically from left (PXL) to right (NL surface). This is not a design preference; it is a governance invariant.

---

## 3. The Four-Layer Compilation Model

Language is assembled through four compositional layers. Each layer is constructed, closed, and stabilized before the next layer begins. Lower layers are immutable once closed. Higher layers compose over lower layers but cannot modify them.

```
Layer 1: AXIOM        — atomic semantic units, deterministic rendering
Layer 2: MODIFIER     — qualifiers binding to axioms
Layer 3: CONTEXTUAL   — situational framing binding to axioms or modified axioms
Layer 4: DISCOURSE    — multi-statement assembly and coherence structures
```

This is analogous to building a type system before building a language: primitives first, then combinators, then context, then programs.

### 3.1 Compilation Sequence at Runtime

For any given Resolved Output Packet, the compiler:

1. Resolves the semantic state to one or more externalization primitives
2. Selects the corresponding AXIOM template(s) from the manifest
3. Validates template headers against the Header Schema
4. Confirms primitive identity and slot requirements against registries
5. Binds slot values from the packet's semantic content
6. Applies MODIFIER templates where binding constraints permit
7. Applies CONTEXTUAL templates where binding constraints permit
8. Assembles DISCOURSE structure if multi-statement output is required
9. Validates the rendered NL against L2 and L3 artifacts
10. Emits output with linkage metadata and consistency declaration

Every step is deterministic. Every step is auditable. Every step fails closed on missing data.

---

## 4. Artifact Authority Model

The externalization system is defined by five artifact classes with strict authority separation.

### 4.1 Registries (Authoritative — Source of Truth)

Registries define what exists. They enumerate the closed sets that all other artifacts reference.

**Semantic Lexicon Registry**
Defines every canonical externalization primitive. Each entry includes:
- Term and term_id (canonical identifier)
- Part of speech and natural language definition
- Lambda signature and role (semantic type)
- PXL grounding expression (formal anchor)
- PXL constraints (admissibility conditions)
- Status (canonical / deprecated / reserved)

The Semantic Lexicon Registry is the authoritative bridge between the Meaning Layer's Semantic Primitives (SP-01 through SP-12) and the externalization system's rendering vocabulary. Each externalization primitive maps to a specific configuration of SPs, SRs, and SSC classifications. This derivation is explicit and auditable.

**Template Type Registry (JSON)**
Defines the closed set of template roles and their compilation behavior:

| Type | Category | Priority | Composable | Sequence Class |
|---|---|---|---|---|
| AXIOM | Foundational | 1 | Yes | Base |
| MODIFIER | Qualifying | 2 | Yes | Dependent |
| CONTEXTUAL | Situational | 3 | Yes | Context |
| EXPLANATORY | Human-Facing | 4 | No | Terminal |

Runtime priority determines compilation order. Sequence class determines legal binding targets. EXPLANATORY templates are non-composable terminals that do not participate in logical composition — they exist for human-facing pedagogical output and are appended last, optionally.

**Slot Registry (JSON)**
Defines every semantic slot used by any template, plus the authoritative Primitive_Map that binds each primitive to its ordered slot set. The registry is append-only: future layers add new slots without modifying existing ones. Slot names are canonical, case-sensitive, and must resolve here for any template to be valid.

### 4.2 Schemas (Authoritative — Structural Requirements)

Schemas define what must be present for machine consumption and validation. They do not define what things mean — that is the registry's role.

**Externalization Header Schema (JSON)**
Defines the mandatory machine-readable header for every template:

| Field | Type | Constraint |
|---|---|---|
| Artifact_Type | string | Fixed: "Externalization_Template" |
| Template_Type | enum | AXIOM, MODIFIER, CONTEXTUAL, EXPLANATORY |
| Primitive | string | Must resolve in Semantic Lexicon Registry |
| Slots | ordered array | Must match Slot Registry Primitive_Map |
| Projection_Mode | string | Fixed: "Projection_Only" |
| Runtime_Eligible | boolean | Compiler visibility flag |
| Schema_Version | string | Fixed: "1.0" |

No optional fields. No additional fields permitted. No development-phase identifiers.

**Template Manifest Schema (JSON)**
Defines the structure for all manifests. Manifests must contain metadata (name, type, referenced contracts) and template entries (ID, filename, type, primitive, slots, runtime eligibility). The schema enforces that manifests are declarative and non-authoritative — they are indexes, not definitions.

**Semantic Registry Schema (JSON)**
Defines the structural requirements for the Semantic Lexicon Registry itself: required fields per entry, allowed values for part_of_speech and lambda_role, pattern constraints on term_ids, and the prohibition on additional properties.

### 4.3 Manifests (Non-Authoritative — Discovery Index)

Manifests are lookup surfaces. They allow a compiler to discover what templates exist, what primitives they serve, and what slots they require — without scanning the filesystem or parsing every template file. They are generated from, and validated against, the authoritative registries and schemas. They carry no authority of their own.

Each template type layer produces its own manifest (e.g., `Axiom_Template_Manifest.json`). Manifests are JSON-only. Manifest entries must correspond to existing template files and must not introduce new primitives, types, or slot semantics.

### 4.4 Templates (Renderable Output Forms)

Templates are the rendering endpoint. Each template is a single file containing:

- A JSON header conforming to the Header Schema
- A text body containing slot placeholders (e.g., `{ASSERTION_CONTENT}`)

The body is the natural language surface form. It is parameterized by slots and rendered by substitution. The compiler reads the header, validates it, resolves the primitive and slots against registries, binds values, and produces deterministic output.

Templates are built so that:
- Every rendered sentence traces to exactly one template
- Every template traces to exactly one primitive
- Every primitive traces to the Semantic Lexicon Registry
- Every slot traces to the Slot Registry

Nothing is hidden. Nothing is inferred. Nothing is invented.

### 4.5 Contracts (Interface Descriptions)

Contracts describe how externalization integrates with other system components. They are human-readable descriptions of interface expectations. They are not authoritative compared to schemas and registries. Over time, they may migrate to machine-readable JSON interface contracts. Contracts explain behavior; schemas enforce structure.

---

## 5. Bindings as Structural Invariants

Bindings are not a layer. Bindings are not a phase. Bindings are not an artifact family.

Bindings are structural invariants enforced at layer boundaries. They define legal attachments between template types:

| Binding | Source | Target | Enforcement |
|---|---|---|---|
| Modifier → Axiom | MODIFIER template | AXIOM template (or previously modified AXIOM if schema permits) | Schema-level compatibility constraint |
| Context → Axiom/Modified | CONTEXTUAL template | AXIOM or MODIFIER-applied AXIOM | Schema-level target restriction + ordering constraint |
| Statement → Statement | DISCOURSE template | Any compiled statement | Discourse assembly constraint |

Bindings are represented as:
- Schema constraints (which template types may attach to which)
- Compatibility metadata (which specific primitives accept which modifier types)
- Allowed-target rules (enumerated legal attachment points)
- Ordering rules (modifiers before contexts; contexts before discourse assembly)

This prevents the common failure mode of treating "binding" as a whole development phase with its own artifact explosion. The binding rules live in the schemas that govern each layer's templates. They are validated at compile time, not at authoring time.

---

## 6. Layer-by-Layer Build Specification

### 6.1 Layer 1 — AXIOM (Closed)

**Purpose:** Atomic semantic rendering units. Each template expresses exactly one externalization primitive with deterministic slot substitution.

**Completed artifacts:**
- 22 AXIOM templates covering the full externalization primitive set
- Each template has: canonical header, primitive binding, ordered slot placeholders, deterministic body text
- Slot Registry with complete Primitive_Map (22 primitives → ordered slots)
- Axiom Template Manifest (22 entries, validated against registries)
- Template Type Registry (4 types defined)
- Externalization Header Schema (7 required fields, no optionals)
- Template Manifest Schema
- Semantic Lexicon Registry (22 entries with lambda signatures, PXL grounding)

**Primitive coverage:**

| Category | Primitives |
|---|---|
| Assertion states | ASSERTION_CONFIRMED, ASSERTION_NEGATED, ASSERTION_UNPROVEN |
| Conditional states | CONDITIONAL_SATISFIED, CONDITIONAL_UNSATISFIED |
| Proof states | PROOF_CONFIRMED, PROOF_FAILED |
| Validation states | VALIDATION_INCOMPLETE |
| Scope operations | SCOPE_LIMITATION, SCOPE_VIOLATION |
| Dependency operations | DEPENDENCY_DISCLOSURE, DEPENDENCY_UNSATISFIED |
| Precondition operations | PRECONDITIONS_REQUIRED, PRECONDITIONS_UNMET |
| Constraint operations | CONSTRAINT_DISCLOSURE, CONSTRAINT_VIOLATED |
| Audit operations | AUDIT_PASSED, AUDIT_FAILED |
| Reference operations | ARTIFACT_REFERENCE |
| Explanation types | TECHNICAL_EXPLANATION, DECLARATIVE_EXPLANATION, PEDAGOGICAL_EXPLANATION |

**Closure criteria (met):**
- Every primitive in the Semantic Lexicon Registry has exactly one AXIOM template
- Every template header validates against the Header Schema
- Every template's primitive resolves in the Semantic Lexicon Registry
- Every template's slots match the Slot Registry Primitive_Map
- Manifest entries correspond 1:1 with template files
- No phase terminology in machine-readable artifacts
- Audit trail documented

**Layer 1 invariants (immutable going forward):**
- No existing AXIOM template may be modified
- No existing slot may be redefined
- No existing primitive may be renamed or reinterpreted
- New primitives require explicit governance authorization

### 6.2 Layer 2 — MODIFIER (Next)

**Purpose:** Qualify, constrain, or adjust AXIOM output without introducing new assertions. Modifiers never stand alone. They attach to an AXIOM template's rendered output and transform its surface form within semantic bounds.

**Modifier function categories:**

**Negation/Polarity:**
Inverts or conditions the polarity of an axiom's assertion. Example: an ASSERTION_CONFIRMED axiom modified to express conditional confirmation, or a PROOF_CONFIRMED axiom modified to express confirmation with caveats. The modifier does not negate the underlying semantic state — that is the meaning layer's job. The modifier expresses nuance in the *rendering* of an already-determined state.

**Epistemic qualification:**
Adds certainty/uncertainty markers to rendered output. Driven by Proof/Compile Status and SSC classification from the Resolved Output Packet. When proof status is anything other than fully compiled/verified, the modifier enforces explicit epistemic qualifiers in the surface form (per SI-09: explicit uncertainty and unknowns).

**Scope restriction:**
Narrows the apparent scope of a rendered assertion. The scope is already determined by the meaning state — the modifier makes scope bounds explicit in the NL surface. Driven by SP-11 (Scope) configuration in the packet.

**Strength/confidence:**
Modulates the assertoric force of the rendered output. "X is the case" vs. "X appears to be the case" vs. "X is provisionally the case." Again, determined by upstream semantic state — the modifier selects among pre-authored surface variants.

**Deliverables:**

| Artifact | Description |
|---|---|
| Modifier templates | One per modifier function × applicable axiom category |
| Modifier slot additions | Appended to Slot Registry (append-only) |
| Modifier Template Manifest | JSON, conforming to Template Manifest Schema |
| Binding constraints | Schema-level rules defining legal modifier → axiom attachments |
| Compatibility metadata | Which modifier types apply to which primitive categories |

**Design constraints:**
- Modifier templates must reference a parent AXIOM (by primitive category, not by individual template ID — this keeps the binding space manageable)
- Modifiers must not introduce new primitives
- Modifier slots are additive to the Slot Registry; existing slots remain untouched
- Binding constraints are encoded in schema, not in templates
- The set of modifier functions is finite and closed per layer

**Build sequence:**
1. Enumerate modifier functions against the primitive categories (not against individual primitives — this prevents a 22 × N explosion)
2. Define modifier slots and append to Slot Registry
3. Author modifier templates with headers conforming to the Header Schema (Template_Type: MODIFIER)
4. Define binding constraints as schema-level rules
5. Generate Modifier Template Manifest
6. Validate all artifacts against registries and schemas
7. Audit and close

**Estimated effort:** 3–4 weeks. The modifier set is smaller than the axiom set because modifiers operate on primitive *categories* (assertion, proof, scope, dependency, constraint, audit, explanation) rather than individual primitives.

### 6.3 Layer 3 — CONTEXTUAL

**Purpose:** Introduce situational framing to rendered output without mutating truth content. Contextual templates wrap axiom output (possibly already modified) in temporal, epistemic, domain, or operational frames.

**Contextual function categories:**

**Temporal framing:**
"As of [timestamp]," "At the time of [event]," "Prior to [operation]." Driven by audit timestamps and sequencing records in the Resolved Output Packet. The temporal frame does not assert that something was true at a time — it frames the rendering within the time at which the semantic state was resolved.

**Epistemic framing:**
"Given evidence [E]," "Under the assumption that [A]." Driven by grounding relations (SP-12 Grounding) and dependency chains (SP-05 Dependency) in the meaning state. Makes the epistemic basis of the assertion explicit in the surface form.

**Domain framing:**
"Within scope [S]," "For domain [D]," "Subject to [boundary]." Driven by SP-11 (Scope) and scope-related primitives (SCOPE_LIMITATION, SCOPE_VIOLATION). Renders the declared scope boundaries as explicit surface-level frames.

**Operational framing:**
"During [operation]," "As part of [process]," "In response to [trigger]." Driven by the Applied_Transformation_ID and Sequencing_Termination_Reason fields of the Resolved Output Packet.

**Deliverables:**

| Artifact | Description |
|---|---|
| Contextual templates | One per context function × applicable scope |
| Contextual slot additions | Appended to Slot Registry |
| Contextual Template Manifest | JSON |
| Binding constraints | Context → Axiom/Modified Axiom target rules |
| Ordering constraints | Context applied after modifiers; stacking rules if multiple contexts permitted |

**Design constraints:**
- Contextual templates must not alter logical truth
- Context attaches to axiom or modified axiom — never to another context directly (stacking, if permitted, is mediated by the compiler, not by inter-template references)
- Contextual slots follow the same append-only policy
- Ordering: AXIOM → MODIFIER → CONTEXTUAL is the canonical compilation sequence

**Build sequence:**
1. Enumerate context functions against the packet fields that drive them
2. Define contextual slots and append to Slot Registry
3. Author contextual templates
4. Define binding and ordering constraints in schema
5. Generate manifest, validate, audit, close

**Estimated effort:** 3–4 weeks. Contextual templates are structurally simpler than modifiers (they wrap rather than transform) but require careful alignment with packet field semantics.

### 6.4 Layer 4 — DISCOURSE

**Purpose:** Multi-statement assembly and coherence structures. Discourse templates compose multiple compiled statements (axiom + modifiers + context) into structured, coherent language output.

**Discourse function categories:**

**Explanation chains:**
Ordered sequences where each statement builds on the previous. "X is the case. This follows from Y. Y was established because Z." The ordering is not narrative — it mirrors the dependency structure of the meaning state (SP-05 Dependency acyclicity).

**Argument flows:**
Structured presentations of premises, inference steps, and conclusions. Driven by the transformation chain recorded in the audit trail. Each step in the flow corresponds to a specific TT application with its PXL anchor.

**Pedagogical progressions:**
Graduated explanations that introduce concepts in dependency order, with explicit transition markers. Used when the EXPLANATORY template type is active. These are terminal, non-composable, and do not participate in logical composition.

**Contrastive structures:**
"X holds, but Y does not." "Under scope S, X is the case; outside scope S, X is not established." Driven by multiple meaning states or by scope-differentiated assertions within a single packet.

**Deliverables:**

| Artifact | Description |
|---|---|
| Discourse templates | Assembly patterns for each discourse function |
| Discourse slot additions | Appended to Slot Registry (likely minimal — most slots are inherited from Layers 1–3) |
| Discourse Template Manifest | JSON |
| Assembly constraints | Ordering rules, aggregation rules, reference binding rules |
| Statement-to-statement binding rules | How compiled statements may be composed |

**Design constraints:**
- Discourse assembly is deterministic — given the same set of compiled statements and the same assembly rule, the output is identical
- No probabilistic heuristics for ordering, selection, or presentation
- Pronoun resolution is out of scope initially — discourse uses explicit identifiers (primitive IDs, artifact references) rather than anaphoric binding
- The EXPLANATORY template type integrates at this layer as a terminal, non-composable attachment

**Build sequence:**
1. Define discourse functions against the Resolved Output Packet's multi-statement scenarios
2. Define assembly constraints (ordering, aggregation)
3. Author discourse templates as composition patterns over Layer 1–3 outputs
4. Define statement-to-statement binding rules
5. Generate manifest, validate, audit, close

**Estimated effort:** 4–6 weeks. Discourse is the most complex layer because it operates over composed outputs rather than individual primitives. The key risk is under-constraining assembly (allowing nonsensical compositions) or over-constraining it (making multi-statement output impossible for valid meaning states).

---

## 7. Validation Architecture

### 7.1 Compile-Time Validation (Per Template)

Every template, at authoring time, must pass:

1. **Header schema conformance** — all 7 required fields present, no extras, correct types
2. **Primitive resolution** — Primitive field resolves in Semantic Lexicon Registry
3. **Slot resolution** — Slots field matches Slot Registry Primitive_Map for the declared primitive, in order
4. **Template type resolution** — Template_Type field resolves in Template Type Registry
5. **Manifest consistency** — template is listed in the correct manifest with matching metadata

Failure on any check is fatal. The template is not valid and must not be committed.

### 7.2 Runtime Validation (Per Rendered Output)

Every rendered NL output, at compilation time, must pass:

**Check 1 — Structural coverage.**
Every semantic element in the Resolved Output Packet must have a corresponding rendered clause. Every rendered clause must trace to exactly one template invocation. This is a bijective coverage check. Implementation: each template invocation logs its source content unit. Post-compilation, verify all units covered and no orphan clauses exist.

**Check 2 — Arithmetic shadow consistency.**
The packet's Arithmetic/Mathematical Expression (L2) is the ground truth checksum. Any quantitative claims in the NL output are extracted and compared against L2. Mismatch is fatal — NL is rejected, artifacts are preserved.

**Check 3 — Semantic predicate alignment.**
Because every clause is generated from a known template with known slots, the reverse mapping from NL clause to source primitive + slot values is deterministic. If any clause cannot be reverse-mapped, validation fails.

**Check 4 — Epistemic qualifier enforcement.**
When Proof/Compile Status is anything other than COMPILED/VERIFIED, the NL output must contain an explicit epistemic qualifier. The validator checks for its presence.

**Failure behavior:**
On any check failure, the NL output is discarded. The compiler may retry with an alternative template variant (if variants exist for the given primitive and modifier configuration), up to a configurable retry limit (default: 1). If retries exhaust, output emission halts with a FAILED Consistency Declaration specifying which check failed. The Resolved Output Packet is never modified. Silence is preferred over invalid language.

---

## 8. Cross-Artifact Consistency Model

Every rendered sentence can be validated by walking the artifact graph:

```
Rendered NL clause
  └─ Template file (body with filled slots)
       └─ Template header
            ├─ Primitive → resolves in Semantic Lexicon Registry
            │     └─ PXL grounding → anchors to PXL_Gate proof artifacts
            ├─ Slots → resolves in Slot Registry Primitive_Map
            ├─ Template_Type → resolves in Template Type Registry
            │     └─ Compilation sequence, binding rules
            └─ Schema_Version → validates against Header Schema
       └─ Manifest entry (non-authoritative index)
            └─ Validates against Template Manifest Schema
```

This graph is the formal guarantee of traceability. A compiler can walk it forward (from registries to rendered output) for compilation, or backward (from rendered output to registries) for audit.

---

## 9. Lambda Calculus Alignment

The externalization system admits a clean lambda calculus interpretation:

| NL Externalization Concept | Lambda Calculus Analog |
|---|---|
| Externalization primitive | Semantic constructor |
| Slot | Typed parameter |
| AXIOM template | Base render function: `λ(slot₁, slot₂, ...) → NL string` |
| MODIFIER template | Higher-order function: `λ(axiom_output, mod_slots) → modified NL string` |
| CONTEXTUAL template | Wrapper function: `λ(compiled_output, ctx_slots) → framed NL string` |
| DISCOURSE template | Composition function: `λ(stmt₁, stmt₂, ..., assembly_rule) → structured NL` |
| Binding constraint | Type constraint on function application |
| Compilation | Staged evaluation under typed constraints |

This alignment is not cosmetic. It means the system can be formalized as a simply-typed lambda calculus where:
- Well-typedness guarantees that only legal compositions are expressible
- Evaluation (compilation) is normalizing — it terminates
- The type system (binding constraints) prevents ill-formed output at the structural level

This does not require implementing a lambda calculus evaluator. It means the design *admits* one, which provides a formal correctness argument for the compilation model.

---

## 10. Tooling and Process Governance

### 10.1 Prompt Engineering Discipline

All VS Code prompts are:
- Script-only (no mixed prose/command)
- Deterministic (same input → same mutation)
- Fail-closed (missing authorities halt execution)
- Explanation-separated (commentary in chat, not in scripts)

This is not a style preference. It is a governance requirement. Mixed prompts introduce ambiguity that downstream tooling (GPT-mediated) cannot reliably resolve.

### 10.2 Audit Trail

Every layer closure produces:
- A validation report confirming registry/schema/manifest/template consistency
- A slot update report documenting any append-only additions
- A phase terminology audit confirming no development-internal language in machine-readable artifacts

Audit reports are written to `_Audit_Reports/` within the externalization directory.

### 10.3 Mutation Policy

- Registries: append-only (new entries permitted; existing entries immutable)
- Schemas: immutable once approved (version bump required for changes)
- Manifests: regenerated per layer closure (non-authoritative, derived from registries)
- Templates: immutable once layer is closed
- Slots: append-only (new slots for new layers; existing slots frozen)

---

## 11. Development Roadmap

| Step | Layer | Status | Estimated Effort | Key Dependencies |
|---|---|---|---|---|
| 1 | AXIOM | **Closed** | Complete | None |
| 2 | MODIFIER | Next | 3–4 weeks | Layer 1 closure; binding constraint schema design |
| 3 | CONTEXTUAL | Queued | 3–4 weeks | Layer 2 closure; ordering constraint schema design |
| 4 | DISCOURSE | Queued | 4–6 weeks | Layer 3 closure; assembly constraint design |

**Total estimated build time: 10–14 weeks from Step 2 start to full Layer 4 closure.**

Each step follows the same internal sequence:
1. Enumerate functions against the appropriate driving inputs
2. Define new slots (append-only)
3. Author templates with validated headers
4. Define binding/ordering/assembly constraints in schema
5. Generate manifest
6. Validate all artifacts against registries and schemas
7. Audit and close

No step may begin until the previous step is closed and audited.

---

## 12. LLM-Assisted Rendering (Optional, Constrained)

An LLM may be used as a rendering polish layer under the following non-negotiable conditions:

1. **Second-pass only.** The LLM receives already-validated NL output from the deterministic compiler. It never receives the Resolved Output Packet directly.
2. **Surface variation only.** The LLM may rephrase for tone and fluency. It may not add, remove, or reinterpret content.
3. **Full validation required.** LLM output goes through all four runtime validation checks before emission. Fail-closed.
4. **Non-authoritative.** LLM-polished output is explicitly marked as non-authoritative in the Consistency Declaration.
5. **Removable.** Removal of the LLM layer must not affect correctness, auditability, or provability. The deterministic compiler's output must always be a valid fallback.

The LLM is a renderer, not a reasoner. It has no access to meaning, sequencing, approval, or audit. It sees language and produces language. It is replaceable by construction.

---

## 13. Risk Registry

| Risk | Severity | Mitigation |
|---|---|---|
| Modifier × primitive combinatorial explosion | Medium | Bind modifiers to primitive *categories*, not individual primitives |
| Binding under-constraint (nonsensical compositions) | Medium | Explicit compatibility metadata per modifier/context type |
| Binding over-constraint (valid compositions blocked) | Medium | Test each layer against synthetic Resolved Output Packets before closure |
| Schema drift between JSON and any legacy markdown schemas | High | Deprecate markdown schemas; JSON schemas are sole authority |
| Phase terminology leaking into runtime artifacts | Low (mitigated) | Automated audit grep at each layer closure |
| Discourse assembly non-determinism | Medium | Assembly rules must be total functions over compiled statement sets — no heuristic selection |
| Externalization primitives disconnected from Meaning Layer SPs | High (mitigated) | Explicit derivation mapping in Semantic Lexicon Registry (PXL grounding + lambda signatures) |
| Template body semantic drift from header declaration | Low | Reverse-mapping validation at compile time (Check 3) |

---

## 14. Success Criteria

When all four layers are closed:

- Every externalization primitive has at least one AXIOM template
- Every AXIOM template can be modified by at least one MODIFIER template
- Every compiled statement can be contextually framed
- Multi-statement scenarios can be assembled into coherent discourse
- Every rendered sentence traces through the artifact graph to a PXL-grounded primitive
- Every rendered output passes all four validation checks
- The entire rendering system is removable without affecting the truth engine's correctness
- No NL artifact carries authority, introduces meaning, triggers sequencing, or bypasses audit

Language is a projection. The projection is complete. The truth engine does not depend on it.
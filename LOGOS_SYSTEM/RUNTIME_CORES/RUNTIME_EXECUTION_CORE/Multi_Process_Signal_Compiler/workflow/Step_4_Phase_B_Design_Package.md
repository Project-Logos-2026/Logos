# STEP 4 · PHASE B — DISCOURSE TEMPLATES & MANIFESTS
# COMPLETE DESIGN PACKAGE

Status: DESIGN COMPLETE — READY FOR GPT TRANSLATION
Layer: 4 — DISCOURSE
Authority: LOGOS Externalization Governance
Dependencies: Phase A (APPROVED), Header Schema v1.1 (DECLARED)

---

## PRE-PHASE-B RESOLUTION

Header Schema v1.1 declared. Change log:
- From: 1.0
- To: 1.1
- Change: Template_Type.Allowed_Values extended with "DISCOURSE"
- Scope: Enumerated value extension only
- Backward compatibility: Preserved
- Artifact: Externalization_Header_Schema_v1.1.json

---

## SECTION 1 — DISCOURSE TEMPLATE DESIGN PATTERNS

### 1.0 Common Properties

All discourse templates share:
- Template_Type: DISCOURSE
- Composable: true (Sequence_Class: NonTerminal, Runtime_Priority: 5)
- Projection_Mode: Projection_Only
- Not used in logical inference
- Does not alter compiled statement content
- EXPLANATORY attachment: permitted on all four, always terminal, preceded by EXPLANATORY_BOUNDARY
- Primitive field resolves to the discourse function entry in Semantic Lexicon Registry
- Slots: [DISCOURSE_FUNCTION_ID, ASSEMBLY_STATEMENT_COUNT, ORDERING_SOURCE]
- Schema_Version: 1.1

### 1.1 EXPLANATION_CHAIN

Role: Compositional, non-terminal.
Input: Minimum 2 compiled statements with resolved dependency positions.
Markers: DEPENDENCY_TRANSITION, GROUNDING_TRANSITION, EXPLANATORY_BOUNDARY.

Rendering pattern:
```
[CS at position 0 per topological sort + lexicographic tie-break on term_id]
{DEPENDENCY_TRANSITION | GROUNDING_TRANSITION}
[CS at position 1]
{DEPENDENCY_TRANSITION | GROUNDING_TRANSITION}
...
[CS at position N-1]
{EXPLANATORY_BOUNDARY}
[EXPLANATORY output]
```

Marker selection: SR-01 (grounds) → GROUNDING_TRANSITION (priority 1). SR-04 (depends_on) → DEPENDENCY_TRANSITION (priority 2). No direct relation → DEPENDENCY_TRANSITION (default).

### 1.2 ARGUMENT_FLOW

Role: Compositional, non-terminal.
Input: Minimum 2 compiled statements with audit trail transformation sequence.
Markers: PREMISE_BOUNDARY, INFERENCE_STEP_TRANSITION, CONCLUSION_BOUNDARY, EXPLANATORY_BOUNDARY.

Rendering pattern:
```
{PREMISE_BOUNDARY}
[CS — premise, position 0 in audit trail]
{INFERENCE_STEP_TRANSITION}
[CS — inference step, position 1]
...
{CONCLUSION_BOUNDARY}
[CS — conclusion, final position per Sequencing_Termination_Reason]
{EXPLANATORY_BOUNDARY}
[EXPLANATORY output]
```

Marker selection: PREMISE_BOUNDARY before first CS. CONCLUSION_BOUNDARY before final CS (conclusion). INFERENCE_STEP_TRANSITION between all other consecutive CSs. Ordering is exact audit trail sequence.

### 1.3 PEDAGOGICAL_PROGRESSION

Role: Compositional, non-terminal.
Input: Minimum 2 compiled statements with at least one grounding-level statement (depth 0).
Markers: TIER_BOUNDARY, PEDAGOGICAL_TRANSITION, GROUNDING_TRANSITION, EXPLANATORY_BOUNDARY.

Rendering pattern:
```
[CS depth 0, position 0]
{PEDAGOGICAL_TRANSITION | GROUNDING_TRANSITION}
[CS depth 0, position 1]
{TIER_BOUNDARY}
[CS depth 1, position 0]
{PEDAGOGICAL_TRANSITION | GROUNDING_TRANSITION}
[CS depth 1, position 1]
{TIER_BOUNDARY}
...
{EXPLANATORY_BOUNDARY}
[EXPLANATORY output]
```

Marker selection within tier: SR-01 → GROUNDING_TRANSITION (priority 1), else PEDAGOGICAL_TRANSITION (default). Between tiers: TIER_BOUNDARY inserted exactly once at each depth increment.

### 1.4 CONTRASTIVE_STRUCTURE

Role: Compositional, non-terminal.
Input: Minimum 2 compiled statements differing on truth value, scope, SSC, or proof status.
Markers: CONTRASTIVE_CONNECTIVE, SCOPE_BOUNDARY_MARKER, PAIR_SEPARATOR, EXPLANATORY_BOUNDARY.

Rendering pattern (scope-differentiated):
```
{SCOPE_BOUNDARY_MARKER}
[CS — affirmed / stronger / scope A]
{CONTRASTIVE_CONNECTIVE}
[CS — negated / weaker / scope B]
{PAIR_SEPARATOR}
{SCOPE_BOUNDARY_MARKER}
[CS — pair 2 affirmed]
{CONTRASTIVE_CONNECTIVE}
[CS — pair 2 contrasted]
{EXPLANATORY_BOUNDARY}
[EXPLANATORY output]
```

Rendering pattern (non-scope):
```
[CS — affirmed]
{CONTRASTIVE_CONNECTIVE}
[CS — contrasted]
{PAIR_SEPARATOR}
...
{EXPLANATORY_BOUNDARY}
[EXPLANATORY output]
```

SCOPE_BOUNDARY_MARKER present only when differentiating attribute is scope. Affirmed-first within pairs.

---

## SECTION 2 — SLOT ANALYSIS

3 new slots appended. No existing slots modified.

| Slot Name | Slot_Type | Description |
|---|---|---|
| DISCOURSE_FUNCTION_ID | Identifier | Canonical identifier of the applied discourse function |
| ASSEMBLY_STATEMENT_COUNT | Text | Count of compiled statements in the assembly |
| ORDERING_SOURCE | Identifier | Ordering authority used for the assembly |

4 new Primitive_Map entries (all share same slot signature):
- EXPLANATION_CHAIN → [DISCOURSE_FUNCTION_ID, ASSEMBLY_STATEMENT_COUNT, ORDERING_SOURCE]
- ARGUMENT_FLOW → [DISCOURSE_FUNCTION_ID, ASSEMBLY_STATEMENT_COUNT, ORDERING_SOURCE]
- PEDAGOGICAL_PROGRESSION → [DISCOURSE_FUNCTION_ID, ASSEMBLY_STATEMENT_COUNT, ORDERING_SOURCE]
- CONTRASTIVE_STRUCTURE → [DISCOURSE_FUNCTION_ID, ASSEMBLY_STATEMENT_COUNT, ORDERING_SOURCE]

Artifacts: Slot_Registry_Discourse_Addendum.json

4 new Semantic Lexicon Registry entries (composition-level primitives):
- EXPLANATION_CHAIN, ARGUMENT_FLOW, PEDAGOGICAL_PROGRESSION, CONTRASTIVE_STRUCTURE

Artifacts: Semantic_Lexicon_Registry_Discourse_Addendum.json

---

## SECTION 3 — DISCOURSE TEMPLATE MANIFEST

Manifest: Discourse_Template_Manifest.json
Conformance: Template_Manifest_Schema.json
Entries: 4 (one per discourse function, 1:1 correspondence with template files)

Template ID → File Name mapping:
- DISCOURSE_01_EXPLANATION_CHAIN → DISCOURSE_01_EXPLANATION_CHAIN.md
- DISCOURSE_02_ARGUMENT_FLOW → DISCOURSE_02_ARGUMENT_FLOW.md
- DISCOURSE_03_PEDAGOGICAL_PROGRESSION → DISCOURSE_03_PEDAGOGICAL_PROGRESSION.md
- DISCOURSE_04_CONTRASTIVE_STRUCTURE → DISCOURSE_04_CONTRASTIVE_STRUCTURE.md

Target path: LOGOS_EXTERNALIZATION/Templates/DISCOURSE/

---

## SECTION 4 — VALIDATION & AUDIT EXPECTATIONS

### 4.1 Compile-Time Checks (Per Template)

C1: Header Schema v1.1 conformance (7 required fields, Template_Type=DISCOURSE)
C2: Primitive resolves in Semantic Lexicon Registry
C3: Slots match Slot Registry Primitive_Map
C4: Template_Type resolves in Template_Type_Registry (Composable=true, NonTerminal, Priority=5)
C5: Manifest entry exists with matching metadata
C6: All markers in template body are legal per Assembly Constraint Schema
C7: All required markers for the function are present in template body

### 4.2 Runtime Checks (Per Assembled Block)

R1: Structural coverage — bijective CS ↔ packet scope mapping
R2: Ordering correctness — valid total order per function-specific rules
R3: Marker placement — correct per Marker Selection Table
R4: EXPLANATORY terminal enforcement — after final CS, one EXPLANATORY_BOUNDARY
R5: Immutability — CSs byte-identical to Layer 1-3 output
R6: Single-function — one discourse function per block

Failure: discard output, retry (limit 1), halt with FAILED Consistency Declaration.

---

## SECTION 5 — STEP 4 CLOSURE CRITERIA

### Immutable at closure:
- Externalization_Header_Schema v1.1
- Discourse_Assembly_Constraint_Schema v1.0
- Discourse_Function_Registry
- Discourse_Marker_Selection_Table
- Discourse_Template_Manifest
- All 4 DISCOURSE templates
- 4 Semantic Lexicon Registry entries (discourse primitives)
- 3 Slot Registry entries (discourse slots)
- 4 Primitive_Map entries (discourse primitives)

### Append-only:
- Slot Registry (overall)
- Template Type Registry
- Semantic Lexicon Registry (overall)

### Required audit reports:
1. Step 4 Compile-Time Validation Report (C1-C7 pass)
2. Step 4 Slot Audit Report (3 new, 0 modified)
3. Step 4 Schema Change Report (1.0 → 1.1)
4. Step 4 Terminology Audit (no phase terminology)
5. Step 4 Manifest Consistency Report (4 entries ↔ 4 files)
6. Step 4 Cross-Reference Integrity Report (all references resolve)

### Risks eliminated:
- Heuristic ordering → total deterministic functions
- Semantic inference → opaque CS handling
- CS mutation → byte-identity verification
- Non-deterministic markers → total selection function
- Cross-packet assembly → homogeneity constraint
- EXPLANATORY composition → terminal enforcement
- Header desynchronization → v1.1 bump
- Anaphoric binding → explicit prohibition

### Closure statement:
"Step 4 — DISCOURSE is formally CLOSED. The four-layer externalization compiler is complete. No Layer 1-4 artifact may be modified without explicit governance reauthorization."

---

## ARTIFACT INVENTORY

Files produced by this design:

1. Externalization_Header_Schema_v1.1.json — Schema (version bump)
2. Discourse_Function_Registry.json — Registry (new)
3. Discourse_Assembly_Constraint_Schema.json — Schema (promoted from DRAFT-1.0)
4. Discourse_Marker_Selection_Table.json — Registry (new)
5. Discourse_Template_Manifest.json — Manifest (new)
6. Slot_Registry_Discourse_Addendum.json — Addendum (append-only)
7. Semantic_Lexicon_Registry_Discourse_Addendum.json — Addendum (append-only)

Templates (to be authored per these patterns):
8. DISCOURSE_01_EXPLANATION_CHAIN.md
9. DISCOURSE_02_ARGUMENT_FLOW.md
10. DISCOURSE_03_PEDAGOGICAL_PROGRESSION.md
11. DISCOURSE_04_CONTRASTIVE_STRUCTURE.md

---

## PHASE B COMPLETE. NO FURTHER WORK AUTHORIZED ON THIS LAYER WITHOUT GOVERNANCE REVIEW.

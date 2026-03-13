# ARP Reconstruction Directive — Baseline Engine Construction

```
Artifact Type   : Reconstruction Strategy Directive
Target System   : Advanced Reasoning Protocol (ARP)
Pipeline Phase  : Phase-4 Pre-Construction
Directive ID    : ARP-RD-001
Generated       : 2026-03-12
Status          : APPROVED FOR PHASE-4 CONSTRUCTION
Engine Count    : 25 reasoning engines + 3 hub modules
```

---

## SECTION 0 — Reconstruction Summary

| # | Engine | Layer | Group | Tier | Atoms | Src Mods | Est. Lines | New Code | Priority |
|---|--------|-------|-------|------|-------|----------|-----------|---------|---------|
| 1 | `Bayesian_Reasoning_Engine` | 1 | PROBABILISTIC | **A** | 0 | 0 | 350-420 | ~25% | 1 |
| 2 | `Consistency_Reasoning_Engine` | 1 | LOGICAL | **A** | 0 | 0 | 250-340 | ~45% | 2 |
| 3 | `Topological_Reasoning_Engine` | 1 | STRUCTURAL | **A** | 0 | 0 | 300-400 | ~40% | 3 |
| 4 | `Graph_Reasoning_Engine` | 1 | STRUCTURAL | **A** | 0 | 0 | 280-360 | ~55% | 4 |
| 5 | `Ontological_Reasoning_Engine` | 1 | SEMANTIC | **A** | 0 | 0 | 300-420 | ~50% | 5 |
| 6 | `Logical_Coherence_Engine` | 2 | LOGICAL | B | 0 | 0 | 350-480 | ~50% | 6 |
| 7 | `Structural_Systems_Engine` | 2 | STRUCTURAL | B | 0 | 0 | 380-520 | ~55% | 7 |
| 8 | `Causal_Reasoning_Engine` | 1 | PROBABILISTIC | B | 0 | 0 | 220-320 | ~60% | 8 |
| 9 | `Deductive_Reasoning_Engine` | 1 | LOGICAL | B | 0 | 0 | 280-380 | ~55% | 9 |
| 10 | `Invariant_Reasoning_Engine` | 1 | LOGICAL | B | 0 | 0 | 200-300 | ~50% | 10 |
| 11 | `Causal_Dynamics_Engine` | 2 | PROBABILISTIC | B | 0 | 0 | 320-440 | ~65% | 11 |
| 12 | `Abductive_Reasoning_Engine` | 1 | LOGICAL | B | 0 | 0 | 240-320 | ~60% | 12 |
| 13 | `Analogical_Reasoning_Engine` | 1 | SEMANTIC | B | 0 | 0 | 220-320 | ~60% | 13 |
| 14 | `Relational_Dependency_Reasoning_Engine` | 1 | STRUCTURAL | B | 0 | 0 | 280-380 | ~55% | 14 |
| 15 | `Complexity_Analysis_Engine` | 1 | PATTERN | B | 0 | 0 | 200-300 | ~55% | 15 |
| 16 | `Dynamic_Pattern_Engine` | 2 | PATTERN | C | 0 | 0 | 300-420 | ~95% | 16 |
| 17 | `Information_Theory_Reasoning_Engine` | 1 | PROBABILISTIC | C | 0 | 0 | 250-350 | ~90% | 17 |
| 18 | `Inductive_Reasoning_Engine` | 1 | LOGICAL | C | 0 | 0 | 280-380 | ~80% | 18 |
| 19 | `Uncertainty_Estimation_Engine` | 1 | PROBABILISTIC | C | 0 | 0 | 220-320 | ~85% | 19 |
| 20 | `Semantic_Analysis_Engine` | 1 | SEMANTIC | C | 0 | 0 | 300-420 | ~85% | 20 |
| 21 | `Metaphorical_Reasoning_Engine` | 1 | SEMANTIC | C | 0 | 0 | 250-350 | ~85% | 21 |
| 22 | `Pattern_Detection_Engine` | 1 | PATTERN | C | 0 | 0 | 280-380 | ~95% | 22 |
| 23 | `Anomaly_Detection_Engine` | 1 | PATTERN | C | 0 | 0 | 240-340 | ~95% | 23 |
| 24 | `Predictive_Projection_Engine` | 1 | PATTERN | C | 0 | 0 | 260-360 | ~95% | 24 |
| 25 | `Semantic_Integration_Engine` | 2 | SEMANTIC | C | 0 | 0 | 380-520 | ~90% | 25 |

| # | Hub Module | Role | Est. Lines | New Code |
|---|-----------|------|-----------|---------|
| — | `Reasoning_Execution_Orchestrator` | Engine orchestration — invoke all 25 engines in layer order, | 280-380 | ~70% |
| — | `Reasoning_Output_Aggregator` | Collect AnalysisResult objects from all engines; build ARP r | 200-280 | ~65% |
| — | `Reasoning_Validation_Router` | Validate engine outputs before routing to consumers; enforce | 220-300 | ~50% |

### Tier Summary

| Tier | Engines | Description |
|------|---------|-------------|
| **A** | 5 | Immediately buildable — strong legacy data coverage (≥18 atoms, overlap ≤0.4) |
| B | 10 | Moderate augmentation needed — identifiable seed logic (~40–65% new code) |
| C | 10 | Write-mostly-fresh — zero or minimal legacy atoms, design-first |

---

## SECTION 1 — Design Principles

### Construction Hierarchy

Each engine is built using the following priority order:

```
1. Recovered logic atoms   → domain-specific functions from legacy staging
2. Legacy module fragments → seed algorithms, domain heuristics, utility logic
3. DRAC primitives         → shared scaffolding, schema, safety gates, operators
4. Minimal new code        → fill remaining gaps only
```

### Engine Constraints (all 25 engines)

```
Target size      : 150–450 lines
Reasoning domain : Single domain per engine
Dependencies     : No external heavy libraries (stdlib + DRAC only)
Execution style  : Pure functional analysis where possible
State            : Stateless execution
```

### Output Schema (AnalysisResult)

All 25 engines emit a single object conforming to:

```python
@dataclass
class AnalysisResult:
    engine_id:           str               # canonical engine name
    reasoning_domain:    str               # group: LOGICAL, PROBABILISTIC, STRUCTURAL, SEMANTIC, PATTERN
    confidence_score:    float             # [0.0, 1.0]
    detected_structures: list[dict]        # domain-specific findings
    derived_hypotheses:  list[str]         # generated conclusions
    supporting_signals:  dict[str, float]  # signal name → weight
```

### DRAC Integration Pattern

```
Required universals (inject into ALL engines):
  FBC_0007  Invariant_Constraints   — constraint enforcement
  FBC_0014  Semantic_Capability_Gate — capability boundary check

Optional composables (inject when domain-relevant):
  FBC_0004  Evidence_Chain          — inference provenance tracking
  FBC_0012  Runtime_Input_Sanitizer — input boundary validation
  FBC_0017  Trinitarian_Logic_Core  — 3-way logical operators
  FBC_0015  Temporal_Supersession   — temporal priority resolution
  FBC_0005  Global_Bijective_Recursion_Core — recursive mapping

Context (select one per engine, or inherit from hub):
  SCX-001  Agent_Policy_Decision_Context   — for logical decision engines
  SCX-002  Bootstrap_Runtime_Context       — for initialization-phase engines
  SCX-003  Privation_Handling_Context      — for constraint/privation engines
  SCX-004  Runtime_Mode_Context            — for operational runtime engines
  SCX-005  Trinitarian_Optimization_Context— for semantic/optimization engines
```

---

## SECTION 2 — Per-Engine Reconstruction Specifications

Each entry follows this format:

```
engine_name         : canonical identifier
layer               : 1 or 2
group               : LOGICAL | PROBABILISTIC | STRUCTURAL | SEMANTIC | PATTERN
tier                : A | B | C
legacy_sources_used : source module names
recovered_atoms_used: atom names matched to this engine
drac_primitives_used: DRAC axiom/context names
estimated_lines     : line count range
missing_components  : gaps requiring new code
```

---

### 01. `Bayesian_Reasoning_Engine`

*TIER A — Immediately Buildable*

**Purpose:** Update belief states from evidence; posterior probability computation.

```
engine_id         : Bayesian_Reasoning_Engine
layer             : 1
group             : PROBABILISTIC
tier              : A
atom_count        : 0
source_modules    : 0
estimated_lines   : 350-420
new_code_needed   : ~25%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Extract update_beliefs(), compute_posterior(), weight_evidence(), evaluate_likelihood() from bayesian_* modules. These provide a complete belief-update scaffold.

**drac_primitives_used:**

- `FBC_0004 Evidence_Chain`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-002 Bootstrap_Runtime_Context`

**missing_components** (require new code):

- posterior normalization routine (sum-to-one enforcement)
- likelihood ratio calculator
- evidence accumulation buffer with decay

---

### 02. `Consistency_Reasoning_Engine`

*TIER A — Immediately Buildable*

**Purpose:** Detect logical contradictions and conflicts across assertion sets.

```
engine_id         : Consistency_Reasoning_Engine
layer             : 1
group             : LOGICAL
tier              : A
atom_count        : 0
source_modules    : 0
estimated_lines   : 250-340
new_code_needed   : ~45%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> coherence_formalism, coherence_metrics, attestation provide check_coherence(), validate_assertions(), detect_conflicts() — use as-is with minor interface wrapping.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0001 3PDN_Constraint`
- `FBC_0002 3PDN_Validator`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components** (require new code):

- incompatibility matrix builder
- lightweight contradiction scorer (SAT-style)
- conflict graph data structure

---

### 03. `Topological_Reasoning_Engine`

*TIER A — Immediately Buildable*

**Purpose:** Analyze structural connectivity; fractal dimension and topological properties.

```
engine_id         : Topological_Reasoning_Engine
layer             : 1
group             : STRUCTURAL
tier              : A
atom_count        : 0
source_modules    : 0
estimated_lines   : 300-400
new_code_needed   : ~40%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Fractal analysis modules (compute_fractal_dimension, analyze_orbital_structure, detect_self_similarity) map directly to topological analysis. Extract them as seed algorithms.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0005 Global_Bijective_Recursion_Core`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- Euler characteristic computation
- classical boundary detection (non-fractal)
- homotopy-equivalence stub

---

### 04. `Graph_Reasoning_Engine`

*TIER A — Immediately Buildable*

**Purpose:** Analyze graph structures: paths, cycles, centrality, reachability.

```
engine_id         : Graph_Reasoning_Engine
layer             : 1
group             : STRUCTURAL
tier              : A
atom_count        : 0
source_modules    : 0
estimated_lines   : 280-360
new_code_needed   : ~55%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> cycle_ledger, commitment_ledger, tool_optimizer provide cycle detection and dependency resolution. Extract detect_cycles(), score_centrality(), resolve_dependencies() as base.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- BFS / DFS traversal (stdlib-only, no networkx)
- shortest-path (Dijkstra, unweighted fallback)
- node centrality scoring (degree, betweenness proxy)
- subgraph extraction primitive

---

### 05. `Ontological_Reasoning_Engine`

*TIER A — Immediately Buildable*

**Purpose:** Map concepts into hierarchical class/property models; taxonomy reasoning.

```
engine_id         : Ontological_Reasoning_Engine
layer             : 1
group             : SEMANTIC
tier              : A
atom_count        : 0
source_modules    : 0
estimated_lines   : 300-420
new_code_needed   : ~50%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> gen_worldview_ontoprops provides ontology property mapping. iel_registryv1/v2 provide class scaffolding. arp_nexus provides concept-to-class routing.

**drac_primitives_used:**

- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0011 Runtime_Context_Initializer`
- `FBC_0007 Invariant_Constraints`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- subsumption check (is-a hierarchy traversal)
- taxonomy path query (ancestor, descendant)
- RDFS-equivalent property inference stub

---

### 06. `Logical_Coherence_Engine` [LAYER 2]

*TIER B — Moderate Augmentation*

**Purpose:** (Layer 2) Integrate L1 logical outputs; global consistency check.

```
engine_id         : Logical_Coherence_Engine
layer             : 2
group             : LOGICAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 350-480
new_code_needed   : ~50%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> coherence_formalism is a direct seed. iel_integration provides integration scaffolding. privative_policies provides constraint enforcement. Extract global_coherence_check(), resolve_contradictions().

**drac_primitives_used:**

- `FBC_0017 Trinitarian_Logic_Core`
- `FBC_0007 Invariant_Constraints`
- `FBC_0001 3PDN_Constraint`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components** (require new code):

- implication closure computation
- global contradiction resolution (cross-engine)
- confidence-weighted coherence score

---

### 07. `Structural_Systems_Engine` [LAYER 2]

*TIER B — Moderate Augmentation*

**Purpose:** (Layer 2) Integrate L1 structural outputs; systems-level analysis.

```
engine_id         : Structural_Systems_Engine
layer             : 2
group             : STRUCTURAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 380-520
new_code_needed   : ~55%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Memory_Recall_Integration provides component integration logic. system_utils provides structural measurement seeds. iel_integration provides bridging. Extract integrate_systems(), analyze_system_state().

**drac_primitives_used:**

- `FBC_0008 Monolith_Runtime`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0011 Runtime_Context_Initializer`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- graph-level structural stability analysis
- compositionality metric
- emergent behavior detector (cross-module)

---

### 08. `Causal_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Trace cause-effect relationships through causal chains.

```
engine_id         : Causal_Reasoning_Engine
layer             : 1
group             : PROBABILISTIC
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 220-320
new_code_needed   : ~60%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> causal_chain_node_predictor is a direct seed module. id_handler provides entity-linkage primitives. Extract propagate_cause(), trace_chain().

**drac_primitives_used:**

- `FBC_0015 Temporal_Supersession`
- `FBC_0004 Evidence_Chain`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- causal influence graph builder
- do-calculus stub (intervention model)
- counterfactual comparison primitive

---

### 09. `Deductive_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Apply formal inference rules; implication chaining; modus ponens.

```
engine_id         : Deductive_Reasoning_Engine
layer             : 1
group             : LOGICAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 280-380
new_code_needed   : ~55%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> arp_nexus contains rule application scaffolding. bayesian_nexus provides weighted rule evaluation. Extract rule_apply(), evaluate_rule_chain() as seeds.

**drac_primitives_used:**

- `FBC_0017 Trinitarian_Logic_Core`
- `FBC_0016 Trinitarian_Alignment_Core`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components** (require new code):

- modus ponens / modus tollens primitives
- implication chain builder
- rule conflict resolver (priority ordering)

---

### 10. `Invariant_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Detect and enforce stable invariant properties across reasoning states.

```
engine_id         : Invariant_Reasoning_Engine
layer             : 1
group             : LOGICAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 200-300
new_code_needed   : ~50%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> lambda_parser provides functional constraint logic. hashing provides stable-property fingerprinting. iterative_loop provides fixpoint detection. Extract check_invariant(), detect_fixpoint().

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0001 3PDN_Constraint`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-003 Privation_Handling_Context`

**missing_components** (require new code):

- monotonicity verifier
- constraint fixpoint loop with convergence check
- invariant violation reporter

---

### 11. `Causal_Dynamics_Engine` [LAYER 2]

*TIER B — Moderate Augmentation*

**Purpose:** (Layer 2) Integrate L1 causal and probabilistic signals into dynamic causal model.

```
engine_id         : Causal_Dynamics_Engine
layer             : 2
group             : PROBABILISTIC
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 320-440
new_code_needed   : ~65%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> causal_chain_node_predictor provides a direct L1 seed that can be elevated. Use its propagation logic as the L2 integration scaffold.

**drac_primitives_used:**

- `FBC_0015 Temporal_Supersession`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0004 Evidence_Chain`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- temporal state-transition model
- feedback loop detector
- causal equilibrium solver

---

### 12. `Abductive_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Generate best-explanation hypotheses from incomplete evidence.

```
engine_id         : Abductive_Reasoning_Engine
layer             : 1
group             : LOGICAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 240-320
new_code_needed   : ~60%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> prioritization module provides hypothesis ranking. self_diagnosis provides fault-check → hypothesis paths. Extract score_hypothesis(), rank_explanations().

**drac_primitives_used:**

- `FBC_0004 Evidence_Chain`
- `FBC_0009 Necessary_Existence_Core`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components** (require new code):

- hypothesis generation loop (search space enumeration)
- plausibility scorer
- parsimony metric (Occam ranking)

---

### 13. `Analogical_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Map structural correspondences between domains; analogy scoring.

```
engine_id         : Analogical_Reasoning_Engine
layer             : 1
group             : SEMANTIC
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 220-320
new_code_needed   : ~60%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> translation_engine provides structural mapping primitives; logging_utils provides token-level comparison. Extract map_structure(), score_correspondence().

**drac_primitives_used:**

- `FBC_0005 Global_Bijective_Recursion_Core`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- isomorphism scoring algorithm
- analogy candidate ranker
- cross-domain attribute mapper

---

### 14. `Relational_Dependency_Reasoning_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** (Merged: Relational + Dependency) Analyze relational tuples and resolve dependency graphs.

```
engine_id         : Relational_Dependency_Reasoning_Engine
layer             : 1
group             : STRUCTURAL
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 280-380
new_code_needed   : ~55%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> pxl_schema provides tuple/relation schemas. export_tool_registry provides dependency declaration logic. tool_optimizer provides dependency resolution. Extract resolve_deps(), score_relation(), infer_link().

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0005 Global_Bijective_Recursion_Core`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- transitive closure computation
- relation inference (A→B+B→C ⇒ A→C)
- cycle-breaking heuristic for dependency resolution

---

### 15. `Complexity_Analysis_Engine`

*TIER B — Moderate Augmentation*

**Purpose:** Measure structural and computational complexity of reasoning artifacts.

```
engine_id         : Complexity_Analysis_Engine
layer             : 1
group             : PATTERN
tier              : B
atom_count        : 0
source_modules    : 0
estimated_lines   : 200-300
new_code_needed   : ~55%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> tool_introspection provides structural measurement infrastructure. attestation provides completeness scoring. tool_optimizer provides size/cost estimation. Extract measure_complexity(), score_completeness().

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- Kolmogorov complexity proxy (LZ-compression ratio)
- cyclomatic complexity counter
- depth-of-nesting metric

---

### 16. `Dynamic_Pattern_Engine` [LAYER 2]

*TIER C — Write-Mostly-Fresh*

**Purpose:** (Layer 2) Integrate L1 pattern outputs; detect emergent or evolving patterns.

```
engine_id         : Dynamic_Pattern_Engine
layer             : 2
group             : PATTERN
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 300-420
new_code_needed   : ~95%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Zero atoms. REASONING_PRIMITIVES provide thin scaffold for state tracking.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0013 Runtime_Mode_Controller`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- pattern trajectory tracker
- emergent-signal aggregator
- attractor / stability detector (qualitative)
- cross-engine pattern unification

---

### 17. `Information_Theory_Reasoning_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** (New) Apply information-theoretic measures: entropy, KL-divergence, mutual information.

```
engine_id         : Information_Theory_Reasoning_Engine
layer             : 1
group             : PROBABILISTIC
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 250-350
new_code_needed   : ~90%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> No direct legacy atoms. Complexity_Analysis atoms (entropy references) provide a thin scaffold. Use REASONING_PRIMITIVES for scaffolding.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- Shannon entropy calculator (discrete distributions)
- KL-divergence / JS-divergence primitives
- mutual information estimator
- channel capacity proxy

---

### 18. `Inductive_Reasoning_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Generalize patterns from observed instances; rule induction.

```
engine_id         : Inductive_Reasoning_Engine
layer             : 1
group             : LOGICAL
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 280-380
new_code_needed   : ~80%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> system_utils provides thin generalization stubs. Use VALIDATION_PRIMITIVES for instance-validation scaffolding.

**drac_primitives_used:**

- `FBC_0004 Evidence_Chain`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-002 Bootstrap_Runtime_Context`

**missing_components** (require new code):

- pattern extraction from example sets
- rule generalization algorithm
- support / confidence scoring (Apriori-style)
- counter-example checker

---

### 19. `Uncertainty_Estimation_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Quantify epistemic and aleatoric uncertainty in reasoning outputs.

```
engine_id         : Uncertainty_Estimation_Engine
layer             : 1
group             : PROBABILISTIC
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 220-320
new_code_needed   : ~85%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> translation_engine provides thin confidence-signal primitives. Use NORMALIZATION_PRIMITIVES for score normalization.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-003 Privation_Handling_Context`

**missing_components** (require new code):

- credible interval estimation (bootstrap)
- Dempster-Shafer belief mass allocator
- entropy-based uncertainty quantifier
- propagation-of-uncertainty through engine chain

---

### 20. `Semantic_Analysis_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Analyze semantic content: term mapping, lexical structure, meaning alignment.

```
engine_id         : Semantic_Analysis_Engine
layer             : 1
group             : SEMANTIC
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 300-420
new_code_needed   : ~85%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> arp_nexus, gen_worldview_ontoprops provide minimal token-handling stubs. Primary implementation must be written fresh.

**drac_primitives_used:**

- `FBC_0011 Runtime_Context_Initializer`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0007 Invariant_Constraints`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- token normalization pipeline (no NLP deps)
- term frequency / IDF proxy
- semantic distance metric (edit + structural)
- context window alignment

---

### 21. `Metaphorical_Reasoning_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Identify and apply conceptual metaphors; symbolic substitution mapping.

```
engine_id         : Metaphorical_Reasoning_Engine
layer             : 1
group             : SEMANTIC
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 250-350
new_code_needed   : ~85%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Memory_Recall_Integration, pxl_schema provide symbolic substitution primitives at schema level. Use as data-model seeds only.

**drac_primitives_used:**

- `FBC_0005 Global_Bijective_Recursion_Core`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- conceptual metaphor schema library
- source-to-target domain mapper
- metaphor coherence scorer
- blended-space constructor

---

### 22. `Pattern_Detection_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Detect recurring structures, sequences, and frequency signatures.

```
engine_id         : Pattern_Detection_Engine
layer             : 1
group             : PATTERN
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 280-380
new_code_needed   : ~95%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Zero legacy atoms. Use NORMALIZATION_PRIMITIVES for data normalization scaffold only.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0012 Runtime_Input_Sanitizer`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- sliding-window frequency counter
- sequence pattern matcher (stdlib only)
- structural signature extractor
- pattern confidence scorer

---

### 23. `Anomaly_Detection_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Identify outliers, distributional drift, and abnormal reasoning signals.

```
engine_id         : Anomaly_Detection_Engine
layer             : 1
group             : PATTERN
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 240-340
new_code_needed   : ~95%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Zero legacy atoms. Write entirely from design specification.

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0001 3PDN_Constraint`

**drac_context:** `SCX-003 Privation_Handling_Context`

**missing_components** (require new code):

- z-score / IQR outlier detector (no scipy)
- moving-average baseline tracker
- threshold-based drift classifier
- anomaly severity scorer

---

### 24. `Predictive_Projection_Engine`

*TIER C — Write-Mostly-Fresh*

**Purpose:** Project future states by extrapolating from current reasoning trajectories.

```
engine_id         : Predictive_Projection_Engine
layer             : 1
group             : PATTERN
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 260-360
new_code_needed   : ~95%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Zero legacy atoms. Write entirely from design specification.

**drac_primitives_used:**

- `FBC_0015 Temporal_Supersession`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-004 Runtime_Mode_Context`

**missing_components** (require new code):

- linear extrapolation primitive
- confidence-decay model (horizon weighting)
- trajectory comparison (current vs. projected)
- hypothesis projection validator

---

### 25. `Semantic_Integration_Engine` [LAYER 2]

*TIER C — Write-Mostly-Fresh*

**Purpose:** (Layer 2) Integrate L1 semantic outputs into unified concept graph.

```
engine_id         : Semantic_Integration_Engine
layer             : 2
group             : SEMANTIC
tier              : C
atom_count        : 0
source_modules    : 0
estimated_lines   : 380-520
new_code_needed   : ~90%
```

**legacy_sources_used:**

- *(none — write fresh)*

**recovered_atoms_used:** (0 atoms)

- *(none — DRAC primitives + new code only)*

**legacy_fragment_strategy:**

> Zero direct atoms. SCHEMA_PRIMITIVES provide concept-node data model scaffolding.

**drac_primitives_used:**

- `FBC_0011 Runtime_Context_Initializer`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0007 Invariant_Constraints`

**drac_context:** `SCX-005 Trinitarian_Optimization_Context`

**missing_components** (require new code):

- concept graph builder
- semantic disambiguation resolver
- cross-engine meaning alignment (unification)
- concept-to-output schema serializer

---

## SECTION 3 — Hub Module Specifications

The ARP reasoning hub operates as the orchestration layer above the engine stack.

```
Hub Architecture:

  [25 Engines]
       ↓
  Reasoning_Execution_Orchestrator
       ↓
  Reasoning_Output_Aggregator  ← append-only accumulation
       ↓
  Reasoning_Validation_Router  ← schema contract enforcement
       ↓
  [EpistemicArtifact output → Meta Layer]
```

### `Reasoning_Execution_Orchestrator`

**Role:** Engine orchestration — invoke all 25 engines in layer order, manage timeouts and failures

```
estimated_lines   : 280-380
new_code_needed   : ~70%
```

**legacy_fragments_used:**

- `run_all_checks (attestation)`
- `tool_optimizer scheduling logic`

**drac_primitives_used:**

- `FBC_0008 Monolith_Runtime`
- `FBC_0010 Read_Only_Agent_Interface`
- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`

**drac_context:** `SCX-002 Bootstrap_Runtime_Context`

**missing_components:**

- engine invocation dispatcher (layer-ordered)
- per-engine timeout enforcer
- failure isolation (one engine failure does not abort stack)
- execution trace logger

---

### `Reasoning_Output_Aggregator`

**Role:** Collect AnalysisResult objects from all engines; build ARP reasoning bundle

```
estimated_lines   : 200-280
new_code_needed   : ~65%
```

**legacy_fragments_used:**

- `Memory_Recall_Integration aggregation logic`
- `coherence_metrics summary builder`

**drac_primitives_used:**

- `FBC_0007 Invariant_Constraints`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0018 UWM_Ingestion`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components:**

- append-only result collector (immutable accumulator)
- confidence vector builder
- cross-engine cross-reference table
- bundle serializer → EpistemicArtifact

---

### `Reasoning_Validation_Router`

**Role:** Validate engine outputs before routing to consumers; enforce schema contracts

```
estimated_lines   : 220-300
new_code_needed   : ~50%
```

**legacy_fragments_used:**

- `attestation validation logic`
- `check_imports schema enforcement`
- `UWM_Validator patterns`

**drac_primitives_used:**

- `FBC_0019 UWM_Validator`
- `FBC_0002 3PDN_Validator`
- `FBC_0014 Semantic_Capability_Gate`
- `FBC_0007 Invariant_Constraints`

**drac_context:** `SCX-001 Agent_Policy_Decision_Context`

**missing_components:**

- AnalysisResult schema validator (dataclass contract check)
- confidence threshold gate (reject low-confidence outputs)
- routing table → correct L2 engine per L1 output
- error escalation path

---

## SECTION 4 — DRAC Primitive Reference

### Semantic Axioms (DRAC_Core/DRAC_Invariables/SEMANTIC_AXIOMS/)

| FBC ID | Module Name | Taxonomy Class | Role in Cores |
|--------|------------|----------------|---------------|
| `FBC_0001` | `3PDN_Constraint` | safety_core | OPTIONAL_COMPOSABLE |
| `FBC_0002` | `3PDN_Validator` | safety_core | OPTIONAL_COMPOSABLE |
| `FBC_0003` | `Agent_Activation_Gate` | safety_core | OPTIONAL_COMPOSABLE |
| `FBC_0004` | `Evidence_Chain` | inference_core | OPTIONAL_COMPOSABLE |
| `FBC_0005` | `Global_Bijective_Recursion_Core` | inference_core | OPTIONAL_COMPOSABLE |
| `FBC_0006` | `Hypostatic_ID_Validator` | safety_core | OPTIONAL_COMPOSABLE |
| `FBC_0007` | `Invariant_Constraints` | safety_core | REQUIRED_UNIVERSAL |
| `FBC_0008` | `Monolith_Runtime` | protocol_core | OPTIONAL_COMPOSABLE |
| `FBC_0009` | `Necessary_Existence_Core` | inference_core | OPTIONAL_COMPOSABLE |
| `FBC_0010` | `Read_Only_Agent_Interface` | agent_orchestration | OPTIONAL_COMPOSABLE |
| `FBC_0011` | `Runtime_Context_Initializer` | semantic_core | CONTEXT_SELECTIVE |
| `FBC_0012` | `Runtime_Input_Sanitizer` | safety_core | OPTIONAL_COMPOSABLE |
| `FBC_0013` | `Runtime_Mode_Controller` | semantic_core | CONTEXT_SELECTIVE |
| `FBC_0014` | `Semantic_Capability_Gate` | safety_core | REQUIRED_UNIVERSAL |
| `FBC_0015` | `Temporal_Supersession` | inference_core | OPTIONAL_COMPOSABLE |
| `FBC_0016` | `Trinitarian_Alignment_Core` | inference_core | CONTEXT_SELECTIVE |
| `FBC_0017` | `Trinitarian_Logic_Core` | inference_core | OPTIONAL_COMPOSABLE |
| `FBC_0018` | `UWM_Ingestion` | protocol_core | OPTIONAL_COMPOSABLE |
| `FBC_0019` | `UWM_Validator` | safety_core | OPTIONAL_COMPOSABLE |

### Semantic Contexts (DRAC_Core/DRAC_Invariables/SEMANTIC_CONTEXTS/)

| SCX ID | Context Name | Compatible Clusters |
|--------|-------------|---------------------|
| `SCX-001` | `Agent_Policy_Decision_Context` | agent_runtime, memory_access, planning |
| `SCX-002` | `Bootstrap_Runtime_Context` | agent_runtime, memory_access, planning |
| `SCX-003` | `Privation_Handling_Context` | agent_runtime, memory_access, planning |
| `SCX-004` | `Runtime_Mode_Context` | agent_runtime, memory_access, planning |
| `SCX-005` | `Trinitarian_Optimization_Context` | agent_runtime, memory_access, numerical_compute |

---

## SECTION 5 — Build Sequence

```
PHASE 4A — Foundation (build first, others depend on output schema)
  1.  Bayesian_Reasoning_Engine           (richest dataset)
  2.  Consistency_Reasoning_Engine        (logical gate for L2)
  3.  Reasoning_Execution_Orchestrator    (needed to run engines)
  4.  Reasoning_Output_Aggregator         (defines EpistemicArtifact)
  5.  Reasoning_Validation_Router         (defines AnalysisResult contract)

PHASE 4B — Tier A Engines
  6.  Topological_Reasoning_Engine
  7.  Graph_Reasoning_Engine
  8.  Ontological_Reasoning_Engine

PHASE 4C — Layer 2 Tier B (blocked until L1 outputs exist)
  9.  Logical_Coherence_Engine [L2]
  10. Structural_Systems_Engine [L2]
  11. Causal_Reasoning_Engine
  12. Causal_Dynamics_Engine [L2]

PHASE 4D — Remaining Tier B
  13. Deductive_Reasoning_Engine
  14. Invariant_Reasoning_Engine
  15. Abductive_Reasoning_Engine
  16. Analogical_Reasoning_Engine
  17. Relational_Dependency_Reasoning_Engine
  18. Complexity_Analysis_Engine

PHASE 4E — Tier C Write-Fresh
  (all can be built in parallel with each other)
  19. Information_Theory_Reasoning_Engine
  20. Dynamic_Pattern_Engine [L2]
  21. Inductive_Reasoning_Engine
  22. Uncertainty_Estimation_Engine
  23. Semantic_Analysis_Engine
  24. Metaphorical_Reasoning_Engine
  25. Pattern_Detection_Engine
  26. Anomaly_Detection_Engine
  27. Predictive_Projection_Engine
  28. Semantic_Integration_Engine [L2]
```

---

## Validation

| Check | Value |
|-------|-------|
| Total engines specified | 25 |
| Hub modules specified | 3 |
| Tier A (immediately buildable) | 5 |
| Tier B (moderate augmentation) | 10 |
| Tier C (write-mostly-fresh) | 10 |
| Layer 1 engines | 20 |
| Layer 2 engines | 5 |
| DRAC axioms referenced | 19 |
| DRAC contexts referenced | 5 |
| Engine set adjustment applied | YES — Relational+Dependency merged; Information_Theory added |
| All engines output AnalysisResult | REQUIRED |
| All engines stateless | REQUIRED |
| External heavy deps prohibited | REQUIRED |

---

*End of ARP Reconstruction Directive ARP-RD-001*
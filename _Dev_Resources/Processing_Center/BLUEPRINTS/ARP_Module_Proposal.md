# ARP Module Proposal — Legacy Dataset Analysis

```
Artifact Type   : ARP Reasoning Stack Module Proposal
Source Dataset  : LOGIC_ATOM_EXTRACTION_PLAN.md (287 atoms)
                  Legacy module JSON datasets (161 modules)
Pipeline Phase  : Pre-Phase-4 (ARP Engine Construction Planning)
Generated       : 2026-03-12
Status          : PROPOSAL — Awaiting Phase-4 Authorization
```

---

## Executive Summary

**Bottom line answer: 5 genuinely high-leverage, low-overlap modules**
can be built immediately from existing atom data with minimal augmentation.

A further **10 modules** are buildable with targeted augmentation (40–60% new code).

**10 modules** have negligible or zero legacy coverage and must be written
primarily from design requirements.

The **2 aggregators** (Layer 1 → Layer 2, Layer 2 → Meta) are net-new modules
by design and do not depend on legacy data — they operate on output schema contracts.

**Total proposed modules: 27** (25 engines + 2 aggregators)

---

## SECTION 1 — Scoring Methodology

Each of the 287 extracted logic atoms was scored against the keyword
profile of each ARP engine target. Scores drive two metrics:

| Metric | Definition | High = Good |
|--------|-----------|-------------|
| **Leverage score** | Unique matching atoms ÷ average module overlap | YES — more atoms, less sharing |
| **Coverage %** | Fraction of the engine's keyword profile matched | YES — richer coverage |
| **Avg overlap** | Average shared source modules with other engines | NO — lower is more distinct |
| **Atom count** | Total unique atoms directly matching the engine role | YES |

**Tier thresholds:**

| Tier | Atom count | Overlap | Description |
|------|-----------|---------|-------------|
| A — Immediately buildable | ≥ 10 atoms | ≤ 0.4 | Strong data foundation, distinct sources |
| B — Moderate augmentation | 2–9 atoms | ≤ 0.5 | Viable seed, ~40–60% new code needed |
| C — Write-mostly-fresh | 0–1 atoms | any | Design-first, minimal legacy leverage |

---

## SECTION 2 — Full Engine Scoring Table

All 25 ARP engine targets scored against the 287-atom legacy dataset:

| Engine | Layer | Group | Atoms | Src Mods | Est. Lines | Avg Overlap | Coverage | Leverage | TIER |
|--------|-------|-------|-------|----------|------------|------------|----------|----------|------|
| `Topological_Reasoning_Engine` | 1 | STRUCTURAL | 20 | 7 | 600 | 0.08 | 50.0% | 200.0 | **A** |
| `Bayesian_Reasoning_Engine` | 1 | PROBABILISTIC | 44 | 11 | 600 | 0.29 | 66.7% | 150.9 | **A** |
| `Graph_Reasoning_Engine` | 1 | STRUCTURAL | 27 | 4 | 600 | 0.38 | 22.2% | 72.0 | **A** |
| `Analogical_Reasoning_Engine` | 1 | SEMANTIC | 9 | 2 | 300 | 0.12 | 25.0% | 72.0 | B |
| `Consistency_Reasoning_Engine` | 1 | LOGICAL | 19 | 10 | 600 | 0.29 | 37.5% | 65.1 | **A** |
| `Ontological_Reasoning_Engine` | 1 | SEMANTIC | 18 | 13 | 600 | 0.29 | 22.2% | 61.7 | **A** |
| `Logical_Coherence_Engine` | 2 | LOGICAL | 4 | 4 | 600 | 0.08 | 37.5% | 40.0 | B |
| `Abductive_Reasoning_Engine` | 1 | LOGICAL | 3 | 2 | 315 | 0.08 | 22.2% | 30.0 | B |
| `Structural_Systems_Engine` | 2 | STRUCTURAL | 9 | 5 | 600 | 0.33 | 42.9% | 27.0 | B |
| `Causal_Reasoning_Engine` | 1 | PROBABILISTIC | 2 | 2 | 75 | 0.08 | 37.5% | 20.0 | B |
| `Invariant_Reasoning_Engine` | 1 | LOGICAL | 6 | 6 | 600 | 0.33 | 62.5% | 18.0 | B |
| `Relational_Reasoning_Engine` | 1 | STRUCTURAL | 9 | 7 | 600 | 0.71 | 44.4% | 12.7 | B |
| `Complexity_Analysis_Engine` | 1 | PATTERN | 4 | 3 | 600 | 0.33 | 11.1% | 12.0 | B |
| `Semantic_Analysis_Engine` | 1 | SEMANTIC | 2 | 2 | 525 | 0.17 | 22.2% | 12.0 | C |
| `Metaphorical_Reasoning_Engine` | 1 | SEMANTIC | 2 | 2 | 600 | 0.17 | 14.3% | 12.0 | C |
| `Deductive_Reasoning_Engine` | 1 | LOGICAL | 8 | 7 | 600 | 0.75 | 45.5% | 10.7 | B |
| `Dependency_Reasoning_Engine` | 1 | STRUCTURAL | 3 | 3 | 585 | 0.29 | 25.0% | 10.3 | B |
| `Causal_Dynamics_Engine` | 2 | PROBABILISTIC | 1 | 1 | 50 | 0.04 | 42.9% | 10.0 | C |
| `Inductive_Reasoning_Engine` | 1 | LOGICAL | 1 | 1 | 120 | 0.12 | 11.1% | 8.0 | C |
| `Uncertainty_Estimation_Engine` | 1 | PROBABILISTIC | 1 | 1 | 270 | 0.12 | 12.5% | 8.0 | C |
| `Pattern_Detection_Engine` | 1 | PATTERN | 0 | 0 | 50 | 0.0 | 0.0% | 0.0 | C |
| `Anomaly_Detection_Engine` | 1 | PATTERN | 0 | 0 | 50 | 0.0 | 0.0% | 0.0 | C |
| `Predictive_Projection_Engine` | 1 | PATTERN | 0 | 0 | 50 | 0.0 | 0.0% | 0.0 | C |
| `Semantic_Integration_Engine` | 2 | SEMANTIC | 0 | 0 | 50 | 0.0 | 0.0% | 0.0 | C |
| `Dynamic_Pattern_Engine` | 2 | PATTERN | 0 | 0 | 50 | 0.0 | 0.0% | 0.0 | C |

---

## SECTION 3 — Tier A: High-Leverage, Low-Overlap Modules (5 engines)

These 5 engines have a strong data foundation and minimal source-module
overlap with other engines. They are the **priority construction targets**.

### A1. `Bayesian_Reasoning_Engine` (Layer 1 — PROBABILISTIC)

**Purpose:** Update belief states based on evidence; posterior probability computation.

```
Atom count       : 44
Source modules   : 11
Est. lines       : 380–450
Avg overlap      : 0.29 (low)
Coverage         : 66.7%
New code needed  : ~25%
```

**Primary legacy sources:**

- `bayes_update_real_time`
- `bayesian_data_parser`
- `bayesian_interface`
- `bayesian_inferencer`
- `bayesian_nexus`
- `bayesian_updates`

**Key atoms available:**

- `update_beliefs`
- `compute_posterior`
- `weight_evidence`
- `evaluate_likelihood`
- `propagate_prior`

**Missing logic (requires augmentation):**

- posterior normalization
- likelihood ratio computation
- evidence accumulation interface

> **Assessment:** The richest single-domain dataset in the entire legacy corpus. 11 source modules, 44 atoms. Low competition. **Build first.**

### A2. `Topological_Reasoning_Engine` (Layer 1 — STRUCTURAL)

**Purpose:** Analyze structural connectivity patterns; fractal and geometric properties.

```
Atom count       : 20
Source modules   : 7
Est. lines       : 300–420
Avg overlap      : 0.08 (low)
Coverage         : 50.0%
New code needed  : ~40%
```

**Primary legacy sources:**

- `advanced_fractal_analyzer`
- `comprehensive_fractal_analysis`
- `fractal_nexus`
- `fractal_orbit_toolkit`
- `fractal_geometry_engine`
- `fractal_validator`

**Key atoms available:**

- `compute_fractal_dimension`
- `analyze_orbital_structure`
- `detect_self_similarity`
- `measure_connectivity`
- `compute_hausdorff`

**Missing logic (requires augmentation):**

- classical topology primitives (holes, genus)
- manifold detection
- boundary detection

> **Assessment:** The fractal modules are de facto topological analyzers. 20 distinct atoms, overlap=0.1. Gap is in classical topology vocabulary — augment with Euler characteristic, boundary detection, and homotopy stubs.

### A3. `Graph_Reasoning_Engine` (Layer 1 — STRUCTURAL)

**Purpose:** Analyze graph structures in the artifact: paths, centrality, reachability.

```
Atom count       : 27
Source modules   : 4
Est. lines       : 280–380
Avg overlap      : 0.38 (low)
Coverage         : 22.2%
New code needed  : ~55%
```

**Primary legacy sources:**

- `commitment_ledger`
- `cycle_ledger`
- `tool_introspection`
- `tool_optimizer`

**Key atoms available:**

- `detect_cycles`
- `resolve_dependencies`
- `score_centrality`
- `find_paths`

**Missing logic (requires augmentation):**

- BFS/DFS traversal primitives
- node centrality scoring
- shortest-path logic
- subgraph detection

> **Assessment:** 27 atoms but coverage only 22% — source modules are cycle/dependency tools which are graph reasoning by nature. Augment with graph algorithm primitives (networkx-free, stdlib-only). Distinct sources, low overlap.

### A4. `Consistency_Reasoning_Engine` (Layer 1 — LOGICAL)

**Purpose:** Detect contradictions and logical conflicts across assertion sets.

```
Atom count       : 19
Source modules   : 10
Est. lines       : 250–350
Avg overlap      : 0.29 (low)
Coverage         : 37.5%
New code needed  : ~45%
```

**Primary legacy sources:**

- `attestation`
- `check_imports`
- `coherence`
- `coherence_formalism`
- `coherence_metrics`
- `privative_policies`

**Key atoms available:**

- `check_coherence`
- `validate_assertions`
- `detect_conflicts`
- `score_consistency`
- `run_all_checks`

**Missing logic (requires augmentation):**

- formal contradiction detection (SAT-style)
- incompatibility matrix
- conflict graph

> **Assessment:** The coherence_formalism and coherence_metrics modules are purpose-built for this engine. 19 atoms, overlap=0.3. Gap is formal logical conflict resolution — add a lightweight contradiction scorer.

### A5. `Ontological_Reasoning_Engine` (Layer 1 — SEMANTIC)

**Purpose:** Map concepts into hierarchical class/property models; taxonomy reasoning.

```
Atom count       : 18
Source modules   : 13
Est. lines       : 300–420
Avg overlap      : 0.29 (low)
Coverage         : 22.2%
New code needed  : ~50%
```

**Primary legacy sources:**

- `agent_nexus`
- `arp_nexus`
- `bridge`
- `iel_registryv1`
- `iel_registryv2`
- `gen_worldview_ontoprops`

**Key atoms available:**

- `build_ontology`
- `classify_concept`
- `resolve_hierarchy`
- `get_subclasses`
- `map_properties`

**Missing logic (requires augmentation):**

- subsumption checking
- taxonomy traversal
- concept hierarchy queries
- RDFS-style reasoning

> **Assessment:** gen_worldview_ontoprops is directly ontological; iel_registry modules give class/concept scaffolding. Gap is formal taxonomy traversal logic. 18 atoms, low overlap.

---

## SECTION 4 — Tier B: Moderate-Leverage Modules (10 engines)

These engines have identifiable seed atoms but require 40–60% new code.
Worth building, but schedule after Tier A.

| # | Engine | Layer | Group | Atoms | Key Sources | Est. Lines | New Code | Primary Gap |
|---|--------|-------|-------|-------|-------------|-----------|----------|-------------|
| B1 | `Deductive_Reasoning_Engine` | 1 | LOGICAL | 8 | `arp_nexus`, `bayesian_nexus`, `commitment_ledger` | 280–380 | 50–60% | implication chaining, modus ponens primitives |
| B2 | `Invariant_Reasoning_Engine` | 1 | LOGICAL | 6 | `gen_worldview_ontoprops`, `hashing`, `iterative_loop` | 200–300 | 50–60% | constraint fixpoint detection, stability proofs |
| B3 | `Causal_Reasoning_Engine` | 1 | PROBABILISTIC | 2 | `causal_chain_node_predictor`, `id_handler` | 220–320 | 50–60% | influence graph, do-calculus stubs |
| B4 | `Logical_Coherence_Engine` | 2 | LOGICAL | 4 | `coherence_formalism`, `iel_integration`, `iel_registryv2` | 350–500 | 50–60% | global contradiction resolution, implication closure |
| B5 | `Structural_Systems_Engine` | 2 | STRUCTURAL | 9 | `Memory_Recall_Integration`, `iel_integration`, `logos_monitor` | 400–550 | 50–60% | graph-level stability analysis, structural constraint checki |
| B6 | `Relational_Reasoning_Engine` | 1 | STRUCTURAL | 9 | `arp_nexus`, `fractal_nexus`, `id_handler` | 260–360 | 50–60% | relation inference, tuple-level reasoning |
| B7 | `Complexity_Analysis_Engine` | 1 | PATTERN | 4 | `attestation`, `tool_introspection`, `tool_optimizer` | 200–300 | 50–60% | Kolmogorov complexity proxy, LZ compression metric |
| B8 | `Analogical_Reasoning_Engine` | 1 | SEMANTIC | 9 | `logging_utils`, `translation_engine` | 220–320 | 50–60% | isomorphism scoring, analogy ranking algorithm |
| B9 | `Dependency_Reasoning_Engine` | 1 | STRUCTURAL | 3 | `export_tool_registry`, `tool_introspection`, `tool_optimizer` | 180–260 | 50–60% | topological sort, cycle breaking, transitive closure |
| B10 | `Abductive_Reasoning_Engine` | 1 | LOGICAL | 3 | `prioritization`, `self_diagnosis` | 240–340 | 50–60% | hypothesis generation loop, plausibility scoring |

**Key notes on Tier B overlap risks:**

- `Deductive_Reasoning_Engine` and `Relational_Reasoning_Engine` share `arp_nexus` as a
  source — ensure atom partitioning during extraction to prevent duplication.
- `Logical_Coherence_Engine` (L2) is the natural consumer of `Consistency_Reasoning_Engine`
  (L1) output — keep their atom pools strictly separated even though they address related domains.
- `Structural_Systems_Engine` (L2) sits directly above `Graph_Reasoning_Engine` and
  `Dependency_Reasoning_Engine` — its source atoms must be distinct at the function level.

---

## SECTION 5 — Tier C: Write-Mostly-Fresh Modules (10 engines)

These engines have 0–1 matching atoms in the legacy dataset.
The legacy corpus **does not** give meaningful leverage here.
These should be scheduled after Tier A/B, designed from ARP specification.

| # | Engine | Layer | Group | Atoms | Legacy Verdict | Recommended Approach |
|---|--------|-------|-------|-------|----------------|---------------------|
| C1 | `Pattern_Detection_Engine` | 1 | PATTERN | 0 | 0 atoms — no pattern clustering legacy | Write fresh; use NORMALIZATION_PRIMITIVES atoms as normalizers |
| C2 | `Anomaly_Detection_Engine` | 1 | PATTERN | 0 | 0 atoms — no outlier/distribution legacy | Write fresh; pure statistical primitives needed |
| C3 | `Predictive_Projection_Engine` | 1 | PATTERN | 0 | 0 atoms — no forecasting/trajectory legacy | Write fresh; linear extrapolation + hypothesis projection |
| C4 | `Inductive_Reasoning_Engine` | 1 | LOGICAL | 1 | 1 atom — system_utils provides thin coverage | Write mostly fresh; pattern recognition kernel needed |
| C5 | `Uncertainty_Estimation_Engine` | 1 | PROBABILISTIC | 1 | 1 atom — translation_engine is weak signal | Write mostly fresh; entropy + credible interval logic |
| C6 | `Semantic_Analysis_Engine` | 1 | SEMANTIC | 2 | 2 atoms; gen_worldview_ontoprops partial | Write mostly fresh; semantic parsing kernel needed |
| C7 | `Metaphorical_Reasoning_Engine` | 1 | SEMANTIC | 2 | 2 atoms; pxl_schema gives substitution hint | Write mostly fresh; symbolic mapping algebra required |
| C8 | `Causal_Dynamics_Engine` | 2 | PROBABILISTIC | 1 | 1 atom; causal_chain_node_predictor is seed | Write mostly fresh; propagation logic needed |
| C9 | `Semantic_Integration_Engine` | 2 | SEMANTIC | 0 | 0 atoms — no concept graph legacy | Write fresh; SCHEMA_PRIMITIVES provide schema scaffolding |
| C10 | `Dynamic_Pattern_Engine` | 2 | PATTERN | 0 | 0 atoms — no trajectory/emergence legacy | Write fresh; REASONING_PRIMITIVES provide partial scaffold |

---

## SECTION 6 — Aggregator Modules (2 new modules)

These are **net-new modules** by design — they do not reconstruct legacy logic.
Their inputs and outputs are defined by the ARP output schema contracts.

### AGG-1. `ARP_L1_Aggregator`

```
Role             : Layer 1 → Layer 2 bridge
Input            : 20 Layer 1 engine output objects
Output           : 5 thematic group bundles for Layer 2 consumption
Est. lines       : 200–280
Legacy atoms     : 0 (net-new aggregation logic)
Dependencies     : None (pure schema-in / schema-out)
Side effects     : NONE — stateless transform
```

**Aggregation groups produced:**

| Output Bundle | Consumed by L2 Engine | Source L1 Engines |
|-------------|----------------------|-----------|
| `logical_group` | `Logical_Coherence_Engine` | Deductive, Inductive, Abductive, Consistency, Invariant |
| `probabilistic_group` | `Causal_Dynamics_Engine` | Bayesian, Causal, Uncertainty |
| `structural_group` | `Structural_Systems_Engine` | Graph, Relational, Topological, Dependency |
| `semantic_group` | `Semantic_Integration_Engine` | Semantic, Analogical, Metaphorical, Ontological |
| `pattern_group` | `Dynamic_Pattern_Engine` | Pattern, Anomaly, Complexity, Predictive |

**Design constraints:**

- Each L1 output object is a typed `AnalysisResult` with fields:
  `engine_id`, `confidence`, `detected_structures`, `hypotheses`, `metadata`
- Aggregator groups outputs by thematic tag, compresses confidence signals
  (mean + variance), and packages into a `GroupedReasoningBundle`
- No reasoning is performed — compression and routing only
- Must preserve all detected structures from all engines (no information loss)

### AGG-2. `ARP_L2_Synthesizer`

```
Role             : Layer 2 → Meta-Layer bridge
Input            : 5 Layer 2 engine output artifacts
Output           : 1 synthesized EpistemicArtifact for meta-layer consumption
Est. lines       : 250–350
Legacy atoms     : 0 (net-new synthesis logic)
Dependencies     : None (pure schema-in / schema-out)
Side effects     : NONE — stateless transform
```

**Synthesis process:**

| Step | Operation |
|------|-----------|
| 1. Collect | Accept 5 `DomainReasoningArtifact` objects from L2 engines |
| 2. Reconcile | Cross-check conflicting signals across domains (logical vs. causal) |
| 3. Weight | Apply confidence-weighted merge across all domain reasoning |
| 4. Compress | Reduce to a ranked set of epistemic claims with supporting evidence |
| 5. Emit | Output a single `EpistemicArtifact` containing: top claims, conflict map, confidence vector, reasoning trace |

**`EpistemicArtifact` schema (proposed):**

```python
@dataclass
class EpistemicArtifact:
    top_claims:         list[Claim]          # ranked epistemic conclusions
    conflict_map:       dict[str, list[str]] # domain → conflicting signals
    confidence_vector:  dict[str, float]     # domain → aggregate confidence
    reasoning_trace:    list[ReasoningStep]  # audit trail
    emergent_patterns:  list[str]            # cross-domain observations
    meta_layer_ready:   bool                 # gate check before meta consumption
```

---

## SECTION 7 — Build Priority Recommendation

### Proposed Build Sequence

| Priority | Module | Tier | Rationale |
|----------|--------|------|-----------|
| 1 | `Bayesian_Reasoning_Engine` | A | Richest data (44 atoms, 11 src mods). No dependency on other engines. |
| 2 | `Consistency_Reasoning_Engine` | A | coherence_formalism is ready. Low overlap. Core logical gate. |
| 3 | `Topological_Reasoning_Engine` | A | Fractal corpus maps directly. Distinct. No other engine touches it. |
| 4 | `Graph_Reasoning_Engine` | A | 27 atoms, cycle/dependency sources. Needed by Structural_Systems_Engine. |
| 5 | `Ontological_Reasoning_Engine` | A | iel_registry + pxl_schema + gen_worldview. Needed by Semantic_Integration_Engine. |
| 6 | `Logical_Coherence_Engine` | B | Depends on Consistency engine output. Use coherence_formalism seed. |
| 7 | `Structural_Systems_Engine` | B | Depends on Graph engine. system_utils + iel_integration as seeds. |
| 8 | `Causal_Reasoning_Engine` | B | causal_chain_node_predictor is a direct seed. |
| 9 | `Deductive_Reasoning_Engine` | B | arp_nexus + rule-based fragments from bayesian_nexus. |
| 10 | `ARP_L1_Aggregator` | NEW | Should be designed in parallel with Tier A — its schema drives L1 engine output contracts. |
| 11 | `ARP_L2_Synthesizer` | NEW | Design alongside first L2 engines. EpistemicArtifact schema needed early. |
| 12–21 | Remaining Tier B engines | B | Build in group-order: LOGICAL → STRUCTURAL → SEMANTIC → PATTERN |
| 22–27 | Tier C engines | C | Write fresh; schedule last. Pattern/Anomaly/Predictive can share design. |

### Coverage Summary by Group

| Group | Tier A Engines | Tier B Engines | Tier C Engines | Dataset Coverage |
|-------|--------------|--------------|--------------|-----------------|
| LOGICAL | Consistency | Deductive, Invariant, Abductive, Logical_Coherence | Inductive | Medium — coherence modules strong, inference logic thin |
| PROBABILISTIC | Bayesian | Causal, Causal_Dynamics | Uncertainty | Strong — Bayesian corpus is the best in the dataset |
| STRUCTURAL | Topological, Graph | Relational, Dependency, Structural_Systems | — | Strong — fractal + graph tools cover well |
| SEMANTIC | Ontological | Analogical, Relational | Semantic_Analysis, Metaphorical, Semantic_Integration | Weak — NLP/semantic tools were rejected (External_Dependency) |
| PATTERN | — | Complexity, Analogical | Pattern, Anomaly, Predictive, Dynamic_Pattern | Very weak — no pattern/dynamics legacy survives safety gates |

---

## SECTION 8 — Critical Observation: The Pattern/Dynamics Gap

The PATTERN group (Pattern_Detection, Anomaly_Detection, Predictive_Projection,
Dynamic_Pattern_Engine) has **zero legacy atom coverage**.

This is because:
1. Pattern/ML modules were primarily External_Dependency classified (rejected).
2. Runtime_Support modules with dynamics logic had subprocess/network side effects (rejected).
3. No pure-function pattern primitives were found in the staging area.

**Recommendation:** The 4 PATTERN engines should be treated as a separate
write-fresh sub-project using NORMALIZATION_PRIMITIVES and VALIDATION_PRIMITIVES
as infrastructure scaffolding. Consider whether lightweight stdlib-based
implementations (sliding window, frequency counting, moving average) satisfy
the Layer 1 performance targets (< 40ms).

---

## Validation

| Check | Result |
|-------|--------|
| Total engines analyzed | 25 |
| Tier A qualified | 5 |
| Tier B qualified | 10 |
| Tier C (write-fresh) | 10 |
| Aggregators (net-new) | 2 |
| Total proposed modules | 27 |
| Cross-engine atom overlap detected and flagged | YES |
| Zero rejected modules used as sources | CONFIRMED |
| Pattern group gap identified | CONFIRMED |

---

*End of ARP Module Proposal — 5 high-leverage / low-overlap builds recommended as priority.*
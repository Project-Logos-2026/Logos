# Capability Function Spec

**Status:** DESIGN-ONLY · NON-EXECUTABLE · NON-AUTHORITATIVE  
**Date:** 2026-02-19  
**Authority:** Requires human approval before downstream implementation  
**Scope:** Defines protocol capability vectors p_j(t) and proves boundedness of total cost C(ω)  
**Dependencies:** Constraint_Taxonomy_Spec.md (approved)

---

## 1. Purpose

This specification defines the **Capability Function** — the mapping from triad regions to per-protocol capability vectors — and proves that the total cost function C(ω) used by RGE is bounded, deterministic, and finite.

The Capability Function answers: "Given a task with triad profile t(x), how well does each protocol match that profile?"

The boundedness proof answers: "Can C(ω) ever diverge, oscillate unboundedly, or produce non-deterministic results?"

---

## 2. Protocol Domain Profiles (Repo-Grounded)

These profiles are derived from canonical repo artifacts, not from inference.

### 2.1 SCP — Synthetic Cognition Protocol (I1)

**Repo evidence:** I1AA schema fields: `fractal_configuration`, `modal_analysis_summary`, `causal_chain_findings`, `extrapolation_results`, `salvageability_assessment`. SMP mandatory-pass lens. Fractal/modal/causal analysis domain.

**Domain character:** Epistemic-dominant. SCP analyzes structure, coherence, and causal chains. It validates truth conditions and assesses epistemic stability. Structural grounding is secondary. Normative assessment is not in its mandate.

**Triad emphasis:** T-primary, E-secondary, G-minimal.

### 2.2 MTP — Meaning Translation Protocol (I2)

**Repo evidence:** MTP_README: 7-stage pipeline (projection → linearization → fractal evaluation → rendering → validation → I2 critique → emission). I2AA schema fields: `privation_stage`, `compression_results`, `semantic_enrichment_gaps`, `transformation_notes`. Language Governance Charter: "language renders meaning, does not create it." I2 provides translatability verification, privation surface checks, ontological grounding audits.

**Domain character:** Balanced with existential lean. MTP must realize output (E), preserve meaning coherence (T), and respect semantic obligations including privation awareness (G). It is the most balanced protocol because translation touches all three axes.

**Triad emphasis:** E-moderate, T-moderate, G-moderate. Slight E-lean because realizability is primary.

### 2.3 ARP — Advanced Reasoning Protocol (I3)

**Repo evidence:** ARP_README: 12 base reasoning engines (deductive, abductive, inductive, Bayesian, causal, topological, graph, relational, analogical, metaphorical, consistency, invariant), 5 taxonomical aggregators, PXL/IEL/Math integration. I3AA schema fields: `reasoning_domains_used`, `aggregation_summary`, `validation_conflicts`, `meta_reasoning_flags`.

**Domain character:** Epistemic-dominant with structural depth. ARP reasons, validates, detects contradictions, and aggregates multi-domain conclusions. Stronger structural grounding than SCP (topological, graph, relational engines). Normative reasoning is not primary but not absent (consistency with value constraints).

**Triad emphasis:** T-primary, E-secondary (stronger than SCP's E), G-weak.

### 2.4 LOGOS — Integrative Orchestration

**Repo evidence:** LogosAA schema fields: `pre_triune_analysis_ref`, `post_triune_integration_ref`, `convergence_assessment`, `conflict_resolution_notes`, `optimization_effect_summary`, `final_confidence_score`. Phase-G contract: `route_messages`, `manage_lifecycle`, `query_health`.

**Domain character:** Balanced integrator. Logos orchestrates across all three axes. Its purpose is convergence and conflict resolution, which requires balanced sensitivity to existential feasibility, epistemic coherence, and normative alignment.

**Triad emphasis:** E-moderate, G-moderate, T-moderate. Near-equal.

---

## 3. Triad Space Partition

The triad space is the set of all normalized triads t = (E, G, T) where E + G + T ≈ 1 and E, G, T ∈ [0, 1].

### 3.1 Partition Scheme: 7 Regions

Define:

```
max_axis(t) = max(E, G, T)
min_axis(t) = min(E, G, T)
```

| Region | ID | Condition | Interpretation |
|--------|----|-----------|---------------|
| E-strong | R_E | max_axis = E AND E > 0.5 | Existential pressure dominates |
| G-strong | R_G | max_axis = G AND G > 0.5 | Normative pressure dominates |
| T-strong | R_T | max_axis = T AND T > 0.5 | Epistemic pressure dominates |
| E-T pair | R_ET | max_axis ≤ 0.5 AND min_axis < 0.2 AND G = min_axis | Existential + epistemic, normative weak |
| E-G pair | R_EG | max_axis ≤ 0.5 AND min_axis < 0.2 AND T = min_axis | Existential + normative, epistemic weak |
| G-T pair | R_GT | max_axis ≤ 0.5 AND min_axis < 0.2 AND E = min_axis | Normative + epistemic, existential weak |
| Balanced | R_B | max_axis ≤ 0.5 AND min_axis ≥ 0.2 | No axis dominates |

### 3.2 Partition Properties

**Complete coverage:** Every point on the simplex E + G + T = 1 falls into exactly one region.

- If max_axis > 0.5 → one of R_E, R_G, R_T (mutually exclusive since at most one axis can exceed 0.5 when sum ≈ 1).
- If max_axis ≤ 0.5 and min_axis < 0.2 → one of R_ET, R_EG, R_GT (classified by which axis is minimal; ties broken alphabetically: E < G < T).
- If max_axis ≤ 0.5 and min_axis ≥ 0.2 → R_B.

**Tie-breaking:** If two axes are exactly equal and both maximal, use alphabetical precedence: E > G > T for max classification. If two axes are exactly equal and both minimal, use alphabetical precedence: E < G < T for min classification. This preserves determinism.

**No gaps, no overlaps.** The conditions form a complete partition.

---

## 4. Capability Vectors

For each protocol j ∈ {SCP, MTP, ARP, LOGOS} and each region R, define capability vector p_j(R) ∈ [0, 1]³.

The capability vector represents the protocol's strength profile — where in the triad space it operates most effectively. A protocol whose capability vector is close to the task triad is a good fit. A protocol whose capability vector is far from the task triad is a poor fit.

### 4.1 Capability Table

All vectors are normalized to sum to 1.0 (on the simplex).

```
                    R_E         R_G         R_T         R_ET        R_EG        R_GT        R_B
                  (E,G,T)     (E,G,T)     (E,G,T)     (E,G,T)     (E,G,T)     (E,G,T)     (E,G,T)

SCP (I1)        (0.20,0.10,0.70) (0.15,0.15,0.70) (0.15,0.10,0.75) (0.20,0.10,0.70) (0.20,0.15,0.65) (0.15,0.15,0.70) (0.20,0.10,0.70)

MTP (I2)        (0.40,0.25,0.35) (0.30,0.40,0.30) (0.30,0.25,0.45) (0.35,0.20,0.45) (0.40,0.35,0.25) (0.25,0.35,0.40) (0.35,0.30,0.35)

ARP (I3)        (0.25,0.15,0.60) (0.20,0.20,0.60) (0.20,0.15,0.65) (0.25,0.15,0.60) (0.25,0.20,0.55) (0.20,0.20,0.60) (0.25,0.15,0.60)

LOGOS           (0.40,0.30,0.30) (0.30,0.40,0.30) (0.30,0.30,0.40) (0.35,0.25,0.40) (0.35,0.35,0.30) (0.25,0.35,0.40) (0.34,0.33,0.33)
```

### 4.2 Reading the Table

Row = protocol. Column = triad region. Cell = capability vector.

Example: For a T-dominant task (region R_T), SCP's capability vector is (0.15, 0.10, 0.75). This means SCP is strongly T-aligned in T-heavy contexts, making it a good fit. MTP's vector is (0.30, 0.25, 0.45) — moderate T-alignment, less ideal for pure epistemic tasks.

### 4.3 Design Rationale

**SCP** is consistently T-heavy across all regions (0.65–0.75 on T axis). It shifts slightly: in E-heavy contexts, it contributes more E (structural grounding via fractal analysis). It never exceeds 0.15 on G because it has no normative mandate.

**MTP** is the most region-adaptive protocol. In E-heavy contexts it leans E (realizability is primary for translation). In G-heavy contexts it leans G (privation awareness, semantic obligations). In T-heavy contexts it leans T (coherence validation). It is never extreme on any axis because translation is inherently balanced.

**ARP** is T-heavy but less extremely than SCP (0.55–0.65 on T). It has stronger E contribution (0.20–0.25) than SCP because its reasoning engines include topological, graph, and relational analysis (structural grounding). G is weak (0.15–0.20) but slightly stronger than SCP's.

**LOGOS** mirrors the task region. In E-heavy contexts it leans E; in G-heavy it leans G; in T-heavy it leans T. In balanced contexts it is near-equilateral (0.34, 0.33, 0.33). This reflects its integrative function: it converges toward whatever the task requires.

### 4.4 Invariants

1. **All vectors sum to 1.0** (±0.01 for display rounding).
2. **All components ∈ [0, 1].**
3. **Table is static.** No runtime modification. No learning. No adaptation.
4. **Table is deterministic.** Same region → same vectors, always.
5. **Piecewise-constant.** Within a region, the vector is fixed. No interpolation between regions.

### 4.5 Future Refinement

If empirical observation reveals the 7-region partition is too coarse:

- Subdivide dominant regions (e.g., R_T into "T-strong-with-E" and "T-strong-with-G") for up to 13 regions.
- Or increase to a 27-cell grid (3×3×3 discretization of the simplex).
- Refinement must preserve: static table, deterministic lookup, bounded vectors, no learning.

---

## 5. Fit Cost Definition

### 5.1 Per-Axis Weighted L1 Distance

For a task triad t = (E_x, G_x, T_x) and protocol j with capability p_j(R(t)):

```
d(t, p_j) = α_E · |E_x - p_j^E| + α_G · |G_x - p_j^G| + α_T · |T_x - p_j^T|
```

Where α_E, α_G, α_T are axis weights.

**Default:** α_E = α_G = α_T = 1.0 (equal weighting across pillars).

### 5.2 Topology Fit Cost

A topology configuration ω assigns agents to axes. Each axis k ∈ {0, 1, 2, 3} is served by a protocol A_ω(k). The fit cost across all axes:

```
C_fit(ω; t) = Σ_{k=0}^{3} w_k · d(t, p_{A_ω(k)})
```

Where w_k are axis priority weights.

**Default:** w_k = 0.25 for all k (equal priority).

### 5.3 Fit Cost Bound

Since t ∈ [0,1]³ with sum ≈ 1 and p_j ∈ [0,1]³ with sum = 1:

```
d(t, p_j) = α_E·|E_x - p_j^E| + α_G·|G_x - p_j^G| + α_T·|T_x - p_j^T|
```

Maximum L1 distance between two points on the unit simplex is 2 (achieved when one point is a vertex and the other is the opposite edge midpoint).

Therefore: `d(t, p_j) ≤ max(α_E, α_G, α_T) · 2`

With default weights (all 1.0): `d(t, p_j) ≤ 2`

And: `C_fit(ω; t) ≤ Σ w_k · 2 = 4 · max(w_k) · 2`

With default weights: **C_fit ≤ 2.0**

---

## 6. Total Cost Function

### 6.1 Definition

```
C(ω) = C_fit(ω; t) + C_comm(ω; x) + C_stab(ω; x) + C_hyst(ω)
```

Where:

```
C_fit(ω; t) = Σ_{k=0}^{3} w_k · d(t, p_{A_ω(k)})

C_comm(ω; x) = γ · Σ_{k=0}^{3} w_k^prio(ω) · R_{A_ω(k)}(x)

C_stab(ω; x) = μ · Σ_{k=0}^{3} w_k^prio(ω) · (1 - S_{A_ω(k)}(x))

C_hyst(ω) = λ · switch(ω, ω_prev)
```

### 6.2 Parameter Definitions

| Parameter | Symbol | Default | Range | Meaning |
|-----------|--------|---------|-------|---------|
| Axis weights (fit) | α_E, α_G, α_T | 1.0 | [0, ∞) | Relative importance of E/G/T fit |
| Configuration weights | w_k | 0.25 | [0, 1] | Priority of axis k in topology |
| Commutation weight | γ | 1.0 | [0, ∞) | Importance of commutation preservation |
| Stability weight | μ | 1.0 | [0, ∞) | Importance of protocol stability |
| Hysteresis weight | λ | 0.5 | [0, ∞) | Switching cost penalty |
| Priority weights | w_k^prio(ω) | 1/4 | [0, 1] | Topology-derived priority for axis k |

### 6.3 Input Bounds

| Input | Symbol | Range | Source |
|-------|--------|-------|--------|
| Task triad | t = (E, G, T) | [0,1]³, sum ≈ 1 | Logos (Constraint Taxonomy Spec) |
| Capability vectors | p_j(R) | [0,1]³, sum = 1 | This spec (static table) |
| Commutation residuals | R_j(x) | [0, 1] | Logos (MESH validation) |
| Stability scalars | S_j(x) | [0, 1] | Logos (protocol telemetry) |
| Switch indicator | switch(ω, ω_prev) | {0, 1} | Hysteresis Governor |

---

## 7. Boundedness Proof

### 7.1 Theorem

**For any fixed parameter set (α, γ, μ, λ, w_k) and any valid inputs (t, R_j, S_j), the total cost C(ω) is bounded above by a finite constant B.**

### 7.2 Proof

**Bound on C_fit:**

For each axis k:

```
d(t, p_{A_ω(k)}) ≤ α_max · L1_max
```

where α_max = max(α_E, α_G, α_T) and L1_max = 2 (maximum L1 distance on the unit simplex).

```
C_fit ≤ Σ_{k=0}^{3} w_k · α_max · 2 = 2 · α_max · Σ w_k
```

Let W = Σ w_k. Then: **C_fit ≤ 2 · α_max · W**

With defaults (α_max = 1, W = 1): **C_fit ≤ 2** ∎

**Bound on C_comm:**

Each R_j(x) ∈ [0, 1]. Each w_k^prio(ω) ∈ [0, 1].

```
C_comm = γ · Σ w_k^prio · R_{A_ω(k)} ≤ γ · Σ w_k^prio · 1 = γ · W_prio
```

Let W_prio = Σ w_k^prio ≤ 4. Then: **C_comm ≤ 4γ**

With defaults (γ = 1, W_prio = 1): **C_comm ≤ 1** ∎

**Bound on C_stab:**

Each (1 - S_j(x)) ∈ [0, 1]. Same structure as C_comm.

**C_stab ≤ 4μ**

With defaults (μ = 1): **C_stab ≤ 1** ∎

**Bound on C_hyst:**

switch(ω, ω_prev) ∈ {0, 1}.

**C_hyst ≤ λ**

With defaults (λ = 0.5): **C_hyst ≤ 0.5** ∎

**Total bound:**

```
C(ω) = C_fit + C_comm + C_stab + C_hyst
     ≤ 2·α_max·W + 4γ + 4μ + λ
```

**With default parameters:**

```
C(ω) ≤ 2 + 1 + 1 + 0.5 = 4.5
```

Define: **B = 2·α_max·W + 4γ + 4μ + λ**

Then: **∀ω ∈ Ω, ∀t, ∀R, ∀S: C(ω) ∈ [0, B]** ∎

### 7.3 Corollaries

**Corollary 1 (Determinism):** C(ω) is a pure function of (ω, t, R, S, ω_prev) and fixed parameters. Same inputs → same output. No randomness.

**Corollary 2 (Finite search):** Since |Ω| = 192 and C is bounded, argmin C(ω) always exists and is computable by exhaustive enumeration.

**Corollary 3 (Stable tie-break):** When multiple ω achieve the same C, the canonical config_id tie-break (lexicographic on rotation index + sorted assignment string) produces a unique deterministic winner.

**Corollary 4 (No axis collapse):** The Trinitarian Optimization Theorem requires balanced triadic pressure. C_fit penalizes configurations where protocol capability is misaligned with task triad. A configuration that collapses to a single axis (all agents on T-heavy protocols for a balanced task) will have high C_fit, naturally preventing axis collapse.

**Corollary 5 (Monotone parameter sensitivity):** Increasing γ increases the relative importance of commutation. Increasing μ increases stability importance. Increasing λ increases switching resistance. All effects are linear and bounded.

---

## 8. Non-Degeneracy Conditions

For C(ω) to produce meaningful topology differentiation:

### 8.1 Required

- At least one scoring component must have non-zero weight. (Trivially satisfied with defaults.)
- Task triad must have at least one non-zero component. (Guaranteed by Constraint Taxonomy Spec edge case handling — zero-constraint tasks default to base topology without invoking scoring.)

### 8.2 Recommended

- α_E = α_G = α_T (equal axis weighting) unless there is a formally justified reason to deviate.
- γ, μ > 0 to ensure commutation and stability influence selection.
- λ > 0 to prevent thrashing.

---

## 9. Implementation Mapping

| Spec Element | Implementation Target | Notes |
|--------------|----------------------|-------|
| Capability table | `Triune_Capability_Table.json` | Static JSON, loaded at session init |
| Region classification | `Triad_Region_Classifier` function | Pure function, no state |
| C_fit | `Triune_Fit_Score.py` (ScoringInterface) | Plugs into Composite_Aggregator |
| C_comm | `Commutation_Balance_Score.py` (ScoringInterface) | Consumes R_j from telemetry |
| C_stab | `Divergence_Metric.py` update (ScoringInterface) | Consumes S_j from telemetry |
| C_hyst | `Hysteresis_Governor.py` (already built) | switch_threshold parameter |
| Composite C(ω) | `Composite_Aggregator.evaluate()` (already built) | Weighted sum of registered scorers |
| Exhaustive search | `Genesis_Selector.select_best()` (already built) | Enumerates 192 configs |

---

## 10. Invariants

1. **Boundedness:** C(ω) ∈ [0, B] for finite B determined by fixed parameters.
2. **Determinism:** Same (ω, t, R, S, ω_prev, params) → same C(ω). No randomness.
3. **Finite search:** 192 configurations, exhaustively evaluated.
4. **Static capability:** Table does not change at runtime. No learning. No adaptation.
5. **Piecewise-constant:** Capability vectors are constant within each region. No interpolation.
6. **Layer purity:** RGE looks up capability vectors. It does not compute them from protocol internals.
7. **Parameter fixity:** All parameters (α, γ, μ, λ, w_k) are fixed at session initialization. No within-session modification except via Logos override.

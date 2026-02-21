# Constraint Taxonomy Spec

**Status:** DESIGN-ONLY · NON-EXECUTABLE · NON-AUTHORITATIVE  
**Date:** 2026-02-19  
**Authority:** Requires human approval before downstream implementation  
**Scope:** Defines the classification rules for deriving the Task Triad vector `t(x) = (E_x, G_x, T_x)` from formal constraint accounting  
**Governing Ruling:** Three Pillars decomposition (E/G/T co-equal transcendentals). Bijection structure governs commutation verification, not constraint classification.

---

## 1. Purpose

This specification defines how runtime task constraints are classified into three co-equal axes to produce the Task Triad vector consumed by RGE's triune scoring pipeline.

The Task Triad is the sole input that connects LOGOS's formal mathematical commitments to RGE's topology optimization. Without this classification, RGE remains a geometry-only optimizer. With it, RGE becomes a triune-grounded topology advisor.

---

## 2. Three Axes (Co-Equal Transcendentals)

Each axis corresponds to one of the Three Pillars.

### 2.1 Existence Axis (E)

**Domain:** Ontological grounding — "does it exist, is it real, is it feasible?"

**Constraint types that count toward c_E:**

| Constraint Class | Description | PXL Lattice Anchor |
|-----------------|-------------|-------------------|
| Feasibility | Task requires a resource, state, or precondition to exist | Existence (X) |
| Grounding | Task depends on something being ontologically present | Existence (X) |
| Non-null | Input/output must be non-empty, non-void | Existence (X) |
| Realizability | A proposed artifact must be constructible | Distinction (D) |
| State dependency | Task depends on a specific system state being active | Existence (X) |
| Resource constraint | Bounded compute, memory, time, tick budget | Existence (X) |
| Uniqueness | A distinct entity must exist and be distinguishable | Distinction (D) |

**Lattice elements anchoring this axis:** Existence (X), Distinction (D)

**What does NOT count as E:** Agency obligations (→ G), even though Agency appears in Bijection B's sufficient triad. Per the anti-double-count rule, Agency is normatively framed and goes to G.

### 2.2 Truth Axis (T)

**Domain:** Epistemic coherence — "is it consistent, provable, valid?"

**Constraint types that count toward c_T:**

| Constraint Class | Description | PXL Lattice Anchor |
|-----------------|-------------|-------------------|
| Consistency check | Result must not contradict known state | Non-Contradiction (N) |
| Proof obligation | A formal claim must be verified | Identity (I) / Coherence (C) |
| Validation | Output must pass structural or semantic validation | Coherence (C) |
| Contradiction sensitivity | Task is flagged for contradiction risk | Non-Contradiction (N) |
| Logical completeness | All cases must be covered | Excluded Middle (E_m) |
| Coherence requirement | Multiple components must cohere | Coherence (C) |
| Truthfulness gate | Output must be veridical | Truth (T_r) |
| Determinism requirement | Same inputs must produce same outputs | Identity (I) |

**Lattice elements anchoring this axis:** Identity (I), Non-Contradiction (N), Excluded Middle (E_m), Truth (T_r), Coherence (C)

**What does NOT count as T:** Structural feasibility checks (→ E). Normative consistency (e.g., "does this violate ethical constraints?") goes to G, not T.

### 2.3 Goodness Axis (G)

**Domain:** Normative alignment — "is it good, right, aligned with purpose?"

**Constraint types that count toward c_G:**

| Constraint Class | Description | PXL Lattice Anchor |
|-----------------|-------------|-------------------|
| Goal/utility constraint | Task must serve a declared purpose | Goodness (G_o) |
| Preference ordering | Multiple options must be ranked by desirability | Goodness (G_o) |
| Harm-avoidance gate | Output must not cause declared harm | Goodness (G_o) |
| Teleological requirement | Task has an "ought" or "should" framing | Goodness (G_o) |
| Agency obligation | An agent must act, decide, or exercise autonomy | Agency (A) |
| Relational constraint | Task involves inter-entity obligations or mappings | Relation (R) |
| Value alignment | Output must align with declared values/norms | Goodness (G_o) |
| Governance compliance | Task must satisfy governance rules (normative, not structural) | Agency (A) |

**Lattice elements anchoring this axis:** Goodness (G_o), Agency (A), Relation (R)

**What does NOT count as G:** Structural relation checks (e.g., "do these two artifacts reference each other?") → T (coherence). Existential relation checks (e.g., "does this entity exist in relation to another?") → E.

---

## 3. Anti-Double-Count Rule

A single constraint instance is classified to exactly one axis. No constraint is counted on two axes.

### 3.1 Precedence Rules

When a constraint could plausibly belong to multiple axes, the following precedence applies:

**Rule 1: Normative framing wins for G.**
If a constraint involves "ought," "should," "must (ethically)," "prefer," "harm," "goal," or "purpose," it goes to G regardless of structural overlap with E or T.

**Rule 2: Coherence/proof framing wins for T.**
If a constraint involves "consistent," "valid," "provable," "contradicts," "complete," "deterministic," or "coherent," it goes to T regardless of structural overlap with E.

**Rule 3: E is the residual axis.**
If a constraint is neither normatively framed (G) nor epistemically framed (T), it goes to E. Existence is the default axis for structural/grounding constraints that do not carry normative or epistemic qualification.

### 3.2 Precedence Order

```
G (normative) > T (epistemic) > E (existential/residual)
```

This means: check for normative framing first. If absent, check for epistemic framing. If absent, classify as existential.

### 3.3 Examples

| Constraint | Classification | Reasoning |
|-----------|---------------|-----------|
| "Output must not be null" | E | Existential: non-null requirement |
| "Output must be logically consistent" | T | Epistemic: consistency check |
| "Output must not cause harm" | G | Normative: harm-avoidance |
| "Agent must decide between options" | G | Normative: agency obligation |
| "Result must be deterministic" | T | Epistemic: determinism = identity preservation |
| "Resource budget must not be exceeded" | E | Existential: resource constraint |
| "All proof obligations must be discharged" | T | Epistemic: proof obligation |
| "The preferred option should be selected" | G | Normative: preference ordering |
| "Entity X must exist before processing" | E | Existential: grounding dependency |
| "The mapping must preserve relations" | T | Epistemic: coherence between mapped structures |
| "Agent must exercise autonomy within bounds" | G | Normative: agency with governance |
| "Tick budget available" | E | Existential: resource feasibility |
| "Commutation must be preserved" | T | Epistemic: structural coherence (commutation is a formal property) |

---

## 4. Constraint Extraction Procedure

### 4.1 Input

A task instance `x` arriving at Logos Core, represented as a structured object containing:

- Declared constraints (explicit in task specification)
- Inferred constraints (derived by Logos from governance rules, SMP pipeline requirements, and active Phase contracts)

### 4.2 Extraction Steps (Deterministic)

```
PROCEDURE extract_triad(task x):

    c_E ← 0
    c_G ← 0
    c_T ← 0

    FOR EACH constraint k IN x.constraints:

        IF k has normative framing:
            c_G ← c_G + weight(k)

        ELSE IF k has epistemic framing:
            c_T ← c_T + weight(k)

        ELSE:
            c_E ← c_E + weight(k)

    RETURN (c_E, c_G, c_T)
```

### 4.3 Framing Detection Rules

**Normative framing indicators** (trigger G classification):
- Constraint references: goal, purpose, preference, harm, benefit, ought, should, value, agency, obligation, teleological, normative, ethical, aligned

**Epistemic framing indicators** (trigger T classification):
- Constraint references: consistent, valid, provable, coherent, contradicts, complete, deterministic, identity-preserving, verified, truthful, proof, logical, sound

**Existential framing (default E):**
- Everything else: exists, non-null, feasible, resource, state, grounding, realizability, bounded, available, constructible, distinguishable, unique

### 4.4 Determinism Guarantee

The extraction procedure is deterministic because:

1. Constraint enumeration order is fixed (sorted by constraint ID or declaration order).
2. Framing detection uses a fixed keyword/tag set, not NLP interpretation.
3. Precedence rules are total-ordered (G > T > E).
4. Weight assignment is defined in Section 5 (no runtime learning).

---

## 5. Weighting Rules

### 5.1 Default: Unit Weights

In the initial implementation, all constraints have weight 1.0:

```
weight(k) = 1.0  for all k
```

This means `c_E`, `c_G`, `c_T` are simple counts of constraints classified to each axis.

### 5.2 Optional: Tiered Weights

If constraint severity differentiation is needed, a two-tier system is defined:

| Tier | Weight | Criteria |
|------|--------|----------|
| Standard | 1.0 | Default for all constraints |
| Critical | 2.0 | Constraint is marked as fail-closed or governance-mandatory |

Critical constraints are those whose violation triggers immediate halt (per existing governance semantics). They contribute double weight to their axis.

### 5.3 Weight Source

Weights are assigned at constraint declaration time, not at classification time. The classifier reads pre-assigned weights. It does not compute, learn, or adjust weights.

---

## 6. Normalization

### 6.1 Formula

Given raw counts `(c_E, c_G, c_T)`:

```
S(x) = c_E + c_G + c_T + ε
```

Where `ε = 1e-10` (prevents division by zero for tasks with zero classified constraints).

```
E_x = c_E / S(x)
G_x = c_G / S(x)
T_x = c_T / S(x)
```

### 6.2 Properties

- `t(x) = (E_x, G_x, T_x) ∈ [0, 1]³`
- `E_x + G_x + T_x ≈ 1` (exactly 1 minus negligible ε contribution)
- Deterministic: same constraint set → same triad
- Bounded: all components in [0, 1]
- Audit-friendly: raw counts and normalized values are both logged

### 6.3 Edge Cases

| Case | c_E | c_G | c_T | Result | Handling |
|------|-----|-----|-----|--------|----------|
| No constraints | 0 | 0 | 0 | (≈0, ≈0, ≈0) | Fail-closed: RGE uses default topology (rotation_index=0). A task with zero constraints is either trivial or malformed. |
| Single axis dominant | 0 | 0 | 5 | (0, 0, 1) | Valid. Task is purely epistemic. RGE scores accordingly. |
| Perfectly balanced | 3 | 3 | 3 | (⅓, ⅓, ⅓) | Valid. Task is triune-balanced. Optimization theorem applies directly. |
| One constraint total | 1 | 0 | 0 | (1, 0, 0) | Valid but low-information. Hysteresis may hold prior topology. |

---

## 7. Telemetry Snapshot Structure

The triad, once computed by Logos, is delivered to RGE as part of an immutable telemetry snapshot. This snapshot is the interface contract between Logos (producer) and RGE (consumer).

### 7.1 Minimal Required Fields

```
{
    "task_id": "<string>",
    "tick_id": "<string>",
    "triad": {
        "E": <float ∈ [0,1]>,
        "G": <float ∈ [0,1]>,
        "T": <float ∈ [0,1]>
    },
    "raw_counts": {
        "c_E": <int ≥ 0>,
        "c_G": <int ≥ 0>,
        "c_T": <int ≥ 0>
    },
    "immutable": true
}
```

### 7.2 Optional Extended Fields

```
{
    "residuals": {
        "R_SCP": <float ∈ [0,1]>,
        "R_MTP": <float ∈ [0,1]>,
        "R_ARP": <float ∈ [0,1]>
    },
    "stability": {
        "S_SCP": <float ∈ [0,1]>,
        "S_MTP": <float ∈ [0,1]>,
        "S_ARP": <float ∈ [0,1]>
    },
    "hysteresis_key": "<string>"
}
```

Residuals (`R_j`) are per-protocol commutation residuals computed by Logos from MESH validation. Stability scalars (`S_j`) are per-protocol stability signals surfaced by Logos from protocol telemetry. Both are optional in the initial implementation and can be added when the relevant scoring modules are activated.

### 7.3 Immutability Contract

- Once produced, the telemetry snapshot MUST NOT be modified within the same tick.
- RGE MUST treat the snapshot as read-only.
- Logos MUST NOT alter the triad based on RGE output within the same tick.
- No feedback loops within a single tick boundary.

---

## 8. Relationship to Commutation Verification

The Three Pillars classification (this spec) and the bijection commutation structure (MESH) are complementary, not competing.

### 8.1 Classification vs. Verification

| Function | Governed By | Purpose |
|----------|------------|---------|
| Constraint classification into E/G/T | This spec (Three Pillars) | Produces the task triad for RGE scoring |
| Commutation validation Φ ∘ T_E = T_O ∘ Φ | MESH / Bijection structure | Produces commutation residuals R_j for RGE scoring |

### 8.2 Why They Don't Conflict

The bijection structure maps:

- Bijection A: {Identity, Non-Contradiction, Excluded Middle} → {Coherence, Truth} (epistemic domain)
- Bijection B: {Distinction, Relation, Agency} → {Existence, Goodness} (ontological domain)

The classification spec maps:

- T axis: Identity, Non-Contradiction, Excluded Middle, Truth, Coherence (epistemic constraints)
- E axis: Existence, Distinction (existential constraints)
- G axis: Goodness, Agency, Relation (normative constraints)

Goodness appears in Bijection B (ontological mapping target) AND on the G axis (normative classification). This is not a contradiction because:

- Bijection B says: Goodness is the ontological closure target of normative primitives (Relation, Agency).
- The G axis says: constraints framed normatively are classified as Goodness-axis.
- These are the same claim stated from two directions: the bijection maps normative structure to Goodness; the taxonomy classifies normative constraints under the Goodness axis.

### 8.3 Commutation Residual Computation

The commutation residual R(x) is computed by Logos using the bijection structure, NOT by RGE. The computation verifies:

```
Φ ∘ T_E(x) = T_O ∘ Φ(x)
```

If commutation holds, R(x) = 0. If not, R(x) measures the magnitude of the violation. Per-protocol attribution (R_SCP, R_MTP, R_ARP) identifies which protocol lens contributes most to the violation.

This residual is delivered to RGE as an optional telemetry field and consumed by the Commutation_Balance_Score module.

---

## 9. Downstream Dependencies

Once this spec is approved, the following artifacts become producible:

| Artifact | Type | Depends On |
|----------|------|-----------|
| Task_Triad_Derivation.py | Logos Core module | This spec (constraint classification rules) |
| Telemetry_Contract.json | Interface schema | Section 7 of this spec |
| Triune_Fit_Score.py | RGE ScoringInterface impl | Triad + Capability Function Spec |
| Commutation_Balance_Score.py | RGE ScoringInterface impl | Residuals from telemetry |
| Divergence_Metric.py (update) | RGE ScoringInterface impl | Stability from telemetry |
| Capability_Function_Spec.md | Design artifact | This spec + protocol analysis |

---

## 10. Invariants

1. **Determinism:** Same constraint set → same triad. No randomness, no learning, no NLP interpretation.
2. **Boundedness:** All triad components ∈ [0, 1]. Sum ≈ 1.
3. **Completeness:** Every constraint is classified to exactly one axis. No constraint is uncounted. No constraint is double-counted.
4. **Auditability:** Raw counts, classification decisions, and normalized values are all logged.
5. **Immutability:** The triad is frozen once computed. No within-tick mutation.
6. **Layer purity:** Logos computes the triad. RGE consumes it. RGE never classifies constraints.
7. **Fail-closed:** Zero-constraint tasks produce a near-zero triad. RGE defaults to base topology.

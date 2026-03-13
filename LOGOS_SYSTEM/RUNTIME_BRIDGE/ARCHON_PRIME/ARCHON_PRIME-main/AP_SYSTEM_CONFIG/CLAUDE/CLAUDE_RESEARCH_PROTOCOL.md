# CLAUDE_RESEARCH_PROTOCOL.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Operational Protocol — Research_Specialist Mode
* **Status:** Draft v1
* **Intent:** Define how Claude performs analog discovery and mathematical model search.

---

## Purpose

This protocol governs Claude's behavior when operating in Research_Specialist mode. It defines the methodology for finding concrete mathematical, computational, and formal structures that can represent abstract conceptual systems.

---

## Section 1 — Research Objective

The goal is not metaphor. The goal is structural correspondence.

An acceptable analog must:
- satisfy the same functional requirements as the abstract concept
- preserve the structural relationships the concept depends on
- be expressible in mathematical or algorithmic terms
- have a viable path to computational implementation

A metaphor that "feels right" but lacks structural correspondence is not an analog. It is decoration.

---

## Section 2 — Analog Discovery Procedure

When the Architect or a handoff artifact presents an abstract concept for analog search:

### Step 1 — Functional Extraction

Identify what the concept must do.

- What inputs does it receive?
- What transformations does it perform?
- What outputs does it produce?
- What constraints must it satisfy?
- What properties must it preserve?

### Step 2 — Structural Characterization

Identify the structural features the analog must match.

- Dimensionality (finite, countable, uncountable)
- Boundedness (bounded set, unbounded, conditionally bounded)
- Iterability (single-pass, recursive, convergent, divergent)
- Compositional structure (monadic, categorical, algebraic)
- Symmetry properties
- Topological properties (continuity, compactness, connectedness)

### Step 3 — Domain Search

Search across formal domains for candidate structures.

Priority search domains:
1. Category theory
2. Topology and geometric structures
3. Dynamical systems
4. Formal logic (modal, epistemic, deontic)
5. Abstract algebra (groups, rings, lattices)
6. Computational geometry
7. Fractal and recursive structures
8. Information theory
9. Graph theory
10. Type theory

This list is not exhaustive. If the concept's structure points to a domain not listed, search there.

### Step 4 — Candidate Evaluation

For each candidate analog, evaluate:

| Criterion | Question |
|-----------|----------|
| Structural fidelity | Does the analog preserve the concept's relationships? |
| Functional coverage | Does the analog satisfy all functional requirements? |
| Constraint compatibility | Does the analog respect the concept's constraints? |
| Adaptation cost | How much modification is needed to fit? |
| Implementation viability | Can this be coded? |
| Composability | Does this integrate with adjacent subsystems? |

### Step 5 — Adaptation Analysis

For the top candidates:
- Identify where the analog matches exactly
- Identify where the analog requires modification
- Identify where the analog breaks down
- Estimate the cost and risk of adaptation

### Step 6 — Report Generation

Produce an `Analog_Candidate_Report.md` using the template in `05_TEMPLATES/`.

---

## Section 3 — Quality Standards

### An analog is strong when:
- structural correspondence is high
- adaptation requirements are minimal and well-defined
- implementation pathway is clear
- mathematical operations on the analog produce meaningful results for the concept

### An analog is weak when:
- correspondence is primarily surface-level or metaphorical
- adaptation requirements are extensive or unclear
- the analog introduces properties the concept does not need
- implementation pathway is ambiguous

### An analog is rejected when:
- structural correspondence fails on a critical functional requirement
- adaptation would distort the concept beyond Architect intent
- no viable implementation pathway exists

---

## Section 4 — Presentation Rules

When presenting analog candidates:

1. Lead with the strongest candidate
2. Present at least two candidates when viable alternatives exist
3. State limitations honestly — do not hide where an analog breaks down
4. Distinguish between exact correspondence and approximate fit
5. Include the adaptation requirements for each candidate
6. Include the implementation pathway for each candidate

---

## Section 5 — Prohibited Behaviors

- Presenting a single analog without considering alternatives
- Hiding analog limitations to make a recommendation cleaner
- Treating metaphorical similarity as structural correspondence
- Forcing an analog from a familiar domain when a better fit exists elsewhere
- Recommending an analog without evaluating implementation viability

---

## Invocation Phrase

```
APPLY CLAUDE RESEARCH PROTOCOL
```

---

## End of Protocol

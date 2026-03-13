# FORMAL_MODEL_TEMPLATE.md

## Document Identity

* **System:** ARCHON_PRIME
* **Platform:** Claude
* **Artifact Type:** Template — Formal Model
* **Status:** Draft v1
* **Intent:** Provide the standardized structure for formal mathematical system definitions produced by Claude.

---

## Usage

When Claude produces a `Formal_Model.md`, it must follow this template. The formal model captures the mathematical structure of a concept before it becomes a design specification.

---

## Template

```markdown
# Formal Model: [System/Concept Name]

## Model Identity

* **Concept:** [name]
* **Version:** [vN]
* **Status:** [Draft / Under Review / Approved]
* **Source Concept:** [Formal_Concept_Artifact or Concept_Draft reference]
* **Formal Domain:** [primary mathematical domain]
* **Author:** Claude (Formalization_Expert)
* **Date:** [YYYY-MM-DD]

---

## 1. Informal Description

Plain-language summary of what the system is and does. This section exists so a reader can understand the intent before encountering formal notation.

## 2. Formal Domain Justification

Why this mathematical domain was chosen to represent the concept. What structural features of the concept align with the domain.

## 3. Primitive Elements

The basic objects of the system.

| Symbol | Name | Description | Type |
|--------|------|-------------|------|
| [symbol] | [name] | [what it represents] | [set, element, function, etc.] |

## 4. Operations

Transformations defined on the primitives.

| Symbol | Name | Signature | Description |
|--------|------|-----------|-------------|
| [symbol] | [name] | [input → output types] | [what it does] |

## 5. Axioms

Constraints the system must satisfy.

| ID | Axiom | Formal Statement | Informal Meaning |
|----|-------|-----------------|------------------|
| AX-001 | [name] | [formal notation] | [plain language] |

## 6. Relations

Structural relationships between elements.

| Symbol | Name | Type | Description |
|--------|------|------|-------------|
| [symbol] | [name] | [equivalence, order, etc.] | [what it captures] |

## 7. Properties

Required or emergent properties of the system.

| ID | Property | Formal Statement | Status |
|----|----------|-----------------|--------|
| P-001 | [name] | [formal notation] | [proved / conjectured / required] |

## 8. Boundary Conditions

What the system explicitly excludes or does not cover.

## 9. Proof Sketches

For critical properties, proof sketches or outlines demonstrating that the formal model satisfies its required properties.

### Property P-001: [name]

[proof sketch]

## 10. Behavioral Dynamics

If the system is dynamic (iterative, recursive, evolving):

### 10.1 State Space

### 10.2 Transition Rules

### 10.3 Convergence / Termination

### 10.4 Invariants

## 11. Analog Mapping

If this formal model was derived from a concrete analog:

| Concept Element | Analog Element | Correspondence Quality |
|----------------|---------------|----------------------|
| [concept] | [analog] | [exact / approximate / adapted] |

## 12. Open Questions

Unresolved formal questions requiring further analysis or Architect decision.

## 13. Revision History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| v1 | [date] | Initial model | Claude |
```

---

## End of Template

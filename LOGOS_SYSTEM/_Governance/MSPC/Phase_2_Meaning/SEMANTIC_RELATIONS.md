# Meaning Layer - Semantic Relation Types (Canonical)

This document defines the complete and closed set of Semantic Relation (SR) types
admitted by the LOGOS Meaning Layer.

Relations define how Semantic Primitives may be related WITHOUT implying:
- order
- execution
- causality
- control flow

This is a design-only governance artifact aligned to PXL semantic definitions.

---

SR-01 - grounds
Domain/Range: {Assertion, Commitment, Evaluation} -> {Grounding}
Directionality: Directed
Semantic Effect: Declares epistemic grounding.
Non-Implications: No causality, no execution, no temporal order.
PXL Alignment: Grounding relation in PXL kernel.

---

SR-02 - entails
Domain/Range: {Assertion} -> {Assertion}
Directionality: Directed
Semantic Effect: Logical entailment preserving truth.
Non-Implications: No procedural implication, no sequence.
PXL Alignment: Entailment semantics.

---

SR-03 - constrains
Domain/Range: {Constraint} -> {Assertion, Scope, Evaluation}
Directionality: Directed
Semantic Effect: Restricts admissible meaning states.
Non-Implications: No enforcement action, no execution.
PXL Alignment: Constraint semantics.

---

SR-04 - depends_on
Domain/Range: {Assertion, Evaluation} -> {Assertion, Grounding}
Directionality: Directed
Semantic Effect: Declares prerequisite meaning.
Non-Implications: No order, no scheduling.
PXL Alignment: Dependency semantics (acyclic at meaning level).

---

SR-05 - excludes
Domain/Range: {Assertion, Commitment} <-> {Assertion, Commitment}
Directionality: Symmetric
Semantic Effect: Mutual incompatibility.
Non-Implications: No resolution mechanism implied.
PXL Alignment: Incompatibility semantics.

---

SR-06 - compatible_with
Domain/Range: {Assertion, Commitment} <-> {Assertion, Commitment}
Directionality: Symmetric
Semantic Effect: Mutual admissibility.
Non-Implications: No preference or selection implied.
PXL Alignment: Compatibility semantics.

---

SR-07 - refines
Domain/Range: {Assertion} -> {Assertion}
Directionality: Directed
Semantic Effect: Increases specificity without changing truth value.
Non-Implications: No replacement, no override.
PXL Alignment: Refinement semantics.

---

SR-08 - abstracts
Domain/Range: {Assertion} -> {Assertion}
Directionality: Directed
Semantic Effect: Decreases specificity while preserving truth.
Non-Implications: No loss of validity.
PXL Alignment: Abstraction semantics.

---

Global Relation Invariants

- Relations are non-temporal and non-procedural
- No relation implies execution or control
- No implicit sequencing
- Dependency relations must be acyclic at the meaning level
- All relations must preserve I1 consistency

---

Status

Semantic Relations: FINALIZED
Semantic Invariants: PENDING
Semantic State Conditions: PENDING

# LOGOS — Semantic State × Transformation Admissibility Matrix

**Directory:** `_Governance/Sequencing/`  
**Status:** Design-Only (Derived, Non-Normative)  

This matrix is derived directly from Meaning Layer Step Two.
It introduces no new semantics.

Legend:
✔ = admissible  
✖ = prohibited  

| Transformation Type | COMPLETE | PARTIAL | UNRESOLVED | INADMISSIBLE |
|---------------------|----------|---------|------------|--------------|
| TT-01 Definitional_Unfolding | ✔ | ✔ | ✔ | ✖ |
| TT-02 Equivalence_Rewrite | ✔ | ✔ | ✖ | ✖ |
| TT-04 Grounding_Lift | ✔ | ✔ | ✖ | ✖ |
| TT-05 Coherence_Globalization | ✔ | ✖ | ✖ | ✖ |
| TT-06 Global_Entailment_Extraction | ✔ | ✖ | ✖ | ✖ |
| TT-07 Privative_Collapse | ✔ | ✖ | ✖ | ✖ |
| TT-08 Knowledge_Lift | ✔ | ✖ | ✖ | ✖ |
| TT-09 Dependency_Substitution | ✔ | ✖ | ✖ | ✖ |
| TT-10 S2_Domain_Boundary_Transport | ✔ | ✔* | ✖ | ✖ |

*TT-10 is admissible in PARTIAL only if explicitly declared non-resolving.

Notes:

- INADMISSIBLE admits no transformations.
- UNRESOLVED admits only non-resolving normalization.
- PARTIAL admits only normalization and grounding enforcement.
- COMPLETE admits only invariant-preserving transformations.

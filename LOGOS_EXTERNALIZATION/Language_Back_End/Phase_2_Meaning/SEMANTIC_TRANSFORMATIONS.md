# Meaning Layer - Step Two: Semantic Transformations (Canonical)

This document defines the complete set of allowed Semantic Transformation Types (TT)
for the LOGOS Meaning Layer.

Transformations are meaning-preserving operations that:
- do not imply order
- do not imply execution
- do not encode control flow
- do not introduce autonomy

They are declarative constraints over admissible meaning state changes.

Representation requirement:
Each TT must admit:
1) PXL formal representation (proof artifacts later)
2) structural/arithmetic shadow (bounded deltas)
3) natural language rendering (explanation-only)

Traceability:
Each TT lists its PXL semantic anchor files for consistency.

---

## Admissibility (SSC Gate)

Unless explicitly stated otherwise:
- TT applies only when Semantic Invariants hold.
- TT must not resolve Unknown or Uncertainty implicitly.

Default admissibility:
- COMPLETE: allowed if effects do not violate invariants
- PARTIAL: allowed only for normalization/projection/grounding enforcement
- UNRESOLVED: allowed only for projection/normalization that does not claim resolution
- INADMISSIBLE: no TT is allowed

---

## TT-01 Definitional_Unfolding
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Definitions.v
Admissible: COMPLETE, PARTIAL, UNRESOLVED
Effects (bounded):
- Replace a defined symbol with its definitional meaning
- No new primitives introduced
- No new commitments introduced
Preserves:
- All Semantic Invariants (no meaning drift)

---

## TT-02 Equivalence_Rewrite
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Definitions.v (MEquiv) and derived intro/elim patterns
Admissible: COMPLETE, PARTIAL
Effects (bounded):
- Rewrite across established equivalence without changing truth conditions
- Must not expand scope
Preserves:
- Non-contradiction and no implicit commitments

---

## TT-03 Identity_Substitution
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (modus_groundens)
Admissible: COMPLETE
Effects (bounded):
- Substitute along identity (x Ident y) in entailment-bearing structures
- No new assertions introduced
Preserves:
- Identity preservation; scope boundedness

---

## TT-04 Grounding_Lift
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (grounding_yields_entails)
Admissible: COMPLETE, PARTIAL
Effects (bounded):
- From grounded_in(P,x), introduce entails(x,P)
- Does not assert truth directly; only entailment registration
Preserves:
- Grounding validity; no implicit authority

---

## TT-05 Coherence_Globalization
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (coherence_lifts_entailment)
Admissible: COMPLETE
Effects (bounded):
- From coherence(O) and entails(x,P), introduce entails(O,P)
- No expansion beyond declared coherence precondition
Preserves:
- Non-contradiction; no autonomy; scope boundedness

---

## TT-06 Global_Entailment_Extraction
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (entails_global_implies_truth)
Admissible: COMPLETE
Effects (bounded):
- From entails(O,P), register P as established within the meaning state
- Must be explicit and traceable (no hidden assertions)
Preserves:
- Non-contradiction; no implicit commitments

---

## TT-07 Privative_Collapse
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (privative_collapse)
Admissible: COMPLETE
Effects (bounded):
- If not possible that entails(O,P), classify P as incoherent (semantic invalidity marker)
- Does not execute; records semantic inadmissibility
Preserves:
- I1 consistency; denial of implicit resolution

---

## TT-08 Knowledge_Lift
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (Perfect_self_knowledge)
Admissible: COMPLETE
Effects (bounded):
- From grounded_in(p,x), register K(x,p) as epistemic transparency-to-ground
- No new truth claims introduced beyond grounding
Preserves:
- Grounding validity; no autonomy

---

## TT-09 Dependency_Substitution
PXL Anchor: STARTUP/PXL_Gate/coq/src/PXL_Kernel_Axioms.v (triune_dependency_substitution)
Admissible: COMPLETE
Effects (bounded):
- Under explicit grounded dependencies and equivalence, register coherence constraints
- Must not introduce cycles; must preserve dependency acyclicity
Preserves:
- Dependency acyclicity; I1 consistency

---

## TT-10 S2_Domain_Boundary_Transport (Atomic-at-Meaning-Layer)
PXL Anchor: STARTUP/PXL_Gate/coq/src/baseline/PXL_S2_Axioms.v
Admissible: COMPLETE (optionally PARTIAL if explicitly declared non-resolving)
Effects (bounded):
- Treat S2 as a single semantic transport transformation at the Meaning Layer
- Internal recognition/decompose/recombine is NOT exposed as sequence here
Preserves:
- Identity and coherence preservation constraints as declared in PXL S2 axioms

---

## Status

Transformation Types: FINALIZED
Admissibility Rules: FINALIZED (coarse-grained; refine only if needed)
Effects: FINALIZED (bounded, non-procedural)
Sequencing: NOT DEFINED HERE

# AF-PXL-VALIDATE — Proof-Anchored Planning (Design-Only)

## Status
- Design-only
- No implementation
- No proof execution
- Runtime_Control authoritative

## Purpose
Define the proof obligations and downgrade semantics required to legitimately
implement AF-PXL-VALIDATE in the future.

## Scope
Application Function:
- AF-PXL-VALIDATE

## Required Proof Artifacts (Coq)
Expected modules (names authoritative, contents pending):
- PXL_Relation_Soundness.v
- PXL_Modal_Soundness.v
- PXL_Relation_Closure.v

## Proof Obligations
- OBL-PXL-REL-SOUND:
  Relation validation implies no contradiction under PXL axioms.
- OBL-PXL-MOD-SAFE:
  Modal necessity/possibility handling is sound under S5 semantics.
- OBL-PXL-REL-CLOSE:
  Validation preserves closure properties (no expansion of claims).

## Downgrade & Failure Semantics
- Missing proof artifact → heuristic_only downgrade
- Proof mismatch → DENY + audit entry
- Partial proof → heuristic_only downgrade
- No proof refs allowed to escalate epistemic labels

## Runtime_Control Interaction
- Invocation requires AF registration
- Outputs labeled at or below weakest-epistemic level
- Any attempt to escalate without proof → DENY

## Non-Goals
- No logic implementation
- No Coq compilation
- No runtime wiring

## Status
Planning complete. Implementation NOT authorized.

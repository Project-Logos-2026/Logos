# AF-UNIFIED-AGGREGATE — Proof-Anchored Planning (Design-Only)

## Status
- Design-only
- No implementation
- No proof execution
- Runtime_Control authoritative

## Purpose
Define the proof obligations and downgrade semantics required to legitimately
implement AF-UNIFIED-AGGREGATE in the future.

## Scope
Application Function:
- AF-UNIFIED-AGGREGATE

## Required Proof Artifacts (Coq)
Expected modules (names authoritative, contents pending):
- PXL_Epistemic_Ordering.v
- IEL_Domain_Compatibility.v
- Aggregation_Weakest_Epistemic.v

## Proof Obligations
- OBL-UNIFIED-WEAK:
  Aggregation must not elevate epistemic status above the weakest input.
- OBL-UNIFIED-COMPAT:
  Aggregated domains are mutually compatible under IEL constraints.
- OBL-UNIFIED-NONESC:
  Aggregation cannot introduce new claims or authority.

## Downgrade & Failure Semantics
- Missing proof artifact → heuristic_only downgrade
- Any attempted escalation → DENY + audit entry
- Partial proofs → heuristic_only downgrade
- Conflicting inputs → downgrade or DENY (as specified)

## Runtime_Control Interaction
- Invocation requires AF registration.
- Inputs must already be labeled.
- Outputs capped at weakest-epistemic level.
- Any mismatch → DENY.

## Non-Goals
- No logic implementation
- No aggregation heuristics
- No runtime wiring

## Status
Planning complete. Implementation NOT authorized.

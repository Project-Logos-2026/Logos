# Phase-2.4 Plan Validation Pipeline (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Validation Order
1) privation
2) provenance
3) role
4) memory-read safety (per Phase-2.2)
5) plan coherence (structural checks only)

## Outcomes
- ACCEPTABLE (inert): no side effects; plan remains data only.
- REJECTED (with rejection_reason): fail-closed; no state change.

## Prohibitions
- No execution, activation, scheduling, continuation, or persistence.
- No mutation of SMPs or memory.
- No partial acceptance or conditional execution.

Declarative only; no runtime logic is added.

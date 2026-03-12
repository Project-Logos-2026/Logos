# Phase-2.4 Plan Rejection Semantics (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Fail-Closed Conditions
- Missing required fields (plan_id, intent_description, referenced_SMPs, constraints, validation_status, temporal_scope).
- Ambiguity or inconsistency in constraints or referenced_SMPs.
- Any privation match.
- Provenance missing or invalid for plan or referenced SMPs.
- Role not authorized per memory safety rules.
- Memory-read safety not satisfied.

## Behavior on Rejection
- Set validation_status to REJECTED with rejection_reason populated.
- No state change, no execution, no scheduling, no persistence.
- Audit logging required (design-only requirement).

This is declarative; it adds no runtime code or authorization objects.

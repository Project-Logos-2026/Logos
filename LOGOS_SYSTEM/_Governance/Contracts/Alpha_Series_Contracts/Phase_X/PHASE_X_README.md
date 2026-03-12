# Phase-X — Emergency Halt & Override Semantics

Status: DESIGN_ONLY

Phase-X defines absolute emergency halt authority.
Halt supersedes all other authorities and is terminal.

## Authoritative Artifacts

- PHASE_X_ENTRY.json
- halt_override_semantics_schema.json
- halt_override_invariants.json
- halt_override_denial_conditions.json
- PHASE_X_AUDIT_CLOSURE_CRITERIA.md

## Guarantees

- Halt overrides execution, planning, goals, time, ticks, and autonomy
- Halt requires no preconditions
- Halt cannot be overridden
- Halt introduces no execution or continuation

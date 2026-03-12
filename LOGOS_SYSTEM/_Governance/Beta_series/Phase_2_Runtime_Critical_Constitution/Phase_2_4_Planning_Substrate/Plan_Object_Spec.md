# Phase-2.4 Plan Object Specification (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)
Scope: Canonical, inert plan object schema. Plans are data only and cannot execute, schedule, tick, continue, or persist.

## Required Fields
- plan_id: unique identifier for the plan object (opaque, immutable).
- intent_description: declarative description of the intended outcome; no embedded actions.
- referenced_SMPs: list of SMP identities referenced; SMPs remain canonical and provenance-bound.
- constraints: set of applicable constraints, including privation matches, provenance requirements, and role boundaries.
- validation_status: ACCEPTABLE or REJECTED (design-only). No partial or provisional states.
- rejection_reason: mandatory when validation_status is REJECTED; empty otherwise.
- temporal_scope: descriptive time context (e.g., intended window); confers no scheduling or tick authority.

## Prohibitions
- No execution, scheduling, ticking, continuation, or chaining.
- No persistence or reuse across ticks by default.
- No implicit authority escalation or side effects.

Declarative only; introduces no executable logic or authorization objects.

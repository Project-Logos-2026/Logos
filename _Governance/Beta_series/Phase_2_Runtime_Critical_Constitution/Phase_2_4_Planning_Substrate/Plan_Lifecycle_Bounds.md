# Phase-2.4 Plan Lifecycle Bounds (Design-Only)

Status: DESIGN_ONLY
Authority: DENY (default)

## Lifecycle
- create → validate → discard

## Explicit Denials
- No execution or activation.
- No scheduling, ticking, or continuation.
- No persistence or reuse across ticks by default.
- No chaining of plans or escalation of authority.

Plans remain inert data objects; any deviation is denied by default. Declarative only; no runtime logic is added.

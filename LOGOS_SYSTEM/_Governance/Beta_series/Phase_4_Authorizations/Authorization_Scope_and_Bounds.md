# Authorization Scope and Bounds (Design-Only)

Status: DESIGN_ONLY — NON-EXECUTABLE — NON-AUTHORIZING
Authority: DENY (default)

## Bounding Principles
- Capability limits must be explicit and enumerated.
- Temporal limits must be explicit (start/end); no indefinite scopes by default.
- Resource limits must be explicit; no implicit expansion.

## Explicit Denials
- No scope escalation beyond stated bounds.
- No inheritance or delegation of authority.
- No transitive authority or chaining.

No execution, activation, scheduling, or persistence is implied. All ambiguity resolves to denial.

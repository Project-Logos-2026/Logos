# PMTE ↔ IGL Cross-Validation Matrix

This matrix formalizes the boundary between protocol admissibility (PMTE)
and invocation permissibility (IGL).

## PMTE Classifications

| PMTE Classification | Meaning |
|--------------------|--------|
| FORBIDDEN | Protocol is intrinsically non-governable |
| CONDITIONALLY_ADMISSIBLE | Protocol is structurally governable in principle |

## IGL Invocation Outcomes

| IGL Risk Class | Meaning |
|---------------|--------|
| DENIED | Invocation impermissible in principle |
| THEORETICALLY_BOUNDABLE | Invocation conceivable but unsafe |
| STRICTLY_CONSTRAINED | Invocation hypothetically boundable under maximal constraints |
| UNSAFE_BY_COMPOSITION | Invocation unsafe when combined |

## Cross-Layer Rules

| PMTE | Invocation Context | IGL Outcome |
|-----|-------------------|------------|
| FORBIDDEN | Any | DENIED |
| CONDITIONALLY_ADMISSIBLE | Any context with persistence | DENIED |
| CONDITIONALLY_ADMISSIBLE | Any context with repetition | DENIED |
| CONDITIONALLY_ADMISSIBLE | Any non-revocable context | DENIED |
| CONDITIONALLY_ADMISSIBLE | Any compositional context | DENIED |
| CONDITIONALLY_ADMISSIBLE | Single-step, revocable, non-persistent, non-composed | STRICTLY_CONSTRAINED |

## Canonical Rule

PMTE approval never implies invocation permission.
IGL assessment never implies execution authorization.

All evaluations are hypothetical and discard-only.

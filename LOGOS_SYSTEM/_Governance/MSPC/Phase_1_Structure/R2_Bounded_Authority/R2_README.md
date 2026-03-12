# R2 — Bounded Authority (Explicit, Scoped, Revocable)

**Phase:** R2 (Design-Only)
**Authority Granted:** NONE (definition stage)
**External IO:** NONE
**Persistence:** NONE (beyond governed audit spine)
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Purpose & Scope

Define how authority could be **explicitly granted** under strict bounds:
scoped, time/tick-bounded, and revocable. This phase remains definition-only and
does not grant or enable authority.

## Non-Goals

- No implicit or transitive grants.
- No authority accumulation or chaining.
- No external IO or persistence beyond the governed audit spine.
- No scheduling, planning, or continuation enablement beyond explicit scope.
- No autonomy or self-authorization.

## Preconditions

- R0 and R1 artifacts are present and active; eligibility and evaluation are in force.
- Privation and revocation supremacy remain dominant and verified.
- Audit channel is reachable for grant lifecycle events.
- Bounded scopes and TTL/tick budgets are defined and non-extendable.

## Disqualifiers

Any of the following forces denial and halt:

- Missing provenance for scope, issuer, or TTL definitions.
- Attempted implicit grant, delegation, or inference.
- Revocation channel unavailable or unverifiable.
- Ambiguity in grant class, scope, or budget.
- Detection of accumulation, chaining, or persistence beyond scope.

## Halt Semantics (Fail-Closed)

- Ambiguity or revocation weakness → denial and halt.
- No grants survive a halt; revocation is default.
- Termination reason is recorded in the governed spine; missing reasoning is failure.

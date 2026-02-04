# R3 — Semantic Contract

**Phase:** R3 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Continuation Definition

- **Continuation:** A supervised, bounded sequence of ticks authorized explicitly
  by governance. Continuation is not self-directed and cannot extend itself.
- **Continuation Envelope:** Immutable description of allowed actions, tick budget,
  supervision identity, and termination conditions.

## Pre-Continuation Invariants

- R0 tick binding and R1 evaluation references are available.
- Any R2 grants required for actions exist, are in-force, and are revocable.
- Continuation envelope is immutable and provenance-verified.
- Budgets (ticks/time) are defined and non-extendable.
- Supervisory channel and revocation paths are verified reachable.

## In-Continuation Invariants

- No self-extension or modification of the envelope.
- Each tick conforms to R0 invariants and is individually auditable.
- Revocation supremacy applies at every step; supervision can halt immediately.
- No background or unsignaled work between ticks.

## Post-Continuation Invariants

- All ticks accounted for with audit entries and termination reasons.
- No residual authority, continuation handles, or budgets persist beyond envelope.
- Revocation status recorded; any pending tasks are denied and halted.

## Continuation Flow (Conceptual)

1. **Authorize Envelope:** Governance issues a continuation envelope with fixed
   bounds and supervision identity; self-issuance is forbidden.
2. **Pre-Flight Check:** Validate invariants; if ambiguous, deny and halt.
3. **Tick-by-Tick Execution:** For each tick, run R0 flow and applicable R2 grant
   checks; supervision remains active.
4. **Supervision & Revocation:** Supervisory channel can halt at any tick; revocation
   is immediate and dominant.
5. **Audit & Terminate:** Record audit per tick and a final continuation summary;
   enforce deterministic halt at envelope completion or on failure.

Ambiguity or supervision loss triggers immediate halt and denial.

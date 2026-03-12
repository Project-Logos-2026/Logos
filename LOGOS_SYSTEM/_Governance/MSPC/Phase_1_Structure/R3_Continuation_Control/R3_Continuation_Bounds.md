# R3 — Continuation Bounds

**Phase:** R3 (Design-Only)
**Authority Granted:** NONE
**Continuation:** Bounded, supervised, non-self-directed

---

## Budgeting Rules

- **Tick Budget:** Fixed maximum number of ticks; cannot be extended or replenished.
- **Time Budget:** Optional wall-clock limit; cannot be extended.
- **Action Budget:** Optional bound on governed actions per tick; cannot be extended.

## Boundaries and Prohibitions

- No self-extension of tick/time/action budgets.
- No implicit continuation; every sequence requires an explicit envelope.
- No background or hidden ticks; all ticks are declared and auditable.
- No execution outside the envelope scope; violations trigger halt and revocation.

## Termination Conditions

- Budget exhaustion (tick/time/action) → halt.
- Revocation by supervision or governance → halt.
- Invariant breach (scope, budget, privation, revocation) → halt.
- Audit failure or observability loss → halt.

## Denial Conditions

- Ambiguity in envelope bounds or supervising identity.
- Missing revocation proof or unresolved revocation token.
- Attempted chaining or parallel continuations without explicit governance.

## Post-Termination Requirements

- Final audit summary referencing all tick entries and termination reason.
- No residual handles, timers, or schedules remain active.

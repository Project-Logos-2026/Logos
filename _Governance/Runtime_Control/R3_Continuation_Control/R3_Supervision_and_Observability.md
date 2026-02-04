# R3 — Supervision and Observability

**Phase:** R3 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO

---

## Supervision Requirements

- A designated supervising governance identity must be bound to the continuation
  envelope; self-supervision is forbidden.
- Supervisor must have active revocation rights and reachable signaling paths.
- Supervisor can halt at any tick without consent from the controlled entity.

## Observability Requirements

- Per-tick audits (see R3 Audit Spec) are mandatory and real-time reachable.
- State visibility must be sufficient to prove no external IO or unauthorized
  persistence occurred.
- Loss of observability is treated as an invariant breach and triggers halt.

## Monitoring Signals (Allowed)

- Tick progression and budget consumption.
- Revocation channel health and responsiveness.
- Scope adherence (actions constrained to envelope and any R2 grants in-force).
- Absence of background tasks between ticks.

## Prohibited Behaviors

- Deferred or batched supervision that could hide per-tick behavior.
- Asynchronous continuations without explicit supervisory acknowledgment.
- Any attempt to suppress or delay revocation signals.

## Failure Handling

- Supervision loss, monitoring gaps, or delayed revocation triggers → immediate
  halt and audit.
- Any ambiguity in supervisory authority or identity → denial.

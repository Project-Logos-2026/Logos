# R3 — Continuation Control (Multi-Tick Continuation Without Self-Direction)

**Phase:** R3 (Design-Only)
**Authority Granted:** NONE
**External IO:** NONE
**Persistence:** NONE (beyond governed audit spine)
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Purpose & Scope

Define how bounded continuation across ticks could occur under strict supervision
and revocation. Continuation remains **non-self-directed** and must respect explicit
budgets and termination conditions.

## Non-Goals

- No self-extension or self-directed scheduling.
- No background loops or indefinite continuations.
- No external IO or persistence beyond the governed audit spine.
- No authority escalation or inference.
- No autonomy enablement.

## Preconditions

- R0–R2 artifacts are present and active (eligibility, evaluation, bounded grants).
- Continuation budgets (ticks/time) are defined and non-extendable.
- Supervisory authority and revocation channels are verified and reachable.
- Deterministic halt path is available for any failure.

## Disqualifiers

Any of the following forces denial and halt:

- Ambiguity in continuation plan, bounds, or supervising identity.
- Missing or unreachable revocation channel.
- Attempted self-extension or scheduling by the controlled entity.
- Detection of background loops or persistence outside the governed spine.
- Loss of observability or audit reachability.

## Halt Semantics (Fail-Closed)

- On any ambiguity, invariant breach, or supervision loss → immediate halt.
- Continuation budgets are consumed; no retries or silent restarts.
- Termination reason is recorded; absence of a reason is failure.

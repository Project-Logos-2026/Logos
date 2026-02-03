# R0 — Semantic Contract

**Phase:** R0 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Formal Definitions

- **Tick:** A single, bounded execution window governed by R0. One tick is admitted
  only if all preconditions hold; it does not imply autonomy or authority.
- **Tick Envelope:** The minimal, governed set of inputs and constraints that define
  the tick (identity, budget, invariants). Envelopes are immutable during the tick.
- **Internal-Only Execution:** No external IO, no persistence beyond the governed
  audit spine, and no interaction with systems outside the Runtime spine.

## Pre-Tick Invariants

- Tick identity and envelope are validated and immutable.
- Tick budget is positive, fixed, and non-extendable.
- Privation and revocation semantics are active and verifiable.
- Audit channel is reachable and ready to accept entries.
- No pending authority, autonomy, or continuation state exists.

## Post-Tick Invariants

- No external side effects occurred (IO, persistence, scheduling).
- Tick budget is decremented to zero or the defined consumption level; no surplus
  is auto-carried or reused.
- All invariants remain satisfied; any breach forces halt.
- Audit record is emitted with termination reason.
- System remains in denial posture (no new authority, autonomy, or continuation).

## Tick Flow (Conceptual)

1. **Pre-Check:** Validate preconditions and invariants; if ambiguous, deny.
2. **Tick Execution (Internal-Only):** Execute the governed payload under the fixed
   envelope; no self-modification, no new claims.
3. **Post-Check:** Re-validate invariants and detect any side effects or drift.
4. **Audit:** Emit the tick audit entry with required fields (see Audit Spec).
5. **Halt:** Deterministic halt; no retries, no background continuation.

Any ambiguity or partial success is treated as failure and triggers immediate halt.

## Audit Event Requirements (Per Tick)

Each tick **must** emit an audit event containing:

- Tick identity (monotonic, non-reusable).
- Envelope hash (immutability proof of constraints and inputs).
- Pre-check outcome and any disqualifiers triggered.
- Budget baseline and consumption.
- Post-check outcome and invariant status.
- Termination reason (enumerated) and timestamp.

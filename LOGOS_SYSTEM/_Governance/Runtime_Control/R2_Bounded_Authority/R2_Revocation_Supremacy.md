# R2 — Revocation Supremacy

**Phase:** R2 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Posture:** REVOCATION DOMINATES ALL OPERATIONS

---

## Revocation Principles

- Revocation overrides issuance, use, continuation, and renewal attempts.
- Revocation is immediate, unilateral, and does not require subject consent.
- Failure modes resolve to revocation; ambiguity is treated as grounds to revoke.

## Revocation Triggers (Non-Exhaustive)

- Invariant breach (scope, ttl, tick limit, constraints).
- Conflict with privation semantics or denial conditions.
- Audit channel failure or loss of observability.
- Detected accumulation, chaining, delegation, or inference of authority.
- Expiry of ttl/tick_limit or budget exhaustion.
- Governance directive to halt.

## Revocation Enforcement

- Revocation token must be checked before each use; inability to resolve → deny.
- Once revoked, the grant cannot be reinstated without full re-issuance.
- All revocations produce audit entries with cause, timestamp, and issuer.

## Failure Semantics

- If revocation cannot be proven available, **no grant is valid**.
- If revocation signaling is delayed or uncertain, halt and deny.
- Revocation status is part of post-use verification; missing proof voids use.

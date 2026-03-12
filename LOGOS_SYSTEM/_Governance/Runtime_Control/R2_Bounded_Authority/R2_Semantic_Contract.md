# R2 — Semantic Contract

**Phase:** R2 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Authority Object Definition

A bounded authority grant is a **revocable, scoped permission** with the following
minimal fields:

- `grant_id` — unique, non-reusable identifier.
- `grant_class` — one of the defined authority classes (read, propose, plan, execute,
  persist); each class is independent.
- `scope` — explicit bounds on objects, operations, and contexts.
- `ttl` / `tick_limit` — expiration in wall-clock or tick units; non-extendable
  without re-issuance.
- `issuer` — governance identity authorized to issue; must itself be validated.
- `revocation_token` — binding handle for immediate revocation.
- `constraints` — invariants, rate limits, and denial conditions.

## Pre-Grant Invariants

- R0 tick binding is established; R1 evaluation has occurred and is recorded.
- Privation supremacy is active; revocation path is verified before issuance.
- Scope is minimal, explicit, and non-ambiguous.
- No existing grant conflicts or accumulations for the same subject and scope.

## Post-Grant Invariants

- Grant is revocable at any time; revocation supersedes use.
- Grant does not imply other grants; no chaining or accumulation.
- Grant expires at ttl/tick_limit without renewal; no auto-extension.
- Audit entry exists for issuance with full provenance and constraints.

## Use Invariants

- Each use is bound to a tick and consumes budget; no reuse across ticks without
  explicit allowance inside scope and ttl.
- Any invariant breach triggers immediate revocation and halt.
- Use without a matching, valid grant is denied and audited.

## Revocation Semantics

- Revocation dominance: revocation overrides issuance, use, and continuation.
- Revocation is immediate, does not require consent, and is always permitted.
- Revocation events are audited with cause and timestamp.

## Failure Semantics

- Ambiguity in scope, ttl, or issuer → NO GRANT.
- Loss of audit or revocation channel → halt and deny.
- Any inability to prove adherence to constraints → revoke and halt.

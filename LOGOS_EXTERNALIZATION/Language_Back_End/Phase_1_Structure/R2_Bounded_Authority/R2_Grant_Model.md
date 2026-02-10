# R2 — Grant Model (Scoped, Time/Tick-Bounded, Revocable)

**Phase:** R2 (Design-Only)
**Authority Granted:** NONE
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Grant Structure

Each grant is an explicit object with the following minimum fields:

- `grant_id` — unique, non-reusable identifier.
- `subject` — identity bound to the grant (cannot be wildcards).
- `grant_class` — read | propose | plan | execute | persist (non-overlapping).
- `scope` — explicit resource/operation bounds; references immutable policy versions.
- `ttl` / `tick_limit` — expiration; cannot be extended in-place.
- `issuer` — validated governance identity; issuance without validation is denied.
- `constraints` — invariants, rate limits, denial conditions, and observability rules.
- `revocation_token` — binding handle enabling immediate revocation.
- `audit_ref` — issuance audit entry reference for provenance.

## Bounding Rules

- Scopes MUST be minimal and explicit; no wildcard or transitive coverage.
- TTL and tick limits are mandatory and non-extendable; renewal requires a new grant.
- Grants are non-transferable and non-delegable.
- Grants cannot be combined to widen scope (no accumulation).

## Usage Rules

- Each use is bound to a tick and logged; unlogged use is invalid.
- If scope, ttl, or revocation proofs cannot be confirmed, deny and halt.
- Any conflict with privation or revocation semantics voids the grant immediately.

## Revocation Hooks

- Revocation token must be resolvable before any use.
- Revocation may be triggered by governance, invariants breach, budget exhaustion,
  or revocation supremacy conditions (see Revocation Supremacy).

## Failure Handling

- Ambiguity in any field → deny and halt.
- Audit or revocation channel unavailability → deny and halt.

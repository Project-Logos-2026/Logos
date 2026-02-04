# R2 — Audit Specification

**Phase:** R2 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Audit Channel:** Governed spine only

---

## Required Fields (Grant Lifecycle)

**Issuance Entry**
- `grant_id`
- `subject`
- `grant_class`
- `scope_ref` (immutable policy reference)
- `ttl` / `tick_limit`
- `issuer`
- `constraints` (summarized)
- `revocation_token`
- `eligibility_ref` (links to R1 evaluation entry)
- `termination_reason` (for issuance path; should be `issued` or denial reason)

**Use Entry (Per Tick)**
- `grant_id`
- `tick_ref`
- `scope_check_status`
- `revocation_status` (pre- and post-use)
- `budget_consumed`
- `side_effect_check` (must confirm no unauthorized IO/persistence)
- `termination_reason` — `use_completed`, `revoked`, `expired`, `denied`, `invariant_breach`, `audit_channel_failure`

**Revocation Entry**
- `grant_id`
- `trigger` (see Revocation Supremacy)
- `timestamp`
- `issuer` (if applicable)
- `termination_reason` (e.g., `revoked`, `expired`, `superseded`)

## Termination Recording (Mandatory)

- Every lifecycle event must include `termination_reason`.
- Missing or ambiguous termination reasoning is a failure.
- Audit channel failures force halt; no deferred logging.

## Enforcement Notes

- No batch logging; each event is discrete and attributable.
- No persistence outside the governed spine.
- No aggregation that hides revocation or denial details.

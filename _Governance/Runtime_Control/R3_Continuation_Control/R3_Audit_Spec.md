# R3 — Audit Specification

**Phase:** R3 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Audit Channel:** Governed spine only

---

## Required Fields (Per Tick)

- `continuation_id` — unique identifier for the continuation envelope.
- `tick_ref` — bound tick identity and envelope hash (from R0).
- `grants_in_use` — list of R2 grants referenced (if any) with revocation status.
- `budget_status` — remaining tick/time/action budgets.
- `supervision_signal` — confirmation that supervision was active this tick.
- `side_effect_check` — confirmation of no unauthorized IO/persistence.
- `termination_reason` — `tick_completed`, `revoked`, `budget_exhausted`, `invariant_breach`, `audit_channel_failure`, `supervision_loss`.

## Required Fields (Continuation Summary)

- `continuation_id`
- `ticks_executed` and `ticks_budgeted`
- `final_budget_status`
- `revocation_events` (if any)
- `termination_reason` — `completed`, `revoked`, `budget_exhausted`, `denied`, `audit_channel_failure`, `supervision_loss`
- `audit_refs` — list of per-tick audit entry references

## Termination Recording (Mandatory)

- Every tick and the final summary must carry a `termination_reason`.
- Missing or ambiguous termination reasoning is a failure.
- Audit channel failure triggers immediate halt; no deferred logging.

## Enforcement Notes

- No batching that obscures per-tick visibility.
- No persistence outside the governed spine.
- No background continuation outside the audited ticks.

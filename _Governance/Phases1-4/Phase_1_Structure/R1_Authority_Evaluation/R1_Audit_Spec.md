# R1 — Audit Specification

**Phase:** R1 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Audit Channel:** Governed spine only

---

## Required Fields (Per Evaluation Entry)

- `evaluation_id` — unique, monotonic, bound to a single tick.
- `tick_ref` — reference to R0 tick identity and envelope hash.
- `signals_considered` — enumerated list with provenance and timestamps.
- `preconditions_status` — pass/fail with validated items.
- `eligibility_outcome` — `eligible_for_granting` or `not_eligible`.
- `denial_reasons` — list; non-empty when `not_eligible`.
- `side_effect_check` — confirmation that no IO/persistence occurred.
- `termination_reason` — enumerated:
  - `completed_without_grant`
  - `precondition_failure`
  - `signal_ambiguity`
  - `invariant_breach`
  - `audit_channel_failure`
- `budget_consumed` — evaluation budget units used.
- `operator_signature` or governance marker when applicable.

## Termination Recording (Mandatory)

- Every evaluation ends with a `termination_reason`.
- Missing or ambiguous termination reasoning is a failure.
- If the audit channel is unavailable, halt and write to the governed spine only;
  no retries and no deferred logging.

## Enforcement Notes

- Evaluations cannot be batched; one entry per evaluation per tick.
- No aggregation that removes provenance or denial details.
- No persistence outside the governed spine.

# R0 — Audit Specification

**Phase:** R0 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Audit Channel:** Governed spine only

---

## Required Fields (Per Tick Entry)

- `tick_id` — unique, monotonic, non-reusable identifier.
- `envelope_ref` — reference or hash of the immutable tick envelope.
- `timestamp_start` / `timestamp_end` — bounded window for the tick.
- `preconditions_status` — pass/fail with list of validated items.
- `disqualifiers_triggered` — list (empty allowed); any entry implies denial.
- `budget_baseline` and `budget_consumed` — fixed units, no extension.
- `postconditions_status` — pass/fail for invariants and side-effect checks.
- `termination_reason` — enumerated:
  - `clean_halt`
  - `precondition_failure`
  - `disqualifier_detected`
  - `invariant_breach`
  - `audit_channel_failure`
  - `ambiguous_state`
- `operator_signature` or governance marker when applicable.

## Termination Recording (Mandatory)

- Every tick MUST end with a recorded `termination_reason`.
- Missing or ambiguous termination reasoning is itself a failure.
- If the audit channel is unavailable, the system halts and records locally in the
  governed spine; external retransmission is forbidden.

## Additional Enforcement Notes

- No persistence outside the governed spine is permitted.
- No batching that obscures per-tick visibility; entries remain one-to-one with ticks.
- No aggregation that removes termination reasoning or budgets.

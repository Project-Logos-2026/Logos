# R1 — Authority Evaluation (Evaluate Only, Still Deny)

**Phase:** R1 (Design-Only)
**Authority Granted:** NONE
**External IO:** NONE
**Persistence:** NONE (beyond governed audit spine)
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Purpose & Scope

Evaluate authority conditions **without granting or holding authority**. R1 permits
observation and evaluation of governance signals but does not enable execution,
autonomy, or persistence.

- Evaluations are per-tick and non-accumulating.
- Outputs are eligibility assessments only; no implicit grants.
- All actions remain internal-only and auditable.

## Non-Goals

- No authority issuance, delegation, or inference.
- No external IO or persistence beyond the audit spine.
- No stateful carryover of evaluation results between ticks.
- No scheduling, planning, or continuation enablement.
- No background loops or self-directed activity.

## Preconditions

- R0 eligibility documents and audit specification are present and active.
- Privation and revocation semantics remain dominant and verifiable.
- Audit channel is reachable for evaluation records.
- Tick budget and evaluation budget are defined and non-extendable.

## Disqualifiers

Any of the following forces denial and halt:

- Missing R0 audit channel or inability to bind evaluation to a tick.
- Attempt to persist evaluation outputs outside the governed spine.
- Detection of authority inference, escalation, or delegation attempts.
- Ambiguity in evaluation signals or provenance.
- Loss of halt path or observability.

## Halt Semantics (Fail-Closed)

- Ambiguity, drift, or signal loss → immediate halt and denial.
- No retries and no deferred evaluations across ticks.
- Termination reason must be recorded; absence of a reason is a failure.

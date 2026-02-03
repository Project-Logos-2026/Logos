# R1 — Semantic Contract

**Phase:** R1 (Design-Only)
**Authority Granted:** NONE
**Execution Enabled:** NO
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Formal Definitions

- **Authority Evaluation:** A bounded, per-tick assessment of whether conditions for
authority could be satisfied. Outputs are assessments only; no grants are produced.
- **Evaluation Envelope:** The governed set of inputs (signals, provenance, policies)
  required for an evaluation. Immutable during the evaluation.
- **Observable-Only Signals:** Signals that can be read without implying authority or
  causing side effects (see Evaluation Signals).

## Pre-Evaluation Invariants

- Evaluation is bound to a specific R0 tick identity.
- Envelope is immutable and provenance-verified.
- No prior or pending authority claims exist for this tick.
- Audit channel is ready to capture evaluation inputs and outcomes.
- Budgets (tick and evaluation) are defined and non-extendable.

## Post-Evaluation Invariants

- No authority is granted, inferred, or cached.
- No external side effects (IO, persistence, scheduling) occurred.
- Audit entry exists with signals considered and the denial/eligibility outcome.
- Budgets consumed are recorded; no surplus is auto-carried.

## Evaluation Flow (Conceptual)

1. **Bind to Tick:** Acquire immutable tick identity and envelope from R0.
2. **Pre-Check:** Validate pre-evaluation invariants; deny on ambiguity.
3. **Evaluate:** Inspect observable-only signals; produce an eligibility assessment
   (`eligible_for_granting` / `not_eligible`). No action or grant follows.
4. **Post-Check:** Verify no side effects or state drift.
5. **Audit:** Emit evaluation audit entry with inputs, outcomes, and termination reason.
6. **Halt:** Deterministic halt; no continuation and no reuse of evaluation outputs.

Any ambiguity or partial evaluation results in denial and halt.

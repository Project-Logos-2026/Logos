# R-Series TODO (R0–R3)

**Status:** Documentation for R0–R3 completed. No runtime implementation performed.
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED. Authority/Autonomy remain disabled.

---

## Completed

- R0 Eligibility — README, Semantic Contract, Audit Spec
- R1 Authority Evaluation — README, Semantic Contract, Evaluation Signals, Audit Spec
- R2 Bounded Authority — README, Semantic Contract, Grant Model, Revocation Supremacy, Audit Spec
- R3 Continuation Control — README, Semantic Contract, Continuation Bounds, Supervision and Observability, Audit Spec

## Deferred / Requires Explicit Authorization

- Minimal tick runner scaffold (R0 flow: pre-check → tick → post-check → audit → halt)
- Any live authority evaluation or grant logic
- Any continuation control runtime behavior
- R-series exit markers and freeze artifacts

## Next Checks After R3 Closure (Mandatory)

- Run full governance lattice audit and drift scan covering R0–R3.
- Confirm no external IO, scheduling, persistence, or autonomy enabled outside R-series bounds.
- Confirm audit logging captures tick lifecycle end-to-end.
- Only after a PASS and explicit authorization may Step-5 autonomous agent loops be evaluated.

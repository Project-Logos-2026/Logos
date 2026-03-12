# R0 — Eligibility (Tick Existence Without Authority)

**Phase:** R0 (Design-Only)
**Authority Granted:** NONE
**External IO:** NONE
**Persistence:** NONE (beyond governed audit spine)
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Purpose & Scope

Establish a governed tick concept that can exist **without granting authority** and
without enabling autonomy. Eligibility defines whether a tick may be admitted into
the governed spine under strict denial semantics.

- Tick existence does **not** imply autonomy, scheduling, or execution authority.
- Eligibility is evaluated per tick; no carryover or accumulation.
- Observation and audit are permitted; external IO, persistence, and authority are not.

## Non-Goals

- No authority grants, escalation, or inference.
- No external IO (network, filesystem beyond governed audit spine, IPC).
- No persistence beyond the governed audit spine.
- No planning, scheduling, or continuation enablement.
- No background loops or self-directed activity.

## Preconditions

- Privation and revocation semantics are active and non-bypassable.
- A deterministic halt path is available for any failure.
- An audit sink on the governed spine is reachable for tick records.
- Tick budget for the run is defined (non-zero, non-extendable).

## Disqualifiers

Any of the following forces immediate denial and halt:

- Missing or unreachable audit sink.
- Undefined or zero tick budget.
- Detection of external IO intent or persistence intent beyond the audit spine.
- Ambiguity in tick identity or envelope.
- Loss of halt path or observability.

## Halt Semantics (Fail-Closed)

- On any precondition failure or disqualifier, **halt immediately** and record the
  denial reason.
- No continuation, no retries, no degradation path.
- Halting is deterministic and consumes the remaining budget.
- Absence of a recorded termination reason is itself a failure.

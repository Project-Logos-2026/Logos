# Planning Substrate — Semantic Contract

**Domain:** Protocol-Wide Planning Substrate  
**Phase:** A₂ (Design-Only)  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose

This document defines the **semantic substrate for planning** shared across
the LOGOS system protocols.

It governs what plans are, how they are validated, how they fail,
and how they terminate—without performing planning, reasoning, or execution.

---

## 2. Definition of a Plan

A **plan** is a governed, declarative structure representing
a proposed course of action across one or more ticks.

A plan is:
- not an intention,
- not an execution,
- not a commitment.

A plan has no authority until admitted by governance.

---

## 3. Plan States

A plan may exist in one of the following states:

- **Proposed** — generated but not yet validated
- **Valid** — permitted under all constraints
- **Invalid** — violates constraints or privation
- **Failed** — could not satisfy required conditions
- **Revoked** — explicitly withdrawn or invalidated
- **Terminated** — concluded or expired

Plans may not transition arbitrarily between states.

---

## 4. Plan State Transitions

All plan transitions are governed.

Examples:
- Proposed → Valid (after validation)
- Proposed → Invalid (constraint violation)
- Valid → Revoked (privation or governance change)
- Valid → Failed (unsatisfied conditions)
- Any → Terminated (end-of-life)

No protocol may force a transition outside these rules.

---

## 5. Privation Supremacy

Privation semantics override all plan semantics.

If a plan conflicts with privation:
- it is immediately **Invalid** or **Revoked**,
- no continuation is permitted,
- no recovery path exists unless governance lifts privation.

Privation cannot be reasoned around or deferred.

---

## 6. Multi-Tick Continuation Rules

Plans spanning multiple ticks must satisfy:

- continuous validity at each tick,
- preserved validation context,
- no intervening privation,
- no loss of constraint visibility.

Loss of any requirement resolves to DENY or HALT.

---

## 7. Protocol Interactions (Canonical)

- **Advanced Reasoning Protocol (ARP)**  
  Generates and evaluates candidate plans.

- **Meaning Translation Protocol (MTP)**  
  Interprets plans into mediated representations.

- **Synthetic Cognition Protocol (SCP)**  
  Enforces coherence and global constraints.

- **Cognitive State Protocol (CSP)**  
  Enforces capability and context safety.

- **Systems Operations Protocol (SOP)**  
  Acts as the operational admission boundary.

No protocol may bypass the planning substrate.

---

## 8. Failure & Ambiguity Semantics

- Ambiguity → DENY
- Conflicting constraints → strongest constraint
- Loss of validation context → HALT or DENY
- Partial observability → DENY

There is no degraded planning mode.

---

## 9. Non-Bypass Guarantee

If any protocol or agent can:
- self-validate a plan,
- continue a revoked plan,
- reinterpret plan validity contextually,

then this design has failed.

---

## 10. Phase Completion Statement

Phase A₂ is complete when:
- this document exists,
- it is treated as authoritative,
- no enforcement is implied,
- autonomy remains blocked.

---

**END OF PLANNING SUBSTRATE SEMANTICS — PHASE A₂**

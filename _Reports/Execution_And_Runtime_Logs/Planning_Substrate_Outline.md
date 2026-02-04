# Planning Substrate — Phase A₂ (Outline)

**Domain:** Protocol-Wide Planning Substrate  
**Status:** DESIGN-ONLY  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose

Define the **semantic substrate for planning** shared across protocols.

This substrate governs what plans are, how they are validated,
how they fail, and how they terminate—without performing planning itself.

---

## 2. Scope (What This Phase Covers)

- Semantic definition of a plan
- Plan states and state transitions
- Validation and invalidation semantics
- Privation constraints on plans
- Failure, revocation, and termination rules
- Multi-tick continuation boundaries

---

## 3. Explicit Non-Goals

This phase does NOT:

- implement planners or reasoning
- define execution or scheduling
- authorize autonomy
- introduce runtime logic
- grant any protocol authority over plan validity

---

## 4. Canonical Protocol Roles

- **Advanced Reasoning Protocol (ARP)** — plan generation and evaluation
- **Meaning Translation Protocol (MTP)** — plan interpretation and mediation
- **Synthetic Cognition Protocol (SCP)** — coherence and constraint enforcement
- **Cognitive State Protocol (CSP)** — capability and context safety
- **Systems Operations Protocol (SOP)** — operational admission boundary

No protocol may bypass the planning substrate.

---

## 5. Core Concepts to Be Defined

- Plan vs intention vs execution
- Valid, invalid, failed, and revoked plans
- Plan lifecycle and termination
- Continuation eligibility across ticks
- Privation-driven plan invalidation

---

## 6. Failure & Ambiguity Semantics

- Ambiguity → DENY
- Conflicting constraints → strongest constraint
- Loss of validation context → HALT or DENY

---

## 7. Completion Criteria

Phase A₂ is complete when:
- a full planning substrate semantics document exists,
- scope is locked,
- no enforcement is implied,
- autonomy remains blocked.

---

**END OF PHASE A₂ OUTLINE**

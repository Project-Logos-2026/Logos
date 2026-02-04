# Privation & Negative Knowledge Semantics — Phase P₁ (Outline)

**Domain:** I₂ — Privation / Negative Knowledge  
**Status:** DESIGN-ONLY  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose

Define how the system represents and reasons about **negative knowledge**, including:

- what must not exist,
- what must not be done,
- what is no longer permitted,
- what has been revoked or invalidated.

This phase defines **semantics only**, not enforcement.

---

## 2. Scope (What This Phase Covers)

- Conceptual definition of privation
- Categories of negative knowledge
- Propagation rules across planning and memory
- Precedence over planning and continuation
- Ambiguity → DENY semantics

---

## 3. Explicit Non-Goals

This phase does NOT:

- define enforcement hooks
- implement runtime logic
- modify agents or planners
- authorize autonomy
- permit bypass via reasoning

---

## 4. Core Concepts to Be Defined

- Privation vs absence
- Revocation vs denial
- Permanent vs contextual negation
- Temporal negation (“no longer allowed”)
- Irreversible prohibitions

---

## 5. Privation Categories (To Be Specified)

- Ontic privation (must not exist)
- Epistemic privation (must not be known or inferred)
- Action privation (must not be done)
- Continuation privation (must not continue)
- Memory privation (must not persist or rehydrate)

---

## 6. Interaction With Other Domains

- Planning (privation overrides plans)
- Memory (privation survives rehydration)
- Orchestration (privation escalates to DENY/HALT)
- Governance (only governance may lift privation)

---

## 7. Failure & Ambiguity Semantics

- Ambiguity resolves to DENY
- Conflicting privations resolve to strongest constraint
- Loss of privation visibility triggers HALT

---

## 8. Completion Criteria

Phase P₁ is complete when:
- a full privation semantics document exists,
- scope is locked,
- no enforcement is implied,
- autonomy remains blocked.

---

**END OF PHASE P₁ OUTLINE**

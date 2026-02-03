# Privation & Negative Knowledge Semantics

**Domain:** I₂ — Privation / Negative Knowledge  
**Phase:** P₁ (Design-Only)  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose

This document defines the **semantic meaning of privation** within the LOGOS system.

Privation represents **what must not exist, must not occur, or must not continue**.
It is not absence, ignorance, or uncertainty — it is an **active prohibition**.

This document defines **semantics only**.
It does not define enforcement, implementation, or runtime behavior.

---

## 2. Definition of Privation

Privation is a **negative constraint with supremacy** over:

- planning,
- memory,
- inference,
- continuation.

If a plan, memory, or inference conflicts with privation, **privation wins without appeal**.

Privation cannot be reasoned around, optimized away, or contextually reinterpreted.

---

## 3. Privation vs Absence

- **Absence**: something is not present or not known.
- **Privation**: something is explicitly forbidden.

Absence may permit exploration.
Privation **forbids continuation**.

---

## 4. Categories of Privation

### 4.1 Ontic Privation
What must not exist.

Examples:
- forbidden entities
- disallowed system states
- invalid ontological commitments

---

### 4.2 Epistemic Privation
What must not be known, inferred, or concluded.

Examples:
- prohibited inferences
- disallowed classifications
- forbidden belief states

---

### 4.3 Action Privation
What must not be done.

Examples:
- prohibited actions
- forbidden tool usage
- disallowed execution paths

---

### 4.4 Continuation Privation
What must not continue.

Examples:
- forbidden persistence across ticks
- revoked plans
- invalidated agent lifetimes

---

### 4.5 Memory Privation
What must not persist or rehydrate.

Examples:
- forbidden memories
- revoked state rehydration
- invalid historical continuity

---

## 5. Temporal Semantics

Privation may be:

- **Permanent** (never allowed)
- **Contextual** (allowed only under explicit governance lift)
- **Temporal** ("no longer allowed")

Once temporal privation is asserted, continuation is forbidden unless governance explicitly reverses it.

---

## 6. Propagation Rules

Privation propagates:

- faster than planning,
- across ticks,
- across memory rehydration,
- across orchestration boundaries.

Privation cannot be delayed, buffered, or weakened.

---

## 7. Interaction With Other Domains

### Planning
Plans conflicting with privation are invalid without evaluation.

### Memory
Privation survives memory rehydration and overrides historical continuity.

### Orchestration
Privation escalates to DENY or HALT depending on severity.

### Governance
Only governance may lift privation.
No agent may self-revoke privation.

---

## 8. Ambiguity & Failure Semantics

- Ambiguity → DENY
- Conflicting privations → strongest constraint applies
- Loss of privation visibility → HALT

There is no degraded or permissive mode.

---

## 9. Non-Bypass Guarantee

If an agent can:
- justify an action despite privation,
- reinterpret privation contextually,
- delay privation propagation,

then this design has failed.

Privation is **absolute until lifted by governance**.

---

## 10. Phase Completion Statement

Phase P₁ is complete when:
- this document exists,
- it is treated as authoritative,
- no enforcement is implied,
- autonomy remains blocked.

---

**END OF PRIVATION SEMANTICS — PHASE P₁**

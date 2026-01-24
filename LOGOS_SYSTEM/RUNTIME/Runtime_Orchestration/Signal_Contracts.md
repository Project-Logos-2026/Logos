# Runtime Orchestration — Signal Contracts

**Status:** Authoritative, Design-Only  
**Layer:** Runtime_Orchestration  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose and Scope

This document defines the **signal contracts** used by Runtime_Orchestration.
It specifies what signals exist, how they propagate, their precedence, and their mandatory effects.

This document defines **no implementation**, **no wiring**, and **no executable behavior**.

Signals are **constraints and interrupts only**.
They never grant authority, approve execution, or reinterpret governance.

---

## 2. Global Invariants

1. **Deny-by-Default**  
   Absence of an explicit non-denial state does not imply permission.

2. **Fail-Closed**  
   Under uncertainty, ambiguity, partial visibility, or conflict, the system must deny or halt.

3. **Constraint-Only Semantics**  
   Signals may only constrain, interrupt, refuse, or escalate visibility.

4. **Propagation Supremacy**  
   Signal propagation is strictly faster than any execution or coordination flow.

5. **No Authority Creation**  
   No signal may allow, approve, prioritize, or justify continuation.

---

## 3. Signal Precedence Model

Signals are totally ordered. Higher-precedence signals preempt all lower-precedence signals.

**Precedence (Highest → Lowest):**

1. HALT  
2. DENY  
3. SUPERVISION_LOSS  
4. FAIL  
5. AUDIT  

Rules:
- Higher-precedence signals immediately interrupt lower-precedence handling.
- Lower-precedence signals may not delay, mask, or downgrade higher-precedence signals.
- Conflicting signals resolve to the highest-precedence signal present.

---

## 4. Signal Emission Rules

### 4.1 Authorized Emitters
- Runtime_Governance
- Runtime_Spine
- Supervision and observability mechanisms
- Audit infrastructure

### 4.2 Forbidden Emitters
Runtime_Orchestration must never emit signals that imply approval, authorization, goal promotion, or execution permission.
It may only relay, propagate, or escalate signals.

### 4.3 Provenance Requirement
All signals must have identifiable source, verifiable provenance, and traceable emission context.
Unverifiable signals are treated as DENY.

---

## 5. Signal Propagation Rules

- Signals propagate immediately upon detection.
- No buffering, batching, retries, or deferred handling.
- No "wait and see" semantics.
- If propagation cannot be guaranteed, coordination must be refused.

---

## 6. Signal Definitions

### 6.1 HALT
Immediate and unconditional cessation of all coordinated activity.
Overrides everything without exception.

### 6.2 DENY
Refusal to coordinate or continue an action.
Final unless governance explicitly changes state.

### 6.3 SUPERVISION_LOSS
Loss of required observability or supervision guarantees.
Escalates to DENY or HALT.

### 6.4 FAIL
Detected failure in prerequisites or downstream components.
Refuses continuation and escalates to governance paths.

### 6.5 AUDIT
Visibility or compliance review requirement.
Never delays or overrides HALT or DENY.

---

## 7. Ambiguity and Timing Semantics

Ambiguity, partial observability, conflicting signals, or timing anomalies mandate DENY or HALT.
There is no permissive or degraded mode.

---

## 8. Failure Semantics

Runtime_Orchestration must fail closed.
No retries that alter semantics.
No continuation under pressure.

---

## 9. Non-Authority Guarantees

Signals must never approve execution, create authority, interpret policy, or prioritize outcomes.

---

## 10. Design Completeness Statement

This signal contract definition is complete.
Any expansion requires explicit post-Phase-7 governance authorization.

---

**END OF SIGNAL CONTRACTS — PHASE O₁**

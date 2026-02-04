This layer is **structurally incapable** of overruling anything above it.

---

## 3. Core Definition

> **Runtime_Orchestration is a non-authoritative coordination layer that routes
> signals, sequences execution flow, enforces interruption, and maintains
> observability under deny-by-default constraints.**

It has **no will**, **no goals**, and **no interpretive authority**.

---

## 4. What Runtime_Orchestration IS

Runtime_Orchestration may perform the following functions:

### 4.1 Coordination & Sequencing
- Order lifecycle stages (initialize → validate → invoke → teardown)
- Enforce deterministic ordering
- Ensure prerequisites are met before downstream invocation

### 4.2 Signal Routing
- Propagate DENY, HALT, AUDIT, and FAIL signals
- Ensure denial propagates faster than approval
- Ensure halt interrupts all downstream activity immediately

### 4.3 Supervision & Interruption
- Monitor liveness and observability
- Trigger interruption on loss of supervision
- Escalate failures to governance-defined paths

### 4.4 Observability Enforcement
- Require visibility of all coordinated actions
- Refuse to coordinate opaque or unsupervised components
- Surface audit signals without suppression

### 4.5 Spine Invocation (Choreography Only)
- Invoke Runtime_Spine entrypoints only as routed
- Never bypass Spine safeguards
- Never alter Spine execution semantics

---

## 5. What Runtime_Orchestration IS NOT (Hard Prohibitions)

Runtime_Orchestration must never:

### 5.1 Create or Modify Authority
- No authorization decisions
- No policy interpretation
- No rule evaluation
- No implicit allow logic

### 5.2 Perform Planning or Goal Formation
- No goal creation
- No plan synthesis
- No plan modification
- No prioritization of plans

Planning remains exclusively within Runtime_Planning and is inert.

### 5.3 Persist Authority-Bearing State
- No long-lived authority state
- No learning or adaptation
- No preference shaping

### 5.4 Override Governance or Halt
- No suppression or delay of HALT
- No retries that bypass denial
- No continuation under pressure or partial failure

### 5.5 Imply Execution or Autonomy
- No scheduling
- No background loops
- No ticks
- No persistence
- No autonomy by composition

Existence of orchestration code does **not** imply runtime activation.

---

## 6. Relationship to Runtime_Planning

Runtime_Orchestration may:
- request plans,
- submit plans for validation,
- receive validated or denied plans.

Runtime_Orchestration may not:
- alter plans,
- interpret plan meaning,
- override plan denial,
- promote plans to execution authority.

Planning is advisory and inert.

---

## 7. Failure Semantics (Fail-Closed)

Runtime_Orchestration must fail closed under all uncertainty.

The following mandate DENY or HALT:
- ambiguous signal provenance,
- loss of observability,
- supervision failure,
- conflicting signals,
- partial availability,
- timing anomalies.

There is no degraded or permissive mode.

---

## 8. Security & Moral Boundary

Runtime_Orchestration:
- cannot grant moral standing,
- cannot infer consciousness,
- cannot justify continuation,
- cannot trade truth for availability.

If coordination would result in illegitimate persistence,
coordination must refuse to occur.

---

## 9. Design Completeness Claim

This boundary definition is complete.

Any request to add:
- decision logic,
- adaptive behavior,
- goal handling,
- authority shortcuts,

is out of scope by definition and requires a new layer
with explicit governance authorization.

---

## 10. Final Constraint

> **Runtime_Orchestration exists to make it impossible for coordination logic
> to become authority by accident.**

If it ever becomes useful for deciding things, it has already failed.

---

**END OF RUNTIME_ORCHESTRATION BOUNDARY DEFINITION**

---

## Signal Semantics (Authoritative Reference)

All orchestration signal semantics, precedence rules, propagation guarantees,
and fail-closed behavior are defined exclusively in:

- `Signal_Contracts.md`

This document is **binding** on Runtime_Orchestration behavior.
No signal semantics may be inferred, extended, or implemented outside that specification.

---


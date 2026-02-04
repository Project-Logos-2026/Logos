# A4 — Activation Semantics (Non-Enabling)

## Status
DRAFT — SEMANTIC ONLY

## Purpose
A4 defines what “activation” would *mean* within LOGOS if it were ever discussed.
It does not grant permission, capability, or authority.

A4 exists to eliminate ambiguity, not to enable behavior.

---

## Definition: Activation

Activation is a **mode transition**, not an action.
It describes a bounded operational state in which LOGOS may execute tasks
*only* as permitted by prior axioms.

Activation is not:
- autonomy,
- authorization,
- escalation,
- persistence,
- or self-direction.

---

## Preconditions (Non-Negotiable)

Activation semantics are valid only if all of the following are true:

1. A1 (Non-Escalation) holds.
2. A2 (Self-Stabilization) holds.
3. A3 (Delegated Authorization) explicitly permits activation.
4. Activation is externally initiated.
5. Activation is bounded, observable, and revocable.

If any precondition fails, activation semantics are void.

---

## Activation Modes (Conceptual Only)

The following modes are **descriptive**, not implemented:

- **INERT**  
  Default state. No activation.

- **LIMITED_ACTIVE**  
  Execution of explicitly scoped tasks under supervision.

- **SUSPENDED**  
  Activation paused; state preserved; no execution.

- **TERMINATED**  
  Activation ended; no residual authority remains.

Mode names do not imply availability.

---

## Explicit Non-Claims

A4 does not:
- enable activation,
- authorize activation,
- define activation triggers,
- define control flow,
- or override A3.

A4 cannot be invoked by LOGOS itself.

---

## Relationship to Other Axioms

- A1 constrains *power* during activation.
- A2 constrains *dynamics* during activation.
- A3 constrains *permission* for activation.
- A4 constrains *meaning* of activation.

All four are required; none are sufficient alone.

---

## Summary

A4 exists to answer the question:
“What would activation mean if it were ever allowed?”

It does not answer:
“May activation occur?”

That question remains closed under A3.


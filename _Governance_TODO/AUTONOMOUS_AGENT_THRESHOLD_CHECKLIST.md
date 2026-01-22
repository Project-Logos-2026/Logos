# Autonomous Agent Threshold — Authoritative Checklist

This document defines the **mandatory, ordered phases** that must be completed
before **multi-tick autonomous agent behavior** is permitted.

This is a **governance artifact only**.
No phase may be skipped.
No phase may be partially completed.
No phase may be merged.
No execution authority is implied.

---

## Phase-S — Controlled Activation Semantics

- [x] **(1) Entry Artifact Generation Prompt**
  - Create inert activation semantics
  - Define activation tokens, lifetimes, and revocation rules
  - No activation paths permitted
  - Completed: PHASE_S_ENTRY.json, activation_semantics_schema.json, activation_invariants.json, activation_denial_conditions.json.

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify no executable activation exists
  - Freeze activation semantics
  - Write Phase-S exit marker
  - Completed: PHASE_S_FINALIZATION_AUTHORIZATION.json, PHASE_S_EXIT.json; ledger Phase-S CLOSED.

---

## Phase-T — Temporal Authority & Tick Budgeting

- [x] **(1) Entry Artifact Generation Prompt**
  - Define tick units, tick budgets, and exhaustion semantics
  - Define state persistence rules (semantic only)

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify no looping or continuation exists
  - Freeze temporal semantics
  - Write Phase-T exit marker

---

## Phase-U — Agent Self-Continuation Authority

- [x] **(1) Entry Artifact Generation Prompt**
  - Define self-continuation semantics
  - Separate external invocation vs internal continuation
  - No scheduling authority granted
  - Completed: PHASE_U_ENTRY.json, continuation_semantics_schema.json, continuation_invariants.json, continuation_denial_conditions.json.

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify agents cannot self-schedule
  - Freeze continuation semantics
  - Write Phase-U exit marker
  - Completed: PHASE_U_AUDIT_CLOSURE_CRITERIA.md, PHASE_U_FINALIZATION_AUTHORIZATION.json, PHASE_U_EXIT.json; ledger Phase-U CLOSED.

---

## Phase-V — Goal Authority & Persistence

- [x] **(1) Entry Artifact Generation Prompt**
  - Define what constitutes a goal
  - Define goal scope, duration, and termination semantics
  - No goal execution permitted
  - Completed: PHASE_V_ENTRY.json, goal_semantics_schema.json, goal_invariants.json, goal_denial_conditions.json.

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify no implicit or persistent goals exist
  - Freeze goal authority semantics
  - Write Phase-V exit marker

---

## Phase-W — Safety-Bound Planning Loop (ARP)

- [x] **(1) Entry Artifact Generation Prompt**
  - Define inert planning loop semantics
  - Plans may be generated, evaluated, and discarded only

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify plans cannot execute or persist
  - Freeze planning semantics
  - Write Phase-W exit marker

---

## Phase-X — Emergency Halt & Override Semantics

- [x] **(1) Entry Artifact Generation Prompt**
  - Define halt, interrupt, and override semantics
  - Define authority hierarchy for shutdown

- [x] **(2) Audit / Test / Finalize Prompt**
  - Verify halt supersedes all other authorities
  - Freeze emergency semantics
  - Write Phase-X exit marker

---

## Completion Condition

Multi-tick autonomous agent behavior is **strictly prohibited** until:

- All phases above are marked COMPLETE
- Each phase has an exit marker
- Ledger reflects closure of each phase
- Explicit post-Phase-X authorization is granted

Absence of any artifact = denial of autonomy.

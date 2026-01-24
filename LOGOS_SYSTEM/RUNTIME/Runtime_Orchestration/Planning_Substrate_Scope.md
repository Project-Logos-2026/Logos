# Planning Substrate — Scope & Ownership Clarification

**Status:** DESIGN-ONLY  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## Purpose

This document clarifies the **scope and ownership** of the planning substrate
prior to Phase A₂ design.

It exists to prevent architectural drift, implicit authority capture,
and protocol-level ambiguity.

---

## Core Determination

The planning substrate is **protocol-wide**, not owned by any single protocol.

The **Advanced Reasoning Protocol (ARP)** is a *planner and consumer* of plans.
It is **not** the owner of planning semantics.

---

## Planning Substrate Responsibilities

The planning substrate defines, at a semantic level:

- what constitutes a plan,
- valid plan states and state transitions,
- plan validation and invalidation semantics,
- privation constraints on plans,
- failure and revocation propagation,
- multi-tick continuation boundaries.

The substrate itself performs **no reasoning, planning, or optimization**.

---

## Protocol Interfaces (Canonical)

The planning substrate is consumed by the following canonical protocols:

- **Advanced Reasoning Protocol (ARP)**  
  Plan generation, simulation, and evaluation.

- **Meaning Translation Protocol (MTP)**  
  Interpretation and mediation of plans across representational domains.

- **Synthetic Cognition Protocol (SCP)**  
  Global coherence, constraint enforcement, and optimization validation.

- **Cognitive State Protocol (CSP)**  
  Capability, context, and cognitive-state safety enforcement.

The **Systems Operations Protocol (SOP)** provides the operational boundary
within which planning artifacts may be admitted or rejected at runtime.

No protocol may bypass the planning substrate.

---

## Authority Constraints

- No protocol may self-validate plans.
- No planner may redefine plan validity.
- All plan continuation is subject to substrate constraints.
- Privation semantics override all planning semantics.

---

## Phase Implication

Phase A₂ will define the planning substrate as a
**governed, shared semantic layer** across protocols.

ARP-facing interfaces are a **subset**, not the definition, of the substrate.

---

**END OF PLANNING SUBSTRATE SCOPE CLARIFICATION**

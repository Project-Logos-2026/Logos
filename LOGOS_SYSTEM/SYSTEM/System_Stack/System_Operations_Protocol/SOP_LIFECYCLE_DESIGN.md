# SOP Lifecycle — Formal Design Specification

Status: DESIGN_ONLY  
Authority: NONE  
Execution: FORBIDDEN  

---

## 1. Purpose

This document formally defines the **System Operations Protocol (SOP) lifecycle**
as a **design-only state machine**.

It introduces:
- no execution,
- no logic,
- no wiring,
- no authority.

Its sole purpose is to define the *intended lifecycle semantics* for SOP so that
future implementations are constrained, auditable, and non-speculative.

---

## 2. Canonical Lifecycle States

SOP SHALL operate in exactly one of the following states at any time:

### INIT
- SOP structures are instantiated.
- No coordination or optimization is active.
- No external interaction is permitted.

### ACTIVE_LIMITED
- SOP may coordinate already-authorized subsystems.
- No self-expansion, scheduling, or autonomy is permitted.
- All actions remain Phase-gated and fail-closed.

### HALT
- SOP coordination is suspended.
- State entered on fatal governance violation or explicit shutdown.
- No transitions permitted except to INERT.

### INERT
- SOP is fully inactive.
- No coordination, no memory interaction, no execution.
- Terminal state unless explicitly re-instantiated.

---

## 3. Allowed State Transitions

The following transitions are permitted by design:

- INIT → ACTIVE_LIMITED  
- ACTIVE_LIMITED → HALT  
- HALT → INERT  

The following transitions are **explicitly forbidden**:

- INIT → HALT (without instantiation)
- ACTIVE_LIMITED → INIT
- INERT → any state
- Any implicit or time-based transition

All transitions MUST be explicit and authorized in future phases.

---

## 4. Invariants

The following invariants apply in all states:

- SOP does not generate goals.
- SOP does not authorize execution.
- SOP does not escalate privileges.
- SOP does not self-modify.
- SOP remains subordinate to Phase-X governance.

Violation of any invariant SHALL force transition to HALT.

---

## 5. Lifecycle Boundary

The canonical implementation boundary for this lifecycle, when authorized,
SHALL be located at:

SYSTEM/System_Stack/System_Operations_Protocol/infrastructure/agent_system/

No lifecycle logic is permitted elsewhere.

---

## 6. Telemetry (Design Note)

Telemetry MAY observe lifecycle state transitions via design-approved adapters.

Telemetry:
- is read-only,
- has no causal power,
- cannot trigger transitions.

No telemetry wiring is permitted prior to explicit authorization.

---

## 7. Governance

This document is declarative only.

It does not:
- permit implementation,
- authorize wiring,
- or modify execution posture.

All future SOP lifecycle code MUST conform to this specification.

# SOP_BLUEPRINT_DRAFT.md

## Status
DRAFT — DESIGN-ONLY — NON-EXECUTABLE

## Purpose
This document provides a **rough baseline blueprint** for rebuilding the **System Operations Protocol (SOP)** under the normalized LOGOS V1 architecture.
It is intended to:
- Establish scope and boundaries
- Define internal structure
- Enumerate required responsibilities
- Serve as a working reference during implementation

This blueprint does **not** authorize execution, mutation, or runtime behavior.

---

## SOP High-Level Role

SOP is the **operations-side authority** of the LOGOS runtime.

It is responsible for:
- System integrity and operational governance
- Proof-gated operations control
- Persistence authorization and enforcement
- Diagnostics, monitoring, and attestation
- Acting as the sole operations interface to DRAC, EMP, and CSP persistence

SOP does **not**:
- Execute goals
- Plan behavior
- Interpret meaning
- Interact with users
- Bypass the Runtime Bridge
- Mutate runtime logic

---

## Runtime Position

- SOP lives on the **Operations Side** of the runtime bifurcation.
- SOP interfaces with the **Logos Protocol only** via the Runtime Bridge.
- SOP is activated through STARTUP after PXL Gate validation.
- SOP operates under strict deny-by-default semantics.

---

## Canonical Directory Structure

```
System_Operations_Protocol/
├── Core/
├── Nexus/
├── Tools/
└── Documentation/
```

---

## SOP/Core (Authoritative Operations Kernel)

### Responsibilities
- Operations authority and policy enforcement
- Proof-gated validation for ops requests
- Persistence control and integrity enforcement
- Provenance and attestation
- Runtime health and readiness reporting

### Core Components (Conceptual)

- Ops_Kernel
- Capability_Registry
- Policy_Engine
- Proof_Gate_Client
- Runtime_Bridge_Client
- Persistence_Controller
- Integrity_Attestation
- Ops_Event_Bus

All Core modules:
- Are deny-by-default
- Require explicit capability admission
- Cannot perform goal execution
- Cannot call agents directly

---

## SOP/Nexus (Wiring and Lifecycle)

### Responsibilities
- Deterministic SOP boot sequence
- Registration of SOP Core services
- Controlled exposure to runtime spine
- Health and readiness signaling

### Nexus Components (Conceptual)

- SOP_Nexus_Orchestrator
- Service_Registry
- Health_State_Manager

Nexus:
- Contains no authority logic
- Does not make policy decisions
- Only wires approved Core components

---

## SOP/Tools (Non-Authoritative Utilities)

### Responsibilities
- Supporting utilities for SOP/Core
- No independent authority
- No persistence decisions

### Tool Categories
- Hashing and signing utilities
- Audit log writers (append-only)
- Serialization and schema enforcement
- Telemetry emitters

Tools must:
- Be stateless where possible
- Be callable only by SOP/Core
- Never bypass policy enforcement

---

## SOP/Documentation (Binding, Non-Executable)

Required files:
- MANIFEST.md
- ORDER_OF_OPERATIONS.md
- STACK_POSITION.md
- RUNTIME_ROLE.md
- GOVERNANCE_SCOPE.md
- METADATA.json

Documentation:
- Is binding for audits and refactors
- Is never imported by runtime code
- Explicitly states prohibitions

---

## Interfaces to Other Protocols

### DRAC
- SOP authorizes compilation phases
- SOP governs artifact cataloging
- SOP enforces persistence scope

### EMP
- SOP governs attestation workflows
- SOP stores verification outputs
- SOP enforces proof result immutability

### CSP
- SOP controls persistence eligibility
- SOP manages holding-cell snapshots
- SOP enforces resume integrity

---

## Critical Invariants

- Fail-closed, deny-by-default
- No remediation via Runtime Bridge
- Proof-gated operations only
- No runtime code generation
- No external service spawning
- No direct filesystem writes outside approved scopes

---

## Open Design Questions

(To be resolved before implementation)
- Exact EMP attestation data model
- CSP snapshot lifecycle details
- DRAC artifact retention policies
- Telemetry emission boundaries

---
Map once all 3 protocols are final
mapping ARP ↔ SOP ↔ EMP interfaces precisely.


END DRAFT

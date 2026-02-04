# Runtime Import & Authority Graph (LOGOS)

This document defines the **runtime authority structure, dependency flow, and observability boundaries** of the LOGOS System.

It is authoritative for understanding:
- who controls execution
- how meaning flows
- how observability is isolated
- how audit history is kept from contaminating runtime state

---

## Conceptual Overview

LOGOS is divided into **two strictly separated domains**:

1. **Runtime (Execution + Meaning)**
2. **Observability & Record (Non-Semantic, Out-of-Runtime)**

No data flows back from Observability into Runtime.

---

## Runtime Domain (Execution & Meaning)

- Governance defines what is allowed
- Startup proves admissibility
- Logos_Agent is runtime-sovereign
- Subordinate agents propose only
- Meaning lives exclusively in UWM/SMP

---

## Observability Domain (Non-Semantic)

- SOP observes runtime behavior
- SYSTEM_AUDIT_LOGS record history
- No runtime component may read audit logs
- No audit data enters memory

---

## Canonical Mermaid Diagram

```mermaid
flowchart TB

%% Runtime Domain
GOV[Governance]
STARTUP[STARTUP / PXL_Gate]
LP[Logos_Protocol]
LA[Logos_Agent<br/>Runtime Sovereign]

I1[I₁ Agent<br/>SCP-bound]
I2[I₂ Agent<br/>MTP-bound]
I3[I₃ Agent<br/>ARP-bound]

SCP[SCP / MVS / BDN]
MTP[Meaning Translation]
ARP[Advanced Reasoning]

UWM[UWM / SMP<br/>Semantic Memory]

%% Observability Domain
SOP[System Operations Protocol<br/>Telemetry / Health / Ops]
AUDIT[SYSTEM_AUDIT_LOGS<br/>Append-only / Immutable<br/>Out-of-runtime]

%% Runtime Flow
GOV --> STARTUP --> LP --> LA
LA --> I1 --> SCP --> UWM
LA --> I2 --> MTP --> UWM
LA --> I3 --> ARP --> UWM

%% Observability (write-only)
LA -. observes .-> SOP
SOP -. writes .-> AUDIT
STARTUP -. writes .-> AUDIT

%% Explicit constraints
AUDIT -. no readback .-x LA
AUDIT -. no readback .-x SOP

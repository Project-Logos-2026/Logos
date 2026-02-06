
---

# 2️⃣ `MEMORY_DOMAIN_SEPARATION.md`

```md
# Memory Domain Separation (LOGOS)

This document defines the **mandatory separation of memory domains** in the LOGOS System.

This separation is critical for safety, alignment, and prevention of state leakage.

---

## The Three Memory Domains

### 1. Epistemic Memory — UWM / SMP

**Purpose**
- Stores structured meaning packets
- Holds reasoning state
- Represents interpreted inputs and evaluated outputs

**Properties**
- Semantic
- In-runtime
- Governed by PXL and coherence rules
- Resettable between sessions

**Access**
- Writes mediated by Logos_Agent
- Sub-agents may propose, not persist
- No access to SOP or audit logs

---

### 2. Operational Memory — SOP

**Purpose**
- Observes runtime behavior
- Tracks health and performance

**Contents**
- Telemetry
- Heartbeats
- Tick counters
- Smoke tests
- Runtime health metrics

**Properties**
- Non-semantic
- No execution influence
- Readable only by Logos_Agent

---

### 3. Historical Record — SYSTEM_AUDIT_LOGS

**Purpose**
- Canonical record of what occurred

**Contents**
- Test results
- Simulation records
- Crypto hash verifications
- JSON audits
- Governance checks

**Properties**
- Append-only
- Immutable
- Out-of-runtime
- Not importable
- Not readable by runtime

---

## Forbidden Interactions

- SOP → UWM (forbidden)
- AUDIT → SOP (forbidden)
- AUDIT → Runtime (forbidden)
- UWM → AUDIT (direct write forbidden)

All audit writes must be mediated by SOP or Logos_Agent.

---

## Safety Guarantee

This separation ensures:
- No leakage from failed sessions
- No recursive contamination
- No hidden long-term memory
- Clean resets between runs

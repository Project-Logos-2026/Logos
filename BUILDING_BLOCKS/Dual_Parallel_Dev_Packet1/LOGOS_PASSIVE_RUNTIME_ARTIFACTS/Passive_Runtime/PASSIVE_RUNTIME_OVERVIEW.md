# PASSIVE_RUNTIME_OVERVIEW.md

## Purpose
Defines the canonical LOGOS passive runtime model for non-canonical SMP processing.

---

## Core Principles
- Bounded computation
- Zero starvation
- Cross-domain epistemic saturation
- Cryptographic accountability

---

## SMP Classifications
- Provisional
- Conditional
- Rejected

Canonical SMPs live exclusively in CSP.

---

## Semantic Family Batching
Passive runtime operates on **families of semantically related SMPs**, not isolated items.

Each batch contains:
- 1 Provisional SMP
- 1 Conditional SMP
- 1 Rejected SMP

---

## Tri-Cycle Rotation Model

### Cycle 1
- I₂ + MTP → Provisional
- I₃ + ARP → Conditional
- I₁ + SCP → Rejected

### Cycle 2
- Redistribution based on IxAA deficit signals

### Cycle 3
- Final rotation to ensure full agent coverage

No early exit permitted.

---

## Outcomes
- 3/3 approvals → highest priority
- 2/3 approvals → medium priority
- 1/3 approvals → low priority
- 0/3 approvals → re-catalog

---

END DOCUMENT

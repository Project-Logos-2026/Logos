# Agent Read Interfaces — Phase A₁ (Outline)

**Domain:** Agent Read Access (UWM / SMP)  
**Status:** DESIGN-ONLY  
**Authority:** NONE  
**Execution:** FORBIDDEN  
**Posture:** DENY-BY-DEFAULT, FAIL-CLOSED

---

## 1. Purpose

Define how agents may **read** from system knowledge stores
without gaining authority, bypassing governance, or violating privation.

This phase governs **consumption of truth**, not reasoning or action.

---

## 2. Scope (What This Phase Covers)

- Conceptual UWM read access
- SMP read filtering by agent role
- Provenance-aware query semantics
- Privation-aware read denial
- Read-time ambiguity handling

---

## 3. Explicit Non-Goals

This phase does NOT:

- define agent logic or reasoning
- permit writes to memory
- authorize planning or execution
- expose raw storage access
- allow unrestricted queries

---

## 4. Core Concepts to Be Defined

- Read vs infer vs decide
- Role-scoped visibility
- Provenance tagging and trust levels
- Read denial vs redaction
- Privation-enforced read blocking

---

## 5. Read Domains (To Be Specified)

- UWM (Unified World Model)
- SMP (Structured Memory Primitives)
- Cross-agent visibility boundaries
- Historical vs current state access

---

## 6. Privation Interaction (Binding)

- Privation overrides all reads
- Forbidden knowledge must not be revealed
- Ambiguous access resolves to DENY
- Loss of read provenance triggers HALT or DENY

---

## 7. Failure & Ambiguity Semantics

- Ambiguous query → DENY
- Partial visibility → DENY
- Conflicting provenance → strongest constraint
- Unverifiable source → DENY

---

## 8. Completion Criteria

Phase A₁ is complete when:
- a full read-interface semantics document exists,
- scope is locked,
- no enforcement is implied,
- autonomy remains blocked.

---

**END OF PHASE A₁ OUTLINE**

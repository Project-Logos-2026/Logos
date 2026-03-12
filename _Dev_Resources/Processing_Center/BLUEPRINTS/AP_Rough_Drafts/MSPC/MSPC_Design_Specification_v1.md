# MSPC Design Specification v1

**Subsystem:** Manifest & Semantic Projection Controller (MSPC)  
**Tier:** 2 (Operations-Side Governance)  
**Status:** Design Specification  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Subsystem Identity

### §1.1 Core Definition
MSPC (Manifest & Semantic Projection Controller) is the semantic projection governance subsystem within LOGOS. It manages the Semantic Projection Manifest (SMP) and orchestrates the multi-tick pipeline that projects Atomic Axioms (AAs) from the epistemic substrate (EMP/CSP) into the runtime semantic space.

### §1.2 Primary Function
MSPC ensures that **semantic projections are not ad-hoc—they are governed, versioned, and auditable**. Every projection from AA to SMP carries hash-chained integrity, explicit provenance, and fail-closed verification.

### §1.3 Architectural Position
- **Tier:** 2 (Operations-Side)
- **Domain:** Governance (projection orchestration, not semantic reasoning)
- **Upstream Dependencies:** EMP (AA source), CSP (semantic validation), SOP (audit spine), Logos Core (projection consumption)
- **Downstream Consumers:** Logos Core (runtime semantic access), SOP (projection audit trail), CSP (projection feedback)

### §1.4 Authority Boundary
MSPC is **orchestrative only**. It does not:
- Generate semantic content
- Interpret axiom semantics
- Override CSP semantic authority
- Execute reasoning

MSPC governs the projection pipeline; CSP defines semantic coherence.

---

## §2. Semantic Projection Manifest (SMP) Architecture

### §2.1 SMP Structure
```
SMP := {
  manifest_version: Version,
  manifest_hash: Hash,
  genesis_hash: Hash,
  projections: List[SMPEntry],
  metadata: ManifestMetadata
}

SMPEntry := {
  entry_id: EntryID,
  axiom_id: AxiomID,
  projection_context: ContextDescriptor,
  projection_hash: Hash,
  parent_aa_hash: Hash,
  created_at: ISO8601,
  projection_tier: Enum[Active, Staged, Deprecated]
}

ManifestMetadata := {
  created_at: ISO8601,
  last_updated: ISO8601,
  projection_count: int,
  integrity_verified_at: ISO8601
}
```

**Invariants:**
- **INV-SMP-01:** SMP MUST maintain hash chain from genesis.
- **INV-SMP-02:** Every SMPEntry MUST reference a canonical AA.
- **INV-SMP-03:** projection_hash MUST derive from parent_aa_hash.
- **INV-SMP-04:** SMP updates MUST be atomic and versioned.

### §2.2 Projection Tiers
SMP entries are tiered by operational status:

**Active Tier:** Projections currently accessible to Logos Core
**Staged Tier:** Projections validated but not yet activated
**Deprecated Tier:** Projections marked for removal (preserved for audit)

**Invariants:**
- **INV-TIER-01:** Only Active projections served to Logos Core.
- **INV-TIER-02:** Staged projections MUST pass integrity verification before activation.
- **INV-TIER-03:** Deprecated projections MUST remain in SMP (no deletion).

### §2.3 SMP Versioning
SMP is versioned with semantic versioning:
- **Major:** Breaking changes to projection schema
- **Minor:** New projections added
- **Patch:** Integrity fixes or metadata updates

**Invariants:**
- **INV-VER-01:** SMP version MUST increment on any modification.
- **INV-VER-02:** Version increments MUST log to SOP audit spine.
- **INV-VER-03:** Version history MUST be preserved (no overwrite).

---

## §3. Projection Pipeline Architecture

### §3.1 Multi-Tick Projection Pipeline
Projection from AA to SMP occurs over multiple ticks:

**Tick 1: Projection Request**
- Logos Core or CSP requests AA projection
- MSPC validates request against governance rules
- MSPC stages projection request

**Tick 2-N: Semantic Validation**
- MSPC delegates semantic coherence check to CSP
- CSP validates projection context compatibility
- MSPC awaits CSP validation result (async)

**Tick N+1: Hash Chain Integration**
- MSPC receives CSP validation (PASS/FAIL)
- On PASS: MSPC computes projection_hash
- MSPC appends to SMP hash chain via EMP

**Tick N+2: Activation**
- MSPC transitions projection from Staged → Active
- MSPC updates SMP version (minor increment)
- MSPC logs activation to SOP audit spine

**Invariants:**
- **INV-PIPE-01:** Pipeline MUST be multi-tick (no single-tick projection).
- **INV-PIPE-02:** CSP validation MUST complete before hash-chaining.
- **INV-PIPE-03:** Failed projections MUST NOT enter SMP.

### §3.2 Projection Request Structure
```
ProjectionRequest := {
  request_id: UUID,
  axiom_id: AxiomID,
  projection_context: ContextDescriptor,
  requester: Enum[LogosCore, CSP, Manual],
  governance_override: bool  # P2 mode only
}
```

**Invariants:**
- **INV-REQ-01:** Projection requests MUST reference canonical AAs.
- **INV-REQ-02:** governance_override requires P2 mode (§7).
- **INV-REQ-03:** All requests MUST log to SOP before processing.

### §3.3 Projection Lifecycle States
```
ProjectionState := Enum[
  REQUESTED,       # Initial state, awaiting validation
  VALIDATING,      # CSP semantic validation in progress
  VALIDATED,       # CSP validation passed
  HASH_CHAINING,   # EMP hash chain append in progress
  STAGED,          # In SMP Staged tier
  ACTIVE,          # In SMP Active tier
  DEPRECATED,      # Marked for deprecation
  FAILED           # Validation or hash-chaining failed
]
```

**Invariants:**
- **INV-STATE-01:** State transitions MUST be unidirectional (no reversal).
- **INV-STATE-02:** FAILED state MUST trigger SOP audit log.
- **INV-STATE-03:** State transitions MUST be atomic.

---

## §4. Projection Governance

### §4.1 Admissibility Rules
MSPC enforces projection admissibility rules:

1. **AA Existence:** Axiom MUST exist in EMP registry
2. **AA Integrity:** Axiom hash MUST verify via EMP
3. **Projection Context:** Context MUST be CSP-validated
4. **No Duplication:** Projection MUST NOT duplicate existing SMP entry
5. **Governance Mode:** P1/P2 mode constraints MUST be honored

**Invariants:**
- **INV-ADMIT-01:** All admissibility rules MUST pass before projection.
- **INV-ADMIT-02:** Rule violations MUST trigger projection denial.
- **INV-ADMIT-03:** Denials MUST log rationale to SOP.

### §4.2 Projection Denial Protocol
When projection fails admissibility:

```
ProjectionDenial := {
  request_id: UUID,
  denial_reason: DenialReason,
  failed_rule: AdmissibilityRule,
  timestamp: ISO8601
}
```

**Invariants:**
- **INV-DENY-01:** Denials MUST include explicit rationale.
- **INV-DENY-02:** Denials MUST log to SOP before returning.
- **INV-DENY-03:** Repeated denials MUST trigger SOP alert.

### §4.3 Projection Context Validation
MSPC delegates context validation to CSP:

**Validation Contract:**
- CSP receives projection_context
- CSP validates semantic coherence with axiom content
- CSP returns PASS/FAIL with rationale

**Invariants:**
- **INV-CTX-01:** MSPC MUST NOT override CSP validation verdict.
- **INV-CTX-02:** Context validation MUST complete before hash-chaining.
- **INV-CTX-03:** Validation timeouts MUST trigger projection failure.

---

## §5. SMP Integrity Management

### §5.1 Hash Chain Integration
MSPC maintains SMP hash chain via EMP:

```
SMP_hash_n = H(
  SMP_entry_n.projection_context ||
  SMP_hash_{n-1} ||
  AA_parent.hash
)
```

**Invariants:**
- **INV-HASH-01:** SMP hash MUST chain to previous SMP entry.
- **INV-HASH-02:** SMP hash MUST chain to parent AA.
- **INV-HASH-03:** Hash chain breaks MUST trigger integrity failure.

### §5.2 Integrity Verification
MSPC verifies SMP integrity on:
- Projection activation (Staged → Active)
- Logos Core SMP read requests
- Periodic SOP-initiated audits
- Bootstrap self-test

**Invariants:**
- **INV-VERIFY-01:** Verification MUST recompute hash chain.
- **INV-VERIFY-02:** Chain breaks MUST escalate to SOP emergency mode.
- **INV-VERIFY-03:** Verification results MUST log to SOP.

### §5.3 SMP Snapshot Governance
MSPC produces versioned SMP snapshots for audit:

```
SMPSnapshot := {
  snapshot_id: UUID,
  smp_version: Version,
  manifest_hash: Hash,
  created_at: ISO8601,
  projection_count: int
}
```

**Invariants:**
- **INV-SNAP-01:** Snapshots MUST be immutable once created.
- **INV-SNAP-02:** Snapshot manifest_hash MUST match SMP state.
- **INV-SNAP-03:** Snapshots MUST log to SOP audit spine.

---

## §6. Integration Surfaces

### §6.1 EMP Integration
**Interface:** `MSPC ↔ EMP (Hash Chain, AA Access)`

**Contract:**
- MSPC retrieves AAs via EMP (not direct CSP access)
- MSPC delegates hash-chaining to EMP
- EMP verifies AA integrity before serving to MSPC

**Invariants:**
- **INV-EMP-01:** MSPC MUST access AAs via EMP, not CSP directly.
- **INV-EMP-02:** MSPC MUST use EMP for SMP hash-chaining.
- **INV-EMP-03:** MSPC MUST honor EMP AA deprecation flags.

Cross-reference: EMP v1 §6.4 (SMP Integration)

### §6.2 CSP Integration
**Interface:** `MSPC → CSP (Semantic Validation)`

**Contract:**
- MSPC delegates projection context validation to CSP
- CSP validates semantic coherence, not projection governance
- CSP provides async validation results

**Invariants:**
- **INV-CSP-01:** MSPC MUST delegate semantic validation to CSP.
- **INV-CSP-02:** MSPC MUST NOT override CSP validation verdicts.
- **INV-CSP-03:** MSPC MUST handle CSP validation timeouts gracefully.

Cross-reference: CSP v1 §4 (Semantic Validation), §11 (MSPC Integration)

### §6.3 SOP Integration
**Interface:** `MSPC → SOP (Audit Spine)`

**Contract:**
- MSPC logs all projection lifecycle events to SOP
- SOP provides hash chain integrity verification
- MSPC participates in SOP audit spine

**Invariants:**
- **INV-SOP-01:** MSPC MUST log projection requests, denials, activations to SOP.
- **INV-SOP-02:** MSPC MUST verify SOP audit hash before appending events.
- **INV-SOP-03:** MSPC MUST escalate audit failures to SOP emergency mode.

Cross-reference: SOP v1 §4 (Audit Spine), §12 (MSPC Integration)

### §6.4 Logos Core Integration
**Interface:** `Logos Core → MSPC (SMP Access)`

**Contract:**
- Logos Core reads Active-tier SMP entries via MSPC
- MSPC verifies SMP integrity before serving projections
- Logos Core honors MSPC projection tier boundaries

**Invariants:**
- **INV-LC-01:** Logos Core MUST access SMP via MSPC, not directly.
- **INV-LC-02:** MSPC MUST serve only Active-tier projections.
- **INV-LC-03:** MSPC MUST verify SMP integrity before serving.

Cross-reference: Logos Core v1 §8 (SMP Access), §13 (MSPC Integration)

---

## §7. Governance Mode Compatibility

### §7.1 P1/P2 Mode Awareness
MSPC adapts to governance mode (P1 vs P2) as configured in Logos Core §14:

**P1 Mode (Strict):**
- All projection admissibility rules enforced
- No governance overrides permitted
- Maximum audit verbosity

**P2 Mode (Relaxed Task Sources):**
- Admissibility rules unchanged
- governance_override flag permitted in ProjectionRequest (§3.2)
- Manual projection requests allowed (P1: denied)

**Invariants:**
- **INV-GM-01:** Projection integrity rules MUST NOT relax in P2 mode.
- **INV-GM-02:** MSPC MUST query Logos Core for governance mode per-tick.
- **INV-GM-03:** Mode transitions MUST preserve SMP hash chain.

### §7.2 Mode Transition Protocol
When Logos Core signals governance mode change:
1. MSPC completes in-flight projection operations
2. MSPC flushes pending audit events to SOP
3. MSPC re-initializes with new mode parameters
4. MSPC resumes operation

**Invariants:**
- **INV-MT-01:** Transitions MUST NOT corrupt SMP hash chain.
- **INV-MT-02:** Transitions MUST log to SOP audit spine.
- **INV-MT-03:** MSPC MUST reject new projections during transition.

---

## §8. Telemetry & Observability

### §8.1 Projection Metrics
MSPC produces telemetry on:
- **Projection Request Rate:** Requests per tick
- **Projection Success Rate:** Activated projections / total requests
- **Validation Latency:** CSP validation duration
- **Hash-Chaining Latency:** EMP hash append duration

**Invariants:**
- **INV-TEL-01:** All metrics MUST emit to SOP telemetry backend.
- **INV-TEL-02:** Metrics MUST NOT leak semantic content.
- **INV-TEL-03:** Telemetry failures MUST NOT block projection operations.

### §8.2 SMP Health Metrics
MSPC tracks SMP operational health:
- **Active Projection Count**
- **Staged Projection Count**
- **Deprecated Projection Count**
- **SMP Hash Verification Pass Rate**

**Invariants:**
- **INV-HEALTH-01:** Health metrics MUST aggregate per-tick.
- **INV-HEALTH-02:** Hash verification failures MUST trigger SOP alert.
- **INV-HEALTH-03:** Health metrics MUST log to SOP audit spine.

### §8.3 Pipeline Performance Metrics
MSPC tracks pipeline throughput:
- **Average Projection Completion Time:** Request → Activation
- **Pipeline Stage Latencies:** Per-stage timing breakdown
- **Validation Timeout Frequency**

**Invariants:**
- **INV-PERF-01:** Pipeline metrics MUST aggregate per-tick.
- **INV-PERF-02:** Timeout spikes MUST trigger SOP degradation ladder.
- **INV-PERF-03:** Performance data MUST be available for SOP analysis.

---

## §9. Bootstrap & Initialization

### §9.1 Initialization Sequence
MSPC initializes during Logos Core Phase-G activation (Logos Core §5.2):

1. **Verify Upstream Dependencies:**
   - EMP hash chain manager accessible
   - CSP semantic validation interface available
   - SOP audit spine initialized
   - Logos Core SMP access interface ready

2. **Load or Initialize SMP:**
   - If SMP exists: Load and verify hash chain integrity
   - If SMP absent: Initialize with genesis hash from EMP

3. **Initialize Projection Pipeline:**
   - Allocate pipeline state tracker
   - Initialize projection request queue
   - Configure CSP validation client

4. **Self-Test:**
   - Create synthetic projection request
   - Verify CSP validation path
   - Test SOP audit logging
   - Verify SMP hash chain integrity

5. **Signal Ready:**
   - Notify Logos Core MSPC available
   - Begin accepting projection requests

**Invariants:**
- **INV-INIT-01:** MSPC MUST NOT signal ready until dependencies verified.
- **INV-INIT-02:** SMP hash chain MUST verify before accepting projections.
- **INV-INIT-03:** Self-test failure MUST trigger Logos Core bootstrap halt.

### §9.2 Shutdown Protocol
MSPC shutdown occurs during Logos Core tick boundary (Logos Core §4.2):

1. Stop accepting new projection requests
2. Complete in-flight projection operations
3. Flush all pending audit events to SOP
4. Create final SMP snapshot
5. Verify SMP hash chain integrity (final check)
6. Signal shutdown complete to Logos Core

**Invariants:**
- **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight projections.
- **INV-SHUT-02:** Shutdown MUST guarantee all audit events logged.
- **INV-SHUT-03:** Incomplete shutdown MUST trigger Logos Core emergency halt.

---

## §10. Invariant Summary

### Core Invariants
1. **INV-SMP-01:** SMP MUST maintain hash chain from genesis.
2. **INV-SMP-02:** Every SMPEntry MUST reference canonical AA.
3. **INV-SMP-03:** projection_hash MUST derive from parent_aa_hash.
4. **INV-SMP-04:** SMP updates MUST be atomic and versioned.
5. **INV-TIER-01:** Only Active projections served to Logos Core.
6. **INV-TIER-02:** Staged projections MUST pass verification before activation.
7. **INV-TIER-03:** Deprecated projections MUST remain in SMP.
8. **INV-VER-01:** SMP version MUST increment on modification.
9. **INV-VER-02:** Version increments MUST log to SOP.
10. **INV-VER-03:** Version history MUST be preserved.
11. **INV-PIPE-01:** Pipeline MUST be multi-tick.
12. **INV-PIPE-02:** CSP validation MUST complete before hash-chaining.
13. **INV-PIPE-03:** Failed projections MUST NOT enter SMP.
14. **INV-REQ-01:** Requests MUST reference canonical AAs.
15. **INV-REQ-02:** governance_override requires P2 mode.
16. **INV-REQ-03:** Requests MUST log to SOP before processing.
17. **INV-STATE-01:** State transitions MUST be unidirectional.
18. **INV-STATE-02:** FAILED state MUST log to SOP.
19. **INV-STATE-03:** State transitions MUST be atomic.
20. **INV-ADMIT-01:** All admissibility rules MUST pass.
21. **INV-ADMIT-02:** Rule violations MUST deny projection.
22. **INV-ADMIT-03:** Denials MUST log rationale to SOP.
23. **INV-DENY-01:** Denials MUST include rationale.
24. **INV-DENY-02:** Denials MUST log to SOP before return.
25. **INV-DENY-03:** Repeated denials MUST trigger SOP alert.
26. **INV-CTX-01:** MSPC MUST NOT override CSP validation.
27. **INV-CTX-02:** Context validation before hash-chaining.
28. **INV-CTX-03:** Validation timeouts MUST fail projection.
29. **INV-HASH-01:** SMP hash MUST chain to previous entry.
30. **INV-HASH-02:** SMP hash MUST chain to parent AA.
31. **INV-HASH-03:** Hash chain breaks MUST trigger failure.
32. **INV-VERIFY-01:** Verification MUST recompute hash chain.
33. **INV-VERIFY-02:** Chain breaks MUST escalate to SOP emergency.
34. **INV-VERIFY-03:** Verification results MUST log to SOP.
35. **INV-SNAP-01:** Snapshots MUST be immutable.
36. **INV-SNAP-02:** Snapshot hash MUST match SMP state.
37. **INV-SNAP-03:** Snapshots MUST log to SOP.
38. **INV-EMP-01:** MSPC MUST access AAs via EMP.
39. **INV-EMP-02:** MSPC MUST use EMP for hash-chaining.
40. **INV-EMP-03:** MSPC MUST honor EMP deprecation flags.
41. **INV-CSP-01:** MSPC MUST delegate validation to CSP.
42. **INV-CSP-02:** MSPC MUST NOT override CSP verdicts.
43. **INV-CSP-03:** MSPC MUST handle validation timeouts.
44. **INV-SOP-01:** MSPC MUST log all lifecycle events to SOP.
45. **INV-SOP-02:** MSPC MUST verify SOP audit hash.
46. **INV-SOP-03:** MSPC MUST escalate audit failures.
47. **INV-LC-01:** Logos Core MUST access SMP via MSPC.
48. **INV-LC-02:** MSPC MUST serve only Active projections.
49. **INV-LC-03:** MSPC MUST verify SMP before serving.
50. **INV-GM-01:** Integrity rules MUST NOT relax in P2.
51. **INV-GM-02:** MSPC MUST query governance mode per-tick.
52. **INV-GM-03:** Mode transitions MUST preserve hash chain.
53. **INV-MT-01:** Transitions MUST NOT corrupt SMP.
54. **INV-MT-02:** Transitions MUST log to SOP.
55. **INV-MT-03:** MSPC MUST reject projections during transition.
56. **INV-TEL-01:** Metrics MUST emit to SOP telemetry.
57. **INV-TEL-02:** Metrics MUST NOT leak semantic content.
58. **INV-TEL-03:** Telemetry failures MUST NOT block operations.
59. **INV-HEALTH-01:** Health metrics MUST aggregate per-tick.
60. **INV-HEALTH-02:** Hash failures MUST trigger SOP alert.
61. **INV-HEALTH-03:** Health metrics MUST log to SOP.
62. **INV-PERF-01:** Pipeline metrics MUST aggregate per-tick.
63. **INV-PERF-02:** Timeout spikes MUST trigger degradation ladder.
64. **INV-PERF-03:** Performance data MUST be available to SOP.
65. **INV-INIT-01:** MSPC MUST verify dependencies before ready.
66. **INV-INIT-02:** SMP hash chain MUST verify before operations.
67. **INV-INIT-03:** Self-test failure MUST halt bootstrap.
68. **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight ops.
69. **INV-SHUT-02:** Shutdown MUST guarantee all events logged.
70. **INV-SHUT-03:** Incomplete shutdown MUST trigger emergency halt.

**Total Invariants:** 70

---

## §11. Cross-Reference Map

| External Subsystem | Referenced Sections | Integration Surface |
|--------------------|---------------------|---------------------|
| EMP v1 | §6.4 | Hash Chain, AA Access |
| CSP v1 | §4, §11 | Semantic Validation |
| SOP v1 | §4, §12 | Audit Spine, Telemetry Backend |
| Logos Core v1 | §4.2, §5.2, §8, §13, §14 | SMP Access, Phase-G, Governance Mode |

---

**End of Specification**

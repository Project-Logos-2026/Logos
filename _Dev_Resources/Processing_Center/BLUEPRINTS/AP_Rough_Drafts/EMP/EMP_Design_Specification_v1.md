# EMP Design Specification v1

**Subsystem:** Epistemic Management Protocol (EMP)  
**Tier:** 2 (Operations-Side Governance)  
**Status:** Design Specification  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Subsystem Identity

### §1.1 Core Definition
EMP (Epistemic Management Protocol) is the epistemic artifact governance subsystem within LOGOS. It manages the lifecycle, integrity, and provenance of all epistemic artifacts—primarily Atomic Axioms (AAs) and their projections into the Semantic Projection Manifest (SMP).

### §1.2 Primary Function
EMP ensures that **knowledge is not created or modified—it is verified, tracked, and governed**. Every epistemic artifact in LOGOS carries cryptographic provenance, hash-chained integrity, and explicit governance boundaries.

### §1.3 Architectural Position
- **Tier:** 2 (Operations-Side)
- **Domain:** Governance (epistemic integrity, not semantic reasoning)
- **Upstream Dependencies:** CSP (semantic substrate), SOP (audit spine), Logos Core (artifact consumption)
- **Downstream Consumers:** CSP (AA registry), SMP (projection manifest), Logos Core (axiom access), SOP (provenance audit)

### §1.4 Authority Boundary
EMP is **custodial only**. It does not:
- Generate semantic content
- Interpret axiom meaning
- Override CSP semantic authority
- Execute reasoning

EMP manages artifacts; CSP defines their semantics.

---

## §2. Epistemic Artifact Model

### §2.1 Artifact Hierarchy
```
Epistemic Artifacts
├── Atomic Axioms (AAs)
│   ├── Canonical Definition
│   ├── Provenance Record
│   ├── Hash Chain Entry
│   └── Governance Metadata
└── Semantic Projections
    ├── SMP Entries (manifest projections)
    ├── Projection Provenance
    └── Integrity Hash
```

### §2.2 Atomic Axiom Structure
```
AtomicAxiom := {
  axiom_id: AxiomID,
  content: SemanticContent,
  provenance: ProvenanceRecord,
  hash: Hash,
  created_at: ISO8601,
  governance_tags: List[GovernanceTag]
}

ProvenanceRecord := {
  source: AxiomSource,
  creator_signature: Signature,
  verification_chain: List[VerificationStep],
  immutability_lock: bool
}
```

**Invariants:**
- **INV-AA-01:** Every AA MUST have a unique axiom_id.
- **INV-AA-02:** AA content MUST be immutable once hash-chained.
- **INV-AA-03:** AA provenance MUST include creator signature.
- **INV-AA-04:** AA hash MUST be verifiable via hash chain.

### §2.3 Semantic Projection Manifest (SMP) Integration
SMP entries are **projections** of AAs into the runtime semantic space. EMP governs the projection integrity:

```
SMPEntry := {
  axiom_id: AxiomID,
  projection_context: ContextDescriptor,
  projection_hash: Hash,
  parent_aa_hash: Hash,
  timestamp: ISO8601
}
```

**Invariants:**
- **INV-SMP-01:** SMP entries MUST reference a canonical AA.
- **INV-SMP-02:** projection_hash MUST derive from parent_aa_hash.
- **INV-SMP-03:** SMP updates MUST preserve hash chain continuity.

---

## §3. Artifact Lifecycle Management

### §3.1 AA Creation Protocol
AA creation is a governed process with fail-closed semantics:

**Workflow:**
```
[CSP] → EMP.create_axiom(content, provenance)
         ↓
    [Provenance Validation]
         ↓
    [Hash Chain Append]
         ↓
    [Immutability Lock]
         ↓
    [SOP Audit Log]
         ↓
    ADMIT → [AA Registry] → [Return axiom_id]
    DENY  → [Audit Log] → [Raise CreationFailure]
```

**Invariants:**
- **INV-CREATE-01:** AA creation MUST validate provenance before hash-chaining.
- **INV-CREATE-02:** Creation failure MUST NOT leave partial AA state.
- **INV-CREATE-03:** Successful creation MUST log to SOP audit spine.

### §3.2 AA Retrieval Protocol
EMP provides read-only access to AAs with integrity verification:

```python
def retrieve_axiom(axiom_id: AxiomID) -> AtomicAxiom:
    """
    Retrieve AA with hash chain verification.
    
    Invariants:
        - INV-RETRIEVE-01: Verify hash before return
        - INV-RETRIEVE-02: Reject corrupted AAs
        - INV-RETRIEVE-03: Log retrieval to SOP
    """
```

**Invariants:**
- **INV-RETRIEVE-01:** Retrieval MUST verify AA hash against chain.
- **INV-RETRIEVE-02:** Corrupted AAs MUST trigger integrity alert.
- **INV-RETRIEVE-03:** All retrievals MUST log to SOP audit spine.

### §3.3 AA Immutability Guarantee
Once an AA is hash-chained, it is **immutable**. Modifications are prohibited:

**Invariants:**
- **INV-IMMUT-01:** Hash-chained AAs MUST NOT be modified.
- **INV-IMMUT-02:** Update attempts MUST raise ImmutabilityViolation.
- **INV-IMMUT-03:** Immutability violations MUST trigger SOP emergency mode.

### §3.4 AA Deprecation (Not Deletion)
AAs cannot be deleted—only deprecated with provenance tracking:

```
Deprecation := {
  axiom_id: AxiomID,
  deprecated_at: ISO8601,
  rationale: String,
  superseded_by: Optional[AxiomID]
}
```

**Invariants:**
- **INV-DEPREC-01:** Deprecation MUST preserve AA in hash chain.
- **INV-DEPREC-02:** Deprecated AAs MUST be flagged, not deleted.
- **INV-DEPREC-03:** Deprecation MUST log rationale to SOP.

---

## §4. Hash Chain Integrity

### §4.1 Hash Chain Architecture
EMP maintains a two-tier hash chain:

**Tier 1: AA Hash Chain** (per-axiom integrity)
```
AA_n.hash = H(AA_n.content || AA_{n-1}.hash)
```

**Tier 2: SMP Projection Chain** (manifest integrity)
```
SMP_n.hash = H(SMP_n.projection || SMP_{n-1}.hash || AA_parent.hash)
```

**Invariants:**
- **INV-HC-01:** AA hash MUST chain to previous AA.
- **INV-HC-02:** SMP projection hash MUST chain to parent AA.
- **INV-HC-03:** Hash chain breaks MUST trigger integrity failure.

### §4.2 Integrity Verification
EMP verifies hash chain integrity on:
- AA retrieval (INV-RETRIEVE-01)
- SMP projection read
- Periodic SOP-initiated audits
- Bootstrap self-test

**Invariants:**
- **INV-VERIFY-01:** Verification MUST recompute full hash chain.
- **INV-VERIFY-02:** Chain breaks MUST escalate to SOP emergency mode.
- **INV-VERIFY-03:** Verification results MUST log to SOP audit spine.

### §4.3 Genesis Hash
The hash chain originates from a **genesis hash** established at LOGOS bootstrap:

```
GenesisHash := H("LOGOS_EMP_GENESIS" || bootstrap_timestamp || system_nonce)
```

**Invariants:**
- **INV-GENESIS-01:** Genesis hash MUST be immutable.
- **INV-GENESIS-02:** First AA MUST chain to genesis hash.
- **INV-GENESIS-03:** Genesis hash MUST be verifiable via SOP audit log.

---

## §5. Provenance Tracking

### §5.1 Provenance Record Structure
Every AA carries a provenance record:

```
ProvenanceRecord := {
  source: AxiomSource,              # CSP, Import, Generated
  creator_id: CreatorID,            # Entity that authored AA
  creator_signature: Signature,     # Cryptographic signature
  verification_steps: List[Step],   # Validation history
  import_metadata: Optional[Dict],  # If imported from external source
  immutability_lock: bool           # True once hash-chained
}

VerificationStep := {
  verifier: VerifierID,
  timestamp: ISO8601,
  verification_type: Enum[Structural, Semantic, Cryptographic],
  result: Enum[Pass, Fail]
}
```

**Invariants:**
- **INV-PROV-01:** Provenance MUST include creator signature.
- **INV-PROV-02:** Verification steps MUST be append-only.
- **INV-PROV-03:** Provenance MUST be immutable once AA is hash-chained.

### §5.2 Creator Signature Verification
EMP validates creator signatures before AA creation:

**Invariants:**
- **INV-SIG-01:** EMP MUST verify creator signature before hash-chaining.
- **INV-SIG-02:** Invalid signatures MUST trigger AA creation denial.
- **INV-SIG-03:** Signature verification failures MUST log to SOP.

### §5.3 Import Governance
AAs imported from external sources require additional provenance:

```
ImportMetadata := {
  source_uri: URI,
  import_timestamp: ISO8601,
  importer_signature: Signature,
  trust_level: Enum[Trusted, Untrusted, Quarantined]
}
```

**Invariants:**
- **INV-IMPORT-01:** Imported AAs MUST include import metadata.
- **INV-IMPORT-02:** Untrusted imports MUST be flagged for manual review.
- **INV-IMPORT-03:** Import provenance MUST be verifiable via SOP audit.

---

## §6. Integration Surfaces

### §6.1 CSP Integration
**Interface:** `EMP ↔ CSP (AA Registry)`

**Contract:**
- CSP delegates AA storage and retrieval to EMP
- CSP provides semantic content; EMP governs integrity
- EMP validates AA structure; CSP validates semantic coherence

**Invariants:**
- **INV-CSP-01:** EMP MUST delegate semantic validation to CSP.
- **INV-CSP-02:** CSP MUST route all AA storage through EMP.
- **INV-CSP-03:** EMP MUST NOT interpret semantic content.

Cross-reference: CSP v1 §3 (Semantic Axiom Management), §10 (EMP Integration)

### §6.2 SOP Integration
**Interface:** `EMP → SOP (Audit Spine)`

**Contract:**
- EMP logs all AA lifecycle events to SOP
- SOP provides hash chain integrity verification
- EMP participates in SOP audit spine

**Invariants:**
- **INV-SOP-01:** EMP MUST log AA creation, retrieval, deprecation to SOP.
- **INV-SOP-02:** EMP MUST verify SOP audit hash before appending events.
- **INV-SOP-03:** EMP MUST escalate audit failures to SOP emergency mode.

Cross-reference: SOP v1 §4 (Audit Spine), §11 (EMP Integration)

### §6.3 Logos Core Integration
**Interface:** `Logos Core → EMP (Axiom Access)`

**Contract:**
- Logos Core retrieves AAs via EMP (not direct CSP access)
- EMP verifies hash integrity before serving AAs
- Logos Core honors EMP deprecation flags

**Invariants:**
- **INV-LC-01:** Logos Core MUST access AAs via EMP, not CSP directly.
- **INV-LC-02:** EMP MUST reject corrupted AA requests.
- **INV-LC-03:** Logos Core MUST respect AA deprecation flags.

Cross-reference: Logos Core v1 §7 (Axiom Access), §12 (EMP Integration)

### §6.4 SMP Integration
**Interface:** `EMP → SMP (Projection Manifest)`

**Contract:**
- EMP governs SMP projection integrity
- SMP projections MUST chain to parent AAs
- EMP verifies projection hash on SMP updates

**Invariants:**
- **INV-SMP-INT-01:** SMP projections MUST reference canonical AAs.
- **INV-SMP-INT-02:** EMP MUST verify projection hash chain.
- **INV-SMP-INT-03:** SMP updates MUST log to SOP via EMP.

Cross-reference: MSPC v1 §4 (SMP Architecture) [to be defined in T2]

---

## §7. Telemetry & Observability

### §7.1 Artifact Metrics
EMP produces telemetry on:
- **AA Creation Rate:** New axioms per tick
- **AA Retrieval Frequency:** Access patterns
- **Deprecation Events:** AA lifecycle transitions
- **Hash Verification Success Rate:** Integrity health

**Invariants:**
- **INV-TEL-01:** All metrics MUST emit to SOP telemetry backend.
- **INV-TEL-02:** Metrics MUST NOT leak AA semantic content.
- **INV-TEL-03:** Telemetry failures MUST NOT block AA operations.

### §7.2 Integrity Audit Metrics
EMP tracks hash chain health:
- **Hash Chain Verification Pass Rate**
- **Chain Break Detection Events**
- **Genesis Hash Validation Frequency**

**Invariants:**
- **INV-AUDIT-01:** Chain breaks MUST trigger immediate SOP alert.
- **INV-AUDIT-02:** Audit metrics MUST aggregate per-tick.
- **INV-AUDIT-03:** Audit results MUST log to SOP audit spine.

### §7.3 Provenance Audit Trail
Every AA operation contributes to the SOP audit spine:
- AA creation events
- Retrieval requests
- Deprecation actions
- Integrity verification results

**Invariants:**
- **INV-TRAIL-01:** Audit trail MUST be append-only.
- **INV-TRAIL-02:** Audit entries MUST be hash-chained.
- **INV-TRAIL-03:** Trail breaks MUST trigger SOP emergency mode.

---

## §8. Governance Mode Compatibility

### §8.1 P1/P2 Mode Awareness
EMP adapts to governance mode (P1 vs P2) as configured in Logos Core §14:

**P1 Mode (Strict):**
- All provenance validation enforced
- Maximum audit verbosity
- No relaxation of integrity checks

**P2 Mode (Relaxed Task Sources):**
- Provenance validation unchanged
- Integrity checks unchanged
- AA lifecycle governance unchanged

**Invariants:**
- **INV-GM-01:** EMP integrity rules MUST NOT relax in P2 mode.
- **INV-GM-02:** EMP MUST query Logos Core for governance mode per-tick.
- **INV-GM-03:** Mode transitions MUST preserve hash chain integrity.

### §8.2 Mode Transition Protocol
When Logos Core signals governance mode change:
1. EMP completes in-flight AA operations
2. EMP flushes pending audit events to SOP
3. EMP re-initializes with new mode parameters
4. EMP resumes operation

**Invariants:**
- **INV-MT-01:** Transitions MUST NOT corrupt hash chain.
- **INV-MT-02:** Transitions MUST log to SOP audit spine.
- **INV-MT-03:** EMP MUST reject new AA operations during transition.

---

## §9. Bootstrap & Initialization

### §9.1 Initialization Sequence
EMP initializes during Logos Core Phase-G activation (Logos Core §5.2):

1. **Verify Upstream Dependencies:**
   - CSP semantic substrate accessible
   - SOP audit spine initialized
   - Logos Core axiom access interface available

2. **Load Genesis Hash:**
   - Retrieve or generate genesis hash
   - Verify genesis hash immutability
   - Log genesis hash to SOP

3. **Initialize Hash Chains:**
   - AA hash chain (starting from genesis)
   - SMP projection chain (if SMP exists)

4. **Self-Test:**
   - Create synthetic AA
   - Verify hash chain integrity
   - Test SOP audit logging

5. **Signal Ready:**
   - Notify Logos Core EMP available
   - Begin accepting AA operations

**Invariants:**
- **INV-INIT-01:** EMP MUST NOT signal ready until dependencies verified.
- **INV-INIT-02:** Genesis hash MUST be established before AA operations.
- **INV-INIT-03:** Self-test failure MUST trigger Logos Core bootstrap halt.

### §9.2 Shutdown Protocol
EMP shutdown occurs during Logos Core tick boundary (Logos Core §4.2):

1. Stop accepting new AA operations
2. Complete in-flight AA operations
3. Flush all pending audit events to SOP
4. Verify hash chain integrity (final check)
5. Signal shutdown complete to Logos Core

**Invariants:**
- **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight operations.
- **INV-SHUT-02:** Shutdown MUST guarantee all audit events logged.
- **INV-SHUT-03:** Incomplete shutdown MUST trigger Logos Core emergency halt.

---

## §10. Invariant Summary

### Core Invariants
1. **INV-AA-01:** Every AA MUST have unique axiom_id.
2. **INV-AA-02:** AA content MUST be immutable once hash-chained.
3. **INV-AA-03:** AA provenance MUST include creator signature.
4. **INV-AA-04:** AA hash MUST be verifiable via hash chain.
5. **INV-SMP-01:** SMP entries MUST reference canonical AA.
6. **INV-SMP-02:** projection_hash MUST derive from parent_aa_hash.
7. **INV-SMP-03:** SMP updates MUST preserve hash chain continuity.
8. **INV-CREATE-01:** AA creation MUST validate provenance first.
9. **INV-CREATE-02:** Creation failure MUST NOT leave partial state.
10. **INV-CREATE-03:** Successful creation MUST log to SOP.
11. **INV-RETRIEVE-01:** Retrieval MUST verify AA hash.
12. **INV-RETRIEVE-02:** Corrupted AAs MUST trigger alert.
13. **INV-RETRIEVE-03:** Retrievals MUST log to SOP.
14. **INV-IMMUT-01:** Hash-chained AAs MUST NOT be modified.
15. **INV-IMMUT-02:** Update attempts MUST raise violation.
16. **INV-IMMUT-03:** Violations MUST trigger SOP emergency mode.
17. **INV-DEPREC-01:** Deprecation MUST preserve AA in chain.
18. **INV-DEPREC-02:** Deprecated AAs MUST be flagged, not deleted.
19. **INV-DEPREC-03:** Deprecation MUST log rationale to SOP.
20. **INV-HC-01:** AA hash MUST chain to previous AA.
21. **INV-HC-02:** SMP projection hash MUST chain to parent AA.
22. **INV-HC-03:** Hash chain breaks MUST trigger failure.
23. **INV-VERIFY-01:** Verification MUST recompute full chain.
24. **INV-VERIFY-02:** Chain breaks MUST escalate to SOP emergency.
25. **INV-VERIFY-03:** Verification results MUST log to SOP.
26. **INV-GENESIS-01:** Genesis hash MUST be immutable.
27. **INV-GENESIS-02:** First AA MUST chain to genesis hash.
28. **INV-GENESIS-03:** Genesis hash MUST be verifiable via SOP.
29. **INV-PROV-01:** Provenance MUST include creator signature.
30. **INV-PROV-02:** Verification steps MUST be append-only.
31. **INV-PROV-03:** Provenance MUST be immutable once chained.
32. **INV-SIG-01:** EMP MUST verify creator signature.
33. **INV-SIG-02:** Invalid signatures MUST deny creation.
34. **INV-SIG-03:** Signature failures MUST log to SOP.
35. **INV-IMPORT-01:** Imported AAs MUST include import metadata.
36. **INV-IMPORT-02:** Untrusted imports MUST be flagged.
37. **INV-IMPORT-03:** Import provenance MUST be verifiable.
38. **INV-CSP-01:** EMP MUST delegate semantic validation to CSP.
39. **INV-CSP-02:** CSP MUST route AA storage through EMP.
40. **INV-CSP-03:** EMP MUST NOT interpret semantic content.
41. **INV-SOP-01:** EMP MUST log AA lifecycle events to SOP.
42. **INV-SOP-02:** EMP MUST verify SOP audit hash before append.
43. **INV-SOP-03:** EMP MUST escalate audit failures.
44. **INV-LC-01:** Logos Core MUST access AAs via EMP.
45. **INV-LC-02:** EMP MUST reject corrupted AA requests.
46. **INV-LC-03:** Logos Core MUST respect deprecation flags.
47. **INV-SMP-INT-01:** SMP projections MUST reference canonical AAs.
48. **INV-SMP-INT-02:** EMP MUST verify projection hash chain.
49. **INV-SMP-INT-03:** SMP updates MUST log to SOP via EMP.
50. **INV-TEL-01:** Metrics MUST emit to SOP telemetry.
51. **INV-TEL-02:** Metrics MUST NOT leak semantic content.
52. **INV-TEL-03:** Telemetry failures MUST NOT block operations.
53. **INV-AUDIT-01:** Chain breaks MUST trigger SOP alert.
54. **INV-AUDIT-02:** Audit metrics MUST aggregate per-tick.
55. **INV-AUDIT-03:** Audit results MUST log to SOP.
56. **INV-TRAIL-01:** Audit trail MUST be append-only.
57. **INV-TRAIL-02:** Audit entries MUST be hash-chained.
58. **INV-TRAIL-03:** Trail breaks MUST trigger SOP emergency.
59. **INV-GM-01:** Integrity rules MUST NOT relax in P2.
60. **INV-GM-02:** EMP MUST query governance mode per-tick.
61. **INV-GM-03:** Mode transitions MUST preserve hash chain.
62. **INV-MT-01:** Transitions MUST NOT corrupt hash chain.
63. **INV-MT-02:** Transitions MUST log to SOP.
64. **INV-MT-03:** EMP MUST reject operations during transition.
65. **INV-INIT-01:** EMP MUST verify dependencies before ready.
66. **INV-INIT-02:** Genesis hash MUST be established first.
67. **INV-INIT-03:** Self-test failure MUST halt bootstrap.
68. **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight ops.
69. **INV-SHUT-02:** Shutdown MUST guarantee all events logged.
70. **INV-SHUT-03:** Incomplete shutdown MUST trigger emergency halt.

**Total Invariants:** 70

---

## §11. Cross-Reference Map

| External Subsystem | Referenced Sections | Integration Surface |
|--------------------|---------------------|---------------------|
| CSP v1 | §3, §10 | AA Registry, Semantic Validation |
| SOP v1 | §4, §11 | Audit Spine, Telemetry Backend |
| Logos Core v1 | §4.2, §5.2, §7, §12, §14 | Axiom Access, Phase-G, Governance Mode |
| MSPC v1 | §4 | SMP Projection Integrity |

---

**End of Specification**

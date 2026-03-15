# DRAC Design Specification v1

**Subsystem:** Dynamic Reasoning Admissibility Controller (DRAC)  
**Tier:** 2 (Operations-Side Governance)  
**Status:** Design Specification  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Subsystem Identity

### §1.1 Core Definition
DRAC (Dynamic Reasoning Admissibility Controller) is the proof-gated reasoning authorization subsystem within LOGOS. It enforces the architectural principle that **reasoning authority is not assumed—it is proven and granted**.

### §1.2 Primary Function
DRAC evaluates reasoning requests against Protopraxic Logic (PXL) proof obligations and issues admissibility decisions with fail-closed semantics. No reasoning occurs in LOGOS without DRAC authorization.

### §1.3 Architectural Position
- **Tier:** 2 (Operations-Side)
- **Domain:** Governance (not reasoning execution)
- **Upstream Dependencies:** Logos Core (PXL Gate interface), SOP (audit spine), RGE (proof context provision)
- **Downstream Consumers:** Logos Core (execution gate), SOP (admissibility audit trail)

### §1.4 Authority Boundary
DRAC is **evaluative only**. It does not:
- Execute reasoning
- Modify proofs
- Override PXL constraints
- Interpret task semantics

DRAC issues **ADMIT** or **DENY** verdicts. Execution authority remains with Logos Core.

---

## §2. PXL Proof Gate Architecture

### §2.1 Proof Obligation Model
Every reasoning request arriving at DRAC carries a **Proof Obligation Packet (POP)**:

```
POP := {
  request_id: UUID,
  task_descriptor: TaskDescriptor,
  axiom_references: List[AxiomID],
  proof_fragments: List[ProofFragment],
  context_hash: Hash,
  timestamp: ISO8601
}
```

**Invariants:**
- **INV-POP-01:** Every POP MUST reference at least one canonical axiom.
- **INV-POP-02:** Proof fragments MUST be PXL-compliant (validated by PXL Gate in Logos Core).
- **INV-POP-03:** Context hash MUST match RGE-supplied context fingerprint.

### §2.2 PXL Gate Interface
DRAC delegates PXL proof verification to the **PXL Gate** (owned by Logos Core, §6). DRAC's role is to:
1. Receive POP from Logos Core
2. Request proof validation from PXL Gate
3. Interpret validation result as ADMIT/DENY decision
4. Return decision to Logos Core

**Invariants:**
- **INV-GATE-01:** DRAC MUST NOT bypass PXL Gate for proof validation.
- **INV-GATE-02:** DRAC MUST NOT cache or replay proof validation results.
- **INV-GATE-03:** Every ADMIT decision MUST have a corresponding PXL Gate validation record.

### §2.3 Proof Fragment Sources
DRAC accepts proof fragments from three sources:
1. **Task Payload:** Embedded proofs from task initiator
2. **RGE Context:** RGE-supplied geometric/configuration proofs (per RGE v3 §8.4)
3. **CSP Axioms:** Axiom references from CSP's semantic substrate

**Invariants:**
- **INV-SRC-01:** DRAC MUST validate source authenticity before proof evaluation.
- **INV-SRC-02:** Proof fragments from untrusted sources MUST trigger automatic DENY.
- **INV-SRC-03:** RGE-supplied proofs MUST include RGE signature (RGE v3 §8.4.3).

---

## §3. Admission Protocol

### §3.1 Request Lifecycle
```
[Logos Core] → DRAC.evaluate(POP)
              ↓
    [Proof Validation] (via PXL Gate)
              ↓
    [Admissibility Decision]
              ↓
    ADMIT → [SOP Audit Log] → [Logos Core: Execute]
    DENY  → [SOP Audit Log] → [Logos Core: Halt]
```

### §3.2 Evaluation Stages
DRAC evaluation proceeds in three sequential stages:

**Stage 1: Structural Validation**
- POP schema conformance
- Axiom reference validity (CSP lookup)
- Context hash verification (RGE fingerprint match)
- **Exit:** DENY if structural validation fails

**Stage 2: Proof Verification**
- Delegate to PXL Gate (Logos Core §6)
- Await synchronous validation result
- **Exit:** DENY if proof invalid or PXL Gate timeout

**Stage 3: Admissibility Decision**
- If all validations pass: Issue ADMIT
- Generate decision packet for SOP audit spine
- Return decision to Logos Core
- **Exit:** ADMIT or DENY (no ambiguous states)

**Invariants:**
- **INV-EVAL-01:** Evaluation MUST proceed sequentially (no stage skipping).
- **INV-EVAL-02:** DENY at any stage MUST halt evaluation immediately.
- **INV-EVAL-03:** ADMIT decisions MUST complete all three stages.

### §3.3 Decision Packet Format
```
DecisionPacket := {
  request_id: UUID,
  decision: Enum[ADMIT, DENY],
  rationale: DenyReason | None,
  pxl_gate_validation_id: UUID | None,
  timestamp: ISO8601,
  drac_signature: Signature
}
```

**Invariants:**
- **INV-DEC-01:** DENY decisions MUST include rationale.
- **INV-DEC-02:** ADMIT decisions MUST include PXL Gate validation ID.
- **INV-DEC-03:** All decisions MUST be cryptographically signed by DRAC.

---

## §4. Fail-Closed Semantics

### §4.1 Default Denial Principle
DRAC operates under **deny-by-default**:
- Ambiguous proofs → DENY
- Timeout during validation → DENY
- Missing axiom references → DENY
- Corrupted context hash → DENY
- PXL Gate unavailable → DENY

**Invariants:**
- **INV-FC-01:** DRAC MUST NOT default to ADMIT under any failure condition.
- **INV-FC-02:** DRAC MUST NOT implement fallback reasoning paths.
- **INV-FC-03:** All failure modes MUST produce explicit DENY with rationale.

### §4.2 Error Propagation
DRAC errors propagate to:
1. **SOP Audit Spine:** Every DENY logged with full context
2. **Logos Core:** Execution halt signal
3. **Telemetry System:** Error classification and frequency metrics

**Invariants:**
- **INV-ERR-01:** Errors MUST NOT be silently suppressed.
- **INV-ERR-02:** DENY rationales MUST be sufficient for SOP root cause analysis.
- **INV-ERR-03:** Repeated DENY patterns MUST trigger SOP degradation ladder.

### §4.3 No Silent Failures
DRAC guarantees observability:
- Every evaluation produces a decision
- Every DENY includes machine-parseable rationale
- Every decision is logged to SOP audit spine before returning to Logos Core

**Invariants:**
- **INV-OBS-01:** DRAC MUST NOT return control without issuing a decision.
- **INV-OBS-02:** Decision logging MUST complete before decision transmission.
- **INV-OBS-03:** Logging failures MUST escalate to SOP emergency shutdown.

---

## §5. Integration Surfaces

### §5.1 Logos Core Integration
**Interface:** `DRAC.evaluate(POP) → DecisionPacket`

**Contract:**
- Logos Core invokes DRAC before executing any reasoning operation
- Logos Core provides POP with complete proof fragments
- Logos Core honors ADMIT/DENY verdicts (no override)

**Invariants:**
- **INV-LC-01:** Logos Core MUST NOT execute reasoning on DENY.
- **INV-LC-02:** Logos Core MUST route all reasoning requests through DRAC (no bypass).
- **INV-LC-03:** Logos Core MUST provide PXL Gate access to DRAC.

Cross-reference: Logos Core v1 §6 (PXL Gate), §11 (DRAC Integration)

### §5.2 SOP Integration
**Interface:** `DRAC → SOP.log_decision(DecisionPacket)`

**Contract:**
- DRAC sends every decision to SOP audit spine
- SOP hash-chains decisions into audit log
- SOP provides DENY frequency metrics to DRAC (feedback loop)

**Invariants:**
- **INV-SOP-01:** DRAC MUST log decisions before returning to Logos Core.
- **INV-SOP-02:** DRAC MUST NOT retry failed logging operations (escalate to SOP shutdown).
- **INV-SOP-03:** DRAC MUST participate in SOP audit integrity verification.

Cross-reference: SOP v1 §4 (Audit Spine), §10 (DRAC Integration)

### §5.3 RGE Integration
**Interface:** `RGE → DRAC (proof context provision)`

**Contract:**
- RGE supplies geometric/configuration proofs as proof fragments
- RGE signs proof fragments for authenticity verification
- DRAC validates RGE signatures before including in POP evaluation

**Invariants:**
- **INV-RGE-01:** DRAC MUST validate RGE signatures on all RGE-supplied proofs.
- **INV-RGE-02:** DRAC MUST reject unsigned or malformed RGE proofs.
- **INV-RGE-03:** DRAC MUST treat RGE proofs as advisory (not authoritative override).

Cross-reference: RGE v3 §8.4 (DRAC Integration Surface)

### §5.4 CSP Integration
**Interface:** `DRAC → CSP (axiom reference validation)`

**Contract:**
- DRAC queries CSP to validate axiom references in POP
- CSP provides canonical axiom definitions
- DRAC rejects POPs with invalid axiom references

**Invariants:**
- **INV-CSP-01:** DRAC MUST validate all axiom references before proof evaluation.
- **INV-CSP-02:** DRAC MUST reject POPs referencing undefined axioms.
- **INV-CSP-03:** DRAC MUST NOT cache axiom definitions (query CSP per-request).

Cross-reference: CSP v1 §3 (Semantic Axiom Management), §9 (DRAC Integration)

---

## §6. Telemetry & Observability

### §6.1 Decision Metrics
DRAC produces the following telemetry:
- **Admission Rate:** ADMIT decisions per tick
- **Denial Rate:** DENY decisions per tick
- **Denial Reasons:** Categorized by failure stage (structural, proof, timeout)
- **Evaluation Latency:** Time from POP receipt to decision emission

**Invariants:**
- **INV-TEL-01:** All metrics MUST be emitted to SOP telemetry backend.
- **INV-TEL-02:** Metrics MUST NOT contain proof fragment contents (privacy boundary).
- **INV-TEL-03:** Telemetry emission failures MUST NOT block decision processing.

### §6.2 Proof Validation Metrics
DRAC tracks PXL Gate performance:
- **Gate Validation Success Rate**
- **Gate Timeout Frequency**
- **Gate Validation Latency**

These metrics inform SOP degradation ladder thresholds.

**Invariants:**
- **INV-PVM-01:** Gate metrics MUST be aggregated per-tick.
- **INV-PVM-02:** Gate timeout patterns MUST trigger SOP alerts.
- **INV-PVM-03:** Gate metrics MUST be logged to SOP audit spine.

### §6.3 Audit Trail Compliance
Every DRAC decision is part of the SOP audit spine hash chain. DRAC ensures:
- Decision ordering is preserved
- Hash chain integrity is maintained
- Audit log is append-only (no retroactive modification)

**Invariants:**
- **INV-AUD-01:** DRAC MUST verify audit log hash before appending decision.
- **INV-AUD-02:** DRAC MUST escalate hash chain breaks to SOP emergency mode.
- **INV-AUD-03:** DRAC MUST NOT append decisions out of temporal order.

---

## §7. Governance Mode Compatibility

### §7.1 P1/P2 Mode Awareness
DRAC adapts to governance mode (P1 vs P2) as configured in Logos Core §14:

**P1 Mode (Strict):**
- All proof obligations enforced without relaxation
- DENY on any ambiguity
- Maximum audit verbosity

**P2 Mode (Relaxed Task Sources):**
- Same proof requirements as P1
- Task source constraint relaxed (Logos Core §14.2)
- DRAC proof evaluation unchanged

**Invariants:**
- **INV-GM-01:** DRAC proof gate MUST NOT relax in P2 mode.
- **INV-GM-02:** DRAC MUST query Logos Core for active governance mode per-tick.
- **INV-GM-03:** Mode transitions MUST trigger full DRAC re-initialization.

### §7.2 Mode Transition Protocol
When Logos Core signals governance mode change:
1. DRAC completes in-flight evaluations (no interruption)
2. DRAC flushes evaluation queue
3. DRAC re-initializes with new mode parameters
4. DRAC resumes operation

**Invariants:**
- **INV-MT-01:** Mode transitions MUST NOT corrupt in-flight decisions.
- **INV-MT-02:** Mode transitions MUST be logged to SOP audit spine.
- **INV-MT-03:** DRAC MUST reject new requests during mode transition.

---

## §8. Bootstrap & Initialization

### §8.1 Initialization Sequence
DRAC initializes during Logos Core Phase-G activation (Logos Core §5.2):

1. **Verify Upstream Dependencies:**
   - Logos Core PXL Gate accessible
   - SOP audit spine initialized
   - CSP axiom registry available
   - RGE signature verification keys loaded

2. **Load Configuration:**
   - Active governance mode (P1/P2)
   - PXL Gate timeout threshold
   - Audit spine endpoint

3. **Self-Test:**
   - Submit synthetic POP to PXL Gate
   - Verify SOP logging functional
   - Validate CSP axiom query path

4. **Signal Ready:**
   - Notify Logos Core DRAC available
   - Begin accepting evaluation requests

**Invariants:**
- **INV-INIT-01:** DRAC MUST NOT signal ready until all dependencies verified.
- **INV-INIT-02:** Self-test failure MUST trigger Logos Core bootstrap halt.
- **INV-INIT-03:** Initialization failures MUST be logged to SOP pre-init log.

### §8.2 Shutdown Protocol
DRAC shutdown occurs during Logos Core tick boundary (Logos Core §4.2):

1. Stop accepting new evaluation requests
2. Complete in-flight evaluations
3. Flush all pending decisions to SOP audit spine
4. Release PXL Gate connection
5. Signal shutdown complete to Logos Core

**Invariants:**
- **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight evaluations.
- **INV-SHUT-02:** Shutdown MUST guarantee all decisions logged before termination.
- **INV-SHUT-03:** Incomplete shutdown MUST trigger Logos Core emergency halt.

---

## §9. Invariant Summary

### Core Invariants
1. **INV-POP-01:** Every POP MUST reference at least one canonical axiom.
2. **INV-POP-02:** Proof fragments MUST be PXL-compliant.
3. **INV-POP-03:** Context hash MUST match RGE fingerprint.
4. **INV-GATE-01:** DRAC MUST NOT bypass PXL Gate.
5. **INV-GATE-02:** DRAC MUST NOT cache proof validation results.
6. **INV-GATE-03:** Every ADMIT MUST have PXL Gate validation record.
7. **INV-SRC-01:** DRAC MUST validate proof source authenticity.
8. **INV-SRC-02:** Untrusted proofs MUST trigger DENY.
9. **INV-SRC-03:** RGE proofs MUST include RGE signature.
10. **INV-EVAL-01:** Evaluation MUST proceed sequentially.
11. **INV-EVAL-02:** DENY at any stage MUST halt evaluation.
12. **INV-EVAL-03:** ADMIT MUST complete all three stages.
13. **INV-DEC-01:** DENY MUST include rationale.
14. **INV-DEC-02:** ADMIT MUST include PXL Gate validation ID.
15. **INV-DEC-03:** All decisions MUST be signed.
16. **INV-FC-01:** DRAC MUST NOT default to ADMIT on failure.
17. **INV-FC-02:** DRAC MUST NOT implement fallback reasoning.
18. **INV-FC-03:** All failures MUST produce explicit DENY.
19. **INV-ERR-01:** Errors MUST NOT be suppressed.
20. **INV-ERR-02:** DENY rationales MUST support root cause analysis.
21. **INV-ERR-03:** Repeated DENY MUST trigger degradation ladder.
22. **INV-OBS-01:** DRAC MUST NOT return without decision.
23. **INV-OBS-02:** Logging MUST complete before decision transmission.
24. **INV-OBS-03:** Logging failures MUST escalate to SOP shutdown.
25. **INV-LC-01:** Logos Core MUST NOT execute on DENY.
26. **INV-LC-02:** Logos Core MUST NOT bypass DRAC.
27. **INV-LC-03:** Logos Core MUST provide PXL Gate access.
28. **INV-SOP-01:** DRAC MUST log before returning decision.
29. **INV-SOP-02:** DRAC MUST NOT retry failed logging.
30. **INV-SOP-03:** DRAC MUST participate in audit integrity verification.
31. **INV-RGE-01:** DRAC MUST validate RGE signatures.
32. **INV-RGE-02:** DRAC MUST reject unsigned RGE proofs.
33. **INV-RGE-03:** DRAC MUST treat RGE proofs as advisory.
34. **INV-CSP-01:** DRAC MUST validate axiom references.
35. **INV-CSP-02:** DRAC MUST reject invalid axiom references.
36. **INV-CSP-03:** DRAC MUST NOT cache axiom definitions.
37. **INV-TEL-01:** Metrics MUST emit to SOP telemetry.
38. **INV-TEL-02:** Metrics MUST NOT contain proof contents.
39. **INV-TEL-03:** Telemetry failures MUST NOT block decisions.
40. **INV-PVM-01:** Gate metrics MUST aggregate per-tick.
41. **INV-PVM-02:** Gate timeouts MUST trigger SOP alerts.
42. **INV-PVM-03:** Gate metrics MUST log to SOP audit spine.
43. **INV-AUD-01:** DRAC MUST verify audit hash before append.
44. **INV-AUD-02:** DRAC MUST escalate hash chain breaks.
45. **INV-AUD-03:** DRAC MUST preserve temporal decision order.
46. **INV-GM-01:** Proof gate MUST NOT relax in P2 mode.
47. **INV-GM-02:** DRAC MUST query governance mode per-tick.
48. **INV-GM-03:** Mode transitions MUST trigger re-initialization.
49. **INV-MT-01:** Transitions MUST NOT corrupt in-flight decisions.
50. **INV-MT-02:** Transitions MUST log to SOP audit spine.
51. **INV-MT-03:** DRAC MUST reject requests during mode transition.
52. **INV-INIT-01:** DRAC MUST verify dependencies before ready signal.
53. **INV-INIT-02:** Self-test failure MUST halt bootstrap.
54. **INV-INIT-03:** Init failures MUST log to SOP pre-init log.
55. **INV-SHUT-01:** Shutdown MUST NOT terminate in-flight evals.
56. **INV-SHUT-02:** Shutdown MUST guarantee all decisions logged.
57. **INV-SHUT-03:** Incomplete shutdown MUST trigger emergency halt.

**Total Invariants:** 57

---

## §10. Cross-Reference Map

| External Subsystem | Referenced Sections | Integration Surface |
|--------------------|---------------------|---------------------|
| Logos Core v1 | §4.2, §5.2, §6, §11, §14 | PXL Gate, Phase-G, Governance Mode |
| SOP v1 | §4, §10 | Audit Spine, Telemetry Backend |
| CSP v1 | §3, §9 | Axiom Registry, Semantic Validation |
| RGE v3 | §8.4 | Proof Context, Signature Verification |

---

**End of Specification**

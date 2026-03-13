# DRAC Implementation Guide v1

**Paired Specification:** DRAC_Design_Specification_v1.md  
**Status:** Implementation Guide  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Purpose & Scope

This guide translates DRAC_Design_Specification_v1.md into concrete implementation obligations. Every section traces back to the originating design spec section. This is a **processable packet** for downstream implementation—no architectural ambiguity remains.

---

## §2. Module Structure

### §2.1 Primary Module
**Location:** `LOGOS_SYSTEM/operations_side/governance/drac/`

**Files:**
```
drac/
├── __init__.py                 # Module exports
├── controller.py               # DRACController class (§3)
├── proof_obligation.py         # ProofObligationPacket dataclass (§4)
├── decision.py                 # DecisionPacket dataclass (§5)
├── evaluator.py                # AdmissibilityEvaluator class (§6)
├── fail_closed.py              # FailClosedSemantics enforcement (§7)
├── integration/
│   ├── __init__.py
│   ├── logos_core.py          # Logos Core interface (§8)
│   ├── sop.py                 # SOP audit spine interface (§9)
│   ├── rge.py                 # RGE proof verification (§10)
│   └── csp.py                 # CSP axiom validation (§11)
├── telemetry.py               # Metrics emission (§12)
└── bootstrap.py               # Initialization sequence (§13)
```

**Derivation:** DRAC Spec §1.3 (Architectural Position), §5 (Integration Surfaces)

---

## §3. DRACController Class

**Source Spec:** DRAC Spec §3 (Admission Protocol)

### §3.1 Class Definition
```python
class DRACController:
    """
    Primary interface for reasoning admissibility evaluation.
    
    Authority: Evaluative only (Spec §1.4).
    Integration: Called by Logos Core per-reasoning-request (Spec §5.1).
    """
    
    def __init__(
        self,
        pxl_gate: PXLGateInterface,
        sop_client: SOPClient,
        csp_client: CSPClient,
        rge_verifier: RGEProofVerifier,
        governance_mode: GovernanceMode
    ):
        """
        Initialize DRAC controller.
        
        Args from Spec:
            pxl_gate: Logos Core PXL Gate interface (Spec §2.2, §5.1)
            sop_client: SOP audit spine client (Spec §5.2)
            csp_client: CSP axiom registry client (Spec §5.4)
            rge_verifier: RGE proof signature verifier (Spec §5.3)
            governance_mode: Active P1/P2 mode (Spec §7.1)
        
        Invariants: INV-INIT-01, INV-INIT-02
        """
        self._pxl_gate = pxl_gate
        self._sop_client = sop_client
        self._csp_client = csp_client
        self._rge_verifier = rge_verifier
        self._governance_mode = governance_mode
        self._evaluator = AdmissibilityEvaluator(...)  # §6
        self._is_operational = False
    
    def evaluate(self, pop: ProofObligationPacket) -> DecisionPacket:
        """
        Evaluate reasoning admissibility request.
        
        Workflow (Spec §3.1):
            1. Structural validation (Spec §3.2 Stage 1)
            2. Proof verification via PXL Gate (Spec §3.2 Stage 2)
            3. Issue ADMIT/DENY decision (Spec §3.2 Stage 3)
            4. Log to SOP audit spine (Spec §5.2, INV-SOP-01)
            5. Return decision to Logos Core
        
        Args:
            pop: Proof obligation packet (Spec §2.1)
        
        Returns:
            DecisionPacket with ADMIT or DENY verdict (Spec §3.3)
        
        Invariants:
            - INV-EVAL-01: Sequential stage execution
            - INV-EVAL-02: DENY halts immediately
            - INV-OBS-01: Must return decision
            - INV-OBS-02: Log before return
        """
        # Stage 1: Structural Validation
        structural_result = self._evaluator.validate_structure(pop)
        if not structural_result.valid:
            decision = self._create_deny_decision(
                pop.request_id,
                structural_result.rationale
            )
            self._log_decision(decision)  # INV-OBS-02
            return decision
        
        # Stage 2: Proof Verification
        pxl_result = self._pxl_gate.validate_proof(pop.proof_fragments)
        if not pxl_result.valid:
            decision = self._create_deny_decision(
                pop.request_id,
                pxl_result.rationale
            )
            self._log_decision(decision)
            return decision
        
        # Stage 3: Admissibility Decision
        decision = self._create_admit_decision(
            pop.request_id,
            pxl_result.validation_id
        )
        self._log_decision(decision)
        return decision
    
    def _log_decision(self, decision: DecisionPacket) -> None:
        """
        Log decision to SOP audit spine.
        
        Spec: §5.2, §6.3
        Invariants: INV-SOP-01, INV-SOP-02, INV-OBS-03
        """
        try:
            self._sop_client.log_decision(decision)
        except Exception as e:
            # INV-SOP-02: No retry, escalate to SOP shutdown
            raise DRACLoggingFailure(
                "Decision logging failed, escalating to SOP shutdown",
                original_exception=e
            )
```

**Key Implementation Notes:**
- No bypass paths (INV-LC-02)
- Fail-closed on any error (Spec §4)
- Synchronous SOP logging before return (INV-OBS-02)

---

## §4. ProofObligationPacket Dataclass

**Source Spec:** DRAC Spec §2.1

### §4.1 Class Definition
```python
@dataclass(frozen=True)
class ProofObligationPacket:
    """
    Reasoning request with embedded proof obligations.
    
    Spec: §2.1
    """
    request_id: UUID
    task_descriptor: TaskDescriptor
    axiom_references: List[AxiomID]
    proof_fragments: List[ProofFragment]
    context_hash: Hash
    timestamp: str  # ISO8601
    
    def __post_init__(self):
        """
        Validate invariants on construction.
        
        Invariants (Spec §2.1):
            - INV-POP-01: At least one axiom reference
            - INV-POP-02: Proof fragments PXL-compliant (delegated to PXL Gate)
            - INV-POP-03: Context hash matches RGE fingerprint (validated in evaluator)
        """
        if not self.axiom_references:
            raise InvalidPOPError("INV-POP-01: Must reference at least one axiom")
        
        if not self.proof_fragments:
            raise InvalidPOPError("Proof fragments required for evaluation")
        
        # Context hash validation delegated to evaluator (§6)
```

**Derivation:** Direct translation of Spec §2.1 POP structure.

---

## §5. DecisionPacket Dataclass

**Source Spec:** DRAC Spec §3.3

### §5.1 Class Definition
```python
class DecisionType(Enum):
    """Decision verdicts (Spec §3.3)."""
    ADMIT = "ADMIT"
    DENY = "DENY"

@dataclass(frozen=True)
class DecisionPacket:
    """
    DRAC admissibility decision.
    
    Spec: §3.3
    """
    request_id: UUID
    decision: DecisionType
    rationale: Optional[str]  # Required for DENY (INV-DEC-01)
    pxl_gate_validation_id: Optional[UUID]  # Required for ADMIT (INV-DEC-02)
    timestamp: str  # ISO8601
    drac_signature: Signature
    
    def __post_init__(self):
        """
        Validate decision packet invariants.
        
        Invariants (Spec §3.3):
            - INV-DEC-01: DENY must include rationale
            - INV-DEC-02: ADMIT must include PXL Gate validation ID
            - INV-DEC-03: All decisions must be signed
        """
        if self.decision == DecisionType.DENY and self.rationale is None:
            raise InvalidDecisionError("INV-DEC-01: DENY requires rationale")
        
        if self.decision == DecisionType.ADMIT and self.pxl_gate_validation_id is None:
            raise InvalidDecisionError("INV-DEC-02: ADMIT requires PXL Gate validation ID")
        
        if not self.drac_signature:
            raise InvalidDecisionError("INV-DEC-03: Decision must be signed")
```

**Derivation:** Direct translation of Spec §3.3 DecisionPacket structure.

---

## §6. AdmissibilityEvaluator Class

**Source Spec:** DRAC Spec §3.2 (Evaluation Stages)

### §6.1 Class Definition
```python
class AdmissibilityEvaluator:
    """
    Three-stage admissibility evaluation pipeline.
    
    Spec: §3.2
    Invariants: INV-EVAL-01, INV-EVAL-02, INV-EVAL-03
    """
    
    def __init__(
        self,
        csp_client: CSPClient,
        rge_verifier: RGEProofVerifier
    ):
        self._csp_client = csp_client
        self._rge_verifier = rge_verifier
    
    def validate_structure(self, pop: ProofObligationPacket) -> ValidationResult:
        """
        Stage 1: Structural validation.
        
        Spec: §3.2 Stage 1
        Checks:
            - POP schema conformance
            - Axiom reference validity (via CSP)
            - Context hash verification (via RGE)
            - Proof source authenticity (Spec §2.3)
        
        Invariants: INV-SRC-01, INV-CSP-01, INV-CSP-02
        """
        # Validate axiom references against CSP
        for axiom_id in pop.axiom_references:
            if not self._csp_client.axiom_exists(axiom_id):
                return ValidationResult(
                    valid=False,
                    rationale=f"INV-CSP-02: Undefined axiom {axiom_id}"
                )
        
        # Validate RGE-supplied proofs
        for fragment in pop.proof_fragments:
            if fragment.source == ProofSource.RGE:
                if not self._rge_verifier.verify_signature(fragment):
                    return ValidationResult(
                        valid=False,
                        rationale="INV-RGE-02: Unsigned RGE proof"
                    )
        
        # Verify context hash matches RGE fingerprint
        if not self._rge_verifier.verify_context_hash(pop.context_hash):
            return ValidationResult(
                valid=False,
                rationale="INV-POP-03: Context hash mismatch"
            )
        
        return ValidationResult(valid=True)
```

**Derivation:** Spec §3.2 Stage 1 validation checks translated to method logic.

---

## §7. FailClosedSemantics Module

**Source Spec:** DRAC Spec §4 (Fail-Closed Semantics)

### §7.1 Default Denial Handler
```python
class FailClosedHandler:
    """
    Enforce deny-by-default policy.
    
    Spec: §4.1
    Invariants: INV-FC-01, INV-FC-02, INV-FC-03
    """
    
    @staticmethod
    def handle_ambiguous_proof() -> DecisionPacket:
        """INV-FC-01: Ambiguous → DENY."""
        return DecisionPacket(
            decision=DecisionType.DENY,
            rationale="Ambiguous proof structure",
            ...
        )
    
    @staticmethod
    def handle_timeout() -> DecisionPacket:
        """INV-FC-01: Timeout → DENY."""
        return DecisionPacket(
            decision=DecisionType.DENY,
            rationale="PXL Gate validation timeout",
            ...
        )
    
    @staticmethod
    def handle_missing_axiom() -> DecisionPacket:
        """INV-FC-01: Missing axiom → DENY."""
        return DecisionPacket(
            decision=DecisionType.DENY,
            rationale="Axiom reference not found in CSP",
            ...
        )
    
    @staticmethod
    def handle_pxl_gate_unavailable() -> DecisionPacket:
        """INV-FC-01: PXL Gate down → DENY."""
        return DecisionPacket(
            decision=DecisionType.DENY,
            rationale="PXL Gate unavailable",
            ...
        )
```

**Derivation:** Spec §4.1 failure modes mapped to explicit DENY constructors.

---

## §8. Logos Core Integration

**Source Spec:** DRAC Spec §5.1

### §8.1 Interface Contract
```python
class LogosCoreInterface:
    """
    DRAC interface to Logos Core.
    
    Spec: §5.1
    Contract:
        - Logos Core invokes DRAC.evaluate() before reasoning execution
        - Logos Core honors ADMIT/DENY verdicts (no override)
        - Logos Core provides PXL Gate access to DRAC
    
    Invariants: INV-LC-01, INV-LC-02, INV-LC-03
    """
    
    def request_admissibility(
        self,
        task_descriptor: TaskDescriptor,
        proof_fragments: List[ProofFragment]
    ) -> DecisionPacket:
        """
        Called by Logos Core to evaluate reasoning admissibility.
        
        Spec: §5.1
        Flow:
            Logos Core → DRAC.evaluate(POP) → DecisionPacket
        
        Returns:
            DecisionPacket with ADMIT/DENY verdict
        
        Invariants:
            - INV-LC-02: No bypass (always routed through DRAC)
            - INV-LC-01: Logos Core must halt on DENY
        """
        pop = self._construct_pop(task_descriptor, proof_fragments)
        return self._drac_controller.evaluate(pop)
```

**Cross-Reference:** Logos Core v1 §11 (DRAC Integration)

---

## §9. SOP Integration

**Source Spec:** DRAC Spec §5.2

### §9.1 Audit Spine Client
```python
class SOPClient:
    """
    DRAC client for SOP audit spine.
    
    Spec: §5.2
    Contract:
        - DRAC logs every decision to SOP
        - SOP hash-chains decisions into audit log
        - No retry on logging failure (escalate)
    
    Invariants: INV-SOP-01, INV-SOP-02, INV-AUD-01
    """
    
    def log_decision(self, decision: DecisionPacket) -> None:
        """
        Append decision to SOP audit spine.
        
        Spec: §5.2, §6.3
        Pre-condition: Verify audit hash before append (INV-AUD-01)
        Post-condition: Decision logged, hash chain updated
        
        Raises:
            DRACLoggingFailure: On any logging error (INV-SOP-02)
        """
        # Verify audit log hash integrity before append
        current_hash = self._fetch_current_audit_hash()
        if not self._verify_hash_chain(current_hash):
            raise AuditHashChainBroken("INV-AUD-02: Hash chain integrity violated")
        
        # Append decision to audit spine
        try:
            self._append_to_audit_log(decision)
        except Exception as e:
            # INV-SOP-02: No retry, escalate
            raise DRACLoggingFailure(
                "Audit spine append failed, escalating to SOP shutdown"
            ) from e
```

**Cross-Reference:** SOP v1 §4 (Audit Spine), §10 (DRAC Integration)

---

## §10. RGE Integration

**Source Spec:** DRAC Spec §5.3

### §10.1 Proof Verifier
```python
class RGEProofVerifier:
    """
    RGE proof fragment signature verification.
    
    Spec: §5.3
    Invariants: INV-RGE-01, INV-RGE-02, INV-RGE-03
    """
    
    def verify_signature(self, proof_fragment: ProofFragment) -> bool:
        """
        Verify RGE signature on proof fragment.
        
        Spec: §5.3
        Invariants: INV-RGE-01, INV-RGE-02
        
        Returns:
            True if signature valid, False otherwise
        """
        if not proof_fragment.rge_signature:
            return False  # INV-RGE-02: Unsigned → reject
        
        # Cryptographic signature verification
        return self._crypto_verify(
            proof_fragment.content,
            proof_fragment.rge_signature
        )
    
    def verify_context_hash(self, context_hash: Hash) -> bool:
        """
        Verify context hash matches RGE fingerprint.
        
        Spec: §2.1 (INV-POP-03)
        """
        rge_fingerprint = self._fetch_rge_context_fingerprint()
        return context_hash == rge_fingerprint
```

**Cross-Reference:** RGE v3 §8.4 (DRAC Integration Surface)

---

## §11. CSP Integration

**Source Spec:** DRAC Spec §5.4

### §11.1 Axiom Registry Client
```python
class CSPClient:
    """
    DRAC client for CSP axiom registry.
    
    Spec: §5.4
    Contract:
        - DRAC queries CSP to validate axiom references
        - CSP provides canonical axiom definitions
        - No caching (per-request query)
    
    Invariants: INV-CSP-01, INV-CSP-02, INV-CSP-03
    """
    
    def axiom_exists(self, axiom_id: AxiomID) -> bool:
        """
        Check if axiom exists in CSP registry.
        
        Spec: §5.4
        Invariants:
            - INV-CSP-01: Validate before proof evaluation
            - INV-CSP-03: No caching (query per-request)
        
        Returns:
            True if axiom defined in CSP, False otherwise
        """
        # INV-CSP-03: Always query, never cache
        return self._query_csp_registry(axiom_id)
    
    def get_axiom_definition(self, axiom_id: AxiomID) -> AxiomDefinition:
        """
        Retrieve canonical axiom definition from CSP.
        
        Spec: §5.4
        
        Raises:
            UndefinedAxiomError: If axiom not in registry (INV-CSP-02)
        """
        definition = self._query_csp_registry_definition(axiom_id)
        if definition is None:
            raise UndefinedAxiomError(f"INV-CSP-02: Axiom {axiom_id} undefined")
        return definition
```

**Cross-Reference:** CSP v1 §3 (Semantic Axiom Management), §9 (DRAC Integration)

---

## §12. Telemetry Module

**Source Spec:** DRAC Spec §6 (Telemetry & Observability)

### §12.1 Metrics Emitter
```python
class DRACTelemetry:
    """
    DRAC telemetry and observability.
    
    Spec: §6
    Invariants: INV-TEL-01, INV-TEL-02, INV-TEL-03
    """
    
    def emit_decision_metrics(
        self,
        decision: DecisionPacket,
        evaluation_latency_ms: float
    ) -> None:
        """
        Emit decision metrics to SOP telemetry backend.
        
        Spec: §6.1
        Metrics:
            - Admission rate
            - Denial rate
            - Denial reason categorization
            - Evaluation latency
        
        Invariants:
            - INV-TEL-01: Emit to SOP telemetry backend
            - INV-TEL-02: No proof fragment contents in metrics
            - INV-TEL-03: Emission failure must not block decision
        """
        try:
            self._sop_telemetry.record({
                "decision_type": decision.decision.value,
                "evaluation_latency_ms": evaluation_latency_ms,
                "denial_reason_category": self._categorize_denial(decision.rationale),
                # INV-TEL-02: No proof contents included
            })
        except Exception as e:
            # INV-TEL-03: Log telemetry failure but continue
            logger.warning(f"Telemetry emission failed: {e}")
    
    def emit_pxl_gate_metrics(
        self,
        validation_success: bool,
        validation_latency_ms: float
    ) -> None:
        """
        Emit PXL Gate performance metrics.
        
        Spec: §6.2
        Invariants: INV-PVM-01, INV-PVM-02
        """
        self._aggregate_gate_metrics({
            "validation_success": validation_success,
            "latency_ms": validation_latency_ms
        })
        
        # INV-PVM-02: Alert SOP on timeout patterns
        if validation_latency_ms > TIMEOUT_THRESHOLD:
            self._sop_telemetry.alert("PXL Gate timeout pattern detected")
```

**Derivation:** Spec §6.1, §6.2 metrics definitions translated to emission methods.

---

## §13. Bootstrap Module

**Source Spec:** DRAC Spec §8 (Bootstrap & Initialization)

### §13.1 Initialization Sequence
```python
class DRACBootstrap:
    """
    DRAC initialization and shutdown orchestration.
    
    Spec: §8
    Invariants: INV-INIT-01, INV-INIT-02, INV-SHUT-01, INV-SHUT-02
    """
    
    def initialize(self) -> DRACController:
        """
        Initialize DRAC during Logos Core Phase-G.
        
        Spec: §8.1
        Sequence:
            1. Verify upstream dependencies
            2. Load configuration
            3. Self-test
            4. Signal ready to Logos Core
        
        Invariants:
            - INV-INIT-01: Verify deps before ready signal
            - INV-INIT-02: Self-test failure → bootstrap halt
        
        Returns:
            Initialized DRACController instance
        
        Raises:
            DRACBootstrapFailure: On initialization failure
        """
        # Step 1: Verify dependencies
        self._verify_pxl_gate_accessible()
        self._verify_sop_audit_spine_initialized()
        self._verify_csp_axiom_registry_available()
        self._verify_rge_signature_keys_loaded()
        
        # Step 2: Load configuration
        governance_mode = self._load_governance_mode()
        pxl_gate_timeout = self._load_pxl_gate_timeout()
        
        # Step 3: Self-test
        if not self._run_self_test():
            # INV-INIT-02: Self-test failure halts bootstrap
            raise DRACBootstrapFailure("Self-test failed, halting Logos Core bootstrap")
        
        # Step 4: Construct controller and signal ready
        controller = DRACController(...)
        controller._is_operational = True
        return controller
    
    def shutdown(self, controller: DRACController) -> None:
        """
        Shutdown DRAC at tick boundary.
        
        Spec: §8.2
        Sequence:
            1. Stop accepting new requests
            2. Complete in-flight evaluations
            3. Flush decisions to SOP
            4. Release PXL Gate connection
            5. Signal shutdown complete
        
        Invariants:
            - INV-SHUT-01: Complete in-flight evals
            - INV-SHUT-02: Guarantee all decisions logged
        """
        controller._is_operational = False  # Stop new requests
        controller._wait_for_inflight_evaluations()  # INV-SHUT-01
        controller._flush_pending_decisions()  # INV-SHUT-02
        controller._release_pxl_gate()
```

**Derivation:** Spec §8.1, §8.2 initialization/shutdown sequences mapped to orchestration methods.

---

## §14. Governance Mode Handling

**Source Spec:** DRAC Spec §7 (Governance Mode Compatibility)

### §14.1 Mode Adapter
```python
class GovernanceModeAdapter:
    """
    Adapt DRAC behavior to P1/P2 governance modes.
    
    Spec: §7
    Invariants: INV-GM-01, INV-GM-02, INV-GM-03
    """
    
    def query_active_mode(self, logos_core: LogosCoreInterface) -> GovernanceMode:
        """
        Query Logos Core for active governance mode.
        
        Spec: §7.1
        Invariant: INV-GM-02 (query per-tick)
        """
        return logos_core.get_governance_mode()
    
    def handle_mode_transition(
        self,
        controller: DRACController,
        new_mode: GovernanceMode
    ) -> None:
        """
        Handle governance mode transition.
        
        Spec: §7.2
        Protocol:
            1. Complete in-flight evaluations
            2. Flush evaluation queue
            3. Re-initialize with new mode
            4. Resume operation
        
        Invariants:
            - INV-MT-01: No corruption of in-flight decisions
            - INV-MT-02: Log transition to SOP
            - INV-MT-03: Reject new requests during transition
        """
        controller._is_operational = False  # INV-MT-03
        controller._complete_inflight_evaluations()  # INV-MT-01
        controller._flush_evaluation_queue()
        
        # Log transition to SOP
        self._sop_client.log_governance_transition(new_mode)  # INV-MT-02
        
        # Re-initialize
        controller._governance_mode = new_mode
        controller._evaluator.reconfigure(new_mode)
        controller._is_operational = True
```

**Derivation:** Spec §7.1, §7.2 mode handling protocols translated to adapter methods.

---

## §15. Implementation Checklist

### §15.1 Core Components
- [ ] DRACController class (§3)
- [ ] ProofObligationPacket dataclass (§4)
- [ ] DecisionPacket dataclass (§5)
- [ ] AdmissibilityEvaluator class (§6)
- [ ] FailClosedHandler class (§7)

### §15.2 Integration Interfaces
- [ ] LogosCoreInterface (§8)
- [ ] SOPClient (§9)
- [ ] RGEProofVerifier (§10)
- [ ] CSPClient (§11)

### §15.3 Supporting Modules
- [ ] DRACTelemetry (§12)
- [ ] DRACBootstrap (§13)
- [ ] GovernanceModeAdapter (§14)

### §15.4 Invariant Enforcement
- [ ] All 57 invariants implemented as runtime checks
- [ ] Invariant violation triggers appropriate failure mode
- [ ] Fail-closed semantics verified across all code paths

### §15.5 Cross-Subsystem Contracts
- [ ] Logos Core integration tested (PXL Gate, Phase-G)
- [ ] SOP audit spine logging functional
- [ ] CSP axiom validation operational
- [ ] RGE proof verification integrated

---

## §16. Integration Test Targets

**Derivation:** Spec §5 (Integration Surfaces)

### §16.1 Logos Core Integration
- PXL Gate validation roundtrip
- Phase-G initialization handshake
- ADMIT/DENY verdict enforcement
- Governance mode query

### §16.2 SOP Integration
- Decision logging to audit spine
- Hash chain verification
- Telemetry backend emission
- Logging failure escalation

### §16.3 RGE Integration
- Proof signature verification
- Context hash validation
- Unsigned proof rejection

### §16.4 CSP Integration
- Axiom existence validation
- Axiom definition retrieval
- Invalid axiom reference handling

---

**End of Implementation Guide**

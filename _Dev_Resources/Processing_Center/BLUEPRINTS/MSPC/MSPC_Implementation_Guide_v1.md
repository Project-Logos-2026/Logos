# MSPC Implementation Guide v1

**Paired Specification:** MSPC_Design_Specification_v1.md  
**Status:** Implementation Guide  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Purpose & Scope

This guide translates MSPC_Design_Specification_v1.md into concrete implementation obligations. Every section traces back to the originating design spec section. This is a **processable packet** for downstream implementation—no architectural ambiguity remains.

---

## §2. Module Structure

### §2.1 Primary Module
**Location:** `LOGOS_SYSTEM/operations_side/governance/mspc/`

**Files:**
```
mspc/
├── __init__.py                      # Module exports
├── controller.py                    # MSPCController class (§3)
├── manifest/
│   ├── __init__.py
│   ├── smp.py                      # SMP dataclass (§4)
│   ├── smp_entry.py                # SMPEntry dataclass (§5)
│   ├── versioning.py               # SMP versioning (§6)
│   └── snapshot.py                 # SMP snapshot management (§7)
├── pipeline/
│   ├── __init__.py
│   ├── orchestrator.py             # Projection pipeline orchestrator (§8)
│   ├── request.py                  # ProjectionRequest dataclass (§9)
│   ├── state_machine.py            # Projection state transitions (§10)
│   └── validation.py               # Projection validation (§11)
├── governance/
│   ├── __init__.py
│   ├── admissibility.py            # Admissibility rules (§12)
│   └── denial.py                   # Projection denial protocol (§13)
├── integrity/
│   ├── __init__.py
│   ├── hash_chain.py               # SMP hash chain management (§14)
│   └── verification.py             # Integrity verification (§15)
├── integration/
│   ├── __init__.py
│   ├── emp.py                      # EMP interface (§16)
│   ├── csp.py                      # CSP interface (§17)
│   ├── sop.py                      # SOP audit spine interface (§18)
│   └── logos_core.py               # Logos Core interface (§19)
├── telemetry.py                    # Metrics emission (§20)
└── bootstrap.py                    # Initialization sequence (§21)
```

**Derivation:** MSPC Spec §1.3 (Architectural Position), §6 (Integration Surfaces)

---

## §3. MSPCController Class

**Source Spec:** MSPC Spec §3 (Projection Pipeline Architecture)

### §3.1 Class Definition
```python
class MSPCController:
    """
    Primary interface for semantic projection management.
    
    Authority: Orchestrative only (Spec §1.4).
    Domain: Projection governance, not semantic reasoning.
    Integration: Called by Logos Core for SMP access, by CSP for projections.
    """
    
    def __init__(
        self,
        emp_client: EMPClient,
        csp_client: CSPClient,
        sop_client: SOPClient,
        smp: SemanticProjectionManifest,
        governance_mode: GovernanceMode
    ):
        """
        Initialize MSPC controller.
        
        Args from Spec:
            emp_client: EMP hash chain and AA access (Spec §6.1)
            csp_client: CSP semantic validation (Spec §6.2)
            sop_client: SOP audit spine (Spec §6.3)
            smp: Semantic Projection Manifest (Spec §2)
            governance_mode: Active P1/P2 mode (Spec §7.1)
        
        Invariants: INV-INIT-01, INV-INIT-02
        """
        self._emp_client = emp_client
        self._csp_client = csp_client
        self._sop_client = sop_client
        self._smp = smp
        self._governance_mode = governance_mode
        self._pipeline_orchestrator = ProjectionPipelineOrchestrator(...)
        self._is_operational = False
    
    def request_projection(
        self,
        projection_request: ProjectionRequest
    ) -> UUID:
        """
        Initiate projection from AA to SMP.
        
        Workflow (Spec §3.1):
            Tick 1: Validate request, stage projection
            Tick 2-N: CSP semantic validation (async)
            Tick N+1: Hash chain integration via EMP
            Tick N+2: Activate projection in SMP
        
        Args:
            projection_request: Projection request packet (Spec §3.2)
        
        Returns:
            request_id for tracking projection progress
        
        Invariants:
            - INV-REQ-03: Log request before processing
            - INV-PIPE-01: Multi-tick pipeline (no single-tick)
            - INV-ADMIT-01: All admissibility rules must pass
        """
        # INV-REQ-03: Log request to SOP
        self._sop_client.log_projection_request(projection_request)
        
        # Validate admissibility (Spec §4.1)
        if not self._validate_admissibility(projection_request):
            denial = self._create_denial(projection_request)
            self._sop_client.log_projection_denial(denial)
            raise ProjectionDeniedError(denial.denial_reason)
        
        # Stage projection and initiate pipeline
        self._pipeline_orchestrator.initiate_projection(projection_request)
        
        return projection_request.request_id
    
    def get_active_projections(self) -> List[SMPEntry]:
        """
        Retrieve Active-tier SMP entries for Logos Core.
        
        Spec: §2.2, §6.4
        Invariants:
            - INV-TIER-01: Only Active projections served
            - INV-LC-03: Verify SMP integrity before serving
        """
        # INV-LC-03: Verify integrity
        if not self._verify_smp_integrity():
            self._sop_client.alert_integrity_failure()
            raise SMPIntegrityError("SMP hash chain verification failed")
        
        # INV-TIER-01: Filter Active tier only
        return [
            entry for entry in self._smp.projections
            if entry.projection_tier == ProjectionTier.ACTIVE
        ]
```

**Key Implementation Notes:**
- Multi-tick pipeline (INV-PIPE-01)
- Fail-closed on admissibility (INV-ADMIT-01)
- Only Active-tier projections served (INV-TIER-01)

---

## §4. SemanticProjectionManifest Dataclass

**Source Spec:** MSPC Spec §2.1

### §4.1 Class Definition
```python
@dataclass
class SemanticProjectionManifest:
    """
    SMP structure with versioning and hash chain.
    
    Spec: §2.1
    """
    manifest_version: str  # Semantic versioning
    manifest_hash: Hash
    genesis_hash: Hash
    projections: List[SMPEntry]
    metadata: ManifestMetadata
    
    def __post_init__(self):
        """
        Validate SMP invariants.
        
        Invariants (Spec §2.1):
            - INV-SMP-01: Maintain hash chain from genesis
            - INV-SMP-02: Every entry references canonical AA
            - INV-SMP-04: Updates atomic and versioned
        """
        if not self.projections:
            # Empty SMP valid at bootstrap
            return
        
        # Verify all entries reference canonical AAs (INV-SMP-02)
        for entry in self.projections:
            if not entry.axiom_id:
                raise InvalidSMPError("INV-SMP-02: Entry missing axiom_id")
        
        # Hash chain verification delegated to integrity module (§14)
```

**Derivation:** Direct translation of Spec §2.1 SMP structure.

---

## §5. SMPEntry Dataclass

**Source Spec:** MSPC Spec §2.1

### §5.1 Class Definition
```python
class ProjectionTier(Enum):
    """Projection operational tiers (Spec §2.2)."""
    ACTIVE = "ACTIVE"
    STAGED = "STAGED"
    DEPRECATED = "DEPRECATED"

@dataclass(frozen=True)
class SMPEntry:
    """
    SMP projection entry.
    
    Spec: §2.1
    """
    entry_id: str  # EntryID
    axiom_id: str  # AxiomID
    projection_context: str  # ContextDescriptor
    projection_hash: Hash
    parent_aa_hash: Hash
    created_at: str  # ISO8601
    projection_tier: ProjectionTier
    
    def __post_init__(self):
        """
        Validate SMP entry invariants.
        
        Invariants (Spec §2.1):
            - INV-SMP-02: Reference canonical AA
            - INV-SMP-03: projection_hash derives from parent_aa_hash
        """
        if not self.axiom_id:
            raise InvalidSMPEntryError("INV-SMP-02: axiom_id required")
        
        # Hash derivation validated by hash chain manager (§14)
```

**Derivation:** Direct translation of Spec §2.1 SMPEntry structure.

---

## §6. SMP Versioning Module

**Source Spec:** MSPC Spec §2.3

### §6.1 Versioning Manager
```python
class SMPVersionManager:
    """
    Semantic versioning for SMP.
    
    Spec: §2.3
    Invariants: INV-VER-01, INV-VER-02, INV-VER-03
    """
    
    def __init__(self, sop_client: SOPClient):
        self._sop_client = sop_client
        self._version_history: List[str] = []
    
    def increment_version(
        self,
        current_version: str,
        change_type: Enum[Major, Minor, Patch]
    ) -> str:
        """
        Increment SMP version semantically.
        
        Spec: §2.3
        Invariants:
            - INV-VER-01: Version must increment on modification
            - INV-VER-02: Log version increment to SOP
        """
        major, minor, patch = map(int, current_version.split('.'))
        
        if change_type == ChangeType.MAJOR:
            new_version = f"{major + 1}.0.0"
        elif change_type == ChangeType.MINOR:
            new_version = f"{major}.{minor + 1}.0"
        else:  # PATCH
            new_version = f"{major}.{minor}.{patch + 1}"
        
        # INV-VER-02: Log to SOP
        self._sop_client.log_version_increment(current_version, new_version)
        
        # INV-VER-03: Preserve history
        self._version_history.append(current_version)
        
        return new_version
```

**Derivation:** Spec §2.3 versioning rules mapped to increment logic.

---

## §7. SMP Snapshot Module

**Source Spec:** MSPC Spec §5.3

### §7.1 Snapshot Manager
```python
@dataclass(frozen=True)
class SMPSnapshot:
    """SMP snapshot for audit (Spec §5.3)."""
    snapshot_id: UUID
    smp_version: str
    manifest_hash: Hash
    created_at: str  # ISO8601
    projection_count: int

class SMPSnapshotManager:
    """
    SMP snapshot governance.
    
    Spec: §5.3
    Invariants: INV-SNAP-01, INV-SNAP-02, INV-SNAP-03
    """
    
    def create_snapshot(
        self,
        smp: SemanticProjectionManifest
    ) -> SMPSnapshot:
        """
        Create immutable SMP snapshot.
        
        Spec: §5.3
        Invariants:
            - INV-SNAP-01: Snapshots immutable once created
            - INV-SNAP-02: Snapshot hash must match SMP state
            - INV-SNAP-03: Log snapshot to SOP
        """
        snapshot = SMPSnapshot(
            snapshot_id=uuid4(),
            smp_version=smp.manifest_version,
            manifest_hash=smp.manifest_hash,
            created_at=datetime.utcnow().isoformat(),
            projection_count=len(smp.projections)
        )
        
        # INV-SNAP-02: Verify hash match
        if snapshot.manifest_hash != smp.manifest_hash:
            raise SnapshotHashMismatch("Snapshot hash does not match SMP")
        
        # INV-SNAP-03: Log to SOP
        self._sop_client.log_smp_snapshot(snapshot)
        
        return snapshot  # INV-SNAP-01: Frozen dataclass ensures immutability
```

**Derivation:** Spec §5.3 snapshot structure and governance mapped to manager methods.

---

## §8. Projection Pipeline Orchestrator

**Source Spec:** MSPC Spec §3.1

### §8.1 Orchestrator Class
```python
class ProjectionPipelineOrchestrator:
    """
    Multi-tick projection pipeline orchestration.
    
    Spec: §3.1
    Invariants: INV-PIPE-01, INV-PIPE-02, INV-PIPE-03
    """
    
    def __init__(
        self,
        csp_client: CSPClient,
        emp_client: EMPClient,
        sop_client: SOPClient
    ):
        self._csp_client = csp_client
        self._emp_client = emp_client
        self._sop_client = sop_client
        self._active_projections: Dict[UUID, ProjectionState] = {}
    
    def initiate_projection(
        self,
        request: ProjectionRequest
    ) -> None:
        """
        Initiate multi-tick projection pipeline.
        
        Spec: §3.1 Tick 1
        Invariant: INV-PIPE-01 (multi-tick pipeline)
        """
        # Create initial state
        state = ProjectionState(
            request_id=request.request_id,
            current_state=StateEnum.REQUESTED,
            axiom_id=request.axiom_id,
            projection_context=request.projection_context
        )
        
        self._active_projections[request.request_id] = state
        
        # Initiate CSP validation (async)
        self._csp_client.request_validation_async(
            request.axiom_id,
            request.projection_context,
            callback=self._handle_csp_validation
        )
    
    def _handle_csp_validation(
        self,
        request_id: UUID,
        validation_result: ValidationResult
    ) -> None:
        """
        Handle CSP validation result.
        
        Spec: §3.1 Tick N+1
        Invariants: INV-PIPE-02, INV-PIPE-03
        """
        state = self._active_projections[request_id]
        
        if validation_result.passed:
            # INV-PIPE-02: Validation complete, proceed to hash-chaining
            self._transition_to_hash_chaining(state)
        else:
            # INV-PIPE-03: Failed validation, do not enter SMP
            self._transition_to_failed(state, validation_result.rationale)
```

**Derivation:** Spec §3.1 multi-tick workflow mapped to orchestrator methods.

---

## §9. ProjectionRequest Dataclass

**Source Spec:** MSPC Spec §3.2

### §9.1 Class Definition
```python
class RequesterType(Enum):
    """Projection requester types (Spec §3.2)."""
    LOGOS_CORE = "LOGOS_CORE"
    CSP = "CSP"
    MANUAL = "MANUAL"

@dataclass(frozen=True)
class ProjectionRequest:
    """
    Projection request packet.
    
    Spec: §3.2
    """
    request_id: UUID
    axiom_id: str  # AxiomID
    projection_context: str  # ContextDescriptor
    requester: RequesterType
    governance_override: bool
    
    def __post_init__(self):
        """
        Validate projection request invariants.
        
        Invariants (Spec §3.2):
            - INV-REQ-01: Reference canonical AA
            - INV-REQ-02: governance_override requires P2 mode
        """
        if not self.axiom_id:
            raise InvalidProjectionRequestError("INV-REQ-01: axiom_id required")
        
        # INV-REQ-02: governance_override validation done by controller (§3)
```

**Derivation:** Direct translation of Spec §3.2 ProjectionRequest structure.

---

## §10. Projection State Machine

**Source Spec:** MSPC Spec §3.3

### §10.1 State Machine Implementation
```python
class StateEnum(Enum):
    """Projection lifecycle states (Spec §3.3)."""
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    HASH_CHAINING = "HASH_CHAINING"
    STAGED = "STAGED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    FAILED = "FAILED"

@dataclass
class ProjectionState:
    """Projection state tracking."""
    request_id: UUID
    current_state: StateEnum
    axiom_id: str
    projection_context: str
    state_history: List[Tuple[StateEnum, str]] = field(default_factory=list)

class ProjectionStateMachine:
    """
    Projection state transitions.
    
    Spec: §3.3
    Invariants: INV-STATE-01, INV-STATE-02, INV-STATE-03
    """
    
    def transition(
        self,
        state: ProjectionState,
        new_state: StateEnum
    ) -> ProjectionState:
        """
        Execute state transition.
        
        Spec: §3.3
        Invariants:
            - INV-STATE-01: Unidirectional transitions
            - INV-STATE-03: Atomic transitions
        """
        # INV-STATE-01: Validate transition is valid
        if not self._is_valid_transition(state.current_state, new_state):
            raise InvalidStateTransition(
                f"Cannot transition from {state.current_state} to {new_state}"
            )
        
        # Record state history
        state.state_history.append((state.current_state, datetime.utcnow().isoformat()))
        
        # Atomic update (INV-STATE-03)
        state.current_state = new_state
        
        # INV-STATE-02: Log FAILED state to SOP
        if new_state == StateEnum.FAILED:
            self._sop_client.log_projection_failure(state.request_id)
        
        return state
```

**Derivation:** Spec §3.3 state transitions mapped to state machine logic.

---

## §11. Projection Validation Module

**Source Spec:** MSPC Spec §4.3

### §11.1 Validation Orchestrator
```python
class ProjectionValidator:
    """
    Projection context validation delegation.
    
    Spec: §4.3
    Invariants: INV-CTX-01, INV-CTX-02, INV-CTX-03
    """
    
    def __init__(
        self,
        csp_client: CSPClient,
        timeout_seconds: int = 30
    ):
        self._csp_client = csp_client
        self._timeout_seconds = timeout_seconds
    
    def validate_context(
        self,
        axiom_id: str,
        projection_context: str
    ) -> ValidationResult:
        """
        Delegate context validation to CSP.
        
        Spec: §4.3
        Invariants:
            - INV-CTX-01: Cannot override CSP verdict
            - INV-CTX-02: Validation before hash-chaining
            - INV-CTX-03: Timeout triggers failure
        """
        try:
            # Delegate to CSP with timeout
            result = self._csp_client.validate_projection_context(
                axiom_id,
                projection_context,
                timeout=self._timeout_seconds
            )
            
            # INV-CTX-01: Return CSP verdict as-is (no override)
            return result
        except ValidationTimeoutError:
            # INV-CTX-03: Timeout triggers projection failure
            return ValidationResult(
                passed=False,
                rationale="CSP validation timeout"
            )
```

**Derivation:** Spec §4.3 context validation protocol mapped to validator methods.

---

## §12. Admissibility Rules Module

**Source Spec:** MSPC Spec §4.1

### §12.1 Admissibility Checker
```python
class AdmissibilityChecker:
    """
    Projection admissibility rule enforcement.
    
    Spec: §4.1
    Invariants: INV-ADMIT-01, INV-ADMIT-02, INV-ADMIT-03
    """
    
    def __init__(
        self,
        emp_client: EMPClient,
        smp: SemanticProjectionManifest,
        governance_mode: GovernanceMode
    ):
        self._emp_client = emp_client
        self._smp = smp
        self._governance_mode = governance_mode
    
    def check_admissibility(
        self,
        request: ProjectionRequest
    ) -> AdmissibilityResult:
        """
        Validate projection admissibility.
        
        Spec: §4.1 Rules
        Invariants:
            - INV-ADMIT-01: All rules must pass
            - INV-ADMIT-02: Violations trigger denial
        """
        # Rule 1: AA Existence
        if not self._emp_client.axiom_exists(request.axiom_id):
            return AdmissibilityResult(
                passed=False,
                failed_rule="AA_EXISTENCE",
                rationale=f"Axiom {request.axiom_id} not found in EMP"
            )
        
        # Rule 2: AA Integrity
        if not self._emp_client.verify_axiom_integrity(request.axiom_id):
            return AdmissibilityResult(
                passed=False,
                failed_rule="AA_INTEGRITY",
                rationale="Axiom hash verification failed"
            )
        
        # Rule 4: No Duplication
        if self._is_duplicate_projection(request):
            return AdmissibilityResult(
                passed=False,
                failed_rule="NO_DUPLICATION",
                rationale="Projection already exists in SMP"
            )
        
        # Rule 5: Governance Mode
        if request.governance_override and self._governance_mode == GovernanceMode.P1:
            return AdmissibilityResult(
                passed=False,
                failed_rule="GOVERNANCE_MODE",
                rationale="governance_override not permitted in P1 mode"
            )
        
        # INV-ADMIT-01: All rules passed
        return AdmissibilityResult(passed=True)
```

**Derivation:** Spec §4.1 admissibility rules mapped to checker methods.

---

## §13. Projection Denial Module

**Source Spec:** MSPC Spec §4.2

### §13.1 Denial Protocol
```python
@dataclass(frozen=True)
class ProjectionDenial:
    """Projection denial record (Spec §4.2)."""
    request_id: UUID
    denial_reason: str
    failed_rule: str
    timestamp: str  # ISO8601

class ProjectionDenialProtocol:
    """
    Projection denial handling.
    
    Spec: §4.2
    Invariants: INV-DENY-01, INV-DENY-02, INV-DENY-03
    """
    
    def __init__(self, sop_client: SOPClient):
        self._sop_client = sop_client
        self._denial_counter: Dict[str, int] = {}
    
    def deny_projection(
        self,
        request: ProjectionRequest,
        admissibility_result: AdmissibilityResult
    ) -> ProjectionDenial:
        """
        Execute projection denial protocol.
        
        Spec: §4.2
        Invariants:
            - INV-DENY-01: Include explicit rationale
            - INV-DENY-02: Log to SOP before return
            - INV-DENY-03: Alert on repeated denials
        """
        # INV-DENY-01: Construct denial with rationale
        denial = ProjectionDenial(
            request_id=request.request_id,
            denial_reason=admissibility_result.rationale,
            failed_rule=admissibility_result.failed_rule,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # INV-DENY-02: Log to SOP before return
        self._sop_client.log_projection_denial(denial)
        
        # INV-DENY-03: Track denial frequency
        self._denial_counter[denial.failed_rule] = \
            self._denial_counter.get(denial.failed_rule, 0) + 1
        
        if self._denial_counter[denial.failed_rule] > REPEATED_DENIAL_THRESHOLD:
            self._sop_client.alert_repeated_denials(denial.failed_rule)
        
        return denial
```

**Derivation:** Spec §4.2 denial protocol mapped to handler methods.

---

## §14. SMP Hash Chain Manager

**Source Spec:** MSPC Spec §5.1

### §14.1 Hash Chain Manager
```python
class SMPHashChainManager:
    """
    SMP hash chain management.
    
    Spec: §5.1
    Invariants: INV-HASH-01, INV-HASH-02, INV-HASH-03
    """
    
    def __init__(
        self,
        emp_client: EMPClient,
        genesis_hash: Hash
    ):
        self._emp_client = emp_client
        self._genesis_hash = genesis_hash
        self._smp_chain: List[Hash] = [genesis_hash]
    
    def compute_projection_hash(
        self,
        projection_context: str,
        parent_aa_hash: Hash
    ) -> Hash:
        """
        Compute SMP projection hash.
        
        Spec: §5.1
        Formula: SMP_hash_n = H(projection_context || SMP_hash_{n-1} || AA_parent.hash)
        
        Invariants: INV-HASH-01, INV-HASH-02
        """
        previous_smp_hash = self._smp_chain[-1]
        
        # Compute hash chaining to both previous SMP and parent AA
        projection_hash = hashlib.sha256(
            f"{projection_context}{previous_smp_hash}{parent_aa_hash}".encode()
        ).hexdigest()
        
        # Append to chain
        self._smp_chain.append(projection_hash)
        
        return projection_hash
    
    def verify_projection_hash(
        self,
        entry: SMPEntry
    ) -> bool:
        """
        Verify SMP projection hash.
        
        Spec: §5.1
        Invariant: INV-HASH-03 (detect chain breaks)
        """
        if entry.projection_hash not in self._smp_chain:
            return False  # Chain break detected
        
        # Recompute and verify
        index = self._smp_chain.index(entry.projection_hash)
        previous_hash = self._smp_chain[index - 1]
        
        recomputed = hashlib.sha256(
            f"{entry.projection_context}{previous_hash}{entry.parent_aa_hash}".encode()
        ).hexdigest()
        
        return recomputed == entry.projection_hash
```

**Derivation:** Spec §5.1 hash chain formula mapped to manager methods.

---

## §15. Integrity Verification Module

**Source Spec:** MSPC Spec §5.2

### §15.1 Verification Orchestrator
```python
class SMPIntegrityVerifier:
    """
    SMP integrity verification.
    
    Spec: §5.2
    Invariants: INV-VERIFY-01, INV-VERIFY-02, INV-VERIFY-03
    """
    
    def __init__(
        self,
        hash_chain: SMPHashChainManager,
        sop_client: SOPClient
    ):
        self._hash_chain = hash_chain
        self._sop_client = sop_client
    
    def verify_full_smp(
        self,
        smp: SemanticProjectionManifest
    ) -> bool:
        """
        Verify complete SMP integrity.
        
        Spec: §5.2
        Invariants:
            - INV-VERIFY-01: Recompute hash chain
            - INV-VERIFY-02: Escalate breaks to SOP
            - INV-VERIFY-03: Log results to SOP
        """
        try:
            # INV-VERIFY-01: Recompute full chain
            chain_valid = all(
                self._hash_chain.verify_projection_hash(entry)
                for entry in smp.projections
            )
            
            # INV-VERIFY-03: Log results
            self._sop_client.log_smp_verification(chain_valid)
            
            if not chain_valid:
                # INV-VERIFY-02: Escalate to SOP emergency mode
                self._sop_client.trigger_emergency_mode("SMP hash chain break detected")
            
            return chain_valid
        except Exception as e:
            self._sop_client.trigger_emergency_mode(f"SMP verification failed: {e}")
            return False
```

**Derivation:** Spec §5.2 verification procedures mapped to orchestrator methods.

---

## §16. EMP Integration

**Source Spec:** MSPC Spec §6.1

### §16.1 EMP Client
```python
class EMPClient:
    """
    MSPC client for EMP integration.
    
    Spec: §6.1
    Contract:
        - MSPC accesses AAs via EMP
        - MSPC uses EMP for hash-chaining
        - MSPC honors EMP deprecation flags
    
    Invariants: INV-EMP-01, INV-EMP-02, INV-EMP-03
    """
    
    def retrieve_axiom_for_projection(
        self,
        axiom_id: str
    ) -> AtomicAxiom:
        """
        Retrieve AA for projection.
        
        Spec: §6.1
        Invariants:
            - INV-EMP-01: Access via EMP, not CSP
            - INV-EMP-03: Honor deprecation flags
        """
        # INV-EMP-01: Route through EMP
        aa = self._emp_controller.retrieve_axiom(axiom_id)
        
        # INV-EMP-03: Check deprecation
        if self._is_deprecated(aa):
            raise AxiomDeprecatedError(
                f"Axiom {axiom_id} is deprecated, cannot project"
            )
        
        return aa
    
    def append_to_smp_hash_chain(
        self,
        projection_context: str,
        parent_aa_hash: Hash
    ) -> Hash:
        """
        Delegate SMP hash-chaining to EMP.
        
        Spec: §6.1
        Invariant: INV-EMP-02
        """
        # INV-EMP-02: Use EMP for hash-chaining
        return self._emp_hash_chain.append_smp_projection(
            projection_context,
            parent_aa_hash
        )
```

**Cross-Reference:** EMP v1 §6.4 (SMP Integration)

---

## §17. CSP Integration

**Source Spec:** MSPC Spec §6.2

### §17.1 CSP Client
```python
class CSPClient:
    """
    MSPC client for CSP semantic validation.
    
    Spec: §6.2
    Contract:
        - MSPC delegates context validation to CSP
        - CSP validates semantic coherence
        - Async validation with timeout
    
    Invariants: INV-CSP-01, INV-CSP-02, INV-CSP-03
    """
    
    def validate_projection_context(
        self,
        axiom_id: str,
        projection_context: str,
        timeout: int
    ) -> ValidationResult:
        """
        Delegate projection context validation to CSP.
        
        Spec: §6.2
        Invariants:
            - INV-CSP-01: Delegate validation to CSP
            - INV-CSP-02: Cannot override CSP verdict
            - INV-CSP-03: Handle timeouts gracefully
        """
        try:
            # INV-CSP-01: Delegate to CSP
            result = self._query_csp_validation(
                axiom_id,
                projection_context,
                timeout=timeout
            )
            
            # INV-CSP-02: Return CSP verdict unchanged
            return result
        except TimeoutError:
            # INV-CSP-03: Graceful timeout handling
            return ValidationResult(
                passed=False,
                rationale="CSP validation timeout exceeded"
            )
```

**Cross-Reference:** CSP v1 §4 (Semantic Validation), §11 (MSPC Integration)

---

## §18. SOP Integration

**Source Spec:** MSPC Spec §6.3

### §18.1 SOP Client
```python
class SOPClient:
    """
    MSPC client for SOP audit spine.
    
    Spec: §6.3
    Invariants: INV-SOP-01, INV-SOP-02, INV-SOP-03
    """
    
    def log_projection_request(
        self,
        request: ProjectionRequest
    ) -> None:
        """
        Log projection request to SOP.
        
        Spec: §6.3
        Invariant: INV-SOP-01
        """
        self._append_audit_event({
            "event_type": "PROJECTION_REQUEST",
            "request_id": str(request.request_id),
            "axiom_id": request.axiom_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_projection_activation(
        self,
        entry: SMPEntry
    ) -> None:
        """
        Log projection activation to SOP.
        
        Spec: §6.3
        Invariants: INV-SOP-01, INV-SOP-02
        """
        # INV-SOP-02: Verify audit hash before append
        current_hash = self._fetch_audit_hash()
        if not self._verify_audit_hash(current_hash):
            raise AuditHashMismatch("SOP audit hash chain break")
        
        # INV-SOP-01: Append activation event
        self._append_audit_event({
            "event_type": "PROJECTION_ACTIVATION",
            "entry_id": entry.entry_id,
            "axiom_id": entry.axiom_id,
            "timestamp": entry.created_at
        })
```

**Cross-Reference:** SOP v1 §4 (Audit Spine), §12 (MSPC Integration)

---

## §19. Logos Core Integration

**Source Spec:** MSPC Spec §6.4

### §19.1 Logos Core Interface
```python
class LogosCoreInterface:
    """
    MSPC interface to Logos Core.
    
    Spec: §6.4
    Invariants: INV-LC-01, INV-LC-02, INV-LC-03
    """
    
    def serve_active_projections(
        self
    ) -> List[SMPEntry]:
        """
        Serve Active-tier SMP entries to Logos Core.
        
        Spec: §6.4
        Invariants:
            - INV-LC-01: Logos Core accesses via MSPC
            - INV-LC-02: Only Active tier served
            - INV-LC-03: Verify integrity before serving
        """
        # INV-LC-03: Verify SMP integrity
        if not self._verifier.verify_full_smp(self._smp):
            raise SMPIntegrityError("SMP verification failed")
        
        # INV-LC-02: Filter Active tier only
        return [
            entry for entry in self._smp.projections
            if entry.projection_tier == ProjectionTier.ACTIVE
        ]
```

**Cross-Reference:** Logos Core v1 §8 (SMP Access), §13 (MSPC Integration)

---

## §20. Telemetry Module

**Source Spec:** MSPC Spec §8 (Telemetry & Observability)

### §20.1 Metrics Emitter
```python
class MSPCTelemetry:
    """
    MSPC telemetry and observability.
    
    Spec: §8
    Invariants: INV-TEL-01, INV-TEL-02, INV-TEL-03
    """
    
    def emit_projection_metrics(
        self,
        request_count: int,
        success_count: int,
        avg_validation_latency_ms: float
    ) -> None:
        """
        Emit projection pipeline metrics.
        
        Spec: §8.1
        Invariants: INV-TEL-01, INV-TEL-02, INV-TEL-03
        """
        try:
            self._sop_telemetry.record({
                "projection_request_count": request_count,
                "projection_success_count": success_count,
                "avg_validation_latency_ms": avg_validation_latency_ms,
                # INV-TEL-02: No semantic content
            })
        except Exception as e:
            # INV-TEL-03: Telemetry failure doesn't block
            logger.warning(f"Telemetry emission failed: {e}")
    
    def emit_smp_health_metrics(
        self,
        active_count: int,
        staged_count: int,
        deprecated_count: int,
        hash_verification_pass_rate: float
    ) -> None:
        """
        Emit SMP health metrics.
        
        Spec: §8.2
        Invariants: INV-HEALTH-01, INV-HEALTH-02
        """
        self._sop_telemetry.record({
            "active_projection_count": active_count,
            "staged_projection_count": staged_count,
            "deprecated_projection_count": deprecated_count,
            "hash_verification_pass_rate": hash_verification_pass_rate
        })
        
        # INV-HEALTH-02: Alert on hash failures
        if hash_verification_pass_rate < 1.0:
            self._sop_telemetry.alert("SMP hash verification failures detected")
```

**Derivation:** Spec §8.1, §8.2 metrics definitions translated to emission methods.

---

## §21. Bootstrap Module

**Source Spec:** MSPC Spec §9 (Bootstrap & Initialization)

### §21.1 Initialization Sequence
```python
class MSPCBootstrap:
    """
    MSPC initialization and shutdown orchestration.
    
    Spec: §9
    Invariants: INV-INIT-01, INV-INIT-02, INV-SHUT-01, INV-SHUT-02
    """
    
    def initialize(self) -> MSPCController:
        """
        Initialize MSPC during Logos Core Phase-G.
        
        Spec: §9.1
        Invariants:
            - INV-INIT-01: Verify dependencies before ready
            - INV-INIT-02: SMP hash chain verify before operations
        """
        # Step 1: Verify dependencies
        self._verify_emp_accessible()
        self._verify_csp_available()
        self._verify_sop_initialized()
        self._verify_logos_core_ready()
        
        # Step 2: Load or initialize SMP
        smp = self._load_or_initialize_smp()
        
        # INV-INIT-02: Verify SMP hash chain
        if not self._verify_smp_integrity(smp):
            raise MSPCBootstrapFailure("SMP hash chain verification failed")
        
        # Step 3: Initialize pipeline
        pipeline = ProjectionPipelineOrchestrator(...)
        
        # Step 4: Self-test
        if not self._run_self_test(smp, pipeline):
            raise MSPCBootstrapFailure("Self-test failed")
        
        # Step 5: Construct controller
        controller = MSPCController(
            emp_client=self._emp_client,
            csp_client=self._csp_client,
            sop_client=self._sop_client,
            smp=smp,
            governance_mode=self._governance_mode
        )
        controller._is_operational = True
        return controller
    
    def shutdown(self, controller: MSPCController) -> None:
        """
        Shutdown MSPC at tick boundary.
        
        Spec: §9.2
        Invariants: INV-SHUT-01, INV-SHUT-02
        """
        controller._is_operational = False
        controller._complete_inflight_projections()  # INV-SHUT-01
        controller._flush_audit_events()  # INV-SHUT-02
        controller._create_final_smp_snapshot()
```

**Derivation:** Spec §9.1, §9.2 initialization/shutdown sequences mapped to orchestration methods.

---

## §22. Implementation Checklist

### §22.1 Core Components
- [ ] MSPCController class (§3)
- [ ] SemanticProjectionManifest dataclass (§4)
- [ ] SMPEntry dataclass (§5)
- [ ] SMPVersionManager (§6)
- [ ] SMPSnapshotManager (§7)

### §22.2 Pipeline Components
- [ ] ProjectionPipelineOrchestrator (§8)
- [ ] ProjectionRequest dataclass (§9)
- [ ] ProjectionStateMachine (§10)
- [ ] ProjectionValidator (§11)

### §22.3 Governance Components
- [ ] AdmissibilityChecker (§12)
- [ ] ProjectionDenialProtocol (§13)

### §22.4 Integrity Management
- [ ] SMPHashChainManager (§14)
- [ ] SMPIntegrityVerifier (§15)

### §22.5 Integration Interfaces
- [ ] EMPClient (§16)
- [ ] CSPClient (§17)
- [ ] SOPClient (§18)
- [ ] LogosCoreInterface (§19)

### §22.6 Supporting Modules
- [ ] MSPCTelemetry (§20)
- [ ] MSPCBootstrap (§21)

---

**End of Implementation Guide**

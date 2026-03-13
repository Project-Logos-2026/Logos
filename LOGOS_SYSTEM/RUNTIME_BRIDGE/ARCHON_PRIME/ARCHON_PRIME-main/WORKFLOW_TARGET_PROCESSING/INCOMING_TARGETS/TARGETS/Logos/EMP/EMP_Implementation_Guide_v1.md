# EMP Implementation Guide v1

**Paired Specification:** EMP_Design_Specification_v1.md  
**Status:** Implementation Guide  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Purpose & Scope

This guide translates EMP_Design_Specification_v1.md into concrete implementation obligations. Every section traces back to the originating design spec section. This is a **processable packet** for downstream implementation—no architectural ambiguity remains.

---

## §2. Module Structure

### §2.1 Primary Module
**Location:** `LOGOS_SYSTEM/operations_side/governance/emp/`

**Files:**
```
emp/
├── __init__.py                    # Module exports
├── controller.py                  # EMPController class (§3)
├── artifacts/
│   ├── __init__.py
│   ├── atomic_axiom.py           # AtomicAxiom dataclass (§4)
│   ├── provenance.py             # ProvenanceRecord dataclass (§5)
│   └── smp_projection.py         # SMPEntry dataclass (§6)
├── lifecycle/
│   ├── __init__.py
│   ├── creation.py               # AA creation protocol (§7)
│   ├── retrieval.py              # AA retrieval protocol (§8)
│   ├── deprecation.py            # AA deprecation protocol (§9)
│   └── immutability.py           # Immutability enforcement (§10)
├── integrity/
│   ├── __init__.py
│   ├── hash_chain.py             # Hash chain management (§11)
│   ├── verification.py           # Integrity verification (§12)
│   └── genesis.py                # Genesis hash (§13)
├── integration/
│   ├── __init__.py
│   ├── csp.py                    # CSP interface (§14)
│   ├── sop.py                    # SOP audit spine interface (§15)
│   ├── logos_core.py             # Logos Core interface (§16)
│   └── smp.py                    # SMP interface (§17)
├── telemetry.py                  # Metrics emission (§18)
└── bootstrap.py                  # Initialization sequence (§19)
```

**Derivation:** EMP Spec §1.3 (Architectural Position), §6 (Integration Surfaces)

---

## §3. EMPController Class

**Source Spec:** EMP Spec §3 (Artifact Lifecycle Management)

### §3.1 Class Definition
```python
class EMPController:
    """
    Primary interface for epistemic artifact management.
    
    Authority: Custodial only (Spec §1.4).
    Domain: Governance, not semantic reasoning.
    Integration: Called by CSP for AA storage, by Logos Core for AA access.
    """
    
    def __init__(
        self,
        csp_client: CSPClient,
        sop_client: SOPClient,
        hash_chain: HashChainManager,
        genesis_hash: Hash
    ):
        """
        Initialize EMP controller.
        
        Args from Spec:
            csp_client: CSP semantic substrate client (Spec §6.1)
            sop_client: SOP audit spine client (Spec §6.2)
            hash_chain: Hash chain integrity manager (Spec §4)
            genesis_hash: Immutable genesis hash (Spec §4.3)
        
        Invariants: INV-INIT-01, INV-INIT-02
        """
        self._csp_client = csp_client
        self._sop_client = sop_client
        self._hash_chain = hash_chain
        self._genesis_hash = genesis_hash
        self._aa_registry: Dict[AxiomID, AtomicAxiom] = {}
        self._is_operational = False
    
    def create_axiom(
        self,
        content: SemanticContent,
        provenance: ProvenanceRecord
    ) -> AxiomID:
        """
        Create new Atomic Axiom with governance.
        
        Workflow (Spec §3.1):
            1. Validate provenance (Spec §5)
            2. Hash-chain append (Spec §4.1)
            3. Immutability lock (Spec §3.3)
            4. SOP audit log (Spec §6.2)
            5. Return axiom_id
        
        Args:
            content: Semantic content (validated by CSP)
            provenance: Provenance record with creator signature
        
        Returns:
            AxiomID of created axiom
        
        Raises:
            CreationFailure: On any validation failure
        
        Invariants:
            - INV-CREATE-01: Validate provenance before hash-chaining
            - INV-CREATE-02: No partial state on failure
            - INV-CREATE-03: Log creation to SOP
            - INV-SIG-01: Verify creator signature
        """
        # Step 1: Provenance validation
        if not self._verify_provenance(provenance):
            self._sop_client.log_creation_failure("Invalid provenance")
            raise CreationFailure("INV-SIG-02: Invalid creator signature")
        
        # Step 2: Construct AA
        axiom_id = self._generate_axiom_id()
        aa = AtomicAxiom(
            axiom_id=axiom_id,
            content=content,
            provenance=provenance,
            hash=None,  # Computed during hash-chaining
            created_at=datetime.utcnow().isoformat(),
            governance_tags=[]
        )
        
        # Step 3: Hash-chain append
        try:
            aa_hash = self._hash_chain.append_axiom(aa)
            aa = dataclasses.replace(aa, hash=aa_hash)
        except Exception as e:
            # INV-CREATE-02: No partial state
            raise CreationFailure(f"Hash-chaining failed: {e}") from e
        
        # Step 4: Immutability lock
        aa = self._lock_immutability(aa)
        
        # Step 5: Store in registry
        self._aa_registry[axiom_id] = aa
        
        # Step 6: SOP audit log (INV-CREATE-03)
        self._sop_client.log_aa_creation(aa)
        
        return axiom_id
    
    def retrieve_axiom(self, axiom_id: AxiomID) -> AtomicAxiom:
        """
        Retrieve AA with hash chain verification.
        
        Spec: §3.2
        Invariants:
            - INV-RETRIEVE-01: Verify hash before return
            - INV-RETRIEVE-02: Reject corrupted AAs
            - INV-RETRIEVE-03: Log retrieval to SOP
        """
        if axiom_id not in self._aa_registry:
            raise AxiomNotFoundError(f"Axiom {axiom_id} not found")
        
        aa = self._aa_registry[axiom_id]
        
        # INV-RETRIEVE-01: Verify hash integrity
        if not self._hash_chain.verify_axiom_hash(aa):
            # INV-RETRIEVE-02: Corrupted AA
            self._sop_client.alert_integrity_failure(axiom_id)
            raise AxiomCorruptedError(f"Hash verification failed for {axiom_id}")
        
        # INV-RETRIEVE-03: Log retrieval
        self._sop_client.log_aa_retrieval(axiom_id)
        
        return aa
    
    def deprecate_axiom(
        self,
        axiom_id: AxiomID,
        rationale: str,
        superseded_by: Optional[AxiomID] = None
    ) -> None:
        """
        Deprecate AA (not delete).
        
        Spec: §3.4
        Invariants:
            - INV-DEPREC-01: Preserve AA in hash chain
            - INV-DEPREC-02: Flag, don't delete
            - INV-DEPREC-03: Log rationale to SOP
        """
        if axiom_id not in self._aa_registry:
            raise AxiomNotFoundError(f"Axiom {axiom_id} not found")
        
        aa = self._aa_registry[axiom_id]
        
        # INV-DEPREC-02: Flag with deprecation metadata
        deprecation = Deprecation(
            axiom_id=axiom_id,
            deprecated_at=datetime.utcnow().isoformat(),
            rationale=rationale,
            superseded_by=superseded_by
        )
        
        # Update governance tags (AA remains in registry and hash chain)
        updated_aa = dataclasses.replace(
            aa,
            governance_tags=aa.governance_tags + [deprecation]
        )
        self._aa_registry[axiom_id] = updated_aa
        
        # INV-DEPREC-03: Log to SOP
        self._sop_client.log_aa_deprecation(deprecation)
```

**Key Implementation Notes:**
- No AA deletion, only deprecation (INV-DEPREC-01)
- Hash chain verification on every retrieval (INV-RETRIEVE-01)
- Fail-closed on provenance validation (INV-CREATE-01)

---

## §4. AtomicAxiom Dataclass

**Source Spec:** EMP Spec §2.2

### §4.1 Class Definition
```python
@dataclass(frozen=True)
class AtomicAxiom:
    """
    Atomic Axiom with provenance and hash chain integrity.
    
    Spec: §2.2
    """
    axiom_id: AxiomID
    content: SemanticContent
    provenance: ProvenanceRecord
    hash: Hash
    created_at: str  # ISO8601
    governance_tags: List[GovernanceTag]
    
    def __post_init__(self):
        """
        Validate invariants on construction.
        
        Invariants (Spec §2.2):
            - INV-AA-01: Unique axiom_id
            - INV-AA-02: Immutable once hash-chained
            - INV-AA-03: Provenance includes creator signature
            - INV-AA-04: Hash verifiable via chain
        """
        if not self.axiom_id:
            raise InvalidAxiomError("INV-AA-01: axiom_id required")
        
        if not self.provenance.creator_signature:
            raise InvalidAxiomError("INV-AA-03: Creator signature required")
        
        # Hash verification delegated to hash chain manager (§11)
```

**Derivation:** Direct translation of Spec §2.2 AtomicAxiom structure.

---

## §5. ProvenanceRecord Dataclass

**Source Spec:** EMP Spec §5.1

### §5.1 Class Definition
```python
class AxiomSource(Enum):
    """Source of axiom (Spec §5.1)."""
    CSP = "CSP"
    IMPORT = "IMPORT"
    GENERATED = "GENERATED"

class VerificationType(Enum):
    """Verification types (Spec §5.1)."""
    STRUCTURAL = "STRUCTURAL"
    SEMANTIC = "SEMANTIC"
    CRYPTOGRAPHIC = "CRYPTOGRAPHIC"

class VerificationResult(Enum):
    """Verification results (Spec §5.1)."""
    PASS = "PASS"
    FAIL = "FAIL"

@dataclass(frozen=True)
class VerificationStep:
    """Single verification step in provenance chain."""
    verifier: str  # VerifierID
    timestamp: str  # ISO8601
    verification_type: VerificationType
    result: VerificationResult

@dataclass(frozen=True)
class ProvenanceRecord:
    """
    Provenance tracking for AA.
    
    Spec: §5.1
    """
    source: AxiomSource
    creator_id: str
    creator_signature: Signature
    verification_steps: List[VerificationStep]
    import_metadata: Optional[Dict]
    immutability_lock: bool
    
    def __post_init__(self):
        """
        Validate provenance invariants.
        
        Invariants (Spec §5.1):
            - INV-PROV-01: Creator signature required
            - INV-PROV-02: Verification steps append-only
            - INV-PROV-03: Immutable once locked
        """
        if not self.creator_signature:
            raise InvalidProvenanceError("INV-PROV-01: Creator signature required")
        
        # Verification steps append-only enforced by frozen dataclass
        # Immutability lock enforced by AA lifecycle (§10)
```

**Derivation:** Direct translation of Spec §5.1 ProvenanceRecord structure.

---

## §6. SMPEntry Dataclass

**Source Spec:** EMP Spec §2.3

### §6.1 Class Definition
```python
@dataclass(frozen=True)
class SMPEntry:
    """
    Semantic Projection Manifest entry.
    
    Spec: §2.3
    """
    axiom_id: AxiomID
    projection_context: str  # ContextDescriptor
    projection_hash: Hash
    parent_aa_hash: Hash
    timestamp: str  # ISO8601
    
    def __post_init__(self):
        """
        Validate SMP entry invariants.
        
        Invariants (Spec §2.3):
            - INV-SMP-01: Reference canonical AA
            - INV-SMP-02: projection_hash derives from parent_aa_hash
            - INV-SMP-03: Preserve hash chain continuity
        """
        if not self.axiom_id:
            raise InvalidSMPEntryError("INV-SMP-01: axiom_id required")
        
        # Hash derivation validated by hash chain manager (§11)
```

**Derivation:** Direct translation of Spec §2.3 SMPEntry structure.

---

## §7. AA Creation Protocol

**Source Spec:** EMP Spec §3.1

### §7.1 Creation Workflow Module
```python
class AACreationProtocol:
    """
    AA creation workflow with fail-closed semantics.
    
    Spec: §3.1
    Invariants: INV-CREATE-01, INV-CREATE-02, INV-CREATE-03
    """
    
    def __init__(
        self,
        provenance_validator: ProvenanceValidator,
        hash_chain: HashChainManager,
        sop_client: SOPClient
    ):
        self._provenance_validator = provenance_validator
        self._hash_chain = hash_chain
        self._sop_client = sop_client
    
    def execute(
        self,
        content: SemanticContent,
        provenance: ProvenanceRecord
    ) -> AtomicAxiom:
        """
        Execute AA creation protocol.
        
        Spec: §3.1 Workflow
        Steps:
            1. Provenance validation
            2. Hash-chain append
            3. Immutability lock
            4. SOP audit log
        
        Invariants:
            - INV-CREATE-01: Validate provenance first
            - INV-CREATE-02: No partial state on failure
        """
        # Step 1: Provenance validation (INV-CREATE-01)
        if not self._provenance_validator.validate(provenance):
            raise CreationFailure("Provenance validation failed")
        
        # Step 2: Construct AA (transactional)
        try:
            aa = self._construct_axiom(content, provenance)
            aa = self._hash_chain.append_and_lock(aa)
            self._sop_client.log_creation(aa)  # INV-CREATE-03
            return aa
        except Exception as e:
            # INV-CREATE-02: Rollback on any failure
            self._sop_client.log_creation_failure(str(e))
            raise CreationFailure(f"AA creation failed: {e}") from e
```

**Derivation:** Spec §3.1 workflow steps mapped to protocol execution method.

---

## §8. AA Retrieval Protocol

**Source Spec:** EMP Spec §3.2

### §8.1 Retrieval Workflow Module
```python
class AARetrievalProtocol:
    """
    AA retrieval with hash chain verification.
    
    Spec: §3.2
    Invariants: INV-RETRIEVE-01, INV-RETRIEVE-02, INV-RETRIEVE-03
    """
    
    def __init__(
        self,
        aa_registry: Dict[AxiomID, AtomicAxiom],
        hash_chain: HashChainManager,
        sop_client: SOPClient
    ):
        self._aa_registry = aa_registry
        self._hash_chain = hash_chain
        self._sop_client = sop_client
    
    def execute(self, axiom_id: AxiomID) -> AtomicAxiom:
        """
        Retrieve AA with integrity verification.
        
        Spec: §3.2
        Steps:
            1. Lookup in registry
            2. Verify hash chain
            3. Log retrieval to SOP
        
        Invariants:
            - INV-RETRIEVE-01: Verify hash before return
            - INV-RETRIEVE-02: Alert on corruption
            - INV-RETRIEVE-03: Log retrieval
        """
        if axiom_id not in self._aa_registry:
            raise AxiomNotFoundError(f"Axiom {axiom_id} not found")
        
        aa = self._aa_registry[axiom_id]
        
        # INV-RETRIEVE-01: Verify hash
        if not self._hash_chain.verify(aa):
            # INV-RETRIEVE-02: Corruption detected
            self._sop_client.alert_corruption(axiom_id)
            raise AxiomCorruptedError(f"Axiom {axiom_id} corrupted")
        
        # INV-RETRIEVE-03: Log retrieval
        self._sop_client.log_retrieval(axiom_id)
        
        return aa
```

**Derivation:** Spec §3.2 retrieval protocol mapped to execution method.

---

## §9. AA Deprecation Protocol

**Source Spec:** EMP Spec §3.4

### §9.1 Deprecation Workflow Module
```python
@dataclass(frozen=True)
class Deprecation:
    """Deprecation metadata (Spec §3.4)."""
    axiom_id: AxiomID
    deprecated_at: str  # ISO8601
    rationale: str
    superseded_by: Optional[AxiomID]

class AADeprecationProtocol:
    """
    AA deprecation (not deletion).
    
    Spec: §3.4
    Invariants: INV-DEPREC-01, INV-DEPREC-02, INV-DEPREC-03
    """
    
    def execute(
        self,
        aa: AtomicAxiom,
        rationale: str,
        superseded_by: Optional[AxiomID]
    ) -> AtomicAxiom:
        """
        Deprecate AA while preserving in hash chain.
        
        Spec: §3.4
        Invariants:
            - INV-DEPREC-01: Preserve in chain
            - INV-DEPREC-02: Flag, don't delete
            - INV-DEPREC-03: Log rationale
        """
        deprecation = Deprecation(
            axiom_id=aa.axiom_id,
            deprecated_at=datetime.utcnow().isoformat(),
            rationale=rationale,
            superseded_by=superseded_by
        )
        
        # INV-DEPREC-02: Add deprecation tag, don't remove AA
        updated_aa = dataclasses.replace(
            aa,
            governance_tags=aa.governance_tags + [deprecation]
        )
        
        # INV-DEPREC-03: Log to SOP
        self._sop_client.log_deprecation(deprecation)
        
        return updated_aa  # INV-DEPREC-01: AA preserved
```

**Derivation:** Spec §3.4 deprecation protocol mapped to execution method.

---

## §10. Immutability Enforcement

**Source Spec:** EMP Spec §3.3

### §10.1 Immutability Guard
```python
class ImmutabilityGuard:
    """
    Enforce AA immutability once hash-chained.
    
    Spec: §3.3
    Invariants: INV-IMMUT-01, INV-IMMUT-02, INV-IMMUT-03
    """
    
    @staticmethod
    def lock(aa: AtomicAxiom) -> AtomicAxiom:
        """
        Lock AA immutability after hash-chaining.
        
        Spec: §3.3
        Invariant: INV-IMMUT-01
        """
        return dataclasses.replace(
            aa,
            provenance=dataclasses.replace(
                aa.provenance,
                immutability_lock=True
            )
        )
    
    @staticmethod
    def enforce(aa: AtomicAxiom) -> None:
        """
        Enforce immutability constraint.
        
        Spec: §3.3
        Invariants: INV-IMMUT-02, INV-IMMUT-03
        
        Raises:
            ImmutabilityViolation: If AA is hash-chained
        """
        if aa.provenance.immutability_lock:
            # INV-IMMUT-02: Raise violation
            raise ImmutabilityViolation(
                f"Axiom {aa.axiom_id} is immutable (hash-chained)"
            )
            # INV-IMMUT-03: SOP emergency mode triggered by exception handler
```

**Derivation:** Spec §3.3 immutability guarantee mapped to enforcement methods.

---

## §11. HashChainManager Class

**Source Spec:** EMP Spec §4 (Hash Chain Integrity)

### §11.1 Class Definition
```python
class HashChainManager:
    """
    Two-tier hash chain management.
    
    Spec: §4
    Invariants: INV-HC-01, INV-HC-02, INV-HC-03
    """
    
    def __init__(self, genesis_hash: Hash):
        """
        Initialize hash chain with genesis hash.
        
        Args:
            genesis_hash: Immutable genesis hash (Spec §4.3)
        
        Invariants: INV-GENESIS-01, INV-GENESIS-02
        """
        self._genesis_hash = genesis_hash
        self._aa_chain: List[Hash] = [genesis_hash]
        self._smp_chain: List[Hash] = []
    
    def append_axiom(self, aa: AtomicAxiom) -> Hash:
        """
        Append AA to hash chain.
        
        Spec: §4.1 Tier 1
        Formula: AA_n.hash = H(AA_n.content || AA_{n-1}.hash)
        
        Invariants: INV-HC-01, INV-GENESIS-02
        """
        previous_hash = self._aa_chain[-1]
        aa_hash = self._compute_hash(aa.content, previous_hash)
        self._aa_chain.append(aa_hash)
        return aa_hash
    
    def append_smp_projection(
        self,
        smp_entry: SMPEntry,
        parent_aa_hash: Hash
    ) -> Hash:
        """
        Append SMP projection to hash chain.
        
        Spec: §4.1 Tier 2
        Formula: SMP_n.hash = H(SMP_n.projection || SMP_{n-1}.hash || AA_parent.hash)
        
        Invariant: INV-HC-02
        """
        previous_smp_hash = self._smp_chain[-1] if self._smp_chain else self._genesis_hash
        smp_hash = self._compute_hash(
            smp_entry.projection_context,
            previous_smp_hash,
            parent_aa_hash
        )
        self._smp_chain.append(smp_hash)
        return smp_hash
    
    def verify_axiom_hash(self, aa: AtomicAxiom) -> bool:
        """
        Verify AA hash against chain.
        
        Spec: §4.2
        Invariants: INV-VERIFY-01, INV-HC-03
        """
        if aa.hash not in self._aa_chain:
            return False  # INV-HC-03: Chain break detected
        
        # INV-VERIFY-01: Recompute and verify
        index = self._aa_chain.index(aa.hash)
        previous_hash = self._aa_chain[index - 1]
        recomputed_hash = self._compute_hash(aa.content, previous_hash)
        
        return recomputed_hash == aa.hash
```

**Derivation:** Spec §4.1, §4.2 hash chain formulas and verification procedures mapped to manager methods.

---

## §12. Integrity Verification Module

**Source Spec:** EMP Spec §4.2

### §12.1 Verification Orchestrator
```python
class IntegrityVerifier:
    """
    Hash chain integrity verification.
    
    Spec: §4.2
    Invariants: INV-VERIFY-01, INV-VERIFY-02, INV-VERIFY-03
    """
    
    def __init__(
        self,
        hash_chain: HashChainManager,
        sop_client: SOPClient
    ):
        self._hash_chain = hash_chain
        self._sop_client = sop_client
    
    def verify_full_chain(self) -> bool:
        """
        Verify entire hash chain.
        
        Spec: §4.2
        Triggers: AA retrieval, SOP audit, bootstrap self-test
        
        Invariants:
            - INV-VERIFY-01: Recompute full chain
            - INV-VERIFY-02: Escalate breaks to SOP
            - INV-VERIFY-03: Log results to SOP
        """
        try:
            # INV-VERIFY-01: Recompute entire chain
            chain_valid = self._hash_chain.recompute_and_verify_all()
            
            # INV-VERIFY-03: Log results
            self._sop_client.log_integrity_verification(chain_valid)
            
            if not chain_valid:
                # INV-VERIFY-02: Escalate to SOP emergency mode
                self._sop_client.trigger_emergency_mode("Hash chain break detected")
            
            return chain_valid
        except Exception as e:
            self._sop_client.trigger_emergency_mode(f"Verification failed: {e}")
            return False
```

**Derivation:** Spec §4.2 verification procedures mapped to orchestrator methods.

---

## §13. Genesis Hash Module

**Source Spec:** EMP Spec §4.3

### §13.1 Genesis Hash Generator
```python
class GenesisHashGenerator:
    """
    Genesis hash generation and validation.
    
    Spec: §4.3
    Invariants: INV-GENESIS-01, INV-GENESIS-02, INV-GENESIS-03
    """
    
    @staticmethod
    def generate(
        bootstrap_timestamp: str,
        system_nonce: str
    ) -> Hash:
        """
        Generate genesis hash at bootstrap.
        
        Spec: §4.3
        Formula: H("LOGOS_EMP_GENESIS" || bootstrap_timestamp || system_nonce)
        
        Invariant: INV-GENESIS-01 (immutable)
        """
        genesis_preimage = f"LOGOS_EMP_GENESIS{bootstrap_timestamp}{system_nonce}"
        genesis_hash = hashlib.sha256(genesis_preimage.encode()).hexdigest()
        return genesis_hash
    
    @staticmethod
    def verify(
        genesis_hash: Hash,
        bootstrap_timestamp: str,
        system_nonce: str
    ) -> bool:
        """
        Verify genesis hash integrity.
        
        Spec: §4.3
        Invariant: INV-GENESIS-03
        """
        expected_hash = GenesisHashGenerator.generate(
            bootstrap_timestamp,
            system_nonce
        )
        return expected_hash == genesis_hash
```

**Derivation:** Spec §4.3 genesis hash formula and verification mapped to generator methods.

---

## §14. CSP Integration

**Source Spec:** EMP Spec §6.1

### §14.1 CSP Interface
```python
class CSPClient:
    """
    EMP client for CSP semantic substrate.
    
    Spec: §6.1
    Contract:
        - CSP delegates AA storage to EMP
        - EMP delegates semantic validation to CSP
        - Clear authority boundary
    
    Invariants: INV-CSP-01, INV-CSP-02, INV-CSP-03
    """
    
    def validate_semantic_content(
        self,
        content: SemanticContent
    ) -> bool:
        """
        Delegate semantic validation to CSP.
        
        Spec: §6.1
        Invariant: INV-CSP-01 (EMP delegates semantic validation)
        """
        # EMP does NOT interpret semantics (INV-CSP-03)
        return self._query_csp_validation(content)
    
    def store_axiom_reference(
        self,
        axiom_id: AxiomID,
        semantic_metadata: Dict
    ) -> None:
        """
        Notify CSP of new AA for semantic indexing.
        
        Spec: §6.1
        Invariant: INV-CSP-02 (CSP routes storage through EMP)
        """
        # EMP handles storage, CSP maintains semantic index
        self._notify_csp_new_axiom(axiom_id, semantic_metadata)
```

**Cross-Reference:** CSP v1 §3 (Semantic Axiom Management), §10 (EMP Integration)

---

## §15. SOP Integration

**Source Spec:** EMP Spec §6.2

### §15.1 SOP Audit Client
```python
class SOPClient:
    """
    EMP client for SOP audit spine.
    
    Spec: §6.2
    Contract:
        - EMP logs all AA lifecycle events to SOP
        - SOP provides hash chain integrity verification
        - EMP participates in audit spine
    
    Invariants: INV-SOP-01, INV-SOP-02, INV-SOP-03
    """
    
    def log_aa_creation(self, aa: AtomicAxiom) -> None:
        """
        Log AA creation to SOP audit spine.
        
        Spec: §6.2
        Invariants: INV-SOP-01, INV-SOP-02
        """
        # Verify audit hash before append (INV-SOP-02)
        current_hash = self._fetch_audit_hash()
        if not self._verify_audit_hash(current_hash):
            raise AuditHashMismatch("Hash chain break in SOP audit spine")
        
        # Append creation event (INV-SOP-01)
        self._append_audit_event({
            "event_type": "AA_CREATION",
            "axiom_id": aa.axiom_id,
            "timestamp": aa.created_at,
            "hash": aa.hash
        })
    
    def log_aa_retrieval(self, axiom_id: AxiomID) -> None:
        """Log AA retrieval (Spec §6.2, INV-SOP-01)."""
        self._append_audit_event({
            "event_type": "AA_RETRIEVAL",
            "axiom_id": axiom_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def alert_corruption(self, axiom_id: AxiomID) -> None:
        """
        Alert SOP of AA corruption.
        
        Spec: §6.2
        Invariant: INV-SOP-03 (escalate audit failures)
        """
        self._trigger_sop_alert({
            "alert_type": "AA_CORRUPTION",
            "axiom_id": axiom_id,
            "severity": "CRITICAL"
        })
```

**Cross-Reference:** SOP v1 §4 (Audit Spine), §11 (EMP Integration)

---

## §16. Logos Core Integration

**Source Spec:** EMP Spec §6.3

### §16.1 Logos Core Interface
```python
class LogosCoreInterface:
    """
    EMP interface to Logos Core.
    
    Spec: §6.3
    Contract:
        - Logos Core accesses AAs via EMP
        - EMP verifies integrity before serving
        - Logos Core honors deprecation flags
    
    Invariants: INV-LC-01, INV-LC-02, INV-LC-03
    """
    
    def request_axiom(
        self,
        axiom_id: AxiomID
    ) -> AtomicAxiom:
        """
        Serve AA to Logos Core with integrity verification.
        
        Spec: §6.3
        Invariants:
            - INV-LC-01: Route through EMP, not CSP
            - INV-LC-02: Reject corrupted AAs
            - INV-LC-03: Honor deprecation flags
        """
        # Retrieve with hash verification (INV-LC-02)
        aa = self._emp_controller.retrieve_axiom(axiom_id)
        
        # Check deprecation status (INV-LC-03)
        if self._is_deprecated(aa):
            raise AxiomDeprecatedError(
                f"Axiom {axiom_id} is deprecated",
                deprecation_info=self._get_deprecation_info(aa)
            )
        
        return aa
```

**Cross-Reference:** Logos Core v1 §7 (Axiom Access), §12 (EMP Integration)

---

## §17. SMP Integration

**Source Spec:** EMP Spec §6.4

### §17.1 SMP Interface
```python
class SMPInterface:
    """
    EMP interface to Semantic Projection Manifest.
    
    Spec: §6.4
    Contract:
        - EMP governs SMP projection integrity
        - SMP projections chain to parent AAs
        - EMP verifies projection hashes
    
    Invariants: INV-SMP-INT-01, INV-SMP-INT-02, INV-SMP-INT-03
    """
    
    def create_projection(
        self,
        axiom_id: AxiomID,
        projection_context: str
    ) -> SMPEntry:
        """
        Create SMP projection with hash chain integrity.
        
        Spec: §6.4
        Invariants:
            - INV-SMP-INT-01: Reference canonical AA
            - INV-SMP-INT-02: Verify projection hash chain
        """
        # INV-SMP-INT-01: Verify AA exists
        aa = self._emp_controller.retrieve_axiom(axiom_id)
        
        # Compute projection hash (INV-SMP-INT-02)
        projection_hash = self._hash_chain.append_smp_projection(
            projection_context,
            aa.hash
        )
        
        smp_entry = SMPEntry(
            axiom_id=axiom_id,
            projection_context=projection_context,
            projection_hash=projection_hash,
            parent_aa_hash=aa.hash,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # INV-SMP-INT-03: Log to SOP
        self._sop_client.log_smp_projection(smp_entry)
        
        return smp_entry
```

**Cross-Reference:** MSPC v1 §4 (SMP Architecture) [to be defined in T2]

---

## §18. Telemetry Module

**Source Spec:** EMP Spec §7 (Telemetry & Observability)

### §18.1 Metrics Emitter
```python
class EMPTelemetry:
    """
    EMP telemetry and observability.
    
    Spec: §7
    Invariants: INV-TEL-01, INV-TEL-02, INV-TEL-03
    """
    
    def emit_artifact_metrics(
        self,
        creation_count: int,
        retrieval_count: int,
        deprecation_count: int
    ) -> None:
        """
        Emit artifact lifecycle metrics.
        
        Spec: §7.1
        Invariants:
            - INV-TEL-01: Emit to SOP telemetry
            - INV-TEL-02: No semantic content leakage
        """
        try:
            self._sop_telemetry.record({
                "aa_creation_count": creation_count,
                "aa_retrieval_count": retrieval_count,
                "aa_deprecation_count": deprecation_count,
                # INV-TEL-02: No semantic content included
            })
        except Exception as e:
            # INV-TEL-03: Telemetry failure doesn't block operations
            logger.warning(f"Telemetry emission failed: {e}")
    
    def emit_integrity_metrics(
        self,
        hash_verification_pass_rate: float,
        chain_break_count: int
    ) -> None:
        """
        Emit hash chain integrity metrics.
        
        Spec: §7.2
        Invariants: INV-AUDIT-01, INV-AUDIT-02
        """
        self._sop_telemetry.record({
            "hash_verification_pass_rate": hash_verification_pass_rate,
            "chain_break_count": chain_break_count
        })
        
        # INV-AUDIT-01: Alert on chain breaks
        if chain_break_count > 0:
            self._sop_telemetry.alert("Hash chain break detected")
```

**Derivation:** Spec §7.1, §7.2 metrics definitions translated to emission methods.

---

## §19. Bootstrap Module

**Source Spec:** EMP Spec §9 (Bootstrap & Initialization)

### §19.1 Initialization Sequence
```python
class EMPBootstrap:
    """
    EMP initialization and shutdown orchestration.
    
    Spec: §9
    Invariants: INV-INIT-01, INV-INIT-02, INV-SHUT-01, INV-SHUT-02
    """
    
    def initialize(self) -> EMPController:
        """
        Initialize EMP during Logos Core Phase-G.
        
        Spec: §9.1
        Sequence:
            1. Verify upstream dependencies
            2. Load/generate genesis hash
            3. Initialize hash chains
            4. Self-test
            5. Signal ready
        
        Invariants:
            - INV-INIT-01: Verify deps before ready
            - INV-INIT-02: Genesis hash before AA ops
        
        Returns:
            Initialized EMPController instance
        """
        # Step 1: Verify dependencies
        self._verify_csp_accessible()
        self._verify_sop_audit_spine_initialized()
        self._verify_logos_core_available()
        
        # Step 2: Load/generate genesis hash (INV-INIT-02)
        genesis_hash = self._load_or_generate_genesis_hash()
        
        # Step 3: Initialize hash chains
        hash_chain = HashChainManager(genesis_hash)
        
        # Step 4: Self-test
        if not self._run_self_test(hash_chain):
            raise EMPBootstrapFailure("Self-test failed")
        
        # Step 5: Construct controller
        controller = EMPController(
            csp_client=self._csp_client,
            sop_client=self._sop_client,
            hash_chain=hash_chain,
            genesis_hash=genesis_hash
        )
        controller._is_operational = True
        return controller
    
    def shutdown(self, controller: EMPController) -> None:
        """
        Shutdown EMP at tick boundary.
        
        Spec: §9.2
        Invariants: INV-SHUT-01, INV-SHUT-02
        """
        controller._is_operational = False
        controller._complete_inflight_operations()  # INV-SHUT-01
        controller._flush_audit_events()  # INV-SHUT-02
        controller._verify_final_hash_chain()
```

**Derivation:** Spec §9.1, §9.2 initialization/shutdown sequences mapped to orchestration methods.

---

## §20. Implementation Checklist

### §20.1 Core Components
- [ ] EMPController class (§3)
- [ ] AtomicAxiom dataclass (§4)
- [ ] ProvenanceRecord dataclass (§5)
- [ ] SMPEntry dataclass (§6)

### §20.2 Lifecycle Protocols
- [ ] AACreationProtocol (§7)
- [ ] AARetrievalProtocol (§8)
- [ ] AADeprecationProtocol (§9)
- [ ] ImmutabilityGuard (§10)

### §20.3 Integrity Management
- [ ] HashChainManager (§11)
- [ ] IntegrityVerifier (§12)
- [ ] GenesisHashGenerator (§13)

### §20.4 Integration Interfaces
- [ ] CSPClient (§14)
- [ ] SOPClient (§15)
- [ ] LogosCoreInterface (§16)
- [ ] SMPInterface (§17)

### §20.5 Supporting Modules
- [ ] EMPTelemetry (§18)
- [ ] EMPBootstrap (§19)

### §20.6 Invariant Enforcement
- [ ] All 70 invariants implemented as runtime checks
- [ ] Hash chain integrity verification
- [ ] Immutability enforcement
- [ ] Fail-closed semantics

---

**End of Implementation Guide**

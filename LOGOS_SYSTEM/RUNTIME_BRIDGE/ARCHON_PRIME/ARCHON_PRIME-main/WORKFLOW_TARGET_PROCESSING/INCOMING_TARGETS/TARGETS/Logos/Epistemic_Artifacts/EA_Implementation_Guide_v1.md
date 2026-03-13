# LOGOS EA System — Implementation Guide

**Version**: 1.0.0  
**Status**: AUTHORITATIVE  
**Date**: 2026-03-06  
**Entailed From**: LOGOS_EA_System_Design_Spec_V1.md  
**Scope**: GPT-processable implementation obligations for EA system integration  
**Purpose**: Remove ambiguity at spec→code translation boundary

---

## 1. Overview

This guide translates the EA System Design Specification into concrete implementation obligations. The EA system does not introduce new components—it formalizes the relationship between existing modules under a unified governance model.

**Core principle** (§1, §16.5): EA = SMP + AA Catalog. No new classes, no new files, no new import paths. Implementation consists of integration wiring and cleanup.

**Critical dependency** (§16.2): EA system becomes operational only after P3.1 (SMP Pipeline) is complete. Until then, the EA abstraction exists as a design model but lacks runtime activation.

---

## 2. Component Inventory

### 2.1 Existing Modules (Already Implemented)

All paths relative to: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/`

| Module | Path | Status | Spec Reference |
|--------|------|--------|----------------|
| SMP_Schema.py | CSP_Core/Unified_Working_Memory/ | ✓ Compliant | §4.1, §16.3 |
| SMP_Store.py | CSP_Core/Unified_Working_Memory/ | ✓ Compliant | §4.3, §16.1 |
| AA_Catalog.py | CSP_Core/Unified_Working_Memory/ | ⚠ Exists, not integrated | §5.5, §16.1 |
| Classification_Tracker.py | CSP_Core/Unified_Working_Memory/ | ✓ Compliant | §6, §16.1 |
| UWM_Access_Control.py | CSP_Core/Unified_Working_Memory/ | ✓ Compliant | §9.2, §16.1 |
| Promotion_Evaluator.py | CSP_Core/ | ✓ Compliant | §8.3, §16.1 |
| Canonical_SMP_Producer.py | CSP_Core/ | ✓ Compliant | §8.3, §16.1 |
| CSP_Canonical_Store.py | CSP_Core/ | ✓ Compliant | §7.2, §16.1 |
| Boundary_Validators.py | Logos_Core/Orchestration/ | ✓ Compliant | §9.3, §16.1 |
| Agent_Wrappers.py | Logos_Core/Orchestration/ | ⚠ Stubs only | §8.1, §16.1 |
| Runtime_Loop.py | Logos_Core/Orchestration/ | ⚠ Partial | §12, §16.1 |

### 2.2 Required Integrations

**REM-09** (§16.2, §5.5): Integrate AA_Catalog into SMP_Store
- **Action**: Wire AA_Catalog methods into SMP_Store.append_aa() for indexed lookup
- **Status**: Blocked until P3.1 complete (no runtime context to test against)

**REM-06** (§16.2, §16.1): Clean UWM `__init__.py`
- **Action**: Remove duplicate class definitions
- **Status**: Can be completed independently

**REM-01** (§16.2, P3.1): Implement SMP Pipeline in Logos Agent
- **Action**: Full agent wrapper implementation with subsystem injection, SMP routing state machine, multi-tick processing
- **Status**: Critical path blocker for EA system activation

---

## 3. Implementation Obligations by Spec Section

### 3.1 SMP Schema (§4)

**Obligation**: SMP_Schema.py must define the canonical dataclass with exact field names and types per §4.1.

**Implementation contract**:
```python
@dataclass
class SMP:
    identity: str              # Format: SMP:<session>:<seq> or C-SMP:<session>:<seq>
    type: str                  # Declarative category (observation, plan_fragment, etc.)
    provenance: dict           # Structured envelope (creator, source, chain_of_custody)
    temporal_context: dict     # Time metadata (created_at, session_tick)
    status_confidence: dict    # Status and confidence bounds
    classification: str        # One of: rejected, conditional, provisional, canonical
    privation: dict            # Redaction/quarantine flags
    append_artifacts: list     # Ordered AA catalog
    payload: dict              # Structured, bounded, inert content
    content_hash: str          # SHA-256 of content fields
```

**Immutability enforcement** (§3.3):
- Hard immutable: identity, type, provenance, temporal_context, privation, payload
- Governed mutable: classification (monotonic), append_artifacts (append-only), content_hash (recomputed at canonicalization only)

**Prohibitions** (§4.2): SMP_Schema validation must reject:
- Executable code or module references
- Scheduling/continuation directives
- Self-referential autonomy markers
- Template identifiers
- Unbounded/streaming payloads
- Mutable external state references

**Validation method signature** (entailed from §4.2):
```python
def validate_smp_inertness(smp: SMP) -> tuple[bool, Optional[str]]:
    """
    Returns: (is_valid, error_message)
    Raises: InertViolation if prohibited content detected
    """
```

### 3.2 SMP Creation (§4.3, §8.1)

**Obligation**: SMP_Store.create_smp() must implement creation protocol with sealing and hash computation.

**Method signature** (§4.3):
```python
def create_smp(
    self,
    smp_type: str,
    payload: dict,
    provenance: dict,
    temporal_context: dict,
    initial_classification: str = "conditional"
) -> SMP:
    """
    Creates and seals a new SMP.
    
    Pre-conditions (§14.1):
    - smp_type must be valid declarative category
    - payload must pass inertness validation
    - provenance must contain required fields: creator, source
    - temporal_context must contain: created_at, session_tick
    - initial_classification must be in {conditional, provisional}
    
    Post-sealing guarantees (§4.3):
    - All core fields immutable
    - content_hash computed over identity+type+provenance+temporal+payload
    - append_artifacts initialized to empty list
    - SMP stored in UWM with unique identity
    
    Error handling (§14.1):
    - Missing required field → ValidationError
    - Payload inertness violation → InertViolation
    - Invalid provenance → ProvenanceError
    - Identity collision → UniquenessViolation
    
    Returns: Sealed SMP
    """
```

**Identity generation** (§3.2):
- Format: `f"SMP:{session_id}:{sequence}"`
- session_id: From RuntimeLoop context
- sequence: Monotonically increasing per session
- V1.1+ forward compatibility note (§3.2.1): Future format may include agent_id prefix

### 3.3 AA Attachment (§5, §8.2)

**Obligation**: SMP_Store.append_aa() must implement append-only AA attachment with validation.

**Method signature** (§5.3, §8.2):
```python
def append_aa(
    self,
    smp_id: str,
    aa_type: str,
    content: dict,
    producer: str
) -> bool:
    """
    Appends an AA to an existing SMP's catalog.
    
    Pre-conditions (§14.2):
    - Target SMP must exist in UWM
    - Target SMP must not be canonical (C-SMP)
    - Target SMP must not be rejected
    - aa_type must be valid (§5.2)
    - producer must be authorized (§9.3)
    
    AA schema enforcement (§5.1):
    - aa_id: Generated as f"{smp_id}:AA:{len(append_artifacts)}"
    - aa_type: One of evaluation, governance_annotation, context_link, transformation_record
    - content: Dict with type-specific required fields
    - producer: String identifying protocol/agent
    - timestamp: ISO-8601 format
    
    Post-attachment guarantees (§5.3):
    - AA appended to append_artifacts list
    - No modification to SMP core fields
    - EA lifecycle event logged to SOP (§15.1)
    
    Error handling (§14.2):
    - SMP not found → LookupError
    - Target is canonical → ImmutabilityViolation
    - Target is rejected → TerminalStateError
    - Schema violation → ValidationError
    
    Returns: True on success
    """
```

**AA Schema** (§5.1):
```python
AA = {
    "aa_id": str,          # Format: <smp_id>:AA:<index>
    "aa_type": str,        # One of 4 types per §5.2
    "content": dict,       # Type-specific fields
    "producer": str,       # Protocol or agent identifier
    "timestamp": str       # ISO-8601
}
```

**AA Types** (§5.2):
- `evaluation`: Analysis/scoring from protocol
- `governance_annotation`: Governance decision record
- `context_link`: Cross-reference to other EAs
- `transformation_record`: Proof of reasoning step

### 3.4 Classification System (§6, §8.3)

**Obligation**: Classification_Tracker must enforce monotonic ladder and terminal states.

**Classification Ladder** (§6.1):
```
rejected ← terminal (no upward transitions)
    ↑
conditional → provisional → canonical
```

**Transition rules** (§6.2):
- Forward transitions: conditional → provisional → canonical (allowed)
- Backward transition: any → rejected (allowed, terminal)
- All other backward transitions: prohibited (§14.3)

**Method signature** (entailed from §6.2):
```python
def validate_classification_transition(
    current: str,
    target: str
) -> tuple[bool, Optional[str]]:
    """
    Returns: (is_valid, error_message)
    Raises: MonotonicLadderViolation if backward transition attempted (except to rejected)
    """
```

**Promotion Protocol** (§8.3):
```python
def promote_classification(
    self,
    smp_id: str,
    new_classification: str
) -> bool:
    """
    Promotes SMP classification via monotonic ladder.
    
    For promotion to 'canonical':
    - Must pass through PromotionEvaluator (§8.3)
    - Triggers Canonical_SMP_Producer (§8.3)
    - Recomputes content_hash to include full AA chain (§3.3)
    - Persists to CSP_Canonical_Store (§7.2)
    - Assigns C-SMP: prefix to identity (§3.2)
    
    Error handling (§14.3):
    - Backward transition → MonotonicLadderViolation
    - Promotion eval failure → Set to rejected, attach governance_annotation
    - Hash mismatch → Reject, attach governance_annotation
    
    Returns: True on success
    """
```

### 3.5 Storage Layers (§7)

**UWM (Unified Working Memory)** (§7.1):
- **Authority**: Session-scoped, in-memory, authoritative epistemic memory
- **Scope**: All active EAs (non-canonical SMPs)
- **Access**: Via UWM_Access_Control role-based API (§9.2)
- **Lifecycle**: Cleared at session end (no persistence)

**CSP Canonical Store** (§7.2):
- **Authority**: Persistent, long-term storage for C-SMPs only
- **Scope**: Canonical EAs promoted via PromotionEvaluator
- **Access**: Read-only to all protocols; write-only to Promotion pipeline
- **Format**: C-SMP prefix on identity field

**Data flow** (§7.3):
```
Task → Logos Agent → UWM (working SMPs)
                        ↓ (if promoted)
                  CSP Canonical Store (C-SMPs)
```

### 3.6 Authority Model (§9)

**Logos Agent Sovereignty** (§9.1):
- Only Logos Agent may create SMPs (§9.1)
- Only Logos Agent may modify classification (§9.1)
- Sub-agents (I1, I2, I3) propose AAs but cannot attach them (§9.1)
- Logos Agent reviews AA proposals and attaches via SMP_Store.append_aa() (§9.1)

**UWM Write Boundaries** (§9.2):
```python
# From UWM_Access_Control.py
class UWMWriteRole(Enum):
    LOGOS_AGENT_ONLY = "logos_agent"  # Can create SMPs, attach AAs, promote
    SUB_AGENT = "sub_agent"            # Cannot write (proposals only)
    PROTOCOL = "protocol"              # Cannot write directly
```

**Boundary Validation** (§9.3):
```python
# From Boundary_Validators.py (§16.1)
def validate_agent_write_boundary(
    actor: str,
    operation: str
) -> tuple[bool, Optional[str]]:
    """
    Enforces Logos Agent sovereignty over EA writes.
    
    Permitted operations by actor:
    - Logos Agent: create_smp, append_aa, promote_classification
    - Sub-agents: propose_aa only (writes rejected)
    - Protocols: read-only
    
    Returns: (is_authorized, denial_reason)
    """
```

### 3.7 Protocol Integration Surface (§10)

**RGE Integration** (§10.1):
- RGE provides geometric context to Logos Agent
- RGE does not read or write EAs directly
- RGE context influences AA content but not structure

**Per-Protocol Integration Points** (§10.2-§10.9):

**CSP** (§10.2):
- Reads: EAs from UWM for analysis
- Writes: Proposes `evaluation` AAs
- Authority: Promotion pipeline (PromotionEvaluator, CanonicalSMPProducer)

**SCP** (§10.3):
- Reads: EAs for semantic projection
- Writes: Proposes `evaluation` AAs with semantic scores

**MTP** (§10.4):
- Reads: Task-in-progress context from active EAs
- Writes: Proposes `context_link` AAs for multi-tick continuity

**DRAC** (§10.5):
- Reads: EA metadata for risk assessment
- Writes: Proposes `governance_annotation` AAs with risk flags

**EMP** (§10.6):
- Reads: Canonical EAs for embedding computation
- Writes: None (read-only protocol)

**MSPC** (§10.7):
- Reads: Projection-ready EAs
- Writes: Proposes `transformation_record` AAs

**ARP** (§10.8):
- Reads: EAs for axiom reconciliation
- Writes: Proposes `evaluation` AAs with axiom compliance scores

**SOP** (§10.9):
- Reads: EA lifecycle events from operational logger
- Writes: None (observability-only)

### 3.8 Tick-Level Execution Flow (§12)

**Per-Tick Processing** (§12.1):
```
Tick N begins
  ↓
Logos Agent receives task or continues SMP processing
  ↓
Sub-agents (I1, I2, I3) execute via _on_tick()
  ↓
Sub-agents return AA proposals in tick_result
  ↓
Logos Agent reviews proposals via _process_task()
  ↓
Logos Agent attaches approved AAs via SMP_Store.append_aa()
  ↓
Logos Agent evaluates classification promotion
  ↓
If provisional → canonical: Promotion pipeline triggered
  ↓
Tick N completes, EA state logged
```

**Tick Budget** (§12.2):
- Max 50 ticks per EA lifecycle
- Exhaustion triggers governance_annotation attachment
- No silent failures (§14.4)

**Multi-Tick Lifecycle** (§12.3):
- EAs may span multiple ticks
- MTP provides continuity context via `context_link` AAs
- Logos Agent maintains routing state machine (§12.4)

### 3.9 Governance Constraints (§13)

**Inertness** (§13.1):
- No executable content in any SMP field
- No scheduling directives
- No autonomy markers
- Validation at creation time (fail-closed)

**Append-Only AA Catalog** (§13.2):
- AAs can only be added, never removed
- AA catalog order is immutable
- AA content is immutable post-attachment

**No Audit Readback** (§13.3):
- SOP receives EA lifecycle events
- No runtime component reads from operational log
- Absolute separation of observability and execution

**Deny-by-Default** (§13.4):
- All write operations require explicit authorization
- Unknown actors denied
- Missing fields trigger rejection

### 3.10 Error Handling (§14)

**Failure Response Protocol**: All EA operations fail-closed. No silent failures.

**SMP Creation Failures** (§14.1):
```python
# Example error handling pattern
try:
    smp = smp_store.create_smp(...)
except ValidationError:
    # Log error, reject operation, propagate exception
except InertViolation:
    # Log error, halt processing, notify operator
except UniquenessViolation:
    # Log error, generate new identity, retry once
```

**AA Attachment Failures** (§14.2):
```python
try:
    success = smp_store.append_aa(...)
except LookupError:
    # SMP not found - log, skip AA, continue
except ImmutabilityViolation:
    # Target is canonical - log, reject AA
except TerminalStateError:
    # Target is rejected - log, skip AA
```

**Classification Failures** (§14.3):
```python
try:
    success = smp_store.promote_classification(...)
except MonotonicLadderViolation:
    # Backward transition attempted - log, reject
    # If promotion eval failed - set to rejected, attach governance_annotation
```

### 3.11 Observability (§15)

**EA Lifecycle Events** (§15.1):

Required log events to SOP operational logger:

```python
# Event types and required data fields
EA_LIFECYCLE_EVENTS = {
    "ea_created": {
        "trigger": "SMPStore.create_smp()",
        "data": ["smp_id", "type", "classification", "tick"]
    },
    "aa_attached": {
        "trigger": "SMPStore.append_aa()",
        "data": ["smp_id", "aa_id", "aa_type", "producer", "tick"]
    },
    "classification_changed": {
        "trigger": "SMPStore.promote_classification()",
        "data": ["smp_id", "old_classification", "new_classification", "tick"]
    },
    "promotion_evaluated": {
        "trigger": "PromotionEvaluator.evaluate()",
        "data": ["smp_id", "result", "rationale", "tick"]
    },
    "csmp_produced": {
        "trigger": "CanonicalSMPProducer.produce()",
        "data": ["csmp_id", "source_smp_id", "tick"]
    },
    "ea_rejected": {
        "trigger": "Classification → rejected",
        "data": ["smp_id", "rejection_reason", "tick"]
    }
}
```

**Logging Injection Points** (§15.3):
- RuntimeLoop: EA creation event, tick-level EA state summary
- Agent_Wrappers: AA proposal submission, AA attachment confirmation
- SMP_Store: create_smp(), append_aa(), promote_classification() events
- CSP_Canonical_Store: C-SMP production event

**Total allocation**: 19 logging points across 5 files (per P4.5, referenced in §15.3)

---

## 4. Integration Sequencing

**Dependency Chain** (§16.2):

```
1. REM-01 (P3.1) — SMP Pipeline Implementation [CRITICAL PATH BLOCKER]
   ↓
2. REM-02 — Fix tick_result schema to P1-IF-07
   ↓
3. REM-06 — Clean UWM __init__.py duplicates
   ↓
4. REM-09 — Integrate AA_Catalog into SMPStore
   ↓
5. REM-07 — Add operational logging points (19 total)
   ↓
EA System Fully Operational
```

**REM-01 Details** (P3.1, §16.1):
- Implement agent wrappers with subsystem injection
- Implement SMP routing state machine in Logos Agent
- Implement multi-tick EA lifecycle processing via _process_task()
- Wire UWM/SCP/CSP/MTP/ARP into agent constructors
- Status: **Blocks all other EA integrations**

**REM-06 Details** (§16.1):
- Clean duplicate class definitions in UWM `__init__.py`
- Status: **Can be completed independently**

**REM-09 Details** (§16.1, §5.5):
- Wire AA_Catalog methods into SMP_Store.append_aa()
- Enable indexed AA lookup by type, producer, or temporal range
- Status: **Blocked by REM-01 (needs runtime context for testing)**

---

## 5. File-Level Implementation Map

### 5.1 SMP_Schema.py

**Spec Reference**: §4.1  
**Path**: `CSP_Core/Unified_Working_Memory/SMP_Schema.py`  
**Status**: ✓ Implemented  
**Required Changes**: None (compliant with spec)

**Implementation obligations**:
- Dataclass with 10 canonical fields (§4.1)
- Type annotations match spec exactly
- No additional fields beyond spec
- No methods beyond __init__ and __repr__

### 5.2 SMP_Store.py

**Spec Reference**: §4.3, §5.3, §6.2, §8.1-§8.3  
**Path**: `CSP_Core/Unified_Working_Memory/SMP_Store.py`  
**Status**: ✓ Implemented, ⚠ Needs REM-09 integration  

**Required methods**:
```python
class SMPStore:
    def create_smp(self, ...) -> SMP:
        # §4.3 creation protocol
        
    def append_aa(self, smp_id: str, aa_type: str, content: dict, producer: str) -> bool:
        # §5.3 AA attachment
        # REM-09: Integrate AA_Catalog here
        
    def promote_classification(self, smp_id: str, new_classification: str) -> bool:
        # §6.2 monotonic ladder enforcement
        # §8.3 promotion pipeline for canonical transition
        
    def get_smp(self, smp_id: str) -> Optional[SMP]:
        # Read accessor for UWM
        
    def get_all_smps_by_classification(self, classification: str) -> list[SMP]:
        # Query interface for protocols
```

**REM-09 integration**:
- Import AA_Catalog module
- Instantiate catalog in append_aa()
- Add indexed lookup methods per §5.5

### 5.3 AA_Catalog.py

**Spec Reference**: §5.5  
**Path**: `CSP_Core/Unified_Working_Memory/AA_Catalog.py`  
**Status**: ⚠ Exists but not integrated  

**Required methods** (entailed from §5.5):
```python
class AACatalog:
    def add_aa(self, aa: dict) -> None:
        # Append AA to catalog
        
    def get_aa_by_index(self, index: int) -> Optional[dict]:
        # Retrieve nth AA
        
    def get_aas_by_type(self, aa_type: str) -> list[dict]:
        # Filter by type
        
    def get_aas_by_producer(self, producer: str) -> list[dict]:
        # Filter by producer
        
    def get_catalog_length(self) -> int:
        # Count total AAs
```

**Integration target**: SMP_Store.append_aa() (§16.1 REM-09)

### 5.4 Classification_Tracker.py

**Spec Reference**: §6  
**Path**: `CSP_Core/Unified_Working_Memory/Classification_Tracker.py`  
**Status**: ✓ Implemented  

**Required methods** (entailed from §6.2):
```python
class ClassificationTracker:
    def validate_transition(self, current: str, target: str) -> tuple[bool, Optional[str]]:
        # Monotonic ladder enforcement
        
    def is_terminal(self, classification: str) -> bool:
        # Check if rejected (terminal state)
```

### 5.5 UWM_Access_Control.py

**Spec Reference**: §9.2  
**Path**: `CSP_Core/Unified_Working_Memory/UWM_Access_Control.py`  
**Status**: ✓ Implemented  

**Required classes**:
```python
class UWMWriteRole(Enum):
    LOGOS_AGENT_ONLY = "logos_agent"
    SUB_AGENT = "sub_agent"
    PROTOCOL = "protocol"

class UWMReadAPI:
    def get_smp(self, smp_id: str, requester_role: UWMWriteRole) -> Optional[SMP]:
        # Role-based read access
        
    def query_smps(self, filters: dict, requester_role: UWMWriteRole) -> list[SMP]:
        # Filtered query interface
```

### 5.6 Promotion_Evaluator.py

**Spec Reference**: §8.3  
**Path**: `CSP_Core/Promotion_Evaluator.py`  
**Status**: ✓ Implemented  

**Required method** (entailed from §8.3):
```python
class PromotionEvaluator:
    def evaluate(self, smp: SMP) -> tuple[str, str]:
        """
        Returns: (decision, rationale)
        decision: "PROMOTE" or "REJECT"
        rationale: Explanation string
        
        Evaluation criteria (§8.3):
        - SMP classification must be 'provisional'
        - SMP must have non-empty AA catalog
        - Hash integrity verified
        - No privation flags set
        """
```

### 5.7 Canonical_SMP_Producer.py

**Spec Reference**: §8.3  
**Path**: `CSP_Core/Canonical_SMP_Producer.py`  
**Status**: ✓ Implemented  

**Required method** (entailed from §8.3):
```python
class CanonicalSMPProducer:
    def produce(self, smp: SMP) -> SMP:
        """
        Converts provisional SMP to canonical SMP.
        
        Transformations:
        - Recompute content_hash to include full AA chain
        - Change identity prefix: SMP: → C-SMP:
        - Set classification to 'canonical'
        - Freeze all fields (full immutability)
        
        Returns: Canonical SMP
        """
```

### 5.8 CSP_Canonical_Store.py

**Spec Reference**: §7.2  
**Path**: `CSP_Core/CSP_Canonical_Store.py`  
**Status**: ✓ Implemented  

**Required methods** (entailed from §7.2):
```python
class CSPCanonicalStore:
    def store_csmp(self, csmp: SMP) -> bool:
        # Persist canonical SMP
        
    def retrieve_csmp(self, csmp_id: str) -> Optional[SMP]:
        # Read accessor
        
    def query_csmps(self, filters: dict) -> list[SMP]:
        # Query interface for protocols
```

### 5.9 Boundary_Validators.py

**Spec Reference**: §9.3  
**Path**: `Logos_Core/Orchestration/Boundary_Validators.py`  
**Status**: ✓ Implemented (7 validators per §16.1)  

**Required validator** (entailed from §9.3):
```python
def validate_agent_write_boundary(actor: str, operation: str) -> tuple[bool, Optional[str]]:
    """
    Enforces Logos Agent sovereignty over EA writes.
    
    Authorization matrix:
    - logos_agent: create_smp, append_aa, promote_classification
    - sub_agent_i1/i2/i3: None (proposals only)
    - protocol_*: None (read-only)
    
    Returns: (is_authorized, denial_reason)
    """
```

### 5.10 Agent_Wrappers.py

**Spec Reference**: §8.1, §9.1, §12.1  
**Path**: `Logos_Core/Orchestration/Agent_Wrappers.py`  
**Status**: ⚠ Stubs only (REM-01 blocker)  

**Required implementation** (entailed from §8.1, §12.1):
```python
class LogosAgentWrapper:
    def __init__(self, uwm: UWM, scp: SCP, csp: CSP, mtp: MTP, arp: ARP, operational_logger: Logger):
        # Subsystem injection per REM-01
        
    def _on_tick(self, task_context: dict) -> dict:
        """
        Per-tick processing:
        1. Route task to appropriate sub-agents
        2. Collect AA proposals from sub-agent tick_results
        3. Return proposals to _process_task()
        """
        
    def _process_task(self, task: dict) -> dict:
        """
        Multi-tick EA lifecycle orchestration:
        1. Review AA proposals from _on_tick()
        2. Validate proposals via Boundary_Validators
        3. Attach approved AAs via SMP_Store.append_aa()
        4. Evaluate classification promotion
        5. Trigger promotion pipeline if provisional → canonical
        6. Return tick_result with EA state
        """
        
class SubAgentWrapper:  # I1, I2, I3
    def _on_tick(self, context: dict) -> dict:
        """
        Sub-agent processing:
        1. Analyze task context
        2. Generate AA proposal
        3. Return proposal in tick_result (no direct EA writes)
        """
```

### 5.11 Runtime_Loop.py

**Spec Reference**: §12, §15.3  
**Path**: `Logos_Core/Orchestration/Runtime_Loop.py`  
**Status**: ⚠ Partial (REM-01 blocker)  

**Required additions** (entailed from §12, §15.3):
```python
class RuntimeLoop:
    def execute_tick(self, tick_num: int) -> dict:
        """
        Per-tick EA lifecycle:
        1. Invoke Logos Agent _on_tick()
        2. Invoke Logos Agent _process_task()
        3. Log EA lifecycle events to operational_logger
        4. Return tick_result with EA state summary
        
        EA-specific logging (§15.3):
        - ea_created events
        - Tick-level EA state summary (active SMPs, classifications)
        """
```

---

## 6. Ambiguities and Escalation Points

### 6.1 AA Catalog Integration Strategy

**Ambiguity**: §5.5 specifies AA_Catalog module exists but §16.1 notes it's not integrated. Spec does not prescribe exact wiring pattern.

**Resolution required**:
- Should AA_Catalog be instantiated per-SMP or as singleton?
- Should AA_Catalog replace list storage in SMP.append_artifacts or augment it?
- Should indexed lookup methods be exposed via SMP_Store or AA_Catalog directly?

**Recommendation**: Escalate to architecture review. Do not guess.

### 6.2 Identity Format Migration Path

**Ambiguity**: §3.2.1 provides forward compatibility guidance for V1.1+ three-part identity format (`SMP:<agent_id>:<session_id>:<seq>`), but does not specify migration mechanism from V1 two-part format.

**Resolution required**:
- How should V1 → V1.1 migration handle identity collisions?
- Should V1.1 accept both formats during transition?
- Should canonical store enforce format versioning?

**Recommendation**: Not blocking for V1 implementation. Defer to V1.1 planning.

### 6.3 Promotion Evaluation Criteria

**Ambiguity**: §8.3 states PromotionEvaluator.evaluate() must assess provisional SMPs for canonicalization, but does not specify exact evaluation criteria beyond "non-empty AA catalog" and "hash integrity."

**Resolution required**:
- What minimum AA count qualifies?
- What AA types are required (e.g., must include at least one `evaluation` AA)?
- Should temporal criteria apply (e.g., minimum age, tick count)?

**Recommendation**: Escalate to spec clarification. Current implementation likely has heuristics not documented in spec.

### 6.4 Tick Budget Exhaustion Recovery

**Ambiguity**: §12.2 specifies 50-tick budget with governance_annotation on exhaustion, but does not specify recovery path.

**Resolution required**:
- Is exhausted EA terminal (rejected)?
- Can operator manually extend budget?
- Should MTP provide resumption mechanism?

**Recommendation**: Escalate to governance policy review.

---

## 7. Testing Strategy

### 7.1 Unit Tests

**SMP_Store tests**:
- create_smp() with valid inputs → success
- create_smp() with inert violation → InertViolation exception
- create_smp() with identity collision → UniquenessViolation exception
- append_aa() to non-canonical SMP → success
- append_aa() to canonical SMP → ImmutabilityViolation
- append_aa() to rejected SMP → TerminalStateError
- promote_classification() forward transition → success
- promote_classification() backward transition (non-rejected) → MonotonicLadderViolation

**Classification_Tracker tests**:
- validate_transition() all forward paths → valid
- validate_transition() conditional → rejected → valid
- validate_transition() canonical → provisional → invalid
- is_terminal() rejected → True
- is_terminal() canonical → False

**Boundary_Validators tests**:
- validate_agent_write_boundary("logos_agent", "create_smp") → authorized
- validate_agent_write_boundary("sub_agent_i1", "create_smp") → denied
- validate_agent_write_boundary("protocol_csp", "append_aa") → denied

### 7.2 Integration Tests

**EA Lifecycle Flow** (requires REM-01 completion):
1. Create task
2. Logos Agent creates SMP
3. Sub-agents propose AAs
4. Logos Agent attaches AAs
5. Classification promotes conditional → provisional → canonical
6. Canonical SMP persisted to CSP Canonical Store
7. Verify all lifecycle events logged to SOP

**Multi-Tick Processing** (requires REM-01 completion):
1. Create EA requiring 3-tick processing
2. Verify MTP provides continuity context via context_link AAs
3. Verify Logos Agent routing state machine persists across ticks
4. Verify final EA state correct after tick 3

### 7.3 Compliance Tests

**Inertness validation**:
- Payload with executable code → rejected
- Payload with scheduling directive → rejected
- Payload with template identifier → rejected
- Payload with valid inert content → accepted

**Immutability enforcement**:
- Attempt to modify sealed SMP.identity → exception
- Attempt to modify sealed SMP.payload → exception
- Attempt to remove AA from catalog → exception
- Governed mutability (classification, append_artifacts) → allowed per rules

---

## 8. Deployment Checklist

**Pre-deployment validation**:
- [ ] REM-01 (P3.1) complete: Agent wrappers operational
- [ ] REM-02 complete: tick_result schema compliant with P1-IF-07
- [ ] REM-06 complete: UWM __init__.py duplicates removed
- [ ] REM-09 complete: AA_Catalog integrated into SMP_Store
- [ ] REM-07 complete: 19 operational logging points active
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All compliance tests pass
- [ ] Spec ambiguities resolved or documented as known limitations

**Operational readiness**:
- [ ] SOP operational logger configured and receiving EA lifecycle events
- [ ] CSP Canonical Store persistence layer operational
- [ ] UWM session lifecycle (clear on session end) verified
- [ ] Promotion pipeline (Evaluator → Producer → Canonical Store) end-to-end tested
- [ ] Authority boundaries enforced (Logos Agent sovereignty verified)

---

*End of implementation guide.*

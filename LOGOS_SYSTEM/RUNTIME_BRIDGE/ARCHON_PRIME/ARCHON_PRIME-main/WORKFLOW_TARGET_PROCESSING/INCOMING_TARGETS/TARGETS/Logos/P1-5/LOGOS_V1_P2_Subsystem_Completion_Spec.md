# LOGOS V1 — Phase P2: Subsystem Completion Design Specification

**Document ID:** `LOGOS-V1-P2-SUBSYSTEM-COMPLETION`
**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires human governance ratification
**Parent:** `LOGOS_V1_Operational_Readiness_Blueprint.md`
**Depends On:** `LOGOS-V1-P1-RUNTIME-ACTIVATION` (P1 complete, tick loop functional)
**Phase:** P2 (second development phase)
**Date:** 2026-03-01

---

## 0. Cross-Reference Index

| Reference ID | Section | Description |
|---|---|---|
| P2.1 | §2 | UWM Implementation |
| P2.2 | §3 | SCP Core Orchestrator |
| P2.3 | §4 | CSP Canonical Promotion Path |
| P2.4 | §5 | DRAC Session Reconstruction |
| P2.5 | §6 | EMP Deployment |
| P2.6 | §7 | SOP Runtime Observation |
| P2-IF-01 | §2.2 | SMP runtime schema |
| P2-IF-02 | §2.3 | AA runtime schema |
| P2-IF-03 | §2.5 | UWM read API contract |
| P2-IF-04 | §2.6 | UWM write API contract |
| P2-IF-05 | §3.3 | SCPOrchestrator interface |
| P2-IF-06 | §4.3 | Promotion evaluator interface |
| P2-IF-07 | §5.3 | DRAC assembler interface |
| P2-IF-08 | §6.3 | EMP wiring contract |
| P2-IF-09 | §7.3 | Runtime observer interface |

---

## 1. Phase Overview

P2 replaces six stub subsystems with operational implementations. All six workstreams may proceed in parallel after P1 completion. Each workstream is independently testable. No workstream depends on another P2 workstream.

**Prerequisite:** P1 complete (tick loop functional with stub agents).

**Post-condition:** Each subsystem is individually operational and ready for end-to-end wiring in P3.

| Workstream | Replaces | Critical for V1? |
|---|---|---|
| P2.1 UWM | Stub `__init__.py` (NotImplementedError) | YES — irreducible minimum |
| P2.2 SCP Orchestrator | Stub `run_cognition` (NotImplementedError) | YES — I1 cognitive path |
| P2.3 CSP Promotion | No implementation exists | YES — canonicalization path |
| P2.4 DRAC Assembler | Empty `DRAC_Core` shell | NO — V1 uses static loading (deferrable) |
| P2.5 EMP Deployment | Wiring only (modules built) | NO — V1 operates without Coq verification (deferrable) |
| P2.6 SOP Observer | No runtime observer exists | NO — V1 operates with startup logging only (deferrable) |

V1 irreducible minimum: P2.1 + P2.2 + P2.3. The remaining three are high-value but deferrable to V1.1.

---

## 2. P2.1 — UWM Implementation

### 2.1 Problem Statement

The Unified Working Memory stub exports `UWMContext`, `UWMStore`, `read`, and `write`. `read` and `write` raise `NotImplementedError`. `UWMStore` is a trivial `dict` wrapper with no governance, no provenance, no classification tracking, and no AA cataloging.

The SMP/AA design packet (Phase-2.1.1) provides comprehensive governance specs for SMP schema, classification ladder, cataloging, and shared AA schema. None of this is implemented at runtime.

Without operational UWM, there is nowhere for the cognitive loop to store SMPs. P3.1 (end-to-end SMP pipeline) cannot function.

### 2.2 SMP Runtime Schema (P2-IF-01)

Derived from `SMP_Canonical_Spec.md` (Phase-2.1.1). This is the in-memory representation. Not a persistence schema.

```python
@dataclass
class SMPHeader:
    smp_id: str                          # "SMP:{hash}" — unique, immutable
    smp_type: str                        # "observation" | "plan_fragment" | "hypothesis" | "analytic" | "audit_event"
    classification_state: str            # "rejected" | "conditional" | "provisional" | "canonical"
    created_at: float                    # time.time() at creation
    created_by: str                      # "logos_agent" (only Logos Agent creates SMPs)
    session_id: str                      # universal session ID

@dataclass
class SMPProvenance:
    source: str                          # originating entity
    acquisition_path: str                # how it entered the system
    content_hash: str                    # SHA-256 of payload
    chain_of_custody: List[str]          # ordered list of handlers

@dataclass
class SMPConfidence:
    status: str                          # "draft" | "asserted" | "revoked"
    confidence: float                    # [0.0, 1.0]

@dataclass
class SMPPrivation:
    redaction_compatible: bool
    quarantine_compatible: bool
    partial_elision_allowed: bool

@dataclass
class SMPAppendArtifacts:
    aa_hashes: List[str]                 # ordered list of AA content hashes
    aa_count: int                        # len(aa_hashes)
    last_aa_added_at: Optional[float]    # timestamp of last AA append

@dataclass
class SMP:
    header: SMPHeader
    provenance: SMPProvenance
    confidence: SMPConfidence
    privation: SMPPrivation
    append_artifacts: SMPAppendArtifacts
    payload: Dict[str, Any]              # inert structured content — no executable code

    def validate(self) -> bool:
        """Fail-closed schema validation. Returns True or raises SMPValidationError."""
```

**Invariants (from SMP_Invariants.md):**
- `classification_state` follows monotonic ladder: rejected → conditional → provisional → canonical. Never regresses.
- `append_artifacts` is append-only. `aa_hashes` never shrinks.
- `payload` is immutable after creation. All cognitive change is via AAs.
- No SMP is deleted. Reclassification, supersedence, and archival only.
- `privation` metadata is mandatory. Absence is a hard error.

### 2.3 AA Runtime Schema (P2-IF-02)

Derived from `SMP_AA_Shared_Schema_Appendix.md`.

```python
@dataclass
class AppendArtifact:
    aa_id: str                           # unique AA identifier
    aa_type: str                         # "I1AA" | "I2AA" | "I3AA" | "LogosAA" | "ProtocolAA"
    aa_origin_type: str                  # "agent" | "protocol"
    originating_entity: str              # "I1" | "I2" | "I3" | "Logos" | "RGE" | "EMP" | etc.
    bound_smp_id: str                    # immutable reference to parent SMP
    bound_smp_hash: str                  # hash of the bound SMP at time of AA creation
    creation_timestamp: float
    aa_hash: str                         # SHA-256 of this AA's content
    classification_state: str            # follows same ladder as SMP
    content: Dict[str, Any]              # analytic results, reasoning outputs, etc.

    def validate(self) -> bool:
        """Fail-closed AA validation."""
```

**Invariants:**
- AAs never modify SMP content.
- AAs never directly promote an SMP.
- AAs support promotion by providing evidence that Logos Agent evaluates.
- Canonical SMPs (C-SMPs) are closed to further AAs.

### 2.4 UWM Architecture

```
UWM (session-scoped, in-memory)
├── SMP_Store          — Dict[smp_id, SMP]
├── AA_Catalog         — Dict[aa_id, AppendArtifact] + index by bound_smp_id
├── Access_Control     — role + scope + provenance gate on all reads
└── Classification_Tracker — enforces monotonic ladder transitions
```

No persistence. No disk I/O. Session-scoped only. When session terminates, UWM state is gone. This is by design per DRAC reconstruction model.

### 2.5 UWM Read API (P2-IF-03)

Governed reads per Phase-2.2 UWM Read-Only API Spec.

```python
class UWMReadAPI:

    def get_smp(self, smp_id: str, requester_role: str) -> Optional[SMP]:
        """
        Retrieve SMP by ID.

        Requester roles:
        - "logos_agent" — full access to all SMPs
        - "agent_i1" — access to SMPs routed to SCP (by Logos Agent routing table)
        - "agent_i2" — access to SMPs routed to MTP
        - "agent_i3" — access to SMPs routed to ARP
        - "protocol" — read-only access to SMPs in their protocol scope

        On role mismatch: return None (deny-by-default, no error leak).
        On missing SMP: return None.
        On provenance failure: return None, emit audit event.
        """

    def get_aas_for_smp(self, smp_id: str, requester_role: str) -> List[AppendArtifact]:
        """Return all AAs bound to this SMP, ordered by creation_timestamp."""

    def get_smps_by_classification(self, classification_state: str) -> List[SMP]:
        """Return all SMPs with the given classification. Logos Agent only."""

    def get_smp_count(self) -> int:
        """Total SMP count. Unrestricted."""

    def get_aa_count(self) -> int:
        """Total AA count. Unrestricted."""
```

### 2.6 UWM Write API (P2-IF-04)

Write access is restricted to Logos Agent only. No other entity may create SMPs or modify classification state.

```python
class UWMWriteAPI:

    def create_smp(
        self,
        smp_type: str,
        payload: Dict[str, Any],
        session_id: str,
        source: str,
    ) -> SMP:
        """
        Create and store a new SMP.

        Caller: Logos Agent ONLY.
        Initial classification_state: "conditional".
        Provenance auto-populated from arguments.
        content_hash computed from payload.
        smp_id generated as "SMP:{sha256(payload + timestamp)}".

        Returns the created SMP.
        Raises SMPCreationError on validation failure.
        """

    def append_aa(
        self,
        bound_smp_id: str,
        aa_type: str,
        originating_entity: str,
        content: Dict[str, Any],
    ) -> AppendArtifact:
        """
        Create and append an AA to an existing SMP.

        Caller: Any authorized agent or protocol (via Logos Agent delegation).
        Validates bound SMP exists and is not canonical (closed to AAs).
        Updates SMP's append_artifacts catalog.
        aa_hash computed from content.

        Returns the created AA.
        Raises AAAppendError if SMP is canonical or missing.
        """

    def promote_classification(
        self,
        smp_id: str,
        target_state: str,
    ) -> SMP:
        """
        Promote SMP classification state.

        Caller: Logos Agent ONLY.
        Validates monotonic ladder (conditional → provisional → canonical).
        Raises ClassificationError on regression or invalid transition.

        Returns the updated SMP.
        """

    def reject_smp(self, smp_id: str) -> SMP:
        """
        Set classification to "rejected".

        Caller: Logos Agent ONLY.
        Rejected SMPs remain in store (non-deletion principle) but are excluded from active processing.
        """
```

### 2.7 Classification Tracker

```python
CLASSIFICATION_LADDER = {
    "rejected": 0,
    "conditional": 1,
    "provisional": 2,
    "canonical": 3,
}

class ClassificationTracker:

    @staticmethod
    def validate_transition(current: str, target: str) -> bool:
        """
        Returns True if transition is valid (monotonic, non-regressing).

        Valid transitions:
        - conditional → provisional
        - conditional → canonical (skip allowed if all requirements met)
        - provisional → canonical
        - Any state → rejected (rejection is always valid)

        Invalid:
        - canonical → anything (canonical is terminal)
        - provisional → conditional (regression)
        - rejected → anything except rejected (rejected is terminal unless governance override)
        """
        if target == "rejected":
            return current != "canonical"  # cannot reject canonical
        current_rank = CLASSIFICATION_LADDER.get(current, -1)
        target_rank = CLASSIFICATION_LADDER.get(target, -1)
        if current == "rejected":
            return False  # rejected is terminal
        return target_rank > current_rank
```

### 2.8 File Manifest

| File | Path | Purpose |
|---|---|---|
| SMP_Schema.py | `CSP_Core/Unified_Working_Memory/` | SMP + AA dataclasses, validation |
| SMP_Store.py | `CSP_Core/Unified_Working_Memory/` | In-memory SMP dict + index |
| AA_Catalog.py | `CSP_Core/Unified_Working_Memory/` | In-memory AA dict + smp_id index |
| UWM_Access_Control.py | `CSP_Core/Unified_Working_Memory/` | Role-scoped read gating |
| Classification_Tracker.py | `CSP_Core/Unified_Working_Memory/` | Monotonic ladder enforcement |
| `__init__.py` (rewrite) | `CSP_Core/Unified_Working_Memory/` | Replace stub with operational exports |

### 2.9 Integration Points

| Consumer | What it needs from UWM |
|---|---|
| LogosAgentParticipant (P1) | `create_smp()`, `promote_classification()`, `get_smps_by_classification()` |
| I1AgentParticipant (P1) | `get_smp()` (read routed SMPs), `append_aa()` (write I1AA) |
| I2AgentParticipant (P1) | `get_smp()`, `append_aa()` (write I2AA) |
| I3AgentParticipant (P1) | `get_smp()`, `append_aa()` (write I3AA) |
| P2.3 CSP Promotion | `get_aas_for_smp()`, `promote_classification()` |
| P3.1 SMP Pipeline | All read + write APIs |

### 2.10 Verification

```bash
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory.SMP_Store import SMPStore
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory.SMP_Schema import SMP
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory.Classification_Tracker import ClassificationTracker

store = SMPStore()

# Create SMP
smp = store.create_smp(smp_type='observation', payload={'input': 'test'}, session_id='sess-01', source='logos_agent')
assert smp.header.classification_state == 'conditional'
assert store.get_smp_count() == 1

# Append AA
aa = store.append_aa(bound_smp_id=smp.header.smp_id, aa_type='I1AA', originating_entity='I1', content={'analysis': 'stub'})
assert store.get_aa_count() == 1

# Promote
smp2 = store.promote_classification(smp.header.smp_id, 'provisional')
assert smp2.header.classification_state == 'provisional'

# Monotonic enforcement
try:
    store.promote_classification(smp.header.smp_id, 'conditional')
    assert False, 'Should have raised'
except Exception:
    pass

# Canonical is terminal for AAs
smp3 = store.promote_classification(smp.header.smp_id, 'canonical')
try:
    store.append_aa(bound_smp_id=smp.header.smp_id, aa_type='I2AA', originating_entity='I2', content={})
    assert False, 'Should have raised'
except Exception:
    pass

print('ALL PASS')
"
```

### 2.11 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_1_UWM_Implementation_Lock.json
```

---

## 3. P2.2 — SCP Core Orchestrator

### 3.1 Problem Statement

`SCP_Core/__init__.py` exports `CognitionContext`, `CognitionResult`, and `run_cognition` — all stubs. `run_cognition` raises `NotImplementedError`.

Meanwhile, the I1 Agent tool library contains a complete `analysis_runner.py` that calls MVS and BDN adapters (with both stub and real implementations), produces `SCPAnalysisBundle` (mvs result, bdn result, summary), and an `i1aa_binder.py` that packages results into I1AA format.

The gap: nothing connects the I1AgentParticipant's `execute_tick()` to these existing tool libraries. The SCP orchestrator bridges this.

### 3.2 Existing Components (Verified)

| Module | Status | What It Does |
|---|---|---|
| `analysis_runner.py` | Operational | `run_analysis()` calls MVS + BDN adapters, returns `SCPAnalysisBundle` |
| `mvs_adapter.py` | Operational | `IMVSAdapter` interface + `StubMVSAdapter` |
| `bdn_adapter.py` | Operational | `IBDNAdapter` interface + `StubBDNAdapter` |
| `smp_intake.py` | Operational | `load_smp()` validates and parses SMP input |
| `i1aa_binder.py` | Operational | `I1AABinder.bind()` packages analysis into I1AA dict |
| `sign_grounding.py` | Operational | Sign grounding adapter for SCP analysis |
| `SCP_Core/__init__.py` | STUB | `run_cognition` raises NotImplementedError |

### 3.3 SCPOrchestrator Interface (P2-IF-05)

```python
class SCPOrchestrator:
    """
    Bridges SMP data from UWM to the I1 analysis pipeline.
    Does NOT contain reasoning logic — delegates to existing adapters.
    """

    def __init__(
        self,
        mvs_adapter: Optional[IMVSAdapter] = None,
        bdn_adapter: Optional[IBDNAdapter] = None,
    ) -> None:
        """
        Constructs SCP orchestrator with pluggable adapters.
        Defaults to stub adapters if none provided.
        """

    def analyze(self, smp: SMP) -> AppendArtifact:
        """
        Run full SCP analysis on an SMP and return an I1AA.

        Sequence:
        1. Extract smp_id and content_hash from SMP header/provenance
        2. Call run_analysis(smp_id, input_hash, payload_ref=smp.payload)
        3. Receive SCPAnalysisBundle (mvs, bdn, summary)
        4. Call I1AABinder.bind(smp_id, analysis_bundle)
        5. Return I1AA as AppendArtifact

        Fail-closed: any exception in analysis pipeline produces a
        rejection AA rather than propagating the error.
        """

    def analyze_batch(self, smps: List[SMP]) -> List[AppendArtifact]:
        """Analyze multiple SMPs. Order preserved. Each independently fail-closed."""
```

### 3.4 Wiring to I1AgentParticipant

The I1AgentParticipant (from P1, `Agent_Wrappers.py`) currently has a stub `_on_tick()`. After P2.2:

```python
# In I1AgentParticipant._on_tick():
def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for packet in self._received_packets:
        payload = packet.payload
        if payload.get("type") == "smp_route_to_i1":
            smp_id = payload["content"]["smp_id"]
            smp = self._uwm_read.get_smp(smp_id, requester_role="agent_i1")
            if smp is None:
                continue
            i1aa = self._scp_orchestrator.analyze(smp)
            # Emit I1AA back to Logos Agent via StatePacket
            return {
                "type": "i1_analysis_complete",
                "content": {
                    "smp_id": smp_id,
                    "aa_id": i1aa.aa_id,
                    "aa_type": "I1AA",
                },
            }
    return None
```

This wiring happens in P3.1 (end-to-end pipeline), NOT in P2.2. P2.2 only builds and tests SCPOrchestrator in isolation.

### 3.5 SCP_Core `__init__.py` Rewrite

Replace the stub:

```python
from .SCP_Orchestrator import SCPOrchestrator

__all__ = [
    "SCPOrchestrator",
]
```

`CognitionContext`, `CognitionResult`, and `run_cognition` are deprecated. No downstream module should import them. If any legacy imports exist, they break deliberately (fail-closed is preferable to silent stub behavior).

### 3.6 File Manifest

| File | Path | Purpose |
|---|---|---|
| SCP_Orchestrator.py | `SCP_Core/` | SCPOrchestrator class |
| `__init__.py` (rewrite) | `SCP_Core/` | Replace stub exports |

### 3.7 Verification

```bash
python3 -c "
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core.SCP_Orchestrator import SCPOrchestrator

orch = SCPOrchestrator()  # defaults to stub adapters

# Create mock SMP (matching P2-IF-01 schema)
class MockSMP:
    class header:
        smp_id = 'SMP:test001'
        classification_state = 'conditional'
    class provenance:
        content_hash = 'abc123'
    payload = {'input': 'test data'}

result = orch.analyze(MockSMP())
assert result.aa_type == 'I1AA'
assert result.bound_smp_id == 'SMP:test001'
print('ALL PASS')
"
```

### 3.8 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_2_SCP_Orchestrator_Lock.json
```

---

## 4. P2.3 — CSP Canonical Promotion Path

### 4.1 Problem Statement

No promotion evaluator exists. The classification ladder is defined in governance docs but has no runtime enforcement. Logos Agent has no mechanism to evaluate whether an SMP has accumulated sufficient AAs for promotion, and no mechanism to produce a Canonical SMP (C-SMP).

### 4.2 Promotion Requirements (from Governance)

Per `SMP_AA_Shared_Schema_Appendix.md` and `SMP_Classification_Ladder.md`:

**Conditional → Provisional:**
- At least one AA from any agent (I1, I2, or I3)
- No unresolved conflict AAs

**Provisional → Canonical:**
- I1AA present (SCP analysis complete)
- I3AA present (ARP reasoning complete)
- I2AA present (MTP egress critique complete)
- No unresolved conflict AAs
- EMP proof coverage when available (V1: optional, EMP may be deferred)
- Logos Agent explicit approval

**Canonicalization produces a C-SMP:**
- New immutable SMP derived from source SMP + all AAs
- C-SMP is closed to further AAs
- C-SMP lives in CSP
- C-SMP retains full derivation lineage

### 4.3 Promotion Evaluator Interface (P2-IF-06)

```python
class PromotionEvaluator:
    """
    Evaluates whether an SMP is ready for promotion.
    Does NOT promote — returns evaluation result.
    Logos Agent makes the final decision.
    """

    def __init__(self, uwm_read: UWMReadAPI) -> None:
        """Constructs evaluator with read access to UWM."""

    def evaluate_for_provisional(self, smp_id: str) -> PromotionEvaluation:
        """
        Check if SMP meets criteria for conditional → provisional.

        Returns PromotionEvaluation:
        - eligible: bool
        - missing_requirements: List[str]
        - aa_summary: Dict[str, int]  (count by aa_type)
        - conflicts: List[str]  (conflict AA ids, if any)
        """

    def evaluate_for_canonical(self, smp_id: str) -> PromotionEvaluation:
        """
        Check if SMP meets criteria for provisional → canonical.

        Checks:
        1. Current state is "provisional"
        2. I1AA present
        3. I3AA present
        4. I2AA present
        5. No unresolved conflict AAs
        6. EMP proof AA present (optional for V1, controlled by flag)

        Returns PromotionEvaluation with detailed breakdown.
        """


@dataclass
class PromotionEvaluation:
    eligible: bool
    current_state: str
    target_state: str
    missing_requirements: List[str]
    aa_summary: Dict[str, int]
    conflicts: List[str]
    emp_proof_available: bool
```

### 4.4 Canonical SMP Producer

```python
class CanonicalSMPProducer:
    """
    Produces a Canonical SMP (C-SMP) from a source SMP and its AAs.
    """

    def produce(self, source_smp: SMP, aas: List[AppendArtifact]) -> SMP:
        """
        Create a new C-SMP.

        The C-SMP:
        - Gets a new smp_id: "C-SMP:{hash}"
        - classification_state: "canonical"
        - payload: source SMP payload (unchanged)
        - append_artifacts: frozen copy of all AA hashes
        - provenance.chain_of_custody: includes "canonical_producer"
        - New content_hash covering source + all AAs

        The source SMP is NOT mutated. It remains in UWM
        with its classification promoted to "canonical" by Logos Agent.

        Returns the new C-SMP.
        """
```

### 4.5 CSP Storage for C-SMPs

C-SMPs live in CSP, separate from UWM working memory. CSP is the canonical knowledge store.

```python
class CSPCanonicalStore:
    """
    Session-scoped store for Canonical SMPs.
    Separate from UWM (which holds working-state SMPs).
    """

    def __init__(self) -> None:
        self._store: Dict[str, SMP] = {}

    def store(self, csmp: SMP) -> None:
        """Store a C-SMP. Validates classification_state == 'canonical'."""
        if csmp.header.classification_state != "canonical":
            raise CSPViolation("Only canonical SMPs may enter CSP store")
        if csmp.header.smp_id in self._store:
            raise CSPViolation(f"Duplicate C-SMP: {csmp.header.smp_id}")
        self._store[csmp.header.smp_id] = csmp

    def get(self, csmp_id: str) -> Optional[SMP]:
        return self._store.get(csmp_id)

    def list_all(self) -> List[SMP]:
        return list(self._store.values())

    def count(self) -> int:
        return len(self._store)
```

### 4.6 File Manifest

| File | Path | Purpose |
|---|---|---|
| Promotion_Evaluator.py | `CSP_Core/` | PromotionEvaluator + PromotionEvaluation |
| Canonical_SMP_Producer.py | `CSP_Core/` | C-SMP construction |
| CSP_Canonical_Store.py | `CSP_Core/` | Session-scoped canonical storage |

### 4.7 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_3_CSP_Promotion_Lock.json
```

---

## 5. P2.4 — DRAC Session Reconstruction

### 5.1 Problem Statement

`DRAC_Core.py` provides phase-tracking (`start_phase`, `complete_phase`, `status`) but no actual assembly logic. The `DRAC_Invariables` directory contains 15+ semantic axiom files, 6+ semantic context files, orchestration overlays, and call registries — but nothing loads, resolves dependencies, or produces a session artifact from them.

V1 can operate with static module loading (import statements). Full dynamic reconstruction is the architectural target but not a V1 blocker.

**V1 Scope:** Simplified DRAC assembler that scans canonical directories, validates module presence, produces a session artifact documenting what was loaded. No dynamic import graph resolution. No topological sort. No dead code detection. Those are V1.1.

### 5.2 Existing DRAC Inventory

```
DRAC_Core/DRAC_Invariables/
├── SEMANTIC_AXIOMS/           (15+ .py files)
│   ├── 3PDN_Constraint.py
│   ├── Agent_Activation_Gate.py
│   ├── Evidence_Chain.py
│   ├── Global_Bijective_Recursion_Core.py
│   ├── Hypostatic_ID_Validator.py
│   ├── Invariant_Constraints.py
│   ├── Monolith_Runtime.py
│   ├── Necessary_Existence_Core.py
│   ├── Runtime_Context_Initializer.py
│   ├── Runtime_Input_Sanitizer.py
│   ├── Runtime_Mode_Controller.py
│   ├── Semantic_Capability_Gate.py
│   ├── Temporal_Supersession.py
│   ├── Trinitarian_Alignment_Core.py
│   ├── Trinitarian_Logic_Core.py
│   ├── UWM_Ingestion.py
│   ├── UWM_Validator.py
│   └── SEMANTIC_AXIOMS.json (catalog)
├── SEMANTIC_CONTEXTS/         (6+ .py files)
│   ├── Agent_Policy_Decision_Context.py
│   ├── Bootstrap_Runtime_Context.py
│   ├── Privation_Handling_Context.py
│   ├── Runtime_Mode_Context.py
│   ├── Trinitarian_Optimization_Context.py
│   └── SEMANTIC_CONTEXTS_CATALOG.json
├── ORCHESTRATION_AND_ENTRYPOINTS/
│   └── Proposed_Orchestration_Overlays.json
└── APPLICATION_FUNCTIONS/     (call registries)
```

### 5.3 DRAC Assembler Interface (P2-IF-07)

```python
class DRACAssembler:
    """
    V1 session reconstruction: scan, validate, document.
    Does NOT dynamically import or execute modules.
    """

    def __init__(self, drac_root: str) -> None:
        """
        drac_root: path to DRAC_Core/DRAC_Invariables/
        """

    def scan(self) -> AssemblyScan:
        """
        Scan all canonical directories.

        Returns AssemblyScan:
        - axioms_found: List[str] (filenames)
        - contexts_found: List[str]
        - registries_found: List[str]
        - overlays_found: List[str]
        - catalog_matches: bool (do .json catalogs match filesystem?)
        - missing_from_catalog: List[str]
        - extra_in_catalog: List[str]
        """

    def validate(self, scan: AssemblyScan) -> AssemblyValidation:
        """
        Validate scan results against governance requirements.

        Checks:
        - All catalog-listed modules exist on filesystem
        - No uncatalogued modules in directories (warning, not halt)
        - Catalog JSON files are valid JSON
        - Each .py file has canonical header

        Returns AssemblyValidation:
        - valid: bool
        - errors: List[str] (hard failures)
        - warnings: List[str] (non-blocking)
        """

    def produce_session_artifact(
        self, scan: AssemblyScan, validation: AssemblyValidation, session_id: str
    ) -> SessionArtifact:
        """
        Produce an immutable, auditable record of what was assembled.

        SessionArtifact:
        - session_id: str
        - timestamp: float
        - axioms_loaded: List[str]
        - contexts_loaded: List[str]
        - registries_loaded: List[str]
        - validation_result: AssemblyValidation
        - artifact_hash: str (SHA-256 of entire artifact)
        - frozen: True (immutable after creation)
        """


@dataclass(frozen=True)
class SessionArtifact:
    session_id: str
    timestamp: float
    axioms_loaded: Tuple[str, ...]
    contexts_loaded: Tuple[str, ...]
    registries_loaded: Tuple[str, ...]
    validation_errors: Tuple[str, ...]
    validation_warnings: Tuple[str, ...]
    artifact_hash: str
```

### 5.4 V1.1 Upgrade Path

| Capability | V1 | V1.1 |
|---|---|---|
| Directory scan | Yes | Yes |
| Catalog validation | Yes | Yes |
| Session artifact | Yes | Yes |
| Dynamic import graph | No | Yes — topological sort, cycle detection |
| Dependency resolution | No | Yes — per-module declared dependencies |
| Dead code detection | No | Yes — unreferenced module identification |
| Executable surface generation | No | Yes — session-specific import graph |

### 5.5 File Manifest

| File | Path | Purpose |
|---|---|---|
| DRAC_Assembler.py | `DRAC_Core/` | Scan + validate + produce artifact |
| Session_Artifact.py | `DRAC_Core/` | Frozen dataclass + hashing |

### 5.6 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_4_DRAC_Assembler_Lock.json
```

---

## 6. P2.5 — EMP Deployment

### 6.1 Problem Statement

All EMP modules are built (E1–E7). None are deployed. Deployment is blocked by four gates:

1. Coq environment resolution (coqc on PATH or jsCoq WebAssembly bridge)
2. PXL kernel axiom set formal declaration (canonicalize from PXLv3_SemanticModal.v)
3. MSPC Protocol operational readiness (for E7 coherence witness)
4. Logos Agent approval of MSPC routing path

### 6.2 Current EMP Module Status

| Module | Phase | Built? | Operational? | Deployment Blocker |
|---|---|---|---|---|
| EMP_Coq_Bridge | E1 | Yes | No | coqc path resolution |
| EMP_Meta_Reasoner | E2 | Yes | No | Depends on E1 |
| EMP_Proof_Index | E3 | Yes | No | Depends on E2 |
| EMP_Nexus (PostProcessGate v2) | E4 | Yes | Partial | Falls back to keyword tagging without E2 |
| EMP_Template_Engine | E5 | Yes | No | Depends on E3 |
| EMP_Abstraction_Engine | E6 | Yes | No | Depends on E3 |
| EMP_MSPC_Witness | E7 | Yes | No | Depends on MSPC + Logos Agent |

### 6.3 EMP Wiring Contract (P2-IF-08)

EMP deployment is sequential wiring, not new code. The modules exist. The integration connections do not.

**Wire 1: Coq Environment → EMP_Coq_Bridge**

```python
# EMP_Coq_Bridge needs to know how to invoke Coq.
# Option A: coqc subprocess
coq_bridge = EMP_Coq_Bridge(
    coqc_path="/usr/bin/coqc",       # or discovered via shutil.which("coqc")
    loadpath=[str(PXL_GATE_COQ_DIR)], # STARTUP/PXL_Gate/coq/
    timeout_seconds=30,
)

# Option B: jsCoq WebAssembly (if coqc unavailable)
# Requires browser environment — not applicable for V1 CLI mode
```

**Wire 2: EMP_Coq_Bridge → EMP_Meta_Reasoner**

```python
# Replace 14-line stub Meta_Reasoner with Coq-backed version
meta_reasoner = EMP_Meta_Reasoner(
    coq_bridge=coq_bridge,
    budget=1000,                      # reasoning budget per analysis
)
```

**Wire 3: EMP_Meta_Reasoner → EMP_Nexus PostProcessGate**

```python
# PostProcessGate already accepts optional meta_reasoner in constructor
post_gate = PostProcessGate(meta_reasoner=meta_reasoner)
# When meta_reasoner is present, PostProcessGate uses Coq-backed proof tagging
# When absent, it falls back to keyword-based provisional tagging
```

**Wire 4: EMP_Meta_Reasoner → MSPC PostProcessGate (cross-protocol)**

```python
# MSPC's PostProcessGate can also accept EMP_Meta_Reasoner for proof classification
# This wire enables the six-tier classification system:
# VERIFIED → PARTIAL → STRUCTURAL → UNVERIFIED → FAILED → TIMEOUT
```

**Wire 5: EMP_MSPC_Witness → Logos Agent routing (P3.3 concern)**

This wire is deferred to P3.3 (EMP ↔ MSPC coherence loop). Not a P2.5 concern.

### 6.4 V1 EMP Strategy

**If coqc is available:** Deploy E1 + E2 + E4 (minimum viable). Proof verification is operational. PostProcessGate upgrades from keyword tagging to Coq-backed tagging. E3 (Proof Index) adds search capability. E5, E6, E7 deferred.

**If coqc is unavailable:** EMP operates in fallback mode. PostProcessGate uses keyword-based provisional tagging (existing behavior). No Coq verification. No proof engine. System is fully operational without it — EMP proof artifacts are optional for V1 canonicalization.

**Decision required:** Is coqc expected to be available on V1 target environment? If not, P2.5 consists solely of documenting the fallback and ensuring PostProcessGate gracefully degrades.

### 6.5 File Manifest

| File | Change Type | Purpose |
|---|---|---|
| EMP_Deployment_Config.py | New | Coq path discovery, bridge construction, graceful degradation |
| EMP_Nexus.py | Modify (wiring) | Pass constructed Meta_Reasoner to PostProcessGate |

### 6.6 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_5_EMP_Deployment_Lock.json
```

---

## 7. P2.6 — SOP Runtime Observation

### 7.1 Problem Statement

SOP has extensive tooling built:

- `Startup_Gate.py` — startup boundary validation
- `Invariant_Enforcer.py` — governance invariant checks
- `Invariant_Drift_Detector.py` — drift detection
- `Audit_Logger.py` — structured audit output
- `Hash_Attestation_Service.py` — integrity verification
- `SOP_Nexus.py` — full StandardNexus implementation
- `System_Health_Checks.py` — health monitoring
- `Metrics_Registry.py` — telemetry collection

None of these are wired to the runtime tick loop. SOP currently operates only at startup (via startup gate). During runtime, no observation occurs.

### 7.2 Design Constraint: SOP is Write-Only

From `RUNTIME_IMPORT_AND_AUTHORITY_GRAPH.md`:

```
SOP -. writes .-> AUDIT
AUDIT -. no readback .-x LA
AUDIT -. no readback .-x SOP
```

SOP observes and writes. SOP never feeds back into runtime. No SOP output may influence agent decisions, Nexus execution, or SMP classification. This is architecturally enforced by making the observer a NexusParticipant that receives state but never emits actionable state.

### 7.3 Runtime Observer Interface (P2-IF-09)

```python
class RuntimeObserver(NexusParticipant):
    """
    SOP runtime observation participant.
    Registered in LP Nexus alongside agent participants.

    Receives all routed StatePackets.
    Records health snapshots per tick.
    Emits ONLY audit events (non-actionable by any consumer).
    """

    participant_id: str = "sop_runtime_observer"

    def __init__(
        self,
        audit_logger: Any,        # operational logger or SOP audit logger
        session_id: str,
    ) -> None:
        self._logger = audit_logger
        self._session_id = session_id
        self._handle: Optional[NexusHandle] = None
        self._tick_snapshots: List[Dict[str, Any]] = []

    def register(self, nexus_handle: NexusHandle) -> None:
        self._handle = nexus_handle

    def receive_state(self, packet: StatePacket) -> None:
        """
        Observe all routed packets. Record metadata only.
        Does NOT inspect payload content (privacy boundary).
        """
        self._tick_snapshots.append({
            "source": packet.source_id,
            "timestamp": packet.timestamp,
            "causal_intent": packet.causal_intent,
            "payload_type": packet.payload.get("type", "unknown"),
        })

    def execute_tick(self, context: Dict[str, Any]) -> None:
        """
        Per-tick observation:
        1. Record tick_id, participant count, MRE state
        2. Flush accumulated snapshots to audit logger
        3. Clear snapshots for next tick
        """
        tick_id = context.get("tick_id", 0)

        health_record = {
            "event": "tick_observation",
            "tick_id": tick_id,
            "session_id": self._session_id,
            "packets_observed": len(self._tick_snapshots),
            "packet_sources": [s["source"] for s in self._tick_snapshots],
            "timestamp": time.time(),
        }

        self._logger.info(json.dumps(health_record))
        self._tick_snapshots.clear()

    def project_state(self) -> Optional[StatePacket]:
        """
        SOP observer projects audit metadata ONLY.

        Payload type: "sop_audit_event"
        This is explicitly non-actionable. Any consumer that attempts
        to use SOP audit data for routing decisions violates governance.
        """
        return StatePacket(
            source_id=self.participant_id,
            payload={
                "type": "sop_audit_event",
                "content": {
                    "observer": "sop_runtime",
                    "status": "observing",
                },
            },
            timestamp=time.time(),
            causal_intent="audit_observation",
        )
```

### 7.4 Execution Order Impact

`participant_id = "sop_runtime_observer"` sorts AFTER all agent participants (`agent_i1` through `agent_logos`) and AFTER RGE (`rge_topology_advisor`). This means SOP observes the results of all other participants' ticks — correct behavior for an observer.

```
Sorted execution order (with SOP):
  1. "agent_i1"
  2. "agent_i2"
  3. "agent_i3"
  4. "agent_logos"
  5. "rge_topology_advisor"
  6. "sop_runtime_observer"    ← observes all preceding
```

### 7.5 Registration

SOP observer is registered in the LP Nexus by `NexusFactory.build_lp_nexus()` (P1.2). The factory needs a parameter to optionally include SOP:

```python
# In NexusFactory.build_lp_nexus():
if sop_observer is not None:
    nexus.register_participant(sop_observer)
```

Construction of the observer is handled by `RuntimeLoop` (P1.3), which has access to the operational logger.

### 7.6 File Manifest

| File | Path | Purpose |
|---|---|---|
| Runtime_Observer.py | `SOP_Core/` or `Logos_Core/Orchestration/` | RuntimeObserver NexusParticipant |

### 7.7 Phase Lock

```
_Governance/Phase_Locks/Phase_P2_6_SOP_Observer_Lock.json
```

---

## 8. Dependency Graph (P2 Internal)

```
P1 (complete)
  │
  ├──→ P2.1 UWM Implementation     (independent)
  ├──→ P2.2 SCP Orchestrator        (independent)
  ├──→ P2.3 CSP Promotion           (depends on P2.1 UWM read API)
  ├──→ P2.4 DRAC Assembler          (independent)
  ├──→ P2.5 EMP Deployment          (independent)
  └──→ P2.6 SOP Observer            (independent)
```

P2.3 has a soft dependency on P2.1 (needs UWM read API to query AAs for promotion evaluation). All others are fully independent. Recommended execution: start P2.1 first, then parallelize everything else.

---

## 9. Complete File Manifest (All P2 Workstreams)

### New Files (11-13)

| File | Workstream | Path |
|---|---|---|
| SMP_Schema.py | P2.1 | `CSP_Core/Unified_Working_Memory/` |
| SMP_Store.py | P2.1 | `CSP_Core/Unified_Working_Memory/` |
| AA_Catalog.py | P2.1 | `CSP_Core/Unified_Working_Memory/` |
| UWM_Access_Control.py | P2.1 | `CSP_Core/Unified_Working_Memory/` |
| Classification_Tracker.py | P2.1 | `CSP_Core/Unified_Working_Memory/` |
| SCP_Orchestrator.py | P2.2 | `SCP_Core/` |
| Promotion_Evaluator.py | P2.3 | `CSP_Core/` |
| Canonical_SMP_Producer.py | P2.3 | `CSP_Core/` |
| CSP_Canonical_Store.py | P2.3 | `CSP_Core/` |
| DRAC_Assembler.py | P2.4 | `DRAC_Core/` |
| Session_Artifact.py | P2.4 | `DRAC_Core/` |
| EMP_Deployment_Config.py | P2.5 | `EMP_Core/` |
| Runtime_Observer.py | P2.6 | `SOP_Core/` |

### Modified Files (3-5)

| File | Workstream | Change |
|---|---|---|
| `CSP_Core/Unified_Working_Memory/__init__.py` | P2.1 | Replace stub with operational exports |
| `SCP_Core/__init__.py` | P2.2 | Replace stub with SCPOrchestrator export |
| `DRAC_Core/DRAC_Core.py` | P2.4 | Wire assembler into phase orchestration |
| `EMP_Nexus/EMP_Nexus.py` | P2.5 | Wire Meta_Reasoner to PostProcessGate |

---

## 10. GPT Prompt Generation Instructions

P2 should be executed as 6 independent prompt sequences (one per workstream). They may run in any order, with the exception that P2.3 should follow P2.1.

**Prompt Sequence 1 (P2.1):** Create SMP_Schema.py, SMP_Store.py, AA_Catalog.py, UWM_Access_Control.py, Classification_Tracker.py. Rewrite `__init__.py`. Run verification suite. Write phase lock.

**Prompt Sequence 2 (P2.2):** Create SCP_Orchestrator.py. Rewrite SCP_Core `__init__.py`. Run verification. Write phase lock.

**Prompt Sequence 3 (P2.3):** Create Promotion_Evaluator.py, Canonical_SMP_Producer.py, CSP_Canonical_Store.py. Run verification against P2.1 UWM. Write phase lock.

**Prompt Sequence 4 (P2.4):** Create DRAC_Assembler.py, Session_Artifact.py. Run scan against live DRAC_Invariables directory. Write phase lock.

**Prompt Sequence 5 (P2.5):** Create EMP_Deployment_Config.py. Wire Coq bridge discovery. Wire Meta_Reasoner to PostProcessGate. Test graceful degradation. Write phase lock.

**Prompt Sequence 6 (P2.6):** Create Runtime_Observer.py. Test NexusParticipant registration and tick observation. Write phase lock.

---

## 11. Open Governance Questions

1. **UWM access scoping:** Should agent access be controlled by a routing table maintained by Logos Agent, or by static role declarations? Routing table is more flexible but adds complexity. Recommendation: static roles for V1, routing table for V1.1.

2. **AA append authorization:** Can agents append AAs directly, or must all AA appends go through Logos Agent? Recommendation: agents append directly to their bound SMP (after being routed the SMP by Logos Agent). Logos Agent does not intermediate every AA write.

3. **C-SMP storage location:** Does the CSP canonical store live alongside UWM (same package) or in a separate CSP subdirectory? Recommendation: separate module in CSP_Core, distinct from UWM.

4. **EMP coqc availability:** Is coqc expected on V1 target? If not, should P2.5 be deferred entirely? Recommendation: build deployment config with graceful degradation, defer actual Coq wiring to V1.1 unless coqc is confirmed available.

5. **SOP observer granularity:** Should the observer record packet metadata only (source, type, timestamp) or also record payload size / classification state? Recommendation: metadata only for V1 (privacy boundary). Payload inspection in V1.1 under explicit governance permission.

---

END OF P2 SPECIFICATION

# Logos Core Implementation Guide v1

**Paired Specification:** Logos_Core_Design_Specification_v1.md  
**Status:** Implementation Guide  
**Version:** 1.0.0  
**Date:** 2026-03-06  
**Authority:** LOGOS Development Hub  

---

## §1. Purpose & Scope

This guide translates Logos_Core_Design_Specification_v1.md into concrete implementation obligations. Every section traces back to the originating design spec section. This is a **processable packet** for downstream implementation—no architectural ambiguity remains.

---

## §2. Module Structure

### §2.1 Primary Module
**Location:** `LOGOS_SYSTEM/execution_side/logos_core/`

**Files:**
```
logos_core/
├── __init__.py                      # Module exports
├── controller.py                    # LogosCoreController class (§3)
├── tick_lifecycle/
│   ├── __init__.py
│   ├── dual_phase.py               # Dual-phase tick model (§4)
│   ├── phase_g.py                  # Phase-G activation (§5)
│   └── tick_boundary.py            # Tick boundary management (§6)
├── smp_pipeline/
│   ├── __init__.py
│   ├── orchestrator.py             # 7-tick SMP processing (§7)
│   ├── agent_router.py             # Agent routing logic (§8)
│   └── synthesis.py                # Tetrahedral synthesis (§9)
├── uwm/
│   ├── __init__.py
│   ├── access_control.py           # UWM write authority (§10)
│   └── interface.py                # UWM access interface (§11)
├── pxl_gate/
│   ├── __init__.py
│   ├── gate.py                     # PXL Gate interface (§12)
│   └── proof_validation.py         # Proof verification (§13)
├── governance/
│   ├── __init__.py
│   ├── mode.py                     # P1/P2 governance modes (§14)
│   └── reconciliation.py           # Governance reconciliation (§15)
├── integration/
│   ├── __init__.py
│   ├── drac.py                     # DRAC integration (§16)
│   ├── emp.py                      # EMP integration (§17)
│   ├── mspc.py                     # MSPC integration (§18)
│   ├── sop.py                      # SOP integration (§19)
│   └── rge.py                      # RGE integration (§20)
├── telemetry.py                    # Metrics emission (§21)
└── bootstrap.py                    # Initialization sequence (§22)
```

**Derivation:** Logos Core Spec §1.3 (Architectural Position), §4-16 (Integration Surfaces)

---

## §3. LogosCoreController Class

**Source Spec:** Logos Core Spec §4 (Tick Lifecycle)

### §3.1 Class Definition
```python
class LogosCoreController:
    """
    Unified execution-side controller (formerly Logos Agent + Logos Protocol).
    
    Authority: Sovereign runtime orchestrator (Spec §1.4).
    Domain: Execution coordination, not governance or semantic reasoning.
    """
    
    def __init__(
        self,
        drac_controller: DRACController,
        emp_controller: EMPController,
        mspc_controller: MSPCController,
        sop_client: SOPClient,
        rge_interface: RGEInterface,
        uwm: UnifiedWorldModel,
        governance_mode: GovernanceMode
    ):
        """
        Initialize Logos Core.
        
        Args from Spec:
            drac_controller: Reasoning admissibility gate (Spec §11)
            emp_controller: Epistemic artifact access (Spec §12)
            mspc_controller: SMP projection access (Spec §13)
            sop_client: Audit spine client (Spec §14)
            rge_interface: Radial Genesis Engine (Spec §15)
            uwm: Unified World Model (Spec §7)
            governance_mode: Active P1/P2 mode (Spec §14)
        """
        self._drac = drac_controller
        self._emp = emp_controller
        self._mspc = mspc_controller
        self._sop = sop_client
        self._rge = rge_interface
        self._uwm = uwm
        self._governance_mode = governance_mode
        self._tick_orchestrator = TickOrchestrator(...)
        self._is_operational = False
    
    def execute_tick(self) -> TickResult:
        """
        Execute dual-phase tick lifecycle.
        
        Workflow (Spec §4):
            Phase 1: Passive (context loading, RGE advisory)
            Phase 2: Active (reasoning execution, UWM writes)
        
        Returns:
            TickResult with execution summary
        
        Invariants:
            - INV-TICK-01: Dual-phase execution
            - INV-TICK-02: Phase-G before first tick
            - INV-TICK-05: SOP logging before phase transitions
        """
        # Verify Phase-G complete (INV-TICK-02)
        if not self._is_operational:
            raise LogosCoreNotReadyError("Phase-G activation incomplete")
        
        # Phase 1: Passive
        context = self._tick_orchestrator.execute_passive_phase()
        self._sop.log_phase_transition("PASSIVE_COMPLETE")
        
        # Phase 2: Active
        result = self._tick_orchestrator.execute_active_phase(context)
        self._sop.log_phase_transition("ACTIVE_COMPLETE")
        
        return result
```

**Key Implementation Notes:**
- Dual-phase tick execution (INV-TICK-01)
- Phase-G activation required before ticks (INV-TICK-02)
- SOP logging at phase boundaries (INV-TICK-05)

---

## §4. Dual-Phase Tick Model

**Source Spec:** Logos Core Spec §4.1

### §4.1 Tick Orchestrator
```python
class TickOrchestrator:
    """
    Dual-phase tick lifecycle orchestration.
    
    Spec: §4.1
    Invariants: INV-TICK-01, INV-TICK-03, INV-TICK-04
    """
    
    def __init__(
        self,
        rge_interface: RGEInterface,
        mspc_controller: MSPCController,
        smp_pipeline: SMPPipeline,
        uwm: UnifiedWorldModel
    ):
        self._rge = rge_interface
        self._mspc = mspc_controller
        self._smp_pipeline = smp_pipeline
        self._uwm = uwm
    
    def execute_passive_phase(self) -> PassivePhaseContext:
        """
        Execute Phase 1: Passive context loading.
        
        Spec: §4.1 Phase 1
        Operations:
            - Load SMP projections from MSPC
            - Request RGE geometric context (advisory)
            - Prepare execution context for Phase 2
        
        Invariants:
            - INV-TICK-03: No UWM writes in passive phase
            - INV-TICK-04: RGE context must be advisory only
        """
        # Load SMP projections
        smp_entries = self._mspc.get_active_projections()
        
        # Request RGE context (INV-TICK-04: advisory only)
        rge_context = self._rge.provide_advisory_context()
        
        # Construct passive context (no UWM writes)
        context = PassivePhaseContext(
            smp_projections=smp_entries,
            rge_context=rge_context,
            timestamp=datetime.utcnow().isoformat()
        )
        
        return context
    
    def execute_active_phase(
        self,
        passive_context: PassivePhaseContext
    ) -> TickResult:
        """
        Execute Phase 2: Active reasoning and UWM updates.
        
        Spec: §4.1 Phase 2
        Operations:
            - Execute SMP pipeline (7-tick processing)
            - Authorize UWM writes
            - Produce tick telemetry
        
        Invariants:
            - INV-UWM-01: Only Logos Core writes to UWM
            - INV-SMP-01: 7-tick SMP processing
        """
        # Execute SMP pipeline
        smp_result = self._smp_pipeline.process(passive_context.smp_projections)
        
        # Authorize UWM write (INV-UWM-01: exclusive authority)
        self._uwm.write(smp_result.world_model_updates)
        
        # Produce tick result
        return TickResult(
            tick_id=uuid4(),
            uwm_updates_count=len(smp_result.world_model_updates),
            timestamp=datetime.utcnow().isoformat()
        )
```

**Derivation:** Spec §4.1 dual-phase workflow mapped to orchestrator methods.

---

## §5. Phase-G Activation

**Source Spec:** Logos Core Spec §5

### §5.1 Phase-G Orchestrator
```python
class PhaseGOrchestrator:
    """
    Phase-G activation sequence.
    
    Spec: §5
    Invariants: INV-PHASEG-01, INV-PHASEG-02
    """
    
    def execute_activation(
        self,
        drac: DRACController,
        emp: EMPController,
        mspc: MSPCController,
        sop: SOPClient
    ) -> None:
        """
        Execute Phase-G subsystem activation.
        
        Spec: §5.2
        Sequence:
            1. SOP audit spine initialization
            2. EMP hash chain initialization
            3. DRAC proof gate activation
            4. MSPC projection pipeline activation
            5. Signal ready to Logos Core
        
        Invariants:
            - INV-PHASEG-01: Sequential activation (no parallelism)
            - INV-PHASEG-02: Failure at any step halts bootstrap
        """
        # Step 1: SOP
        try:
            sop.initialize()
        except Exception as e:
            raise PhaseGFailure(f"SOP initialization failed: {e}")
        
        # Step 2: EMP
        try:
            emp.initialize()
        except Exception as e:
            raise PhaseGFailure(f"EMP initialization failed: {e}")
        
        # Step 3: DRAC
        try:
            drac.initialize()
        except Exception as e:
            raise PhaseGFailure(f"DRAC initialization failed: {e}")
        
        # Step 4: MSPC
        try:
            mspc.initialize()
        except Exception as e:
            raise PhaseGFailure(f"MSPC initialization failed: {e}")
        
        # Step 5: Signal ready (INV-PHASEG-01: all steps complete)
        self._signal_phase_g_complete()
```

**Derivation:** Spec §5.2 activation sequence mapped to orchestrator method.

---

## §6. Tick Boundary Management

**Source Spec:** Logos Core Spec §4.2

### §6.1 Boundary Controller
```python
class TickBoundaryController:
    """
    Tick boundary enforcement.
    
    Spec: §4.2
    Invariants: INV-BOUNDARY-01, INV-BOUNDARY-02, INV-BOUNDARY-03
    """
    
    def finalize_tick(
        self,
        tick_id: UUID,
        sop_client: SOPClient
    ) -> None:
        """
        Finalize tick at boundary.
        
        Spec: §4.2
        Operations:
            - Flush SOP audit events
            - Verify UWM write completion
            - Prepare for next tick
        
        Invariants:
            - INV-BOUNDARY-01: SOP flush before next tick
            - INV-BOUNDARY-02: UWM writes must complete
        """
        # Flush SOP audit log (INV-BOUNDARY-01)
        sop_client.flush_pending_events()
        
        # Verify UWM write completion (INV-BOUNDARY-02)
        if not self._uwm.verify_write_completion():
            raise TickBoundaryViolation("UWM writes incomplete at tick boundary")
        
        # Log tick completion
        sop_client.log_tick_boundary(tick_id)
```

**Derivation:** Spec §4.2 boundary conditions mapped to controller method.

---

## §7. SMP Pipeline Orchestrator

**Source Spec:** Logos Core Spec §8

### §7.1 7-Tick Pipeline
```python
class SMPPipeline:
    """
    7-tick SMP processing pipeline.
    
    Spec: §8
    Invariants: INV-SMP-01, INV-SMP-02, INV-SMP-03
    """
    
    def __init__(
        self,
        agent_router: AgentRouter,
        synthesizer: TetrahedralSynthesizer
    ):
        self._router = agent_router
        self._synthesizer = synthesizer
    
    def process(
        self,
        smp_projections: List[SMPEntry]
    ) -> SMPPipelineResult:
        """
        Execute 7-tick SMP processing pipeline.
        
        Spec: §8.1
        Workflow:
            Tick 1: Load SMP projections
            Tick 2-3: Agent I1 evaluation
            Tick 3-4: Agent I2 evaluation
            Tick 4-5: Agent I3 evaluation
            Tick 6: Tetrahedral synthesis
            Tick 7: UWM write preparation
        
        Invariants:
            - INV-SMP-01: 7-tick processing (not fewer)
            - INV-SMP-02: Sequential agent evaluation
            - INV-SMP-03: Synthesis before UWM write
        """
        # Tick 1: Load
        context = self._load_smp_context(smp_projections)
        
        # Ticks 2-3: I1 evaluation (INV-SMP-02: sequential)
        i1_result = self._router.route_to_agent("I1", context)
        
        # Ticks 3-4: I2 evaluation
        i2_result = self._router.route_to_agent("I2", context)
        
        # Ticks 4-5: I3 evaluation
        i3_result = self._router.route_to_agent("I3", context)
        
        # Tick 6: Synthesis (INV-SMP-03: before UWM write)
        synthesis_result = self._synthesizer.synthesize(
            i1_result, i2_result, i3_result
        )
        
        # Tick 7: Prepare UWM write
        uwm_updates = self._prepare_uwm_write(synthesis_result)
        
        return SMPPipelineResult(world_model_updates=uwm_updates)
```

**Derivation:** Spec §8.1 7-tick workflow mapped to pipeline method.

---

## §8. Agent Router

**Source Spec:** Logos Core Spec §9

### §8.1 Routing Logic
```python
class AgentRouter:
    """
    Agent routing and protocol binding.
    
    Spec: §9
    Invariants: INV-ROUTE-01, INV-ROUTE-02
    """
    
    def route_to_agent(
        self,
        agent_id: str,
        context: SMPContext
    ) -> AgentEvaluationResult:
        """
        Route evaluation to specific agent.
        
        Spec: §9.1
        Agents:
            - I1: Logical/deductive reasoning
            - I2: Probabilistic/inductive reasoning
            - I3: Geometric/spatial reasoning
        
        Invariants:
            - INV-ROUTE-01: Agent-protocol binding enforced
            - INV-ROUTE-02: Agents cannot write to UWM
        """
        # Verify agent exists
        if agent_id not in ["I1", "I2", "I3"]:
            raise InvalidAgentError(f"Unknown agent: {agent_id}")
        
        # Route to agent (INV-ROUTE-01: protocol binding)
        agent = self._get_agent(agent_id)
        result = agent.evaluate(context)
        
        # INV-ROUTE-02: Verify no UWM writes
        if result.attempted_uwm_write:
            raise AgentAuthorityViolation(f"Agent {agent_id} attempted UWM write")
        
        return result
```

**Derivation:** Spec §9.1 routing logic mapped to router method.

---

## §9. Tetrahedral Synthesis

**Source Spec:** Logos Core Spec §10

### §9.1 Synthesizer
```python
class TetrahedralSynthesizer:
    """
    Tetrahedral synthesis of agent evaluations.
    
    Spec: §10
    Invariants: INV-SYNTH-01, INV-SYNTH-02
    """
    
    def synthesize(
        self,
        i1_result: AgentEvaluationResult,
        i2_result: AgentEvaluationResult,
        i3_result: AgentEvaluationResult
    ) -> SynthesisResult:
        """
        Synthesize agent evaluations into unified result.
        
        Spec: §10.1
        Geometry: Tetrahedral vertices (I1, I2, I3 + origin)
        
        Invariants:
            - INV-SYNTH-01: All three agents must contribute
            - INV-SYNTH-02: Synthesis produces single unified output
        """
        # INV-SYNTH-01: Verify all agents contributed
        if not all([i1_result, i2_result, i3_result]):
            raise IncompleteSynthesisError("All agents must contribute")
        
        # Tetrahedral synthesis (Spec §10.1)
        unified_output = self._compute_synthesis(
            i1_result.evaluation,
            i2_result.evaluation,
            i3_result.evaluation
        )
        
        # INV-SYNTH-02: Single unified output
        return SynthesisResult(unified_output=unified_output)
```

**Derivation:** Spec §10.1 synthesis geometry mapped to synthesizer method.

---

## §10. UWM Access Control

**Source Spec:** Logos Core Spec §7

### §10.1 Write Authority Enforcement
```python
class UWMAccessControl:
    """
    UWM write authority enforcement.
    
    Spec: §7
    Invariants: INV-UWM-01, INV-UWM-02, INV-UWM-03
    """
    
    def authorize_write(
        self,
        caller: str,
        updates: List[UWMUpdate]
    ) -> None:
        """
        Authorize UWM write operation.
        
        Spec: §7.1
        Invariants:
            - INV-UWM-01: Only Logos Core can write
            - INV-UWM-02: Agents are read-only
            - INV-UWM-03: RGE is advisory only
        """
        # INV-UWM-01: Verify caller is Logos Core
        if caller != "LOGOS_CORE":
            raise UWMWriteViolation(
                f"INV-UWM-01: Only Logos Core can write to UWM, not {caller}"
            )
        
        # Execute write
        self._uwm.apply_updates(updates)
```

**Derivation:** Spec §7.1 write authority rules mapped to access control method.

---

## §11. UWM Interface

**Source Spec:** Logos Core Spec §7.2

### §11.1 UWM Client
```python
class UnifiedWorldModel:
    """
    Unified World Model interface.
    
    Spec: §7.2
    Invariants: INV-UWM-01, INV-UWM-04
    """
    
    def write(self, updates: List[UWMUpdate]) -> None:
        """
        Write updates to UWM (Logos Core exclusive).
        
        Spec: §7.2
        Invariant: INV-UWM-01
        """
        # Verify caller authority (delegated to access control)
        self._access_control.authorize_write("LOGOS_CORE", updates)
        
        # Apply updates
        for update in updates:
            self._apply_update(update)
        
        # INV-UWM-04: Log writes to SOP
        self._sop.log_uwm_write(len(updates))
    
    def read(self, query: UWMQuery) -> UWMData:
        """
        Read from UWM (available to all subsystems).
        
        Spec: §7.2
        """
        return self._query_uwm(query)
```

**Derivation:** Spec §7.2 UWM interface mapped to client methods.

---

## §12. PXL Gate Interface

**Source Spec:** Logos Core Spec §6

### §12.1 PXL Gate Wrapper
```python
class PXLGateInterface:
    """
    PXL Gate proof validation interface.
    
    Spec: §6
    Invariants: INV-PXL-01, INV-PXL-02
    """
    
    def validate_proof(
        self,
        proof_fragments: List[ProofFragment]
    ) -> PXLValidationResult:
        """
        Validate PXL proof fragments.
        
        Spec: §6.1
        Invariants:
            - INV-PXL-01: All proofs validated via PXL Gate
            - INV-PXL-02: Invalid proofs trigger DENY
        """
        try:
            # Delegate to PXL proof engine
            validation_result = self._pxl_engine.verify(proof_fragments)
            
            return PXLValidationResult(
                valid=validation_result.passed,
                validation_id=uuid4(),
                rationale=validation_result.rationale if not validation_result.passed else None
            )
        except Exception as e:
            # INV-PXL-02: Errors trigger DENY
            return PXLValidationResult(
                valid=False,
                validation_id=uuid4(),
                rationale=f"PXL validation error: {e}"
            )
```

**Derivation:** Spec §6.1 PXL Gate interface mapped to wrapper methods.

---

## §13. Proof Validation Module

**Source Spec:** Logos Core Spec §6.2

### §13.1 Validation Orchestrator
```python
class ProofValidator:
    """
    PXL proof validation orchestration.
    
    Spec: §6.2
    Invariants: INV-PXL-03, INV-PXL-04
    """
    
    def validate_reasoning_request(
        self,
        proof_fragments: List[ProofFragment]
    ) -> bool:
        """
        Validate reasoning request proofs.
        
        Spec: §6.2
        Invariants:
            - INV-PXL-03: Validation before reasoning execution
            - INV-PXL-04: Failed validation halts reasoning
        """
        # INV-PXL-03: Validate before execution
        result = self._pxl_gate.validate_proof(proof_fragments)
        
        if not result.valid:
            # INV-PXL-04: Halt on failure
            self._sop.log_proof_validation_failure(result.rationale)
            return False
        
        return True
```

**Derivation:** Spec §6.2 validation workflow mapped to orchestrator method.

---

## §14. Governance Mode Module

**Source Spec:** Logos Core Spec §14

### §14.1 Mode Manager
```python
class GovernanceMode(Enum):
    """Governance modes (Spec §14)."""
    P1 = "P1"  # Strict
    P2 = "P2"  # Relaxed task sources

class GovernanceModeManager:
    """
    P1/P2 governance mode management.
    
    Spec: §14
    Invariants: INV-GM-01, INV-GM-02
    """
    
    def __init__(self, initial_mode: GovernanceMode):
        self._current_mode = initial_mode
    
    def get_current_mode(self) -> GovernanceMode:
        """
        Query current governance mode.
        
        Spec: §14.1
        Invariant: INV-GM-02 (subsystems query per-tick)
        """
        return self._current_mode
    
    def transition_mode(
        self,
        new_mode: GovernanceMode,
        sop_client: SOPClient
    ) -> None:
        """
        Transition governance mode.
        
        Spec: §14.2
        Invariants:
            - INV-GM-01: Mode transitions logged to SOP
            - INV-GM-03: Subsystems re-initialize on transition
        """
        if self._current_mode == new_mode:
            return  # No change
        
        # INV-GM-01: Log transition
        sop_client.log_governance_mode_transition(
            old_mode=self._current_mode,
            new_mode=new_mode
        )
        
        # Update mode
        self._current_mode = new_mode
        
        # INV-GM-03: Trigger subsystem re-initialization
        self._notify_subsystems_mode_change(new_mode)
```

**Derivation:** Spec §14.1, §14.2 mode management mapped to manager methods.

---

## §15. Governance Reconciliation

**Source Spec:** Logos Core Spec §17

### §15.1 Reconciliation Handler
```python
class GovernanceReconciliation:
    """
    Handle governance artifact reconciliation.
    
    Spec: §17
    """
    
    @staticmethod
    def flag_stale_artifacts() -> List[str]:
        """
        Identify stale artifacts from pre-unification model.
        
        Spec: §17
        Categories:
            1. Logos Agent-specific artifacts
            2. Logos Protocol-specific artifacts
            3. Octafolium references
            4. Agent/Protocol decomposition assumptions
        
        Returns:
            List of artifact names flagged for reconciliation
        """
        stale_artifacts = [
            "Logos_Agent_Design_Spec_v*.md",
            "Logos_Protocol_Design_Spec_v*.md",
            "Octafolium_Architecture_Blueprint.md",
            # ... additional artifacts per Spec §17
        ]
        
        return stale_artifacts
```

**Derivation:** Spec §17 reconciliation categories mapped to handler method.

---

## §16. DRAC Integration

**Source Spec:** Logos Core Spec §11

### §16.1 DRAC Client
```python
class DRACClient:
    """
    Logos Core client for DRAC integration.
    
    Spec: §11
    Contract:
        - Logos Core invokes DRAC before reasoning
        - Logos Core honors ADMIT/DENY verdicts
        - Logos Core provides PXL Gate access
    
    Invariants: INV-DRAC-01, INV-DRAC-02
    """
    
    def request_reasoning_admissibility(
        self,
        task_descriptor: TaskDescriptor,
        proof_fragments: List[ProofFragment]
    ) -> DecisionPacket:
        """
        Request reasoning admissibility from DRAC.
        
        Spec: §11.1
        Invariants:
            - INV-DRAC-01: Always invoke before reasoning
            - INV-DRAC-02: Honor DENY verdicts
        """
        # Construct POP
        pop = ProofObligationPacket(
            request_id=uuid4(),
            task_descriptor=task_descriptor,
            axiom_references=self._extract_axioms(task_descriptor),
            proof_fragments=proof_fragments,
            context_hash=self._compute_context_hash(),
            timestamp=datetime.utcnow().isoformat()
        )
        
        # INV-DRAC-01: Request admissibility
        decision = self._drac.evaluate(pop)
        
        # INV-DRAC-02: Honor DENY
        if decision.decision == DecisionType.DENY:
            raise ReasoningDeniedError(decision.rationale)
        
        return decision
```

**Cross-Reference:** DRAC v1 §5.1 (Logos Core Integration)

---

## §17. Implementation Checklist

### §17.1 Core Components
- [ ] LogosCoreController class (§3)
- [ ] TickOrchestrator (§4)
- [ ] PhaseGOrchestrator (§5)
- [ ] TickBoundaryController (§6)

### §17.2 SMP Pipeline
- [ ] SMPPipeline (§7)
- [ ] AgentRouter (§8)
- [ ] TetrahedralSynthesizer (§9)

### §17.3 UWM Management
- [ ] UWMAccessControl (§10)
- [ ] UnifiedWorldModel (§11)

### §17.4 PXL Gate
- [ ] PXLGateInterface (§12)
- [ ] ProofValidator (§13)

### §17.5 Governance
- [ ] GovernanceModeManager (§14)
- [ ] GovernanceReconciliation (§15)

### §17.6 Integration Interfaces
- [ ] DRACClient (§16)
- [ ] EMPClient (§17)
- [ ] MSPCClient (§18)
- [ ] SOPClient (§19)
- [ ] RGEInterface (§20)

---

**End of Implementation Guide**

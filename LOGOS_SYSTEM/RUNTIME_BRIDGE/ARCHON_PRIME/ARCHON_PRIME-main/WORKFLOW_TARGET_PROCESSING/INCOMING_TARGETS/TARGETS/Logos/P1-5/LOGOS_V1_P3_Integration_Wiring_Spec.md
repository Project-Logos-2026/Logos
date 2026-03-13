# LOGOS V1 — Phase P3: Integration Wiring Design Specification

**Document ID:** `LOGOS-V1-P3-INTEGRATION-WIRING`
**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires human governance ratification
**Parent:** `LOGOS_V1_Operational_Readiness_Blueprint.md`
**Depends On:** `LOGOS-V1-P1-RUNTIME-ACTIVATION`, `LOGOS-V1-P2-SUBSYSTEM-COMPLETION` (P2.1, P2.2, P2.3 minimum)
**Phase:** P3 (third development phase)
**Date:** 2026-03-01

---

## 0. Cross-Reference Index

| Reference ID | Section | Description |
|---|---|---|
| P3.1 | §2 | SMP Pipeline (End-to-End) |
| P3.2 | §3 | RGE ↔ MSPC ↔ SMP Pipeline |
| P3.3 | §4 | EMP ↔ MSPC Coherence Loop (V1.1 candidate) |
| P3.4 | §5 | Import Path Remediation |
| P3-IF-01 | §2.3 | Task-to-SMP conversion contract |
| P3-IF-02 | §2.4 | SMP routing protocol |
| P3-IF-03 | §2.5 | Agent-to-UWM write-back contract |
| P3-IF-04 | §2.8 | MTP emission contract |
| P3-IF-05 | §3.3 | RGE → MSPC topology handoff |
| P3-IF-06 | §3.4 | MSPC → SMP routing advisory |

---

## 1. Phase Overview

P3 wires individually operational subsystems into end-to-end execution paths. Every component needed for P3.1 exists after P1 + P2 (minimum). P3 creates NO new subsystem logic. P3 creates connection code, adapter code, and lifecycle orchestration code.

**Prerequisite:** P1 complete. P2.1 (UWM), P2.2 (SCP Orchestrator), P2.3 (CSP Promotion) individually functional.

**Post-condition:** A task submitted to LOGOS produces governed NL output through the full cognitive loop.

| Workstream | What It Wires | Critical for V1? |
|---|---|---|
| P3.1 SMP Pipeline | Task → SMP → I1 → I3 → I2 → Promotion → MTP → Output | YES — irreducible minimum |
| P3.2 RGE ↔ MSPC ↔ SMP | Topology advice into SMP routing and MSPC compilation | YES — M6 completion |
| P3.3 EMP ↔ MSPC Coherence | Dual-compiler coherence loop (Octafolium) | NO — V1.1 candidate |
| P3.4 Import Path Remediation | Clean up legacy/duplicate import paths | YES — integration hygiene |

---

## 2. P3.1 — SMP Pipeline (End-to-End)

### 2.1 Problem Statement

After P1 and P2, these components exist independently:

- RuntimeLoop receives tasks and ticks the LP Nexus (P1.3)
- LogosAgentParticipant can enqueue tasks (P1, stub _on_tick)
- I1/I2/I3 AgentParticipants can execute ticks (P1, stub _on_tick)
- UWM can store/retrieve SMPs and AAs (P2.1)
- SCPOrchestrator can analyze SMPs and produce I1AAs (P2.2)
- PromotionEvaluator can evaluate readiness, CanonicalSMPProducer can produce C-SMPs (P2.3)
- MTPNexus can render NL from SMP payloads (existing)
- ARP compiler can produce I3AAs (existing)

Nothing connects them. P3.1 wires the full cognitive loop.

### 2.2 End-to-End SMP Lifecycle

The complete lifecycle spans multiple ticks. Each agent processes one SMP per tick. Cross-agent communication happens via StatePacket routing between ticks.

```
Tick N:   Logos Agent receives task → creates SMP → stores in UWM (conditional)
          → emits StatePacket: {type: "smp_route_to_i1", smp_id}

Tick N+1: I1 receives packet → reads SMP from UWM → runs SCP analysis
          → produces I1AA → appends I1AA to UWM → emits: {type: "i1_analysis_complete", smp_id}

Tick N+2: Logos Agent receives I1 result → routes SMP to I3
          → emits: {type: "smp_route_to_i3", smp_id}

Tick N+3: I3 receives packet → reads SMP + I1AA from UWM → runs ARP compiler
          → produces I3AA → appends I3AA to UWM → emits: {type: "i3_analysis_complete", smp_id}

Tick N+4: Logos Agent receives I3 result → routes SMP to I2
          → emits: {type: "smp_route_to_i2", smp_id}

Tick N+5: I2 receives packet → reads SMP + all AAs from UWM → runs MTP egress
          → produces I2AA (critique) → appends I2AA to UWM
          → emits: {type: "i2_analysis_complete", smp_id, rendered_text}

Tick N+6: Logos Agent receives I2 result → evaluates promotion readiness
          → if eligible: promote to canonical, produce C-SMP, store in CSP
          → emits: {type: "smp_resolved", smp_id, csmp_id, rendered_text}

Tick N+7: RuntimeLoop reads Logos Agent projection → extracts rendered_text
          → writes to OutputSink → task complete
```

**Minimum ticks for one task: 7** (assuming no retries, no MRE throttling, no topology reroutings).

### 2.3 Task-to-SMP Conversion (P3-IF-01)

LogosAgentParticipant converts incoming tasks into SMPs.

```python
def _create_smp_from_task(self, task: Dict[str, Any]) -> SMP:
    """
    Convert task dict to SMP via UWM write API.

    Task dict expected fields:
    - task_id: str (required)
    - input: str or Dict (required — the content to process)
    - constraints: List[str] (optional — declared constraints for RGE)
    - smp_type: str (optional, defaults to "observation")

    Returns created SMP with classification_state "conditional".
    """
    smp = self._uwm_write.create_smp(
        smp_type=task.get("smp_type", "observation"),
        payload={
            "task_id": task["task_id"],
            "input": task["input"],
            "constraints": task.get("constraints", []),
        },
        session_id=self._session_id,
        source="logos_agent",
    )
    return smp
```

### 2.4 SMP Routing Protocol (P3-IF-02)

Logos Agent maintains a routing state machine per SMP. The state machine determines which agent processes the SMP next.

```python
class SMPRoutingState(Enum):
    CREATED = "created"                # SMP just created, route to I1
    I1_PENDING = "i1_pending"          # Waiting for I1 analysis
    I1_COMPLETE = "i1_complete"        # I1AA received, route to I3
    I3_PENDING = "i3_pending"          # Waiting for I3 analysis
    I3_COMPLETE = "i3_complete"        # I3AA received, route to I2
    I2_PENDING = "i2_pending"          # Waiting for I2 analysis
    I2_COMPLETE = "i2_complete"        # All AAs received, evaluate promotion
    RESOLVED = "resolved"              # Promoted + rendered, ready for output
    REJECTED = "rejected"              # Promotion failed or explicit rejection

ROUTING_TRANSITIONS = {
    SMPRoutingState.CREATED:      SMPRoutingState.I1_PENDING,
    SMPRoutingState.I1_COMPLETE:  SMPRoutingState.I3_PENDING,
    SMPRoutingState.I3_COMPLETE:  SMPRoutingState.I2_PENDING,
    SMPRoutingState.I2_COMPLETE:  SMPRoutingState.RESOLVED,
}
```

The Logos Agent `_on_tick()` implementation:

```python
def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # Phase 1: Process new tasks
    if self._task_queue:
        task = self._task_queue.pop(0)
        smp = self._create_smp_from_task(task)
        self._routing_table[smp.header.smp_id] = SMPRoutingState.CREATED
        self._active_smp_id = smp.header.smp_id

    # Phase 2: Process incoming agent results
    for packet in self._received_packets:
        ptype = packet.payload.get("type")
        smp_id = packet.payload.get("content", {}).get("smp_id")

        if ptype == "i1_analysis_complete" and smp_id:
            self._routing_table[smp_id] = SMPRoutingState.I1_COMPLETE
        elif ptype == "i3_analysis_complete" and smp_id:
            self._routing_table[smp_id] = SMPRoutingState.I3_COMPLETE
        elif ptype == "i2_analysis_complete" and smp_id:
            self._routing_table[smp_id] = SMPRoutingState.I2_COMPLETE

    # Phase 3: Route next SMP based on state
    for smp_id, state in list(self._routing_table.items()):
        if state == SMPRoutingState.CREATED:
            self._routing_table[smp_id] = SMPRoutingState.I1_PENDING
            return {
                "type": "smp_route_to_i1",
                "content": {"smp_id": smp_id, "session_id": self._session_id},
            }
        elif state == SMPRoutingState.I1_COMPLETE:
            self._routing_table[smp_id] = SMPRoutingState.I3_PENDING
            return {
                "type": "smp_route_to_i3",
                "content": {"smp_id": smp_id, "session_id": self._session_id},
            }
        elif state == SMPRoutingState.I3_COMPLETE:
            self._routing_table[smp_id] = SMPRoutingState.I2_PENDING
            return {
                "type": "smp_route_to_i2",
                "content": {"smp_id": smp_id, "session_id": self._session_id},
            }
        elif state == SMPRoutingState.I2_COMPLETE:
            result = self._evaluate_and_resolve(smp_id)
            return result

    return None
```

### 2.5 Agent-to-UWM Write-Back (P3-IF-03)

Each agent wrapper needs UWM references injected at construction time (via P1.1 AgentLifecycleManager).

**Modified AgentLifecycleManager.activate():**

```python
def activate(self) -> Dict[str, NexusParticipant]:
    # Construct UWM
    self._uwm_store = SMPStore()
    uwm_read = UWMReadAPI(self._uwm_store)
    uwm_write = UWMWriteAPI(self._uwm_store)

    # Construct CSP
    self._csp_store = CSPCanonicalStore()

    # Construct SCP Orchestrator
    scp_orch = SCPOrchestrator()

    # Construct Promotion Evaluator
    promo_eval = PromotionEvaluator(uwm_read)
    csmp_producer = CanonicalSMPProducer()

    # Construct agent participants with subsystem references
    logos = LogosAgentParticipant(
        session_id=self._session_id,
        logos_agent_id=self._logos_agent_id,
        uwm_read=uwm_read,
        uwm_write=uwm_write,
        promotion_evaluator=promo_eval,
        csmp_producer=csmp_producer,
        csp_store=self._csp_store,
    )

    i1 = I1AgentParticipant(
        session_id=self._session_id,
        logos_agent_id=self._logos_agent_id,
        uwm_read=uwm_read,
        uwm_write=uwm_write,    # for AA appending
        scp_orchestrator=scp_orch,
    )

    i2 = I2AgentParticipant(
        session_id=self._session_id,
        logos_agent_id=self._logos_agent_id,
        uwm_read=uwm_read,
        uwm_write=uwm_write,
        mtp_nexus=self._build_mtp_nexus(),  # optional, may be None
    )

    i3 = I3AgentParticipant(
        session_id=self._session_id,
        logos_agent_id=self._logos_agent_id,
        uwm_read=uwm_read,
        uwm_write=uwm_write,
        arp_compiler=self._build_arp_compiler(),  # optional, may be None
    )

    return {
        "agent_logos": logos,
        "agent_i1": i1,
        "agent_i2": i2,
        "agent_i3": i3,
    }
```

**I1 `_on_tick()` with UWM wiring:**

```python
def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for packet in self._received_packets:
        if packet.payload.get("type") == "smp_route_to_i1":
            smp_id = packet.payload["content"]["smp_id"]
            smp = self._uwm_read.get_smp(smp_id, requester_role="agent_i1")
            if smp is None:
                continue

            # Run SCP analysis
            i1aa = self._scp_orchestrator.analyze(smp)

            # Write I1AA to UWM
            self._uwm_write.append_aa(
                bound_smp_id=smp_id,
                aa_type="I1AA",
                originating_entity="I1",
                content=i1aa.content if hasattr(i1aa, 'content') else i1aa.to_dict(),
            )

            return {
                "type": "i1_analysis_complete",
                "content": {"smp_id": smp_id, "agent": "I1"},
            }
    return None
```

**I3 `_on_tick()` with UWM wiring:**

```python
def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for packet in self._received_packets:
        if packet.payload.get("type") == "smp_route_to_i3":
            smp_id = packet.payload["content"]["smp_id"]
            smp = self._uwm_read.get_smp(smp_id, requester_role="agent_i3")
            if smp is None:
                continue

            # Get existing AAs for context
            existing_aas = self._uwm_read.get_aas_for_smp(smp_id, requester_role="agent_i3")

            # Run ARP compiler (if available)
            if self._arp_compiler is not None:
                i3aa_content = self._arp_compiler.compile(smp, existing_aas)
            else:
                # Stub: acknowledge receipt
                i3aa_content = {"status": "stub_complete", "agent": "I3"}

            self._uwm_write.append_aa(
                bound_smp_id=smp_id,
                aa_type="I3AA",
                originating_entity="I3",
                content=i3aa_content,
            )

            return {
                "type": "i3_analysis_complete",
                "content": {"smp_id": smp_id, "agent": "I3"},
            }
    return None
```

**I2 `_on_tick()` with MTP wiring:**

```python
def _on_tick(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for packet in self._received_packets:
        if packet.payload.get("type") == "smp_route_to_i2":
            smp_id = packet.payload["content"]["smp_id"]
            smp = self._uwm_read.get_smp(smp_id, requester_role="agent_i2")
            if smp is None:
                continue

            rendered_text = ""

            # Run MTP egress pipeline (if available)
            if self._mtp_nexus is not None:
                egress_result = self._mtp_nexus.process(
                    smp_payload={
                        "smp_id": smp.header.smp_id,
                        **smp.payload,
                    },
                )
                rendered_text = egress_result.emitted_text()

                # I2AA is the critique result
                i2aa_content = {
                    "pipeline_id": egress_result.pipeline_id,
                    "status": egress_result.status.value,
                    "retries_used": egress_result.retries_used,
                    "rendered_text": rendered_text,
                }
            else:
                i2aa_content = {"status": "stub_complete", "agent": "I2"}
                rendered_text = f"[stub output for {smp_id}]"

            self._uwm_write.append_aa(
                bound_smp_id=smp_id,
                aa_type="I2AA",
                originating_entity="I2",
                content=i2aa_content,
            )

            return {
                "type": "i2_analysis_complete",
                "content": {
                    "smp_id": smp_id,
                    "agent": "I2",
                    "rendered_text": rendered_text,
                },
            }
    return None
```

### 2.6 Logos Agent Promotion and Resolution

```python
def _evaluate_and_resolve(self, smp_id: str) -> Dict[str, Any]:
    """
    Called when all three agent AAs are present.
    Evaluates promotion readiness and produces C-SMP if eligible.
    """
    eval_result = self._promotion_evaluator.evaluate_for_canonical(smp_id)

    if not eval_result.eligible:
        # V1 behavior: promote to provisional even if not all requirements met
        # (EMP proof may be unavailable)
        if eval_result.current_state == "conditional":
            self._uwm_write.promote_classification(smp_id, "provisional")

        # Check again with relaxed criteria (V1: EMP optional)
        eval_v1 = self._promotion_evaluator.evaluate_for_canonical(smp_id)
        if not eval_v1.eligible and not eval_v1.emp_proof_available:
            # V1 override: promote without EMP if I1+I2+I3 AAs present
            aa_types = set(eval_v1.aa_summary.keys())
            if {"I1AA", "I2AA", "I3AA"}.issubset(aa_types):
                eval_v1 = PromotionEvaluation(
                    eligible=True,
                    current_state=eval_v1.current_state,
                    target_state="canonical",
                    missing_requirements=[],
                    aa_summary=eval_v1.aa_summary,
                    conflicts=[],
                    emp_proof_available=False,
                )

    # Get rendered text from I2AA
    aas = self._uwm_read.get_aas_for_smp(smp_id, requester_role="logos_agent")
    rendered_text = ""
    for aa in aas:
        if aa.aa_type == "I2AA":
            rendered_text = aa.content.get("rendered_text", "")
            break

    if eval_result.eligible or (eval_v1 and eval_v1.eligible):
        # Promote to canonical
        self._uwm_write.promote_classification(smp_id, "canonical")

        # Produce C-SMP
        smp = self._uwm_read.get_smp(smp_id, requester_role="logos_agent")
        csmp = self._csmp_producer.produce(smp, aas)
        self._csp_store.store(csmp)

        self._routing_table[smp_id] = SMPRoutingState.RESOLVED
        return {
            "type": "smp_resolved",
            "content": {
                "smp_id": smp_id,
                "csmp_id": csmp.header.smp_id,
                "rendered_text": rendered_text,
                "status": "canonical",
            },
        }
    else:
        self._routing_table[smp_id] = SMPRoutingState.REJECTED
        return {
            "type": "smp_resolved",
            "content": {
                "smp_id": smp_id,
                "csmp_id": None,
                "rendered_text": rendered_text,
                "status": "rejected",
                "reason": eval_result.missing_requirements,
            },
        }
```

### 2.7 RuntimeLoop Output Extraction

The RuntimeLoop (P1.3) needs to extract the final rendered text from Logos Agent's projection after a resolved SMP.

**Modified `_execute_tick()`:**

```python
# After nexus.tick() and projection collection:
for pid, proj_payload in projections.items():
    if proj_payload.get("type") == "smp_resolved":
        content = proj_payload.get("content", {})
        rendered = content.get("rendered_text", "")
        if rendered:
            return {
                "tick_id": self._nexus.tick_counter,
                "session_id": self._session_id,
                "task_id": task_id,
                "status": "completed",
                "rendered_output": rendered,
                "smp_id": content.get("smp_id"),
                "csmp_id": content.get("csmp_id"),
                "classification": content.get("status"),
                # ... other fields
            }
```

**Multi-tick task processing in run():**

```python
def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single task through multiple ticks until resolved.
    """
    self._logos_participant.enqueue_task(task)
    task_id = task.get("task_id", str(uuid.uuid4()))

    max_ticks = 50  # safety limit
    for tick_num in range(max_ticks):
        result = self._execute_tick(task)
        if result.get("status") == "completed" and result.get("rendered_output"):
            return result
        if result.get("status") == "halted":
            return result

    # Tick budget exhausted
    return {
        "tick_id": self._nexus.tick_counter,
        "session_id": self._session_id,
        "task_id": task_id,
        "status": "halted",
        "halt_reason": f"Tick budget exhausted ({max_ticks} ticks)",
        "rendered_output": None,
    }
```

### 2.8 MTP Emission Contract (P3-IF-04)

The MTPNexus.process() method is the final rendering step. Its contract:

**Input:** `smp_payload: Dict[str, Any]` containing at minimum `smp_id` and the original task payload fields.

**Output:** `EgressPipelineResult` with:
- `status`: `PipelineStatus.EMITTED` | `HALTED` | `FAILED`
- `emitted_text()`: returns L1 paragraph string (the NL output)
- `stages`: list of `PipelineStageRecord` for audit
- `i2_critique`: critique result (if I2 critique engine available)

**MTP construction:** MTPNexus requires 5 engines (projection, linearizer, fractal evaluator, renderer, validation gate) plus optional I2 critique. For V1, if any engine is unavailable, the I2AgentParticipant falls back to stub output. The MTPNexus is constructed in AgentLifecycleManager via a `_build_mtp_nexus()` method that attempts imports and returns None on failure.

### 2.9 File Manifest (P3.1)

P3.1 creates NO new files. It modifies existing P1 and P2 files:

| File | Change |
|---|---|
| `Agent_Wrappers.py` (P1) | Rewrite all four agent `_on_tick()` methods. Add UWM/subsystem constructor parameters. Add SMPRoutingState to LogosAgent. |
| `Agent_Lifecycle_Manager.py` (P1) | Inject UWM, SCP, CSP, MTP, ARP references into agent constructors. Add `_build_mtp_nexus()`, `_build_arp_compiler()`. |
| `Runtime_Loop.py` (P1) | Add multi-tick `_process_task()`. Modify output extraction to read `smp_resolved` projections. |

### 2.10 Verification

```bash
python3 -c "
# End-to-end integration test
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Orchestration.Runtime_Loop import RuntimeLoop, SingleTaskSource, StdoutOutputSink

ctx = {
    'status': 'LOGOS_AGENT_READY',
    'logos_identity': {'logos_agent_id': 'LOGOS:test', 'session_id': 'test'},
    'logos_session': {'session_id': 'test'},
    'constructive_compile_output': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'prepared_bindings': {}},
    'agent_orchestration_plan': {'logos_agent_id': 'LOGOS:test', 'universal_session_id': 'test', 'agents_planned': ['I1','I2','I3'], 'protocols_planned': ['SCP','ARP','MTP'], 'execution': 'FORBIDDEN', 'phase': 'Phase-E', 'status': 'ORCHESTRATION_PLAN_PREPARED'},
}

loop = RuntimeLoop(ctx)
result = loop.run_single({'task_id': 'e2e-001', 'input': 'What is the nature of truth?'})

assert result['status'] in ('completed', 'halted')
assert result['task_id'] == 'e2e-001'
if result['status'] == 'completed':
    assert result['rendered_output'] is not None
    assert len(result['rendered_output']) > 0
    print(f'OUTPUT: {result[\"rendered_output\"]}')
print('E2E TEST: PASS')
"
```

### 2.11 Phase Lock

```
_Governance/Phase_Locks/Phase_P3_1_SMP_Pipeline_Lock.json
```

---

## 3. P3.2 — RGE ↔ MSPC ↔ SMP Pipeline

### 3.1 Problem Statement

M6 defines three integration tasks:
- M6A: Task Constraint Provider (declared constraints → RGE input)
- M6B: Topology Context Provider (RGE output → MSPC input)
- M6C: Orchestration Tick Binding (Nexus tick → RGE + MSPC execution)

After M6, RGE produces topology recommendations and MSPC receives them. But this operates in parallel to the SMP pipeline — the two systems do not influence each other. P3.2 closes this gap.

### 3.2 Integration Points

**RGE → MSPC (M6, already designed):**

```
LP Nexus tick
  → RGENexusAdapter.execute_tick()
    → RGERuntime.inject_telemetry(task_id, tick_id, constraints, ...)
    → RGERuntime.evaluate()
    → RGERuntime.select()
  → RGENexusAdapter.project_state()
    → StatePacket {type: "rge_topology_recommendation", content: {...}}

RuntimeLoop reads RGE projection
  → MSPCRuntime.set_topology_context(TopologyContext(config_id=...))
  → MSPCPipeline.execute_tick()
    → IncrementalCompiler.compile_batch(..., topology_context=ctx)
  → RuntimeLoop clears topology context
```

This path is wired in P1.3 `_execute_tick()`. No additional P3.2 work needed for this direction.

**MSPC → SMP Routing (NEW in P3.2):**

MSPC compilation results can advise the Logos Agent on SMP routing decisions. For example, if MSPC compilation indicates that a particular protocol axis has higher coherence for the current topology, Logos Agent may prefer routing through that protocol.

```python
# In RuntimeLoop._execute_tick(), after MSPC tick:
if mspc_result and not mspc_result.get("halted"):
    # Extract routing advisory
    compiled_artifacts = mspc_result.get("compiled", [])
    for artifact in compiled_artifacts:
        content = artifact.get("content", {})
        if content.get("topology_routing"):
            # Store advisory for Logos Agent to consume
            self._logos_participant.set_topology_advisory(content["topology_routing"])
```

### 3.3 RGE → MSPC Topology Handoff (P3-IF-05)

**Verified from repo:** `MSPCRuntime.set_topology_context(topology_context)` accepts a `TopologyContext` object with a `config_id` attribute. `IncrementalCompiler.compile_batch()` stamps `topology_context.config_id` into compiled artifact content.

```python
# TopologyContext construction in RuntimeLoop:
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.Topology_Context import TopologyContext

rge_result = self._rge_adapter.get_last_result()
if rge_result and rge_result.get("selected"):
    topology_ctx = TopologyContext(config_id=rge_result.get("config_id"))
    self._mspc_runtime.set_topology_context(topology_ctx)
```

### 3.4 MSPC → SMP Routing Advisory (P3-IF-06)

This is advisory-only. Logos Agent is never bound by MSPC output.

```python
class LogosAgentParticipant:
    def set_topology_advisory(self, config_id: str) -> None:
        """
        Receive topology advisory from MSPC via RuntimeLoop.
        Stored for consideration during routing decisions.
        Does NOT override routing state machine.
        """
        self._topology_advisory = config_id

    def _consider_topology_for_routing(self, smp_id: str) -> Optional[str]:
        """
        Optional routing consideration based on topology.
        V1: ignored (always follows fixed I1 → I3 → I2 order).
        V1.1: may reorder or skip agents based on topology.
        """
        return None  # V1: no topology-based routing modification
```

### 3.5 RGE Constraint Injection from Tasks

Task constraints need to reach RGE. The path:

```
Task dict → task["constraints"]
  → RuntimeLoop builds tick context with constraints
    → LP Nexus tick passes context to all participants
      → RGENexusAdapter.execute_tick(context)
        → _extract_telemetry_input(context) reads context["constraints"]
          → RGERuntime.inject_telemetry(constraints=...)
```

This path already works via P1.3 tick context construction. The only requirement is that `RuntimeLoop._execute_tick()` includes the task's declared constraints in the Nexus tick context:

```python
# Already in P1.3 design:
task_context = {
    "task_id": task_id,
    "constraints": self._constraint_provider.get_constraints_for_tick(task),
    "session_id": self._session_id,
}
```

And the LP Nexus passes this context to `execute_tick()` for each participant. RGENexusAdapter already reads `context["constraints"]` in `_extract_telemetry_input()`.

### 3.6 MSPC Pipeline Construction

MSPC requires 10 components. Construction:

```python
def _build_mspc_runtime(self) -> Optional[Any]:
    """
    Attempt to construct MSPCRuntime.
    Returns None if any required component is unavailable.
    """
    try:
        from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_Runtime import MSPCRuntime
        runtime = MSPCRuntime()
        runtime.boot()
        return runtime
    except Exception:
        return None
```

### 3.7 File Manifest (P3.2)

| File | Change |
|---|---|
| `Runtime_Loop.py` (P1) | Add MSPC runtime construction, topology handoff, advisory extraction |
| `Agent_Wrappers.py` (P1) | Add `set_topology_advisory()` to LogosAgentParticipant |

### 3.8 Phase Lock

```
_Governance/Phase_Locks/Phase_P3_2_RGE_MSPC_SMP_Lock.json
```

---

## 4. P3.3 — EMP ↔ MSPC Coherence Loop (V1.1 Candidate)

### 4.1 Deferral Recommendation

P3.3 implements the full Octafolium dual-compiler coherence engine. This is the most architecturally ambitious integration in the entire system. It requires:

- EMP operational with Coq verification (P2.5, may be deferred)
- MSPC operational with full compilation (P3.2)
- I2 Agent with TRI-CORE fractal recursion (not yet implemented)
- Logos Agent MSPC routing approval (governance gate)
- Four-modality expressibility checking (NL + math + lambda + PXL)

**V1 operates without this loop.** SMPs are canonicalized based on I1+I2+I3 AAs without EMP proof verification. This is explicitly permitted by the V1 promotion evaluator (EMP proof optional flag).

### 4.2 Architecture (For Reference)

When implemented, the coherence loop operates:

```
1. I2 + TRI-CORE explores abstraction space → candidate claims
2. Ship to MSPC → formalize in NL + math + lambda + PXL simultaneously
3. Ship to EMP → CONC compiler produces multi-layer artifacts
4. Back to I2 → mediate via privation gating + bridge principle
5. Back to MSPC → diff comparison of I2 → EMP → I2 transformation
6. Loop closes → MSPC validates coherence across all four modalities
```

### 4.3 V1.1 Prerequisites

| Prerequisite | V1 Status |
|---|---|
| EMP Coq verification | Deferred unless coqc confirmed |
| MSPC four-modality check | Not implemented |
| TRI-CORE | Not implemented |
| EMP_MSPC_Witness | Built, not wired |
| Logos Agent MSPC routing | Advisory only in V1 |

### 4.4 Phase Lock

```
_Governance/Phase_Locks/Phase_P3_3_EMP_MSPC_Coherence_DEFERRED.json
```

Status: DEFERRED_TO_V1_1

---

## 5. P3.4 — Import Path Remediation

### 5.1 Problem Statement

The codebase contains legacy import paths from multiple rewrite phases (Phase_B, Header_Injection, Phase-8 Tier 1/2). Many modules exist at multiple paths due to the structural rewrites from `System_Stack/` to `RUNTIME_CORES/RUNTIME_EXECUTION_CORE/` and `RUNTIME_OPPERATIONS_CORE/`. Compatibility shims exist (e.g., `LOGOS_SYSTEM/Governance/exceptions.py`). Legacy `__init__.py` stubs may re-export deprecated paths.

During P3.1 integration, incorrect import paths cause `ImportError` or worse — importing a stale copy of a module that was superseded. This is a silent correctness hazard.

### 5.2 Remediation Strategy

**Step 1: Canonical Path Audit**

For every module imported by P1, P2, and P3 artifacts, establish the single canonical import path:

| Module | Canonical Path |
|---|---|
| NexusParticipant, StatePacket, etc. | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus` |
| RGENexusAdapter | `LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Integration.RGE_Nexus_Adapter` |
| RGERuntime | `LOGOS_SYSTEM.RUNTIME_BRIDGE.Radial_Genesis_Engine.Controller.RGE_Bootstrap` |
| MSPCRuntime | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Multi_Process_Signal_Compiler.MSCP_Protocol.MSPC_Runtime` |
| MTPNexus | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Meaning_Translation_Protocol.MTP_Nexus.MTP_Nexus` |
| analysis_runner | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I1_Agent.I1_Agent_Tools.scp_analysis.analysis_runner` |
| UWM (P2.1) | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core.Unified_Working_Memory` |
| SCP_Core (P2.2) | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Synthetic_Cognition_Protocol.SCP_Core` |
| CSP (P2.3) | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Cognitive_State_Protocol.CSP_Core` |
| DRAC_Core | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Dynamic_Reconstruction_Adaptive_Compilation_Protocol.DRAC_Core` |
| EMP_Core | `LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.Epistemic_Monitoring_Protocol.EMP_Core` |
| Operational_Logger | `LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Operational_Logging.Operational_Logger` |
| repo_root | `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.repo_root` |

**Step 2: Duplicate Identification**

Scan for modules that exist at multiple paths. Known duplicates from repo inspection:

- `agent_orchestration.py` exists in at least 3 locations (GOVERNANCE_ENFORCEMENT, RUNTIME_EXECUTION_CORE, legacy System_Stack)
- `NexusParticipant` is defined identically in 8 Nexus files (LP, SCP, ARP, CSP, SOP, DRAC, EMP, MTP). All P1/P3 code imports from LP_Nexus only.
- `exceptions.py` has a compatibility shim at `LOGOS_SYSTEM/Governance/exceptions.py`
- Various `__init__.py` stubs may re-export from legacy paths

**Step 3: Consumer Redirect**

For each non-canonical import found across the codebase, redirect to the canonical path. This is a mechanical find-and-replace operation:

```bash
# Example: Find all imports of agent_orchestration
grep -rn "import.*agent_orchestration" LOGOS_SYSTEM/ STARTUP/ --include="*.py"

# Redirect all to canonical path
# OLD: from LOGOS_SYSTEM.GOVERNANCE_ENFORCEMENT.Runtime_Enforcement.Runtime_Spine.Agent_Orchestration.agent_orchestration import ...
# CANONICAL: (same — this IS the canonical path used by STARTUP/LOGOS_SYSTEM.py)
```

**Step 4: Deprecation Markers**

Non-canonical copies get a deprecation marker added to their module docstring:

```python
"""
DEPRECATED: This module is a legacy copy.
Canonical path: LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.LP_Nexus.Logos_Protocol_Nexus
This file will be removed in V1.1.
"""
```

**Step 5: CI Check (V1.1)**

A linting script that fails if any new import uses a non-canonical path. Deferred to V1.1 (no CI infrastructure in V1).

### 5.3 Scope Estimate

- Modules requiring audit: ~40-60 (all modules imported by P1/P2/P3 artifacts)
- Expected redirects: ~20-50 import statements across ~15-30 files
- Expected deprecated copies: ~10-20 files marked
- No files deleted in P3.4 (deletion is V1.1)

### 5.4 Execution Approach

P3.4 can run in parallel with P3.1 and P3.2. It should START early (ideally alongside P2) because import failures discovered during P3.1 integration testing are expensive to debug.

Recommended workflow:
1. Generate import graph from all P1/P2/P3 new files
2. For each import, verify the target exists at exactly one canonical path
3. If the import resolves to a non-canonical path, redirect
4. If the import fails entirely, determine the correct canonical path and fix
5. Produce audit report listing all changes

### 5.5 File Manifest (P3.4)

| Deliverable | Type |
|---|---|
| `_Reports/P3_4_Import_Audit.json` | Audit report: every import, canonical path, redirect status |
| 20-50 modified .py files | Import statement redirects |
| 10-20 modified .py files | Deprecation markers added |

### 5.6 Phase Lock

```
_Governance/Phase_Locks/Phase_P3_4_Import_Remediation_Lock.json
```

---

## 6. Dependency Graph (P3 Internal)

```
P2.1 (UWM) ──┐
P2.2 (SCP) ──┤
P2.3 (CSP) ──┼──→ P3.1 SMP Pipeline ──→ P3.2 RGE ↔ MSPC wiring
P1 (runtime) ─┘                            │
                                           ▼
                                      P3.3 EMP ↔ MSPC (DEFERRED)

P3.4 Import Remediation ── runs in parallel, independent of P3.1/P3.2
```

**Critical path:** P3.1 → P3.2.
**P3.3 deferred.** P3.4 parallel.

---

## 7. Complete Tick Sequence (Post-P3)

After P3.1 and P3.2 are complete, a single task produces this tick sequence:

```
Tick 1: Logos creates SMP, routes to I1. RGE evaluates topology.
Tick 2: I1 runs SCP analysis, produces I1AA. MSPC compiles with topology.
Tick 3: Logos routes SMP to I3.
Tick 4: I3 runs ARP compiler, produces I3AA.
Tick 5: Logos routes SMP to I2.
Tick 6: I2 runs MTP egress, produces I2AA + rendered NL.
Tick 7: Logos evaluates promotion, produces C-SMP.
         RuntimeLoop extracts rendered_text, writes to OutputSink.
```

Every tick: LP Nexus executes all participants in sorted order. RGE runs every tick (topology may change). MSPC runs every tick (compilation context updated). SOP observer (if registered) records audit events every tick.

---

## 8. GPT Prompt Generation Instructions

**Prompt 1 (P3.1):** Modify Agent_Wrappers.py, Agent_Lifecycle_Manager.py, Runtime_Loop.py. Add SMPRoutingState, UWM injection, multi-tick processing, output extraction. Run end-to-end verification. Write phase lock.

**Prompt 2 (P3.2):** Modify Runtime_Loop.py for MSPC construction, topology handoff, advisory extraction. Modify Agent_Wrappers.py for topology advisory. Run verification with RGE + MSPC. Write phase lock.

**Prompt 3 (P3.4):** Run import path audit across all P1/P2/P3 files. Redirect non-canonical imports. Add deprecation markers. Produce audit report. Write phase lock.

**P3.3 is not prompted.** Deferred to V1.1.

---

## 9. Open Governance Questions

1. **Multi-SMP concurrency:** V1 processes one SMP at a time (sequential routing). Should the Logos Agent support multiple in-flight SMPs with interleaved ticks? Recommendation: one at a time for V1. Concurrency in V1.1.

2. **Tick budget per task:** Currently set to 50 ticks max. Should this be configurable? Should it be per-SMP or per-session? Recommendation: per-task, configurable via task dict (`max_ticks` field), default 50.

3. **MTP fallback:** If MTPNexus construction fails (missing engines), should I2 produce stub text or should the task fail? Recommendation: stub text (`"[MTP unavailable: raw SMP payload]"`). Task should still complete.

4. **ARP fallback:** Same question for ARP compiler. Recommendation: stub I3AA. Task completes with reduced analysis.

5. **MSPC topology advisory:** V1 stores advisory but ignores it. Should this be logged? Recommendation: yes, log via operational logger for future analysis.

---

END OF P3 SPECIFICATION

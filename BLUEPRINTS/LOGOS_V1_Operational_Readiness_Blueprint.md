# LOGOS V1 Operational Readiness Blueprint

**Status:** DESIGN_ONLY — NON-EXECUTABLE
**Authority:** Requires human governance ratification per section
**Scope:** Post-M6 integration through V1 operational readiness
**Date:** 2026-02-28

---

## 0. How to Read This Document

This blueprint defines every milestone required to take LOGOS from its current state (post-M6 RGE↔MSPC integration closure) to a fully operational V1 system. Each section identifies the subsystem, its current state as verified by repo inspection, what is missing, and the concrete work required.

Milestones are organized into five phases (P1–P5) representing a strict dependency ordering. Each phase can contain parallel workstreams within it, but phases themselves are sequential.

---

## 1. Current System State Summary

### 1.1 What Works (Verified Operational)

| Subsystem | Status | Evidence |
|-----------|--------|----------|
| Startup chain | Operational | `START_LOGOS` → `LOGOS_SYSTEM` → `Lock_And_Key` → `Start_Logos_Agent` → `Lem_Discharge` → `prepare_agent_orchestration` — all wired, all fail-closed |
| Operational logging (v1) | Locked (M1–M5) | Logger module, bootstrap integration, halt sites, startup milestones, print elimination, CI enforcement |
| RGE scoring pipeline | Complete | 5 scoring modules, composite aggregator, genesis selector, hysteresis governor, mode controller, override channel |
| RGE Nexus adapter | Complete | `RGENexusAdapter` wraps `RGERuntime` as `NexusParticipant`, `participant_id = "rge_topology_advisor"` |
| Telemetry production | Complete | `Telemetry_Producer.assemble_telemetry()`, `Task_Triad_Derivation`, `Commutation_Residual_Producer`, `Stability_Scalar_Producer` — all implemented |
| MSPC pipeline | Complete (6 stages) | Ingress → Registration → Conflict Resolution → Compilation → Emission → Publication |
| Phase 5 NL externalization (MSPC) | Frozen | Four-layer compiler (AXIOM/MODIFIER/CONTEXTUAL/DISCOURSE) closed |
| MTP egress pipeline | Complete (7 modules) | Projection → Linearization → Fractal Eval → Rendering → Validation → I2 Critique → Nexus orchestration |
| ARP compiler | Complete (5 stages) | 12 base engines, 5 taxonomy aggregators, triune synthesis, unified binder → I3AA |
| I1/SCP integration | Complete | SMP intake, MVS/BDN adapters (stub + real), analysis runner, I1AA binder, sign grounding |
| Metered Reasoning Enforcer | Complete | Iteration limits, time bounds, novelty/repetition monitoring, deterministic halt |
| All 8 protocol Nexuses | Built | LP, SCP, ARP, MTP, CSP, SOP, DRAC, EMP — all implement `StandardNexus` pattern with mesh enforcement, MRE gating, sorted tick execution |
| Governance contracts | Comprehensive | Phase D/E/F execution contracts, Lock-And-Key contract, runtime module header contract, RGE subordination, Phase 7 freezes |
| M6 integration (pending commit) | Designed | Constraint ingress, topology context provider, orchestration tick binding — blueprinted, implementation in progress |

### 1.2 What Does NOT Work (Gaps)

| Subsystem | Current State | What's Missing |
|-----------|--------------|----------------|
| **Startup → Runtime transition** | Startup chain returns `LOGOS_AGENT_READY` dict with an orchestration plan. Nothing consumes this plan. | Post-startup runtime activation: agent instantiation, protocol binding, Nexus construction, tick loop entry |
| **Agent instantiation** | No agent constructor exists. `prepare_agent_orchestration()` produces a declarative plan with `"execution": "FORBIDDEN"`. I1/I2/I3 are code libraries, not instantiable objects. | Agent lifecycle: construction from orchestration plan, protocol binding, Nexus registration, identity injection |
| **SCP Core** | `__init__.py` exports `CognitionContext`, `CognitionResult`, `run_cognition` — all stubs raising `NotImplementedError`. MVS/BDN subsystems are built but SCP core orchestration is a stub. | SCP pipeline orchestrator that wires MVS/BDN analysis to I1 agent tooling |
| **UWM (Unified Working Memory)** | `__init__.py` exports `UWMContext`, `UWMStore`, `read`, `write` — all stubs. `UWMStore` has trivial `get`/`set` on an in-memory dict. | Governed read/write API per Phase-2.2 UWM Read-Only API Spec, SMP storage, provenance verification, access control |
| **CSP (Cognitive State Protocol)** | Memory subsystem has conceptual classes (`Logos_Memory_Nexus`, `Memory_State_Persistence`, `Memory_Recall_Integration`). Most are design-phase implementations with async patterns not wired to any caller. | Session-scoped SMP store, canonical SMP promotion path, AA cataloging, classification ladder enforcement |
| **DRAC session reconstruction** | `DRAC_Core.py` has a `DRAC_Core` class with phase tracking but no actual reconstruction logic. Semantic axioms, contexts, and invariables exist as individual files but no assembly pipeline consumes them. | Session bootstrap: monolith scanning, dependency resolution, import graph assembly, dynamic codebase construction |
| **EMP (Epistemic Monitoring Protocol)** | Blueprint complete (E1–E8). Implementation modules built (`EMP_Coq_Bridge`, `EMP_Meta_Reasoner`, `EMP_Proof_Index`, `EMP_Template_Engine`, `EMP_Abstraction_Engine`). Not deployed. | Coq environment resolution, MSPC operational readiness, PXL kernel axiom declaration, Logos Agent approval of routing |
| **SOP runtime enforcement** | SOP Nexus exists. `Startup_Gate`, `Invariant_Enforcer` exist. DRAC integration bridge exists. No runtime observation loop. | Live runtime health monitoring, enforcement decision loop, audit event emission during tick execution |
| **Tick loop** | No runtime tick loop exists anywhere in the codebase. The startup chain terminates at `LOGOS_AGENT_READY`. | Main execution loop: task ingestion → constraint derivation → Nexus tick → MSPC tick → output emission → repeat |
| **Task ingestion** | No external interface for receiving tasks. No task object schema. No constraint declaration mechanism. | Task input boundary, task-to-constraint mapping, task lifecycle management |
| **Output emission** | MTP egress pipeline produces rendered NL. No code delivers this output to an external consumer. | Output delivery boundary (API, GUI, file, stdout — TBD) |
| **Import path health** | Legacy fallback import chains persist across many modules. Multiple duplicate module paths exist (e.g., `agent_orchestration.py` in 3+ locations). | Canonical import path enforcement, dead module removal, circular dependency resolution |
| **GUI** | Angular app exists in `LOGOS_GUI`. `LOGOS_SYSTEM.py` has `_launch_gui()` for interactive mode. No integration with runtime tick loop. | GUI ↔ runtime bridge for task submission and output display (V1 may not require this) |

---

## 2. Phase Definitions

### P1 — Runtime Activation (Post-Startup → Live Tick Loop)
### P2 — Subsystem Completion (Stubs → Operational)
### P3 — Integration Wiring (Subsystems → End-to-End Pipeline)
### P4 — Governance Hardening (Audit, Testing, Validation)
### P5 — V1 Operational Boundary (External Interface + Deployment)

---

## 3. P1 — Runtime Activation

**Prerequisite:** M6 committed and locked.

**Objective:** Bridge the gap between startup (which terminates at `LOGOS_AGENT_READY`) and a live runtime tick loop. After P1, LOGOS can execute ticks.

### P1.1 — Agent Lifecycle Manager

**Current state:** Agents are code libraries (I1 has tools, I2 has tools, I3 has ARP compiler). No agent class exists that can be instantiated, registered with a Nexus, and executed per tick.

**Required:**

Create `AgentLifecycleManager` that consumes the orchestration plan produced by `prepare_agent_orchestration()` and:

1. Constructs Logos Agent wrapper (holds session identity, governance context, orchestration authority)
2. Constructs I1, I2, I3 agent wrappers (each holds their protocol binding, tool references, and participant_id)
3. Each agent wrapper implements `NexusParticipant` interface (`register`, `execute_tick`, `receive_state`, `project_state`)
4. Registers all agents with the appropriate Nexus instances
5. Injects RGE adapter as a participant (already built)

**Files:**
- New: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Agent_Lifecycle_Manager.py`
- New: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Agent_Wrappers.py` (I1/I2/I3/Logos wrappers implementing NexusParticipant)

**Constraints:**
- Agent wrappers delegate to existing tool libraries. They do not duplicate logic.
- Agent `participant_id` values must satisfy lexicographic ordering for deterministic tick execution.
- Logos Agent wrapper has orchestration authority. I1/I2/I3 do not.

### P1.2 — Nexus Construction Factory

**Current state:** Multiple Nexus implementations exist (LP, SCP, ARP, MTP, CSP, SOP, DRAC, EMP) but none are instantiated at runtime. The startup chain does not construct any Nexus.

**Required:**

Create `NexusFactory` that:

1. Constructs the primary LP Nexus (Logos Protocol Nexus — the main execution nexus)
2. Constructs MeshEnforcer and MREGovernor instances with appropriate configuration
3. Optionally constructs secondary Nexuses for protocol-specific routing (SCP, ARP, etc.) — V1 may operate with a single LP Nexus only
4. Wires MSPC pipeline construction with `TopologyContextProvider` as `runtime_ref` (M6 Task B)

**Files:**
- New: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Nexus_Factory.py`

### P1.3 — Main Tick Loop

**Current state:** No execution loop exists.

**Required:**

Create `RuntimeLoop` that:

1. Receives the `LOGOS_AGENT_READY` context from startup
2. Calls `AgentLifecycleManager` to instantiate and register agents
3. Calls `NexusFactory` to construct Nexus and MSPC pipeline
4. Enters the main loop:
   - Waits for task ingestion (initially: pull from queue, file, or stdin)
   - Derives constraints via `TaskConstraintProvider` (M6 Task A)
   - Calls `execute_orchestration_tick()` (M6 Task C)
   - Routes MSPC output to MTP egress pipeline
   - Delivers rendered output to external boundary
   - Repeats
5. Handles halt propagation (MSPC halt, governance halt → clean shutdown)
6. Handles session termination (graceful exit, audit log closure)

**Files:**
- New: `LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Orchestration/Runtime_Loop.py`
- Modified: `STARTUP/LOGOS_SYSTEM.py` — after `LOGOS_AGENT_READY`, call into `RuntimeLoop.run()`

**This is the single most important milestone.** Without P1.3, LOGOS cannot execute.

### P1.4 — Startup → Runtime Handoff

**Current state:** `RUN_LOGOS_SYSTEM()` returns a dict. The `if __name__ == "__main__"` block in `START_LOGOS.py` receives this and does nothing further.

**Required:**

Wire `LOGOS_AGENT_READY` result into `RuntimeLoop.run()`. This is the bridge between the existing startup chain and the new runtime activation.

**Files:**
- Modified: `STARTUP/LOGOS_SYSTEM.py` — call `RuntimeLoop` after orchestration plan is ready
- Modified: `STARTUP/START_LOGOS.py` — ensure the handoff is clean

---

## 4. P2 — Subsystem Completion

**Prerequisite:** P1 complete (tick loop functional with stub agents).

**Objective:** Replace all stub subsystems with operational implementations. These workstreams can proceed in parallel.

### P2.1 — UWM Implementation

**Current state:** Stubs only.

**Required:**
- Session-scoped in-memory SMP store (dict-based is fine for V1)
- Governed read API per Phase-2.2 UWM Read-Only API Spec (role + scope + provenance)
- Write API restricted to Logos Agent only
- SMP classification state tracking (rejected → conditional → provisional → canonical)
- AA catalog per SMP (append-only, hash-chained)
- No persistence across sessions (V1 is session-scoped)

**Governance:** Phase-2.1.1 SMP/AA schema appendix is design-complete and binding. Implementation must conform.

**Files:**
- Rewrite: `CSP_Core/Unified_Working_Memory/__init__.py` and associated modules
- New: `CSP_Core/Unified_Working_Memory/SMP_Store.py`
- New: `CSP_Core/Unified_Working_Memory/AA_Catalog.py`
- New: `CSP_Core/Unified_Working_Memory/UWM_Access_Control.py`

### P2.2 — SCP Core Orchestrator

**Current state:** `SCP_Core/__init__.py` exports stubs. MVS/BDN subsystems are built. I1 tooling (analysis runner, adapters, binder) is built. No orchestrator connects them.

**Required:**
- `SCPOrchestrator` class that receives an SMP, runs MVS/BDN analysis via existing adapters, and produces I1AA
- Wire to I1 agent wrapper's `execute_tick()` — when I1 receives an SMP routed to SCP, it delegates to `SCPOrchestrator`
- Replace stub exports in `SCP_Core/__init__.py`

**Files:**
- New: `SCP_Core/SCP_Orchestrator.py`
- Modified: `SCP_Core/__init__.py` — replace stubs with real exports

### P2.3 — CSP Canonical Promotion Path

**Current state:** Design-only. No runtime implementation of the classification ladder or canonical SMP production.

**Required:**
- SMP classification enforcement (monotonic: rejected → conditional → provisional → canonical)
- Logos Agent promotion evaluator: checks required AA types present, no unresolved conflicts, EMP proof coverage (when available)
- Canonical SMP (C-SMP) production: new immutable SMP derived from source + AAs, stored in CSP
- Integration with UWM store (P2.1)

**Files:**
- New: `CSP_Core/Promotion/SMP_Promotion_Evaluator.py`
- New: `CSP_Core/Promotion/Canonical_SMP_Producer.py`

### P2.4 — DRAC Session Reconstruction

**Current state:** `DRAC_Core` class with phase tracking shell. Semantic axioms and contexts exist as files under `DRAC_Invariables/`. Registries exist (`AF_Family_Registry.json`, `Compatibility_Matrix.json`, `Core_Interface_Registry.json`). No assembly pipeline.

**Required:**
- `DRAC_Assembler` that scans monolith directories, resolves dependencies, and produces a session-specific import graph
- Semantic axiom loading: read from `SEMANTIC_AXIOMS/`, validate, register
- Contextual embedding loading: read from `SEMANTIC_CONTEXTS/`, validate against axioms, register
- Application function loading: read from registries, resolve compatibility, register
- Dependency resolution: topological sort of import graph, detect cycles, report dead code
- Session artifact: a frozen, auditable record of what was assembled for this session

**This is the architectural crown jewel of LOGOS.** It is what makes each session a fresh compilation rather than a static monolith. V1 can use a simplified version that loads canonical modules without dynamic resolution, but the architecture must be in place.

**Files:**
- New: `DRAC_Core/DRAC_Assembler.py`
- New: `DRAC_Core/Dependency_Resolver.py`
- New: `DRAC_Core/Session_Artifact.py`
- Modified: `DRAC_Core/DRAC_Core.py` — wire assembler into phase orchestration

### P2.5 — EMP Deployment

**Current state:** Blueprint complete. Implementation modules exist. Deployment gated on external dependencies.

**Required (sequential):**
1. Coq environment resolution (coqc on PATH or jsCoq WebAssembly bridge)
2. PXL kernel axiom set formal declaration (canonicalize from `PXLv3_SemanticModal.v`)
3. Wire `EMP_Coq_Bridge` to Coq subprocess with timeout enforcement
4. Wire `EMP_Meta_Reasoner` six-tier classification into MSPC PostProcessGate
5. Wire `EMP_MSPC_Witness` for four-modality coherence checking
6. Logos Agent approval of MSPC routing path
7. Integration test with live MSPC output

**Files:** Existing EMP modules under `Epistemic_Monitoring_Protocol/EMP_Core/`. Modifications for wiring, not reimplementation.

### P2.6 — SOP Runtime Observation

**Current state:** Nexus exists. Tools exist (startup gate, invariant enforcer, DRAC integration bridge, operational logger). No runtime observation loop.

**Required:**
- SOP observer that runs as a NexusParticipant in the LP Nexus (or a parallel observation channel)
- Per-tick health snapshot: participant execution times, halt events, MRE state, telemetry summary
- Audit event emission to operational logger
- No readback into runtime (SOP is write-only to audit, never influences execution)

**Files:**
- New: `SOP_Core/Runtime_Observer.py` implementing NexusParticipant
- Modified: SOP Nexus registration to include observer

---

## 5. P3 — Integration Wiring

**Prerequisite:** P1 complete, P2 subsystems individually functional.

**Objective:** Wire subsystems into end-to-end execution paths. After P3, a task enters the system and a governed NL output exits.

### P3.1 — SMP Pipeline (End-to-End)

Wire the complete SMP lifecycle:

```
Task Ingestion
  → Logos Agent creates SMP from task input
  → SMP enters UWM (classification: conditional)
  → Logos Agent routes SMP to I1 (via SCP)
  → I1 produces I1AA (via SCP orchestrator + MVS/BDN)
  → I1AA appended to SMP in UWM
  → Logos Agent routes SMP to I3 (via ARP)
  → I3 produces I3AA (via ARP compiler)
  → I3AA appended to SMP in UWM
  → Logos Agent routes SMP to I2 (via MTP)
  → I2 produces I2AA (egress critique)
  → I2AA appended to SMP in UWM
  → Logos Agent evaluates promotion readiness
  → If ready: produce C-SMP (canonical)
  → Route resolved output to MTP egress pipeline
  → MTP renders NL → output emission
```

This is the primary cognitive loop. Every component exists in isolation. P3.1 wires them together.

### P3.2 — RGE ↔ MSPC ↔ SMP Pipeline

Wire topology-aware compilation into the SMP pipeline:

- RGE evaluates topology based on task constraints (M6)
- MSPC receives topology context (M6)
- MSPC compilation results influence SMP routing decisions (which protocol gets which SMP)
- Topology advice from RGE feeds back into Logos Agent routing logic (advisory only, per subordination contract)

### P3.3 — EMP ↔ MSPC Coherence Loop (Octafolium)

Wire the EMP-MSPC dual-compiler coherence engine:

1. I2 + fractal TRI-CORE explores abstraction space → candidate claims
2. Ship to MSPC → formalize in NL + math + lambda + PXL simultaneously
3. Ship to EMP → CONC compiler produces multi-layer artifacts
4. Back to I2 → mediate via privation gating + bridge principle + Trinitarian optimization
5. Back to MSPC → diff comparison of I2→EMP→I2 transformation
6. Loop closes → MSPC validates coherence

This is the advanced reasoning loop. May be deferred to V1.1 if EMP deployment (P2.5) takes longer than expected.

### P3.4 — Import Path Remediation

**Current state:** Multiple duplicate modules across legacy paths (`GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Spine/`, `System_Entry_Point/Agent_Orchestration/`, `Runtime_Spine/Agent_Orchestration/`, etc.). The Phase 6 module load sequence shows modules being loaded from multiple conflicting paths.

**Required:**
- Canonical import path audit: for every module, identify the single authoritative path
- Redirect all consumers to canonical paths
- Remove or deprecate legacy copies
- CI check to prevent new legacy path usage

This is not glamorous but failure to do it will cause import failures, circular dependencies, and version drift during P3 integration.

---

## 6. P4 — Governance Hardening

**Prerequisite:** P3 complete (end-to-end path functional).

**Objective:** Validate the complete system against governance invariants. Produce audit artifacts. Ensure adversarial robustness.

### P4.1 — Adversarial Battery Testing

Extend the existing 1500/1500 PASS adversarial test framework to cover:
- Full tick execution (not just RGE scoring)
- SMP lifecycle (creation → classification → promotion → canonicalization)
- Cross-tick boundary integrity (no state leakage)
- Halt propagation (every halt site triggers clean shutdown)
- Authority boundary enforcement (agents cannot escalate, protocols cannot mutate)

### P4.2 — Governance Audit Trail

Produce Phase locks and closure reports for all P1–P3 milestones:
- Phase lock artifacts (JSON, per existing convention)
- Closure reports documenting what was built, what was deferred, what invariants hold
- Comprehensive import graph audit (canonical paths only)
- Print cleanup (695 production-surface prints tracked since M5)

### P4.3 — Logging v2

Extend operational logging from v1 (startup chain only) to cover:
- Protocol lifecycle events
- Bridge crossing events (runtime ↔ operations boundary)
- Agent tick execution events
- SMP classification state transitions
- Halt and recovery events

### P4.4 — DRAC Validation

Validate session reconstruction produces deterministic results:
- Same input → same import graph
- Same import graph → same execution surface
- Dead code detection works
- Circular dependency detection works
- Session artifacts are immutable and auditable

---

## 7. P5 — V1 Operational Boundary

**Prerequisite:** P4 complete (system validated).

**Objective:** Define and implement the external interface for V1 operation.

### P5.1 — Task Input Boundary

Define how tasks enter the system:
- **Option A — CLI:** stdin/file-based task submission. Minimal. Testable.
- **Option B — API:** HTTP/gRPC endpoint. Scalable. More infrastructure.
- **Option C — GUI integration:** Angular app submits tasks. Requires GUI ↔ runtime bridge.

Recommendation: **Option A for V1.** CLI task submission. JSON-formatted task objects with declared constraints. The system reads, processes, emits output, and waits for the next task.

### P5.2 — Output Delivery Boundary

Define how results exit the system:
- MTP egress pipeline produces rendered NL (L1 surface text)
- Output includes provenance metadata (SMP ID, AA chain, classification state, confidence)
- **V1 delivery:** stdout or file. JSON-wrapped output with NL text + metadata.

### P5.3 — Session Lifecycle

Define session boundaries:
- Session starts when `START_LOGOS` is invoked
- Session ends when the tick loop terminates (explicit exit, halt, or signal)
- All session state is ephemeral (no persistence across sessions — DRAC reconstructs fresh each time)
- Audit logs persist (append-only JSONL, written by operational logger)

### P5.4 — V1 Definition of Done

LOGOS V1 is operational when:

1. `START_LOGOS` succeeds (startup chain: PXL gate, lock-and-key, LEM discharge, orchestration plan)
2. Runtime activates (agents instantiated, Nexus constructed, tick loop entered)
3. A task submitted via CLI produces a governed NL output
4. The SMP lifecycle completes (creation → I1AA → I3AA → I2AA → promotion evaluation → MTP rendering)
5. RGE produces topology advice that reaches MSPC compilation (M6 loop)
6. Operational logging captures the full execution trace
7. Adversarial tests pass with zero failures
8. Session terminates cleanly with audit log closure

---

## 8. Dependency Graph

```
M6 (committed)
  │
  ▼
P1.1 Agent Lifecycle Manager
P1.2 Nexus Construction Factory
  │
  ▼
P1.3 Main Tick Loop ◄── P1.4 Startup Handoff
  │
  ├──────────────────────────────────────────┐
  ▼                                          ▼
P2.1 UWM                               P2.4 DRAC
P2.2 SCP Orchestrator                   P2.5 EMP
P2.3 CSP Promotion                      P2.6 SOP Observer
  │                                          │
  ├──────────────────────────────────────────┘
  ▼
P3.1 SMP Pipeline (end-to-end)
P3.2 RGE ↔ MSPC ↔ SMP wiring
P3.3 EMP ↔ MSPC coherence (optional V1)
P3.4 Import Path Remediation
  │
  ▼
P4.1 Adversarial Testing
P4.2 Governance Audit Trail
P4.3 Logging v2
P4.4 DRAC Validation
  │
  ▼
P5.1 Task Input Boundary
P5.2 Output Delivery
P5.3 Session Lifecycle
P5.4 V1 Definition of Done
```

---

## 9. Estimated Scope

| Phase | New Files | Modified Files | Estimated Effort | Parallelizable |
|-------|-----------|----------------|-----------------|:-:|
| P1 | 4–5 | 2–3 | High | No (sequential) |
| P2.1 UWM | 3–4 | 1–2 | Medium | Yes |
| P2.2 SCP | 1–2 | 1 | Medium | Yes |
| P2.3 CSP Promotion | 2 | 0–1 | Medium | Yes |
| P2.4 DRAC | 3–4 | 1 | High | Yes |
| P2.5 EMP | 0 (wiring) | 3–5 | High | Yes |
| P2.6 SOP Observer | 1–2 | 1 | Low-Medium | Yes |
| P3.1 SMP Pipeline | 1–2 | 3–5 | High | No |
| P3.2 RGE↔MSPC↔SMP | 0–1 | 2–3 | Medium | After P3.1 |
| P3.3 EMP↔MSPC | 0–1 | 2–3 | High | After P2.5, P3.1 |
| P3.4 Import Remediation | 0 | 20–50 | Medium-High | Anytime |
| P4 | 2–5 (test/audit) | 5–10 | High | After P3 |
| P5 | 2–3 | 1–2 | Medium | After P4 |

**Total new files:** ~25–35
**Total modified files:** ~45–90
**Critical path:** M6 → P1 → P2 (parallel) → P3.1 → P3.2 → P4 → P5

---

## 10. What Can Be Deferred to V1.1

These items are valuable but not required for the V1 definition of done:

1. **EMP ↔ MSPC coherence loop (P3.3)** — full Octafolium dual-compiler. V1 can operate without Coq-backed proof verification.
2. **Dynamic DRAC reconstruction** — V1 can use a static module loading sequence. Full dynamic reconstruction is the target architecture but not a V1 blocker.
3. **GUI integration** — CLI is sufficient for V1 operational demonstration.
4. **Path 2 constraint derivation** — governance-inferred constraints. V1 uses declared constraints (Path 1, per M6 spec).
5. **Phase B dynamic coupling weights** — RGE operates on static weights for V1.
6. **Logging v2** — startup logging (v1) is sufficient for V1. Runtime logging is a quality-of-life improvement.
7. **Print cleanup (695 prints)** — tracked, not blocking.
8. **Cross-session persistence** — V1 sessions are ephemeral. Persistence is a V2 concern.

---

## 11. Critical Path Items (Cannot Be Deferred)

These are the items without which LOGOS cannot be called operational:

1. **P1.3 Main Tick Loop** — without this, there is no execution
2. **P1.1 Agent Lifecycle Manager** — without this, agents cannot participate in ticks
3. **P2.1 UWM (minimal)** — without SMP storage, the cognitive loop has nowhere to store semantic state
4. **P3.1 SMP Pipeline** — without end-to-end wiring, the system cannot process a task to completion
5. **P5.1 + P5.2 Task/Output boundaries** — without I/O, the system cannot interact with the external world

Everything else is important for completeness, robustness, and governance compliance — but these five items are the irreducible minimum for "operational."

---

## 12. Recommended Execution Order

1. **Immediate:** Commit M6 (A, B, C). This is in progress.
2. **Next:** P1.1 + P1.2 (agent lifecycle + Nexus factory). These can be designed in parallel with M6 completion.
3. **Then:** P1.3 + P1.4 (tick loop + startup handoff). This is the unlock.
4. **Then (parallel):** P2.1 (UWM minimal), P2.2 (SCP orchestrator), P3.4 (import remediation — start early, run in background)
5. **Then:** P3.1 (SMP pipeline end-to-end). This is the integration milestone.
6. **Then:** P2.4 (DRAC), P2.5 (EMP), P2.3 (CSP promotion) — as resources allow
7. **Then:** P4 (hardening), P5 (operational boundary)

The fastest path to a demonstrable V1 is: M6 → P1 → P2.1 (minimal UWM) → P3.1 → P5.1/P5.2.

---

## 13. Open Governance Questions

These require human decision before implementation:

1. **V1 Nexus topology:** Single LP Nexus for all participants, or multiple protocol-specific Nexuses? Single is simpler. Multiple is architecturally cleaner.

2. **Agent wrapper design:** Thin wrappers delegating to existing tool libraries, or full agent classes with internal state? Thin is V1-appropriate. Full is target architecture.

3. **UWM V1 scope:** Minimal in-memory SMP store, or full Phase-2.2 governed API? Minimal gets V1 running. Full is governance-complete.

4. **DRAC V1 scope:** Static module loading, or simplified dynamic reconstruction? Static is V1-appropriate. Dynamic is the architectural target.

5. **Task format:** What does a V1 task look like? JSON with declared constraints? Free text requiring NL parsing? Structured SMP-like input?

6. **Output format:** Raw NL text? JSON with metadata? Both?

7. **Session mode:** Single-task (process one task, exit) or multi-task (loop until termination signal)?

---

END OF BLUEPRINT

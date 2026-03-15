SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Design_Specification
ARTIFACT_NAME: AP_V2_Tooling_DS
VERSION: 2.0
DATE: 2026-03-10
AUTHORITY: Architect

---------------------------------------------------------------------

# AP_V2_Tooling_DS
## ARCHON PRIME — V2 Tooling Architecture Design Specification (Final)

---

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | SPEC-010 |
| System | ARCHON_PRIME |
| Platform | Python 3.11+ / GitHub Codespaces |
| Artifact Type | Design Specification — Final |
| Version | v2 |
| Status | Final Draft — Pending Architect Approval |
| Schema | AP_DESIGN_SPEC_SCHEMA.json |
| Authority Source | Architect |
| Source Artifacts | RPT-002, GPT_TOOLING_AUDIT_V2, AP_TOOL_PROP_01, MASTER_SYSTEM_DESIGN_SPEC v1.0.0, AP_SYSTEM_AUDIT (77 artifacts), SPEC_AP_V2_TOOLING_ARCHITECTURE_ADDENDUM |
| Author | Claude / Formalization_Expert |
| Date | 2026-03-10 |
| Supersedes | SPEC_AP_V2_TOOLING_ARCHITECTURE.md (v1), IMPLEMENTATION_SEQUENCE.md |
| DRAC Status | Deferred — not targeted by this spec |

---

## Lineage

| Field | Value |
|---|---|
| v1 Source | SPEC_AP_V2_TOOLING_ARCHITECTURE.md (2026-03-10) |
| Addendum Source | SPEC_AP_V2_TOOLING_ARCHITECTURE_ADDENDUM (AP_SYSTEM_AUDIT, 77 artifacts) |
| Revision Basis | Addendum integration: execution spine, artifact routing, repair subsystem, simulation framework, dependency graph engine, header enforcement |
| Divergences Declared | See Section 2.1 |

---

## 1. Purpose and Scope

ARCHON_PRIME is a deterministic, single-pass crawl-mutation-validation engine for the LOGOS repository. Its function is to walk the LOGOS module graph exactly once, apply all required canonical mutations in that pass, validate each module before advancing, and produce a complete, auditable artifact trail.

The V1 tooling pass confirmed that the original AP architecture was structurally correct. Failure was caused not by design error but by missing execution infrastructure. Specifically, six layers were not implemented: orchestration controller, repair subsystem, simulation subsystem, artifact routing, configuration layer, and dependency graph engine. V2 completes these layers without redesigning the system.

**Addendum architectural principle (authoritative):** The correct V2 strategy is to complete the execution infrastructure. Redesign is not warranted.

### In Scope

- Execution spine (orchestration controller)
- Artifact routing system
- Repair subsystem
- Simulation framework
- Dependency graph engine
- Configuration layer
- Header enforcement and validation
- Audit regeneration tooling (M10–M17)
- Repo analysis tooling (M20–M25)
- Crawl planning and execution (M38–M65)
- Quarantine management
- Reporting and commit finalization
- Target repo analysis subsystem (AP_TOOL_PROP_01)

### Out of Scope

- Redesigning the LOGOS runtime architecture
- Adding new LOGOS features or protocols
- Parallel or multi-threaded module processing
- Executing LOGOS modules during the crawl
- Any mutation to governance contracts themselves
- DRAC implementation (Architect standing deferment)
- LOGOS DS/IG V2 schema upgrade (separate workstream)

---

## 2. V1 Failure Analysis — Design Spec Inclusions

### 2.1 Declared Divergences from SPEC-010 v1

The following structural changes were made during addendum integration. Each divergence is stated explicitly per governance rules.

| Divergence ID | v1 Structure | v2 Structure (Final) | Reason |
|---|---|---|---|
| DIV-001 | Artifact routing in `crawler/commit/` | Artifact routing in `WORKFLOW_MUTATION_TOOLING/runtime/` | Addendum authority; cleaner subsystem boundary |
| DIV-002 | Repair modules in `crawler/repair/` | Repair subsystem in `WORKFLOW_MUTATION_TOOLING/repair/` | Addendum authority; repair is a top-level subsystem not a crawler sub-concern |
| DIV-003 | Controllers in `orchestration/controllers/` | Controllers in `WORKFLOW_MUTATION_TOOLING/controllers/` | Addendum authority; drops orchestration wrapper, simplifies hierarchy |
| DIV-004 | `task_router.py` in `orchestration/task_router/` | `task_router.py` in `controllers/` | Addendum authority; `orchestration/task_router/` retains routing table config only |
| DIV-005 | Simulation in `simulation/` with M30–M32 + coordinator | Simulation in `WORKFLOW_MUTATION_TOOLING/simulation/` with 4 addendum-defined modules | Addendum supersedes; functional analog migrations mapped |
| DIV-006 | Analysis tools in `tools/import_analysis/`, `tools/runtime_analysis/` | Dependency graph engine in `WORKFLOW_MUTATION_TOOLING/analysis/`; audit regeneration tools retained in `tools/` | Addendum creates `analysis/` as distinct subsystem; audit tools (M10–M17) remain in `tools/` |
| DIV-007 | Header schema: 13 fields | Header schema: 13 fields (superset of addendum's 6-field minimum) | No conflict; addendum 6 fields are a subset. 13-field schema remains authoritative. |

### 2.2 V1 Failure Summary (from AP_SYSTEM_AUDIT, 77 artifacts)

| Failure Category | Evidence | V2 Resolution |
|---|---|---|
| Missing orchestration layer | `orchestration/controllers/` directory existed, no code | `controllers/` subsystem: 5 modules |
| Missing repair subsystem | S7_ERROR_REPAIR: 0% completion | `repair/` subsystem: 5 modules |
| Missing simulation subsystem | Simulation modules skeletal (146–166B); non-functional stubs | `simulation/` subsystem: 4 modules, full rebuild |
| Missing artifact routing | Modules writing to stdout; no routing layer | `runtime/` subsystem: 3 modules |
| Missing configuration files | 6 required configs absent; pipeline fails at init | `configs/` layer: 6 files |
| Incomplete dependency graph | `dependency_graph.py` incomplete; no cycle detection or execution ordering | `analysis/` subsystem: 3 modules |
| 0/93 header compliance | No module had complete AP metadata header | Header enforcement + `validation/header_validator.py` |
| 35/39 canonical modules missing | Spec-required modules absent across all subsystems | Full module inventory defined; implementation sequence in Section 15 |
| Routing table legacy paths | `routing_table.json` pointed to dissolved `AUDIT_SYSTEM/` | Rebuilt with V2 canonical paths |
| 22 analog modules unresolved | Functional analogs at wrong paths or wrong names | Migration table in Section 7 |

---

## 3. Architectural Principle

V2 preserves the original AP architecture. The V1 design was correct. The implementation did not complete the execution infrastructure. V2 strategy: complete what was specified.

**Non-negotiable structural rules (all binding):**

- FR-001: All runtime modules must reside in exactly one of three canonical workflow domains.
- FR-002: All 39 canonical modules plus addendum-defined modules must be built in dependency order.
- FR-003: Every analog module must be classified before replacement or migration. Non-deletion policy applies.
- FR-004: All 6 config files must exist before pipeline initialization. They are source files, not generated artifacts.
- FR-005: All audit tools must expose a standard `run(target: str) -> dict` interface.
- FR-006: `routing_table.json` must contain no legacy `AUDIT_SYSTEM/` references.
- FR-007: Architecture validator (SPEC-004) must pass before any gated stage proceeds.
- FR-008: Repo analysis pipeline (TA-01 through TA-04) is the primary analysis engine for external target repos.
- FR-009: No mutation may execute without simulation approval. Simulation must PASS before `--execute` flag is authorized.
- FR-010: All modules must produce structured JSON artifacts. stdout-only output is prohibited.
- FR-011: All modules must register outputs through `runtime/artifact_router.py`.
- FR-012: All modules must carry a complete AP metadata header (13 fields minimum).

---

## 4. Canonical Directory Architecture

### 4.1 Domain Assignment Rule

Every module, config, schema, and artifact belongs to exactly one of five root directories. Two are immutable; three are mutable.

```
ARCHON_PRIME/
├── AP_SYSTEM_CONFIG/             [IMMUTABLE — design specs, governance, platform configs]
├── AP_SYSTEM_AUDIT/              [IMMUTABLE — V1 audit artifacts, historical reports]
├── WORKFLOW_MUTATION_TOOLING/    [MUTABLE — AP runtime engine, all tooling]
├── WORKFLOW_TARGET_AUDITS/       [MUTABLE — audit modules for external repos]
└── WORKFLOW_TARGET_PROCESSING/   [MUTABLE — target repo staging and processing]
```

No module may exist outside these five directories. Root-level legacy directories (`controllers/`, `crawler/`, `repair/`, `simulation/`, `AUDIT_SYSTEM/`, `AUDIT_LOGS/`) are migration sources. Non-deletion policy applies — legacy modules are copied to canonical paths, not deleted.

### 4.2 WORKFLOW_MUTATION_TOOLING — Full V2 Directory Tree

```
WORKFLOW_MUTATION_TOOLING/
│
├── controllers/                          [EXECUTION SPINE — addendum Section 2]
│   ├── workflow_controller.py            [stage orchestration, master pipeline driver]
│   ├── task_router.py                    [task dispatch between subsystems]
│   ├── execution_scheduler.py            [pipeline stage sequencing and gating]
│   ├── pipeline_runner.py                [entry point; invokes all stages in order]
│   └── runtime_context_manager.py        [runtime state; artifact registry handle]
│
├── runtime/                              [ARTIFACT ROUTING SYSTEM — addendum Section 3]
│   ├── artifact_router.py                [route artifacts to canonical directories]
│   ├── output_registry.py                [maintain artifact registry; enforce schema compliance]
│   └── routing_table.py                  [routing_table.json loader + path resolution]
│
├── repair/                               [REPAIR SUBSYSTEM — addendum Section 4]
│   ├── repair_engine.py                  [orchestrates repair pipeline]
│   ├── patch_generator.py                [generate deterministic patch plans]
│   ├── schema_repair.py                  [correct schema violations]
│   ├── dependency_rewriter.py            [correct import paths, rewrite deep imports]
│   └── module_normalizer.py              [normalize module structure to spec]
│
├── simulation/                           [SIMULATION FRAMEWORK — addendum Section 5]
│   ├── runtime_simulator.py              [simulate runtime execution; detect dependency breakage]
│   ├── import_surface_simulator.py       [simulate import surface; detect facade violations]
│   ├── integration_simulator.py          [simulate module integration; detect interface mismatches]
│   └── mutation_simulator.py             [simulate all mutations before live execution]
│
├── analysis/                             [DEPENDENCY GRAPH ENGINE — addendum Section 6]
│   ├── dependency_graph_builder.py       [build full import dependency graph]
│   ├── cycle_detector.py                 [detect circular dependencies]
│   └── execution_order_planner.py        [compute deterministic execution order]
│
├── tools/                                [AUDIT REGENERATION + ANALYSIS — Stage1/Stage2]
│   ├── repo_mapping/
│   │   ├── repo_directory_scanner.py     [M10 — migrate+rename from repo_scanner.py]
│   │   ├── python_file_collector.py      [M11 — build]
│   │   └── module_index_builder.py       [M20 — build]
│   ├── import_analysis/
│   │   ├── import_extractor.py           [M12 — migrate+rename from import_scanner.py]
│   │   ├── symbol_import_extractor.py    [M13 — build]
│   │   ├── circular_dependency_detector.py [M22 — build; analysis/ is primary; this is scan-phase version]
│   │   └── canonical_import_registry_builder.py [M25 — build]
│   ├── governance_analysis/
│   │   └── governance_contract_scanner.py [M15 — migrate+rename from governance_scanner.py]
│   ├── runtime_analysis/
│   │   ├── runtime_phase_mapper.py       [M23 — build]
│   │   └── runtime_boot_sequencer.py     [M24 — build]
│   ├── normalization_tools/
│   │   ├── schema_registry.py            [M00 — PRESENT functional]
│   │   ├── header_schema_scanner.py      [M14 — migrate+rename from header_validator.py]
│   │   └── header_schema.json            [config — canonical header field definitions]
│   └── audit_tools/
│       ├── repair_registry_loader.py     [M02 — build]
│       ├── audit_utils.py                [PRESENT — keep]
│       ├── circular_dependency_audit.py  [PRESENT — wire to pipeline]
│       ├── cross_package_dependency_audit.py [PRESENT — wire]
│       ├── duplicate_module_audit.py     [PRESENT — wire]
│       ├── facade_bypass_audit.py        [PRESENT — wire]
│       ├── header_schema_audit.py        [PRESENT — wire]
│       ├── import_surface_audit.py       [PRESENT — wire]
│       ├── module_path_ambiguity_audit.py [PRESENT — wire]
│       ├── namespace_shadow_audit.py     [PRESENT — wire]
│       ├── orphan_module_audit.py        [PRESENT — wire]
│       ├── run_audit_suite.py            [PRESENT — modify: add target_path param]
│       ├── run_governance_audit.py       [PRESENT — modify: add target_path param]
│       └── unused_import_audit.py        [PRESENT — wire]
│
├── validation/                           [HEADER + ARCHITECTURE VALIDATION]
│   ├── validate_architecture.py          [M-VAL-01 — SPEC-004]
│   └── header_validator.py               [addendum Section 8 — validate AP metadata headers]
│
├── crawler/                              [CRAWL PLANNING + EXECUTION — Stage4]
│   ├── engine/
│   │   ├── crawl_planner.py              [M38 — build]
│   │   ├── crawl_executor.py             [M60 — rebuild from skeletal crawl_engine.py]
│   │   └── checklist_evaluator.py        [pre-crawl gate evaluator]
│   ├── pipeline/
│   │   ├── module_processor.py           [M61 — build]
│   │   ├── syntax_validator.py           [M62 — build]
│   │   ├── governance_validator.py       [M63 — build]
│   │   └── phase_validator.py            [M64 — build]
│   ├── mutation/
│   │   ├── header_injector.py            [M50 — migrate from repair/operators/]
│   │   └── import_rewriter.py            [M51 — migrate from repair/operators/]
│   ├── monitor/
│   │   └── crawl_monitor.py              [M65 — rebuild from 142B skeleton]
│   └── quarantine/
│       └── quarantine_manager.py         [M80 — build]
│
├── orchestration/                        [ROUTING CONFIG ONLY — reduced from v1]
│   ├── task_router/
│   │   ├── routing_table.json            [config — V2 canonical paths; rebuilt]
│   │   └── routing_table_loader.py       [M01 — expanded]
│   └── execution_graphs/
│       └── execution_graph_builder.py    [M39 — build]
│
├── registry/
│   ├── module_registry.json              [PRESENT — expand to full inventory]
│   ├── audit_registry.json               [PRESENT — keep]
│   └── repair_registry.json              [PRESENT — update operator paths]
│
├── configs/                              [CONFIGURATION LAYER — addendum Section 7]
│   ├── ap_config.yaml                    [required — architect override layer]
│   ├── logos_targets.yaml                [required — target repo definitions]
│   ├── crawl_configs/
│   │   └── crawl_config.json             [required — runtime crawl parameters]
│   └── phase_maps/
│       └── phase_map_config.json         [required — stage gate definitions]
│
├── schemas/
│   ├── CrawlMutationRecord.schema.json   [PRESENT]
│   ├── ValidationManifest.schema.json    [PRESENT]
│   ├── PhaseGate.schema.json             [PRESENT]
│   └── QuarantineRecord.schema.json      [PRESENT]
│
└── utils/
    └── logger.py                         [PRESENT — functional JSON event logger]
```

### 4.3 WORKFLOW_TARGET_AUDITS — Full V2 Tree

Replaces legacy `AUDIT_SYSTEM/` and `AUDIT_LOGS/`. Hosts the AP_TOOL_PROP_01 four-stage repo analysis pipeline.

```
WORKFLOW_TARGET_AUDITS/
├── modules/
│   ├── repo_mapping/
│   │   └── repo_mapper.py                [migrate from AUDIT_SYSTEM/scripts/repo_scanners/]
│   ├── collection/
│   │   └── artifact_collector.py         [TA-01 — Stage0: traversal + indexing]
│   ├── structure_analysis/
│   │   └── structure_analyzer.py         [TA-02 — Stage1: structural intelligence]
│   ├── subsystem_analysis/
│   │   └── subsystem_analyzer.py         [TA-03 — Stage2: subsystem completeness]
│   └── gap_analysis/
│       └── gap_analysis_engine.py        [TA-04 — Stage3: remediation guidance]
├── configs/
│   └── audit_module_config.json          [file type filters, exclusion rules]
├── logs/                                  [runtime logs — replaces AUDIT_LOGS/]
└── reports/                               [per-repo audit reports, timestamped]
```

### 4.4 WORKFLOW_TARGET_PROCESSING — V2 Structure

```
WORKFLOW_TARGET_PROCESSING/
├── incoming/           [drop zone for external repos and archives]
├── targets/
│   ├── repos/          [target repo clones]
│   └── subsystems/     [subsystem work directories]
├── design_specs/       [authoritative DS for target repo subsystems]
├── implementation_guides/
├── processing/         [active workspace during mutation]
└── validated/          [output of validated processing passes]
```

---

## 5. Subsystem Definitions

### 5.1 Execution Spine (controllers/)

The execution spine is the top-level pipeline driver. All other subsystems are invoked through it. Nothing runs outside the execution spine during a pipeline execution.

| Module | Role | Key Interfaces |
|---|---|---|
| `pipeline_runner.py` | Entry point; invokes all 7 stages in order; owns the execution manifest | `run(target, mode)` → `ExecutionManifest` |
| `workflow_controller.py` | Orchestrates stage-to-stage handoff; enforces gate conditions | `execute_stage(stage_id, context)` → `StageResult` |
| `execution_scheduler.py` | Builds stage execution plan from phase_map_config.json; enforces blocking constraints | `schedule(phase_map)` → `ExecutionPlan` |
| `task_router.py` | Routes tasks between subsystems; dispatches to correct module by task type | `route(task)` → `DispatchResult` |
| `runtime_context_manager.py` | Holds runtime state shared across all stages; provides artifact registry handle | `get_context()` → `RuntimeContext` |

**Gate enforcement:** `workflow_controller.py` must halt the pipeline if any blocking gate condition fails. It must not pass execution to the next stage with an unresolved blocking failure.

### 5.2 Artifact Routing System (runtime/)

No module may write an output artifact by hardcoding a path. All output writes route through `artifact_router.py`. All outputs must be structured JSON. stdout-only outputs are a violation.

| Module | Role | Key Interfaces |
|---|---|---|
| `artifact_router.py` | Receives artifact + artifact_type; resolves canonical path from routing_table; writes file | `route(artifact, artifact_type, metadata)` → `RoutingResult` |
| `output_registry.py` | Maintains in-session registry of all artifacts produced; enforces schema compliance | `register(artifact_path, schema_name)` → `RegistryEntry` |
| `routing_table.py` | Loads routing_table.json; exposes path resolution; validates no legacy paths present | `get_path(artifact_type)` → `str` |

**Routing targets:** All target-repo audit outputs route to `WORKFLOW_TARGET_AUDITS/reports/`. All self-audit and pipeline execution outputs route to `WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/`.

### 5.3 Repair Subsystem (repair/)

Deterministic, automated repair of detected issues. Repair operates after classification by the crawl pipeline. No repair may execute without a patch plan being generated first.

| Module | Role | Key Interfaces |
|---|---|---|
| `repair_engine.py` | Orchestrates repair pipeline; manages retry loop and escalation to quarantine | `repair(violation, simulate)` → `RepairResult` |
| `patch_generator.py` | Generates deterministic patch plan from violation record | `generate(violation)` → `PatchPlan` |
| `schema_repair.py` | Applies schema-level corrections (header injection, field normalization) | `apply(patch, simulate)` → `PatchResult` |
| `dependency_rewriter.py` | Rewrites import paths; corrects deep imports; enforces canonical import facade | `rewrite(patch, simulate)` → `PatchResult` |
| `module_normalizer.py` | Normalizes module structure to spec (path relocation, namespace disambiguation) | `normalize(patch, simulate)` → `PatchResult` |

**Safety rule:** `repair_engine.py` must pass `simulate=True` to all operators unless `--execute` mode is active and VG-SIM has passed.

### 5.4 Simulation Framework (simulation/)

Pre-mutation simulation. The simulation framework must PASS before `--execute` mode is authorized. Simulation failure blocks live mutation absolutely.

| Module | Role | Key Interfaces |
|---|---|---|
| `runtime_simulator.py` | Simulates runtime execution of target repo; detects dependency breakage | `simulate(module_index, dependency_graph)` → `SimResult` |
| `import_surface_simulator.py` | Simulates import surface; detects facade violations | `simulate(repo_imports, facade_registry)` → `SimResult` |
| `integration_simulator.py` | Simulates module integration; detects interface mismatches | `simulate(module_index, governance_map)` → `SimResult` |
| `mutation_simulator.py` | Simulates all planned mutations before execution; produces mutation preview | `simulate(crawl_plan, patch_plans)` → `MutationSimResult` |

**Simulation gate (VG-SIM):** All four simulators must return `status: PASS`. A single FAIL in any simulator blocks `--execute`. `mutation_simulator.py` must run last, after the other three pass.

### 5.5 Dependency Graph Engine (analysis/)

The dependency graph engine builds the import graph and computes the deterministic execution order that the crawl planner consumes.

| Module | Role | Key Interfaces |
|---|---|---|
| `dependency_graph_builder.py` | Builds directed import graph from `repo_imports.json` and `module_index.json` | `build(imports, module_index)` → `DependencyGraph` |
| `cycle_detector.py` | Detects circular dependencies using DFS; produces cycle groups | `detect(graph)` → `CycleReport` |
| `execution_order_planner.py` | Computes topological sort of dependency graph; produces execution order | `plan(graph, cycle_report)` → `ExecutionOrder` |

### 5.6 Configuration Layer (configs/)

Configuration files are source files, not generated artifacts. They must exist before pipeline initialization. `ap_config.yaml` is the architect override layer; values in it supersede `crawl_config.json` defaults.

| File | Path | Purpose |
|---|---|---|
| `ap_config.yaml` | `configs/ap_config.yaml` | Architect-editable override: mutation mode, log level, simulation enforcement |
| `logos_targets.yaml` | `configs/logos_targets.yaml` | Target repo definitions: path, branch, language |
| `crawl_config.json` | `configs/crawl_configs/crawl_config.json` | Runtime crawl parameters: depth, exclusions, repair thresholds |
| `phase_map_config.json` | `configs/phase_maps/phase_map_config.json` | Stage gate definitions, blocking constraints |
| `routing_table.json` | `orchestration/task_router/routing_table.json` | Artifact output path routing (V2 paths only) |
| `header_schema.json` | `tools/normalization_tools/header_schema.json` | Canonical header field definitions |

### 5.7 Header Enforcement (validation/header_validator.py)

0 of 93 modules in V1 had complete AP metadata headers. V2 enforces headers as a blocking gate condition.

**Required header fields (13 — superset of addendum's 6-field minimum):**
```python
# AP METADATA HEADER
# artifact_id: <module ID>
# system: ARCHON_PRIME
# purpose: <one sentence>
# author: ARCHON_PRIME
# authority: Architect
# timestamp: <ISO creation date>
# module_name: <filename without .py>
# subsystem: <subsystem ID>
# canonical_path: WORKFLOW_MUTATION_TOOLING/<relative path>
# runtime_stage: <initialization|analysis|processing|validation|repair|audit|reporting|utility>
# spec_reference: SPEC-010.section.<N>
# implementation_phase: PASS_<N>
# status: canonical|draft|deprecated
```

**Validator interface:**
```python
def validate_file(file_path: str, schema: dict) -> dict
  # Returns {"status": "PASS|FAIL", "missing_fields": [...], "file": "<path>"}

def validate_directory(dir_path: str, schema: dict) -> dict
  # Returns {"total": 0, "compliant": 0, "violations": [...]}
```

---

## 6. Pipeline Execution Model

### 6.1 Seven-Stage Pipeline (addendum Section 9)

```
Stage0 — FOUNDATION
  Load configs; initialize runtime context; validate architecture (VG-ARCH)
  Entry point: pipeline_runner.py → workflow_controller.py
  Gate: VG-ARCH must PASS before Stage1 begins

Stage1 — AUDIT (audit regeneration)
  Run M10–M17 against target repo
  Outputs: repo_directory_tree.json, repo_python_files.json, repo_imports.json,
           header_schema_compliance.json, governance_contract_map.json
  Gate: all S1 artifacts present and schema-valid

Stage2 — ANALYSIS (repo analysis)
  Run analysis/ subsystem: dependency_graph_builder → cycle_detector → execution_order_planner
  Run tools/ analysis: module_index_builder, runtime_phase_mapper, runtime_boot_sequencer,
                       canonical_import_registry_builder
  Outputs: dependency_graph.json, cycle_report.json, execution_order.json,
           module_index.json, runtime_phase_map.json, runtime_boot_sequence.json
  Gate: dependency_graph.json non-empty; execution_order.json valid

Stage3 — SIMULATION
  Run simulation/ subsystem: runtime_simulator → import_surface_simulator →
                              integration_simulator → mutation_simulator
  Output: simulation_report.json
  Gate VG-SIM: simulation_report.status == "PASS" on all four simulators
  HARD RULE: --execute mode is blocked unless VG-SIM passes in the current session

Stage4 — CRAWLER (crawl planning + execution)
  Pre-crawl: crawl_planner.py → execution_graph_builder.py → checklist_evaluator.py
  Crawl loop (per module):
    module_processor → syntax_validator → crawler/mutation/ → governance_validator →
    phase_validator → syntax_validator (post-mutation) →
    if PASS: artifact_router → advance
    if FAIL: repair/ subsystem → if unresolvable: quarantine_manager

Stage5 — REPAIR
  Invoked by crawler on module failure. Also invocable standalone.
  repair_engine → patch_generator → [schema_repair | dependency_rewriter | module_normalizer]
  On repair success: return module to crawler pipeline
  On repair failure (max_attempts exceeded): escalate to quarantine_manager

Stage6 — ORCHESTRATION (reporting + commit)
  artifact_router (final routing pass) → report_generator → commit_finalizer
  Outputs: validation_report.json, repair_event_log.json, mutation_log.json,
           crawl_execution_log.json, crawl_status.json, PIPELINE_EXECUTION_MANIFEST.json
  Commit only in --execute mode with Architect authorization
```

### 6.2 Execution Mode Contract

| Flag | Default | Behavior |
|---|---|---|
| `--simulate` | Yes (default) | All reads and computation execute; no writes to target repo; artifacts produced with `"simulation": true` |
| `--execute` | No | Live mutations applied; requires VG-SIM to have passed in current session |
| `--target <path>` | Required | Path to target repo root |
| `--stage <stage_id>` | Optional | Run single stage only (for debugging; does not skip gates) |

### 6.3 Simulation Enforcement Rule

`pipeline_runner.py` must check that `simulation_report.status == "PASS"` before authorizing `--execute` mode. This check must occur at runtime, not only at startup. If simulation results are stale (older than the current session), VG-SIM is considered unresolved.

---

## 7. Analog Module Migration Table

Full catalog of 22 analog modules requiring migration. Must be logged in `AP_LEGACY_MODULE_MIGRATION_LOG.json` before migration begins.

| # | Module Name | Current Path | Classification | V2 Target Path |
|---|---|---|---|---|
| 1 | `pipeline_controller.py` | `controllers/` | MIGRATE+RENAME → `workflow_controller.py` | `WORKFLOW_MUTATION_TOOLING/controllers/` |
| 2 | `audit_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/controllers/` (wire to execution_scheduler) |
| 3 | `analysis_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/controllers/` (wire to execution_scheduler) |
| 4 | `repair_controller.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/repair/repair_engine.py` (merge logic) |
| 5 | `config_loader.py` | `controllers/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/config_loader.py` |
| 6 | `crawl_engine.py` | `crawler/core/` | REBUILD (146B skeletal) | `WORKFLOW_MUTATION_TOOLING/crawler/engine/crawl_executor.py` |
| 7 | `repo_scanner.py` | `tools/repo_mapping/` | MIGRATE+RENAME → `repo_directory_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/repo_mapping/` |
| 8 | `header_validator.py` | `tools/normalization_tools/` | MIGRATE+RENAME → `header_schema_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/` |
| 9 | `governance_scanner.py` | `tools/governance_analysis/` | MIGRATE+RENAME → `governance_contract_scanner.py` | `WORKFLOW_MUTATION_TOOLING/tools/governance_analysis/` |
| 10 | `dependency_graph.py` | `tools/runtime_analysis/` | MIGRATE+RENAME → `dependency_graph_builder.py` | `WORKFLOW_MUTATION_TOOLING/analysis/` |
| 11 | `runtime_simulator.py` | `simulation/runtime_simulator/` | REBUILD in place (functional but incomplete) | `WORKFLOW_MUTATION_TOOLING/simulation/` |
| 12 | `import_simulator.py` | `simulation/import_simulator/` | MIGRATE+RENAME → `import_surface_simulator.py` | `WORKFLOW_MUTATION_TOOLING/simulation/` |
| 13 | `repo_simulator.py` | `simulation/repo_simulator/` | REBUILD (166B, no JSON output) | Fold into `mutation_simulator.py` |
| 14 | `routing_table_loader.py` | `orchestration/task_router/` | EXPAND (reference impl) | Stay + expand in `orchestration/task_router/`; `routing_table.py` in `runtime/` wraps it |
| 15 | `schema_registry.py` | `tools/normalization_tools/` | PRESENT functional | Keep in place; add V2 header |
| 16 | `header_injection_operator.py` | `repair/operators/` | MIGRATE+RENAME → `header_injector.py` | `WORKFLOW_MUTATION_TOOLING/crawler/mutation/` |
| 17 | `import_rewrite_operator.py` | `repair/operators/` | MIGRATE+RENAME → `import_rewriter.py` | `WORKFLOW_MUTATION_TOOLING/crawler/mutation/` |
| 18 | `dependency_normalizer.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/repair/dependency_rewriter.py` (merge logic) |
| 19 | `module_relocation_operator.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/repair/module_normalizer.py` (merge logic) |
| 20 | `namespace_disambiguator.py` | `repair/operators/` | MIGRATE | `WORKFLOW_MUTATION_TOOLING/repair/module_normalizer.py` (merge logic) |
| 21 | `repo_mapper.py` | `AUDIT_SYSTEM/scripts/repo_scanners/` | MIGRATE to target audits domain | `WORKFLOW_TARGET_AUDITS/modules/repo_mapping/` |
| 22 | 18x `audit_tools/*.py` | `tools/audit_tools/` | PRESENT functional | Keep in place; add target_path param + V2 headers |

---

## 8. Canonical Module Registry

### Foundation

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M00 | schema_registry.py | tools/normalization_tools/ | PRESENT | Add header |
| M01 | routing_table_loader.py | orchestration/task_router/ | PRESENT (ref impl) | Expand |
| M02 | repair_registry_loader.py | tools/audit_tools/ | MISSING | Build |

### Audit Regeneration (Stage1)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M10 | repo_directory_scanner.py | tools/repo_mapping/ | ANALOG | Migrate+Rename |
| M11 | python_file_collector.py | tools/repo_mapping/ | MISSING | Build |
| M12 | import_extractor.py | tools/import_analysis/ | ANALOG | Migrate+Rename |
| M13 | symbol_import_extractor.py | tools/import_analysis/ | MISSING | Build |
| M14 | header_schema_scanner.py | tools/normalization_tools/ | ANALOG | Migrate+Rename |
| M15 | governance_contract_scanner.py | tools/governance_analysis/ | ANALOG | Migrate+Rename |
| M16 | runtime_phase_scanner.py | tools/runtime_analysis/ | MISSING | Build |
| M17 | concept_spec_gap_detector.py | tools/audit_tools/ | MISSING | Build |

### Repo Analysis (Stage2)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M20 | module_index_builder.py | tools/repo_mapping/ | MISSING | Build |
| M21 | dependency_graph_builder.py | analysis/ | ANALOG → rebuild | Migrate+Rebuild |
| M22 | cycle_detector.py | analysis/ | MISSING | Build |
| M23 | runtime_phase_mapper.py | tools/runtime_analysis/ | MISSING | Build |
| M24 | runtime_boot_sequencer.py | tools/runtime_analysis/ | MISSING | Build |
| M25 | canonical_import_registry_builder.py | tools/import_analysis/ | MISSING | Build |
| — | execution_order_planner.py | analysis/ | MISSING | Build |

### Simulation (Stage3)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M30 | runtime_simulator.py | simulation/ | ANALOG → rebuild | Rebuild |
| M31 | import_surface_simulator.py | simulation/ | ANALOG → rebuild+rename | Rebuild |
| M32 | integration_simulator.py | simulation/ | MISSING | Build |
| M33 | mutation_simulator.py | simulation/ | MISSING | Build (absorbs repo_simulator logic) |

### Crawl Planning + Execution (Stage4)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M38 | crawl_planner.py | crawler/engine/ | MISSING | Build |
| M39 | execution_graph_builder.py | orchestration/execution_graphs/ | MISSING | Build |
| M50 | header_injector.py | crawler/mutation/ | ANALOG | Migrate |
| M51 | import_rewriter.py | crawler/mutation/ | ANALOG | Migrate |
| M60 | crawl_executor.py | crawler/engine/ | ANALOG skeletal | Rebuild |
| M61 | module_processor.py | crawler/pipeline/ | MISSING | Build |
| M62 | syntax_validator.py | crawler/pipeline/ | MISSING | Build |
| M63 | governance_validator.py | crawler/pipeline/ | MISSING | Build |
| M64 | phase_validator.py | crawler/pipeline/ | MISSING | Build |
| M65 | crawl_monitor.py | crawler/monitor/ | SKELETON | Rebuild |
| M80 | quarantine_manager.py | crawler/quarantine/ | MISSING | Build |
| — | checklist_evaluator.py | crawler/engine/ | MISSING | Build |

### Repair (Stage5)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M70 | repair_engine.py | repair/ | MISSING | Build |
| M71 | patch_generator.py | repair/ | MISSING | Build |
| M72 | schema_repair.py | repair/ | MISSING | Build |
| M73 | dependency_rewriter.py | repair/ | ANALOG (merge) | Build + merge |
| M74 | module_normalizer.py | repair/ | ANALOG (merge) | Build + merge |

### Orchestration (Stage6)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M90 | artifact_router.py | runtime/ | MISSING | Build |
| M91 | output_registry.py | runtime/ | MISSING | Build |
| M92 | routing_table.py | runtime/ | MISSING | Build |
| M93 | report_generator.py | crawler/commit/ | MISSING | Build |
| M94 | commit_finalizer.py | crawler/commit/ | MISSING | Build |
| M95 | workflow_controller.py | controllers/ | ANALOG → rebuild | Migrate+Rebuild |
| M96 | task_router.py | controllers/ | MISSING | Build |
| M97 | execution_scheduler.py | controllers/ | MISSING | Build |
| M98 | pipeline_runner.py | controllers/ | MISSING | Build |
| M99 | runtime_context_manager.py | controllers/ | MISSING | Build |

### Validation

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| M-VAL-01 | validate_architecture.py | validation/ | SPEC-ONLY (SPEC-004 Draft) | Build after SPEC-004 approved |
| M-VAL-02 | header_validator.py | validation/ | MISSING | Build (addendum Section 8) |

### WORKFLOW_TARGET_AUDITS (AP_TOOL_PROP_01)

| Module ID | Module Name | Path | Status | Action |
|---|---|---|---|---|
| TA-01 | artifact_collector.py | WORKFLOW_TARGET_AUDITS/modules/collection/ | MISSING | Build |
| TA-02 | structure_analyzer.py | WORKFLOW_TARGET_AUDITS/modules/structure_analysis/ | MISSING | Build |
| TA-03 | subsystem_analyzer.py | WORKFLOW_TARGET_AUDITS/modules/subsystem_analysis/ | MISSING | Build |
| TA-04 | gap_analysis_engine.py | WORKFLOW_TARGET_AUDITS/modules/gap_analysis/ | MISSING | Build |

---

## 9. Subsystem Contracts

| Subsystem | May Import From | Forbidden Imports |
|---|---|---|
| Foundation (M00–M02, configs) | stdlib only | All other AP subsystems |
| Audit Regeneration (M10–M17) | Foundation, stdlib | LOGOS runtime, repair, controllers, simulation |
| Analysis (M20–M25, analysis/) | Foundation, Audit Regen, stdlib | LOGOS runtime, repair, controllers, simulation |
| Simulation (simulation/) | Foundation, Audit Regen, Analysis, stdlib | LOGOS runtime, repair, controllers |
| Crawl Planning (M38–M39) | Foundation, Analysis, Simulation, stdlib | LOGOS runtime, repair, controllers direct calls |
| Crawl Execution (M60–M65) | Foundation, Crawl Planning, crawler/mutation/, stdlib | LOGOS runtime |
| Repair (repair/) | Foundation, crawler/mutation/, stdlib | LOGOS runtime, controllers direct calls |
| Quarantine (M80) | Foundation, stdlib | All S6+, LOGOS runtime |
| Artifact Routing (runtime/) | Foundation, stdlib | LOGOS runtime |
| Orchestration/Controllers (controllers/) | All subsystems | LOGOS runtime |
| Validation (validation/) | Foundation, stdlib | LOGOS runtime |
| TARGET_AUDITS | stdlib, Foundation | All LOGOS modules, all mutation modules |

---

## 10. Artifact Surface Definition

| Surface ID | Name | Canonical Directories | Permitted Types |
|---|---|---|---|
| S-001 | runtime_surface | WORKFLOW_MUTATION_TOOLING/tools/, crawler/, simulation/, analysis/, repair/, runtime/, controllers/, validation/ | Python modules only |
| S-002 | audit_surface | WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/, WORKFLOW_TARGET_AUDITS/logs/, reports/ | JSON artifacts, logs |
| S-003 | config_surface | WORKFLOW_MUTATION_TOOLING/configs/, orchestration/task_router/, registry/ | JSON, YAML |
| S-004 | design_surface | AP_SYSTEM_CONFIG/, WORKFLOW_TARGET_PROCESSING/design_specs/, implementation_guides/ | Markdown, JSON schemas |
| S-005 | target_audit_surface | WORKFLOW_TARGET_AUDITS/modules/ | Python modules only |

**Surface isolation invariant:** Runtime modules must not exist in design_surface or audit_surface. Design artifacts must not exist in runtime_surface.

---

## 11. Validation Gate Conditions

| Gate ID | Stage | Condition | Responsible Module |
|---|---|---|---|
| VG-ARCH | Stage0 | architecture_valid == true | validate_architecture.py |
| VG-HDR | Stage0 | header_compliance_rate meets threshold | header_validator.py |
| VG-CFG | Stage0 | All 6 config files present at canonical paths | checklist_evaluator.py |
| VG-S1 | Stage1 | All 8 S1 artifacts present and schema-valid | schema_registry.validate() |
| VG-S2 | Stage2 | dependency_graph.json non-empty; execution_order.json valid | analysis/ outputs |
| VG-SIM | Stage3 | simulation_report.status == "PASS" on all four simulators | simulation_coordinator output |
| VG-CRAWL | Stage4 | crawl_plan.json valid; order_length > 0 | crawl_planner output |
| VG-MOD | Per-module | post-mutation syntax valid | syntax_validator |
| VG-FINAL | Stage6 | crawl_status.json completion_rate == 100% (excl. quarantined) | report_generator |
| VG-EXEC | Before --execute | VG-SIM passed in current session; not stale | pipeline_runner check |

---

## 12. Architecture Validation Rules (V2 Specific)

| Rule ID | Check | Blocking |
|---|---|---|
| AVR-V2-001 | No module exists at repo root outside five canonical directories | Yes |
| AVR-V2-002 | routing_table.json contains no legacy AUDIT_SYSTEM/ references | Yes |
| AVR-V2-003 | All analog modules classified in AP_LEGACY_MODULE_MIGRATION_LOG.json | Yes |
| AVR-V2-004 | All 6 config files present at canonical paths before initialization | Yes |
| AVR-V2-005 | module_registry.json contains full V2 module inventory | Yes |
| AVR-V2-006 | No module produces stdout-only output (all outputs are structured JSON) | Yes |
| AVR-V2-007 | Header compliance: all canonical modules pass header_validator | Yes |
| AVR-V2-008 | All artifact writes route through runtime/artifact_router.py | Yes |

---

## 13. Target Repo Analysis Pipeline (AP_TOOL_PROP_01)

### Pipeline Stages

```
TA-01 ARTIFACT_COLLECTOR
  Inputs:  target repo root, audit_module_config.json
  Outputs: AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE.json, AP_EMPTY_DIRECTORIES.json

TA-02 STRUCTURE_ANALYZER
  Inputs:  TA-01 outputs
  Outputs: AP_STRUCTURE_ANALYSIS.json
  Detects: module clustering, subsystem boundaries, orphan dirs, structural anomalies

TA-03 SUBSYSTEM_ANALYZER
  Inputs:  TA-01 + TA-02 outputs
  Outputs: AP_SUBSYSTEM_ANALYSIS.json
  Detects: empty subsystem dirs, missing module groups, stub modules

TA-04 GAP_ANALYSIS_ENGINE
  Inputs:  TA-03 outputs, Design Specifications (optional)
  Outputs: AP_REPOSITORY_GAP_ANALYSIS.json
  Reports: severity-labeled gaps with remediation guidance
```

---

## 14. Governance Rules

**Non-Deletion Policy:** No module deleted without Architect authorization. Analog modules preserved at original path until migration confirmed complete.

**Canonical Directory Enforcement (FR-001 binding):** No prompt may place a module outside the three mutable canonical workflow domains. Violation rejected at GPT prompt-compilation stage before VS Code execution.

**Simulation Enforcement (FR-009 binding):** `--simulate` is the default execution mode. `--execute` requires VG-SIM to have passed in the current session. `pipeline_runner.py` enforces this at runtime.

**Artifact Routing Enforcement (FR-011 binding):** All artifact writes must route through `runtime/artifact_router.py`. Hardcoded output paths are a spec violation.

**stdout Prohibition (FR-010 binding):** All modules must produce structured JSON. Any module that writes informational output to stdout as its only output is non-compliant.

**Header Enforcement (FR-012 binding):** All canonical modules must carry a complete 13-field AP metadata header. `header_validator.py` is the enforcement mechanism. VG-HDR is a blocking gate.

**Schema Filename Resolution:** Per open risk CL-G1, `AP_DESIGN_SPEC_SCHEMA.json` and `AP_MASTER_SPEC_V2_SCHEMA.json` refer to the same artifact. All produced DS artifacts reference `AP_DESIGN_SPEC_SCHEMA.json` until the Architect resolves the canonical name.

---

## 15. Implementation Sequence

The build sequence aligns with the addendum's 7-pass implementation order mapped to the architectural stage model.

| Pass | Stage | Scope | Entry Condition | Exit Condition |
|---|---|---|---|---|
| PASS_1 | Stage0 — Foundation | Config files (6), migration log, routing_table.json rebuild, analog module migrations (22) | SPEC-010 approved by Architect | All configs present; migration log complete; no modules outside canonical domains; routing_table legacy refs == 0 |
| PASS_2 | Stage6 — Artifact Routing | runtime/artifact_router.py, runtime/output_registry.py, runtime/routing_table.py | PASS_1 complete | Artifact routing operational; test artifact routed to correct path |
| PASS_3 | Stage6 — Execution Spine | controllers/workflow_controller.py, task_router.py, execution_scheduler.py, pipeline_runner.py, runtime_context_manager.py | PASS_2 complete; SPEC-004 approved | Pipeline runner executes single no-op stage without error |
| PASS_4 | Stage2 — Dependency Graph | analysis/dependency_graph_builder.py, cycle_detector.py, execution_order_planner.py | PASS_3 complete | dependency_graph.json + execution_order.json produced for AP repo self-analysis |
| PASS_5 | Stage3 — Simulation | simulation/runtime_simulator.py, import_surface_simulator.py, integration_simulator.py, mutation_simulator.py | PASS_4 complete | simulation_report.status == "PASS" on AP repo |
| PASS_6 | Stage5 — Repair | repair/repair_engine.py, patch_generator.py, schema_repair.py, dependency_rewriter.py, module_normalizer.py | PASS_5 complete | Seeded error repaired; quarantine triggered on max-attempt failure |
| PASS_7 | Stage0+Stage1 — Validation + Audit | validation/header_validator.py, M-VAL-01; all M10–M17 modules | PASS_6 complete; SPEC-004 approved | Architecture validation passes; all S1 artifacts produced; header_validator produces compliance report |
| PASS_8 | Stage4 — Crawl Engine | M38–M39, M50–M65, M80, checklist_evaluator | PASS_7 complete; VG-SIM passed | Single-module crawl pass succeeds end-to-end in --simulate mode |
| PASS_9 | Stage6 — Reporting | M93–M94; M91 output_registry wired | PASS_8 complete | Full pipeline run in --simulate mode produces all 5 post-crawl artifacts |
| PASS_10 | Stage2 full | M11–M17 missing builds; M20–M25 | PASS_9 complete | All Stage1 + Stage2 module outputs valid |
| PASS_11 | Target Analysis | TA-01 through TA-04 | PASS_10 complete | Gap analysis report produced for AP repo self-analysis |
| PASS_12 | LOGOS Integration | All modules; LOGOS present | PASS_11 complete | Simulation PASS on LOGOS snapshot; full crawl plan produced |

---

## 16. Deferments

| Item | Rationale | Status |
|---|---|---|
| LOGOS live crawl | Requires PASS_11 complete + LOGOS available in targets/ | Post PASS_11 |
| LOGOS DS/IG V2 schema upgrade | Separate workstream | Deferred |
| SPEC-011 for AP_TOOL_PROP_01 | Boundary formalization; TA-01–TA-04 scoped here pending decision | Pending Architect |
| CI/CD GitHub Actions integration | Infrastructure concern | Deferred |
| DRAC implementation | Architect standing deferment | Until canonical runtime exists |

---

## 17. Open Questions

| ID | Question | Blocking |
|---|---|---|
| OQ-001 | Resolve CL-G1: canonical schema filename | Yes — blocks DS schema validation |
| OQ-002 | SPEC-004 approval | Yes — blocks PASS_3 and PASS_7 |
| OQ-003 | SPEC-011 for AP_TOOL_PROP_01 subsystem | No |

---

## 18. Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| v1 | 2026-03-10 | Initial specification | Claude / Formalization_Expert |
| v2 | 2026-03-10 | Addendum integration: execution spine (controllers/), artifact routing (runtime/), repair subsystem (repair/), simulation framework (4 modules), dependency graph engine (analysis/), header enforcement, 7-stage pipeline, declared divergences | Claude / Formalization_Expert |

---

*End of AP_V2_Tooling_DS*

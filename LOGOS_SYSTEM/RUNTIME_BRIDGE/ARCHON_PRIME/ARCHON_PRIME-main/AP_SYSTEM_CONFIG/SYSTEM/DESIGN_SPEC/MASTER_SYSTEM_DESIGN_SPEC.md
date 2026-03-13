SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Design_Specification
ARTIFACT_NAME: MASTER_SYSTEM_DESIGN_SPEC
VERSION: 1.0.0
DATE: 2026-03-08
AUTHORITY: Architect
SUBSYSTEM: Design_Specification

---------------------------------------------------------------------

# ARCHON_PRIME — MASTER SYSTEM DESIGN SPECIFICATION
**Version:** 1.0.0 | **Date:** 2026-03-08 | **Status:** AUTHORITATIVE — DO NOT MODIFY WITHOUT ARCHITECT APPROVAL

---

## DELIVERABLE 1 — MASTER SYSTEM DESIGN SPEC

### A. System Purpose

ARCHON_PRIME is a deterministic, single-pass crawl-mutation-validation engine for the LOGOS repository.  
Its job is to walk the LOGOS module graph exactly once, apply all required canonical mutations in that pass, validate each module before advancing, and produce a complete, auditable artifact trail.

The system exists to eliminate the class of technical debt where:
- headers are missing, non-canonical, or inconsistent
- imports bypass the Canonical Import Facade
- governance contracts are absent or mismatched
- runtime phase assignments are incorrect or missing
- audit artifacts are stale or absent

The end state of a successful ARCHON_PRIME run is a LOGOS repo in which every module has been touched once, every mutation has been validated, every artifact is routed to its canonical home, and the commit record is clean.

---

### B. Scope Boundaries

**IN SCOPE:**
- Pre-crawl audit artifact regeneration (fresh repo analysis)
- Canonical schema definitions (all data contracts)
- Repo mapping: directory trees, Python file inventory, module index
- Dependency graphing: import graph, circular dependency detection
- Runtime phase mapping: phase assignment, boot sequence validation
- Governance scanning: contract presence, contract compliance
- Header normalization: canonical schema injection, stale header replacement
- Canonical Import Facade enforcement: deep import detection and rewrite
- Crawl planning: ordered module list with dependency-respecting traversal
- Crawl execution: one-module-at-a-time mutation engine
- In-crawl monitoring: real-time status, error detection
- Repair routing and execution: classified failure remediation
- Quarantine management: isolation of unresolvable modules via stub
- Artifact routing: canonical output locations for all generated artifacts
- Simulation layer: repo, runtime, and import simulation before live mutation
- Final reporting and commit/finalize management

**OUT OF SCOPE:**
- Redesigning the LOGOS runtime architecture
- Adding new LOGOS features or protocols
- Speculative subsystems not directly required for crawl/audit/repair
- Parallel or multi-threaded module processing (one-at-a-time semantics preserved)
- Executing LOGOS modules during the crawl
- Any mutation to governance contracts themselves (contracts are inputs, not targets)

---

### C. Core Subsystems

| ID | Subsystem | Phase | Role |
|----|-----------|-------|------|
| S1 | Audit Regeneration | Pre-crawl | Generate fresh repo analysis artifacts |
| S2 | Canonical Schema Layer | Foundation | Define all data contracts as locked schemas |
| S3 | Repo Analysis Tools | Pre-crawl | Mapping, graphing, phase detection, module indexing |
| S4 | Canonical Import Registry | Foundation | Facade enforcement contract and rewrite plan |
| S5 | Header Schema + Injector | Mutation | Normalize/inject all module headers |
| S6 | Governance Scanner/Validator | Pre-crawl + In-crawl | Contract presence and compliance |
| S7 | Simulation Layer | Pre-crawl | Validate plan before live mutation |
| S8 | Crawl Planner | Pre-crawl | Produce ordered execution graph |
| S9 | Crawl Executor | In-crawl | Single-pass mutation engine |
| S10 | Monitor/Diagnosis/Repair | In-crawl | Real-time error handling and remediation |
| S11 | Quarantine/Fallback | In-crawl | Stub isolation of unresolvable modules |
| S12 | Reporting/Finalize/Commit | Post-crawl | Artifact production and clean commit |

---

### D. Data Flow

```
LOGOS Repo (current state)
    │
    ▼
[S1: Audit Regeneration]
    │  produces: repo_directory_tree.json, repo_python_files.json,
    │            repo_imports.json, repo_symbol_imports.json,
    │            header_schema_compliance.json, modules_missing_headers.json,
    │            governance_contract_map.json, missing_governance_modules.json
    ▼
[S3: Repo Analysis Tools]
    │  produces: module_index.json, dependency_graph.json,
    │            circular_dependency_groups.json, runtime_phase_map.json,
    │            runtime_boot_sequence.json, canonical_import_rewrite_plan.json
    ▼
[S4+S5+S6: Registry/Schema Lock]
    │  canonical_import_registry locked
    │  header_schema locked
    │  governance contract map locked
    ▼
[S7: Simulation Layer]
    │  produces: simulation_report.json
    │  gate: simulation must PASS before crawl is permitted
    ▼
[S8: Crawl Planner]
    │  produces: crawl_plan.json (ordered module list, execution graph)
    ▼
[S9: Crawl Executor]  ←──────────────────────────────────────────────────────┐
    │  for each module:                                                        │
    │    1. load module                                                        │
    │    2. validate syntax                                                    │
    │    3. inject/replace header                                              │
    │    4. rewrite deep imports                                               │
    │    5. validate governance contract                                       │
    │    6. validate runtime phase assignment                                  │
    │    7. post-mutation syntax revalidation                                  │
    │    8. if PASS → log → route artifacts → advance                         │
    │    9. if FAIL → [S10: Repair Loop]                                       │
    ▼                    │                                                     │
[S10: Repair Loop]       │ repair succeeds → back to validation ──────────────┘
    │  if repair fails after threshold → [S11: Quarantine]
    ▼
[S11: Quarantine]
    │  stub module, update quarantine_registry.json, log, advance
    ▼
[S12: Reporting + Commit]
    │  produces: validation_report.json, repair_event_log.json,
    │            mutation_log.json, crawl_execution_log.json,
    │            crawl_status.json, simulation_report.json
    │  commits clean state
```

---

### E. Control Flow

**Pre-crawl phase (must complete fully before crawl begins):**
1. Run all audit regeneration scripts → validate outputs against schemas
2. Run all analysis tools → build module index, dependency graph, phase map
3. Run governance scanner → produce governance_contract_map.json
4. Lock: header schema, canonical import registry, repair registry, routing table
5. Run simulation layer → simulation_report.json must show PASS
6. Run crawl planner → produce ordered execution graph
7. Evaluate pre-crawl checklist (see D6) — all items must be GREEN

**In-crawl phase (deterministic, one-module-at-a-time):**
- Load next module from execution graph
- Execute processing pipeline (syntax → header → import → governance → phase → revalidate)
- On PASS: route artifacts, log, mark module complete, advance
- On FAIL: invoke repair router, execute repair, revalidate
  - If repair PASS: route artifacts, log, advance
  - If repair FAIL after threshold: quarantine, stub, log, advance
- Update crawl_status.json after every module
- If any HALT-class failure: stop crawl, emit diagnostic, await manual resolution

**Post-crawl phase:**
- Generate all reports
- Confirm all artifacts are at canonical locations
- Confirm quarantine registry is complete
- Run final validation sweep
- Produce clean commit

---

### F. Governance Integration

- `governance_contract_map.json` is loaded before crawl begins and treated as read-only during crawl
- Every module's governance contract is checked during the processing pipeline
- Violations are classified per the failure taxonomy (D7)
- Canonical Import Facade is mandatory; deep imports are BLOCKING violations
- Governance headers are mandatory; missing headers are AUTO-INJECTED (not optional)
- Header schema is locked before crawl — no in-crawl schema changes permitted
- Module phase assignments must match `runtime_phase_map.json`
- Boot chain modules (phase 0/1) are subject to STRICTER validation — any failure halts crawl

---

### G. Failure Model

**Three failure severities:**
1. `BLOCKING` — crawl halts on current module; repair attempted; if repair fails → quarantine
2. `HALT` — crawl stops entirely; manual resolution required before resuming
3. `WARNING` — logged, flagged in report; crawl continues

**Fail-closed posture:**
- Any ambiguity (unknown module, unregistered import, unparseable governance contract) = BLOCKING minimum
- Unknown failure class = HALT
- Repair registry miss = BLOCKING → quarantine

**State preservation:**
- `crawl_status.json` is updated after every module
- A crashed crawl can be resumed from last confirmed-PASS module
- No module is marked complete until both mutation AND post-mutation validation pass

---

### H. Repair Model

- Repair is **automated only** for failure classes in the repair registry
- Every repair attempt is logged in `repair_event_log.json`
- Repair is validated (same pipeline as original validation) before advancing
- Maximum 1 retry per module per failure class (configurable in repair registry)
- If repair validation fails: module goes to quarantine
- Repair never modifies the crawl plan — it only modifies the target module

---

### I. Quarantine Model

- Quarantine is the **last resort**, not a shortcut
- A quarantined module is replaced by a governance-compliant stub:
  ```python
  # QUARANTINE STUB — generated by ARCHON_PRIME crawl
  # Original: <original_path>
  # Failure class: <failure_class>
  # Quarantine timestamp: <ISO8601>
  # Manual resolution required
  raise NotImplementedError("Module quarantined by ARCHON_PRIME — see quarantine_registry.json")
  ```
- `quarantine_registry.json` is updated with: original path, failure class, repair attempts, timestamp
- Quarantine does **not** stop the crawl — it logs and advances
- Post-crawl report MUST surface all quarantined modules prominently
- Dependent modules that import a quarantined module receive a WARNING (not a BLOCKING); the import is rewritten to the stub path

---

### J. Logging / Routing Model

- All log files route to canonical locations defined in the routing table (D8)
- Every event (mutation, validation, repair, quarantine, routing) is logged
- Logs are append-only during crawl; no log rotation during a crawl run
- Log format is structured JSON for machine readability; human-readable summary appended at end
- `crawl_status.json` is the real-time progress indicator (updated in-place after every module)
- All other logs are append-only event streams

---

### K. Success Criteria

| Criterion | Verification |
|-----------|-------------|
| Every target module touched exactly once | crawl_execution_log.json: unique module list |
| All mutations applied and validated | mutation_log.json + validation_report.json |
| Zero silent skips | crawl_status.json: no module in SKIPPED state |
| All artifacts at canonical locations | routing table verification pass |
| Quarantine registry complete and accurate | quarantine_registry.json schema check |
| Post-crawl report generated | report_generator.py exit code 0 |
| Clean commit produced | commit_finalizer.py exit code 0 |
| Simulation passed | simulation_report.json: PASS |
| Pre-crawl checklist all GREEN | checklist outputs |

---

### L. Explicit Non-Goals

1. Multi-pass crawl behavior
2. Runtime execution of mutated modules during crawl
3. Concurrent/parallel module processing
4. Redesigning LOGOS runtime, governance, or protocol contracts
5. Speculative module additions beyond what clean one-pass crawl requires
6. Scratchpad or temp artifact accumulation (all artifacts canonical or discarded)
7. Interactive repair (repair is automated or quarantined; no pausing for human input mid-crawl)
8. Cross-repo crawl (LOGOS only)

---

## DELIVERABLE 2 — CANONICAL DIRECTORY OWNERSHIP MAP

### ARCHON_PRIME/ — Crawl Engine Root

| Directory | Purpose | File Types | Example Artifacts | Source/Generated/Mixed | Mutable During Crawl |
|-----------|---------|-----------|-------------------|----------------------|-------------------|
| `tools/repo_mapping/` | Repo structure analysis tooling | `.py` | `repo_directory_scanner.py`, `module_index_builder.py` | Source | NO |
| `tools/import_analysis/` | Import graph and facade tooling | `.py` | `import_extractor.py`, `dependency_graph_builder.py`, `circular_dependency_detector.py`, `canonical_import_registry_builder.py` | Source | NO |
| `tools/governance_analysis/` | Governance contract validation | `.py` | `governance_contract_scanner.py`, `governance_validator.py` | Source | NO |
| `tools/runtime_analysis/` | Runtime phase + boot chain analysis | `.py` | `runtime_phase_mapper.py`, `runtime_boot_sequencer.py` | Source | NO |
| `tools/normalization_tools/` | Schema registry, normalization helpers | `.py`, `.json` | `schema_registry.py`, `header_schema.json` | Source | NO |
| `tools/audit_tools/` | Audit support: repair registry loader, routing table loader | `.py`, `.json` | `repair_registry_loader.py`, `repair_registry.json` | Source | NO |
| `crawler/engine/` | Core crawl planner and executor | `.py` | `crawl_planner.py`, `crawl_executor.py` | Source | NO |
| `crawler/pipeline/` | Per-module processing pipeline steps | `.py` | `module_processor.py`, `syntax_validator.py`, `governance_validator.py` | Source | NO |
| `crawler/mutation/` | Mutation operators: header injector, import rewriter | `.py` | `header_injector.py`, `import_rewriter.py` | Source | NO |
| `crawler/repair/` | Error classification and repair routing/execution | `.py` | `error_classifier.py`, `repair_router.py`, `repair_executor.py` | Source | NO |
| `crawler/monitor/` | Real-time crawl monitoring | `.py` | `crawl_monitor.py` | Source | NO |
| `crawler/quarantine/` | Quarantine stub generation and registry management | `.py` | `quarantine_manager.py` | Source | NO |
| `crawler/commit/` | Artifact routing, report generation, finalize/commit | `.py` | `artifact_router.py`, `report_generator.py`, `commit_finalizer.py` | Source | NO |
| `orchestration/controllers/` | Top-level controller entry point | `.py` | `controller_main.py` | Source | NO |
| `orchestration/execution_graphs/` | Generated execution graph artifacts | `.json` | `crawl_plan.json`, `execution_graph.json` | Generated | Only by planner |
| `orchestration/task_router/` | Task routing logic and config loader | `.py` | `task_router.py`, `routing_table_loader.py` | Source | NO |
| `orchestration/json_drivers/` | JSON schema definitions for all artifacts | `.json` | All schema files from D4 | Source | NO |
| `simulation/repo_simulator/` | Repo state simulation | `.py` | `repo_simulator.py` | Source | NO |
| `simulation/runtime_simulator/` | Runtime boot sequence simulation | `.py` | `runtime_simulator.py` | Source | NO |
| `simulation/import_simulator/` | Import resolution simulation | `.py` | `import_simulator.py` | Source | NO |
| `configs/crawl_configs/` | Crawl configuration files | `.json`, `.yaml` | `crawl_config.json` | Source | NO |
| `configs/audit_configs/` | Audit configuration and pre-crawl checklist | `.json`, `.md` | `audit_config.json`, `PRE_CRAWL_CHECKLIST.md` | Source | NO |
| `configs/repair_registry/` | Repair policy registry | `.json` | `repair_registry.json`, `FAILURE_TAXONOMY.md` | Source | NO |
| `configs/phase_maps/` | Phase map config and implementation sequence | `.json`, `.md` | `phase_map_config.json`, `IMPLEMENTATION_SEQUENCE.md` | Source | NO |
| `logs/crawler_logs/` | Real-time crawl event logs | `.json`, `.log` | `crawl_execution_log.json`, `crawl_status.json` | Generated | YES (append-only) |
| `logs/repair_logs/` | Repair event logs | `.json` | `repair_event_log.json`, `quarantine_registry.json` | Generated | YES (append-only) |
| `logs/execution_logs/` | Mutation and validation logs | `.json` | `mutation_log.json`, `validation_report.json` | Generated | YES (append-only) |
| `logs/simulation_logs/` | Simulation outputs | `.json` | `simulation_report.json` | Generated | NO (pre-crawl only) |
| `sources/repo_snapshots/` | Pre-crawl repo state snapshot | `.json` | `pre_crawl_snapshot.json` | Generated (pre-crawl) | NO |
| `sources/blueprints/` | Canonical design blueprints | `.md`, `.json` | This file, schema definitions | Source | NO |
| `sources/governance_artifacts/` | Governance contract artifacts | `.json` | `governance_contract_map.json`, `missing_governance_modules.json` | Generated (pre-crawl) | NO |
| `sources/baseline_analysis/` | Baseline audit artifacts | `.json` | All pre-crawl audit JSONs | Generated (pre-crawl) | NO |
| `distribution/incoming_bundle/` | Raw incoming artifacts for processing | `.json`, `.py` | Unprocessed source bundles | Mixed | YES (during intake) |
| `distribution/sorted_artifacts/` | Post-processed, sorted artifacts | `.json` | Sorted and routed outputs | Generated | YES (during routing) |

---

### AUDIT_SYSTEM/ — Audit Engine Root

| Directory | Purpose | File Types | Example Artifacts | Source/Generated/Mixed | Mutable During Crawl |
|-----------|---------|-----------|-------------------|----------------------|-------------------|
| `scripts/repo_scanners/` | Scan repo structure, collect Python files | `.py` | `repo_directory_scanner.py`, `python_file_collector.py`, `concept_spec_gap_detector.py` | Source | NO |
| `scripts/dependency_scanners/` | Analyze module dependencies | `.py` | `dependency_graph_builder.py` (caller) | Source | NO |
| `scripts/import_scanners/` | Scan raw and symbol-level imports | `.py` | `import_extractor.py`, `symbol_import_extractor.py` | Source | NO |
| `scripts/governance_scanners/` | Scan governance contract presence/compliance | `.py` | `governance_contract_scanner.py` | Source | NO |
| `scripts/runtime_scanners/` | Scan runtime phase assignments | `.py` | `runtime_phase_scanner.py` | Source | NO |
| `scripts/header_scanners/` | Scan header presence and schema compliance | `.py` | `header_schema_scanner.py` | Source | NO |
| `reports/structural_reports/` | Repo structure reports | `.json`, `.md` | `repo_directory_tree.json`, `module_index.json` | Generated | NO |
| `reports/import_reports/` | Import analysis reports | `.json` | `repo_imports.json`, `dependency_graph.json`, `circular_dependency_groups.json` | Generated | NO |
| `reports/runtime_reports/` | Runtime phase and boot sequence reports | `.json` | `runtime_phase_map.json`, `runtime_boot_sequence.json` | Generated | NO |
| `reports/governance_reports/` | Governance compliance reports | `.json` | `governance_contract_map.json`, `missing_governance_modules.json` | Generated | NO |
| `reports/concept_reports/` | Concept/spec gap reports | `.json` | `concept_spec_gap_report.json` | Generated | NO |
| `analysis/repo_maps/` | Repo structural maps | `.json` | `repo_python_files.json`, `repo_symbol_imports.json` | Generated | NO |
| `analysis/dependency_graphs/` | Dependency graph artifacts | `.json` | `dependency_graph.json`, `canonical_import_rewrite_plan.json` | Generated | NO |
| `analysis/runtime_maps/` | Runtime analysis artifacts | `.json` | `runtime_phase_map.json` | Generated | NO |
| `analysis/protocol_maps/` | Protocol-level maps | `.json` | `protocol_map.json` | Generated | NO |
| `diagnostics/error_catalogs/` | Known error catalogs | `.json` | `error_catalog.json` | Mixed | NO |
| `diagnostics/repair_recommendations/` | Repair recommendation outputs | `.json` | `repair_recommendations.json` | Generated | NO |
| `diagnostics/violation_logs/` | Detected violation records | `.json` | `violation_log.json` | Generated | YES (append-only) |
| `baselines/initial_repo_snapshot/` | Untouched pre-crawl baseline | `.json` | `initial_snapshot.json` | Generated (once) | NO |
| `baselines/post_normalization_snapshot/` | Post-crawl state snapshot | `.json` | `post_normalization_snapshot.json` | Generated (post-crawl) | NO |
| `runtime_monitor/live_status/` | Real-time crawl status mirrors | `.json` | `crawl_status_mirror.json` | Generated | YES |
| `runtime_monitor/progress_tracking/` | Progress tracking artifacts | `.json` | `progress_tracker.json` | Generated | YES |

---

## DELIVERABLE 9 — IMPLEMENTATION READINESS JUDGMENT

### What Is Already Sufficiently Defined

- Directory structure (ARCHON_PRIME + AUDIT_SYSTEM): COMPLETE
- System purpose and scope boundaries: COMPLETE (this document)
- Core subsystem decomposition: COMPLETE
- Data flow and control flow: COMPLETE
- Failure model, repair model, quarantine model: COMPLETE
- Governance integration contract: COMPLETE
- Logging and routing model: COMPLETE
- Success criteria: COMPLETE
- Non-goals: COMPLETE
- Directory ownership map: COMPLETE
- Implementation sequence: COMPLETE (see IMPLEMENTATION_SEQUENCE.md)
- Failure taxonomy: COMPLETE (see FAILURE_TAXONOMY.md)
- Output routing table: COMPLETE (see OUTPUT_ROUTING_TABLE.md)
- Artifact schema set: COMPLETE (see ARTIFACT_SCHEMAS.md)
- Module inventory: COMPLETE (see MODULE_INVENTORY.md)
- Pre-crawl checklist: COMPLETE (see PRE_CRAWL_CHECKLIST.md)

### What Is Still Missing (Minimal Blocking Inputs)

| Missing Item | Impact | Resolution Path |
|-------------|--------|----------------|
| LOGOS repo actual Python file list | Needed by `module_index_builder.py` | Run `python_file_collector.py` as first execution step |
| Actual governance contract schema format | Needed by `governance_contract_scanner.py` | Extract from existing LOGOS governance modules before scanner is built |
| Canonical Import Facade registry (actual entries) | Needed by `canonical_import_registry_builder.py` | Extract from existing LOGOS facade modules before crawl begins |
| Header schema field definitions | Needed by `header_injector.py` | Define from LOGOS governance header conventions before Stage 5 |
| Runtime phase assignment convention | Needed by `runtime_phase_mapper.py` | Extract from LOGOS runtime initialization before Stage 3 |

**None of these blockers prevent implementation from starting.** They are discovered inputs, not design gaps. Stages 0–2 can begin immediately. Each missing input is collected by the pre-crawl audit tools themselves.

### Can Implementation Begin Immediately?

**YES.** Implementation can begin at Stage 0 (foundation schemas + config layer) immediately after this package is accepted. The five missing inputs above are all produced by the Stage 1 audit tools — meaning by the time Stage 3 needs them, they exist.

### Recommended First Action

1. Accept and freeze this design package
2. Begin Stage 0: define all JSON schemas and config files
3. Begin Stage 1: implement audit regeneration scripts
4. First crawl is permitted only after pre-crawl checklist is fully GREEN

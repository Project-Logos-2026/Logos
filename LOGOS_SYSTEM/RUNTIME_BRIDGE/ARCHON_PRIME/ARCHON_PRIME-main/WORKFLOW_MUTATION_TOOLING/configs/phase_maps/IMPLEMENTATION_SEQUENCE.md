# ARCHON_PRIME — SEQUENTIAL IMPLEMENTATION PLAN
**Deliverable 5** | Version 1.0.0 | 2026-03-08 | AUTHORITATIVE

---

## SEQUENCING PRINCIPLES

1. **No implicit wiring.** Every module that is built assumes its dependencies are already built and frozen.
2. **Freeze before downstream.** Once a stage completes its validation gate, its outputs are treated as read-only inputs for all subsequent stages.
3. **Foundation before tools.** Schema and config infrastructure is built before any tool that produces or consumes structured artifacts.
4. **Audit before crawl.** No crawl begins until the full pre-crawl audit package is produced and validates.
5. **Simulation before live run.** The simulation layer must pass before the executor touches any real file.

---

## STAGE 0 — FOUNDATION: SCHEMAS + CONFIG LAYER

### Objective
Establish all data contracts, routing config, and repair policy before any functional module is written.
Nothing is "defined later." Every interface is pinned at this stage.

### Files / Modules Built
| File | Location |
|------|----------|
| `ARTIFACT_SCHEMAS.md` (this package) | `ARCHON_PRIME/orchestration/json_drivers/` |
| `routing_table.json` | `ARCHON_PRIME/configs/crawl_configs/` |
| `repair_registry.json` | `ARCHON_PRIME/configs/repair_registry/` |
| `header_schema.json` | `ARCHON_PRIME/tools/normalization_tools/` |
| `canonical_import_registry.json` (seed) | `ARCHON_PRIME/tools/normalization_tools/` |
| `crawl_config.json` | `ARCHON_PRIME/configs/crawl_configs/` |
| `schema_registry.py` (M00) | `ARCHON_PRIME/tools/normalization_tools/` |
| `routing_table_loader.py` (M01) | `ARCHON_PRIME/orchestration/task_router/` |
| `repair_registry_loader.py` (M02) | `ARCHON_PRIME/tools/audit_tools/` |

### Prerequisites
None. This is the absolute first stage.

### Validation Gate
- [ ] All JSON schema files are syntactically valid JSON
- [ ] `schema_registry.py` can load and validate a sample artifact against each schema
- [ ] `routing_table.json` has an entry for every artifact type defined in D4
- [ ] `repair_registry.json` has an entry for every failure class defined in D7
- [ ] `header_schema.json` has all required fields declared with types
- [ ] `crawl_config.json` is valid and loadable

### Frozen After Completion
- All 21 artifact schemas
- Routing table (every artifact type → canonical path)
- Repair registry (every failure class → remediation)
- Header schema (all fields + types)
- Crawl config structure

**DO NOT MODIFY these after Stage 0 completes without architect approval and full stage re-validation.**

---

## STAGE 1 — PRE-CRAWL AUDIT REGENERATION SCRIPTS

### Objective
Implement all audit scripts that generate fresh repo analysis artifacts from the live LOGOS repo state.
These scripts produce the raw inputs that all analysis tools (Stage 2) consume.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `repo_directory_scanner.py` (M10) | `AUDIT_SYSTEM/scripts/repo_scanners/` |
| `python_file_collector.py` (M11) | `AUDIT_SYSTEM/scripts/repo_scanners/` |
| `import_extractor.py` (M12) | `AUDIT_SYSTEM/scripts/import_scanners/` |
| `symbol_import_extractor.py` (M13) | `AUDIT_SYSTEM/scripts/import_scanners/` |
| `header_schema_scanner.py` (M14) | `AUDIT_SYSTEM/scripts/header_scanners/` |
| `governance_contract_scanner.py` (M15) | `AUDIT_SYSTEM/scripts/governance_scanners/` |
| `runtime_phase_scanner.py` (M16) | `AUDIT_SYSTEM/scripts/runtime_scanners/` |

### Prerequisites
Stage 0 complete:
- `schema_registry.py` available
- `routing_table_loader.py` available
- All target schemas defined (`repo_directory_tree.json` through `modules_missing_headers.json`)

### Validation Gate
- [ ] All 7 scripts run against LOGOS repo root without exception
- [ ] All outputs validate against their defined schemas (M00 validates)
- [ ] `repo_python_files.json` total count > 0
- [ ] `repo_imports.json` total import statement count > 0
- [ ] `header_schema_compliance.json` produced with modules scanned > 0
- [ ] `governance_contract_map.json` produced with compliant + non-compliant counts > 0
- [ ] No artifact left in a temp location — all routed per routing table

### Frozen After Completion
- Output artifact formats (schemas already frozen at Stage 0)
- Audit script interfaces (inputs/outputs/routing)
- The audited baseline (regenerate only if LOGOS repo changes before crawl begins)

---

## STAGE 2 — REPO ANALYSIS TOOLS

### Objective
Build graph, phase, module index, and canonical import registry from the Stage 1 audit artifacts.
This is the analytical layer that transforms raw audit data into structured knowledge the crawl engine uses.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `module_index_builder.py` (M20) | `ARCHON_PRIME/tools/repo_mapping/` |
| `dependency_graph_builder.py` (M21) | `ARCHON_PRIME/tools/import_analysis/` |
| `circular_dependency_detector.py` (M22) | `ARCHON_PRIME/tools/import_analysis/` |
| `runtime_phase_mapper.py` (M23) | `ARCHON_PRIME/tools/runtime_analysis/` |
| `runtime_boot_sequencer.py` (M24) | `ARCHON_PRIME/tools/runtime_analysis/` |
| `canonical_import_registry_builder.py` (M25) | `ARCHON_PRIME/tools/import_analysis/` |

**Also runs (optional, after M20):**
| Module | Location |
|--------|----------|
| `concept_spec_gap_detector.py` (M17) | `AUDIT_SYSTEM/scripts/repo_scanners/` |

### Prerequisites
Stage 1 artifacts fully produced and schema-validated:
- `repo_python_files.json`
- `repo_imports.json`
- `raw_phase_assignments.json`
- `governance_contract_map.json`

### Validation Gate
- [ ] `module_index.json` produced, schema-valid, total_modules > 0
- [ ] `dependency_graph.json` produced, schema-valid
- [ ] `circular_dependency_groups.json` produced — `crawl_blocked` evaluated
- [ ] **If `crawl_blocked: true` → HALT: boot-chain circulars must be manually resolved before proceeding**
- [ ] `runtime_phase_map.json` produced, all modules have a phase assignment
- [ ] `runtime_boot_sequence.json` produced, `unresolvable_boot_modules` is empty
- [ ] `canonical_import_rewrite_plan.json` produced, all rewrites have `confidence: CERTAIN | INFERRED`
- [ ] `canonical_import_registry.json` built (not just seeded) and locked

### Frozen After Completion
- `module_index.json` — the module ordering authority
- `dependency_graph.json` — the dependency authority
- `runtime_phase_map.json` — the phase authority
- `runtime_boot_sequence.json` — the boot order authority
- `canonical_import_registry.json` — the import facade authority
- `canonical_import_rewrite_plan.json` — the rewrite plan executed by M51

**These artifacts are READ-ONLY inputs for all subsequent stages.**

---

## STAGE 3 — MUTATION OPERATORS (ISOLATED)

### Objective
Implement and unit-test the two core mutation operators (`header_injector.py` and `import_rewriter.py`)
as pure functions BEFORE the crawl executor is built. Verify they produce correct output on isolated test cases.

This order matters: the crawl executor depends on these being correct. Building them first and testing them independently prevents debugging of two moving parts simultaneously during Stage 5+.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `header_injector.py` (M50) | `ARCHON_PRIME/crawler/mutation/` |
| `import_rewriter.py` (M51) | `ARCHON_PRIME/crawler/mutation/` |

### Prerequisites
Stage 0 frozen:
- `header_schema.json` available
- `canonical_import_registry.json` available (Stage 2 output)
- `canonical_import_rewrite_plan.json` available

### Validation Gate
- [ ] `header_injector.py` tested on: module with no header (inject), module with stale header (replace), module with compliant header (no-op)
- [ ] `header_injector.py` output always passes `syntax_validator.py` check
- [ ] `import_rewriter.py` tested on: module with deep imports (rewrite), module with clean imports (no-op), module with mix
- [ ] `import_rewriter.py` output always passes `syntax_validator.py` check
- [ ] Both operators are pure functions: no file I/O, no side effects, no global state

### Frozen After Completion
- Mutation operator APIs (function signatures and return types)
- Header schema field handling logic
- Import rewrite AST logic

---

## STAGE 4 — VALIDATION PIPELINE + SYNTAX TOOLS

### Objective
Implement all validators used in the per-module processing pipeline.
These must be independently testable before being wired into the pipeline.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `syntax_validator.py` (M62) | `ARCHON_PRIME/crawler/pipeline/` |
| `governance_validator.py` (M63) | `ARCHON_PRIME/crawler/pipeline/` |
| `phase_validator.py` (M64) | `ARCHON_PRIME/crawler/pipeline/` |

### Prerequisites
- Stage 0: schemas available
- Stage 2: `governance_contract_map.json`, `runtime_phase_map.json` available

### Validation Gate
- [ ] `syntax_validator.py` correctly rejects syntactically invalid Python
- [ ] `syntax_validator.py` correctly passes syntactically valid Python
- [ ] `governance_validator.py` correctly detects missing and mismatched contracts
- [ ] `phase_validator.py` correctly detects phase mismatches
- [ ] All validators return structured `ValidationResult` per schema

### Frozen After Completion
- Validator APIs and return types
- ValidationResult schema

---

## STAGE 5 — SIMULATION LAYER

### Objective
Implement and run the three simulation modules against Stage 2 artifacts and Stage 3 mutation operators
to verify that the full crawl plan (when executed) will produce a valid repo state.

The simulation must PASS before the crawl executor (Stage 6) is run against real files.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `repo_simulator.py` (M30) | `ARCHON_PRIME/simulation/repo_simulator/` |
| `runtime_simulator.py` (M31) | `ARCHON_PRIME/simulation/runtime_simulator/` |
| `import_simulator.py` (M32) | `ARCHON_PRIME/simulation/import_simulator/` |

**Also built here (needed by simulation):**
| Module | Location |
|--------|----------|
| `crawl_planner.py` (M38) — draft | `ARCHON_PRIME/crawler/engine/` |
| `execution_graph_builder.py` (M39) — draft | `ARCHON_PRIME/orchestration/execution_graphs/` |

Rationale: Simulators need a crawl plan to simulate against. Plan is draft at this stage — frozen after simulation passes.

### Prerequisites
- Stage 2 artifacts: `module_index.json`, `dependency_graph.json`, `runtime_phase_map.json`, `runtime_boot_sequence.json`, `canonical_import_rewrite_plan.json`
- Stage 3: `header_injector.py`, `import_rewriter.py`

### Validation Gate
- [ ] `simulation_report.json` produced
- [ ] `simulation_report.json` → `overall_result: "PASS"`
- [ ] `simulation_report.json` → `crawl_permitted: true`
- [ ] `repo_simulation.structural_violations` is empty
- [ ] `runtime_simulation.boot_chain_violations` is empty
- [ ] `import_simulation.broken_after_rewrite` is empty
- [ ] Crawl plan (`crawl_plan.json`) produced and valid

### Frozen After Completion
- Crawl plan module ordering (`crawl_plan.json`)
- Execution graph (`execution_graph.json`)
- Simulation results (pre-crawl evidence package)

---

## STAGE 6 — CRAWL EXECUTOR + PROCESSING PIPELINE

### Objective
Implement the full per-module processing pipeline (`module_processor.py`) and the crawl executor loop
(`crawl_executor.py`). Wire all mutation operators and validators from Stages 3 and 4 into the pipeline.

At this stage, **no repair or quarantine logic yet** — the executor should halt cleanly on any failure, log it,
and stop. Repair and quarantine are added in Stage 7.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `module_processor.py` (M61) | `ARCHON_PRIME/crawler/pipeline/` |
| `crawl_executor.py` (M60) | `ARCHON_PRIME/crawler/engine/` |
| `crawl_monitor.py` (M65) | `ARCHON_PRIME/crawler/monitor/` |

### Prerequisites
- Stage 3: mutation operators
- Stage 4: validators
- Stage 5: `execution_graph.json`, `crawl_plan.json`

### Validation Gate
- [ ] Executor runs on a CLEAN test module set (no mutations needed) → PASS
- [ ] Executor runs on a test module with a missing header → stops on FAIL (before repair logic)
- [ ] Executor runs on a test module with a deep import → stops on FAIL
- [ ] `crawl_status.json` updated correctly after each module
- [ ] `crawl_execution_log.json` entries produced for each processed module
- [ ] `mutation_log.json` entries produced for each mutation applied

### Frozen After Completion
- Processing pipeline API
- Crawl executor loop semantics
- Log entry formats

---

## STAGE 7 — ERROR CLASSIFICATION + REPAIR + QUARANTINE

### Objective
Implement the error classifier, repair router, repair executor, and quarantine manager.
Wire them into the crawl executor so the system can handle failures without halting unnecessarily.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `error_classifier.py` (M70) | `ARCHON_PRIME/crawler/repair/` |
| `repair_router.py` (M71) | `ARCHON_PRIME/crawler/repair/` |
| `repair_executor.py` (M72) | `ARCHON_PRIME/crawler/repair/` |
| `quarantine_manager.py` (M80) | `ARCHON_PRIME/crawler/quarantine/` |

### Prerequisites
- Stage 0: `repair_registry.json` loaded (M02)
- Stage 6: `crawl_executor.py`, `module_processor.py`
- Stage 3: mutation operators (repair executor reuses them)

### Validation Gate
- [ ] Every failure class in the taxonomy (D7) maps to a repair action in the registry
- [ ] `error_classifier.py` correctly classifies a sample of each failure class
- [ ] `repair_router.py` correctly routes BLOCKING → repair, HALT → halt signal
- [ ] `repair_executor.py` successfully repairs a HEADER_MISSING failure on a test module
- [ ] `repair_executor.py` successfully repairs a DEEP_IMPORT_VIOLATION on a test module
- [ ] After max retries: `quarantine_manager.py` produces valid stub and updates `quarantine_registry.json`
- [ ] `repair_event_log.json` entries are produced for all repair attempts
- [ ] Quarantine stub passes `syntax_validator.py`

### Frozen After Completion
- Repair/quarantine logic
- All failure class handling
- Retry policy enforcement

---

## STAGE 8 — ARTIFACT ROUTING + REPORTING + COMMIT

### Objective
Implement the post-crawl artifact routing, report generation, and commit finalization.
Verify that when the crawl completes, all artifacts land at canonical locations and the commit is clean.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `artifact_router.py` (M90) | `ARCHON_PRIME/crawler/commit/` |
| `report_generator.py` (M91) | `ARCHON_PRIME/crawler/commit/` |
| `commit_finalizer.py` (M92) | `ARCHON_PRIME/crawler/commit/` |

### Prerequisites
All prior stages complete. All log artifacts being produced by executor.

### Validation Gate
- [ ] `artifact_router.py` routes every artifact type to its canonical location per routing table
- [ ] `artifact_router.py` fails with ARTIFACT_ROUTING_FAILURE (not silently) if destination does not exist
- [ ] `report_generator.py` produces `validation_report.json` that is schema-valid
- [ ] `report_generator.py` produces `post_crawl_summary_report.md` with quarantine section
- [ ] `commit_finalizer.py` runs routing table verification before committing
- [ ] `commit_finalizer.py` does NOT commit if any artifact is missing from canonical location
- [ ] `commit_finalizer.py` does NOT force-push or bypass pre-commit hooks

### Frozen After Completion
- Report format
- Commit prerequisites and process
- Artifact routing completeness

---

## STAGE 9 — ORCHESTRATION + CONTROLLER

### Objective
Wire everything together under a single controller entry point that enforces stage gates,
handles HALT signals, and can be invoked from a single CLI command.

### Files / Modules Built
| Module | Location |
|--------|----------|
| `task_router.py` (M95) | `ARCHON_PRIME/orchestration/task_router/` |
| `controller_main.py` (M96) | `ARCHON_PRIME/orchestration/controllers/` |

### Prerequisites
All stages 0–8 complete.

### Validation Gate
- [ ] `controller_main.py` invoked → runs full pre-crawl → simulation → crawl → post-crawl sequence
- [ ] HALT signal from any subsystem → `controller_main.py` exits non-zero with diagnostic
- [ ] Pre-crawl checklist can be evaluated by controller before crawl begins
- [ ] Resume-from-last is functional (reads `crawl_status.json` → `resume_from` field)
- [ ] Full end-to-end test on a test subset of LOGOS passes

### Frozen After Completion
- The entire ARCHON_PRIME system
- Everything is considered implementation-complete after Stage 9 validation passes

---

## STAGE DEPENDENCY GRAPH

```
Stage 0 (Foundation)
    └─► Stage 1 (Audit Scripts)
            └─► Stage 2 (Analysis Tools)
                    ├─► Stage 3 (Mutation Operators)  ──┐
                    ├─► Stage 4 (Validators)           ─┤
                    └─► Stage 5 (Simulation + Planner) ─┤
                                                        ├─► Stage 6 (Executor + Pipeline)
                                                        │       └─► Stage 7 (Repair + Quarantine)
                                                        │               └─► Stage 8 (Routing + Report + Commit)
                                                        │                       └─► Stage 9 (Controller)
                                                        └──────────────────────────────────────────────────────►
```

Stages 3 and 4 can be built in parallel once Stage 2 is complete.
Stage 5 requires both Stages 3 and 4 to be complete.

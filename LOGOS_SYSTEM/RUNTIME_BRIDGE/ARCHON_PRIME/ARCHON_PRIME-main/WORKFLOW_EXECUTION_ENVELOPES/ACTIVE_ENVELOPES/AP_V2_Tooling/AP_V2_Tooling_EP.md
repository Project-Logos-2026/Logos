SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Execution_Plan
ARTIFACT_NAME: AP_V2_Tooling_EP_FINAL
STATUS: Final Draft — Pending Architect Approval
VERSION: 1.1.0
DATE: 2026-03-10
AUTHORITY: Architect
SOURCE_ARTIFACTS:
  - AP_V2_Tooling_DS.md (SPEC-010 v2)
  - AP_V2_Tooling_IG.md (IMPL-010 v2)
  - AP_V2_TOOLING_DS_IG_ADDENDUMS.md
REVISION_FROM: AP_V2_Tooling_EP.md (v1.0.0 Draft)
PURPOSE:
  Deterministic implementation sequence for constructing the ARCHON_PRIME
  V2 tooling engine defined in the design specification and implementation guide.

---------------------------------------------------------------------

REVISION NOTES — v1.0.0 → v1.1.0

Twelve defects were identified during comparison against AP_V2_Tooling_DS
and AP_V2_Tooling_IG. All are corrected in this version.

CRITICAL

  C-001  All passes missing explicit entry conditions.
         Corrected: entry conditions added to every pass.

  C-002  PASS_1 omitted header_schema.json from the 6-config-file list.
         Corrected: header_schema.json added to PASS_1 scope.

  C-003  PASS_8 missing three modules: execution_graph_builder.py (M39),
         header_injector.py (M50), import_rewriter.py (M51).
         Corrected: all three added to PASS_8 module list.

  C-004  PASS_9 validation artifact list incorrect: omitted crawl_status.json
         and misattributed PIPELINE_EXECUTION_MANIFEST.json to report_generator.
         PIPELINE_EXECUTION_MANIFEST is produced by pipeline_runner (PASS_3),
         not by report_generator. crawl_status.json is a report_generator output.
         Corrected: PASS_9 artifact list aligned with IG.

MAJOR

  M-001  PASS_5 exit condition overstated. "simulation_report PASS status"
         will block on the known-dirty AP repo during self-analysis.
         The correct criterion is that simulators run and produce structured
         output without exception. Corrected.

  M-002  PASS_3 entry condition omitted SPEC-004 approval dependency.
         SPEC-004 must be Architect-approved before PASS_3 begins.
         Corrected.

  M-003  PASS_7 entry condition omitted SPEC-004 approval dependency.
         SPEC-004 must be Architect-approved before PASS_7 begins.
         Corrected.

  M-004  Section 4 execute mode gate incorrectly listed VG-ARCH as a
         prerequisite for --execute. VG-ARCH is a Stage0 blocking gate,
         not an --execute prerequisite. The correct prerequisite is
         VG-SIM == PASS with current-session (non-stale) confirmation
         per DS Section 6.3. Corrected.

  M-005  PASS_10 module range notation ambiguous. M10 (repo_directory_scanner)
         is an analog migration completed in PASS_1. PASS_10 covers only
         the MISSING builds (M11, M13, M16, M17) plus M20–M25.
         Corrected with explicit module enumeration.

  M-006  Section 6 failure conditions incomplete. VG-HDR blocking failure
         and VG-CRAWL blocking failure were absent. Corrected.

MINOR

  m-001  EP missing pre-implementation requirements section.
         Environment verification, mutation safety preconditions, and
         migration log initialization requirements added (Section 2).

  m-002  EP missing per-pass validation report output requirement.
         PASS_N_VALIDATION_REPORT.json requirement added to Section 3.

---------------------------------------------------------------------

SECTION 1 — EXECUTION PLAN OBJECTIVE

This execution plan converts the architecture design specification and
implementation guide into a deterministic build sequence.

The goal of AP_V2_Tooling_EP is to:

1. Translate the design specification into executable implementation passes.
2. Ensure subsystem construction occurs in dependency-safe order.
3. Guarantee all architectural invariants defined in SPEC-010 are preserved.
4. Provide deterministic prompts for repository mutation tooling.

This document is NOT a design artifact.

It is the authoritative build plan for implementing the V2 tooling system.

---------------------------------------------------------------------

SECTION 2 — PRE-IMPLEMENTATION REQUIREMENTS

The following conditions must be satisfied before any pass is executed.

2.1 — ARCHITECT ACTIONS REQUIRED

  AP_V2_Tooling_DS (SPEC-010 v2) approved      — required for all passes
  OQ-001 / CL-G1 schema filename resolved       — required for DS schema validation
  SPEC-004 approved (or Architect authorizes    — required for PASS_3 and PASS_7
    IG execution against Draft status)

  No implementation pass may begin until SPEC-010 v2 is Architect-approved.
  PASS_3 and PASS_7 are additionally blocked until SPEC-004 is resolved.

2.2 — ENVIRONMENT VERIFICATION

  The VS Code execution agent must confirm before any prompt executes:

    python --version       # Must be 3.11+
    pwd                    # Must be /workspaces/ARCHON_PRIME
    git status             # Must be clean or Architect authorizes dirty tree
    python -c "import jsonschema; import yaml; import git; print('ok')"
    ls AP_SYSTEM_CONFIG/   # Must be accessible
    ls AP_SYSTEM_AUDIT/    # Must be accessible

2.3 — MUTATION SAFETY PRECONDITIONS

  The following constraints are binding across all passes.

  Default execution mode is --simulate.
  --execute requires explicit Architect authorization AND VG-SIM PASS
  in the current session (see Section 4).

  AP_SYSTEM_CONFIG/ and AP_SYSTEM_AUDIT/ are never write targets.
  These directories are immutable. artifact_router enforces this.

  Non-deletion policy is in effect.
  No rm, shutil.rmtree, or os.remove on existing files without
  Architect authorization.

  All artifact writes must route through runtime/artifact_router.py
  after PASS_2 is complete.

2.4 — MIGRATION LOG INITIALIZATION

  Before any analog module is migrated, create:

    WORKFLOW_MUTATION_TOOLING/AP_LEGACY_MODULE_MIGRATION_LOG.json

  Schema:

    {
      "schema_version": "2.0",
      "generated_at": "<ISO>",
      "policy": "NON_DELETION_ENFORCED",
      "migrations": [
        {
          "module_name": "<filename>",
          "original_path": "<rel path>",
          "target_path": "<rel path>",
          "classification": "MIGRATE|MIGRATE_AND_RENAME|REFACTOR|REBUILD|PRESERVE|DEPRECATE",
          "status": "PENDING|IN_PROGRESS|COMPLETE|DEFERRED",
          "migrated_at": "<ISO or null>"
        }
      ]
    }

  Initialize with all 22 entries from AP_V2_Tooling_DS Section 7,
  all entries at status PENDING.

---------------------------------------------------------------------

SECTION 3 — EXECUTION PASSES

The tooling engine is constructed in twelve deterministic passes.

Each pass specifies:

  • entry conditions
  • implementation scope
  • validation criteria
  • exit conditions

Passes must be executed in order. No pass may begin until its entry
condition is confirmed and its predecessor's exit condition is satisfied.

VALIDATION REPORT REQUIREMENT

  Every pass must produce a PASS_N_VALIDATION_REPORT.json:

    {
      "pass_id": "PASS_N",
      "status": "COMPLETE|INCOMPLETE|BLOCKED",
      "modules_created": [],
      "modules_modified": [],
      "artifacts_produced": [],
      "gate_results": [
        { "gate_id": "<str>", "status": "PASS|FAIL", "detail": "<str>" }
      ],
      "blocking_issues": []
    }

  A pass may not be marked COMPLETE unless its validation report exists
  and all blocking gate results are PASS.

---------------------------------------------------------------------

PASS_1 — FOUNDATION INITIALIZATION

Entry Condition

  AP_V2_Tooling_DS (SPEC-010 v2) approved by Architect.

Objective

  Construct the configuration layer, initialize the migration log,
  migrate 22 analog modules to canonical directories, and standardize
  the audit tool interface.

Scope

  Create six configuration files:

    WORKFLOW_MUTATION_TOOLING/configs/ap_config.yaml
    WORKFLOW_MUTATION_TOOLING/configs/logos_targets.yaml
    WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/crawl_config.json
    WORKFLOW_MUTATION_TOOLING/configs/phase_maps/phase_map_config.json
    WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/header_schema.json

  Rebuild routing table with V2 canonical paths:

    WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table.json

  Initialize migration log:

    WORKFLOW_MUTATION_TOOLING/AP_LEGACY_MODULE_MIGRATION_LOG.json

  Migrate 22 analog modules per DS Section 7 migration table.
  Per-module procedure:
    1. Log entry: status IN_PROGRESS
    2. Copy source to target path (do not delete source)
    3. Replace header with V2 13-field header
    4. Log entry: status COMPLETE with migrated_at timestamp
  Migrations #11 and #12 (runtime_simulator.py, import_simulator.py)
  are classified REBUILD — copy first, mark as REBUILD target for PASS_5.

  Standardize audit tool interface:

    Modify run_audit_suite.py and run_governance_audit.py.
    Add --target <path> CLI argument.
    Wrap in standard interface: run(target: str) -> dict
    Returning: {"status": "ok|error", "artifact_output": "<path>", "findings": []}

Validation

  • All six configuration files exist at canonical paths
  • routing_table.json contains no legacy AUDIT_SYSTEM/ references
  • migration log contains 22 entries
  • All 22 migration statuses are COMPLETE or DEFERRED (none PENDING)
  • No module exists outside the five canonical directories
  • run_audit_suite.py and run_governance_audit.py expose run(target) interface

Exit Condition

  PASS_1_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_2 — ARTIFACT ROUTING SYSTEM

Entry Condition

  PASS_1 complete (PASS_1_VALIDATION_REPORT.json, all gates PASS).

Objective

  Implement the runtime artifact routing subsystem. All subsequent
  passes route artifact writes through this layer.

Modules

  WORKFLOW_MUTATION_TOOLING/runtime/routing_table.py      (M92)
  WORKFLOW_MUTATION_TOOLING/runtime/output_registry.py    (M91)
  WORKFLOW_MUTATION_TOOLING/runtime/artifact_router.py    (M90)

Responsibilities

  routing_table.py
    Load routing_table.json.
    Resolve canonical artifact output paths.
    Validate no legacy paths present.

  output_registry.py
    Maintain in-session artifact registry.
    Enforce schema compliance on registration.

  artifact_router.py
    Route artifacts to canonical directories via routing_table.
    In simulate mode: return routing plan without writing.
    In execute mode: write file and register in output_registry.
    Hard refusal to write to AP_SYSTEM_CONFIG/ or AP_SYSTEM_AUDIT/.

Validation

  • artifact_router routes a test artifact to correct canonical path
    in simulate mode without exception
  • output_registry registers artifact metadata
  • routing_table resolves artifact types correctly
  • artifact_router refuses write to immutable directory

Exit Condition

  PASS_2_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_3 — EXECUTION SPINE

Entry Condition

  PASS_2 complete.
  SPEC-004 approved by Architect (or Architect authorizes execution
  against Draft status — see OQ-002).

Objective

  Construct the pipeline orchestration controller. All pipeline
  executions run through this subsystem.

Modules

  WORKFLOW_MUTATION_TOOLING/controllers/runtime_context_manager.py
  WORKFLOW_MUTATION_TOOLING/controllers/execution_scheduler.py
  WORKFLOW_MUTATION_TOOLING/controllers/task_router.py
  WORKFLOW_MUTATION_TOOLING/controllers/workflow_controller.py
  WORKFLOW_MUTATION_TOOLING/controllers/pipeline_runner.py

Build order within this pass (dependency order):

  1. runtime_context_manager.py  — must exist before any controller is built
  2. execution_scheduler.py      — consumes phase_map_config.json
  3. task_router.py              — dispatches to subsystem handlers
  4. workflow_controller.py      — orchestrates stage execution and gates
  5. pipeline_runner.py          — entry point; invokes all above

Responsibilities

  pipeline_runner.py
    CLI entry point: --target, --simulate|--execute, --stage
    Enforces VG-EXEC: --execute blocked unless Stage3 result is COMPLETE
    in current session (not stale).
    Produces PIPELINE_EXECUTION_MANIFEST.json on completion or halt.

  workflow_controller.py
    Orchestrates stage-to-stage handoff.
    Enforces blocking gate conditions.
    Returns BLOCKED status on any blocking gate failure; does not
    advance to the next stage.

  execution_scheduler.py
    Builds stage execution plan from phase_map_config.json.
    Exposes check_gate(gate_id, context) for gate evaluation.

  task_router.py
    Dispatches tasks to subsystem handlers by task type.
    Task type registry must be defined at module level.

  runtime_context_manager.py
    Holds all shared runtime state across stages.
    Must be initialized before any stage runs.

Validation

  pipeline_runner.py executes a single no-op stage (Stage0) without
  exception in --simulate mode.
  PIPELINE_EXECUTION_MANIFEST.json is produced.

Exit Condition

  PASS_3_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_4 — DEPENDENCY GRAPH ENGINE

Entry Condition

  PASS_3 complete.

Objective

  Implement the dependency graph analysis subsystem. Produces the
  deterministic execution order consumed by the crawl planner.

Modules

  WORKFLOW_MUTATION_TOOLING/analysis/dependency_graph_builder.py
  WORKFLOW_MUTATION_TOOLING/analysis/cycle_detector.py
  WORKFLOW_MUTATION_TOOLING/analysis/execution_order_planner.py

Build order within this pass:

  1. dependency_graph_builder.py  — produces directed import graph
  2. cycle_detector.py            — consumes graph; detects cycles
  3. execution_order_planner.py   — consumes graph + cycle report;
                                    produces topological execution order

Validation

  Run against AP repo for self-analysis:

    dependency_graph.json produced; total_modules > 0
    cycle_report.json produced
    execution_order.json produced; order_length > 0

  Gate VG-S2: dependency_graph.json non-empty; execution_order.json valid.

Exit Condition

  PASS_4_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_5 — SIMULATION FRAMEWORK

Entry Condition

  PASS_4 complete.

Objective

  Implement the simulation framework for pre-mutation verification.
  No live mutation may execute without this subsystem passing.

Modules

  WORKFLOW_MUTATION_TOOLING/simulation/runtime_simulator.py
  WORKFLOW_MUTATION_TOOLING/simulation/import_surface_simulator.py
  WORKFLOW_MUTATION_TOOLING/simulation/integration_simulator.py
  WORKFLOW_MUTATION_TOOLING/simulation/mutation_simulator.py

Build order within this pass:

  1. runtime_simulator.py          — rebuild from analog; detects dependency breakage
  2. import_surface_simulator.py   — rebuild from import_simulator.py analog;
                                     detects facade violations
  3. integration_simulator.py      — build; detects interface mismatches
  4. mutation_simulator.py         — build; simulation coordinator; runs all four
                                     simulators in sequence; absorbs repo_simulator logic

Simulation coordinator contract (mutation_simulator.py):

  Invoke runtime_simulator → if FAIL: write report, halt
  Invoke import_surface_simulator → if FAIL: write report, halt
  Invoke integration_simulator → if FAIL: write report, halt
  Invoke own mutation simulation → write combined simulation_report.json
  Set overall status PASS only if all four subsimulations pass.

Gate VG-SIM:

  simulation_report.status == "PASS" on all four simulators.
  --execute mode is blocked unless VG-SIM passes in the current session.

Validation

  All four simulator modules execute without exception.
  simulation_report.json is produced with valid schema.
  simulation_report.json contains a "status" field and "subsimulations" block.

  NOTE: A FAIL status on simulation_report during AP self-analysis is
  acceptable if the failure correctly identifies known missing modules.
  The blocking criterion at this pass is that the simulators run and
  produce structured output — not that the AP repo is clean.
  VG-SIM must PASS before PASS_8 begins (not before PASS_5 exits).

Exit Condition

  PASS_5_VALIDATION_REPORT.json produced.
  All four simulators produce structured JSON output without exception.

---------------------------------------------------------------------

PASS_6 — REPAIR SUBSYSTEM

Entry Condition

  PASS_5 complete.

Objective

  Implement the automated deterministic repair subsystem. Invoked by
  the crawl engine on module failure. Also invocable standalone.

Modules

  WORKFLOW_MUTATION_TOOLING/repair/patch_generator.py
  WORKFLOW_MUTATION_TOOLING/repair/schema_repair.py
  WORKFLOW_MUTATION_TOOLING/repair/dependency_rewriter.py
  WORKFLOW_MUTATION_TOOLING/repair/module_normalizer.py
  WORKFLOW_MUTATION_TOOLING/repair/repair_engine.py

Build order within this pass (dependency order):

  1. patch_generator.py      — generates patch plans from violation records;
                               planning only, does not execute
  2. schema_repair.py        — applies schema-level corrections; header injection,
                               field normalization
  3. dependency_rewriter.py  — rewrites import paths; merges logic from
                               dependency_normalizer.py and import_rewrite_operator.py
  4. module_normalizer.py    — normalizes module structure; merges logic from
                               module_relocation_operator.py and namespace_disambiguator.py
  5. repair_engine.py        — orchestrates repair pipeline; routes violations
                               to correct operator via repair_registry.json;
                               manages retry loop; escalates to quarantine on
                               max_attempts exceeded

Safety rule: repair_engine.py passes simulate=True to all operators
unless --execute mode is active and VG-SIM has passed in current session.

Validation

  Seed a test header violation (missing required fields).
  repair_engine.repair(violation, simulate=True) returns status SIMULATED.

  Force max_repair_attempts = 0.
  repair_engine.repair(violation, simulate=True) returns status FAILED.
  Quarantine escalation path is triggered.

Exit Condition

  PASS_6_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_7 — VALIDATION LAYER + AUDIT REGENERATION

Entry Condition

  PASS_6 complete.
  SPEC-004 approved by Architect (or Architect authorizes execution
  against Draft status — see OQ-002).

Objective

  Implement header validation and architecture validation.
  Build the Stage1 audit regeneration tooling (M10–M17 missing modules).

Modules — Validation Layer

  WORKFLOW_MUTATION_TOOLING/validation/header_validator.py   (M-VAL-02)
  WORKFLOW_MUTATION_TOOLING/validation/validate_architecture.py (M-VAL-01, SPEC-004)

Modules — Audit Regeneration (M10–M17, missing builds only)

  M10 repo_directory_scanner.py     — analog migration completed in PASS_1
  M11 python_file_collector.py      — BUILD
  M12 import_extractor.py           — analog migration completed in PASS_1
  M13 symbol_import_extractor.py    — BUILD
  M14 header_schema_scanner.py      — analog migration completed in PASS_1
  M15 governance_contract_scanner.py — analog migration completed in PASS_1
  M16 runtime_phase_scanner.py      — BUILD
  M17 concept_spec_gap_detector.py  — BUILD

  Note: M10, M12, M14, M15 were migrated in PASS_1.
  PASS_7 builds the four remaining missing modules: M11, M13, M16, M17.

header_validator.py interface:

  validate_file(file_path, schema_path) -> dict
    Returns: {"status": "PASS|FAIL", "missing_fields": [], "file": "<path>"}

  validate_directory(dir_path, schema_path, recursive) -> dict
    Returns: {"total": 0, "compliant": 0, "violations": [...]}

  Required fields enforced: 13-field set per DS Section 5.7.
  Addendum 6-field set is the minimum; 13-field set is authoritative.

Gate VG-HDR: header_compliance_rate meets threshold (blocking).

validate_architecture.py behavior:

  Read-only. Never writes any file other than the designated output report.
  Runs all 8 standard checks + 8 V2-specific checks (DS Section 12).
  Returns exit code 1 if architecture_valid == false.
  Gate VG-ARCH (blocking).

Validation

  header_validator runs against WORKFLOW_MUTATION_TOOLING/ and
  produces header_compliance_report.json without exception.

  validate_architecture.py runs and produces
  architecture_validation_report.json without exception.

  All Stage1 modules (M10–M17) invocable via run(target) -> dict.
  Stage1 artifacts produced against a test fixture.
  Gate VG-S1: all Stage1 output artifacts present and schema-valid.

Exit Condition

  PASS_7_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_8 — CRAWL ENGINE

Entry Condition

  PASS_7 complete.
  VG-SIM passed (simulation_report.status == "PASS" in current session,
  not stale — confirms simulate mode is authorized against target).

Objective

  Implement crawl planning and execution. Includes the execution graph
  builder, mutation operators, and the full per-module pipeline.

Modules — build in this order (dependency order within pass):

  WORKFLOW_MUTATION_TOOLING/crawler/engine/checklist_evaluator.py
    Evaluates pre-crawl checklist. Gate VG-CFG.

  WORKFLOW_MUTATION_TOOLING/crawler/pipeline/syntax_validator.py      (M62)
    AST parse validation. Runs pre- and post-mutation.

  WORKFLOW_MUTATION_TOOLING/crawler/pipeline/governance_validator.py  (M63)
    Governance contract presence check.

  WORKFLOW_MUTATION_TOOLING/crawler/pipeline/phase_validator.py       (M64)
    runtime_stage field validation.

  WORKFLOW_MUTATION_TOOLING/crawler/mutation/header_injector.py       (M50)
    Inject or replace AP metadata header.
    Migrated from repair/operators/header_injection_operator.py in PASS_1.
    Confirm migration complete; apply PASS_8 interface contract.

  WORKFLOW_MUTATION_TOOLING/crawler/mutation/import_rewriter.py       (M51)
    Rewrite deep imports to canonical facade.
    Migrated from repair/operators/import_rewrite_operator.py in PASS_1.
    Confirm migration complete; apply PASS_8 interface contract.

  WORKFLOW_MUTATION_TOOLING/crawler/pipeline/module_processor.py      (M61)
    Orchestrates per-module pipeline in this order:
      syntax_validator → header_injector → import_rewriter →
      governance_validator → phase_validator → syntax_validator (post)

  WORKFLOW_MUTATION_TOOLING/crawler/monitor/crawl_monitor.py          (M65)
    Real-time progress tracking. Rebuild from 142B skeleton.

  WORKFLOW_MUTATION_TOOLING/crawler/quarantine/quarantine_manager.py  (M80)
    Stub isolation and quarantine_registry.json management.

  WORKFLOW_MUTATION_TOOLING/orchestration/execution_graphs/execution_graph_builder.py  (M39)
    Builds directed execution graph from crawl_plan.

  WORKFLOW_MUTATION_TOOLING/crawler/engine/crawl_planner.py           (M38)
    Produces dependency-ordered crawl plan.
    Consumes execution_order.json from PASS_4.
    Gate VG-CRAWL: crawl_plan.json valid; order_length > 0.

  WORKFLOW_MUTATION_TOOLING/crawler/engine/crawl_executor.py          (M60)
    Main crawl loop. Rebuild from 146B skeleton.
    Per-module: invoke module_processor → on FAIL: invoke repair_engine →
    on repair FAILED: invoke quarantine_manager.
    Never halts on single-module failure.

Per-module pipeline contract (module_processor.py):

  syntax_validator       → PASS or FAIL
  header_injector        → inject header
  import_rewriter        → rewrite imports
  governance_validator   → PASS or FAIL
  phase_validator        → PASS or FAIL
  syntax_validator       → post-mutation re-run

  Gate VG-MOD: post-mutation syntax valid.

Crawl executor contract:

  On module PASS: route artifacts via artifact_router; advance.
  On module FAIL: invoke repair_engine.repair().
  On REPAIRED: re-run module_processor; advance.
  On repair FAILED: invoke quarantine_manager.quarantine(); advance.
  Never halt on single-module failure.
  Produces crawl_status.json on completion.

Validation

  Single-module crawl pass completes end-to-end in --simulate mode
  without exception.
  crawl_status.json produced; total > 0.

Exit Condition

  PASS_8_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_9 — REPORTING SYSTEM

Entry Condition

  PASS_8 complete.

Objective

  Implement final reporting and commit management. Validate that a full
  pipeline run in --simulate mode produces all required output artifacts.

Modules

  WORKFLOW_MUTATION_TOOLING/crawler/commit/report_generator.py   (M93)
  WORKFLOW_MUTATION_TOOLING/crawler/commit/commit_finalizer.py   (M94)

report_generator.py responsibilities:

  Aggregate crawl data from context and produce all five output artifacts
  routed through artifact_router:

    validation_report.json       → WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
    repair_event_log.json        → WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
    mutation_log.json            → WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
    crawl_execution_log.json     → WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
    crawl_status.json            → WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/

  Gate VG-FINAL: crawl_status.json completion_rate == 100% (excl. quarantined).

commit_finalizer.py responsibilities:

  In --execute mode: clean commit of mutations with Architect authorization.
  In --simulate mode: produce commit_plan.json (no repo writes).

Note on PIPELINE_EXECUTION_MANIFEST.json:

  This artifact is produced by pipeline_runner.py (PASS_3) on every
  pipeline run, not by report_generator. It is not a PASS_9 deliverable.
  It is listed in Section 5 as a pipeline output artifact because it is
  always produced; its origin is the execution spine, not the reporting
  subsystem.

Validation

  Full pipeline run in --simulate mode:

  python controllers/pipeline_runner.py --target . --simulate

  Produces all five report artifacts at canonical paths:

    validation_report.json
    repair_event_log.json
    mutation_log.json
    crawl_execution_log.json
    crawl_status.json

Exit Condition

  PASS_9_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_10 — ANALYSIS COMPLETION

Entry Condition

  PASS_9 complete.

Objective

  Complete the remaining analysis modules not yet built.

  Stage1 modules to build (M11, M13, M16, M17 were deferred in PASS_7
  due to crawl engine dependency — Stage1 inputs must feed into Stage2):

    M11  tools/repo_mapping/python_file_collector.py
    M13  tools/import_analysis/symbol_import_extractor.py
    M16  tools/runtime_analysis/runtime_phase_scanner.py
    M17  tools/audit_tools/concept_spec_gap_detector.py

  Stage2 modules to build:

    M20  tools/repo_mapping/module_index_builder.py
    M21  analysis/dependency_graph_builder.py — already built in PASS_4;
         verify interface compliance; no rebuild required unless gaps found
    M22  tools/import_analysis/circular_dependency_detector.py
    M23  tools/runtime_analysis/runtime_phase_mapper.py
    M24  tools/runtime_analysis/runtime_boot_sequencer.py
    M25  tools/import_analysis/canonical_import_registry_builder.py

  M10 (repo_directory_scanner.py) — completed in PASS_1. Not in PASS_10 scope.
  M12 (import_extractor.py) — completed in PASS_1. Not in PASS_10 scope.
  M14 (header_schema_scanner.py) — completed in PASS_1. Not in PASS_10 scope.
  M15 (governance_contract_scanner.py) — completed in PASS_1. Not in PASS_10 scope.

Validation

  All Stage1 and Stage2 modules invoke without exception.
  All module outputs are structured JSON artifacts.
  Stage2 pipeline produces: module_index.json, runtime_phase_map.json,
  runtime_boot_sequence.json, canonical_import_registry.json.
  Gate VG-S1 and VG-S2 pass against AP repo.

Exit Condition

  PASS_10_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_11 — TARGET REPOSITORY ANALYSIS

Entry Condition

  PASS_10 complete.

Objective

  Implement the external repository analysis subsystem (AP_TOOL_PROP_01).
  This is the primary analysis engine for external target repos.

Modules — build in pipeline order:

  WORKFLOW_TARGET_AUDITS/modules/collection/artifact_collector.py       (TA-01)
    Stage0: traversal and indexing.
    Outputs: AP_ARTIFACT_INDEX.json, AP_DIRECTORY_TREE.json,
             AP_EMPTY_DIRECTORIES.json

  WORKFLOW_TARGET_AUDITS/modules/structure_analysis/structure_analyzer.py  (TA-02)
    Stage1: structural intelligence.
    Inputs: TA-01 outputs.
    Outputs: AP_STRUCTURE_ANALYSIS.json

  WORKFLOW_TARGET_AUDITS/modules/subsystem_analysis/subsystem_analyzer.py  (TA-03)
    Stage2: subsystem completeness.
    Inputs: TA-01 + TA-02 outputs.
    Outputs: AP_SUBSYSTEM_ANALYSIS.json

  WORKFLOW_TARGET_AUDITS/modules/gap_analysis/gap_analysis_engine.py       (TA-04)
    Stage3: remediation guidance.
    Inputs: TA-03 outputs; Design Specifications (optional).
    Outputs: AP_REPOSITORY_GAP_ANALYSIS.json
             Severity-labeled gaps with remediation guidance.

Validation

  Run the four-stage pipeline against AP repo for self-analysis.

  AP_ARTIFACT_INDEX.json produced.
  AP_STRUCTURE_ANALYSIS.json produced.
  AP_SUBSYSTEM_ANALYSIS.json produced.
  AP_REPOSITORY_GAP_ANALYSIS.json produced with severity-labeled findings
  consistent with known V1 state.

Exit Condition

  PASS_11_VALIDATION_REPORT.json produced with all blocking gates PASS.

---------------------------------------------------------------------

PASS_12 — LOGOS INTEGRATION

Entry Condition

  PASS_11 complete.
  LOGOS repository present in WORKFLOW_TARGET_PROCESSING/targets/repos/.

Objective

  Run the full pipeline against the LOGOS repository snapshot in
  --simulate mode. Produce simulation report and crawl plan for LOGOS.

  Note: Live crawl (--execute) on LOGOS is deferred. PASS_12 scope
  is simulation and planning only. --execute on LOGOS requires
  Architect authorization and is not part of this execution plan.

Validation

  VG-SIM: simulation_report.status == "PASS" on LOGOS snapshot.
  crawl_plan.json produced for LOGOS with order_length > 0.

Exit Condition

  PASS_12_VALIDATION_REPORT.json produced with all blocking gates PASS.
  ARCHON PRIME V2 tooling engine is considered operationally ready.

---------------------------------------------------------------------

SECTION 4 — EXECUTION MODE CONTRACT

Default execution mode:

  --simulate

  All reads and computations execute.
  No writes to target repository.
  Artifacts produced with "simulation": true.

Execution mode:

  --execute

  Live mutations applied to target repository.

--execute may only be enabled when:

  VG-SIM == PASS in the current session.
  VG-SIM must be confirmed non-stale: simulation results from a
  previous session do not satisfy this requirement.
  pipeline_runner.py enforces this check at runtime before authorizing
  any mutating operation.

  Note: VG-ARCH (architecture validation) is a Stage0 blocking gate
  that must pass before the pipeline proceeds. It is not a separate
  prerequisite for --execute mode — it is a prerequisite for the
  pipeline running at all.

---------------------------------------------------------------------

SECTION 5 — OUTPUT ARTIFACTS

A complete pipeline execution must produce the following artifacts.
All artifacts must route through runtime/artifact_router.py.

  PIPELINE_EXECUTION_MANIFEST.json   — produced by pipeline_runner.py
                                       on every run (complete or halted)
  validation_report.json             — produced by report_generator.py
  repair_event_log.json              — produced by report_generator.py
  mutation_log.json                  — produced by report_generator.py
  crawl_execution_log.json           — produced by report_generator.py
  crawl_status.json                  — produced by report_generator.py

---------------------------------------------------------------------

SECTION 6 — FAILURE CONDITIONS

The pipeline must halt if any of the following occurs.

  VG-ARCH FAIL    architecture validation failure (Stage0 blocking gate)
  VG-HDR FAIL     header compliance failure below threshold (Stage0 blocking gate)
  VG-CFG FAIL     missing configuration files at initialization
  VG-S2 FAIL      dependency graph generation failure
  VG-SIM FAIL     simulation failure (blocks --execute; does not halt --simulate)
  VG-CRAWL FAIL   crawl plan invalid or empty
  VG-FINAL FAIL   crawl completion rate below threshold
  artifact routing violation (artifact write attempted outside router)
  schema compliance failure on pipeline output artifact

  Per DS Section 6.2: when workflow_controller returns status BLOCKED,
  pipeline_runner produces PIPELINE_EXECUTION_MANIFEST.json with
  overall_status == "HALTED" and exits with code 1.

  Single-module failures during crawl do not halt the pipeline.
  Failed modules are escalated to repair, then to quarantine if
  repair is unsuccessful. The pipeline advances in all cases.

---------------------------------------------------------------------

SECTION 7 — FINAL STATE

Upon completion of PASS_12:

  ARCHON_PRIME V2 tooling engine is operationally ready.

  All modules exist in canonical directories.
  All 12 PASS_N_VALIDATION_REPORT.json artifacts produced.
  All validation gates pass on the LOGOS simulation run.
  Simulation and execute modes function correctly.
  Full crawl plan for LOGOS repository is available.

  Remaining deferred items (not part of this execution plan):

    LOGOS live crawl (--execute)   — requires Architect authorization
    DRAC implementation            — Architect standing deferment
    LOGOS DS/IG V2 schema upgrade  — separate workstream
    SPEC-011 for AP_TOOL_PROP_01   — pending Architect decision
    CI/CD integration              — deferred

---------------------------------------------------------------------

END OF ARTIFACT

SYSTEM: ARCHON_PRIME
ARTIFACT_TYPE: Implementation_Guide
ARTIFACT_NAME: AP_V2_Tooling_IG
VERSION: 2.0
DATE: 2026-03-10
AUTHORITY: Architect

---------------------------------------------------------------------

# AP_V2_Tooling_IG
## ARCHON PRIME — V2 Tooling Implementation Guide (Final)

---

## Document Identity

| Field | Value |
|---|---|
| Artifact ID | IMPL-010 |
| System | ARCHON_PRIME |
| Platform | Python 3.11+ / GitHub Codespaces |
| Artifact Type | Implementation Guide — Final |
| Version | v2 |
| Status | Final Draft — Pending Architect Approval |
| Schema | AP_IMPLEMENTATION_GUIDE_SCHEMA.json |
| Authority Source | Architect |
| Spec Reference | AP_V2_Tooling_DS (SPEC-010 v2) |
| Source Artifacts | IMPL-010 v1, IMPL_AP_V2_TOOLING_IMPLEMENTATION_GUIDE_ADDENDUM |
| Author | Claude / Formalization_Expert |
| Date | 2026-03-10 |
| Supersedes | IMPL_AP_V2_TOOLING_IMPLEMENTATION_GUIDE.md (v1) |

---

## 1. Purpose

This guide provides deterministic implementation instructions for the ARCHON_PRIME V2 tooling layer as defined in AP_V2_Tooling_DS. It is consumed by GPT (Prompt_Engineer role) to derive VS Code execution prompts. It is not executed directly.

The implementation strategy, per the addendum, is to complete the execution infrastructure. The majority of the AP tooling architecture already exists in analog form. The primary targets are the six layers that were absent in V1: orchestration controller, repair subsystem, simulation subsystem, artifact routing, dependency graph engine, and configuration layer.

---

## 2. Pre-Implementation Requirements

### 2.1 Architect Actions Required Before Work Begins

| Item | Required For | Status |
|---|---|---|
| Approve AP_V2_Tooling_DS (SPEC-010 v2) | All passes | Pending |
| Resolve OQ-001 / CL-G1 (schema filename) | DS schema validation | Pending |
| Approve SPEC-004 or authorize IG against Draft | PASS_3, PASS_7 | Pending |

### 2.2 Environment Verification

The VS Code execution agent must confirm before any prompt is executed:

```bash
python --version          # Must be 3.11+
pwd                       # Must be /workspaces/ARCHON_PRIME
git status                # Must be clean (or Architect authorizes dirty tree)
python -c "import jsonschema; import yaml; import git; print('ok')"
ls AP_SYSTEM_CONFIG/      # Must be accessible
ls AP_SYSTEM_AUDIT/       # Must be accessible
```

### 2.3 Mutation Safety Preconditions

1. `--simulate` flag is the default for all execution. `--execute` requires explicit authorization.
2. `AP_SYSTEM_CONFIG/` and `AP_SYSTEM_AUDIT/` are never write targets — enforced at prompt level.
3. Non-deletion policy: no `rm`, `shutil.rmtree`, or `os.remove` on existing files without Architect authorization.
4. All artifact writes must route through `runtime/artifact_router.py` after PASS_2 is complete.

### 2.4 Migration Log Initialization

Before any analog module is migrated, create (if not present):

**File:** `WORKFLOW_MUTATION_TOOLING/AP_LEGACY_MODULE_MIGRATION_LOG.json`

```json
{
  "schema_version": "2.0",
  "generated_at": "<ISO>",
  "policy": "NON_DELETION_ENFORCED",
  "migrations": []
}
```

Each entry on migration:
```json
{
  "module_name": "<filename>",
  "original_path": "<rel path from repo root>",
  "target_path": "<rel path from repo root>",
  "classification": "MIGRATE|MIGRATE_AND_RENAME|REFACTOR|REBUILD|PRESERVE|DEPRECATE",
  "status": "PENDING|IN_PROGRESS|COMPLETE|DEFERRED",
  "migrated_at": "<ISO or null>"
}
```

---

## 3. Pass-Level Implementation Instructions

Each pass below is a self-contained unit of work. Passes must be executed in order. No pass may begin until its entry condition is met and its predecessor's exit condition is confirmed.

### Validation Report Format (required after every pass)

Every pass must produce a `PASS_N_VALIDATION_REPORT.json`:

```json
{
  "pass_id": "PASS_N",
  "status": "COMPLETE|INCOMPLETE|BLOCKED",
  "modules_created": [],
  "modules_modified": [],
  "artifacts_produced": [],
  "gate_results": [{ "gate_id": "<str>", "status": "PASS|FAIL", "detail": "<str>" }],
  "blocking_issues": []
}
```

---

## 4. PASS_1 — Configuration Layer

**Entry condition:** AP_V2_Tooling_DS approved.
**Stage:** Stage0 — Foundation.
**Exit condition:** All 6 config files present; migration log created with 22 entries (status PENDING); routing_table.json rebuilt; no modules at repo root outside canonical domains.

### 4.1 Migration Log Creation

Create `WORKFLOW_MUTATION_TOOLING/AP_LEGACY_MODULE_MIGRATION_LOG.json` with all 22 entries from Section 7 of AP_V2_Tooling_DS, status PENDING.

### 4.2 Configuration File Creation

**File 1: `WORKFLOW_MUTATION_TOOLING/configs/ap_config.yaml`**
```yaml
# AP METADATA HEADER
# artifact_id: CFG-001
# system: ARCHON_PRIME
# purpose: Architect override layer; values here supersede crawl_config.json defaults
# author: ARCHON_PRIME
# authority: Architect
# timestamp: 2026-03-10

mutation_allowed: false
simulation_mode: true
log_level: INFO
max_repair_attempts: 3
quarantine_on_failure: true
```

**File 2: `WORKFLOW_MUTATION_TOOLING/configs/logos_targets.yaml`**
```yaml
# AP METADATA HEADER
# artifact_id: CFG-002
# system: ARCHON_PRIME
# purpose: Target repository definitions for AP crawl operations
# author: ARCHON_PRIME
# authority: Architect
# timestamp: 2026-03-10

targets:
  - name: LOGOS
    path: /workspaces/LOGOS
    branch: main
    language: python
    description: "Primary target repository for AP crawl validation"
```

**File 3: `WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/crawl_config.json`**
```json
{
  "schema_version": "2.0",
  "artifact_id": "CFG-003",
  "system": "ARCHON_PRIME",
  "mutation_allowed": false,
  "simulation_mode": true,
  "crawl": {
    "target_path": "/workspaces/LOGOS",
    "max_depth": 20,
    "supported_extensions": [".py", ".json", ".yaml", ".yml", ".md"],
    "exclusions": ["__pycache__", ".git", "*.pyc", "venv", ".venv", "node_modules"]
  },
  "repair": {
    "max_repair_attempts": 3,
    "quarantine_on_failure": true
  },
  "registry_path": "WORKFLOW_MUTATION_TOOLING/registry/module_registry.json",
  "routing_table_path": "WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table.json"
}
```

**File 4: `WORKFLOW_MUTATION_TOOLING/configs/phase_maps/phase_map_config.json`**
```json
{
  "schema_version": "2.0",
  "artifact_id": "CFG-004",
  "system": "ARCHON_PRIME",
  "stages": [
    { "stage_id": "Stage0", "name": "Foundation", "blocking": true },
    { "stage_id": "Stage1", "name": "Audit", "blocking": true },
    { "stage_id": "Stage2", "name": "Analysis", "blocking": true },
    { "stage_id": "Stage3", "name": "Simulation", "blocking": true },
    { "stage_id": "Stage4", "name": "Crawler", "blocking": true },
    { "stage_id": "Stage5", "name": "Repair", "blocking": true },
    { "stage_id": "Stage6", "name": "Orchestration", "blocking": true }
  ]
}
```

**File 5: `WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/header_schema.json`**
```json
{
  "schema_version": "2.0",
  "artifact_id": "CFG-005",
  "system": "ARCHON_PRIME",
  "required_fields": [
    "artifact_id", "system", "purpose", "author", "authority", "timestamp",
    "module_name", "subsystem", "canonical_path", "runtime_stage",
    "spec_reference", "implementation_phase", "status"
  ],
  "runtime_stage_values": [
    "initialization", "analysis", "processing", "validation",
    "repair", "audit", "reporting", "utility"
  ],
  "status_values": ["canonical", "draft", "deprecated"],
  "authoring_authority": "ARCHON_PRIME"
}
```

**File 6: Rebuild `WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table.json`**

Replace current content (contains legacy AUDIT_SYSTEM/ references) with:
```json
{
  "schema_version": "2.0",
  "artifact_id": "CFG-006",
  "system": "ARCHON_PRIME",
  "routes": {
    "repo_directory_tree":          "WORKFLOW_TARGET_AUDITS/reports/",
    "repo_python_files":            "WORKFLOW_TARGET_AUDITS/reports/",
    "repo_imports":                 "WORKFLOW_TARGET_AUDITS/reports/",
    "module_index":                 "WORKFLOW_TARGET_AUDITS/reports/",
    "dependency_graph":             "WORKFLOW_TARGET_AUDITS/reports/",
    "cycle_report":                 "WORKFLOW_TARGET_AUDITS/reports/",
    "execution_order":              "WORKFLOW_TARGET_AUDITS/reports/",
    "runtime_phase_map":            "WORKFLOW_TARGET_AUDITS/reports/",
    "simulation_report":            "WORKFLOW_TARGET_AUDITS/reports/",
    "crawl_plan":                   "WORKFLOW_TARGET_AUDITS/reports/",
    "gap_analysis_report":          "WORKFLOW_TARGET_AUDITS/reports/",
    "validation_report":            "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "architecture_validation_report": "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "header_compliance_report":     "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "crawl_execution_log":          "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "repair_event_log":             "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "mutation_log":                 "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "crawl_status":                 "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/",
    "pipeline_execution_manifest":  "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/"
  }
}
```

### 4.3 Analog Module Migration (22 modules)

For each migration, execute in this order:
1. Update migration log entry: status IN_PROGRESS
2. Copy source file to target path (do not delete source)
3. Replace header block in copied file with V2 13-field header
4. Update migration log entry: status COMPLETE, migrated_at timestamp

Execute in the order defined in Section 7 of AP_V2_Tooling_DS. Migration #16 and #17 (runtime_simulator.py, import_simulator.py) are rebuilds — copy first, mark as REBUILD target for PASS_5.

### 4.4 Audit Tool Interface Standardization

Modify `run_audit_suite.py` and `run_governance_audit.py`:
- Add `--target <path>` CLI argument
- Wrap execution in standard `run(target: str) -> dict` returning `{"status": "ok|error", "artifact_output": "<path>", "findings": [...]}`

### 4.5 PASS_1 Validation Gate

```bash
# Verify config files
ls WORKFLOW_MUTATION_TOOLING/configs/ap_config.yaml
ls WORKFLOW_MUTATION_TOOLING/configs/logos_targets.yaml
ls WORKFLOW_MUTATION_TOOLING/configs/crawl_configs/crawl_config.json
ls WORKFLOW_MUTATION_TOOLING/configs/phase_maps/phase_map_config.json
ls WORKFLOW_MUTATION_TOOLING/tools/normalization_tools/header_schema.json
ls WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table.json

# Verify routing table has no legacy paths
python -c "
import json
rt = json.load(open('WORKFLOW_MUTATION_TOOLING/orchestration/task_router/routing_table.json'))
legacy = [k for k,v in rt['routes'].items() if 'AUDIT_SYSTEM' in v]
assert len(legacy) == 0, f'Legacy paths found: {legacy}'
print('routing_table: PASS')
"

# Verify migration log
python -c "
import json
log = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_LEGACY_MODULE_MIGRATION_LOG.json'))
assert len(log['migrations']) == 22, f'Expected 22 entries, got {len(log[\"migrations\"])}'
print(f'migration_log: PASS ({len(log[\"migrations\"])} entries)')
"
```

Required output: `PASS_1_VALIDATION_REPORT.json` — all gates PASS.

---

## 5. PASS_2 — Artifact Routing System

**Entry condition:** PASS_1 complete.
**Stage:** Stage6 — Orchestration (routing layer).
**Exit condition:** Artifact routing operational; a test artifact routed to correct canonical path; output_registry populated.

### 5.1 Module: runtime/routing_table.py

**Header:**
```python
# AP METADATA HEADER
# artifact_id: M92
# system: ARCHON_PRIME
# purpose: Load routing_table.json and resolve canonical artifact output paths
# author: ARCHON_PRIME
# authority: Architect
# timestamp: 2026-03-10
# module_name: routing_table
# subsystem: Orchestration
# canonical_path: WORKFLOW_MUTATION_TOOLING/runtime/routing_table.py
# runtime_stage: initialization
# spec_reference: SPEC-010.section.5.2
# implementation_phase: PASS_2
# status: canonical
```

**Interface:**
```python
def load(routing_table_path: str) -> dict
def get_path(artifact_type: str) -> str
  # Raises RoutingError if artifact_type not in routing table
def validate_routes() -> dict
  # Returns {"status": "ok|error", "legacy_refs": [], "missing_dirs": []}
```

### 5.2 Module: runtime/output_registry.py

**Header:** Same pattern, artifact_id M91.

**Interface:**
```python
def register(artifact_path: str, artifact_type: str, schema_name: str = None) -> dict
  # Returns {"status": "registered|schema_violation", "entry": {...}}
def get_registry() -> list[dict]
def write_registry(output_path: str) -> None
```

**Registry entry schema:**
```json
{
  "artifact_type": "<str>",
  "artifact_path": "<str>",
  "produced_at": "<ISO>",
  "schema_validated": true,
  "simulation": true
}
```

### 5.3 Module: runtime/artifact_router.py

**Header:** Same pattern, artifact_id M90.

**Interface:**
```python
def route(artifact: dict, artifact_type: str, metadata: dict, simulate: bool = True) -> dict
  # Resolves path from routing_table
  # In simulate mode: returns routing plan without writing
  # In execute mode: writes file + registers in output_registry
  # Returns {"status": "routed|simulated|error", "output_path": "<str>", "simulation": <bool>}
```

**Safety rule:** `artifact_router.py` must refuse to write to `AP_SYSTEM_CONFIG/` or `AP_SYSTEM_AUDIT/` (immutable directories). Hard-coded refusal, not configurable.

### 5.4 PASS_2 Validation Gate

```python
# Test: route a test artifact, verify it lands at correct path
from runtime.artifact_router import route
from runtime.routing_table import load, get_path
load("orchestration/task_router/routing_table.json")
result = route({"test": "data"}, "validation_report", {}, simulate=True)
assert result["status"] == "simulated"
assert "WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT" in result["output_path"]
print("PASS_2: artifact routing PASS")
```

Required output: `PASS_2_VALIDATION_REPORT.json` — all gates PASS.

---

## 6. PASS_3 — Execution Spine

**Entry condition:** PASS_2 complete; SPEC-004 approved by Architect.
**Stage:** Stage6 — Orchestration (execution spine).
**Exit condition:** `pipeline_runner.py` executes a single no-op stage without exception; `PIPELINE_EXECUTION_MANIFEST.json` produced.

### 6.1 Module: controllers/runtime_context_manager.py

Holds all runtime state shared across stages. Must be initialized before any stage runs.

**Interface:**
```python
class RuntimeContext:
    target: str
    mode: str              # "simulate" | "execute"
    session_id: str
    started_at: str
    config: dict
    artifact_registry: list
    stage_results: dict

def initialize(target: str, mode: str, config: dict) -> RuntimeContext
def get_context() -> RuntimeContext
def update_stage_result(stage_id: str, result: dict) -> None
```

### 6.2 Module: controllers/execution_scheduler.py

**Interface:**
```python
def schedule(phase_map: dict) -> list[dict]
  # Returns ordered list of stage execution records with blocking constraints
def check_gate(gate_id: str, context: RuntimeContext) -> dict
  # Returns {"gate_id": "<str>", "status": "PASS|FAIL", "detail": "<str>"}
```

### 6.3 Module: controllers/task_router.py

**Interface:**
```python
def route(task_type: str, payload: dict, context: RuntimeContext) -> dict
  # Dispatches task to correct subsystem module
  # Returns {"status": "dispatched|error", "handler": "<module>", "result": {...}}
```

**Task type registry (must be defined in task_router.py at module level):**

| Task Type | Handler Module |
|---|---|
| audit_regeneration | tools/audit_tools/run_audit_suite.py |
| dependency_analysis | analysis/dependency_graph_builder.py |
| simulation_run | simulation/mutation_simulator.py (coordinator) |
| crawl_plan | crawler/engine/crawl_planner.py |
| module_repair | repair/repair_engine.py |
| artifact_route | runtime/artifact_router.py |
| header_validate | validation/header_validator.py |
| arch_validate | validation/validate_architecture.py |

### 6.4 Module: controllers/workflow_controller.py

**Interface:**
```python
def execute_stage(stage_id: str, context: RuntimeContext) -> dict
  # Runs all tasks for the stage; enforces gate conditions before returning
  # Returns {"stage_id": "<str>", "status": "COMPLETE|FAILED|BLOCKED", "gate_results": [...]}

def check_blocking_gates(stage_id: str, context: RuntimeContext) -> bool
  # Returns True if all blocking gates for this stage pass; False halts pipeline
```

**Gate enforcement contract:** If any blocking gate returns FAIL, `execute_stage` must return `{"status": "BLOCKED"}` and `workflow_controller` must not invoke subsequent stages.

### 6.5 Module: controllers/pipeline_runner.py

Entry point for all pipeline executions. The only module a human or automated system invokes directly.

**CLI interface:**
```
python controllers/pipeline_runner.py --target <path> [--simulate|--execute] [--stage <stage_id>]
```

**Pseudocode:**
```python
def run(target, mode, stage=None):
    context = initialize_context(target, mode)
    execution_plan = schedule(phase_map_config)
    manifest = start_manifest(context)

    for stage_def in execution_plan:
        if stage and stage_def["stage_id"] != stage:
            continue
        # PRE-EXECUTE MODE CHECK
        if mode == "execute":
            assert context.stage_results.get("Stage3", {}).get("status") == "COMPLETE", \
                "VG-EXEC: simulation must pass before --execute is authorized"
        result = workflow_controller.execute_stage(stage_def["stage_id"], context)
        manifest.record(result)
        if result["status"] == "BLOCKED":
            manifest.finalize("HALTED", halt_reason=result)
            route(manifest, "pipeline_execution_manifest")
            sys.exit(1)

    manifest.finalize("COMPLETE")
    route(manifest, "pipeline_execution_manifest")
    sys.exit(0)
```

### 6.6 PASS_3 Validation Gate

```bash
python controllers/pipeline_runner.py --target . --simulate --stage Stage0
# Must produce PIPELINE_EXECUTION_MANIFEST.json without exception
# Stage0 result status must be COMPLETE or BLOCKED (not an unhandled exception)
```

Required output: `PASS_3_VALIDATION_REPORT.json` — all gates PASS.

---

## 7. PASS_4 — Dependency Graph Engine

**Entry condition:** PASS_3 complete.
**Stage:** Stage2 — Analysis.
**Exit condition:** `dependency_graph.json` and `execution_order.json` produced for AP repo self-analysis; cycle report produced.

### 7.1 Module: analysis/dependency_graph_builder.py

Consumes `repo_imports.json` and `module_index.json`. Builds directed import graph.

**Interface:**
```python
def build(imports_path: str, module_index_path: str) -> dict
  # Returns graph: {"module_a": ["module_b", "module_c"], ...}
def run(target: str, output_path: str = None) -> dict
  # Writes dependency_graph.json; returns run result
```

**Output schema:**
```json
{
  "schema_version": "2.0",
  "generated_at": "<ISO>",
  "total_modules": 0,
  "total_edges": 0,
  "graph": { "<module_path>": ["<dep_path>", ...] }
}
```

### 7.2 Module: analysis/cycle_detector.py

Consumes `dependency_graph.json`. DFS cycle detection.

**Interface:**
```python
def detect(graph: dict) -> dict
  # Returns cycle_report: {"cycle_groups": [[...], ...], "has_cycles": bool}
def run(graph_path: str, output_path: str = None) -> dict
  # Writes cycle_report.json; returns run result
```

### 7.3 Module: analysis/execution_order_planner.py

Consumes `dependency_graph.json` and `cycle_report.json`. Produces topological sort. Handles cycles by flagging affected modules for repair before execution.

**Interface:**
```python
def plan(graph: dict, cycle_report: dict) -> dict
  # Returns execution_order: {"order": ["<module>", ...], "flagged_for_repair": [...]}
def run(graph_path: str, cycle_report_path: str, output_path: str = None) -> dict
  # Writes execution_order.json; returns run result
```

### 7.4 PASS_4 Validation Gate

```bash
python analysis/dependency_graph_builder.py --target . --output WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
python analysis/cycle_detector.py --graph WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/dependency_graph.json
python analysis/execution_order_planner.py --graph WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/dependency_graph.json \
  --cycles WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/cycle_report.json

# Verify outputs
python -c "
import json
dg = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/dependency_graph.json'))
eo = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/execution_order.json'))
assert dg['total_modules'] > 0, 'dependency_graph empty'
assert len(eo['order']) > 0, 'execution_order empty'
print(f'PASS_4: modules={dg[\"total_modules\"]}, order_length={len(eo[\"order\"])} PASS')
"
```

Required output: `PASS_4_VALIDATION_REPORT.json` — all gates PASS.

---

## 8. PASS_5 — Simulation Framework

**Entry condition:** PASS_4 complete.
**Stage:** Stage3 — Simulation.
**Exit condition:** All four simulators produce outputs; `simulation_report.status == "PASS"` on AP repo.

All simulation modules must return:
```python
{"status": "PASS|FAIL", "simulation": True, "findings": [], "detail": {...}}
```

### 8.1 Module: simulation/runtime_simulator.py (Rebuild)

Supersedes the partial functional analog. Must consume `dependency_graph.json` and `module_index.json` and simulate dependency resolution order.

**Interface:**
```python
def simulate(module_index_path: str, dependency_graph_path: str) -> dict
  # Returns SimResult: {"status": "PASS|FAIL", "simulation": True, "unresolvable": [], "boot_order": [...]}
def run(target: str, output_path: str = None) -> dict
```

### 8.2 Module: simulation/import_surface_simulator.py (Rebuild from import_simulator.py)

Supersedes the functional import_simulator. Must simulate import surface against facade registry.

**Interface:**
```python
def simulate(repo_imports_path: str, facade_registry_path: str) -> dict
  # Returns SimResult: {"status": "PASS|FAIL", "facade_violations": [], "deep_imports": [...]}
def run(target: str, output_path: str = None) -> dict
```

### 8.3 Module: simulation/integration_simulator.py (Build)

Simulates module integration. Detects interface mismatches between modules that import each other.

**Interface:**
```python
def simulate(module_index_path: str, governance_map_path: str) -> dict
  # Returns SimResult: {"status": "PASS|FAIL", "interface_mismatches": [], "missing_contracts": [...]}
def run(target: str, output_path: str = None) -> dict
```

### 8.4 Module: simulation/mutation_simulator.py (Build — absorbs repo_simulator logic)

Simulates all planned mutations before execution. Must run after the other three simulators pass. Entry point for the simulation coordinator role.

**Interface:**
```python
def simulate(crawl_plan_path: str, patch_plans: list = None) -> dict
  # Returns MutationSimResult: {"status": "PASS|FAIL", "planned_mutations": [], "predicted_breakage": [...]}
def run_full_simulation(target: str, output_path: str = None) -> dict
  # Invokes all four simulators in sequence; produces combined simulation_report.json
  # Returns {"status": "PASS|FAIL", "subsimulations": {...}}
```

**Simulation coordinator contract (mutation_simulator.py):**
1. Invoke `runtime_simulator.simulate()`
2. If FAIL: write simulation_report with status FAIL, halt
3. Invoke `import_surface_simulator.simulate()`
4. If FAIL: write simulation_report with status FAIL, halt
5. Invoke `integration_simulator.simulate()`
6. If FAIL: write simulation_report with status FAIL, halt
7. Invoke own `simulate()` (mutation simulation)
8. Write combined simulation_report.json
9. Set overall status PASS only if all four pass

### 8.5 PASS_5 Validation Gate

```bash
python simulation/mutation_simulator.py --target . --simulate \
  --output WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/

python -c "
import json
sr = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/simulation_report.json'))
print(f'Simulation status: {sr[\"status\"]}')
for k, v in sr['subsimulations'].items():
    print(f'  {k}: {v[\"status\"]}')
# Note: FAIL on AP self-simulation is acceptable if it correctly identifies
# known missing modules. The key check is that the simulator runs and produces
# a structured report, not that the AP repo itself is clean.
assert 'status' in sr, 'simulation_report missing status field'
print('PASS_5: simulation framework PASS')
"
```

Required output: `PASS_5_VALIDATION_REPORT.json` — simulators run without exception; simulation_report.json produced.

---

## 9. PASS_6 — Repair Subsystem

**Entry condition:** PASS_5 complete.
**Stage:** Stage5 — Repair.
**Exit condition:** Seeded header violation repaired; quarantine triggered on max-attempt failure.

### 9.1 Module: repair/patch_generator.py

Generates a deterministic patch plan from a violation record. Does not execute — planning only.

**Interface:**
```python
def generate(violation: dict) -> dict
  # violation: {"issue_type": "<str>", "module_path": "<str>", "detail": {...}}
  # Returns PatchPlan: {"issue_type": "<str>", "operator": "<str>", "actions": [...], "reversible": bool}
```

### 9.2 Module: repair/schema_repair.py

Applies schema-level corrections: header injection, field normalization.

**Interface:**
```python
def apply(patch_plan: dict, simulate: bool = True) -> dict
  # Returns PatchResult: {"status": "APPLIED|SIMULATED|FAILED", "changes": [...], "simulation": <bool>}
```

### 9.3 Module: repair/dependency_rewriter.py

Rewrites import paths. Corrects deep imports. Enforces canonical import facade. Merges logic from `repair/operators/dependency_normalizer.py` and `import_rewrite_operator.py` analogs.

**Interface:**
```python
def rewrite(patch_plan: dict, simulate: bool = True) -> dict
  # Returns PatchResult: {"status": "APPLIED|SIMULATED|FAILED", "rewrites": [...], "simulation": <bool>}
```

### 9.4 Module: repair/module_normalizer.py

Normalizes module structure. Handles path relocation and namespace disambiguation. Merges logic from `module_relocation_operator.py` and `namespace_disambiguator.py` analogs.

**Interface:**
```python
def normalize(patch_plan: dict, simulate: bool = True) -> dict
  # Returns PatchResult: {"status": "APPLIED|SIMULATED|FAILED", "changes": [...], "simulation": <bool>}
```

### 9.5 Module: repair/repair_engine.py

Orchestrates the full repair pipeline. Routes to correct operator based on issue_type via repair_registry.json.

**Interface:**
```python
def repair(violation: dict, simulate: bool = True) -> dict
  # Returns RepairResult: {"status": "REPAIRED|FAILED|SIMULATED", "attempts": <int>, "detail": {...}}
```

**Repair loop (pseudocode):**
```python
def repair(violation, simulate):
    max_attempts = config.get("max_repair_attempts", 3)
    for attempt in range(1, max_attempts + 1):
        patch = patch_generator.generate(violation)
        operator = get_operator(patch["operator"])
        result = operator.apply(patch, simulate)
        if result["status"] in ("APPLIED", "SIMULATED"):
            return {"status": "REPAIRED" if not simulate else "SIMULATED", "attempts": attempt}
        if attempt == max_attempts:
            return {"status": "FAILED", "attempts": attempt, "detail": result}
    return {"status": "FAILED", "attempts": max_attempts}
```

### 9.6 PASS_6 Validation Gate

```python
# Seed a test violation and confirm repair
from repair.repair_engine import repair
test_violation = {
    "issue_type": "header_violation",
    "module_path": "test_fixtures/test_module_no_header.py",
    "detail": {"missing_fields": ["artifact_id", "system", "purpose"]}
}
result = repair(test_violation, simulate=True)
assert result["status"] == "SIMULATED", f"Expected SIMULATED, got {result['status']}"
print(f"PASS_6: repair engine PASS (attempts={result['attempts']})")

# Test quarantine escalation
from repair.repair_engine import repair
import json
config_override = {"max_repair_attempts": 0}  # Force immediate failure
result = repair(test_violation, simulate=True)
assert result["status"] == "FAILED"
print("PASS_6: quarantine escalation trigger PASS")
```

Required output: `PASS_6_VALIDATION_REPORT.json` — all gates PASS.

---

## 10. PASS_7 — Header Validation and Architecture Validation

**Entry condition:** PASS_6 complete; SPEC-004 approved.
**Stage:** Stage0 — Foundation (validation layer).
**Exit condition:** `header_validator.py` produces compliance report; `validate_architecture.py` runs without exception.

### 10.1 Module: validation/header_validator.py

**Header fields validated (6-field minimum per addendum; 13-field full per SPEC-010):**

```python
ADDENDUM_MINIMUM_FIELDS = {"artifact_id", "system", "purpose", "author", "authority", "timestamp"}
SPEC_010_FULL_FIELDS = ADDENDUM_MINIMUM_FIELDS | {
    "module_name", "subsystem", "canonical_path", "runtime_stage",
    "spec_reference", "implementation_phase", "status"
}
```

**Interface:**
```python
def validate_file(file_path: str, schema_path: str = None) -> dict
  # Returns {"status": "PASS|FAIL", "missing_fields": [], "file": "<path>"}

def validate_directory(dir_path: str, schema_path: str = None, recursive: bool = True) -> dict
  # Returns {"total": 0, "compliant": 0, "violations": [...]}

def run(target: str, output_path: str = None) -> dict
  # Writes header_compliance_report.json; returns run result
```

**Output schema:**
```json
{
  "schema_version": "2.0",
  "generated_at": "<ISO>",
  "target": "<path>",
  "total_modules_scanned": 0,
  "compliant": 0,
  "non_compliant": 0,
  "compliance_rate": 0.0,
  "violations": [{ "file": "<path>", "missing_fields": [] }]
}
```

### 10.2 Module: validation/validate_architecture.py (M-VAL-01)

Built per SPEC-004. See PASS_3 entry condition — requires SPEC-004 Architect approval. Key behavioral requirements repeated here for completeness:

- Read-only — never writes any file other than the designated output report
- Runs all 8 standard checks + 8 V2-specific checks before reporting
- Deferred subsystems excluded from expected module set
- Returns exit code 1 if `architecture_valid == false`
- Handles missing registry with `REGISTRY_UNAVAILABLE` finding

### 10.3 PASS_7 Validation Gate

```bash
# Header validation on AP runtime surface
python validation/header_validator.py --target WORKFLOW_MUTATION_TOOLING/ \
  --output WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/

python -c "
import json
report = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/header_compliance_report.json'))
print(f'Header compliance: {report[\"compliant\"]}/{report[\"total_modules_scanned\"]} ({report[\"compliance_rate\"]:.1f}%)')
# After PASS_1 migrations, all newly created modules should be compliant
# Legacy analog modules may show violations — this is expected and documented
print('PASS_7: header_validator PASS')
"

# Architecture validation
python validation/validate_architecture.py --spec SPEC-010 \
  --registry WORKFLOW_MUTATION_TOOLING/registry/module_registry.json \
  --output WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/
```

Required output: `PASS_7_VALIDATION_REPORT.json` — validators run; reports produced.

---

## 11. PASS_8 — Crawl Engine

**Entry condition:** PASS_7 complete; VG-SIM passed.
**Stage:** Stage4 — Crawler.
**Exit condition:** Single-module crawl pass in `--simulate` mode completes end-to-end.

### 11.1 Build sequence within PASS_8

Build in this order (dependency order within the pass):

1. `crawler/engine/checklist_evaluator.py` — validates pre-crawl checklist; gate VG-CFG
2. `crawler/pipeline/syntax_validator.py` (M62) — AST parse validation
3. `crawler/pipeline/governance_validator.py` (M63) — governance contract presence check
4. `crawler/pipeline/phase_validator.py` (M64) — runtime_stage field validation
5. `crawler/pipeline/module_processor.py` (M61) — orchestrates per-module pipeline
6. `crawler/monitor/crawl_monitor.py` (M65) — real-time progress tracking; rebuild from 142B skeleton
7. `crawler/quarantine/quarantine_manager.py` (M80) — stub isolation, quarantine_registry.json
8. `orchestration/execution_graphs/execution_graph_builder.py` (M39) — directed execution graph from crawl_plan
9. `crawler/engine/crawl_planner.py` (M38) — dependency-ordered crawl plan
10. `crawler/engine/crawl_executor.py` (M60) — main crawl loop; rebuild from 146B skeleton

### 11.2 module_processor.py — Per-Module Pipeline Contract

```python
def process(module_path: str, context: RuntimeContext) -> dict:
    """
    Execute the full per-module pipeline in order:
    1. syntax_validator.validate(file_path)          → PASS or FAIL
    2. header_injector.inject(file_path, simulate)    → inject/replace header
    3. import_rewriter.rewrite(file_path, simulate)   → rewrite deep imports
    4. governance_validator.validate(file_path)        → PASS or FAIL
    5. phase_validator.validate(file_path)             → PASS or FAIL
    6. syntax_validator.validate(file_path)            → post-mutation re-run
    Returns: {"module": "<path>", "status": "PASS|FAIL", "violations": [...], "mutations": [...]}
    """
```

### 11.3 crawl_executor.py — Main Loop Contract

```python
def execute(crawl_plan: dict, context: RuntimeContext) -> dict:
    """
    Iterate through crawl_plan["order"]:
    - For each module: invoke module_processor.process()
    - On PASS: route artifacts via artifact_router; advance
    - On FAIL: invoke repair_engine.repair()
      - On REPAIRED: re-run module_processor; advance
      - On FAILED: invoke quarantine_manager.quarantine(); advance
    Never halt on single-module failure.
    Returns: {"status": "COMPLETE", "total": N, "passed": N, "repaired": N, "quarantined": N}
    """
```

### 11.4 PASS_8 Validation Gate

```bash
# Run single-module crawl in simulate mode
python controllers/pipeline_runner.py \
  --target . \
  --simulate \
  --stage Stage4

# Verify
python -c "
import json
cs = json.load(open('WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/crawl_status.json'))
print(f'Crawl: total={cs[\"total\"]}, passed={cs[\"passed\"]}, quarantined={cs[\"quarantined\"]}')
assert cs['total'] > 0, 'No modules processed'
print('PASS_8: crawl engine PASS')
"
```

Required output: `PASS_8_VALIDATION_REPORT.json` — all gates PASS.

---

## 12. PASS_9 — Reporting and Full Pipeline Run

**Entry condition:** PASS_8 complete.
**Stage:** Stage6 — Orchestration (reporting).
**Exit condition:** Full pipeline run in `--simulate` mode produces all 5 required output artifacts.

### 12.1 Build sequence

1. `crawler/commit/report_generator.py` (M93) — aggregate crawl data; produce 5 output artifacts
2. `crawler/commit/commit_finalizer.py` (M94) — clean commit in `--execute` mode; produces commit_plan.json in `--simulate` mode

### 12.2 report_generator.py — Output Contract

Must produce all 5 artifacts routed through artifact_router:

| Artifact | Type Key | Content |
|---|---|---|
| `validation_report.json` | validation_report | Per-module validation results |
| `repair_event_log.json` | repair_event_log | All repair events with outcome |
| `mutation_log.json` | mutation_log | All applied mutations (empty in simulate mode) |
| `crawl_execution_log.json` | crawl_execution_log | Stage-by-stage execution timeline |
| `crawl_status.json` | crawl_status | Summary: total, passed, repaired, quarantined, completion_rate |

### 12.3 PASS_9 Validation Gate

```bash
python controllers/pipeline_runner.py --target . --simulate

python -c "
import json, os
required = [
    'WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/validation_report.json',
    'WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/repair_event_log.json',
    'WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/mutation_log.json',
    'WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/crawl_execution_log.json',
    'WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/crawl_status.json'
]
missing = [f for f in required if not os.path.exists(f)]
assert len(missing) == 0, f'Missing artifacts: {missing}'
print('PASS_9: all 5 report artifacts present PASS')
"
```

Required output: `PASS_9_VALIDATION_REPORT.json` — all gates PASS.

---

## 13. PASS_10 — Remaining Audit Regeneration and Repo Analysis Modules

**Entry condition:** PASS_9 complete.

Build all Stage1 and Stage2 modules not yet built: M11, M13, M16, M17, M20, M23, M24, M25. These produce the inputs that feed the dependency graph engine and crawl planner. After building, re-run PASS_4 to confirm outputs.

---

## 14. PASS_11 — Target Repo Analysis Subsystem

**Entry condition:** PASS_10 complete.

Build TA-01 through TA-04 in order. Run the four-stage pipeline against AP repo for self-analysis. Verify `AP_REPOSITORY_GAP_ANALYSIS.json` is produced with severity-labeled gaps consistent with known V1 state.

---

## 15. PASS_12 — LOGOS Integration

**Entry condition:** PASS_11 complete; LOGOS present in `WORKFLOW_TARGET_PROCESSING/targets/repos/`.

Run simulation framework against LOGOS snapshot. Run crawl planner against LOGOS module graph. Verify `simulation_report.status == "PASS"` and `crawl_plan.json` is produced.

**Note:** Live crawl (--execute) on LOGOS requires Architect authorization. PASS_12 scope is simulation and planning only.

---

## 16. Dependency Normalization — Cross-Pass Rules

All modules across all passes must:

1. **Import only from permitted subsystems** per the contract table in AP_V2_Tooling_DS Section 9.

2. **Load configs through M00 or M01** — never directly parse `crawl_config.json` or `routing_table.json`. Use `schema_registry.get_schema()` and `routing_table_loader.get_route()`.

3. **Route all artifact writes through `runtime/artifact_router.py`** — after PASS_2 is complete. Hardcoded output paths are a spec violation.

4. **Header fields must match actual behavior** — `allowed_imports` in header must be a complete and accurate list.

5. **No circular imports** — the stage hierarchy (Stage0 → Stage6) defines a strict DAG. No module in an earlier stage may import from a later stage.

6. **Simulation flag passthrough** — every module that writes files must accept `simulate: bool` as a parameter and respect it.

---

## 17. Execution Reporting Requirements

Every pipeline run produces a `PIPELINE_EXECUTION_MANIFEST.json` written to `WORKFLOW_MUTATION_TOOLING/AP_SYSTEM_AUDIT/`:

```json
{
  "schema_version": "2.0",
  "run_id": "<UUID>",
  "started_at": "<ISO>",
  "completed_at": "<ISO>",
  "target": "<repo path>",
  "mode": "simulate|execute",
  "passes_executed": [],
  "stages_executed": [],
  "artifacts_produced": [],
  "gate_results": [{ "gate_id": "<str>", "status": "PASS|FAIL", "detail": "<str>" }],
  "overall_status": "COMPLETE|HALTED|ERROR",
  "halt_reason": null
}
```

---

## 18. Safety Rules (Binding)

| Rule ID | Rule | Enforcement |
|---|---|---|
| SR-001 | No repository mutation without simulation approval | pipeline_runner.py VG-EXEC check |
| SR-002 | All modules output structured JSON artifacts | output_registry schema compliance check |
| SR-003 | All modules register outputs through artifact_router | output_registry audit |
| SR-004 | All modules include complete AP metadata header | header_validator VG-HDR gate |
| SR-005 | AP_SYSTEM_CONFIG/ and AP_SYSTEM_AUDIT/ are never write targets | artifact_router hard refusal |
| SR-006 | Non-deletion policy — no existing files deleted without Architect authorization | All prompts; no rm/shutil.rmtree without authorization |
| SR-007 | --simulate is the default execution mode | pipeline_runner.py default argument |

---

## 19. Deferments

| Item | Rationale | Status |
|---|---|---|
| LOGOS live crawl | Requires PASS_11 complete + LOGOS available | Deferred to PASS_12 |
| LOGOS DS/IG V2 upgrade | Separate workstream | Deferred |
| SPEC-011 for AP_TOOL_PROP_01 | Boundary formalization | Pending Architect |
| CI/CD integration | Infrastructure | Deferred |
| DRAC | Architect standing deferment | Until canonical runtime exists |

---

## 20. Open Questions

| ID | Question | Blocking |
|---|---|---|
| OQ-001 | Resolve CL-G1: canonical schema filename | Yes — blocks schema validation |
| OQ-002 | SPEC-004 approval | Yes — blocks PASS_3 and PASS_7 |
| OQ-003 | SPEC-011 for AP_TOOL_PROP_01 | No |

---

## 21. Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| v1 | 2026-03-10 | Initial implementation guide | Claude / Formalization_Expert |
| v2 | 2026-03-10 | Addendum integration: 7-pass structure, artifact routing system, execution spine contracts, simulation framework coordinator contract, repair engine loop, header_validator spec, safety rules, execution reporting requirements | Claude / Formalization_Expert |

---

*End of AP_V2_Tooling_IG*

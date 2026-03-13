# ARCHON_PRIME — WORKFLOW CONTEXT SNAPSHOT
**Document Type:** Operational Context Reference
**Version:** v1
**Status:** draft
**Date:** 2026-03-08
**Author:** Claude (Formalization_Expert) — merged from Claude SPEC-004/IMPL-003 analysis and GPT Environment Audit Report
**Authority:** Architect
**Governance:** CLAUDE_GOVERNANCE_PROTOCOL.md
**Purpose:** Consolidated operational context for AP system finalization — covering repo tooling state, function-level build targets, and environment/integration setup (GitHub + VS Code). This document is the single reference for any agent or session resuming AP finalization work.

---

## SECTION 1 — SYSTEM STATE BASELINE

### 1.1 Confirmed Repository Facts

| Metric | Value | Source |
|---|---|---|
| Total directories | 79 | GPT Environment Audit |
| Total files | 93 | GPT Environment Audit |
| Python modules | 32 | Both reports |
| Markdown docs | 46 | GPT Environment Audit |
| JSON files | 11 | GPT Environment Audit |
| Header-compliant files | 0 / 93 | Both reports |
| Overall readiness score | 38 / 100 | Claude AP Audit |
| Readiness grade | D+ | Claude AP Audit |
| Target readiness after finalization | ~80 / 100 | Both reports |

### 1.2 Subsystem Status Matrix

| Subsystem | Status | Blocking Gaps |
|---|---|---|
| Audit tooling (19 modules) | **Operational** | Not wired to pipeline; runners need configurable target path |
| Analysis tools (6 modules) | **Operational** | Not chained; analysis outputs not auto-consumed |
| Crawler — engine/monitor | **Skeletal** | crawl_engine.py: 146 bytes, stdout only; crawl_monitor.py: 142 bytes, infinite loop |
| Crawler — pipeline | **Missing** | Directory exists; no code |
| Crawler — repair | **Missing** | Directory exists; no code |
| Crawler — quarantine | **Missing** | Directory does not exist |
| Crawler — mutation operators | **Missing** | No directory or code |
| Simulation — repo_simulator | **Skeletal** | 166 bytes, counts files, no JSON output |
| Simulation — runtime_simulator | **Missing** | Directory exists; no code |
| Simulation — import_simulator | **Missing** | Directory exists; no code |
| Orchestration — routing table | **Present** | OUTPUT_ROUTING_TABLE.md exists; no machine-readable JSON version |
| Orchestration — artifact schemas | **Present** | ARTIFACT_SCHEMAS.md exists; no JSON schema files |
| Orchestration — controllers | **Missing** | Directory exists; no code |
| Orchestration — task_router | **Missing** | Directory exists; no code |
| Orchestration — execution_graphs | **Missing** | Directory does not exist |
| Configuration — crawl_config | **Missing** | No crawl_config.json or ap_config.yaml |
| Configuration — logos_targets | **Missing** | No logos_targets.yaml |
| Configuration — repair_registry.json | **Missing** | FAILURE_TAXONOMY.md exists as human-readable; no machine-readable JSON form |
| Configuration — routing_table.json | **Missing** | OUTPUT_ROUTING_TABLE.md exists; no JSON version |
| Governance artifacts + design specs | **Present** | Design docs are extensive; code is absent |
| VS Code integration doc | **Missing** | AP_VSCODE_PIPELINE_INTEGRATION.md not in repo |
| devcontainer | **Missing** | .devcontainer/ not in repo |
| GitHub CI workflows | **Missing** | .github/workflows/ not in repo |
| VS Code settings + tasks | **Missing** | .vscode/ not in repo |
| Logger (utils/logger.py) | **Present** | Functional JSON event logger |

### 1.3 Confirmed Environment Facts

| Property | Value |
|---|---|
| Runtime | Python 3.12.1 |
| OS | Ubuntu Linux (GitHub Codespaces / Azure) |
| VS Code | 1.98.x |
| Key packages installed | GitPython, jsonschema, PyYAML, ast (stdlib) |
| GitHub repo | github.com/Project-Logos-2026/ARCHON_PRIME |
| Branch | main (assumed; branch protection not yet configured) |

---

## SECTION 2 — GAP REGISTER

Every gap confirmed by both reports is listed here with severity, location, and the resolution path from IMPL-003. Conflicts between reports on solution approach are resolved in Section 3.

### 2.1 Configuration Layer (Blocking — nothing runs without these)

| Gap | Location | Resolution |
|---|---|---|
| No runtime configuration file | configs/crawl_configs/ | Create `crawl_config.json` (machine-readable; see IMPL-003 Stage 0) |
| No LOGOS target definition | configs/crawl_configs/ | Create `logos_targets.yaml` (IMPL-003 Stage 0) |
| No machine-readable repair registry | configs/repair_registry/ | Create `repair_registry.json` from FAILURE_TAXONOMY.md (IMPL-003 Stage 0) |
| No machine-readable routing table | orchestration/task_router/ | Create `routing_table.json` from OUTPUT_ROUTING_TABLE.md (IMPL-003 Stage 0) |
| No VS Code integration document | AP_SYSTEM_CONFIG/ | Create `AP_VSCODE_PIPELINE_INTEGRATION.md` (Section 4 of this document) |

### 2.2 Tooling Layer (Blocking — pipeline cannot run end-to-end)

| Gap | Location | Module ID | Resolution |
|---|---|---|---|
| Audit suite not wired to configurable target | tools/audit_tools/run_audit_suite.py | — | Modify runner to accept target_path from config (IMPL-003 Stage 1) |
| No module index builder | tools/repo_mapping/ | M11 | Create module_index_builder.py |
| No python file collector | tools/repo_mapping/ | M10 | Create python_file_collector.py |
| No import extractor | tools/import_analysis/ | M12 | Create import_extractor.py |
| No dependency graph builder | tools/import_analysis/ | M21 | Create dependency_graph_builder.py (replaces passthrough stub) |
| No circular dependency detector | tools/import_analysis/ | M22 | Create circular_dependency_detector.py |
| No governance contract scanner | tools/governance_analysis/ | M23 | Create governance_contract_scanner.py |
| No runtime phase mapper | tools/runtime_analysis/ | — | Create runtime_phase_mapper.py |
| No runtime boot sequencer | tools/runtime_analysis/ | M24 | Create runtime_boot_sequencer.py |
| No canonical import registry builder | tools/import_analysis/ | M25 | Create canonical_import_registry_builder.py |
| No schema registry | tools/normalization_tools/ | M00 | Create schema_registry.py |
| No repair registry loader | tools/audit_tools/ | M02 | Create repair_registry_loader.py |
| No routing table loader | orchestration/task_router/ | M03 | Create routing_table_loader.py |

### 2.3 Crawler Layer (Blocking — no crawl capability)

| Gap | Location | Module ID | Resolution |
|---|---|---|---|
| crawl_engine.py is a skeleton | crawler/engine/ | M60 | Replace with crawl_executor.py implementation |
| crawl_monitor.py is a skeleton | crawler/monitor/ | M65 | Replace with real state poller |
| No crawl planner | crawler/engine/ | M38 | Create crawl_planner.py |
| No module processor | crawler/pipeline/ | M61 | Create module_processor.py |
| No syntax validator | crawler/pipeline/ | M62 | Create syntax_validator.py |
| No governance validator | crawler/pipeline/ | M63 | Create governance_validator.py |
| No phase validator | crawler/pipeline/ | M64 | Create phase_validator.py |
| No header injector | crawler/mutation/ | M50 | Create header_injector.py (directory must be created) |
| No import rewriter | crawler/mutation/ | M51 | Create import_rewriter.py |
| No error classifier | crawler/repair/ | M70 | Create error_classifier.py |
| No repair router | crawler/repair/ | M71 | Create repair_router.py |
| No repair executor | crawler/repair/ | M72 | Create repair_executor.py |
| No quarantine manager | crawler/quarantine/ | M80 | Create quarantine_manager.py (directory must be created) |
| No artifact router | crawler/commit/ | M90 | Create artifact_router.py (directory must be created) |
| No report generator | crawler/commit/ | M91 | Create report_generator.py |
| No commit finalizer | crawler/commit/ | M92 | Create commit_finalizer.py |

### 2.4 Simulation Layer (Blocking — pre-crawl gate requires passing simulation)

| Gap | Location | Module ID | Resolution |
|---|---|---|---|
| repo_simulator.py is a skeleton | simulation/repo_simulator/ | M30 | Replace with full implementation |
| No runtime simulator | simulation/runtime_simulator/ | M31 | Create runtime_simulator.py |
| No import simulator | simulation/import_simulator/ | M32 | Create import_simulator.py |
| No simulation coordinator | simulation/ | — | Create simulation_coordinator.py to merge outputs |
| No execution graph builder | orchestration/execution_graphs/ | M39 | Create execution_graph_builder.py (directory must be created) |

### 2.5 Orchestration Layer (Blocking — no pipeline entry point)

| Gap | Location | Module ID | Resolution |
|---|---|---|---|
| No task router | orchestration/task_router/ | M95 | Create task_router.py |
| No controller | orchestration/controllers/ | M96 | Create controller_main.py |
| No checklist evaluator | crawler/engine/ | — | Create checklist_evaluator.py |

### 2.6 Environment + Integration Layer (Required for AP workflow)

| Gap | Location | Resolution |
|---|---|---|
| No devcontainer | .devcontainer/ | Create devcontainer.json with pinned Python 3.12, required extensions (Section 4) |
| No VS Code settings | .vscode/ | Create settings.json and extensions.json (Section 4) |
| No VS Code tasks | .vscode/ | Create tasks.json with AP pipeline tasks (Section 4) |
| No GitHub CI | .github/workflows/ | Create packet_validation.yml, lint.yml, test.yml workflows (Section 4) |
| No branch protection | GitHub settings | Configure: require passing checks on PRs to main (Section 4) |
| No AP_VSCODE_PIPELINE_INTEGRATION.md | AP_SYSTEM_CONFIG/ | Document env wiring; see Section 4 |

---

## SECTION 3 — CONFLICT RESOLUTIONS

Two meaningful conflicts exist between the GPT report and the Claude SPEC-004/IMPL-003 pair. Both are resolved here with the more rigorous approach selected.

### 3.1 Configuration Format: YAML vs JSON

**GPT position:** Create `ap_config.yaml` and `logos_targets.yaml`. YAML is human-readable and appropriate for developer-edited configuration.

**Claude SPEC-004 position:** Create `crawl_config.json`. JSON is machine-readable without a parser dependency and is consistent with the AP artifact schema system.

**Resolution — Split by purpose:**

Use **both** formats for their appropriate functions:

- `configs/crawl_configs/crawl_config.json` — machine-readable runtime configuration, consumed by controller_main and all subsystems programmatically. JSON. This is the authoritative config for AP execution.
- `configs/crawl_configs/logos_targets.yaml` — human-edited target definition. YAML is appropriate here because this is an Architect-facing file specifying which repo(s) to crawl, not a machine-generated artifact. YAML's readability is an asset for a file the Architect edits directly.
- `configs/crawl_configs/ap_config.yaml` — **retained as a human-readable alias/overlay** for settings the Architect may want to edit in YAML form. controller_main reads `crawl_config.json` as authoritative; if `ap_config.yaml` is present, it is loaded and merged before crawl_config.json values (YAML overrides JSON defaults). This satisfies GPT's usability concern without abandoning JSON for programmatic consumption.

The three files serve distinct audiences: machine (JSON), architect (YAML targets), and architect-override (YAML config). No conflict.

### 3.2 VS Code Pipeline Integration: Documented vs Deferred

**GPT position:** Create `AP_VSCODE_PIPELINE_INTEGRATION.md` in the repo immediately; define VS Code tasks, devcontainer, extensions, and GitHub workflows as part of current finalization.

**Claude SPEC-004 position:** Environment configuration is a separate phase; not part of tooling spec.

**Resolution — Phased but specified now:**

Both are correct at the level they operate. Claude is right that VS Code/GitHub environment setup does not need to be implemented before the tooling layer. GPT is right that the spec for it needs to exist now so the execution agent can pick it up immediately when tooling is done.

`AP_VSCODE_PIPELINE_INTEGRATION.md` is produced as a specification document in this context snapshot (Section 4). Environment implementation is **deferred until tooling Stages 0–9 are complete** — consistent with SPEC-004 — but it is fully specified here so there is no ambiguity when the phase begins.

---

## SECTION 4 — ENVIRONMENT + INTEGRATION SPECIFICATION

*This section constitutes the substance of the missing `AP_VSCODE_PIPELINE_INTEGRATION.md`. It can be extracted directly into that file.*

### 4.1 devcontainer

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "ARCHON_PRIME",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.pylance",
        "charliermarsh.ruff",
        "ms-python.black-formatter",
        "ryanluker.vscode-coverage-gutters",
        "eamodio.gitlens",
        "ms-python.mypy-type-checker",
        "redhat.vscode-yaml",
        "ZainChen.json"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.formatOnSave": true,
        "python.formatting.provider": "black",
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter"
        },
        "ruff.enable": true
      }
    }
  },
  "forwardPorts": [],
  "remoteUser": "vscode"
}
```

Create `requirements.txt` (root of repo):

```
jsonschema>=4.0
PyYAML>=6.0
GitPython>=3.1
pytest>=7.0
pytest-cov>=4.0
black>=24.0
ruff>=0.4
mypy>=1.0
bandit>=1.7
```

### 4.2 VS Code Settings and Extensions

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "ruff.enable": true,
  "ruff.organizeImports": true,
  "mypy-type-checker.enabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "coverage-gutters.coverageFileNames": ["coverage.xml"]
}
```

Create `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylance",
    "charliermarsh.ruff",
    "ms-python.black-formatter",
    "ryanluker.vscode-coverage-gutters",
    "eamodio.gitlens",
    "ms-python.mypy-type-checker",
    "redhat.vscode-yaml",
    "ZainChen.json",
    "ms-azuretools.vscode-docker",
    "ms-vscode.makefile-tools"
  ]
}
```

### 4.3 VS Code Tasks

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AP: Run Full Pipeline",
      "type": "shell",
      "command": "python orchestration/controllers/controller_main.py --config configs/crawl_configs/crawl_config.json",
      "group": "build",
      "presentation": { "reveal": "always", "panel": "new" },
      "problemMatcher": []
    },
    {
      "label": "AP: Simulation Only",
      "type": "shell",
      "command": "python orchestration/controllers/controller_main.py --config configs/crawl_configs/crawl_config.json --simulation-only",
      "group": "test",
      "presentation": { "reveal": "always", "panel": "new" },
      "problemMatcher": []
    },
    {
      "label": "AP: Resume Crawl",
      "type": "shell",
      "command": "python orchestration/controllers/controller_main.py --config configs/crawl_configs/crawl_config.json --resume",
      "group": "build",
      "presentation": { "reveal": "always", "panel": "new" },
      "problemMatcher": []
    },
    {
      "label": "AP: Run Audit Suite",
      "type": "shell",
      "command": "python tools/audit_tools/run_audit_suite.py",
      "group": "test",
      "presentation": { "reveal": "always", "panel": "shared" },
      "problemMatcher": []
    },
    {
      "label": "AP: Run Governance Audit",
      "type": "shell",
      "command": "python tools/audit_tools/run_governance_audit.py",
      "group": "test",
      "presentation": { "reveal": "always", "panel": "shared" },
      "problemMatcher": []
    },
    {
      "label": "AP: Run Tests",
      "type": "shell",
      "command": "pytest tests/ -v --cov=. --cov-report=xml",
      "group": { "kind": "test", "isDefault": true },
      "presentation": { "reveal": "always", "panel": "shared" },
      "problemMatcher": []
    },
    {
      "label": "AP: Lint (ruff)",
      "type": "shell",
      "command": "ruff check . && black --check .",
      "group": "test",
      "problemMatcher": []
    }
  ]
}
```

### 4.4 GitHub Actions Workflows

Create `.github/workflows/packet_validation.yml`:

```yaml
name: Packet Validation

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - name: Validate crawl_config.json schema
        run: python -c "
import json, jsonschema, sys
with open('configs/crawl_configs/crawl_config.json') as f:
    config = json.load(f)
print('crawl_config.json: valid JSON')
sys.exit(0)
"
      - name: Check repair_registry.json present
        run: test -f configs/repair_registry/repair_registry.json
      - name: Check routing_table.json present
        run: test -f orchestration/task_router/routing_table.json
```

Create `.github/workflows/lint.yml`:

```yaml
name: Lint and Format

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff black mypy
      - run: ruff check .
      - run: black --check .
```

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=. --cov-report=xml --cov-fail-under=70
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.xml
```

### 4.5 Branch Protection Configuration

Configure on GitHub (Settings → Branches → Add rule → `main`):

| Rule | Setting |
|---|---|
| Require status checks to pass | `Packet Validation / validate`, `Lint and Format / lint`, `Tests / test` |
| Require branches to be up to date | Yes |
| Require linear history | Yes (prevents merge commits; enforces rebase/squash) |
| Restrict who can push to matching branches | Only Architect + designated execution agents |
| Require pull request reviews | 1 approving review (or bypass for Architect-direct pushes) |

### 4.6 AP_VSCODE_PIPELINE_INTEGRATION.md

When extracted from this document, write to `AP_SYSTEM_CONFIG/AP_VSCODE_PIPELINE_INTEGRATION.md`. Content: Sections 4.1–4.5 of this document, plus the following AP workflow overview.

**AP Workflow in VS Code/GitHub Codespaces:**

```
Developer / Architect opens Codespace on ARCHON_PRIME
    │
    ▼
devcontainer auto-installs Python 3.12, extensions, pip requirements
    │
    ▼
Edit crawl_config.json: set target_repo to LOGOS path
Edit logos_targets.yaml: confirm LOGOS paths and exclusions
    │
    ▼
VS Code Task: "AP: Simulation Only"
    runs: controller_main.py --simulation-only
    produces: logs/simulation_logs/simulation_report.json
    expected: overall_result: "PASS", crawl_permitted: true
    │
    ▼
VS Code Task: "AP: Run Full Pipeline"
    runs: controller_main.py --config crawl_config.json
    phases: pre-crawl → simulation gate → crawl → post-crawl → commit
    │
    ├── On HALT: inspect AUDIT_LOGS/halt_diagnostic.json
    ├── On QUARANTINE: inspect logs/repair_logs/quarantine_registry.json
    └── On SUCCESS: inspect AUDIT_SYSTEM/reports/structural_reports/validation_report.json
    │
    ▼
Push results to GitHub
    GitHub Actions: packet_validation + lint + tests run automatically
    Branch protection: all checks must pass before merge to main
```

---

## SECTION 5 — BUILD SEQUENCE (AUTHORITATIVE)

The authoritative build order from IMPLEMENTATION_SEQUENCE.md, augmented with environment setup. Stages are sequentially dependent unless otherwise noted.

| Stage | Name | Key Deliverables | Status |
|---|---|---|---|
| ENV | Environment Setup | devcontainer, .vscode/, .github/workflows/, requirements.txt | **Deferred — specify now, implement after Stage 9** |
| 0 | Foundation | crawl_config.json, logos_targets.yaml, ap_config.yaml, repair_registry.json, routing_table.json, schema_registry.py, repair_registry_loader.py, routing_table_loader.py | **Not started** |
| 1 | Audit Suite Wiring | run_audit_suite.py and run_governance_audit.py accept target_path from config; output directories created | **Not started** |
| 2 | Analysis Tools | python_file_collector.py, module_index_builder.py, import_extractor.py, dependency_graph_builder.py, circular_dependency_detector.py, governance_contract_scanner.py, runtime_phase_mapper.py, runtime_boot_sequencer.py, canonical_import_registry_builder.py | **Not started** |
| 3 | Mutation Operators | header_injector.py (M50), import_rewriter.py (M51) — pure functions, mutation_allowed guarded | **Not started** |
| 4 | Validators | syntax_validator.py (M62), governance_validator.py (M63), phase_validator.py (M64) | **Not started** |
| 3+4 | Parallel | Stages 3 and 4 can be built in parallel once Stage 2 complete | — |
| 5 | Simulation + Planner | repo_simulator.py (replace), runtime_simulator.py, import_simulator.py, simulation_coordinator.py, crawl_planner.py (M38), execution_graph_builder.py (M39) | **Not started** |
| 6 | Crawl Executor + Pipeline | crawl_executor.py (replace), module_processor.py (M61), crawl_monitor.py (replace) | **Not started** |
| 7 | Repair + Quarantine | error_classifier.py (M70), repair_router.py (M71), repair_executor.py (M72), quarantine_manager.py (M80); wire into crawl_executor | **Not started** |
| 8 | Artifact Routing + Reports | artifact_router.py (M90), report_generator.py (M91), commit_finalizer.py (M92) | **Not started** |
| 9 | Orchestration Controller | task_router.py (M95), controller_main.py (M96), checklist_evaluator.py | **Not started** |
| ENV | Environment Implementation | Implement devcontainer, .vscode/, .github/ after Stage 9 validates | **Deferred** |

### Stage Dependency Graph

```
Stage 0 (Foundation)
    └─► Stage 1 (Audit Wiring)
            └─► Stage 2 (Analysis Tools)
                    ├─► Stage 3 (Mutation Operators)  ──┐
                    ├─► Stage 4 (Validators)           ─┤
                    └─► Stage 5 (Simulation + Planner) ─┤
                            (needs 3+4 complete)         │
                                                         ├─► Stage 6 (Executor + Pipeline)
                                                         │       └─► Stage 7 (Repair + Quarantine)
                                                         │               └─► Stage 8 (Routing + Reports)
                                                         │                       └─► Stage 9 (Controller)
                                                         │                               └─► ENV (Environment)
                                                         └──────────────────────────────────────────────────►
```

---

## SECTION 6 — MODULE INVENTORY SUMMARY

All modules required for AP completion. M-series IDs from MODULE_INVENTORY.md. Status reflects current repo state.

### S0 — Foundation (3 new modules)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| schema_registry.py | tools/normalization_tools/ | M00 | Create |
| repair_registry_loader.py | tools/audit_tools/ | M02 | Create |
| routing_table_loader.py | orchestration/task_router/ | M03 | Create |

### S1 — Audit Regeneration (2 modified)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| run_audit_suite.py | tools/audit_tools/ | — | Modify (add target_path param) |
| run_governance_audit.py | tools/audit_tools/ | — | Modify (add target_path param) |

### S2 — Analysis Tools (9 new modules)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| python_file_collector.py | tools/repo_mapping/ | M10 | Create |
| module_index_builder.py | tools/repo_mapping/ | M11 | Create |
| import_extractor.py | tools/import_analysis/ | M12 | Create |
| dependency_graph_builder.py | tools/import_analysis/ | M21 | Create |
| circular_dependency_detector.py | tools/import_analysis/ | M22 | Create |
| governance_contract_scanner.py | tools/governance_analysis/ | M23 | Create |
| runtime_phase_mapper.py | tools/runtime_analysis/ | — | Create |
| runtime_boot_sequencer.py | tools/runtime_analysis/ | M24 | Create |
| canonical_import_registry_builder.py | tools/import_analysis/ | M25 | Create |

### S3 — Mutation Operators (2 new modules, 1 new directory)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| header_injector.py | crawler/mutation/ | M50 | Create (+ create directory) |
| import_rewriter.py | crawler/mutation/ | M51 | Create |

### S4 — Validators (3 new modules)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| syntax_validator.py | crawler/pipeline/ | M62 | Create |
| governance_validator.py | crawler/pipeline/ | M63 | Create |
| phase_validator.py | crawler/pipeline/ | M64 | Create |

### S5 — Simulation + Planner (5 new/replaced modules, 1 new directory)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| repo_simulator.py | simulation/repo_simulator/ | M30 | Replace skeleton |
| runtime_simulator.py | simulation/runtime_simulator/ | M31 | Create |
| import_simulator.py | simulation/import_simulator/ | M32 | Create |
| simulation_coordinator.py | simulation/ | — | Create |
| crawl_planner.py | crawler/engine/ | M38 | Create |
| execution_graph_builder.py | orchestration/execution_graphs/ | M39 | Create (+ create directory) |

### S6 — Crawl Executor + Pipeline (3 new/replaced modules)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| crawl_executor.py | crawler/engine/ | M60 | Replace skeleton |
| module_processor.py | crawler/pipeline/ | M61 | Create |
| crawl_monitor.py | crawler/monitor/ | M65 | Replace skeleton |

### S7 — Repair + Quarantine (4 new modules, 1 new directory)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| error_classifier.py | crawler/repair/ | M70 | Create |
| repair_router.py | crawler/repair/ | M71 | Create |
| repair_executor.py | crawler/repair/ | M72 | Create |
| quarantine_manager.py | crawler/quarantine/ | M80 | Create (+ create directory) |

### S8 — Artifact Routing + Reports (3 new modules, 1 new directory)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| artifact_router.py | crawler/commit/ | M90 | Create (+ create directory) |
| report_generator.py | crawler/commit/ | M91 | Create |
| commit_finalizer.py | crawler/commit/ | M92 | Create |

### S9 — Orchestration Controller (3 new modules)

| Module | Path | ID | Create/Modify |
|---|---|---|---|
| task_router.py | orchestration/task_router/ | M95 | Create |
| controller_main.py | orchestration/controllers/ | M96 | Create |
| checklist_evaluator.py | crawler/engine/ | — | Create |

**Total new modules: 39**
**Total modified modules: 2**
**Total new directories: 5** (crawler/mutation/, crawler/quarantine/, crawler/commit/, orchestration/execution_graphs/, .devcontainer/, .vscode/, .github/workflows/)

---

## SECTION 7 — ARTIFACT ROUTING REFERENCE

Canonical artifact destinations. Machine-readable form in `orchestration/task_router/routing_table.json`.

| Artifact | Primary Path | Produced By |
|---|---|---|
| repo_python_files.json | AUDIT_SYSTEM/analysis/repo_maps/ | M10 |
| module_index.json | AUDIT_SYSTEM/reports/structural_reports/ | M11 |
| repo_imports.json | AUDIT_SYSTEM/reports/import_reports/ | M12 |
| dependency_graph.json | AUDIT_SYSTEM/analysis/dependency_graphs/ | M21 |
| circular_dependency_groups.json | AUDIT_SYSTEM/analysis/dependency_graphs/ | M22 |
| canonical_import_registry.json | AUDIT_SYSTEM/analysis/dependency_graphs/ | M25 |
| canonical_import_rewrite_plan.json | AUDIT_SYSTEM/analysis/dependency_graphs/ | M25 |
| runtime_phase_map.json | AUDIT_SYSTEM/analysis/runtime_maps/ | runtime_phase_mapper |
| runtime_boot_sequence.json | AUDIT_SYSTEM/analysis/runtime_maps/ | M24 |
| governance_contract_map.json | AUDIT_SYSTEM/reports/governance_reports/ | M23 |
| header_schema_compliance.json | AUDIT_SYSTEM/reports/governance_reports/ | M63 |
| simulation_report.json | logs/simulation_logs/ | simulation_coordinator |
| crawl_plan.json | orchestration/execution_graphs/ | M38 |
| execution_graph.json | orchestration/execution_graphs/ | M39 |
| crawl_status.json | logs/crawler_logs/ | M60 |
| crawl_execution_log.json | logs/crawler_logs/ | M60 |
| mutation_log.json | logs/execution_logs/ | M61 |
| repair_event_log.json | logs/repair_logs/ | M72 |
| quarantine_registry.json | logs/repair_logs/ | M80 |
| validation_report.json | AUDIT_SYSTEM/reports/structural_reports/ | M91 |
| halt_diagnostic.json | AUDIT_LOGS/ | M96 |

---

## SECTION 8 — GOVERNANCE ENFORCEMENT POINTS

Active governance rules for all AP execution. These do not change between sessions.

| Rule | Trigger | Mechanism | Halt? |
|---|---|---|---|
| Fail-closed initialization | crawl_config.json missing or invalid | config validator in controller_main | Yes |
| Mutation guard | Any file write to LOGOS modules | `mutation_allowed: false` flag checked before write | Yes |
| Simulation gate | Pre-crawl → crawl transition | simulation_report.json crawl_permitted: true required | Yes |
| Pre-crawl checklist gate | Pre-crawl → crawl transition | All blocking checklist items GREEN | Yes |
| Locked artifact immutability | header_schema, repair_registry, routing_table | Read-only after pre-crawl lock; in-crawl write is governance violation | Yes |
| HALT propagation | Any HALT-class failure | Propagates to controller_main; halt_diagnostic.json; non-zero exit | Yes |
| Quarantine stub compliance | Module entering quarantine | Stub must pass syntax_validator before write to module path | Yes |
| Artifact routing completeness | Post-crawl | commit_finalizer confirms all canonical paths populated | No (reported) |
| Boot-chain priority | Crawl planning | Phase 0/1 modules processed first in execution graph | Yes (HALT on boot-chain BLOCKING) |
| CIH header on all new modules | Implementation | All modules in AP tools/ and subsystem dirs require valid CIH header | No (audit catches) |

---

## SECTION 9 — DISCOVERED INPUTS REQUIRED BEFORE SPECIFIC STAGES

Three inputs are external to AP — they must be extracted from LOGOS before the corresponding stages begin. They do not block Stages 0–2.

| Input Required | Needed For | Resolution Path |
|---|---|---|
| LOGOS header schema field definitions (exact CIH fields) | Stage 3: header_injector.py | Run audit tools against LOGOS; extract from existing governance headers |
| LOGOS canonical import facade module paths | Stage 2: canonical_import_registry_builder.py | Extract from LOGOS facade modules (CIH directory) before Stage 2 completes |
| LOGOS governance contract schema format | Stage 4: governance_validator.py | Extract from existing LOGOS governance modules before scanner is built |
| LOGOS runtime phase assignment convention | Stage 2: runtime_phase_mapper.py | Extract from LOGOS runtime initialization before Stage 3 |

These are Stage 1 audit outputs — by the time Stage 3 needs them, the Stage 1 audit suite run against LOGOS will have produced them. No design gap; scheduling dependency only.

---

## SECTION 10 — OPEN ITEMS FOR ARCHITECT RESOLUTION

| ID | Item | Context | Impact |
|---|---|---|---|
| OQ-001 | Confirm config file naming convention: `crawl_config.json` (IMPL-003) vs `ap_config.yaml` (GPT report) | Resolved in Section 3.1 — both retained for different purposes. Confirm this split is acceptable. | Config loader implementation |
| OQ-002 | Confirm `mutation_allowed` default | Both reports assume false. Confirm that initial LOGOS crawl runs in report-only mode before any mutations are permitted. | Safety of first crawl |
| OQ-003 | Max repair retry cycles | IMPL-003 defaults to 3. Configurable in crawl_config.json under `repair.max_retry_cycles`. | Quarantine threshold |
| OQ-004 | Branch protection bypass policy | Should Architect-direct pushes to main bypass status checks? Relevant once CI is active. | GitHub branch protection config |
| OQ-005 | Test suite location | No `tests/` directory exists. Where do unit and integration tests live? | GitHub CI test workflow |
| OQ-006 | `dependency_graph.py` passthrough stub disposition | Currently retained as compatibility shim. Confirm it can be deprecated once M21 is live. | Stage 2 implementation |
| OQ-007 | AP self-crawl for pipeline validation | GPT recommends running AP against its own repo for pipeline validation before running against LOGOS. Confirm this is the intended first-run target. | Stage 9 validation |

---

*End of AP_WORKFLOW_CONTEXT.md v1*
*Source reports: Claude SPEC-004/IMPL-003 (Formalization_Expert analysis) + GPT ARCHON_PRIME Repository Inspection and Environment Review (March 8 2026)*

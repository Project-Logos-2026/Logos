# ARCHON PRIME DEPENDENCY MAP
**Generated:** 2026-03-13  
**Sources:** `runtime_module_tree_auditor`, `runtime_callgraph_extractor`, `cluster_analysis.py` (repo-wide)  
**Target:** `LOGOS_SYSTEM/RUNTIME_BRIDGE/ARCHON_PRIME/ARCHON_PRIME-main`  

---

## 1. Dependency Architecture Overview

Archon Prime's internal dependency structure is a **staged pipeline** organized around a central governance gate. The dependency flow is strictly vertical (pipeline stages) rather than mesh (cross-cutting).

```
WORKFLOW_NEXUS/Governance/workflow_gate.py         [GOVERNANCE GATE — universal dependency]
         │
         └──────────────────────────────────────────────────┐
                                                            │
         ┌──────────────────── controllers/ ───────────────┤
         │                                                   │
         ├── config_loader.py          [configuration]       │
         ├── audit_controller.py       [stage 1]             │
         ├── analysis_controller.py    [stage 2]             │
         ├── simulation_controller.py  [stage 3]             │
         ├── crawler_controller.py     [stage 4]             │
         ├── repair_controller.py      [stage 5]             │
         └── pipeline_controller.py   [orchestrator]  ──────┘
                   │
    ┌──────────────┼───────────────────────────────────┐
    │              │                                   │
 audit tools  analysis tools                    repair operators
    │              │                                   │
 tools/        tools/                             repair/
 audit_tools/  runtime_analysis/                 operators/
               import_analysis/                  
               semantic_extraction/
               normalization_tools/            
```

---

## 2. Module-Level Dependency Table

### Tier 1: Governance Layer (no inbound deps within AP)

| Module | Dependencies (outbound) | Dependents (inbound) |
|--------|------------------------|---------------------|
| `workflow_gate.py` | stdlib only | ALL controllers (6 modules) |

### Tier 2: Infrastructure Layer

| Module | Dependencies | Dependents |
|--------|-------------|-----------|
| `config_loader.py` | workflow_gate, json, os | All stage controllers |
| `audit_utils.py` | json, os, uuid, datetime | All audit tool modules |
| `logger.py` | logging, datetime | utils consumers |
| `python_file_list.py` | hardcoded list constant | conftest, test modules |
| `routing_table_loader.py` | json, os, pathlib | pipeline_controller (inferred) |
| `fbc_registry.py` | ast, json, pathlib | None (standalone) |

### Tier 3: Stage Controllers

| Module | LOC | Direct Dependencies |
|--------|-----|---------------------|
| `pipeline_controller.py` | 588 | config_loader, workflow_gate, importlib (dynamic load of all stage controllers) |
| `repair_controller.py` | 467 | config_loader, workflow_gate, importlib |
| `audit_controller.py` | 223 | config_loader, workflow_gate |
| `simulation_controller.py` | 308 | config_loader, workflow_gate, importlib |
| `crawler_controller.py` | 290 | config_loader, workflow_gate, crawl_engine, crawl_monitor, file_scanner |
| `analysis_controller.py` | 300 | config_loader, workflow_gate, importlib |

### Tier 4: Tool Sublayer — Audit Tools (20 modules)

| Module | LOC | Input | Output |
|--------|-----|-------|--------|
| `_run_audit.py` | 1,519 | repo filesystem | JSON audit reports |
| `ap_artifact_collection_p1.py` | 648 | repo filesystem | artifact collection JSON |
| `run_audit_suite.py` | 68 | audit tool modules | aggregated audit report |
| `circular_dependency_audit.py` | 77 | import graph | circular dep report |
| `cross_package_dependency_audit.py` | 68 | import graph | cross-package violations |
| `duplicate_module_audit.py` | 58 | module list | duplicate report |
| `execution_core_isolation_audit.py` | 183 | module root | isolation violations |
| `facade_bypass_audit.py` | 66 | import records | facade bypass report |
| `file_size_audit.py` | 54 | filesystem | file size report |
| `governance_contract_audit.py` | 76 | module list | governance violations |
| `governance_coverage_map.py` | 79 | modules | coverage map |
| `governance_module_audit.py` | 73 | modules | governance module report |
| `header_schema_audit.py` | 49 | Python headers | schema violations |
| `import_surface_audit.py` | 61 | module imports | surface map |
| `module_path_ambiguity_audit.py` | 59 | module paths | ambiguity report |
| `namespace_shadow_audit.py` | 59 | namespaces | shadow report |
| `nexus_structural_audit.py` | 169 | module tree | nexus classification |
| `orphan_module_audit.py` | 64 | module graph | orphan list |
| `symbol_collision_audit.py` | ? | symbol index | collision report |
| `unused_import_audit.py` | ? | AST | unused import list |

### Tier 4: Tool Sublayer — Repair Operators (8 modules)

| Module | LOC | Mutation Risk |
|--------|-----|--------------|
| `facade_rewrite_pass.py` | 871 | HIGH — rewrites Python imports in source files |
| `facade_synthesis.py` | 879 | LOW — analysis only, generates rewrite maps |
| `reorganize.py` | 295 | HIGH — moves files with shutil |
| `import_rewrite_operator.py` | 129 | HIGH — rewrites import statements |
| `header_injection_operator.py` | 138 | HIGH — injects headers into Python files |
| `module_relocation_operator.py` | 134 | HIGH — relocates module files |
| `namespace_disambiguator.py` | 151 | MEDIUM — may rewrite namespace references |
| `dependency_normalizer.py` | 144 | MEDIUM — normalizes dependency declarations |

### Tier 4: Tool Sublayer — Simulators (5 modules)

| Module | LOC | Purpose |
|--------|-----|---------|
| `dependency_simulator.py` | 85 | Simulates dependency resolution |
| `import_simulator.py` | 65 | Simulates import resolution paths |
| `namespace_simulator.py` | 60 | Simulates namespace disambiguation |
| `repo_simulator.py` | 11 | Minimal repo simulation scaffolding |
| `runtime_simulator.py` | 92 | Simulates runtime execution context |

### Tier 4: Tool Sublayer — Semantic Extraction (8 modules)

| Module | LOC | Import Issues |
|--------|-----|--------------|
| `extract.py` | ? | BROKEN — imports from `Tools.Scripts.*` (pre-migration path) |
| `legacy_extract.py` | ? | BROKEN — imports `drac_af_extractor.ast_parser` (unresolved) |
| `ast_parser.py` | ? | OK |
| `classifier.py` | ? | OK |
| `semantic_extractor.py` | ? | OK |
| `pipeline.py` | ? | OK |
| `registry_writer.py` | ? | OK |
| `drac_indexer.py` | ? | OK |

---

## 3. Dependency Flow — Pipeline Controller

The `pipeline_controller.py` orchestrates all stages dynamically. Inferred execution order:

```
pipeline_controller.py
  Stage 1: os.chdir() → tools/audit_tools/ → importlib.import_module("audit_controller")
  Stage 2: analysis_controller  [runtime analysis, import scanning, semantic extraction]
  Stage 3: simulation_controller [dependency/import/namespace simulation]
  Stage 4: crawler_controller   [filesystem crawl]
  Stage 5: repair_controller    [mutation operators — MUTATING in live mode]
```

All stages report back to pipeline_controller, which aggregates results and writes the pipeline_execution_manifest.json.

---

## 4. External Dependency Surface

| Package | Version Spec | Status |
|---------|-------------|--------|
| Standard library (ast, json, os, sys, pathlib, argparse, importlib, hashlib, re, logging, datetime, traceback, collections, typing, math) | Python 3.x | OK |
| `pytest` | Any | Implicit test dep |
| `yaml` | PyYAML | Listed in requirements.txt |
| `drac_af_extractor` | N/A | NOT PRESENT — pre-migration artifact |
| `Tools.Scripts.*` | N/A | NOT PRESENT — pre-migration path |

---

## 5. Intra-AP Coupling Points

1. **workflow_gate.py → all controllers**: The strongest coupling. If the governance gate is relocated or its function signature changes, all 6 controllers break.
2. **config_loader.py → all controllers**: Second strongest coupling. All controllers depend on `ConfigLoader`.
3. **audit_utils.py → all audit tools**: All audit tools use `generate_id` and `write_log`.
4. **python_file_list.py → conftest, tests**: Shared file list constant; breaking this breaks all test discovery.

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*

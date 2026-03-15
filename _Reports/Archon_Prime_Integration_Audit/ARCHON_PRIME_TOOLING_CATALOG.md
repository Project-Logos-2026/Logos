# ARCHON PRIME TOOLING CATALOG
**Generated:** 2026-03-13  
**Scope:** All modules in `ARCHON_PRIME-main/WORKFLOW_MUTATION_TOOLING/` responsible for inspection, auditing, examination, analysis, orchestration, filesystem analysis, schema handling, report generation, and interface handling  
**Total tooling modules catalogued:** 59 (tools/), 7 (controllers/), 3 (simulation/), 8 (repair/operators/)  

---

## Category 1: Audit Tools (`tools/audit_tools/` — 20 modules)

### `_run_audit.py` — Master Audit Runner
- **Path:** `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/_run_audit.py`
- **Module ID:** (inferred from pattern) M-0xx
- **Purpose:** Primary audit suite orchestrator — executes all AP audit tools in sequence, collects results, writes JSON audit artifacts to `SYSTEM_AUDITS_AND_REPORTS/AUDIT_SCAN_RESULTS/`
- **LOC:** 1,519 (largest single module in AP)
- **Inputs:** Filesystem paths, Python file list from `python_file_list.py`
- **Outputs:** Multiple JSON audit reports under `SYSTEM_AUDITS_AND_REPORTS/AUDIT_SCAN_RESULTS/`
- **Current repo layout assumption:** Assumes AP root is working directory; uses relative paths throughout
- **Coupling points:** Imports all audit tool modules by bare name; depends on `audit_utils.py`, `python_file_list.py`
- **LOGOS normalization target:** `_Dev_Resources/Dev_Tools/Runtime_Tools/Repo_Audit/` (partial overlap)

### `ap_artifact_collection_p1.py` — Phase 1 Artifact Collector
- **Path:** `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/ap_artifact_collection_p1.py`
- **Purpose:** Phase 1 artifact collection — scans for existing AP audit artifacts, indexes them, produces collection summary
- **LOC:** 648
- **Inputs:** `SYSTEM_AUDITS_AND_REPORTS/` directory tree
- **Outputs:** Artifact collection JSON
- **LOGOS normalization target:** `_Dev_Resources/Dev_Tools/Runtime_Tools/Repo_Audit/`

### `run_audit_suite.py` — Audit Suite Entry Point
- **Path:** `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/run_audit_suite.py`
- **Purpose:** Thin wrapper that invokes `_run_audit.py` suite with configured scope
- **LOC:** 68
- **LOGOS normalization target:** `_Dev_Resources/Dev_Tools/Runtime_Tools/Repo_Audit/`

### `audit_utils.py` — Shared Audit Utilities
- **Path:** `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/audit_utils.py`
- **Purpose:** Shared utility functions: `generate_id()`, `write_log()` — used by all audit tools
- **LOC:** 68
- **Coupling points:** All audit tools depend on this
- **LOGOS normalization target:** `_Dev_Resources/Dev_Tools/Runtime_Tools/Dev_Utilities/`

### `circular_dependency_audit.py` — Circular Dependency Detector
- **LOC:** 77 | **Purpose:** Analyzes import graph for circular dependencies | **Inputs:** import graph JSON | **Outputs:** circular dependency report

### `cross_package_dependency_audit.py` — Cross-Package Dependency Auditor
- **LOC:** 68 | **Purpose:** Detects imports crossing package boundaries | **Inputs:** import graph | **Outputs:** cross-package violation report

### `duplicate_module_audit.py` — Duplicate Module Detector
- **LOC:** 58 | **Purpose:** Finds modules with identical names across different paths | **Inputs:** module list | **Outputs:** duplicate module report

### `execution_core_isolation_audit.py` — Isolation Auditor
- **LOC:** 183 | **Purpose:** Verifies module subtree does not import from forbidden external roots | **Inputs:** `--include-root`, `--roots` | **Outputs:** isolation violation report

### `facade_bypass_audit.py` — Facade Bypass Detector
- **LOC:** 66 | **Purpose:** Identifies imports that bypass canonical facades | **Inputs:** import records | **Outputs:** facade bypass report

### `file_size_audit.py` — File Size Auditor
- **LOC:** 54 | **Purpose:** Flags oversized modules | **Inputs:** filesystem | **Outputs:** file size report

### `governance_contract_audit.py` — Governance Contract Auditor
- **LOC:** 76 | **Purpose:** Verifies modules carry required governance contracts (headers, spec refs) | **Inputs:** module list | **Outputs:** governance violations

### `governance_coverage_map.py` — Governance Coverage Mapper
- **LOC:** 79 | **Purpose:** Maps which modules have governance coverage | **Inputs:** modules | **Outputs:** coverage map JSON

### `governance_module_audit.py` — Governance Module Auditor
- **LOC:** 73 | **Purpose:** Validates governance-specific module properties | **Inputs:** modules | **Outputs:** governance module report

### `header_schema_audit.py` — Header Schema Validator
- **LOC:** 49 | **Purpose:** Validates module headers against `AP_MODULE_HEADER_SCHEMA.json` | **Inputs:** Python file headers | **Outputs:** header schema violations

### `import_surface_audit.py` — Import Surface Auditor
- **LOC:** 61 | **Purpose:** Maps the full import surface of the AP codebase | **Inputs:** Python files | **Outputs:** import surface map

### `module_path_ambiguity_audit.py` — Path Ambiguity Detector
- **LOC:** 59 | **Purpose:** Detects ambiguous module paths (same module name, different locations) | **Inputs:** module paths | **Outputs:** ambiguity report

### `namespace_shadow_audit.py` — Namespace Shadow Detector
- **LOC:** 59 | **Purpose:** Finds namespace shadowing (local module masking stdlib or dependency) | **Inputs:** namespaces | **Outputs:** shadow report

### `nexus_structural_audit.py` — Nexus Classifier
- **LOC:** 169 | **Purpose:** Classifies modules into EXECUTION_NEXUS / BINDING_NEXUS / NON_NEXUS | **Inputs:** `--root` | **Outputs:** nexus classification JSON

### `orphan_module_audit.py` — Orphan Detector
- **LOC:** 64 | **Purpose:** Identifies modules with no inbound imports | **Inputs:** import graph | **Outputs:** orphan list

### `symbol_collision_audit.py` — Symbol Collision Detector
- **Purpose:** Finds symbol-level naming collisions across modules

### `unused_import_audit.py` — Unused Import Detector
- **Purpose:** AST-based detection of imported symbols never used

### `static_ast_analysis.py` — Static AST Analysis
- **LOC:** 175 | **Purpose:** Full AST-based structural analysis of Python modules

### `runtime_entry_audit.py` — Runtime Entry Auditor
- **LOC:** 53 | **Purpose:** Validates runtime entry-point declarations

### `scanner.py` — Python File Scanner
- **LOC:** 105 | **Purpose:** Recursively scans for Python files with ignore filtering

### `triage.py` — Module Triage
- **Purpose:** Categorizes discovered modules by functional type

### `repair_registry_loader.py` — Repair Registry Loader
- **LOC:** 117 | **Purpose:** Loads and validates repair registry JSON for use by repair tools

### `run_governance_audit.py` — Governance Audit Runner
- **LOC:** 50 | **Purpose:** Thin driver for governance-specific audit pass

---

## Category 2: Import Analysis Tools (`tools/import_analysis/` — 11 modules)

| Module | LOC | Purpose | LOGOS Counterpart |
|--------|-----|---------|-------------------|
| `Import_Linter.py` | ? | Static import enforcement linter | `Repo_Audit/Import_Linter.py` |
| `generate_deep_import_violations.py` | ? | Finds cross-cluster import violations | `Dependency_Analysis/generate_deep_import_violations.py` |
| `generate_symbol_import_index.py` | ? | Builds symbol-level import index | `Static_Analysis/generate_symbol_import_index.py` |
| `import_prefix_verifier.py` | ? | Verifies import prefix compliance | `Architecture_Validation/import_prefix_verifier.py` |
| `import_root_grouping_analyzer.py` | ? | Groups imports by root prefix | `Architecture_Validation/import_root_grouping_analyzer.py` |
| `import_scanner.py` | ? | Scans all imports from Python files | (partial: `Repo_Audit/scanner.py`) |
| `import_violation_classifier.py` | ? | Classifies violations as auto-repairable or manual | `Architecture_Validation/import_violation_classifier.py` |
| `module_root_existence_checker.py` | ? | Verifies import roots resolve to real directories | `Architecture_Validation/module_root_existence_checker.py` |
| `namespace_discovery_scan.py` | ? | Discovers where namespaces are located | `Architecture_Validation/namespace_discovery_scan.py` |
| `violation_prefix_grouper.py` | ? | Groups violations by prefix root | `Architecture_Validation/violation_prefix_grouper.py` |
| (scanner equivalent) | — | Already covered by import_scanner.py | — |

**Note:** The AP `tools/import_analysis/` directory is essentially a point-in-time copy of the LOGOS `Architecture_Validation/` tools. The file names and apparent purpose are nearly identical.

---

## Category 3: Runtime Analysis Tools (`tools/runtime_analysis/` — 7 modules)

| Module | LOC | Purpose | LOGOS Counterpart |
|--------|-----|---------|-------------------|
| `dependency_graph.py` | ? | Builds dependency graph between modules | `Dependency_Analysis/cluster_analysis.py` |
| `runtime_analysis.py` | ? | Full runtime topology analysis | `Static_Analysis/runtime_analysis.py` |
| `runtime_callgraph_extractor.py` | ? | Extracts call graph via static analysis | `Runtime_Diagnostics/runtime_callgraph_extractor.py` |
| `runtime_debug_artifact_scanner.py` | ? | Scans for debug artifacts (prints, TODOs) | `Runtime_Diagnostics/runtime_debug_artifact_scanner.py` |
| `runtime_execution_tracer.py` | ? | Live execution tracing via sys.settrace | `Runtime_Diagnostics/runtime_execution_tracer.py` |
| `runtime_module_tree_auditor.py` | ? | AST-based module tree audit | `Runtime_Diagnostics/runtime_module_tree_auditor.py` |
| — | — | Additional runtime analysis (inferred) | — |

**Note:** The AP `tools/runtime_analysis/` directory mirrors LOGOS `Runtime_Diagnostics/` almost exactly.

---

## Category 4: Semantic Extraction Tools (`tools/semantic_extraction/` — 8 modules)

| Module | Purpose | Status |
|--------|---------|--------|
| `extract.py` | Top-level extraction entry point | BROKEN — pre-migration `Tools.Scripts.*` imports |
| `legacy_extract.py` | Legacy extraction (older format) | BROKEN — `drac_af_extractor` not present |
| `ast_parser.py` | AST function/class extraction | OK |
| `classifier.py` | Module classification (reasoning / utility) | OK |
| `semantic_extractor.py` | Semantic record extraction | OK |
| `pipeline.py` | Extraction pipeline orchestrator | OK |
| `registry_writer.py` | Writes FBC registry | OK |
| `drac_indexer.py` | DRAC Application Function indexer | OK |

---

## Category 5: Normalization Tools (`tools/normalization_tools/` — 3 modules)

| Module | Purpose | Notes |
|--------|---------|-------|
| `header_validator.py` | Validates AP module headers against AP_MODULE_HEADER_SCHEMA.json | Read-only validator |
| `normalization_engine.py` | Drives normalization passes (header injection, import rewrite) — **MUTATING when activated** | Safe in validation-only mode |
| `schema_registry.py` | Loads and manages schema definitions from `AP_SYSTEM_CONFIG/SYSTEM/SCHEMAS/` | Read-only |

---

## Category 6: Repo Mapping Tools (`tools/repo_mapping/` — 2 modules)

| Module | Purpose | LOGOS Counterpart |
|--------|---------|-------------------|
| `repo_scanner.py` | Scans repository structure | `Repo_Audit/scanner.py` |
| `repo_structure_export.py` | Exports repo structure to JSON | `Repo_Audit/repo_structure_export.py` |

---

## Category 7: Governance Analysis Tools (`tools/governance_analysis/` — 1 module)

| Module | Purpose |
|--------|---------|
| `governance_scanner.py` | Scans for governance compliance markers (headers, spec refs, gate calls) |

---

## Category 8: Pipeline Orchestration (Controllers — 7 modules)

| Module | Role | Mutation Risk |
|--------|------|--------------|
| `pipeline_controller.py` | Full pipeline orchestrator (audit→analysis→simulation→crawl→repair) | HIGH (repair stage) |
| `audit_controller.py` | Audit stage orchestrator | LOW — reads only |
| `analysis_controller.py` | Analysis stage orchestrator | LOW — reads only |
| `simulation_controller.py` | Simulation stage orchestrator | LOW — simulation only |
| `crawler_controller.py` | Filesystem crawl orchestrator | LOW — reads only |
| `repair_controller.py` | Repair stage orchestrator | HIGH — invokes mutating operators |
| `config_loader.py` | Configuration loading and validation | NONE |

---

## Category 9: Filesystem / Crawler Analysis (`crawler/` — 3 modules)

| Module | Purpose |
|--------|---------|
| `crawl_engine.py` | Core crawl engine — walks filesystem, indexes files |
| `crawl_monitor.py` | Monitors crawl progress, tracks metrics |
| `file_scanner.py` | Scans directories, builds file index |

---

## Category 10: Report Generation (`semantic_extraction/pipeline.py`, `registry_writer.py`, `fbc_registry.py`)

| Module | Inputs | Outputs |
|--------|--------|---------|
| `pipeline.py` | AST extraction results | Aggregated semantic pipeline output |
| `registry_writer.py` | FBC records | FBC registry JSON |
| `fbc_registry.py` | 740 LOC — comprehensive FBC registry system | Full registry + index |

---

## Category 11: Workflow Governance (`WORKFLOW_NEXUS/`)

| Module | Purpose |
|--------|---------|
| `workflow_gate.py` | Enforces runtime governance gate — called as `enforce_runtime_gate()` at module load |

---

## Category 12: Target Processing (`WORKFLOW_TARGET_PROCESSING/`, `WORKFLOW_TARGET_AUDITS/`)

| Module | Purpose |
|--------|---------|
| `WORKFLOW_TARGET_AUDITS/MODULES/analysis/dependency_graphs/cluster_analysis.py` | Cluster analysis for LOGOS target files |
| `WORKFLOW_TARGET_AUDITS/MODULES/analysis/dependency_graphs/packet_discovery.py` | Packet discovery for LOGOS targets |
| `WORKFLOW_TARGET_AUDITS/MODULES/analysis/repo_maps/repo_mapper.py` | Repo mapper for LOGOS target structure |

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*

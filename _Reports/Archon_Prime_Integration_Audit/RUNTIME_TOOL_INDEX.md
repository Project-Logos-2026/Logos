# RUNTIME TOOL INDEX
**Generated:** 2026-03-13  
**Audit Operation:** Archon Prime Integration Audit  
**Tool Surface:** `/workspaces/Logos/_Dev_Resources/Dev_Tools/Runtime_Tools`  
**Target:** `/workspaces/Logos/LOGOS_SYSTEM/RUNTIME_BRIDGE/ARCHON_PRIME`  

---

## Overview

Total tools discovered: **30**  
Read-only tools: **26**  
Mutating tools (SKIP): **2**  
Live-execution tools (SKIP for this audit): **1**  
Data / support files: **4**  

---

## Functional Groups

### Group 1 — Repository Scanners / Structure Exporters
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `scanner.py` | `Repo_Audit/` | Recursively finds all .py files under repo, ignores non-source trees | YES |
| `repo_structure_export.py` | `Repo_Audit/` | Walks repo tree, exports directory+Python-file JSON inventory | YES |
| `triage.py` | `Repo_Audit/` | Triages discovered Python files by category (reasoning, utility, etc.) | YES |

### Group 2 — Import Analyzers
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `Import_Linter.py` | `Repo_Audit/` | Static import enforcement linter; scans for forbidden root prefixes | YES |
| `import_prefix_verifier.py` | `Architecture_Validation/` | Verifies import prefixes against allowed root list from violations JSON | YES (input format issue) |
| `import_root_grouping_analyzer.py` | `Architecture_Validation/` | Groups imports by root prefix, produces frequency analysis | YES (input format issue) |
| `import_violation_classifier.py` | `Architecture_Validation/` | Classifies import violations into AUTO_REPAIRABLE / MANUAL categories | YES (input format issue) |
| `generate_deep_import_violations.py` | `Dependency_Analysis/` | Finds deep import violations (imports crossing module cluster boundaries) | YES |
| `violation_prefix_grouper.py` | `Architecture_Validation/` | Groups violations by import prefix root for batch analysis | YES (input format issue) |
| `generate_symbol_import_index.py` | `Static_Analysis/` | Builds symbol-level import index across all Python files | YES |

### Group 3 — Header Inspectors
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `static_ast_analysis.py` | `Static_Analysis/` | AST-based inspection of headers, docstrings, and module structure | YES |
| `header_schema_audit.py` [AP internal] | `WORKFLOW_MUTATION_TOOLING/tools/audit_tools/` | AP internal: validates headers against AP_MODULE_HEADER_SCHEMA | AP internal |

### Group 4 — Schema Validators
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `drac_indexer.py` | `Static_Analysis/` | Indexes DRAC Application Function (AF) modules, classifies by runtime role | YES |

### Group 5 — Module Graph Analyzers / Semantic
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `ast_parser.py` | `Static_Analysis/` | AST-based function/class extraction, signature and docstring harvesting | YES |
| `classifier.py` | `Static_Analysis/` | Classifies modules extracted by semantic extractor into reasoning/utility | YES |
| `semantic_extractor.py` | `Static_Analysis/` | Extracts semantic records from Python modules (reasoning vs utility) | YES |
| `packet_discovery.py` | `Static_Analysis/` | Discovers and maps module packets and their cycle structure | YES |
| `extract.py` | `Code_Extraction/` | Module code extraction pass | YES |
| `legacy_extract.py` | `Code_Extraction/` | Legacy extraction pass | YES |
| `fbc_registry.py` | `Code_Extraction/` | Function/Behavior/Class registry builder from extracted modules | YES |

### Group 6 — Dependency Mappers
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `cluster_analysis.py` | `Dependency_Analysis/` | Builds cluster-based dependency graph; detects cross-cluster violations | YES |
| `facade_synthesis.py` | `Dependency_Analysis/` | Derives canonical import facades from runtime topology (analysis only) | YES |
| `facade_rewrite_pass.py` | `Dependency_Analysis/` | **MUTATING** — applies facade rewrites to source files | **NO** |

### Group 7 — Runtime Topology Inspectors
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `runtime_analysis.py` | `Static_Analysis/` | Full runtime topology analysis: directory tree, imports, dependency graph, violation detection | YES |
| `runtime_module_tree_auditor.py` | `Runtime_Diagnostics/` | AST-based module tree audit with --module-root arg; produces module_tree_audit.json | YES |
| `runtime_callgraph_extractor.py` | `Runtime_Diagnostics/` | Extracts static call graph from Python module tree | YES |
| `runtime_debug_artifact_scanner.py` | `Runtime_Diagnostics/` | Scans for debug artifacts (print calls, TODO comments, bare asserts) | YES |
| `runtime_execution_tracer.py` | `Runtime_Diagnostics/` | **LIVE EXECUTION** — uses sys.settrace to trace actual entry script execution | **NO** |

### Group 8 — Architecture Validators
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `execution_core_isolation_audit.py` | `Architecture_Validation/` | Validates that modules in a root don't import from forbidden external prefixes | YES |
| `namespace_discovery_scan.py` | `Architecture_Validation/` | Discovers namespace locations of target packages across the repo | YES |
| `nexus_structural_audit.py` | `Architecture_Validation/` | Classifies all Python modules into EXECUTION_NEXUS / BINDING_NEXUS / NON_NEXUS | YES |
| `module_root_existence_checker.py` | `Architecture_Validation/` | Verifies that import root prefixes correspond to real directories | YES |

### Group 9 — Report Generators
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `pipeline.py` | `Report_Generation/` | Report generation pipeline orchestrator | YES |
| `registry_writer.py` | `Report_Generation/` | Writes registry output artifacts | YES |

### Group 10 — Migration Tools
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `reorganize.py` | `Migration/` | **MUTATING** — uses shutil.move to relocate Python modules | **NO** |

### Group 11 — Dev Utilities / Support
| File | Path | Purpose | Safe? |
|------|------|---------|-------|
| `__init__.py` | `Dev_Utilities/` | Package marker | — |
| `conftest.py` | `Dev_Utilities/` | Pytest configuration | — |
| `python_file_list.py` | `Dev_Utilities/` | Shared Python file enumeration utility | — |
| `test_import_base_reasoning_registry.py` | `Dev_Utilities/` | Import base registry test | — |

### Group 12 — Snapshot Data Files (Not Executable)
| File | Path | Purpose |
|------|------|---------|
| `repo_directory_tree.json` | `Repo_Audit/` | Cached directory tree snapshot |
| `repo_imports.json` | `Repo_Audit/` | Cached import snapshot |
| `repo_python_files.json` | `Repo_Audit/` | Cached Python file list snapshot |

---

## Tools with Input Format Incompatibilities (runtime_imports.json format)

The following Architecture_Validation tools expect a `{"violations": [...]}` wrapper but the ARCHON_RUNTIME_ANALYSIS output files are bare JSON arrays or have different schemas. These tools ran against AP data but produced `AttributeError: 'list' object has no attribute 'get'`:

- `import_prefix_verifier.py` — expects `data.get("violations", [])`
- `import_violation_classifier.py` — same
- `import_root_grouping_analyzer.py` — same
- `violation_prefix_grouper.py` — same
- `module_root_existence_checker.py` — runs but finds 0 root prefixes

**Disposition:** Logged as PARTIAL — tools are read-only and safe, but their input schema does not match the current runtime_analysis.py output format. Tools were not mutated to fix this.

---

## Execution Safety Summary

| Category | Count |
|----------|-------|
| Fully safe + executed | 18 |
| Safe but incompatible input format (logged) | 5 |
| Safe but no output (scope mismatch) | 3 |
| SKIPPED — mutating (file writes/moves) | 2 |
| SKIPPED — live code execution | 1 |

---

*Report produced by: LOGOS Archon Prime Integration Audit — 2026-03-13*

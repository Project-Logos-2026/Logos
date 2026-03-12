# Dev Scripts — Tool Reference README
**Version:** 2.0  
**Generated:** 2026-03-11  
**Root:** `_Dev_Resources/_Dev_Scripts/Repo_Tools/`

---

## Overview

This document provides a reference for every tool in the canonical Dev
Tooling suite. All scripts live under `Repo_Tools/` organized by functional
classification. The Tool Index (`Tool_Index/`) contains machine-readable
equivalents of this document.

**Destructive tools are marked ⚠️.**  
**Artifact-producing tools are marked 📄.**

---

## Repo_Audit

### Import_Linter
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Repo_Audit/Import_Linter.py` |
| **Purpose** | Static import enforcement linter. Scans `STARTUP/` and `LOGOS_SYSTEM/` for namespace violations, prohibited import patterns, bare-prefix imports, and forbidden network modules. |
| **Input Artifacts** | Repository source tree (`STARTUP/`, `LOGOS_SYSTEM/`) |
| **Output Artifacts** | Console report (stdout); no files written |
| **Capabilities** | `import_violation_scan`, `namespace_enforcement`, `prohibited_pattern_detection` |
| **Safe Usage** | Read-only. Run freely at any time. |
| **Destructive Potential** | None |

---

### triage ⚠️ 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Repo_Audit/triage.py` |
| **Purpose** | Legacy module triage and extraction. Classifies staging modules into reasoning/utils categories, moves files, deduplicates, and writes JSON + markdown reports. |
| **Input Artifacts** | `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS/` |
| **Output Artifacts** | `_Reports/triage_report.json`, `_Reports/triage_summary.md` |
| **Capabilities** | `module_classification`, `staging_triage`, `deduplication`, `file_relocation`, `json_report_generation` |
| **Safe Usage** | Dry-run verification required before live pass. Confirm staging directory scope. |
| **Destructive Potential** | HIGH — moves files between directories |

---

### scanner
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Repo_Audit/scanner.py` |
| **Purpose** | Repository Python source file scanner. Recursively yields `.py` files under a root, skipping `__pycache__`, `.git`, `node_modules`, and virtual environment directories. |
| **Input Artifacts** | Repository root path (argument: `root: Path`) |
| **Output Artifacts** | Iterator of `Path` objects (library use) |
| **Capabilities** | `python_file_discovery`, `recursive_scan`, `ignore_filter` |
| **Safe Usage** | Read-only library module. Import and use freely. |
| **Destructive Potential** | None |

---

### repo_structure_export 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Repo_Audit/repo_structure_export.py` |
| **Purpose** | Walks the repository tree and exports directory structure, Python file list, and all import statements to JSON artifacts. |
| **Input Artifacts** | Repository root (auto-detected from script location) |
| **Output Artifacts** | `repo_directory_tree.json`, `repo_python_files.json`, `repo_imports.json` |
| **Capabilities** | `directory_tree_export`, `python_file_indexing`, `import_statement_extraction` |
| **Safe Usage** | Read-only analysis; writes output JSON files only. Safe to run at any time. |
| **Destructive Potential** | None (writes new artifact files only) |

---

## Static_Analysis

### ast_parser
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/ast_parser.py` |
| **Purpose** | AST-based function extraction module. Extracts function name, docstring, signature, imports, and body summary from Python source files. |
| **Input Artifacts** | Python source file path |
| **Output Artifacts** | In-memory data structures (library use) |
| **Capabilities** | `function_extraction`, `docstring_extraction`, `signature_extraction`, `import_extraction`, `ast_traversal` |
| **Safe Usage** | Read-only library. Import and use freely. |
| **Destructive Potential** | None |

---

### classifier
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/classifier.py` |
| **Purpose** | Keyword-based function classifier. Maps functions into DRAC AF categories: `AGENT_CONTROL`, `SEMANTIC_PROCESSING`, `REASONING_ENGINE`, `UTILITY_SUPPORT`, `SAFETY_GUARD`, `MATH_OPERATOR`. |
| **Input Artifacts** | Function name, docstring, body_calls (strings) |
| **Output Artifacts** | Classification label (string, library use) |
| **Capabilities** | `function_classification`, `drac_af_categorization`, `keyword_signal_matching` |
| **Safe Usage** | Pure function. No I/O. Safe to call freely. |
| **Destructive Potential** | None |

---

### drac_indexer 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/drac_indexer.py` |
| **Purpose** | DRAC Application Function Master Index Builder. Scans DRAC categorical subdirectories and produces `af_master_index.json`, `af_cluster_index.json`, and `af_runtime_roles.json`. Read-only analysis. |
| **Input Artifacts** | `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS/` |
| **Output Artifacts** | `af_master_index.json`, `af_cluster_index.json`, `af_runtime_roles.json` |
| **Capabilities** | `drac_af_master_index_build`, `cluster_index_generation`, `runtime_role_assignment` |
| **Safe Usage** | Analysis-only. No source mutations. Safe to run at any time. |
| **Destructive Potential** | None |

---

### runtime_analysis 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/runtime_analysis.py` |
| **Purpose** | ARCHON runtime topology analysis. Analyzes `LOGOS_SYSTEM/`, `STARTUP/`, `DOCUMENTS/`, `BLUEPRINTS/`, and `_Governance/` to produce machine-readable topology artifacts. |
| **Input Artifacts** | Runtime surface directories (auto-configured) |
| **Output Artifacts** | `ARCHON_RUNTIME_ANALYSIS/runtime_topology.json` |
| **Capabilities** | `runtime_topology_analysis`, `import_surface_mapping` |
| **Safe Usage** | Analysis-only. No repository mutations. Safe to run at any time. |
| **Destructive Potential** | None |

---

### semantic_extractor
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/semantic_extractor.py` |
| **Purpose** | Derives the minimal semantic modifier expression for a function name (e.g. `symbolic_deduction()` → `"deduce(symbolic)"`). Extracts ARP/CSP/MTP semantic scores from AST node data. |
| **Input Artifacts** | Function name (string) |
| **Output Artifacts** | Semantic label (string, library use) |
| **Capabilities** | `semantic_signal_extraction`, `arp_csp_mtp_scoring`, `function_semantic_labeling` |
| **Safe Usage** | Pure function. No I/O. Safe to call freely. |
| **Destructive Potential** | None |

---

### static_ast_analysis 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/static_ast_analysis.py` |
| **Purpose** | Static AST analysis for the Logos repository. Extracts module paths, file paths, and static imports. Outputs `FULL_STATIC_IMPORT_GRAPH.json` and `LAYER_CLASSIFIED_GRAPH.json`. |
| **Input Artifacts** | `Repo_Tools/Dev_Utilities/python_file_list.py` (PYTHON_FILE_LIST constant) |
| **Output Artifacts** | `_Reports/FULL_STATIC_IMPORT_GRAPH.json`, `_Reports/LAYER_CLASSIFIED_GRAPH.json` |
| **Capabilities** | `import_graph_extraction`, `module_path_mapping`, `layer_classification` |
| **Safe Usage** | Read-only. Refresh `python_file_list.py` before running for accurate results. |
| **Destructive Potential** | None |

---

### packet_discovery 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/packet_discovery.py` |
| **Purpose** | Module packet discovery. Builds an import dependency graph, detects strongly connected components (SCCs), classifies packets, and produces JSON + DOT output. |
| **Input Artifacts** | Staging and Blueprints directories (auto-configured) |
| **Output Artifacts** | `Tools/module_packets.json`, `Tools/dependency_graph.dot` |
| **Capabilities** | `import_dependency_graph_build`, `scc_detection`, `packet_classification`, `dot_export` |
| **Safe Usage** | Read-only. Safe to run at any time. |
| **Destructive Potential** | None |

---

### generate_symbol_import_index 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Static_Analysis/generate_symbol_import_index.py` |
| **Purpose** | Read-only AST audit. Extracts symbol-level import data from all Python files in the repository and writes `repo_symbol_imports.json`. Also refreshes `repo_python_files.json`. |
| **Input Artifacts** | Repository source tree (auto-discovered via `os.walk`) |
| **Output Artifacts** | `_Reports/Canonical_Import_Facade/repo_symbol_imports.json`, `repo_python_files.json` |
| **Capabilities** | `symbol_level_import_extraction`, `repo_wide_ast_audit` |
| **Safe Usage** | Read-only analysis. Safe to run at any time. |
| **Destructive Potential** | None |

---

## Dependency_Analysis

### cluster_analysis 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dependency_Analysis/cluster_analysis.py` |
| **Purpose** | Runtime dependency graph clustering. Ingests topology artifacts and performs Louvain community detection, SCC detection, betweenness centrality, cluster boundary analysis, and facade candidate identification. |
| **Input Artifacts** | `ARCHON_RUNTIME_ANALYSIS/runtime_topology.json` |
| **Output Artifacts** | `ARCHON_RUNTIME_ANALYSIS/cluster_analysis.json` |
| **Capabilities** | `community_detection`, `scc_analysis`, `betweenness_centrality`, `cluster_boundary_analysis`, `facade_candidate_identification` |
| **Safe Usage** | Analysis-only. Requires `runtime_analysis.py` output as input. |
| **Destructive Potential** | None |

---

### facade_rewrite_pass ⚠️ 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dependency_Analysis/facade_rewrite_pass.py` |
| **Purpose** | Facade import rewrite pass. Applies deterministic facade substitutions from a rewrite table to `AUTO_REPAIRABLE` deep import violations. Fail-closed with AST-verified dry-run before any live pass. |
| **Input Artifacts** | `ARCHON_RUNTIME_ANALYSIS/rewrite_table.json`, `BLUEPRINTS/Canonical_Import_Facade/Deep_Import_Violations.json` |
| **Output Artifacts** | `ARCHON_RUNTIME_ANALYSIS/rewrite_report.json`; modifies source `.py` files |
| **Capabilities** | `facade_import_substitution`, `ast_verified_dry_run`, `source_file_rewrite`, `diff_generation` |
| **Safe Usage** | ALWAYS run `--dry-run` first. Review diff output. Only proceed with `--live` after explicit approval. |
| **Destructive Potential** | CRITICAL — rewrites source `.py` files in-place |

---

### facade_synthesis 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dependency_Analysis/facade_synthesis.py` |
| **Purpose** | Runtime Facade Synthesis Pass. Derives canonical import facades and generates automated rewrite mappings from runtime topology artifacts. Analysis only. |
| **Input Artifacts** | `ARCHON_RUNTIME_ANALYSIS/runtime_topology.json`, `BLUEPRINTS/Canonical_Import_Facade/` |
| **Output Artifacts** | `BLUEPRINTS/Canonical_Import_Facade/facade_synthesis.json` |
| **Capabilities** | `canonical_facade_derivation`, `rewrite_mapping_generation` |
| **Safe Usage** | Analysis-only. No source mutation. Safe to run at any time. |
| **Destructive Potential** | None |

---

### generate_deep_import_violations 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dependency_Analysis/generate_deep_import_violations.py` |
| **Purpose** | Canonical Import Facade Phase 3. Scans the entire repository for forbidden-prefix deep imports and produces a structured violation dataset. Exit 0 on success, 1 on fatal error. |
| **Input Artifacts** | Repository source tree (auto-discovered) |
| **Output Artifacts** | `BLUEPRINTS/Canonical_Import_Facade/Deep_Import_Violations.json` |
| **Capabilities** | `deep_import_violation_scan`, `forbidden_prefix_detection` |
| **Safe Usage** | Read-only scan. Safe to run at any time. |
| **Destructive Potential** | None |

---

## Code_Extraction

### extract 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Code_Extraction/extract.py` |
| **Purpose** | Application Function Extraction Pass. Uses semantic-heuristic analysis to identify and extract application functions from the LOGOS repository. COPY ONLY — no source modifications. |
| **Input Artifacts** | Repository source tree |
| **Output Artifacts** | `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS/` (copies only) |
| **Capabilities** | `application_function_extraction`, `semantic_heuristic_analysis`, `function_copy_pipeline` |
| **Safe Usage** | Copy-only. Does not modify source files. Safe to run at any time. |
| **Destructive Potential** | None |

---

### legacy_extract 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Code_Extraction/legacy_extract.py` |
| **Purpose** | Legacy Application Function Deep Semantic Extraction pipeline. Targets legacy staging modules with deep static analysis. Read-only. |
| **Input Artifacts** | `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS/` |
| **Output Artifacts** | `Application_Function_Extraction/` |
| **Capabilities** | `legacy_function_extraction`, `deep_semantic_analysis`, `function_copy_pipeline` |
| **Safe Usage** | Read-only analysis. Safe to run at any time. |
| **Destructive Potential** | None |

---

### fbc_registry 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Code_Extraction/fbc_registry.py` |
| **Purpose** | DRAC Function Block Core (FBC) Registry Builder. Produces the FBC master registry, taxonomy, tag dictionary, compatibility matrix, and modular library manifest. Read-only. |
| **Input Artifacts** | DRAC Invariables directory |
| **Output Artifacts** | `fbc_master_registry.json`, `fbc_taxonomy.json`, `fbc_tag_dictionary.json`, `af_core_compatibility_matrix.json`, `modular_library_manifest.json` |
| **Capabilities** | `fbc_master_registry_build`, `fbc_taxonomy_generation`, `tag_dictionary_generation`, `compatibility_matrix_generation` |
| **Safe Usage** | Read-only. Safe to run at any time. |
| **Destructive Potential** | None |

---

## Migration

### reorganize ⚠️ 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Migration/reorganize.py` |
| **Purpose** | APPLICATION_FUNCTIONS categorical reorganization. Move-only pass: categorizes staging modules and relocates them into canonical directories. No code edits, no deletions, no import modifications. |
| **Input Artifacts** | `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS/`, `Tools/module_packets.json` |
| **Output Artifacts** | `Tools/reorganize_report.json`; moves files between staging directories |
| **Capabilities** | `categorical_file_relocation`, `staging_reorganization`, `move_only_pass` |
| **Safe Usage** | Review `module_packets.json` categorization carefully before running. Confirm target directories are correct. |
| **Destructive Potential** | HIGH — moves files between directories |

---

## Report_Generation

### pipeline 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Report_Generation/pipeline.py` |
| **Purpose** | DRAC AF extraction pipeline orchestrator. Coordinates Pass 1: extracts `agent_control` functions across the entire LOGOS repository. COPY ONLY. |
| **Input Artifacts** | Repository source tree |
| **Output Artifacts** | `MODULAR_LIBRARY/af_semantic_registry.json` |
| **Capabilities** | `af_extraction_orchestration`, `pipeline_coordination`, `registry_population` |
| **Safe Usage** | Copy-only. Does not modify source files. Depends on `ast_parser`, `classifier`, `semantic_extractor`, `registry_writer`. |
| **Destructive Potential** | None |

---

### registry_writer 📄
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Report_Generation/registry_writer.py` |
| **Purpose** | Writes AF semantic registry entries to `MODULAR_LIBRARY` with deterministic AF IDs (AF_0001, AF_0002, …). Called by `pipeline.py`. |
| **Input Artifacts** | AF record dict (library call) |
| **Output Artifacts** | `MODULAR_LIBRARY/af_semantic_registry.json` |
| **Capabilities** | `af_registry_entry_write`, `deterministic_af_id_assignment` |
| **Safe Usage** | Library module. Called by pipeline only. Do not invoke standalone unless writing test entries. |
| **Destructive Potential** | None (appends/updates registry JSON) |

---

## Dev_Utilities

### python_file_list
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dev_Utilities/python_file_list.py` |
| **Purpose** | Auto-generated static index of Python files. Provides `PYTHON_FILE_LIST` constant consumed by `static_ast_analysis.py` and other tools. |
| **Input Artifacts** | None (auto-generated by static analysis agent) |
| **Output Artifacts** | `PYTHON_FILE_LIST` constant (imported) |
| **Capabilities** | `python_file_index_provision`, `static_analysis_input` |
| **Safe Usage** | Regenerate via `generate_symbol_import_index.py` before running static analysis. |
| **Destructive Potential** | None |

---

### conftest
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dev_Utilities/conftest.py` |
| **Purpose** | pytest conftest for the Dev_Utilities test scope. Provides shared fixtures and test session configuration. |
| **Input Artifacts** | None |
| **Output Artifacts** | None (pytest session setup) |
| **Capabilities** | `pytest_fixture_configuration`, `test_session_setup` |
| **Safe Usage** | Auto-loaded by pytest. No standalone invocation needed. |
| **Destructive Potential** | None |

---

### test_import_base_reasoning_registry
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dev_Utilities/test_import_base_reasoning_registry.py` |
| **Purpose** | Smoke test verifying that base reasoning registry imports resolve correctly from the `logos` package. |
| **Input Artifacts** | `logos` package (runtime) |
| **Output Artifacts** | pytest pass/fail result |
| **Capabilities** | `import_smoke_test`, `base_reasoning_registry_validation` |
| **Safe Usage** | Run via `pytest`. Environment-sensitive — skips if `logos` package unavailable. |
| **Destructive Potential** | None |

---

### __init__
| Field | Value |
|-------|-------|
| **Location** | `Repo_Tools/Dev_Utilities/__init__.py` |
| **Purpose** | Package namespace declaration for `Dev_Utilities`. |
| **Input Artifacts** | None |
| **Output Artifacts** | None |
| **Capabilities** | `package_namespace_declaration` |
| **Safe Usage** | Not invoked directly. |
| **Destructive Potential** | None |

---

*Dev Scripts README v2.0 — established as part of canonical Dev Tooling Migration, 2026-03-11*

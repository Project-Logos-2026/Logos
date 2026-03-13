# MODULES TO INTEGRATE — INVENTORY
**Directory:** `WORKFLOW_EXECUTION_ENVELOPES/INCOMING_TARGETS/TARGETS/Modules_To_Integrate/`
**Generated:** 2026-03-12
**Total modules:** 40 (37 parseable, 3 parse errors)

---

## PARSE ERRORS (3 modules — require repair before integration)

| Module | Error |
|---|---|
| `facade_synthesis.py` | `invalid syntax` — line 8 |
| `fbc_registry.py` | `unexpected indent` — line 557 |
| `pipeline.py` | `unexpected indent` — line 190 |
| `test_import_base_reasoning_registry.py` | `expected 'except' or 'finally' block` — line 35 |

---

## AP V1 SALVAGE MODULES (5)

### `_run_audit.py`
*ARCHON PRIME Mechanical Completeness Audit*
| Function | Brief |
|---|---|
| `write_json` | Writes JSON artifact to disk |
| `record_failure` | Records a step failure |
| `flush_failures` | Flushes accumulated failures to file |
| `step1_parse_module_inventory` — `step10_final_report` | Sequential audit pipeline steps (1–10) |
| `main` | Entry point |

### `ap_artifact_collection_p1.py`
*AP_ARTIFACT_COLLECTION_P1_R1_EXECUTION*
| Function | Brief |
|---|---|
| `step0_create_directories` | Creates output directory structure |
| `is_excluded` | Returns True if path should be excluded from scanning |
| `step1_scan_repository` | Scans repo for all files |
| `classify_file` | Returns `(role, type_bucket, unclassified)` for a file |
| `step2_classify` | Classifies all discovered files |
| `path_to_safe_name` | Converts relative path to flat safe filename |
| `step3_handle_collisions` | Resolves filename collisions before copy |
| `step4_copy_files` | Copies files to artifact buckets |
| `build_tree` | Recursively builds directory tree dict |
| `step5_build_directory_tree` | Writes directory tree artifact |
| `collect_empty_dirs` / `find_truly_empty_dirs` | Finds directories with zero files in entire subtree |
| `step51_detect_empty_directories` | Writes empty directory report |
| `step6_write_artifact_index` — `step8_terminal_summary` | Final artifact writing and summary |
| `validate_outputs` | Validates expected outputs exist |
| `main` | Entry point |

### `generate_deep_import_violations.py`
*Canonical Import Facade — Phase 3: Deep Import Violation Dataset*
| Function | Brief |
|---|---|
| `is_import_line` | Returns True if line starts with `import`/`from` |
| `path_is_allowlisted` | Checks if path segment is in the allowlist |
| `scan` | Walks repo, scans every .py, returns `(files_scanned, violations)` |
| `main` | Entry point |

### `generate_symbol_import_index.py`
*AST audit: extracts symbol-level import data from all Python files*
| Function | Brief |
|---|---|
| `should_skip` | Returns True if any path segment matches an ignore dir |
| `discover_python_files` | Walks repo and returns relative paths of all .py files |
| `load_python_files` | Loads from index file or falls back to discovery |
| `read_source_lines` | Reads source lines from a file with error tolerance |
| `parse_imports` | AST-parses a file and returns import records with symbol, module, alias |
| `main` | Entry point; writes `repo_symbol_imports.json` |

### `repo_structure_export.py`
*No docstring — flat script*
Walks `REPO_ROOT`, collects directories/python files/imports, writes `repo_directory_tree.json`, `repo_python_files.json`, `repo_imports.json`.

---

## LOGOS MIGRATION MODULES (35)

### Architecture Validation (8)

#### `execution_core_isolation_audit.py`
| Function | Brief |
|---|---|
| `get_imports` | Returns all imported module strings from a Python file |
| `main` | Audits whether execution core modules are isolated from forbidden imports |
| `write_report` | Writes JSON report to output root |

#### `import_prefix_verifier.py`
| Function | Brief |
|---|---|
| `extract_prefix_distribution` | Builds prefix frequency tables from 1 to max_segments depth |
| `main` | Verifies import prefixes against allowed namespace rules |
| `write_report` | Writes JSON report |

#### `import_root_grouping_analyzer.py`
| Function | Brief |
|---|---|
| `group_by_root` | Groups violations by root (first segment) of imported module |
| `main` | Produces grouped violation report by import root |
| `write_report` | Writes JSON report |

#### `import_violation_classifier.py`
| Function | Brief |
|---|---|
| `classify_violations` | Groups violations by rule ID and root prefix |
| `main` | Classifies import violations from upstream scan results |
| `write_report` | Writes JSON report |

#### `module_root_existence_checker.py`
| Function | Brief |
|---|---|
| `check_root` | Checks whether root_name resolves to a directory in scan dirs |
| `extract_roots` | Extracts root prefix names from various report formats |
| `main` | Validates that all import roots resolve to real filesystem paths |
| `write_report` | Writes JSON report |

#### `namespace_discovery_scan.py`
| Function | Brief |
|---|---|
| `discover_namespaces` | Finds all directories matching each target name under repo_root |
| `main` | Discovers all namespace directories present in the target repo |
| `write_report` | Writes JSON report |

#### `nexus_structural_audit.py`
| Function | Brief |
|---|---|
| `classify_module` | Classifies a module and lists its top-level class names |
| `main` | Audits structural properties of nexus/facade modules |
| `write_report` | Writes JSON report |

#### `violation_prefix_grouper.py`
| Function | Brief |
|---|---|
| `group_by_prefix_depth` | Groups violations by a prefix of exactly N dot-separated segments |
| `main` | Groups violation data by configurable prefix depth |
| `write_report` | Writes JSON report |

---

### Code Extraction (3)

#### `extract.py`
*ARCHON PRIME — Application Function Extraction Pass*
| Function | Brief |
|---|---|
| `should_exclude` | Checks if a path should be excluded from scanning |
| `collect_python_files` | Collects all .py files from configured roots |
| `extract_docstrings` | Extracts docstrings from AST nodes |
| `step1_ast_parse` | Parses all discovered Python files via AST |
| `score_docstring` | Returns match info for signal keywords in a docstring |
| `is_trivial` | Returns True if a function is too simple to extract |
| `step2_filter` | Filters parsed functions by quality signals |
| `tokenize` | Tokenizes function names/docstrings |
| `build_tfidf` | Lightweight TF-IDF using pure Python |
| `step3_vectorize` | Vectorizes functions for clustering |
| `cosine_sim` / `kmeans_cosine` | Cosine-distance KMeans clustering |
| `step4_cluster` | Clusters functions by semantic similarity |
| `derive_module` | Converts file_path to dotted module notation |
| `step5_registry` / `step6_report` | Writes registry and final report |

#### `legacy_extract.py`
*ARCHON PRIME — Legacy Application Function Deep Semantic Extraction*
| Class/Function | Brief |
|---|---|
| `class ModuleAnalysis` | Full AST analysis of a single module (parse, walk, decorators, args, annotations) |
| `should_exclude` | Checks if path is in exclusion list |
| `extract_signal_keywords` | Extracts semantic signal keywords from function metadata |
| `classify_subsystems` | Maps function to subsystem based on signals |
| `infer_runtime_role` | Infers whether function is core runtime, utility, or governance |
| `infer_purpose` | Derives natural-language purpose from signals |
| `assess_salvageability` | Scores whether a function is worth preserving |
| `assess_method_salvageability` | Same assessment for class methods |
| `core_compatibility` | Evaluates compatibility with AP core runtime |
| `run` | Entry point; produces deep semantic extraction report |

#### `fbc_registry.py`
**PARSE ERROR — unexpected indent line 557**

---

### Dependency Analysis (3)

#### `cluster_analysis.py`
*ARCHON Runtime Dependency Graph Clustering Analysis*
| Function | Brief |
|---|---|
| `guess_layer` | Maps a module to an architectural layer label |
| `build_graph` | Builds directed dependency graph from import data |
| `detect_communities` | Louvain community detection on undirected graph |
| `find_sccs` | Finds strongly connected components |
| `compute_betweenness` | Computes betweenness centrality |
| `cluster_boundary_analysis` | Identifies cross-cluster dependency edges |
| `classify_violations` | Flags dependency violations against governance rules |
| `identify_facade_candidates` | Suggests modules that should be facades |
| `repair_feasibility` | Assesses whether deep imports can be repaired algorithmically |
| `write_artifacts` / `write_report` | Writes clustering artifacts and report |
| `main` | Entry point |

#### `facade_rewrite_pass.py`
*ARCHON PRIME — Facade Import Rewrite Pass*
| Function | Brief |
|---|---|
| `check_syntax` | Returns list of syntax errors, empty if clean |
| `step2_preconditions` | Validates preconditions before any mutation |
| `build_import_pattern` | Builds regex matching import lines for a target module |
| `rewrite_import_lines` | Replaces import lines for target_module with canonical facade import |
| `step3_dry_run` | Simulates every rewrite in-memory, verifies syntax |
| `step4_apply` | Writes rewritten files to disk only for changed, syntax-clean files |
| `step5_validate` | Re-scans all rewritten files for correctness |
| `main` | Entry point |

#### `facade_synthesis.py`
**PARSE ERROR — invalid syntax line 8**

---

### Dev Utilities (4)

#### `__init__.py`
Empty package initializer.

#### `conftest.py`
| Function | Brief |
|---|---|
| `pytest_collection_modifyitems` | pytest hook; modifies test collection order or filtering |

#### `python_file_list.py`
Flat script; uses `pathlib` to list Python files. No top-level functions.

#### `test_import_base_reasoning_registry.py`
**PARSE ERROR — expected `except`/`finally` block line 35**

---

### Migration (1)

#### `reorganize.py`
*ARCHON PRIME — APPLICATION_FUNCTIONS Categorical Reorganization*
| Function | Brief |
|---|---|
| `rollback_all` | Rolls back all applied file moves on failure |
| `write_report` | Writes reorganization report |

---

### Report Generation (2)

#### `registry_writer.py`
*Writes AF semantic registry entries to MODULAR_LIBRARY*
| Function | Brief |
|---|---|
| `build_entry` | Constructs a single AF registry entry |
| `write_registry` | Writes the AF registry to `MODULAR_LIBRARY/af_semantic_registry.json` |
| `write_report` | Writes JSON report |

#### `pipeline.py`
**PARSE ERROR — unexpected indent line 190**

---

### Repo Audit (4)

#### `Import_Linter.py`
*LOGOS Static Import Enforcement Linter*
| Function | Brief |
|---|---|
| `is_mathematics_path` | Returns True if path is under the Mathematics subsystem |
| `scan_file` | Scans a single file for import violations |
| `main` | Entry point; runs linter across all repo Python files |
| `write_report` | Writes violation report |

#### `scanner.py`
*Repository Python source file scanner*
| Function | Brief |
|---|---|
| `scan` | Yields all .py files under root, skipping ignored directories |
| `collect` | Returns sorted list of all scannable .py files |
| `write_report` | Writes JSON report |

#### `triage.py`
*ARCHON PRIME — Legacy Module Triage and Extraction*
| Function | Brief |
|---|---|
| `should_exclude` | Returns True if path is in exclusion list |
| `read_source` / `try_parse` | Reads and attempts to parse a Python file |
| `is_stub` | Returns `(is_stub, reason)` for a module |
| `score_signals` | Scores a module against semantic signal keywords |
| `classify_module` | Returns `REASONING`, `UTILITY`, or `UNCLASSIFIED` |
| `find_duplicates` | Compares pairs within destination groups for similarity |
| `safe_move` | Moves a file with rollback on failure |
| `run` | Entry point; triages all legacy modules |

#### `repo_structure_export.py`
*(See AP V1 Salvage section — collision kept the V1 version)*

---

### Runtime Diagnostics (4)

#### `runtime_callgraph_extractor.py`
| Function | Brief |
|---|---|
| `extract_imports` | Returns all imported module names from a single Python file |
| `build_callgraph` | Walks AST from each entry-point file, following discovered .py paths |
| `main` | Entry point; writes call graph artifact |
| `write_report` | Writes JSON report |

#### `runtime_debug_artifact_scanner.py`
| Function | Brief |
|---|---|
| `scan_file` | Scans a single file for debug artifacts (print, breakpoint, etc.) |
| `main` | Entry point; scans all repo files for debug remnants |
| `write_report` | Writes JSON report |

#### `runtime_execution_tracer.py`
| Class/Function | Brief |
|---|---|
| `class ExecutionTracer` | Collects call-edge records via `sys.settrace` |
| `.trace_calls` | Trace function registered with `sys.settrace` |
| `main` | Entry point; runs tracer and writes call-edge artifact |
| `write_report` | Writes JSON report |

#### `runtime_module_tree_auditor.py`
| Function | Brief |
|---|---|
| `audit_module` | Extracts classes, functions, imports, and LOC from a single .py file |
| `main` | Entry point; audits all modules and writes tree artifact |
| `write_report` | Writes JSON report |

---

### Static Analysis (8)

#### `ast_parser.py`
*AST-based function extraction from Python source files*
| Function | Brief |
|---|---|
| `_imports_from_tree` | Returns all imported names from an AST tree |
| `_build_signature` | Builds a string signature for a function node |
| `_body_summary` | Returns compact summary of what the function body does |
| `parse_file` | Parses a Python file and returns a list of function records |
| `write_report` | Writes JSON report |

#### `classifier.py`
*Keyword-based function classification into DRAC AF categories*
| Function | Brief |
|---|---|
| `classify` | Returns best-matching DRAC AF category for a function |
| `classify_record` | Convenience wrapper accepting an ast_parser record dict |
| `write_report` | Writes JSON report |

#### `drac_indexer.py`
*ARCHON PRIME — DRAC Application Function Master Index Builder*
| Function | Brief |
|---|---|
| `_parse_module` | Returns extracted metadata from a Python source file |
| `_assign_cluster` | Assigns a function to a DRAC cluster |
| `_load_packet_data` | Returns `stem → {classification, packet_id, external_deps}` from `module_packets.json` |
| `_compat_tags` | Derives compatibility tags from module metadata |
| `run` | Entry point; builds and writes the DRAC master function index |
| `write_report` | Writes JSON report |

#### `packet_discovery.py`
*ARCHON PRIME — Module Packet Discovery*
| Function | Brief |
|---|---|
| `collect_modules` | Returns `{module_key: Path}` for all Python files in scan roots |
| `parse_imports` | Returns list of module strings imported by a file |
| `build_graph` | Builds directed adjacency list of inter-module imports |
| `tarjan_scc` | Iterative Tarjan's SCC algorithm |
| `classify_packet` | Classifies an SCC packet by semantic signals in module names |
| `build_packet_records` | Constructs full packet record list from SCCs |
| `build_dot` | Builds a DOT graph for visualization |
| `run` | Entry point; discovers, clusters, and writes module packet artifacts |
| `write_report` | Writes JSON report |

#### `runtime_analysis.py`
*ARCHON Runtime Topology Analysis Script*
| Function | Brief |
|---|---|
| `should_skip` | Returns True if any path segment matches an excluded keyword |
| `file_to_module_path` | Converts absolute file path to dotted module path |
| `build_tree` | Builds nested directory tree structure |
| `collect_python_files` | Collects all .py files from repo root |
| `parse_imports` | Returns `(imports_list, symbol_imports_list)` for one file |
| `step5_dependency_graph` | Builds directed import dependency graph |
| `step6_runtime_surfaces` | Identifies public runtime API surfaces |
| `import_depth` | Counts package separators in a dotted path |
| `step7_deep_violations` | Detects deep import violations |
| `guess_facade_namespace` | Assigns recommended facade namespace from module path |
| `step8_facade_candidates` | Identifies modules that should expose facades |
| `step9_graphviz` | Writes DOT graph artifact |
| `step10_report` / `main` | Final report and entry point |

#### `semantic_extractor.py`
*Derives the minimal semantic modifier expression for a function*
| Function | Brief |
|---|---|
| `_tokenize` | Splits snake_case and camelCase name into lowercase tokens |
| `extract` | Returns the smallest semantic modifier expression for a function |
| `extract_record` | Convenience wrapper accepting an ast_parser record dict |
| `write_report` | Writes JSON report |

#### `static_ast_analysis.py`
| Function | Brief |
|---|---|
| `file_to_module_path` | Converts file path to dotted module path |
| `classify_layer` | Assigns an architectural layer label to a module |
| `extract_imports` | Extracts import statements from a file |
| `main` | Entry point; runs static AST analysis across all repo modules |
| `write_report` | Writes JSON report |

#### `generate_symbol_import_index.py`
*(See AP V1 Salvage section — collision kept the V1 version)*

---

## SUMMARY

| Category | Count | Notes |
|---|---|---|
| AP V1 Salvage | 5 | `_run_audit`, `ap_artifact_collection_p1`, `generate_deep_import_violations`, `generate_symbol_import_index`, `repo_structure_export` |
| Architecture Validation | 8 | All parseable |
| Code Extraction | 3 | `fbc_registry.py` — PARSE ERROR |
| Dependency Analysis | 3 | `facade_synthesis.py` — PARSE ERROR |
| Dev Utilities | 4 | `test_import_base_reasoning_registry.py` — PARSE ERROR |
| Migration | 1 | Clean |
| Report Generation | 2 | `pipeline.py` — PARSE ERROR |
| Repo Audit | 4 | Clean |
| Runtime Diagnostics | 4 | Clean |
| Static Analysis | 8 | Clean |
| **Total** | **40** | **4 parse errors require repair** |

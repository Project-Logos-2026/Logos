# Dev Tooling Operations Guide
**Version:** 2.0  
**Generated:** 2026-03-11  
**Root:** `_Dev_Resources/_Dev_Scripts/Repo_Tools/`  
**Policy Reference:** `Tool_Index/Dev_Tooling_Policies.md`

---

## 1. Tool Categories

The Dev Tooling suite is organized into nine functional categories:

| Category | Directory | Tools | Destructive |
|----------|-----------|-------|-------------|
| **Repo_Audit** | `Repo_Tools/Repo_Audit/` | Import_Linter, triage, scanner, repo_structure_export | ⚠️ triage |
| **Static_Analysis** | `Repo_Tools/Static_Analysis/` | ast_parser, classifier, drac_indexer, runtime_analysis, semantic_extractor, static_ast_analysis, packet_discovery, generate_symbol_import_index | None |
| **Dependency_Analysis** | `Repo_Tools/Dependency_Analysis/` | cluster_analysis, facade_rewrite_pass, facade_synthesis, generate_deep_import_violations | ⚠️ facade_rewrite_pass |
| **Migration** | `Repo_Tools/Migration/` | reorganize | ⚠️ reorganize |
| **Code_Extraction** | `Repo_Tools/Code_Extraction/` | extract, legacy_extract, fbc_registry | None |
| **Architecture_Validation** | `Repo_Tools/Architecture_Validation/` | *(reserved)* | None |
| **Runtime_Diagnostics** | `Repo_Tools/Runtime_Diagnostics/` | *(reserved)* | None |
| **Report_Generation** | `Repo_Tools/Report_Generation/` | pipeline, registry_writer | None |
| **Dev_Utilities** | `Repo_Tools/Dev_Utilities/` | python_file_list, conftest, __init__, test_import_base_reasoning_registry | None |

---

## 2. Capability Index

### Repo Scanning & Auditing
| Capability | Tool | Category |
|------------|------|----------|
| `python_file_discovery` | scanner | Repo_Audit |
| `import_violation_scan` | Import_Linter | Repo_Audit |
| `namespace_enforcement` | Import_Linter | Repo_Audit |
| `directory_tree_export` | repo_structure_export | Repo_Audit |
| `import_statement_extraction` | repo_structure_export | Repo_Audit |
| `module_classification` | triage | Repo_Audit |

### Static Analysis
| Capability | Tool | Category |
|------------|------|----------|
| `ast_traversal` | ast_parser | Static_Analysis |
| `function_extraction` | ast_parser | Static_Analysis |
| `docstring_extraction` | ast_parser | Static_Analysis |
| `import_graph_extraction` | static_ast_analysis | Static_Analysis |
| `layer_classification` | static_ast_analysis | Static_Analysis |
| `drac_af_categorization` | classifier | Static_Analysis |
| `semantic_signal_extraction` | semantic_extractor | Static_Analysis |
| `arp_csp_mtp_scoring` | semantic_extractor | Static_Analysis |
| `runtime_topology_analysis` | runtime_analysis | Static_Analysis |
| `drac_af_master_index_build` | drac_indexer | Static_Analysis |
| `import_dependency_graph_build` | packet_discovery | Static_Analysis |
| `scc_detection` | packet_discovery | Static_Analysis |
| `symbol_level_import_extraction` | generate_symbol_import_index | Static_Analysis |

### Dependency Analysis
| Capability | Tool | Category |
|------------|------|----------|
| `community_detection` | cluster_analysis | Dependency_Analysis |
| `betweenness_centrality` | cluster_analysis | Dependency_Analysis |
| `facade_candidate_identification` | cluster_analysis | Dependency_Analysis |
| `canonical_facade_derivation` | facade_synthesis | Dependency_Analysis |
| `rewrite_mapping_generation` | facade_synthesis | Dependency_Analysis |
| `deep_import_violation_scan` | generate_deep_import_violations | Dependency_Analysis |
| `source_file_rewrite` | facade_rewrite_pass | Dependency_Analysis |
| `ast_verified_dry_run` | facade_rewrite_pass | Dependency_Analysis |

### Code Extraction
| Capability | Tool | Category |
|------------|------|----------|
| `application_function_extraction` | extract | Code_Extraction |
| `legacy_function_extraction` | legacy_extract | Code_Extraction |
| `fbc_master_registry_build` | fbc_registry | Code_Extraction |
| `fbc_taxonomy_generation` | fbc_registry | Code_Extraction |

### Report Generation
| Capability | Tool | Category |
|------------|------|----------|
| `af_extraction_orchestration` | pipeline | Report_Generation |
| `af_registry_entry_write` | registry_writer | Report_Generation |
| `deterministic_af_id_assignment` | registry_writer | Report_Generation |

### Migration
| Capability | Tool | Category |
|------------|------|----------|
| `categorical_file_relocation` | reorganize | Migration |
| `move_only_pass` | reorganize | Migration |

---

## 3. Recommended Execution Workflows

### Workflow A: Full Repository Audit
Purpose: Assess current import health, violations, and structure.

```
Step 1 — Scan repo structure:
    python3 Repo_Tools/Repo_Audit/repo_structure_export.py
    → Produces: repo_directory_tree.json, repo_python_files.json, repo_imports.json

Step 2 — Run import linter:
    python3 Repo_Tools/Repo_Audit/Import_Linter.py
    → Reports violations to stdout

Step 3 — Generate symbol import index:
    python3 Repo_Tools/Static_Analysis/generate_symbol_import_index.py
    → Produces: _Reports/Canonical_Import_Facade/repo_symbol_imports.json

Step 4 — Generate deep import violation dataset:
    python3 Repo_Tools/Dependency_Analysis/generate_deep_import_violations.py
    → Produces: BLUEPRINTS/Canonical_Import_Facade/Deep_Import_Violations.json
```

### Workflow B: Runtime Topology Analysis
Purpose: Map the runtime module graph, detect clusters, and identify facade candidates.

```
Step 1 — Analyze runtime topology:
    python3 Repo_Tools/Static_Analysis/runtime_analysis.py
    → Produces: ARCHON_RUNTIME_ANALYSIS/runtime_topology.json

Step 2 — Run cluster analysis:
    python3 Repo_Tools/Dependency_Analysis/cluster_analysis.py
    → Produces: ARCHON_RUNTIME_ANALYSIS/cluster_analysis.json

Step 3 — Synthesize facades:
    python3 Repo_Tools/Dependency_Analysis/facade_synthesis.py
    → Produces: BLUEPRINTS/Canonical_Import_Facade/facade_synthesis.json

Step 4 — Analyze module packets:
    python3 Repo_Tools/Static_Analysis/packet_discovery.py
    → Produces: Tools/module_packets.json, Tools/dependency_graph.dot
```

### Workflow C: DRAC AF Index Rebuild
Purpose: Rebuild the DRAC Application Function master index and FBC registry.

```
Step 1 — Extract application functions:
    python3 Repo_Tools/Code_Extraction/extract.py
    → Copies to: _Dev_Resources/STAGING/APPLICATION_FUNCTIONS/

Step 2 — Run DRAC indexer:
    python3 Repo_Tools/Static_Analysis/drac_indexer.py
    → Produces: af_master_index.json, af_cluster_index.json, af_runtime_roles.json

Step 3 — Build FBC registry:
    python3 Repo_Tools/Code_Extraction/fbc_registry.py
    → Produces: fbc_master_registry.json, fbc_taxonomy.json, fbc_tag_dictionary.json,
                af_core_compatibility_matrix.json, modular_library_manifest.json

Step 4 — Run pipeline to populate AF semantic registry:
    python3 Repo_Tools/Report_Generation/pipeline.py
    → Produces: MODULAR_LIBRARY/af_semantic_registry.json
```

### Workflow D: Static Import Graph Generation
Purpose: Produce the full static import graph for layer analysis.

```
Step 1 — Ensure python_file_list.py is current:
    python3 Repo_Tools/Static_Analysis/generate_symbol_import_index.py
    → Refreshes: repo_python_files.json (side-effect)
    (Manually update Dev_Utilities/python_file_list.py from repo_python_files.json if needed)

Step 2 — Run static AST analysis:
    python3 Repo_Tools/Static_Analysis/static_ast_analysis.py
    → Produces: _Reports/FULL_STATIC_IMPORT_GRAPH.json, _Reports/LAYER_CLASSIFIED_GRAPH.json
```

### Workflow E: Facade Import Repair (⚠️ Destructive)
Purpose: Apply canonical facade substitutions to AUTO_REPAIRABLE violations.

```
PREREQUISITE: Complete Workflows A and B first.

Step 1 — Verify violation dataset exists:
    cat BLUEPRINTS/Canonical_Import_Facade/Deep_Import_Violations.json

Step 2 — Verify rewrite table exists:
    cat BLUEPRINTS/Canonical_Import_Facade/facade_synthesis.json

Step 3 — Run dry-run and review all diffs:
    python3 Repo_Tools/Dependency_Analysis/facade_rewrite_pass.py --dry-run
    → Review ALL proposed changes before proceeding

Step 4 — [REQUIRES EXPLICIT APPROVAL] Run live pass:
    python3 Repo_Tools/Dependency_Analysis/facade_rewrite_pass.py --live
    → Rewrites source files. Verify with git diff afterwards.
```

---

## 4. Typical Use Cases

| Use Case | Recommended Workflow |
|----------|---------------------|
| Check for import violations before a commit | Workflow A (Steps 1–2) |
| Understand module clustering and boundaries | Workflow B |
| Rebuild DRAC AF index after staging changes | Workflow C |
| Generate static import graph for review | Workflow D |
| Identify facade error candidates | Workflow A + B |
| Apply import repairs (after review and approval) | Workflow E |
| Run smoke tests | `pytest Repo_Tools/Dev_Utilities/` |
| Understand repo structure | `repo_structure_export` (Workflow A Step 1) |

---

## 5. Safe Execution Procedures

### 5.1 Before Any Execution
- Run `git status` to confirm clean working tree or note any in-progress changes.
- Identify whether the tool is destructive (see `destructive_tools_index.json`).
- For destructive tools: obtain explicit authorization before proceeding.

### 5.2 Destructive Tool Protocol
1. Identify target scope: which files/directories will be affected
2. Verify no protected directories (`P1-5/`, `RGE/`, `LOGOS_SYSTEM/`) are in scope
3. Run dry-run (where available) and review output completely
4. Record the pre-execution state: `git diff`, `git stash` if needed
5. Execute live pass only after all diffs are reviewed and approved
6. Verify output: `git diff --stat`, check artifact correctness
7. Log the operation in `Systm_Audit_Logs/`

### 5.3 Tool Index Maintenance
After any structural change to `Repo_Tools/`:
1. Update `dev_scripts_manifest.json` manually or via regeneration script
2. Regenerate `dev_tool_registry.json`
3. Regenerate `dev_tool_capability_index.json` from the manifest
4. Verify no orphaned entries with: `python3 -c "import json; [print(e['script_path']) for e in json.load(open('Tool_Index/dev_tool_registry.json'))['entries']]"`

### 5.4 Environment Setup
Most tools require only the Python standard library. No external packages required except:
- `pytest` — for Dev_Utilities test scripts
- `logos` package — for `test_import_base_reasoning_registry.py`

Activate the project venv before running any tool:
```
source /workspaces/Logos/.venv/bin/activate
```

### 5.5 Governance Boundary
Dev tools must never:
- Import from `LOGOS_SYSTEM.Governance` or `_Governance` at runtime
- Write to `LOGOS_SYSTEM/` directories
- Execute or invoke runtime modules
- Grant or simulate autonomous authority

Any tool that crosses the governance boundary must be immediately flagged for human review.

---

## 6. Tool Index Artifacts Reference

| Artifact | Location | Purpose |
|----------|----------|---------|
| `dev_scripts_manifest.json` | `Tool_Index/` | Per-tool metadata: path, classification, capabilities, dependencies, artifact flags |
| `dev_tool_registry.json` | `Tool_Index/` | Full functional registry with invocation patterns, entrypoints, function lists |
| `dev_tool_capability_index.json` | `Tool_Index/` | Inverted capability-to-tool index and category summary |
| `destructive_tools_index.json` | `Tool_Index/` | Index of all destructive tools with mutation scope and safety notes |
| `Dev_Tooling_Policies.md` | `Tool_Index/` | Placement rules, registry rules, confirmation protocol, session enforcement |
| `Dev_Tooling_Operations_Guide.md` | `Tool_Index/` | This document |

---

*Operations Guide v2.0 — established as part of canonical Dev Tooling Migration, 2026-03-11*

## _Dev_Resources Directory Tree

```
_Dev_Resources/
├── Dev_Tools/
│   ├── Archive/
│   │   ├── P1-5/
│   │   │   ├── m5_validation_scan.py
│   │   │   ├── phase6_runtime_callgraph_extractor.py
│   │   │   ├── phase6b_runtime_execution_tracer.py
│   │   │   ├── phase6c_execution_core_isolation_audit.py
│   │   │   ├── Phase_2A_AST_Canonical_Root_Normalization.py
│   │   │   ├── Phase_2A_Corrected_Case_Normalization.py
│   │   │   ├── Phase_2A_Rule2_Classification.py
│   │   │   ├── Phase_2B_A_Rule2_Root_Grouping.py
│   │   │   ├── phase_2b_ast_mutator.py
│   │   │   ├── Phase_2B_Pre_Discovery_Structure_Scan.py
│   │   │   ├── phase_2c_root_existence_map.py
│   │   │   ├── phase_2d_canonical_root_expansion.py
│   │   │   ├── phase_2e_rule2_prefix_grouping.py
│   │   │   ├── Phase_2F_Prefix_String_Verification.py
│   │   │   ├── phase_2f_structural_namespace_relocation.py
│   │   │   ├── Phase_3A_Rule3_Canonical_Expansion.py
│   │   │   ├── Phase_3B_Agent_Canonical_Expansion.py
│   │   │   └── Run_Nexus_Structural_Audit.py
│   │   └── RGE/
│   │       ├── rge_audit_runner.py
│   │       ├── rge_stage10_12_smoke.py
│   │       ├── rge_stage13_16_smoke.py
│   │       ├── rge_stage17_20_smoke.py
│   │       ├── rge_stage21_24_smoke.py
│   │       ├── rge_stage25_28_smoke.py
│   │       └── rge_stage29_31_smoke.py
│   ├── Repo_Governance_Tools/
│   │   ├── abbreviation_registry_validator.py
│   │   ├── dev_resources_freeze_validator.py
│   │   ├── devscript_header_validator.py
│   │   ├── directory_structure_validator.py
│   │   ├── governance_contract_validator.py
│   │   ├── repo_policy_enforcer.py
│   │   ├── runtime_wiring_log_validator.py
│   │   └── tool_registry_validator.py
│   ├── Runtime_Tools/
│   │   ├── Architecture_Validation/
│   │   │   ├── execution_core_isolation_audit.py
│   │   │   ├── import_prefix_verifier.py
│   │   │   ├── import_root_grouping_analyzer.py
│   │   │   ├── import_violation_classifier.py
│   │   │   ├── module_root_existence_checker.py
│   │   │   ├── namespace_discovery_scan.py
│   │   │   ├── nexus_structural_audit.py
│   │   │   └── violation_prefix_grouper.py
│   │   ├── Code_Extraction/
│   │   │   ├── extract.py
│   │   │   ├── fbc_registry.py
│   │   │   └── legacy_extract.py
│   │   ├── Dependency_Analysis/
│   │   │   ├── cluster_analysis.py
│   │   │   ├── facade_rewrite_pass.py
│   │   │   ├── facade_synthesis.py
│   │   │   └── generate_deep_import_violations.py
│   │   ├── Dev_Utilities/
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── python_file_list.py
│   │   │   └── test_import_base_reasoning_registry.py
│   │   ├── Migration/
│   │   │   └── reorganize.py
│   │   ├── Repo_Audit/
│   │   │   ├── Import_Linter.py
│   │   │   ├── repo_structure_export.py
│   │   │   ├── scanner.py
│   │   │   └── triage.py
│   │   ├── Report_Generation/
│   │   │   ├── pipeline.py
│   │   │   └── registry_writer.py
│   │   ├── Runtime_Diagnostics/
│   │   │   ├── runtime_callgraph_extractor.py
│   │   │   ├── runtime_debug_artifact_scanner.py
│   │   │   ├── runtime_execution_tracer.py
│   │   │   └── runtime_module_tree_auditor.py
│   │   └── Static_Analysis/
│   │       ├── ast_parser.py
│   │       ├── classifier.py
│   │       ├── drac_indexer.py
│   │       ├── generate_symbol_import_index.py
│   │       ├── packet_discovery.py
│   │       ├── runtime_analysis.py
│   │       ├── semantic_extractor.py
│   │       └── static_ast_analysis.py
│   └── README.md
├── Developer_Notes/
│   └── External_Wrapper_Testing_Policy.md
├── Processing_Center/
│   ├── BLUEPRINTS/
│   └── STAGING/
│       ├── In_Process/
│       │   ├── EXTRACT_LOGIC/
│       │   │   ├── adaptive_engine.py
│       │   │   ├── agentic_consciousness_core.py
│       │   │   ├── bayes_update_real_time.py
│       │   │   ├── bayesian_data_parser.py
│       │   │   ├── bayesian_recursion.py
│       │   │   ├── coherence.py
│       │   │   ├── comprehensive_fractal_analysis.py
│       │   │   ├── fractal_orbit_toolkit.py
│       │   │   ├── gen_worldview_ontoprops.py
│       │   │   ├── hierarchical_bayes_network.py
│       │   │   ├── iel_overlay.py
│       │   │   ├── logos_mathematical_core.py
│       │   │   ├── Memory_Recall_Integration.py
│       │   │   ├── NLP_Wrapper_Sentence_Transformers.py
│       │   │   ├── privative_policies.py
│       │   │   ├── safety_formalisms.py
│       │   │   └── simulated_consciousness_runtime.py
│       │   ├── KEEP_VERIFY/
│       │   │   ├── action_system.py
│       │   │   ├── advanced_fractal_analyzer.py
│       │   │   ├── agent_identity.py
│       │   │   ├── arithmetic_engine.py
│       │   │   ├── autonomous_learning.py
│       │   │   ├── bayesian_inferencer.py
│       │   │   ├── bayesian_interface.py
│       │   │   ├── bayesian_nexus.py
│       │   │   ├── bayesian_updates.py
│       │   │   ├── belief_network.py
│       │   │   ├── coherence_formalism.py
│       │   │   ├── coherence_metrics.py
│       │   │   ├── export_tool_registry.py
│       │   │   ├── lambda_engine.py
│       │   │   ├── lambda_onto_calculus_engine.py
│       │   │   ├── lambda_parser.py
│       │   │   ├── modal_logic.py
│       │   │   ├── modal_reasoner.py
│       │   │   ├── modal_validator.py
│       │   │   ├── multi_modal_system.py
│       │   │   ├── proof_engine.py
│       │   │   ├── pxl_fractal_orbital_analysis.py
│       │   │   ├── pxl_modal_fractal_boundary_analysis.py
│       │   │   ├── pxl_schema.py
│       │   │   ├── PXL_World_Model.py
│       │   │   ├── relation_mapper.py
│       │   │   ├── semantic_transformers.py
│       │   │   ├── tool_introspection.py
│       │   │   ├── tool_invention.py
│       │   │   ├── tool_optimizer.py
│       │   │   ├── tool_proposal_pipeline.py
│       │   │   ├── tool_repair_proposal.py
│       │   │   └── translation_engine.py
│       │   └── NORMALIZE_INTGRATE/
│       ├── Inspection_Targets/
│       │   └── Nexus_AST_Validator.py
│       ├── Post_Processing/
│       └── Pre-Processing/
│           ├── agent/
│           │   ├── agent_nexus.py
│           │   ├── base_nexus.py
│           │   ├── evaluation_packet.py
│           │   ├── id_handler.py
│           │   ├── knowledge_catalog.py
│           │   ├── legacy_sop_nexus.py
│           │   ├── Logos_Memory_Nexus.py
│           │   ├── plan_packet.py
│           │   ├── sop_nexus.py
│           │   ├── test_agent_planner.py
│           │   ├── test_end_to_end_pipeline.py
│           │   ├── test_hardening.py
│           │   ├── test_integration_identity.py
│           │   ├── test_llm_bypass_smoke.py
│           │   ├── test_lock_unlock.py
│           │   ├── test_logos_agi_bootstrap_modes.py
│           │   ├── test_logos_agi_replay_proposals.py
│           │   ├── test_logos_runtime_phase2_smoke.py
│           │   ├── test_nexus_capability_governance.py
│           │   ├── test_pai.py
│           │   ├── test_plan_revision_on_contradiction.py
│           │   ├── test_scp_recovery_mode_gate.py
│           │   ├── test_self_improvement_cycle.py
│           │   ├── test_stub_beliefs_never_verified.py
│           │   └── test_verify_pai.py
│           ├── math/
│           │   ├── dual_bijection_demo.py
│           │   └── fractal_nexus.py
│           ├── reasoning/
│           │   ├── arp_nexus.py
│           │   ├── ergonomic_optimizer.py
│           │   ├── integration_test.py
│           │   ├── integration_test_suite.py
│           │   ├── modal_vector_sync.py
│           │   ├── resource_manager.py
│           │   ├── scp_nexus.py
│           │   ├── test_arp_nexus.py
│           │   ├── test_bayesian_data_handler.py
│           │   ├── test_dual_bijection.py
│           │   ├── test_integration.py
│           │   ├── test_logos_agi_persistence_smoke.py
│           │   ├── test_proved_grounding.py
│           │   └── uip_nexus.py
│           ├── safety/
│           │   ├── attestation.py
│           │   ├── health_server.py
│           │   ├── test_reference_monitor.py
│           │   └── test_tool_pipeline_smoke.py
│           ├── semantic/
│           │   ├── boot_system.py
│           │   ├── commitment_ledger.py
│           │   ├── dispatch.py
│           │   ├── hashing.py
│           │   ├── maintenance.py
│           │   ├── mtp_nexus_orchestrator.py
│           │   ├── nexus_manager.py
│           │   ├── ontoprops_remap.py
│           │   ├── packet_types.py
│           │   ├── prioritization.py
│           │   ├── providers_llama.py
│           │   ├── providers_openai.py
│           │   ├── test_logos_agi_adapter.py
│           │   ├── test_perception_ingestors.py
│           │   ├── test_registry_and_response.py
│           │   ├── test_simulation_cli.py
│           │   ├── test_tool_fallback_proposal.py
│           │   ├── time_utils.py
│           │   ├── transform_types.py
│           │   └── types.py
│           ├── utility/
│           │   ├── arp_nexus_orchestrator.py
│           │   ├── causal_trace_operator.py
│           │   ├── class_extrapolator.py
│           │   ├── csp_nexus_orchestrator.py
│           │   ├── development_environment.py
│           │   ├── logos_protocol_nexus.py
│           │   ├── regression_checker.py
│           │   ├── scp_nexus_orchestrator.py
│           │   ├── sop_nexus_orchestrator.py
│           │   ├── test_arp_modes.py
│           │   ├── test_determinism.py
│           │   ├── test_evaluator_learning_smoke.py
│           │   └── test_logos_agi_pin_drift.py
│           └── utils/
│               ├── _uip_connector_stubs.py
│               ├── bridge.py
│               ├── causal_chain_node_predictor.py
│               ├── check_imports.py
│               ├── check_run_cycle_prereqs.py
│               ├── config.py
│               ├── cycle_ledger.py
│               ├── evidence.py
│               ├── guardrails.py
│               ├── iel_integration.py
│               ├── iel_registryv1.py
│               ├── iel_registryv2.py
│               ├── io_normalizer.py
│               ├── iterative_loop.py
│               ├── kernel.py
│               ├── logging_utils.py
│               ├── logos_monitor.py
│               ├── ontology_inducer.py
│               ├── policy.py
│               ├── progressive_router.py
│               ├── router.py
│               ├── sanitizer.py
│               ├── schema_utils.py
│               ├── self_diagnosis.py
│               ├── shared_resources.py
│               ├── skill_acquisition.py
│               ├── smp_intake.py
│               ├── stress_sop_runtime.py
│               ├── system_utils.py
│               ├── task_intake.py
│               ├── transform_registry.py
│               ├── uip_operations.py
│               └── worker_kernel.py
├── Repo_Governance/
│   ├── Developer/
│   │   ├── Dev_Environment_Rules.md
│   │   ├── Dev_Resources_Directory_Contract.md
│   │   ├── Dev_Resources_Freeze_Protocol.md
│   │   ├── Dev_Tool_Generation_Policy.md
│   │   ├── Development_Rules.json
│   │   └── Directory_Creation_Authorization_Rules.md
│   ├── Header_Schemas/
│   │   ├── repo_governance_tool_header_schema.json
│   │   ├── runtime_module_header_schema.json
│   │   └── runtime_tool_header_schema.json
│   └── Runtime/
│       ├── Abbreviation_Usage_Policy.md
│       ├── Abbreviations.json
│       ├── Dependency_Wiring_Log_Contract.md
│       ├── Naming_Convention_Enforcement.md
│       ├── Runtime_Artifact_Formatting_Spec.md
│       ├── Runtime_Execution_Environment_Rules.md
│       └── Runtime_Module_Generation_Spec.md
├── Repo_Inventory/
│   ├── Master_Indexes/
│   │   ├── Environment/
│   │   └── Runtime/
│   └── Master_Manifests/
├── Reports/
│   ├── Audit_Outputs/
│   │   ├── DEVELOPER/
│   │   │   ├── dev_scripts/
│   │   │   │   ├── dev_script_reorganization_report.md
│   │   │   │   └── dev_script_repo_tools_completion_plan.md
│   │   │   └── governance/
│   │   ├── ENVIRONMENT/
│   │   ├── INCOMING/
│   │   └── RUNTIME/
│   │       ├── Application_Function_Extraction/
│   │       │   ├── application_function_candidates.json
│   │       │   ├── application_function_clusters.json
│   │       │   ├── application_function_embeddings.json
│   │       │   ├── application_function_filtered.json
│   │       │   ├── application_function_registry.json
│   │       │   ├── application_function_report.md
│   │       │   ├── core_compatibility_hints.json
│   │       │   ├── module_salvage_report.md
│   │       │   ├── module_semantic_profiles.json
│   │       │   ├── reorganization_report.json
│   │       │   └── salvageable_function_blocks.json
│   │       ├── Canonical_Import_Facade/
│   │       │   ├── import_architecture/
│   │       │   │   ├── architecture_dependency_graph.json
│   │       │   │   ├── architecture_edge_classification.json
│   │       │   │   ├── architecture_metrics.json
│   │       │   │   ├── architecture_validation_report.md
│   │       │   │   ├── auto_repair_plan.md
│   │       │   │   ├── boundary_repair_changes.json
│   │       │   │   ├── boundary_repair_report.md
│   │       │   │   ├── boundary_repair_summary.json
│   │       │   │   ├── boundary_repair_validation.json
│   │       │   │   ├── boundary_violation_report.json
│   │       │   │   ├── cluster_boundary_violations.json
│   │       │   │   ├── cluster_dependency_graph.json
│   │       │   │   ├── cluster_map.json
│   │       │   │   ├── cluster_membership.json
│   │       │   │   ├── cluster_summary.json
│   │       │   │   ├── facade_map.json
│   │       │   │   ├── facade_rewrite_changes.json
│   │       │   │   ├── facade_rewrite_report.md
│   │       │   │   ├── facade_rewrite_summary.json
│   │       │   │   ├── facade_rewrite_validation.json
│   │       │   │   ├── facade_surface_spec.json
│   │       │   │   ├── IMPORT_ARCHITECTURE_INDEX.md
│   │       │   │   ├── IMPORT_DEBUG_GUIDE.md
│   │       │   │   ├── import_rewrite_table.json
│   │       │   │   ├── import_toolkit_consolidation_report.md
│   │       │   │   ├── Phase_8_Step_1_Q1_Import_Trace.md
│   │       │   │   ├── repair_feasibility_cluster.json
│   │       │   │   ├── repair_feasibility_facade.json
│   │       │   │   ├── runtime_deep_import_violations.json
│   │       │   │   ├── runtime_dependency_graph.dot
│   │       │   │   ├── runtime_dependency_graph.json
│   │       │   │   ├── runtime_dependency_graph.png
│   │       │   │   ├── runtime_directory_tree.json
│   │       │   │   ├── runtime_imports.json
│   │       │   │   ├── runtime_python_files.json
│   │       │   │   ├── runtime_surface_modules.json
│   │       │   │   ├── runtime_symbol_imports.json
│   │       │   │   └── runtime_topology_report.md
│   │       │   ├── Import_Facade/
│   │       │   │   ├── Canonical_Import_Facade_Blueprint.md
│   │       │   │   └── Canonical_Import_Facade_Integration_Plan.md
│   │       │   ├── Reports/
│   │       │   │   ├── Architecture_Verification/
│   │       │   │   │   ├── arp_packets.json
│   │       │   │   │   ├── Canonical_Trees_and_Import_Roots.json
│   │       │   │   │   ├── Deep_Import_Violations.json
│   │       │   │   │   ├── module_extraction_summary.json
│   │       │   │   │   ├── module_packet_graph.json
│   │       │   │   │   ├── module_packets.json
│   │       │   │   │   ├── modules_deleted.json
│   │       │   │   │   ├── reasoning_modules_moved.json
│   │       │   │   │   ├── reasoning_packets.json
│   │       │   │   │   ├── repo_directory_tree.json
│   │       │   │   │   ├── repo_symbol_imports.json
│   │       │   │   │   ├── runtime_surface_audit.json
│   │       │   │   │   ├── semantic_packets.json
│   │       │   │   │   └── utility_modules_moved.json
│   │       │   │   └── Facade_Rewrite_Pass/
│   │       │   │       ├── canonical_facade_candidates.json
│   │       │   │       ├── facade_rewrite_failure.json
│   │       │   │       ├── privation_mathematics_problems_report.json
│   │       │   │       ├── repo_imports.json
│   │       │   │       ├── repo_python_files.json
│   │       │   │       └── RGE_CIF_Audit.json
│   │       │   └── Runtime_Cluster_Analysis/
│   │       │       ├── cluster_analysis_report.md
│   │       │       ├── facade_candidates.json
│   │       │       ├── Runtime_Spine_Manifest.json
│   │       │       └── Runtime_Surface_Full_Core_Manifest.json
│   │       ├── Misc_Artifacts/
│   │       │   ├── print_call_categorized.json
│   │       │   ├── print_classification_alignment_report.py
│   │       │   ├── runtime_print_classification.json
│   │       │   └── runtime_print_inventory.json
│   │       ├── Module_Logic_Salvage_Pass/
│   │       │   ├── module_triage_report.md
│   │       │   ├── reasoning_triage_report.md
│   │       │   ├── utils_logic_salvage_report.md
│   │       │   └── utils_recovery_scan_report.md
│   │       ├── P1-7/
│   │       │   ├── Phase1_Data_Gathering/
│   │       │   │   ├── broken_imports_consolidated.json
│   │       │   │   ├── FULL_RUNTIME_DEPENDENCY_MAP.json
│   │       │   │   └── P1_Runtime_Activation_Delta_Report.md
│   │       │   ├── Phase2_Normalization/
│   │       │   │   ├── Phase_2A_AST_Mutation_Report.json
│   │       │   │   ├── Phase_2A_Corrected_Mutation_Report.json
│   │       │   │   ├── Phase_2A_Mutation_Report.json
│   │       │   │   ├── Phase_2A_Post_Mutation_Lint.json
│   │       │   │   ├── Phase_2A_Rule2_Classification.json
│   │       │   │   ├── Phase_2B_Mutation_Report.json
│   │       │   │   ├── Phase_2B_Pre_Discovery_Structure.json
│   │       │   │   ├── Phase_2B_Root_Grouping.json
│   │       │   │   ├── Phase_2C_Root_Existence_Map.json
│   │       │   │   ├── Phase_2D_Canonical_Expansion_Mutation_Report.json
│   │       │   │   ├── Phase_2E_Rule2_Prefix_Grouping.json
│   │       │   │   ├── Phase_2F_Prefix_String_Verification.json
│   │       │   │   └── Phase_2F_Structural_Relocation_Mutation_Report.json
│   │       │   ├── Phase3_Nexus/
│   │       │   │   ├── Authoritative_Nexus_Qualification_Audit.json
│   │       │   │   ├── Authoritative_Structural_Nexus_Audit_v2.json
│   │       │   │   ├── Authoritative_Structural_Nexus_Audit_v3.json
│   │       │   │   ├── Authoritative_Structural_Nexus_Audit_v4.json
│   │       │   │   ├── Authoritative_Structural_Nexus_Audit_v5.json
│   │       │   │   ├── Authoritative_Structural_Nexus_Audit_v6.json
│   │       │   │   ├── Full_Nexus_Audit.json
│   │       │   │   ├── Full_Nexus_Contract_Compliance_Matrix.json
│   │       │   │   ├── Full_Nexus_Contract_Gap_Summary.json
│   │       │   │   ├── NEXUS_STRUCTURAL_AUDIT_v1.json
│   │       │   │   ├── Nexus_Structural_Extraction_Artifact.json
│   │       │   │   ├── P3_2_Orchestration_Wiring_Blueprint.md
│   │       │   │   ├── Phase_3A_Residual_Rule3_Classification.json
│   │       │   │   ├── Phase_3A_Rule3_Canonical_Expansion_Report.json
│   │       │   │   ├── Phase_3B_Agent_Canonical_Expansion_Report.json
│   │       │   │   ├── Phase_4A_Rule4_Structural_Classification.json
│   │       │   │   ├── Target_16_Meta_Nexus_Gap_Report.json
│   │       │   │   ├── Target_16_Meta_Nexus_Map.json
│   │       │   │   └── Tier1_Nexus_Formalization_Audit.json
│   │       │   ├── Phase4_Transition/
│   │       │   │   ├── Full_Runtime_Core_Structure.json
│   │       │   │   ├── Import_Audit_Local.json
│   │       │   │   ├── Import_Linter_Report.json
│   │       │   │   ├── P1_P4_Compliance_Audit_Report.json
│   │       │   │   ├── Phase_4B_Import_Star_Elimination_Report.json
│   │       │   │   ├── Phase_4D_Startup_SysPath_Remediation_Report.json
│   │       │   │   ├── Runtime_Directory_Discovery.json
│   │       │   │   └── Targeted_Structural_Leak_Scan.json
│   │       │   ├── Phase5_Reconciliation/
│   │       │   │   ├── CONFLICT_DECISION_MAP.json
│   │       │   │   ├── DOCUMENTATION.txt
│   │       │   │   ├── FETCH_HEAD
│   │       │   │   ├── GOVERNANCE_FILES.txt
│   │       │   │   ├── HIGH_RISK_FILES.txt
│   │       │   │   ├── IMPORT_SURFACE.txt
│   │       │   │   ├── LOW_RISK_FILES.txt
│   │       │   │   ├── MEDIUM_RISK_FILES.txt
│   │       │   │   ├── NEXUS_FILES.txt
│   │       │   │   ├── P5_Full_Core_Runtime_Audit_Report.json
│   │       │   │   ├── P5_Full_Runtime_Spine_Audit_Report.json
│   │       │   │   ├── PHASE5_BRANCH_DIFF_FULL.txt
│   │       │   │   ├── PHASE5_CHANGED_FILES.txt
│   │       │   │   ├── PHASE5_FULL_CONFLICT_FILE_LIST.txt
│   │       │   │   ├── PHASE5_RUNTIME_DIFF_REVIEW.txt
│   │       │   │   ├── PHASE5_RUNTIME_SURFACE_ONLY.txt
│   │       │   │   ├── PHASE5_RUNTIME_UNMERGED.txt
│   │       │   │   ├── PHASE5_STRUCTURAL_SURFACE_DIFF.txt
│   │       │   │   ├── Phase_5_Full_Nexus_Behavioral_Sweep.json
│   │       │   │   ├── Phase_5_Runtime_Behavioral_Sweep.json
│   │       │   │   ├── Phase_5_Runtime_Import_Normalization_Audit.json
│   │       │   │   ├── Phase_5_Runtime_Import_Normalization_Final.json
│   │       │   │   ├── Phase_5_Runtime_Import_Normalization_Reconciliation.json
│   │       │   │   ├── Phase_5_Runtime_Integration_Exit.md
│   │       │   │   ├── Phase_5_Runtime_Surface_Pre_Freeze_Audit.json
│   │       │   │   ├── Phase_5A_Dynamic_Import_Classification.json
│   │       │   │   ├── Phase_5D_LLM_Subsystem_Removal_Report.json
│   │       │   │   ├── RUNTIME_CORE.txt
│   │       │   │   ├── SUMMARY.txt
│   │       │   │   └── TEST_FILES.txt
│   │       │   ├── Phase6_Runtime_CallGraph/
│   │       │   │   ├── PHASE6_RUNTIME_ADJACENCY_MAP.json
│   │       │   │   ├── PHASE6_RUNTIME_DYNAMIC_IMPORT_SITES.json
│   │       │   │   ├── PHASE6_RUNTIME_EVAL_EXEC_SITES.json
│   │       │   │   ├── PHASE6_RUNTIME_EXCLUDED_MODULES.json
│   │       │   │   ├── PHASE6_RUNTIME_REACHABLE_MODULES.json
│   │       │   │   ├── PHASE6_RUNTIME_SYS_PATH_SITES.json
│   │       │   │   ├── PHASE6B_AGENT_BOOT_SEQUENCE.json
│   │       │   │   ├── PHASE6B_DRAC_TOUCHPOINTS.json
│   │       │   │   ├── PHASE6B_EXECUTION_CALL_GRAPH.json
│   │       │   │   ├── PHASE6B_EXECUTION_CALL_TRACE_RAW.json
│   │       │   │   ├── PHASE6B_MODULE_LOAD_SEQUENCE.json
│   │       │   │   ├── PHASE6B_RUNTIME_BRIDGE_TOUCHPOINTS.json
│   │       │   │   ├── PHASE6C_ENTRYPOINT_VALIDATION.json
│   │       │   │   ├── PHASE6C_EXECUTION_BOUNDARIES.json
│   │       │   │   ├── PHASE6C_EXECUTION_CALL_GRAPH.json
│   │       │   │   ├── PHASE6C_EXECUTION_HYGIENE_REPORT.json
│   │       │   │   ├── PHASE6C_EXECUTION_MODULE_LOAD_ORDER.json
│   │       │   │   ├── PHASE6C_EXECUTION_REACHABLE_MODULES.json
│   │       │   │   ├── PHASE6C_RECURSIVE_IMPORT_VALIDATION.json
│   │       │   │   └── Phase_6_Epistemic_Library_Exit.md
│   │       │   ├── Phase7A_Runtime_Control/
│   │       │   │   ├── CONTROL_A_IMPORT_GRAPH.json
│   │       │   │   ├── CONTROL_A_MODULE_LIST.json
│   │       │   │   ├── DEPENDENCY_LAYER_VIOLATIONS.json
│   │       │   │   ├── FULL_STATIC_IMPORT_GRAPH.json
│   │       │   │   ├── LAYER_BOUNDARY_VIOLATIONS.json
│   │       │   │   ├── LAYER_CLASSIFIED_GRAPH.json
│   │       │   │   ├── Phase7_Layer_Schema.json
│   │       │   │   ├── PHASE7A_SUMMARY.md
│   │       │   │   ├── RUNTIME_CONTROL_DYNAMIC_AUDIT.json
│   │       │   │   ├── RUNTIME_CONTROL_IMPORT_GRAPH.json
│   │       │   │   ├── RUNTIME_CONTROL_LAYER_CLASSIFIED.json
│   │       │   │   ├── RUNTIME_CONTROL_LAYER_VIOLATIONS.json
│   │       │   │   ├── RUNTIME_CONTROL_MODULE_LIST.json
│   │       │   │   ├── RUNTIME_CONTROL_MODULE_LIST_CHECK.json
│   │       │   │   ├── RUNTIME_CONTROL_SUMMARY.md
│   │       │   │   └── RUNTIME_DYNAMIC_EXECUTION_AUDIT.json
│   │       │   ├── Phase7B_Runtime_Call_Flow/
│   │       │   │   └── Phase7B_Runtime_Call_Flow.json
│   │       │   ├── m5_refined_report.json
│   │       │   └── m5_validation_report.json
│   │       └── RGE_Audit_Reports/
│   │           ├── RGE_Stage0_Baseline/
│   │           │   ├── RGE_CIF_Compliance_Preflight.json
│   │           │   ├── RGE_Directory_Snapshot.json
│   │           │   ├── RGE_Import_Surface_Report.json
│   │           │   ├── RGE_Module_Disposition_Check.json
│   │           │   ├── RGE_Module_Inventory.json
│   │           │   └── RGE_Obsolete_Module_Report.json
│   │           ├── RGE_Stage_Analysis/
│   │           │   ├── RGE_Stage10_12_Field_Topology.json
│   │           │   ├── RGE_Stage13_16_Topology_Graph.json
│   │           │   ├── RGE_Stage17_20_Packet_Propagation.json
│   │           │   ├── RGE_Stage21_24_Cognition_Broadcast.json
│   │           │   ├── RGE_Stage25_28_Runtime_Bridge.json
│   │           │   ├── RGE_Stage29_31_Activation.json
│   │           │   └── RGE_Stage7_9_Recursion_Routing.json
│   │           ├── RGE_Architecture_Compliance.json
│   │           ├── RGE_Audit_Report.json
│   │           ├── RGE_Audit_Report.md
│   │           ├── RGE_Dependency_Graph.json
│   │           ├── RGE_Final_Audit_Report.json
│   │           ├── RGE_Module_Inventory.json
│   │           └── RGE_Workflow_Metrics.json
│   ├── Execution_Reports/
│   │   ├── _Dev_Governance/
│   │   │   ├── governance_artifact_generation_report.json
│   │   │   ├── governance_tools_generation_report.json
│   │   │   └── runtime_tool_header_injection_report.json
│   │   └── Tool_Outputs/
│   │       ├── Module_Recovery/
│   │       └── Runtime/
│   │           └── runtime_tools_generation_report.json
│   └── Test_Artifacts/
│       └── Tier_1_Test_Run_After_DeductiveEngine_Fix.txt
└── Tool_Index/
    ├── destructive_tools_index.json
    ├── dev_scripts_inventory.json
    ├── dev_scripts_manifest.json
    ├── dev_tool_capability_index.json
    ├── dev_tool_registry.json
    ├── Dev_Tooling_Operations_Guide.md
    └── Dev_Tooling_Policies.md
```

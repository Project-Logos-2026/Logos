# LOGOS Logic Atom Extraction Plan

```
Artifact Type   : Blueprint — Phase-3 Module Recovery
Tool Chain      : Runtime_Tools/Static_Analysis (ast_parser, classifier)
                  Runtime_Tools/Code_Extraction (legacy_extract)
Dataset Path    : _Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery
Staging Path    : _Dev_Resources/Processing_Center/STAGING/Pre-Processing
Output Path     : _Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/
                  LOGIC_ATOM_EXTRACTION_PLAN.md
Generated       : 2026-03-12
Schema Version  : 1.0
Status          : COMPLETE
```

---

## SECTION 1 — Dataset Summary

### Dev Environment Validation

| Directory | Status |
|-----------|--------|
| `_Dev_Resources` | CONFIRMED |
| `_Dev_Resources/Dev_Tools` | CONFIRMED |
| `_Dev_Resources/Dev_Tools/Runtime_Tools` | CONFIRMED |
| `_Dev_Resources/Processing_Center/STAGING` | CONFIRMED |

### Runtime Tools Invoked

| Tool | Category | Purpose |
|------|----------|---------|
| `ast_parser.py` | Static_Analysis | AST-based function extraction |
| `classifier.py` | Static_Analysis | Keyword-based DRAC AF classification |
| `legacy_extract.py` | Code_Extraction | Deep semantic extraction pipeline |
| `triage.py` | Repo_Audit | Module triage and classification |

### Dataset Inventory

| Dataset File | Records | Status |
|-------------|---------|--------|
| `legacy_module_inventory.json` | 161 modules | VALID |
| `legacy_module_classification.json` | 161 modules | VALID |
| `legacy_recovery_candidates.json` | 161 modules | VALID |
| `legacy_dependency_graph.json` | 161 nodes | VALID |
| `legacy_call_graph.json` | 161 modules | VALID |
| `legacy_import_surface.json` | 161 modules | VALID |
| `legacy_symbol_registry.json` | 161 modules | VALID |
| `legacy_side_effect_map.json` | 161 modules | VALID |

### Staged Module Inventory

| Staging Subdirectory | Module Count |
|---------------------|-------------|
| `EXTRACT_LOGIC` | 17 |
| `KEEP_VERIFY` | 33 |
| `NORMALIZE_INTGRATE` | 0 |
| `agent` | 25 |
| `math` | 2 |
| `reasoning` | 14 |
| `safety` | 4 |
| `semantic` | 20 |
| `utility` | 13 |
| `utils` | 33 |
| **TOTAL** | **161** |

### Extraction Metrics

| Metric | Value |
|--------|-------|
| Total Modules Analyzed | 161 |
| Donor Modules | 92 |
| Extractable Logic Atoms | 287 |
| Rejected Modules | 66 |
| Reconstruction Targets | 3 |

### Primitive Library Distribution

| Library | Atom Count |
|---------|-----------|
| `REASONING_PRIMITIVES` | 114 |
| `SCHEMA_PRIMITIVES` | 57 |
| `VALIDATION_PRIMITIVES` | 46 |
| `UTILITY_PRIMITIVES` | 45 |
| `NORMALIZATION_PRIMITIVES` | 25 |

### Classification Distribution (Source)

| Classification | Module Count |
|----------------|-------------|
| Reasoning | 51 |
| Utility | 35 |
| Validation | 15 |
| Schema_Handling | 15 |
| Orchestration | 15 |
| Semantic_Processing | 13 |
| External_Dependency | 7 |
| Runtime_Support | 5 |
| Legacy_Shim | 2 |
| Data_Transformation | 2 |
| Interface_Binding | 1 |

### Recovery Status Distribution

| Recovery Status | Module Count |
|----------------|-------------|
| Recoverable_As_Is | 102 |
| Recoverable_With_Normalization | 42 |
| Recoverable_By_Extraction_Only | 12 |
| Partial_Salvage_Only | 5 |

---

## SECTION 2 — Donor Module Table

All modules tagged DONOR have passed the following qualification gates:

- Classification is in: Utility, Reasoning, Validation, Schema_Handling, Semantic_Processing, or Data_Transformation
- No network or subprocess side effects
- Active side-effect count fewer than 2

| Module Name | Classification | Dep Count | Side-Effect Profile | Recovery Status |
|------------|---------------|-----------|---------------------|-----------------|
| `transform_types` | Data_Transformation | 0 | PURE | Recoverable_As_Is |
| `io_normalizer` | Data_Transformation | 0 | PURE | Recoverable_As_Is |
| `bayes_update_real_time` | Reasoning | 0 | ISOLATED:file_io | Recoverable_With_Normalization |
| `bayesian_data_parser` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `bayesian_recursion` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `coherence` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `comprehensive_fractal_analysis` | Reasoning | 0 | ISOLATED:file_io | Recoverable_With_Normalization |
| `fractal_orbit_toolkit` | Reasoning | 0 | PURE | Recoverable_With_Normalization |
| `hierarchical_bayes_network` | Reasoning | 0 | ISOLATED:file_io | Recoverable_With_Normalization |
| `logos_mathematical_core` | Reasoning | 0 | PURE | Recoverable_With_Normalization |
| `privative_policies` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `safety_formalisms` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `advanced_fractal_analyzer` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `arithmetic_engine` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `bayesian_inferencer` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `bayesian_interface` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `bayesian_nexus` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `belief_network` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `coherence_formalism` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `coherence_metrics` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `lambda_engine` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `lambda_onto_calculus_engine` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `modal_logic` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `modal_reasoner` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `modal_validator` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `multi_modal_system` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `proof_engine` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `pxl_fractal_orbital_analysis` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `pxl_modal_fractal_boundary_analysis` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `relation_mapper` | Reasoning | 0 | ISOLATED:global_state | Recoverable_With_Normalization |
| `tool_optimizer` | Reasoning | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `fractal_nexus` | Reasoning | 0 | ISOLATED:file_io | Recoverable_With_Normalization |
| `arp_nexus` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `ergonomic_optimizer` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `modal_vector_sync` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `resource_manager` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `scp_nexus` | Reasoning | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `uip_nexus` | Reasoning | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `evidence` | Reasoning | 0 | PURE | Recoverable_As_Is |
| `pxl_schema` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `evaluation_packet` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `id_handler` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `knowledge_catalog` | Schema_Handling | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `plan_packet` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `dual_bijection_demo` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `packet_types` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `types` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `guardrails` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `schema_utils` | Schema_Handling | 0 | PURE | Recoverable_As_Is |
| `gen_worldview_ontoprops` | Semantic_Processing | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `lambda_parser` | Semantic_Processing | 0 | PURE | Recoverable_As_Is |
| `translation_engine` | Semantic_Processing | 0 | PURE | Recoverable_As_Is |
| `agent_nexus` | Semantic_Processing | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `hashing` | Semantic_Processing | 0 | PURE | Recoverable_As_Is |
| `mtp_nexus_orchestrator` | Semantic_Processing | 0 | PURE | Recoverable_With_Normalization |
| `ontoprops_remap` | Semantic_Processing | 0 | ISOLATED:file_io | Recoverable_With_Normalization |
| `prioritization` | Semantic_Processing | 0 | PURE | Recoverable_As_Is |
| `time_utils` | Semantic_Processing | 0 | PURE | Recoverable_As_Is |
| `Memory_Recall_Integration` | Utility | 0 | PURE | Recoverable_With_Normalization |
| `adaptive_engine` | Utility | 0 | PURE | Recoverable_As_Is |
| `bayesian_updates` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `export_tool_registry` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `tool_introspection` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `class_extrapolator` | Utility | 0 | PURE | Recoverable_As_Is |
| `development_environment` | Utility | 0 | PURE | Recoverable_As_Is |
| `regression_checker` | Utility | 0 | PURE | Recoverable_As_Is |
| `bridge` | Utility | 0 | PURE | Recoverable_As_Is |
| `causal_chain_node_predictor` | Utility | 0 | PURE | Recoverable_As_Is |
| `check_imports` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `check_run_cycle_prereqs` | Utility | 0 | PURE | Recoverable_As_Is |
| `cycle_ledger` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `iel_integration` | Utility | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `iel_registryv1` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `iel_registryv2` | Utility | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `iterative_loop` | Utility | 0 | PURE | Recoverable_As_Is |
| `kernel` | Utility | 0 | PURE | Recoverable_As_Is |
| `logging_utils` | Utility | 0 | PURE | Recoverable_As_Is |
| `logos_monitor` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `ontology_inducer` | Utility | 0 | PURE | Recoverable_As_Is |
| `policy` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `progressive_router` | Utility | 0 | PURE | Recoverable_As_Is |
| `router` | Utility | 0 | ISOLATED:file_io | Recoverable_As_Is |
| `sanitizer` | Utility | 0 | PURE | Recoverable_As_Is |
| `self_diagnosis` | Utility | 0 | PURE | Recoverable_As_Is |
| `skill_acquisition` | Utility | 0 | PURE | Recoverable_As_Is |
| `smp_intake` | Utility | 0 | PURE | Recoverable_As_Is |
| `system_utils` | Utility | 0 | ISOLATED:global_state | Recoverable_As_Is |
| `task_intake` | Utility | 0 | PURE | Recoverable_As_Is |
| `transform_registry` | Utility | 0 | PURE | Recoverable_As_Is |
| `action_system` | Validation | 0 | PURE | Recoverable_As_Is |
| `attestation` | Validation | 0 | PURE | Recoverable_As_Is |
| `commitment_ledger` | Validation | 0 | ISOLATED:file_io | Recoverable_As_Is |

---

## SECTION 3 — Extractable Logic Atoms

Atoms extracted using `ast_parser.py` function enumeration and
`classifier.py` DRAC AF categorization, with side-effect safety screening
applied per `legacy_side_effect_map.json`.

### REASONING_PRIMITIVES (114 atoms)

| Atom Name | Source Module | Atom Type | Side-Effect Profile | Dependencies | Target Library |
|-----------|--------------|-----------|---------------------|-------------|----------------|
| `analyze_fractal_iterations` | `advanced_fractal_analyzer` | stateless_helper | PURE | collections, dataclasses, typing | REASONING_PRIMITIVES |
| `initialize_logos_agent_nexus` | `agent_nexus` | pure_utility | ISOLATED:global_state | dataclasses, datetime, enum, typing | REASONING_PRIMITIVES |
| `_apply_provisional_proof_tagging` | `arp_nexus` | reasoning_primitive | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_build_span_mapping` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_contains_pxl_fragments` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_derive_polarity` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_extract_proof_refs` | `arp_nexus` | reasoning_primitive | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_payload_is_smp` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_pxl_key_match` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `_tag_append_artifact` | `arp_nexus` | stateless_helper | PURE | dataclasses, datetime, enum, typing, uuid | REASONING_PRIMITIVES |
| `assign_confidence` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `filter_and_score` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `load_priors` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `predictive_refinement` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `resolve_priors_path` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `save_priors` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `score_data_point` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `_disabled` | `bayesian_data_parser` | pure_utility | ISOLATED:file_io | datetime, json, typing | REASONING_PRIMITIVES |
| `FalseP` | `bayesian_interface` | stateless_helper | PURE | dataclasses, typing | REASONING_PRIMITIVES |
| `TrueP` | `bayesian_interface` | stateless_helper | PURE | dataclasses, typing | REASONING_PRIMITIVES |
| `UncertainP` | `bayesian_interface` | stateless_helper | PURE | dataclasses, typing | REASONING_PRIMITIVES |
| `_apply_provisional_proof_tagging` | `bayesian_nexus` | reasoning_primitive | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_build_span_mapping` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_contains_pxl_fragments` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_derive_polarity` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_extract_proof_refs` | `bayesian_nexus` | reasoning_primitive | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_payload_is_smp` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_pxl_key_match` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_tag_append_artifact` | `bayesian_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `analyze_all_fractals` | `comprehensive_fractal_analysis` | pure_utility | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `create_visual_summary` | `comprehensive_fractal_analysis` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `generate_comprehensive_report` | `comprehensive_fractal_analysis` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `generate_julia_set` | `comprehensive_fractal_analysis` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `legacy_main` | `comprehensive_fractal_analysis` | pure_utility | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `load_canonical_c_values` | `comprehensive_fractal_analysis` | pure_utility | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_as_posix` | `evidence` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `_sort_key` | `evidence` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `evidence_to_citation_string` | `evidence` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `_apply_provisional_proof_tagging` | `fractal_nexus` | reasoning_primitive | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_build_span_mapping` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_contains_pxl_fragments` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_derive_polarity` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_extract_proof_refs` | `fractal_nexus` | reasoning_primitive | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_payload_is_smp` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_pxl_key_match` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `_tag_append_artifact` | `fractal_nexus` | stateless_helper | ISOLATED:file_io | json, typing | REASONING_PRIMITIVES |
| `fix_pm` | `gen_worldview_ontoprops` | stateless_helper | ISOLATED:file_io | hashlib, json, re | REASONING_PRIMITIVES |
| `fmt` | `gen_worldview_ontoprops` | stateless_helper | ISOLATED:file_io | hashlib, json, re | REASONING_PRIMITIVES |
| `parse` | `gen_worldview_ontoprops` | stateless_helper | ISOLATED:file_io | hashlib, json, re | REASONING_PRIMITIVES |
| `to_theo` | `gen_worldview_ontoprops` | stateless_helper | ISOLATED:file_io | hashlib, json, re | REASONING_PRIMITIVES |
| `w` | `gen_worldview_ontoprops` | stateless_helper | ISOLATED:file_io | hashlib, json, re | REASONING_PRIMITIVES |
| `safe_hash` | `hashing` | stateless_helper | PURE | hashlib, typing | REASONING_PRIMITIVES |
| `execute_HBN` | `hierarchical_bayes_network` | stateless_helper | ISOLATED:file_io | json, re | REASONING_PRIMITIVES |
| `load_static_priors` | `hierarchical_bayes_network` | stateless_helper | ISOLATED:file_io | json, re | REASONING_PRIMITIVES |
| `preprocess_query` | `hierarchical_bayes_network` | stateless_helper | ISOLATED:file_io | json, re | REASONING_PRIMITIVES |
| `query_intent_analyzer` | `hierarchical_bayes_network` | stateless_helper | ISOLATED:file_io | json, re | REASONING_PRIMITIVES |
| `parse_expr` | `lambda_parser` | stateless_helper | PURE | enum, typing | REASONING_PRIMITIVES |
| `emit_plan_packet` | `plan_packet` | pure_utility | PURE | dataclasses, typing | REASONING_PRIMITIVES |
| `_build_uwm_ref` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `_clamp` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `_default_success_criteria` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `_evidence_refs` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `_find_commitment` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `_parse_priority` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `score_commitment` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `select_next_active_commitment` | `prioritization` | stateless_helper | PURE | datetime, json, typing | REASONING_PRIMITIVES |
| `Coherent` | `privative_policies` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `Good` | `privative_policies` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `TrueP` | `privative_policies` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `obligation_for` | `privative_policies` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `preserves_invariants` | `privative_policies` | stateless_helper | PURE | typing | REASONING_PRIMITIVES |
| `create_orbital_visualization` | `pxl_fractal_orbital_analysis` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, enum, json, typing | REASONING_PRIMITIVES |
| `legacy_main` | `pxl_fractal_orbital_analysis` | pure_utility | ISOLATED:file_io | dataclasses, datetime, enum, json, typing | REASONING_PRIMITIVES |
| `assess_ontological_coherence` | `pxl_modal_fractal_boundary_analysis` | reasoning_primitive | ISOLATED:file_io | collections, dataclasses, datetime, enum, json | REASONING_PRIMITIVES |
| `interpret_privative_boundaries` | `pxl_modal_fractal_boundary_analysis` | reasoning_primitive | ISOLATED:file_io | collections, dataclasses, datetime, enum, json | REASONING_PRIMITIVES |
| `legacy_main` | `pxl_modal_fractal_boundary_analysis` | pure_utility | ISOLATED:file_io | collections, dataclasses, datetime, enum, json | REASONING_PRIMITIVES |
| `initialize_scp_nexus` | `scp_nexus` | pure_utility | ISOLATED:global_state | dataclasses, datetime, enum, typing | REASONING_PRIMITIVES |
| `utc_now_ts` | `time_utils` | pure_utility | PURE | datetime | REASONING_PRIMITIVES |
| `_aggregate_profiles` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_classify_sequence` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_collect_inputs` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_compute_catalog_tail_hash` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_compute_file_hash` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_infer_protocol_tag` | `tool_optimizer` | reasoning_primitive | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_infer_risk_tag` | `tool_optimizer` | reasoning_primitive | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_io_hint_for_risk` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_matches_keyword` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_module_path` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_now_utc` | `tool_optimizer` | pure_utility | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_profile_payload` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_publish_catalog_artifact` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_repo_root_from_identity` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_safe_read_json` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_scan_python_files` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_stable_id` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_write_json` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `run_tool_optimization` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | REASONING_PRIMITIVES |
| `_apply_grammar_rules` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_assess_readability` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_calculate_translation_confidence` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_calculate_translation_quality` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_describe_logical_operators` | `translation_engine` | reasoning_primitive | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_describe_predicates` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_describe_quantifiers` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_determine_translation_mode` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_generate_semantic_mapping` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_generate_structural_description` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_optimize_readability` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_translate_combinator_structure` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_translate_logical_structure` | `translation_engine` | reasoning_primitive | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_translate_natural_structure` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_translate_standard_structure` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `_translate_structure` | `translation_engine` | stateless_helper | PURE | datetime, typing | REASONING_PRIMITIVES |
| `initialize_uip_nexus` | `uip_nexus` | pure_utility | ISOLATED:global_state | dataclasses, datetime, enum, typing | REASONING_PRIMITIVES |

### UTILITY_PRIMITIVES (45 atoms)

| Atom Name | Source Module | Atom Type | Side-Effect Profile | Dependencies | Target Library |
|-----------|--------------|-----------|---------------------|-------------|----------------|
| `demonstrate_complete_memory_system` | `Memory_Recall_Integration` | pure_utility | PURE | collections, dataclasses, datetime, enum, hashlib | UTILITY_PRIMITIVES |
| `assign_confidence` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `execute_HBN` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `filter_and_score` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `load_priors` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `load_static_priors` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `predictive_refinement` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `preprocess_query` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `query_intent_analyzer` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `resolve_priors_path` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `save_priors` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `score_data_point` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | UTILITY_PRIMITIVES |
| `bridge_status` | `bridge` | pure_utility | PURE | dataclasses, datetime, enum, typing | UTILITY_PRIMITIVES |
| `get_bridge_status` | `bridge` | pure_utility | PURE | dataclasses, datetime, enum, typing | UTILITY_PRIMITIVES |
| `run_pc_causal_discovery` | `causal_chain_node_predictor` | stateless_helper | PURE | none | UTILITY_PRIMITIVES |
| `_sha256_file` | `cycle_ledger` | stateless_helper | ISOLATED:file_io | hashlib, json, typing | UTILITY_PRIMITIVES |
| `get_code_environment_status` | `development_environment` | pure_utility | PURE | typing | UTILITY_PRIMITIVES |
| `_write_json` | `export_tool_registry` | stateless_helper | ISOLATED:file_io | dataclasses, json, typing | UTILITY_PRIMITIVES |
| `_write_markdown` | `export_tool_registry` | stateless_helper | ISOLATED:file_io | dataclasses, json, typing | UTILITY_PRIMITIVES |
| `legacy_main` | `export_tool_registry` | stateless_helper | ISOLATED:file_io | dataclasses, json, typing | UTILITY_PRIMITIVES |
| `get_iel_integration` | `iel_integration` | pure_utility | ISOLATED:global_state | typing | UTILITY_PRIMITIVES |
| `initialize_iel_system` | `iel_integration` | pure_utility | ISOLATED:global_state | typing | UTILITY_PRIMITIVES |
| `get_iel_registry` | `iel_registryv2` | pure_utility | ISOLATED:global_state | typing | UTILITY_PRIMITIVES |
| `dumps_log` | `logging_utils` | stateless_helper | PURE | json, typing | UTILITY_PRIMITIVES |
| `log_event` | `logging_utils` | pure_utility | PURE | json, typing | UTILITY_PRIMITIVES |
| `export_json_report` | `logos_monitor` | stateless_helper | ISOLATED:file_io | json | UTILITY_PRIMITIVES |
| `get_detailed_status` | `logos_monitor` | pure_utility | ISOLATED:file_io | json | UTILITY_PRIMITIVES |
| `legacy_main` | `logos_monitor` | pure_utility | ISOLATED:file_io | json | UTILITY_PRIMITIVES |
| `compare_tool_outputs` | `regression_checker` | stateless_helper | PURE | datetime, json, typing | UTILITY_PRIMITIVES |
| `get_system_diagnosis` | `self_diagnosis` | pure_utility | PURE | dataclasses, datetime, enum, typing | UTILITY_PRIMITIVES |
| `perform_system_diagnosis` | `self_diagnosis` | pure_utility | PURE | dataclasses, datetime, enum, typing | UTILITY_PRIMITIVES |
| `calculate_average_processing_time` | `system_utils` | stateless_helper | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `generate_correlation_id` | `system_utils` | pure_utility | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `handle_step_error` | `system_utils` | stateless_helper | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `log_uip_event` | `system_utils` | stateless_helper | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `observe_request_latency` | `system_utils` | stateless_helper | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `record_request_outcome` | `system_utils` | stateless_helper | ISOLATED:global_state | datetime, json, typing, uuid | UTILITY_PRIMITIVES |
| `_builtin_defaults` | `tool_introspection` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `_compute_usage_stats` | `tool_introspection` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `_load_approved_manifests` | `tool_introspection` | pure_utility | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `_load_builtin_tools` | `tool_introspection` | pure_utility | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `_load_run_ledgers` | `tool_introspection` | pure_utility | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `build_capability_records` | `tool_introspection` | pure_utility | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `build_introspection_summary` | `tool_introspection` | pure_utility | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |
| `legacy_main` | `tool_introspection` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, json, typing | UTILITY_PRIMITIVES |

### VALIDATION_PRIMITIVES (46 atoms)

| Atom Name | Source Module | Atom Type | Side-Effect Profile | Dependencies | Target Library |
|-----------|--------------|-----------|---------------------|-------------|----------------|
| `_ensure_hex` | `attestation` | validator | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `_load_json` | `attestation` | stateless_helper | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `_require` | `attestation` | stateless_helper | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `compute_attestation_hash` | `attestation` | stateless_helper | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `load_alignment_attestation` | `attestation` | validator | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `load_mission_profile` | `attestation` | validator | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `validate_attestation` | `attestation` | validator | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `validate_mission_profile` | `attestation` | validator | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `check_imports` | `check_imports` | validator | ISOLATED:file_io | none | VALIDATION_PRIMITIVES |
| `_check` | `check_run_cycle_prereqs` | validator | PURE | typing | VALIDATION_PRIMITIVES |
| `legacy_main` | `check_run_cycle_prereqs` | pure_utility | PURE | typing | VALIDATION_PRIMITIVES |
| `check_logical_consistency` | `coherence` | validator | PURE | dataclasses, datetime, enum, typing | VALIDATION_PRIMITIVES |
| `get_consistency_check` | `coherence` | validator | PURE | dataclasses, datetime, enum, typing | VALIDATION_PRIMITIVES |
| `_clamp_success_criteria` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_clamp_text` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_compute_commitment_id` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_compute_event_id` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_ensure_constraints` | `commitment_ledger` | validator | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_sha256_hex` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_trim_commitments` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `_trim_history` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `atomic_write_json` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `canonical_json` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `compute_ledger_hash` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `ensure_active_commitment` | `commitment_ledger` | validator | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `load_or_create_ledger` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `mark_commitment_status` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `mark_cycle_outcome` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `record_event` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `set_active_commitment` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `sha256_bytes` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `upsert_commitment` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `validate_ledger` | `commitment_ledger` | validator | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `write_ledger` | `commitment_ledger` | stateless_helper | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | VALIDATION_PRIMITIVES |
| `is_proved_reference` | `evidence` | stateless_helper | PURE | typing | VALIDATION_PRIMITIVES |
| `normalize_evidence_refs` | `evidence` | normalizer | PURE | typing | VALIDATION_PRIMITIVES |
| `validate_evidence_ref` | `evidence` | validator | PURE | typing | VALIDATION_PRIMITIVES |
| `_ensure_scripts_importable` | `export_tool_registry` | pure_utility | ISOLATED:file_io | dataclasses, json, typing | VALIDATION_PRIMITIVES |
| `_load_tools` | `export_tool_registry` | pure_utility | ISOLATED:file_io | dataclasses, json, typing | VALIDATION_PRIMITIVES |
| `restrict_writes_to` | `guardrails` | stateless_helper | PURE | functools, json, typing | VALIDATION_PRIMITIVES |
| `legacy_main` | `logos_mathematical_core` | pure_utility | PURE | dataclasses, hashlib, json, math, typing | VALIDATION_PRIMITIVES |
| `_inherit_constraints` | `prioritization` | stateless_helper | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `propose_candidate_commitments` | `prioritization` | stateless_helper | PURE | datetime, json, typing | VALIDATION_PRIMITIVES |
| `analyze_logos_agent_ontology` | `pxl_fractal_orbital_analysis` | pure_utility | ISOLATED:file_io | dataclasses, datetime, enum, json, typing | VALIDATION_PRIMITIVES |
| `merge_validation_results` | `pxl_schema` | stateless_helper | PURE | dataclasses, enum, pydantic, typing | VALIDATION_PRIMITIVES |
| `validate_trinity_vector` | `pxl_schema` | validator | PURE | dataclasses, enum, pydantic, typing | VALIDATION_PRIMITIVES |

### SCHEMA_PRIMITIVES (57 atoms)

| Atom Name | Source Module | Atom Type | Side-Effect Profile | Dependencies | Target Library |
|-----------|--------------|-----------|---------------------|-------------|----------------|
| `StorageConfiguration` | `Memory_Recall_Integration` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `GapDetectionRequest` | `agent_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `LinguisticRequest` | `agent_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `PlanningRequest` | `agent_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `DataBuilder` | `arp_nexus` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `ReasoningRequest` | `arp_nexus` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `ReasoningResult` | `arp_nexus` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `BayesianMLModel` | `bayesian_recursion` | schema_class | ISOLATED:file_io | none | SCHEMA_PRIMITIVES |
| `ModelState` | `bayesian_recursion` | schema_class | ISOLATED:file_io | none | SCHEMA_PRIMITIVES |
| `run_HBN_analysis` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | SCHEMA_PRIMITIVES |
| `BeliefNetwork` | `belief_network` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `Message` | `bridge` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `ModalLogic` | `coherence_formalism` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `CoherenceConfig` | `coherence_metrics` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `f` | `dual_bijection_demo` | stateless_helper | PURE | none | SCHEMA_PRIMITIVES |
| `f_inv` | `dual_bijection_demo` | stateless_helper | PURE | none | SCHEMA_PRIMITIVES |
| `g` | `dual_bijection_demo` | stateless_helper | PURE | none | SCHEMA_PRIMITIVES |
| `g_inv` | `dual_bijection_demo` | stateless_helper | PURE | none | SCHEMA_PRIMITIVES |
| `emit_evaluation_packet` | `evaluation_packet` | pure_utility | PURE | dataclasses, typing | SCHEMA_PRIMITIVES |
| `_tool_metadata` | `export_tool_registry` | stateless_helper | ISOLATED:file_io | dataclasses, json, typing | SCHEMA_PRIMITIVES |
| `FractalOrbitPredictor` | `fractal_orbit_toolkit` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `require_safe_interfaces` | `guardrails` | stateless_helper | PURE | functools, json, typing | SCHEMA_PRIMITIVES |
| `run_HBN_analysis` | `hierarchical_bayes_network` | stateless_helper | ISOLATED:file_io | json, re | SCHEMA_PRIMITIVES |
| `PacketIdentity` | `id_handler` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `generate_packet_identity` | `id_handler` | pure_utility | PURE | dataclasses, typing, uuid | SCHEMA_PRIMITIVES |
| `RegistryConfig` | `iel_registryv1` | schema_class | ISOLATED:file_io | none | SCHEMA_PRIMITIVES |
| `normalize_payload` | `io_normalizer` | normalizer | PURE | datetime, json, typing | SCHEMA_PRIMITIVES |
| `LoopConfig` | `iterative_loop` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `run_iterative_stabilization` | `iterative_loop` | pure_utility | PURE | dataclasses, typing | SCHEMA_PRIMITIVES |
| `FunctionType` | `lambda_onto_calculus_engine` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `ModalReasoner` | `modal_reasoner` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `KripkeModel` | `modal_validator` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `World` | `modal_validator` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `OntologyInducer` | `ontology_inducer` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `Config` | `pxl_schema` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `PXLAnalysisConfig` | `pxl_schema` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `PXLRelation` | `pxl_schema` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `PXLRelationModel` | `pxl_schema` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `PXLSchemaValidator` | `pxl_schema` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `create_default_analysis_config` | `pxl_schema` | pure_utility | PURE | dataclasses, enum, pydantic, typing | SCHEMA_PRIMITIVES |
| `relation_from_json` | `pxl_schema` | stateless_helper | PURE | dataclasses, enum, pydantic, typing | SCHEMA_PRIMITIVES |
| `relation_to_json` | `pxl_schema` | stateless_helper | PURE | dataclasses, enum, pydantic, typing | SCHEMA_PRIMITIVES |
| `SemanticNetworkBuilder` | `relation_mapper` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `InteractionConfig` | `router` | schema_class | ISOLATED:file_io | none | SCHEMA_PRIMITIVES |
| `get_dict` | `schema_utils` | stateless_helper | PURE | typing | SCHEMA_PRIMITIVES |
| `get_list` | `schema_utils` | stateless_helper | PURE | typing | SCHEMA_PRIMITIVES |
| `get_str` | `schema_utils` | stateless_helper | PURE | typing | SCHEMA_PRIMITIVES |
| `require_dict` | `schema_utils` | stateless_helper | PURE | typing | SCHEMA_PRIMITIVES |
| `require_str` | `schema_utils` | stateless_helper | PURE | typing | SCHEMA_PRIMITIVES |
| `CognitiveRequest` | `scp_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `CognitiveResult` | `scp_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `load_smp` | `smp_intake` | pure_utility | PURE | dataclasses, typing | SCHEMA_PRIMITIVES |
| `load_task` | `task_intake` | pure_utility | PURE | dataclasses, typing | SCHEMA_PRIMITIVES |
| `default_registry` | `transform_registry` | pure_utility | PURE | typing | SCHEMA_PRIMITIVES |
| `LogosBundle` | `types` | schema_class | PURE | none | SCHEMA_PRIMITIVES |
| `ReasoningRequest` | `uip_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |
| `ReasoningResult` | `uip_nexus` | schema_class | ISOLATED:global_state | none | SCHEMA_PRIMITIVES |

### NORMALIZATION_PRIMITIVES (25 atoms)

| Atom Name | Source Module | Atom Type | Side-Effect Profile | Dependencies | Target Library |
|-----------|--------------|-----------|---------------------|-------------|----------------|
| `_is_iso` | `attestation` | stateless_helper | PURE | datetime, json, typing | NORMALIZATION_PRIMITIVES |
| `run_BERT_pipeline` | `bayes_update_real_time` | stateless_helper | ISOLATED:file_io | datetime, json, typing | NORMALIZATION_PRIMITIVES |
| `run_BERT_pipeline` | `bayesian_updates` | stateless_helper | ISOLATED:file_io | datetime, json, re, typing | NORMALIZATION_PRIMITIVES |
| `simulate_example_data` | `causal_chain_node_predictor` | stateless_helper | PURE | none | NORMALIZATION_PRIMITIVES |
| `_utc_now` | `commitment_ledger` | pure_utility | ISOLATED:file_io | dataclasses, datetime, hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_collect_bundle_hashes` | `cycle_ledger` | stateless_helper | ISOLATED:file_io | hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_normalize_path` | `cycle_ledger` | normalizer | ISOLATED:file_io | hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_sanitize_outcomes` | `cycle_ledger` | stateless_helper | ISOLATED:file_io | hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_sanitize_steps` | `cycle_ledger` | stateless_helper | ISOLATED:file_io | hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `write_cycle_ledger` | `cycle_ledger` | pure_utility | ISOLATED:file_io | hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `legacy_main` | `iel_registryv1` | pure_utility | ISOLATED:file_io | dataclasses, datetime, hashlib, json, re | NORMALIZATION_PRIMITIVES |
| `print_status_report` | `logos_monitor` | pure_utility | ISOLATED:file_io | json | NORMALIZATION_PRIMITIVES |
| `_dedupe_key` | `prioritization` | stateless_helper | PURE | datetime, json, typing | NORMALIZATION_PRIMITIVES |
| `_iso_to_timestamp` | `prioritization` | stateless_helper | PURE | datetime, json, typing | NORMALIZATION_PRIMITIVES |
| `_now_iso` | `prioritization` | pure_utility | PURE | datetime, json, typing | NORMALIZATION_PRIMITIVES |
| `analyze_privative_modal_boundaries` | `pxl_modal_fractal_boundary_analysis` | pure_utility | ISOLATED:file_io | collections, dataclasses, datetime, enum, json | NORMALIZATION_PRIMITIVES |
| `export_metrics` | `system_utils` | pure_utility | ISOLATED:global_state | datetime, json, typing, uuid | NORMALIZATION_PRIMITIVES |
| `get_current_timestamp` | `system_utils` | pure_utility | ISOLATED:global_state | datetime, json, typing, uuid | NORMALIZATION_PRIMITIVES |
| `utc_now_iso` | `time_utils` | pure_utility | PURE | datetime | NORMALIZATION_PRIMITIVES |
| `_build_tool_registry` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_clean_docstring` | `tool_optimizer` | normalizer | ISOLATED:file_io | collections, datetime, hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_iso_timestamp` | `tool_optimizer` | pure_utility | ISOLATED:file_io | collections, datetime, hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_read_digest_file` | `tool_optimizer` | stateless_helper | ISOLATED:file_io | collections, datetime, hashlib, json, typing | NORMALIZATION_PRIMITIVES |
| `_synthesize_unified_representation` | `translation_engine` | stateless_helper | PURE | datetime, typing | NORMALIZATION_PRIMITIVES |
| `convert_to_nl` | `translation_engine` | normalizer | PURE | datetime, typing | NORMALIZATION_PRIMITIVES |

---

## SECTION 4 — Module Rejection List

Modules are rejected if they match any of:

- Classification: `External_Dependency`, `Runtime_Support`, `Interface_Binding`, `Legacy_Shim`, `Orchestration`
- Network or subprocess side effects present
- Excessive side-effect count (≥ 3 active)
- Module name indicates a test module

| Module Name | Classification | Rejection Reason |
|------------|---------------|-----------------|
| `NLP_Wrapper_Sentence_Transformers` | External_Dependency | classification=External_Dependency |
| `agentic_consciousness_core` | External_Dependency | classification=External_Dependency |
| `semantic_transformers` | External_Dependency | classification=External_Dependency |
| `test_integration` | External_Dependency | test_module |
| `providers_llama` | External_Dependency | classification=External_Dependency |
| `providers_openai` | External_Dependency | classification=External_Dependency |
| `config` | External_Dependency | classification=External_Dependency |
| `_uip_connector_stubs` | Interface_Binding | classification=Interface_Binding |
| `nexus_manager` | Legacy_Shim | classification=Legacy_Shim |
| `causal_trace_operator` | Legacy_Shim | classification=Legacy_Shim |
| `tool_invention` | Orchestration | classification=Orchestration |
| `Logos_Memory_Nexus` | Orchestration | classification=Orchestration |
| `base_nexus` | Orchestration | classification=Orchestration |
| `legacy_sop_nexus` | Orchestration | classification=Orchestration |
| `sop_nexus` | Orchestration | classification=Orchestration |
| `test_logos_runtime_phase2_smoke` | Orchestration | test_module |
| `dispatch` | Orchestration | classification=Orchestration |
| `arp_nexus_orchestrator` | Orchestration | classification=Orchestration |
| `csp_nexus_orchestrator` | Orchestration | classification=Orchestration |
| `logos_protocol_nexus` | Orchestration | classification=Orchestration |
| `scp_nexus_orchestrator` | Orchestration | classification=Orchestration |
| `sop_nexus_orchestrator` | Orchestration | classification=Orchestration |
| `test_arp_modes` | Orchestration | test_module |
| `stress_sop_runtime` | Orchestration | classification=Orchestration |
| `uip_operations` | Orchestration | classification=Orchestration |
| `iel_overlay` | Reasoning | unsafe_side_effects=['network'] |
| `tool_proposal_pipeline` | Reasoning | unsafe_side_effects=['file_io', 'env_mutation', 'subprocess'] |
| `test_hardening` | Reasoning | test_module |
| `test_llm_bypass_smoke` | Reasoning | test_module |
| `test_self_improvement_cycle` | Reasoning | test_module |
| `integration_test` | Reasoning | test_module |
| `integration_test_suite` | Reasoning | unsafe_side_effects=['file_io', 'network'] |
| `test_bayesian_data_handler` | Reasoning | test_module |
| `test_logos_agi_persistence_smoke` | Reasoning | test_module |
| `test_proved_grounding` | Reasoning | test_module |
| `test_evaluator_learning_smoke` | Reasoning | test_module |
| `test_logos_agi_pin_drift` | Reasoning | test_module |
| `simulated_consciousness_runtime` | Runtime_Support | classification=Runtime_Support |
| `health_server` | Runtime_Support | classification=Runtime_Support |
| `boot_system` | Runtime_Support | classification=Runtime_Support |
| `maintenance` | Runtime_Support | classification=Runtime_Support |
| `worker_kernel` | Runtime_Support | classification=Runtime_Support |
| `test_integration_identity` | Schema_Handling | test_module |
| `test_lock_unlock` | Schema_Handling | test_module |
| `test_nexus_capability_governance` | Schema_Handling | test_module |
| `test_arp_nexus` | Schema_Handling | test_module |
| `test_perception_ingestors` | Schema_Handling | test_module |
| `test_dual_bijection` | Semantic_Processing | test_module |
| `test_logos_agi_adapter` | Semantic_Processing | test_module |
| `test_simulation_cli` | Semantic_Processing | test_module |
| `test_tool_fallback_proposal` | Semantic_Processing | test_module |
| `test_tool_pipeline_smoke` | Utility | test_module |
| `test_registry_and_response` | Utility | test_module |
| `test_determinism` | Utility | test_module |
| `agent_identity` | Validation | unsafe_side_effects=['file_io', 'subprocess'] |
| `tool_repair_proposal` | Validation | unsafe_side_effects=['file_io', 'env_mutation', 'subprocess'] |
| `test_agent_planner` | Validation | test_module |
| `test_end_to_end_pipeline` | Validation | test_module |
| `test_logos_agi_bootstrap_modes` | Validation | test_module |
| `test_logos_agi_replay_proposals` | Validation | test_module |
| `test_pai` | Validation | test_module |
| `test_plan_revision_on_contradiction` | Validation | test_module |
| `test_scp_recovery_mode_gate` | Validation | test_module |
| `test_stub_beliefs_never_verified` | Validation | test_module |
| `test_verify_pai` | Validation | test_module |
| `test_reference_monitor` | Validation | test_module |

> **Validation**: No rejected module appears in the Donor Module Table (Section 2).

---

## SECTION 5 — Reconstruction Targets

These modules cannot be extracted as-is nor simply rejected.
They require architectural reconstruction before logic can be recovered.

Reconstruction criteria:

- Classification is a donor type but import coupling prevents direct extraction
- Recovery status indicates partial salvage only
- Side-effect count is borderline (1 active effect, non-network)

| Module Name | Classification | Recovery Status | Reconstruction Reason |
|------------|---------------|----------------|-----------------------|
| `PXL_World_Model` | Reasoning | Recoverable_As_Is | unsafe_side_effects=['file_io', 'global_state'] |
| `autonomous_learning` | Reasoning | Recoverable_With_Normalization | unsafe_side_effects=['file_io', 'global_state'] |
| `shared_resources` | Utility | Recoverable_With_Normalization | unsafe_side_effects=['file_io', 'global_state'] |

---

## Validation Checklist

| Check | Result |
|-------|--------|
| All staged modules were inspected (161) | PASS |
| All donor modules are listed in Section 2 (92) | PASS |
| No rejected module appears in donor list | PASS |
| All atoms pass side-effect safety check | PASS |
| Atom names are symbol-registry compliant | PASS |
| Artifact written to blueprint directory | PASS |

---

## Extraction Methodology

### Side-Effect Safety Gate

Atoms are rejected from extraction if the source module's `legacy_side_effect_map.json`
entry reports any of the following:

- `file_io: true` — filesystem reads or writes
- `network: true` — network socket or HTTP operations
- `subprocess: true` — external process invocation
- `global_state: true` — mutation of module-level or process-level state
- `env_mutation: true` — modification of environment variables

Modules with 1 isolated non-network side effect may still donate atoms from
functions that do not invoke the unsafe operations (per AST call analysis).

### Symbol Canonicalization Rules

Atom names are canonicalized per the following rules applied via `ast_parser.py`:

1. Dunder methods (`__init__` etc.) are excluded except `__init__`
2. Names conflicting with LOGOS reserved symbols receive a `legacy_` prefix
3. Reserved symbols: `run`, `main`, `start`, `stop`, `init`, `execute`, `dispatch`
4. Class-level schema atoms retain their original names

### Target Library Assignment Logic

| Signal | Assigned Library |
|--------|-----------------|
| schema / transform / serialize / dataclass in name or docstring | SCHEMA_PRIMITIVES |
| valid / check / enforce / constraint / assert / ensure / guard | VALIDATION_PRIMITIVES |
| normal / canonicali / clean / sanitize / strip / format / coerce | NORMALIZATION_PRIMITIVES |
| reason / infer / deduc / logic / proof / symbolic / bayes / plan | REASONING_PRIMITIVES |
| All others or classification = Utility | UTILITY_PRIMITIVES |

---

*End of LOGOS Logic Atom Extraction Plan*
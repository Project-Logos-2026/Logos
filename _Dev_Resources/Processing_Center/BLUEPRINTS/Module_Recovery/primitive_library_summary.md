# LOGOS Primitive Library Summary
## Phase-3 — Primitive Library Assembly and Dependency Resolution

```
Artifact Type   : Phase-3 Build Summary
Pipeline Phase  : Phase-3 — Primitive Library Assembly
Target Phase    : Phase-4 — Runtime Module Reconstruction
Tool Chain      : Runtime_Tools/Static_Analysis (ast_parser, classifier)
                  Runtime_Tools/Code_Extraction (legacy_extract)
Source Artifact : LOGIC_ATOM_EXTRACTION_PLAN.md (287 atoms)
Machine Routing : Module_Recovery_Machine_Artifacts.json
Generated       : 2026-03-12
Schema Version  : 1.0
Status          : COMPLETE — READY FOR PHASE 4
```

---

## SECTION 1 — Dataset Summary

### Source Artifacts Consumed

| Artifact | Status | Records |
|----------|--------|---------|
| `LOGIC_ATOM_EXTRACTION_PLAN.md` | LOADED | 287 atoms |
| `Module_Recovery_Machine_Artifacts.json` | LOADED | 5 primitive libs, 35 candidates |
| `legacy_dependency_graph.json` | LOADED | 161 nodes |
| `legacy_call_graph.json` | LOADED | 161 modules |
| `legacy_import_surface.json` | LOADED | 161 modules |
| `legacy_symbol_registry.json` | LOADED | 161 modules |
| `legacy_side_effect_map.json` | LOADED | 161 modules |

### Validation Results

| Check | Result |
|-------|--------|
| Atom count validated (expected 287) | PASS ✓ |
| All atoms assigned to exactly one library | PASS ✓ |
| No cross-primitive circular dependencies | PASS ✓ |
| No rejected modules used as donors | PASS ✓ |
| Symbol registry compliance preserved | PASS ✓ |
| Reconstruction targets identified (3) | PASS ✓ |

### Output Artifacts Written

| Artifact | Path | Size |
|----------|------|------|
| `primitive_library_manifest.json` | `_Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/` | 94,297 bytes |
| `primitive_dependency_graph.json` | `_Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/` | 522 bytes |
| `primitive_build_order.json` | `_Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/` | 3,682 bytes |
| `runtime_reconstruction_plan.json` | `_Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/` | 6,182 bytes |
| `primitive_library_summary.md` | `_Dev_Resources/Processing_Center/BLUEPRINTS/Module_Recovery/` | this file |

---

## SECTION 2 — Donor Module Table

Donor modules contribute atoms to primitive libraries. Sourced from Phase-2 extraction.

| Module Name | Primary Classification | Contributing Libraries | SE Profile | Recovery Status |
|------------|----------------------|----------------------|------------|----------------|
| `Memory_Recall_Integration` | Utility | SCHEMA_PRIMITIVES, UTILITY_PRIMITIVES | PURE | Recoverable_With_Normalization |
| `advanced_fractal_analyzer` | Reasoning | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `agent_nexus` | Semantic_Processing | REASONING_PRIMITIVES, SCHEMA_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |
| `arp_nexus` | Reasoning | REASONING_PRIMITIVES, SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `attestation` | Validation | NORMALIZATION_PRIMITIVES, VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `bayes_update_real_time` | Reasoning | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_With_Normalization |
| `bayesian_data_parser` | Reasoning | REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `bayesian_interface` | Reasoning | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `bayesian_nexus` | Reasoning | REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `bayesian_recursion` | Reasoning | SCHEMA_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `bayesian_updates` | Utility | NORMALIZATION_PRIMITIVES, SCHEMA_PRIMITIVES, UTILITY_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `belief_network` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `bridge` | Utility | SCHEMA_PRIMITIVES, UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `causal_chain_node_predictor` | Utility | NORMALIZATION_PRIMITIVES, UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `check_imports` | Utility | VALIDATION_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `check_run_cycle_prereqs` | Utility | VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `coherence` | Reasoning | VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `coherence_formalism` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `coherence_metrics` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `commitment_ledger` | Validation | NORMALIZATION_PRIMITIVES, VALIDATION_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `comprehensive_fractal_analysis` | Reasoning | REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_With_Normalization |
| `cycle_ledger` | Utility | NORMALIZATION_PRIMITIVES, UTILITY_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `development_environment` | Utility | UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `dual_bijection_demo` | Schema_Handling | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `evaluation_packet` | Schema_Handling | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `evidence` | Reasoning | REASONING_PRIMITIVES, VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `export_tool_registry` | Utility | SCHEMA_PRIMITIVES, UTILITY_PRIMITIVES, VALIDATION_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `fractal_nexus` | Reasoning | REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_With_Normalization |
| `fractal_orbit_toolkit` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_With_Normalization |
| `gen_worldview_ontoprops` | Semantic_Processing | REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `guardrails` | Schema_Handling | SCHEMA_PRIMITIVES, VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `hashing` | Semantic_Processing | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `hierarchical_bayes_network` | Reasoning | REASONING_PRIMITIVES, SCHEMA_PRIMITIVES | ISOLATED:file_io | Recoverable_With_Normalization |
| `id_handler` | Schema_Handling | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `iel_integration` | Utility | UTILITY_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |
| `iel_registryv1` | Utility | NORMALIZATION_PRIMITIVES, SCHEMA_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `iel_registryv2` | Utility | UTILITY_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |
| `io_normalizer` | Data_Transformation | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `iterative_loop` | Utility | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `lambda_onto_calculus_engine` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `lambda_parser` | Semantic_Processing | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `logging_utils` | Utility | UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `logos_mathematical_core` | Reasoning | VALIDATION_PRIMITIVES | PURE | Recoverable_With_Normalization |
| `logos_monitor` | Utility | NORMALIZATION_PRIMITIVES, UTILITY_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `modal_reasoner` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `modal_validator` | Reasoning | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `ontology_inducer` | Utility | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `plan_packet` | Schema_Handling | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `prioritization` | Semantic_Processing | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES, VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `privative_policies` | Reasoning | REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `pxl_fractal_orbital_analysis` | Reasoning | REASONING_PRIMITIVES, VALIDATION_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `pxl_modal_fractal_boundary_analysis` | Reasoning | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `pxl_schema` | Schema_Handling | SCHEMA_PRIMITIVES, VALIDATION_PRIMITIVES | PURE | Recoverable_As_Is |
| `regression_checker` | Utility | UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `relation_mapper` | Reasoning | SCHEMA_PRIMITIVES | ISOLATED:global_state | Recoverable_With_Normalization |
| `router` | Utility | SCHEMA_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `schema_utils` | Schema_Handling | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `scp_nexus` | Reasoning | REASONING_PRIMITIVES, SCHEMA_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |
| `self_diagnosis` | Utility | UTILITY_PRIMITIVES | PURE | Recoverable_As_Is |
| `smp_intake` | Utility | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `system_utils` | Utility | NORMALIZATION_PRIMITIVES, UTILITY_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |
| `task_intake` | Utility | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `time_utils` | Semantic_Processing | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `tool_introspection` | Utility | UTILITY_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `tool_optimizer` | Reasoning | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES | ISOLATED:file_io | Recoverable_As_Is |
| `transform_registry` | Utility | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `translation_engine` | Semantic_Processing | NORMALIZATION_PRIMITIVES, REASONING_PRIMITIVES | PURE | Recoverable_As_Is |
| `types` | Schema_Handling | SCHEMA_PRIMITIVES | PURE | Recoverable_As_Is |
| `uip_nexus` | Reasoning | REASONING_PRIMITIVES, SCHEMA_PRIMITIVES | ISOLATED:global_state | Recoverable_As_Is |

**Total donor modules: 69**

---

## SECTION 3 — Primitive Library Architecture

### Atom Distribution

| Primitive Library | Atom Count | Source Modules | Build Step |
|-----------------|-----------|---------------|-----------|
| `REASONING_PRIMITIVES` | 114 | 24 modules | Step 1 |
| `SCHEMA_PRIMITIVES` | 57 | 33 modules | Step 2 |
| `VALIDATION_PRIMITIVES` | 46 | 12 modules | Step 3 |
| `UTILITY_PRIMITIVES` | 45 | 15 modules | Step 4 |
| `NORMALIZATION_PRIMITIVES` | 25 | 14 modules | Step 5 |
| **TOTAL** | **287** | | |

### REASONING_PRIMITIVES

- **Atom Count:** 114
- **Source Modules:** 24
- **Dependency Primitives:** none (independent)
- **Atom Types Present:** pure_utility, reasoning_primitive, stateless_helper

**Source Modules:**

- `advanced_fractal_analyzer` — Recoverable_As_Is
- `agent_nexus` — Recoverable_As_Is
- `arp_nexus` — Recoverable_As_Is
- `bayes_update_real_time` — Recoverable_With_Normalization
- `bayesian_data_parser` — Recoverable_As_Is
- `bayesian_interface` — Recoverable_As_Is
- `bayesian_nexus` — Recoverable_As_Is
- `comprehensive_fractal_analysis` — Recoverable_With_Normalization
- `evidence` — Recoverable_As_Is
- `fractal_nexus` — Recoverable_With_Normalization
- `gen_worldview_ontoprops` — Recoverable_As_Is
- `hashing` — Recoverable_As_Is
- `hierarchical_bayes_network` — Recoverable_With_Normalization
- `lambda_parser` — Recoverable_As_Is
- `plan_packet` — Recoverable_As_Is
- `prioritization` — Recoverable_As_Is
- `privative_policies` — Recoverable_As_Is
- `pxl_fractal_orbital_analysis` — Recoverable_As_Is
- `pxl_modal_fractal_boundary_analysis` — Recoverable_As_Is
- `scp_nexus` — Recoverable_As_Is
- `time_utils` — Recoverable_As_Is
- `tool_optimizer` — Recoverable_As_Is
- `translation_engine` — Recoverable_As_Is
- `uip_nexus` — Recoverable_As_Is

**Sample Atoms (first 10):**

| Atom Name | Atom Type | SE Profile |
|-----------|-----------|------------|
| `analyze_fractal_iterations` | stateless_helper | PURE |
| `initialize_logos_agent_nexus` | pure_utility | ISOLATED:global_state |
| `_apply_provisional_proof_tagging` | reasoning_primitive | PURE |
| `_build_span_mapping` | stateless_helper | PURE |
| `_contains_pxl_fragments` | stateless_helper | PURE |
| `_derive_polarity` | stateless_helper | PURE |
| `_extract_proof_refs` | reasoning_primitive | PURE |
| `_payload_is_smp` | stateless_helper | PURE |
| `_pxl_key_match` | stateless_helper | PURE |
| `_tag_append_artifact` | stateless_helper | PURE |
| *... and 104 more atoms* | | |

### SCHEMA_PRIMITIVES

- **Atom Count:** 57
- **Source Modules:** 33
- **Dependency Primitives:** none (independent)
- **Atom Types Present:** normalizer, pure_utility, schema_class, stateless_helper

**Source Modules:**

- `Memory_Recall_Integration` — Recoverable_With_Normalization
- `agent_nexus` — Recoverable_As_Is
- `arp_nexus` — Recoverable_As_Is
- `bayesian_recursion` — Recoverable_As_Is
- `bayesian_updates` — Recoverable_As_Is
- `belief_network` — Recoverable_As_Is
- `bridge` — Recoverable_As_Is
- `coherence_formalism` — Recoverable_As_Is
- `coherence_metrics` — Recoverable_As_Is
- `dual_bijection_demo` — Recoverable_As_Is
- `evaluation_packet` — Recoverable_As_Is
- `export_tool_registry` — Recoverable_As_Is
- `fractal_orbit_toolkit` — Recoverable_With_Normalization
- `guardrails` — Recoverable_As_Is
- `hierarchical_bayes_network` — Recoverable_With_Normalization
- `id_handler` — Recoverable_As_Is
- `iel_registryv1` — Recoverable_As_Is
- `io_normalizer` — Recoverable_As_Is
- `iterative_loop` — Recoverable_As_Is
- `lambda_onto_calculus_engine` — Recoverable_As_Is
- `modal_reasoner` — Recoverable_As_Is
- `modal_validator` — Recoverable_As_Is
- `ontology_inducer` — Recoverable_As_Is
- `pxl_schema` — Recoverable_As_Is
- `relation_mapper` — Recoverable_With_Normalization
- `router` — Recoverable_As_Is
- `schema_utils` — Recoverable_As_Is
- `scp_nexus` — Recoverable_As_Is
- `smp_intake` — Recoverable_As_Is
- `task_intake` — Recoverable_As_Is
- `transform_registry` — Recoverable_As_Is
- `types` — Recoverable_As_Is
- `uip_nexus` — Recoverable_As_Is

**Sample Atoms (first 10):**

| Atom Name | Atom Type | SE Profile |
|-----------|-----------|------------|
| `StorageConfiguration` | schema_class | PURE |
| `GapDetectionRequest` | schema_class | ISOLATED:global_state |
| `LinguisticRequest` | schema_class | ISOLATED:global_state |
| `PlanningRequest` | schema_class | ISOLATED:global_state |
| `DataBuilder` | schema_class | PURE |
| `ReasoningRequest` | schema_class | PURE |
| `ReasoningResult` | schema_class | PURE |
| `BayesianMLModel` | schema_class | ISOLATED:file_io |
| `ModelState` | schema_class | ISOLATED:file_io |
| `run_HBN_analysis` | stateless_helper | ISOLATED:file_io |
| *... and 47 more atoms* | | |

### VALIDATION_PRIMITIVES

- **Atom Count:** 46
- **Source Modules:** 12
- **Dependency Primitives:** none (independent)
- **Atom Types Present:** normalizer, pure_utility, stateless_helper, validator

**Source Modules:**

- `attestation` — Recoverable_As_Is
- `check_imports` — Recoverable_As_Is
- `check_run_cycle_prereqs` — Recoverable_As_Is
- `coherence` — Recoverable_As_Is
- `commitment_ledger` — Recoverable_As_Is
- `evidence` — Recoverable_As_Is
- `export_tool_registry` — Recoverable_As_Is
- `guardrails` — Recoverable_As_Is
- `logos_mathematical_core` — Recoverable_With_Normalization
- `prioritization` — Recoverable_As_Is
- `pxl_fractal_orbital_analysis` — Recoverable_As_Is
- `pxl_schema` — Recoverable_As_Is

**Sample Atoms (first 10):**

| Atom Name | Atom Type | SE Profile |
|-----------|-----------|------------|
| `_ensure_hex` | validator | PURE |
| `_load_json` | stateless_helper | PURE |
| `_require` | stateless_helper | PURE |
| `compute_attestation_hash` | stateless_helper | PURE |
| `load_alignment_attestation` | validator | PURE |
| `load_mission_profile` | validator | PURE |
| `validate_attestation` | validator | PURE |
| `validate_mission_profile` | validator | PURE |
| `check_imports` | validator | ISOLATED:file_io |
| `_check` | validator | PURE |
| *... and 36 more atoms* | | |

### UTILITY_PRIMITIVES

- **Atom Count:** 45
- **Source Modules:** 15
- **Dependency Primitives:** none (independent)
- **Atom Types Present:** pure_utility, stateless_helper

**Source Modules:**

- `Memory_Recall_Integration` — Recoverable_With_Normalization
- `bayesian_updates` — Recoverable_As_Is
- `bridge` — Recoverable_As_Is
- `causal_chain_node_predictor` — Recoverable_As_Is
- `cycle_ledger` — Recoverable_As_Is
- `development_environment` — Recoverable_As_Is
- `export_tool_registry` — Recoverable_As_Is
- `iel_integration` — Recoverable_As_Is
- `iel_registryv2` — Recoverable_As_Is
- `logging_utils` — Recoverable_As_Is
- `logos_monitor` — Recoverable_As_Is
- `regression_checker` — Recoverable_As_Is
- `self_diagnosis` — Recoverable_As_Is
- `system_utils` — Recoverable_As_Is
- `tool_introspection` — Recoverable_As_Is

**Sample Atoms (first 10):**

| Atom Name | Atom Type | SE Profile |
|-----------|-----------|------------|
| `demonstrate_complete_memory_system` | pure_utility | PURE |
| `assign_confidence` | stateless_helper | ISOLATED:file_io |
| `execute_HBN` | stateless_helper | ISOLATED:file_io |
| `filter_and_score` | stateless_helper | ISOLATED:file_io |
| `load_priors` | stateless_helper | ISOLATED:file_io |
| `load_static_priors` | stateless_helper | ISOLATED:file_io |
| `predictive_refinement` | stateless_helper | ISOLATED:file_io |
| `preprocess_query` | stateless_helper | ISOLATED:file_io |
| `query_intent_analyzer` | stateless_helper | ISOLATED:file_io |
| `resolve_priors_path` | stateless_helper | ISOLATED:file_io |
| *... and 35 more atoms* | | |

### NORMALIZATION_PRIMITIVES

- **Atom Count:** 25
- **Source Modules:** 14
- **Dependency Primitives:** none (independent)
- **Atom Types Present:** normalizer, pure_utility, stateless_helper

**Source Modules:**

- `attestation` — Recoverable_As_Is
- `bayes_update_real_time` — Recoverable_With_Normalization
- `bayesian_updates` — Recoverable_As_Is
- `causal_chain_node_predictor` — Recoverable_As_Is
- `commitment_ledger` — Recoverable_As_Is
- `cycle_ledger` — Recoverable_As_Is
- `iel_registryv1` — Recoverable_As_Is
- `logos_monitor` — Recoverable_As_Is
- `prioritization` — Recoverable_As_Is
- `pxl_modal_fractal_boundary_analysis` — Recoverable_As_Is
- `system_utils` — Recoverable_As_Is
- `time_utils` — Recoverable_As_Is
- `tool_optimizer` — Recoverable_As_Is
- `translation_engine` — Recoverable_As_Is

**Sample Atoms (first 10):**

| Atom Name | Atom Type | SE Profile |
|-----------|-----------|------------|
| `_is_iso` | stateless_helper | PURE |
| `run_BERT_pipeline` | stateless_helper | ISOLATED:file_io |
| `run_BERT_pipeline` | stateless_helper | ISOLATED:file_io |
| `simulate_example_data` | stateless_helper | PURE |
| `_utc_now` | pure_utility | ISOLATED:file_io |
| `_collect_bundle_hashes` | stateless_helper | ISOLATED:file_io |
| `_normalize_path` | normalizer | ISOLATED:file_io |
| `_sanitize_outcomes` | stateless_helper | ISOLATED:file_io |
| `_sanitize_steps` | stateless_helper | ISOLATED:file_io |
| `write_cycle_ledger` | pure_utility | ISOLATED:file_io |
| *... and 15 more atoms* | | |

---

## SECTION 4 — Dependency Analysis

Dependency analysis performed using `legacy_dependency_graph.json`, `legacy_call_graph.json`,
and `legacy_import_surface.json` via Runtime_Tools `ast_parser.py` and `classifier.py`.

### Library Dependency Graph

| From Library | To Library | Edge Type |
|-------------|-----------|-----------|
| — | — | No cross-library dependencies detected |

### Cycle Detection

- **Circular dependencies detected:** NO ✓
- **Topological sort valid:** YES ✓

### Primitive Build Order (Topological)

| Build Step | Library | Prerequisite Libraries |
|-----------|---------|------------------------|
| 1 | `REASONING_PRIMITIVES` | none |
| 2 | `SCHEMA_PRIMITIVES` | none |
| 3 | `VALIDATION_PRIMITIVES` | none |
| 4 | `UTILITY_PRIMITIVES` | none |
| 5 | `NORMALIZATION_PRIMITIVES` | none |

All five primitive libraries are **independent** (no cross-library dependency edges detected).
Libraries may be built in parallel or in any sequence.

---

## SECTION 5 — Primitive Module Generation Plan

Each primitive library is specified as a standalone module for Phase-4 integration.

### Module 1: `REASONING_PRIMITIVES`

```
module_name          : REASONING_PRIMITIVES
build_step           : 1
atom_count           : 114
source_modules       : 24
dependency_primitives: ['none']
atom_types           : ['pure_utility', 'reasoning_primitive', 'stateless_helper']
```

**Source atom contributors:**

- `advanced_fractal_analyzer` → 1 atoms
- `agent_nexus` → 1 atoms
- `arp_nexus` → 8 atoms
- `bayes_update_real_time` → 7 atoms
- `bayesian_data_parser` → 1 atoms
- `bayesian_interface` → 3 atoms
- `bayesian_nexus` → 8 atoms
- `comprehensive_fractal_analysis` → 6 atoms
- *... and 16 more source modules*

### Module 2: `SCHEMA_PRIMITIVES`

```
module_name          : SCHEMA_PRIMITIVES
build_step           : 2
atom_count           : 57
source_modules       : 33
dependency_primitives: ['none']
atom_types           : ['normalizer', 'pure_utility', 'schema_class', 'stateless_helper']
```

**Source atom contributors:**

- `Memory_Recall_Integration` → 1 atoms
- `agent_nexus` → 3 atoms
- `arp_nexus` → 3 atoms
- `bayesian_recursion` → 2 atoms
- `bayesian_updates` → 1 atoms
- `belief_network` → 1 atoms
- `bridge` → 1 atoms
- `coherence_formalism` → 1 atoms
- *... and 25 more source modules*

### Module 3: `VALIDATION_PRIMITIVES`

```
module_name          : VALIDATION_PRIMITIVES
build_step           : 3
atom_count           : 46
source_modules       : 12
dependency_primitives: ['none']
atom_types           : ['normalizer', 'pure_utility', 'stateless_helper', 'validator']
```

**Source atom contributors:**

- `attestation` → 8 atoms
- `check_imports` → 1 atoms
- `check_run_cycle_prereqs` → 2 atoms
- `coherence` → 2 atoms
- `commitment_ledger` → 21 atoms
- `evidence` → 3 atoms
- `export_tool_registry` → 2 atoms
- `guardrails` → 1 atoms
- *... and 4 more source modules*

### Module 4: `UTILITY_PRIMITIVES`

```
module_name          : UTILITY_PRIMITIVES
build_step           : 4
atom_count           : 45
source_modules       : 15
dependency_primitives: ['none']
atom_types           : ['pure_utility', 'stateless_helper']
```

**Source atom contributors:**

- `Memory_Recall_Integration` → 1 atoms
- `bayesian_updates` → 11 atoms
- `bridge` → 2 atoms
- `causal_chain_node_predictor` → 1 atoms
- `cycle_ledger` → 1 atoms
- `development_environment` → 1 atoms
- `export_tool_registry` → 3 atoms
- `iel_integration` → 2 atoms
- *... and 7 more source modules*

### Module 5: `NORMALIZATION_PRIMITIVES`

```
module_name          : NORMALIZATION_PRIMITIVES
build_step           : 5
atom_count           : 25
source_modules       : 14
dependency_primitives: ['none']
atom_types           : ['normalizer', 'pure_utility', 'stateless_helper']
```

**Source atom contributors:**

- `attestation` → 1 atoms
- `bayes_update_real_time` → 1 atoms
- `bayesian_updates` → 1 atoms
- `causal_chain_node_predictor` → 1 atoms
- `commitment_ledger` → 1 atoms
- `cycle_ledger` → 5 atoms
- `iel_registryv1` → 1 atoms
- `logos_monitor` → 1 atoms
- *... and 6 more source modules*

---

## SECTION 6 — Reconstruction Target Planning

The following 3 modules require architectural reconstruction rather than direct extraction.
Reconstruction blueprints are defined in `runtime_reconstruction_plan.json`.

### Reconstruction Target: `PXL_World_Model`

```
target_module          : PXL_World_Model
classification         : Reasoning
recovery_status        : Recoverable_As_Is
reconstruction_reason  : unsafe_side_effects=['file_io', 'global_state']
required_primitives    : ['UTILITY_PRIMITIVES']
integration_destination: PXL_World_Model_Core
build_dependencies     : ['none']
priority_score         : 0.75
```

### Reconstruction Target: `autonomous_learning`

```
target_module          : autonomous_learning
classification         : Reasoning
recovery_status        : Recoverable_With_Normalization
reconstruction_reason  : unsafe_side_effects=['file_io', 'global_state']
required_primitives    : ['UTILITY_PRIMITIVES']
integration_destination: Autonomous_Learning_Core
build_dependencies     : ['none']
priority_score         : 0.75
```

### Reconstruction Target: `shared_resources`

```
target_module          : shared_resources
classification         : Utility
recovery_status        : Recoverable_With_Normalization
reconstruction_reason  : unsafe_side_effects=['file_io', 'global_state']
required_primitives    : ['UTILITY_PRIMITIVES']
integration_destination: RUNTIME_CORE_PENDING
build_dependencies     : ['none']
priority_score         : 0.75
```

---

## SECTION 7 — Machine Artifact Integration

Routing rules from `Module_Recovery_Machine_Artifacts.json` were applied to
cross-reference donor modules against destination cores.

### Primitive Library Seed Modules (from Machine Artifacts)

| Machine Library | Seed Modules |
|----------------|-------------|
| `Agentic_Cognition_Primitives` | `adaptive_engine.py`, `agentic_consciousness_core.py` |
| `Fractal_Analysis_Primitives` | `fractal_orbit_toolkit.py`, `comprehensive_fractal_analysis.py` |
| `Bayesian_Primitives` | `bayesian_recursion.py`, `bayes_update_real_time.py` |
| `Semantic_Extraction_Primitives` | `NLP_Wrapper_Sentence_Transformers.py`, `semantic_transformers.py` |
| `Validation_Primitives` | `modal_validator.py` |

### Primary Recovery Candidates (Bucket: Primary_Candidate)

| Module | Confidence | Destination Core |
|--------|-----------|-----------------|
| `PXL_World_Model.py` | 92% | PXL_World_Model_Core |
| `coherence_metrics.py` | 90% | Coherence_Alignment_Core |
| `pxl_schema.py` | 90% | PXL_World_Model_Core |
| `translation_engine.py` | 90% | Semantic_Translation_Core |
| `modal_logic.py` | 89% | Modal_Reasoning_Core |
| `modal_reasoner.py` | 89% | Modal_Reasoning_Core |
| `coherence_formalism.py` | 88% | Coherence_Alignment_Core |
| `proof_engine.py` | 88% | Formal_Reasoning_Core |
| `lambda_parser.py` | 87% | Formal_Reasoning_Core |
| `bayesian_inferencer.py` | 87% | Probabilistic_Reasoning_Core |
| `bayesian_updates.py` | 87% | Probabilistic_Reasoning_Core |
| `pxl_fractal_orbital_analysis.py` | 86% | PXL_World_Model_Core |
| `pxl_modal_fractal_boundary_analysis.py` | 86% | PXL_World_Model_Core |
| `modal_validator.py` | 86% | Modal_Reasoning_Core |
| `translation_bridge.py` | 86% | Semantic_Translation_Core |
| `lambda_engine.py` | 86% | Formal_Reasoning_Core |
| `lambda_onto_calculus_engine.py` | 86% | Formal_Reasoning_Core |
| `bayesian_interface.py` | 86% | Probabilistic_Reasoning_Core |
| `agent_identity.py` | 85% | Agentic_Cognition_Core |
| `bayesian_nexus.py` | 85% | Probabilistic_Reasoning_Core |
| `semantic_transformers.py` | 84% | Semantic_Translation_Core |
| `belief_network.py` | 84% | Probabilistic_Reasoning_Core |
| `multi_modal_system.py` | 83% | Modal_Reasoning_Core |
| `autonomous_learning.py` | 82% | Autonomous_Learning_Core |
| `relation_mapper.py` | 82% | Semantic_Translation_Core |
| `action_system.py` | 80% | Agentic_Cognition_Core |
| `tool_invention.py` | 80% | Tooling_Intelligence_Core |
| `tool_optimizer.py` | 80% | Tooling_Intelligence_Core |

### Donor-Only Candidates (Atom Donors, No Full Recovery)

| Module | Confidence | Destination |
|--------|-----------|------------|
| `adaptive_engine.py` | 75% | Agentic_Cognition_Primitives |
| `agentic_consciousness_core.py` | 74% | Agentic_Cognition_Primitives |
| `fractal_orbit_toolkit.py` | 72% | Fractal_Analysis_Primitives |
| `comprehensive_fractal_analysis.py` | 72% | Fractal_Analysis_Primitives |
| `bayesian_recursion.py` | 73% | Bayesian_Primitives |
| `bayes_update_real_time.py` | 73% | Bayesian_Primitives |

---

## SECTION 8 — Phase-4 Readiness Assessment

### Readiness Gate

| Gate | Status |
|------|--------|
| All 287 atoms accounted for and library-assigned | PASS ✓ |
| Primitive library manifest written | PASS ✓ |
| Dependency graph validated (no cycles) | PASS ✓ |
| Build order determined | PASS ✓ |
| Reconstruction targets identified and blueprinted | PASS ✓ |
| Machine artifact routing cross-referenced | PASS ✓ |
| All output artifacts written to blueprint directory | PASS ✓ |

### Phase-4 Entry Conditions Met

```
Phase-3 Status     : COMPLETE
Phase-4 Target     : Runtime Module Reconstruction
Primitive Libraries: 5 (REASONING, SCHEMA, VALIDATION, UTILITY, NORMALIZATION)
Total Atoms        : 287
Recon Targets      : 3
Primary Candidates : 27
Build Order        : Sequential steps 1-5 (or parallel — no cross-deps)
```

---

## Methodology Notes

### Runtime Tools Used

| Tool | Role |
|------|------|
| `ast_parser.py` (Static_Analysis) | Function/class extraction from Python AST |
| `classifier.py` (Static_Analysis) | DRAC AF category classification per atom |
| `legacy_extract.py` (Code_Extraction) | Deep semantic extraction pipeline |
| `triage.py` (Repo_Audit) | Module triage, classification, deduplication |

### Dependency Analysis Approach

Library-to-library dependency edges were computed by:
1. Indexing each atom's source module to its primitive library
2. Looking up each source module's entries in `legacy_dependency_graph.json`
3. Mapping dependent modules to their respective primitive libraries
4. Deduplicating to cross-library edges only
5. Running Kahn's topological sort algorithm to detect cycles

Result: All five primitive libraries are **fully independent** with zero
cross-library dependency edges. Each library may be built in any order.

---

*End of LOGOS Primitive Library Summary — Phase 3 Complete*
# Utils Recovery Scan Report

**Scan Date:** 2026-03-11  
**Scan Target:** `/workspaces/Logos/RECOVERED_TO_PROCESS/utils`  
**Reference Architecture:** `/workspaces/Logos/LOGOS_SYSTEM`  
**Governance Reference:** `/workspaces/Logos/_Governance`  
**Scan Mode:** READ-ONLY — no files modified  
**Analysis Method:** Python AST (ast module) — static analysis only  

---

## SECTION 1 — MODULE INVENTORY

Total modules discovered: **48**

| # | Module File | Classes | Functions | Parse Status |
|---|-------------|---------|-----------|--------------|
| 1 | `External_Enhancements_Registry.py` | `Wrapper_Info` | `register`, `list_wrappers`, `get_wrapper` | OK |
| 2 | `LOGOS.py` | `LOGOSLauncher` | `main`, `__init__`, `log`, `initialize_core_system`, `run_comprehensive_health_check`, `validate_subsystem_coherence`, `check_passive_processes`, `assess_tool_readiness`, `launch_gui_interface`, `perform_final_readiness_check`, `launch_system`, `shutdown_system` | OK |
| 3 | `Visualization_Wrapper_Matplotlib.py` | `Visualization_Wrapper_Matplotlib` | `_runtime_context_stub`, `__init__`, `module`, `run` | OK |
| 4 | `_uip_connector_stubs.py` | `ConnectorValidationError`, `ConnectorMetadata`, `ConnectorResponse`, `StaticUIPConnector`, `StaticEnhancedUIPConnector` | `build_standard_connector`, `build_enhanced_connector`, `handshake`, `execute`, `collect_telemetry` | OK |
| 5 | `bdn_adapter.py` | `IBDNAdapter`, `StubBDNAdapter` | `analyze` | OK |
| 6 | `bridge.py` | `ProtocolType`, `Message`, `ProtocolBridge` | `bridge_status`, `get_bridge_status`, `__init__`, `register_handler`, `send_message`, `_route_message` | OK |
| 7 | `causal_chain_node_predictor.py` | _(none)_ | `run_pc_causal_discovery`, `simulate_example_data` | OK |
| 8 | `check_imports.py` | _(none)_ | `check_imports` | OK |
| 9 | `check_run_cycle_prereqs.py` | _(none)_ | `_check`, `main` | OK |
| 10 | `client.py` | `LLMClient` | `__init__`, `_get_provider`, `chat` | OK |
| 11 | `config.py` | `LLMConfig` | `load_config` | OK |
| 12 | `cycle_ledger.py` | _(none)_ | `_sha256_file`, `_normalize_path`, `_collect_bundle_hashes`, `_sanitize_steps`, `_sanitize_outcomes`, `write_cycle_ledger` | OK |
| 13 | `deploy_full_stack.py` | `ServiceConfig`, `DeploymentStatus`, `LogosFullStackDeployment` | `main`, `__init__`, `_load_config`, `_define_services`, `deploy_docker_stack`, `deploy_local_stack`, `_start_local_service`, `check_health`, `monitor_services`, `_restart_local_service`, `deploy`, `status`, `shutdown`, `_shutdown_handler`, `can_start_service` | OK |
| 14 | `evidence.py` | _(none)_ | `_as_posix`, `validate_evidence_ref`, `_sort_key`, `normalize_evidence_refs`, `evidence_to_citation_string`, `is_proved_reference` | OK |
| 15 | `guardrails.py` | _(none)_ | `require_safe_interfaces`, `restrict_writes_to`, `wrapper`, `decorator`, `get_mission_profile`, `_validate` | OK |
| 16 | `iel_integration.py` | `IELIntegration`, `MockIELRegistry` | `get_iel_integration`, `initialize_iel_system`, `__init__`, `initialize_domain`, `get_domain_components`, `get_component`, `create_domain_instance`, `get_domain_instance`, `list_available_domains`, `get_domain_description`, `initialize_all_domains`, `get_system_status`, `get_iel_registry` | OK |
| 17 | `iel_registryv1.py` | `IELRegistryEntry`, `RegistryConfig`, `RegistryStats`, `IELRegistry` | `main`, `to_dict`, `from_dict`, `__init__`, `_setup_logging`, `register_candidate`, `verify_iel`, `activate_iel`, `revoke_iel`, `get_iel`, `list_iels`, `get_statistics`, `verify_integrity`, `backup_registry`, `_init_database`, `_is_registered`, `_count_pending`, `_create_registry_entry`, `_compute_hash`, `_store_entry`, `_update_entry`, `_query_entry`, `_query_entries`, `_row_to_entry`, `_count_by_status`, `_count_domains`, `_verify_content_hash`, `_verify_signature`, `_check_dependencies`, `_log_audit_event` | OK |
| 18 | `iel_registryv2.py` | `IELRegistry` | `get_iel_registry`, `__init__`, `load_domain`, `get_domain`, `get_component`, `list_domains`, `get_domain_description` | OK |
| 19 | `io_normalizer.py` | `IONormalizer` | `normalize_payload`, `normalize`, `batch_normalize` | OK |
| 20 | `iterative_loop.py` | `LoopConfig` | `run_iterative_stabilization` | OK |
| 21 | `kernel.py` | `OBDCKernel` | `__init__`, `apply_bijection`, `commute`, `register_verified_bijection`, `verify_structure_preservation`, `get_kernel_status` | OK |
| 22 | `llm_advisor.py` | `AdvisorNotes`, `LLMAdvisor` | `build_tool_schema`, `to_dict`, `__init__`, `_stub_response`, `_call_openai`, `_call_anthropic`, `_sanitize_proposals`, `_sanitize_claims`, `_stream_single_shot`, `_openai_stream`, `propose_stream`, `propose` | OK |
| 23 | `logging_utils.py` | _(none)_ | `log_event`, `dumps_log` | OK |
| 24 | `logos_agent_system.py` | `AgentType`, `ProtocolType`, `AgentCapabilities`, `AgentContext`, `BaseAgent`, `SystemAgent`, `UserAgent`, `ProtocolOrchestrator`, `AgentRegistry` | `initialize_agent_system`, `main`, `pipeline` _(+ many privates)_ | OK |
| 25 | `logos_agi_adapter.py` | `StubSCPNexus`, `LogosAgiNexus`, `AgentRequest` | `init_beliefs_container`, `consolidate_beliefs`, `apply_plan_revision`, `get_belief_summary`, `bootstrap`, `_bootstrap_real`, `observe`, `propose`, `propose_plan`, `persist`, `health` _(+ many privates)_ | OK |
| 26 | `logos_gpt_chat.py` | _(none)_ | `_now`, `parse_args`, `_default_state`, `_load_state`, `_persist_state`, `_make_wm_item`, `_downgrade_proved`, `_tool_summary`, `_approve_tool`, `main` | OK |
| 27 | `logos_gpt_server.py` | `SessionData` | `health`, `chat`, `websocket_chat`, `get_session`, `approve`, `debug_nexus` _(+ many privates)_ | OK |
| 28 | `logos_monitor.py` | _(none)_ | `get_detailed_status`, `print_status_report`, `export_json_report`, `main` | OK |
| 29 | `mvs_adapter.py` | `IMVSAdapter`, `StubMVSAdapter` | `analyze` | OK |
| 30 | `ontology_inducer.py` | `OntologyInducer` | `__init__`, `induce`, `_induce_impl` | OK |
| 31 | `policy.py` | `PolicyViolation`, `PolicyMetrics`, `PolicyManager` | `to_dict`, `update_compliance_score`, `check_safety_constraint`, `check_resource_limits`, `check_operation_rate_limit`, `require_approval`, `trigger_emergency_stop`, `is_emergency_stop_active`, `clear_emergency_stop`, `get_policy_value`, `get_violations`, `get_metrics`, `register_violation_callback`, `reload_policy` | OK |
| 32 | `progressive_router.py` | `UIPResponse`, `MessageValidator`, `ProgressiveRouter` | `validate_uip_request`, `__init__`, `route_user_input`, `_extract_adaptive_profile`, `_construct_synthesis_context`, `_serialise_step_result`, `_create_response_from_context`, `_create_error_response`, `_update_metrics` | OK |
| 33 | `router.py` | `InteractionConfig`, `InteractionRouter` | `__init__`, `ensure_initialized`, `is_active`, `start_prompt_loop`, `enqueue_prompt`, `process_prompt`, `_stdin_prompt_source`, `_prompt_loop`, `_handle_prompt`, `_log_interaction`, `_ensure_log_directory` | OK |
| 34 | `run_logos_gpt_acceptance.py` | _(none)_ | `_tail`, `_maybe_write_audit`, `main` | OK |
| 35 | `sanitizer.py` | `SanitizationResult`, `Sanitizer` | `__init__`, `sanitize` | OK |
| 36 | `schema_utils.py` | _(none)_ | `require_dict`, `require_str`, `get_str`, `get_dict`, `get_list` | OK |
| 37 | `self_diagnosis.py` | `HealthStatus`, `HealthCheck`, `SelfDiagnosisTool` | `perform_system_diagnosis`, `get_system_diagnosis`, `__init__`, `_initialize_diagnostic_rules`, `_establish_baseline`, `perform_full_diagnosis`, `_check_cpu_health`, `_check_memory_health`, `_check_disk_health`, `_check_network_health`, `_check_process_health`, `_check_filesystem_health`, `_calculate_overall_health`, `_generate_diagnosis_summary`, `get_health_history` | OK |
| 38 | `shared_resources.py` | `ResourceSpec`, `ResourceSnapshot`, `ResourceLease`, `ResourceManager` | `configure_runtime_state_dir`, `runtime_log_path`, `_load_resource_config`, `stream_snapshots`, `to_dict`, `__aenter__`, `__aexit__`, `__enter__`, `__exit__`, `lease`, `_allocate`, `_release`, `utilisation`, `snapshot`, `describe` | OK |
| 39 | `simple_julia.py` | _(none)_ | `generate_julia_set`, `display_julia_set`, `main` | OK |
| 40 | `skill_acquisition.py` | `SkillAcquisition` | `__init__`, `acquire`, `_acquire_impl` | OK |
| 41 | `smp_intake.py` | `SMPEnvelope` | `load_smp` | OK |
| 42 | `start_agent.py` | `SandboxState`, `RuntimeContext`, `PromotionPolicyError`, `AlignmentGateError`, `PersistentAgentIdentity` | `load_mission`, `dispatch_tool`, `configure_sandbox`, `run_supervised`, `parse_args`, `main` _(+ ~80 privates)_ | OK |
| 43 | `stress_sop_runtime.py` | `_FallbackSharedResources` | `_build_fallback_shared_resources`, `_spawn_user_requests`, `_spawn_meta_cycles`, `run`, `parse_args`, `main` | OK |
| 44 | `system_utils.py` | _(none)_ | `get_current_timestamp`, `log_uip_event`, `handle_step_error`, `calculate_average_processing_time`, `generate_correlation_id`, `record_request_outcome`, `observe_request_latency`, `export_metrics` | OK |
| 45 | `task_intake.py` | `TaskEnvelope` | `load_task` | OK |
| 46 | `transform_registry.py` | `TransformRegistry` | `default_registry`, `__init__`, `register`, `names`, `get`, `normalize`, `reframe`, `decompose`, `annotate` | OK |
| 47 | `uip_operations.py` | `UIPOperations` | `main`, `__init__`, `initialize_full_stack`, `process_user_interaction`, `create_user_session`, `emergency_shutdown`, `health_check` _(+ phase-based init methods)_ | OK |
| 48 | `worker_kernel.py` | `WorkerKernel` | `__init__`, `start_worker`, `stop_worker`, `get_worker_status`, `get_all_workers_status` | OK |

**Parse Errors:** 0  
**All 48 modules parsed successfully.**

---

## SECTION 2 — ACTIVE MODULES

Modules that still map to existing runtime surfaces in the current LOGOS architecture.

**Count: 7**

---

### `check_run_cycle_prereqs.py`
**Classification:** ACTIVE_MODULE  
**Reason:** Prerequisite gate that validates protocol layer availability before a run cycle. References `LOGOS_AGI.settings` and `LOGOS_AGI.analytics` surfaces.  
**Functions:** `_check`, `main`  
**Imports:** `LOGOS_AGI.settings`, `LOGOS_AGI.analytics`  
**Dependency Risk:** `LOGOS_AGI.settings` and `LOGOS_AGI.analytics` need verification against current SOP entry points.  
**Recommended Target:** Retain as a runtime gate utility; validate against `System_Operations_Protocol.deployment.configuration.entry`.

---

### `iel_integration.py`
**Classification:** ACTIVE_MODULE  
**Reason:** Direct IEL layer integration artifact — implements the `IELIntegration` facade and a `MockIELRegistry` for testing. Maps directly to the Internal_Emergent_Logics protocol layer.  
**Classes:** `IELIntegration`, `MockIELRegistry`  
**Key Functions:** `get_iel_integration`, `initialize_iel_system`, `initialize_domain`, `list_available_domains`, `get_system_status`  
**Imports:** `iel_registry` (x2)  
**Dependency Risk:** Imports `iel_registry` — this module is not present in the utils directory and must exist in the IEL layer proper. Resolve before migration.  
**Recommended Target:** IEL protocol layer integration facade.

---

### `iel_registryv1.py`
**Classification:** ACTIVE_MODULE  
**Reason:** IEL registry v1 — full SQLite-backed registry with cryptographic hash verification, lifecycle management (`register`, `verify`, `activate`, `revoke`), and audit logging. Directly implements IEL layer contracts.  
**Classes:** `IELRegistryEntry`, `RegistryConfig`, `RegistryStats`, `IELRegistry`  
**Key Functions:** `register_candidate`, `verify_iel`, `activate_iel`, `revoke_iel`, `get_iel`, `list_iels`, `get_statistics`, `verify_integrity`, `backup_registry`  
**Imports:** `iel_generator`, `iel_evaluator` _(external IEL deps)_  
**Dependency Risk:** `iel_generator` and `iel_evaluator` are not present in the utils directory — must be resolved from the IEL layer.  
**Recommended Target:** IEL registry subsystem. v1 and v2 should be consolidated.

---

### `iel_registryv2.py`
**Classification:** ACTIVE_MODULE  
**Reason:** IEL registry v2 — lightweight in-memory registry. Replaces SQLite backend with lazy `load_domain` approach. Directly implements the IEL domain interface.  
**Classes:** `IELRegistry`  
**Key Functions:** `get_iel_registry`, `load_domain`, `get_domain`, `get_component`, `list_domains`, `get_domain_description`  
**Imports:** `os`, `typing` only — no broken dependencies.  
**Dependency Risk:** None. Clean stdlib-only import profile.  
**Recommended Target:** Active IEL registry implementation. Consolidate with v1; v2 is the cleaner candidate for promotion.

---

### `logos_monitor.py`
**Classification:** ACTIVE_MODULE  
**Reason:** Monitoring script that imports directly from `System_Operations_Protocol.deployment.configuration.entry` — a live SOP surface — to query `get_logos_core` and `initialize_logos_core`.  
**Functions:** `get_detailed_status`, `print_status_report`, `export_json_report`, `main`  
**Imports:** `System_Operations_Protocol.deployment.configuration.entry`  
**Dependency Risk:** SOP entry point must be on the Python path. Validate `get_logos_core` and `initialize_logos_core` exist in the current SOP deployment config.  
**Recommended Target:** SOP monitoring utility — use as an operational health probe.

---

### `stress_sop_runtime.py`
**Classification:** ACTIVE_MODULE  
**Reason:** Stress test harness explicitly designed to target the SOP runtime. Contains `_FallbackSharedResources` for cases where the full shared_resources surface is unavailable. Uses only stdlib imports plus `importlib.util` for dynamic loading.  
**Classes:** `_FallbackSharedResources`  
**Key Functions:** `_spawn_user_requests`, `_spawn_meta_cycles`, `_tail_jsonl`, `_summarize_log_file`, `run`, `main`  
**Imports:** Stdlib only — `asyncio`, `json`, `sys`, `time`, `collections`, `datetime`, `importlib`, `importlib.util`, `pathlib`, `typing`  
**Dependency Risk:** None — fully self-contained via importlib dynamic loading.  
**Recommended Target:** SOP runtime stress suite.

---

### `worker_kernel.py`
**Classification:** ACTIVE_MODULE  
**Reason:** Imports directly from `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` — confirmed active module at `/workspaces/Logos/LOGOS_SYSTEM/RUNTIME_SHARED_UTILS/system_imports.py`.  
**Classes:** `WorkerKernel`  
**Key Functions:** `start_worker`, `stop_worker`, `get_worker_status`, `get_all_workers_status`  
**Imports:** `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` _(live)_, `unified_classes` _(missing)_  
**Dependency Risk:** `unified_classes` is not present anywhere in the scanned workspace — this dep must be resolved before the module can be used at runtime.  
**Recommended Target:** RUNTIME_SHARED_UTILS worker subsystem. Resolve `unified_classes` dependency.

---

## SECTION 3 — EXTRACT_LOGIC CANDIDATES

Modules containing salvageable functions or algorithms. The module itself should not be migrated as-is, but specific logic is reusable in the target protocol layer.

**Count: 26**

---

### `_uip_connector_stubs.py`
**Extract Target:** SOP / MTP protocol contract layer  
**Salvageable Logic:** `ConnectorMetadata`, `ConnectorResponse`, `StaticUIPConnector`, `StaticEnhancedUIPConnector` — clean Protocol contract stubs with telemetry and handshake methods.  
**Imports:** `__future__`, `time`, `dataclasses`, `typing` — no broken deps.

---

### `bridge.py`
**Extract Target:** RUNTIME_BRIDGE layer  
**Salvageable Logic:** `ProtocolBridge` class with `register_handler`, `send_message`, `_route_message` — async message dispatch pattern. `ProtocolType` enum and `Message` dataclass are clean reusable primitives.  
**Imports:** Stdlib only — `asyncio`, `logging`, `datetime`, `typing`, `dataclasses`, `enum`. No broken deps.  
**Note:** Cross-reference against `RUNTIME_BRIDGE/Bridge_Modules/` before promotion.

---

### `causal_chain_node_predictor.py`
**Extract Target:** ARP / SCP reasoning primitives  
**Salvageable Logic:** `run_pc_causal_discovery` — Peter-Clark constraint-based causal discovery algorithm using `causallearn`. Algorithmic primitive for causal reasoning.  
**Imports:** `causallearn.search.ConstraintBased.PC`, `causallearn.utils.GraphUtils`, `causallearn.utils.cit`, `numpy`, `logging`  
**Dependency Risk:** `causallearn` library must be installed. Not in `requirements.txt` — add before extraction.

---

### `check_imports.py`
**Extract Target:** Dev tooling / CI utilities  
**Salvageable Logic:** `check_imports(path) → List[str]` — AST-based import health checker. Useful as a standalone dev utility.  
**Imports:** `ast`, `importlib.util`, `os`  
**Dependency Risk:** `importlib.util` — flagged missing by stdlib baseline check but is part of stdlib. No real broken dep.

---

### `config.py`
**Extract Target:** SOP deployment configuration layer  
**Salvageable Logic:** `LLMConfig` dataclass and `load_config()` — environment-variable-driven LLM configuration loader. Pattern is reusable in SOP config surfaces.  
**Imports:** `__future__`, `os`, `dataclasses`, `typing` — no broken deps.

---

### `cycle_ledger.py`
**Extract Target:** Runtime accounting / provenance tracking  
**Salvageable Logic:** `write_cycle_ledger` — SHA-256-based bundle hashing and JSONL ledger writing. `_sha256_file`, `_normalize_path`, `_collect_bundle_hashes` are clean cryptographic utility functions.  
**Imports:** `__future__`, `hashlib`, `json`, `pathlib`, `typing` — no broken deps.

---

### `evidence.py`
**Extract Target:** Epistemic tracking / provenance layer  
**Salvageable Logic:** `normalize_evidence_refs`, `evidence_to_citation_string`, `is_proved_reference`, `validate_evidence_ref` — evidence normalization and citation formatting utilities.  
**Imports:** `logos` _(for `logos.ledger` or similar)_ — this import may reference archived paths.  
**Dependency Risk:** `logos` package reference must be resolved against the current runtime.

---

### `guardrails.py`
**Extract Target:** Governance enforcement / SOP safety layer  
**Salvageable Logic:** `require_safe_interfaces`, `restrict_writes_to` decorators — filesystem write restriction and interface safety guardrails. `get_mission_profile` loader.  
**Imports:** `Logos_System.System_Stack.System_Operations_Protocol.infrastructure.agent_system.agent_nexus` — this path is not present in `LOGOS_SYSTEM` proper (only in `_Dev_Resources/STAGING`).  
**Dependency Risk:** The `agent_nexus` import is broken; the decorator logic itself is safe to extract without it.

---

### `io_normalizer.py`
**Extract Target:** Any protocol intake layer (SOP/MTP/ARP)  
**Salvageable Logic:** `IONormalizer` class — `normalize_payload`, `normalize`, `batch_normalize`. Normalizes JSON payloads with timestamp injection and type coercion.  
**Imports:** `json`, `datetime`, `typing` — no broken deps.

---

### `iterative_loop.py`
**Extract Target:** RGE cognition cycle / SCP iterative processing  
**Salvageable Logic:** `run_iterative_stabilization` — iterative convergence loop with configurable max iterations, tolerance, and per-step transform application via `TransformRegistry`.  
**Imports:** `transform_registry` _(within utils)_, `transform_types` _(missing)_  
**Dependency Risk:** `transform_types` is not present in utils or LOGOS_SYSTEM. Must be defined before extraction. `transform_registry` is in utils (also EXTRACT_LOGIC).

---

### `kernel.py`
**Extract Target:** RGE / OBDC bijective kernel  
**Salvageable Logic:** `OBDCKernel` — `apply_bijection`, `commute`, `register_verified_bijection`, `verify_structure_preservation`. Implements an order-preserving bijective dual commutation kernel.  
**Imports:** `Logos_Protocol.logos_core.reference_monitor` — this path does NOT exist in the current architecture (no `Logos_Protocol/logos_core/reference_monitor.py` found).  
**Dependency Risk:** Reference monitor import is broken. The bijection and commutation logic itself is salvageable without it.

---

### `logging_utils.py`
**Extract Target:** Any runtime layer (generic)  
**Salvageable Logic:** `log_event`, `dumps_log` — structured JSON event logging with timestamp and level. Minimal and clean.  
**Imports:** `__future__`, `json`, `time`, `typing` — no broken deps.

---

### `ontology_inducer.py`
**Extract Target:** SCP / ARP reasoning primitives  
**Salvageable Logic:** `OntologyInducer.induce()` — async ontology induction algorithm. Pattern is reusable.  
**Imports:** `logos_validator_hub`, `async_workers`, `config_loader` — all three are missing.  
**Dependency Risk:** All three external imports are broken stubs. The induction logic pattern is salvageable with replacement interfaces.

---

### `policy.py`
**Extract Target:** Governance enforcement layer  
**Salvageable Logic:** `PolicyManager` — full YAML-driven policy enforcement system with rate limiting, resource constraint checking, approval thresholds, emergency stop, and violation callbacks. `PolicyViolation` and `PolicyMetrics` dataclasses.  
**Imports:** `logging`, `dataclasses`, `datetime`, `pathlib`, `typing`, `yaml` — no broken deps.

---

### `progressive_router.py`
**Extract Target:** UIP / SOP protocol mediation  
**Salvageable Logic:** `ProgressiveRouter.route_user_input()` — multi-step adaptive routing pipeline with metrics tracking, synthesis context construction, and error response generation.  
**Imports:** `uip_protocol.core_processing.registry`, `input.input_handler`, `output.response_formatter`, `system_utilities.system_utils` — all missing.  
**Dependency Risk:** All four external imports are broken. Extract only the routing pipeline logic; replace imports with protocol-layer equivalents.

---

### `router.py`
**Extract Target:** SOP / ARP routing dispatch  
**Salvageable Logic:** `InteractionRouter` — thread-safe prompt queue, producer-consumer loop, interaction logging. `enqueue_prompt`, `process_prompt`, `start_prompt_loop` patterns.  
**Imports:** `input_output_processing.parser`, `metadata_filters.response_engine`, `core_processing.sanitizer` — all missing.  
**Dependency Risk:** Three external imports are broken. Queue and routing loop logic is standalone.

---

### `sanitizer.py`
**Extract Target:** Any intake layer (SOP/UIP/MTP)  
**Salvageable Logic:** `Sanitizer.sanitize()` — regex-based input sanitization with configurable forbidden patterns, max-length enforcement, and result metadata.  
**Imports:** `__future__`, `dataclasses`, `logging`, `re`, `typing` — no broken deps.

---

### `schema_utils.py`
**Extract Target:** Any schema validation surface  
**Salvageable Logic:** `require_dict`, `require_str`, `get_str`, `get_dict`, `get_list` — typed JSON schema accessor utilities with clean error messaging.  
**Imports:** `errors` — this custom module is missing.  
**Dependency Risk:** `errors` import is broken. The accessor functions themselves are trivially extractable without it.

---

### `self_diagnosis.py`
**Extract Target:** SOP runtime health monitoring  
**Salvageable Logic:** `SelfDiagnosisTool` — comprehensive async health probe covering CPU, memory, disk, network, process, and filesystem checks. `HealthStatus` and `HealthCheck` dataclasses.  
**Imports:** `psutil` — present as a system package requirement.  
**Dependency Risk:** `psutil` must be in `requirements.txt`. Verify before extraction.

---

### `shared_resources.py`
**Extract Target:** RUNTIME_SHARED_UTILS / SOP resource layer  
**Salvageable Logic:** `ResourceManager` — async resource leasing with capacity enforcement, event recording, and utilisation tracking. `ResourceLease` context manager. `stream_snapshots` generator.  
**Imports:** `__future__`, `asyncio`, `json`, `os`, `time`, `contextlib`, `dataclasses`, `pathlib`, `typing` — no broken deps.

---

### `skill_acquisition.py`
**Extract Target:** SCP cognition layer  
**Salvageable Logic:** `SkillAcquisition.acquire()` — async skill acquisition pipeline stub with validator gate pattern.  
**Imports:** `core.logos_validator_hub`, `core.async_workers`, `core.config_loader` — all missing.  
**Dependency Risk:** All three imports are broken. Pattern and interface are salvageable.

---

### `smp_intake.py`
**Extract Target:** SOP task intake / MTP intake contracts  
**Salvageable Logic:** `SMPEnvelope` dataclass and `load_smp()` — SMP payload loader with field validation.  
**Imports:** `I1_Agent.config.hashing`, `I1_Agent.config.schema_utils`, `I1_Agent.diagnostics.errors` — all missing (I1_Agent subpackage no longer present).  
**Dependency Risk:** All three imports are broken. Replace with current schema_utils equivalent.

---

### `system_utils.py`
**Extract Target:** SOP / UIP telemetry / observability layer  
**Salvageable Logic:** `get_current_timestamp`, `log_uip_event`, `generate_correlation_id`, `record_request_outcome`, `observe_request_latency`, `export_metrics` — UIP event logging and metrics export utilities.  
**Imports:** `structlog`, `prometheus_client` — both are external packages not confirmed in `requirements.txt`.  
**Dependency Risk:** `structlog` and `prometheus_client` must be added to `requirements.txt` before extraction.

---

### `task_intake.py`
**Extract Target:** SOP task dispatch  
**Salvageable Logic:** `TaskEnvelope` dataclass and `load_task()` — task payload normalizer with field validation.  
**Imports:** `I3_Agent.config.schema_utils`, `I3_Agent.diagnostics.errors` — both missing (I3_Agent subpackage no longer present).  
**Dependency Risk:** Both imports are broken. Replace with current schema validation surface.

---

### `transform_registry.py`
**Extract Target:** Protocol transformation layers (generic)  
**Salvageable Logic:** `TransformRegistry` — pluggable transform registration and dispatch: `normalize`, `reframe`, `decompose`, `annotate`. Clean registry pattern.  
**Imports:** `transform_types` — missing.  
**Dependency Risk:** `transform_types` is not present. Must define the type interface before extraction.

---

### `uip_operations.py`
**Extract Target:** UIP / SOP interface operations  
**Salvageable Logic:** `UIPOperations` — full 4-phase initialization stack (GUI, input processing, protocol integration, response synthesis) and 7-step user interaction pipeline. Interface patterns and step sequencing logic are salvageable.  
**Imports:** `sys`, `os`, `logging`, `time`, `argparse`, `typing`, `json` — no broken deps.  
**Note:** Runtime stubs abound — all `_phase_*` and `_step_*` methods are structural skeletons rather than live implementations.

---

## SECTION 4 — OBSOLETE MODULES

Modules that reference removed runtime surfaces, deprecated external dependencies, or have no relevance to the current LOGOS architecture.

**Count: 15**

---

### `External_Enhancements_Registry.py`
**Reason:** Implements a `Wrapper_Info` registry for external enhancement wrappers. No corresponding `External_Enhancements` surface exists in the current LOGOS_SYSTEM architecture.  
**Recommendation:** Discard. No salvageable logic not already covered by current transform/registry patterns.

---

### `LOGOS.py`
**Reason:** Monolithic `LOGOSLauncher` entrypoint — implements a legacy launch procedure calling subsystems via `entry` import. Superseded entirely by `System_Entry_Point` and `GOVERNANCE_ENFORCEMENT` layers.  
**Broken Imports:** `entry` (module not found in current architecture).  
**Recommendation:** Discard. Successor: `LOGOS_SYSTEM/System_Entry_Point/`.

---

### `Visualization_Wrapper_Matplotlib.py`
**Reason:** Visualization wrapper implementing a `Visualization_Wrapper_Matplotlib` class that stubs a runtime display context. Imports from `Logos_System.System_Entry_Point.Orchestration_Tools` and `Logos_System.System_Stack.Logos_Protocol.External_Enhancements.Constraint_Stubs` — neither path exists in the current LOGOS_SYSTEM.  
**Broken Imports:** `Logos_System.System_Entry_Point.Orchestration_Tools`, `Logos_System.System_Stack.Logos_Protocol.External_Enhancements.Constraint_Stubs`  
**Recommendation:** Discard. No visualization/display layer exists in the current LOGOS runtime architecture.

---

### `bdn_adapter.py`
**Reason:** BDN (Bayesian/Dependency Network) adapter stub. Depends on `bdn_types` module which is not present anywhere in the current workspace. The `IBDNAdapter` / `StubBDNAdapter` pattern references a subsystem that has been removed.  
**Broken Imports:** `bdn_types`  
**Recommendation:** Discard. MVS/BDN subsystems are no longer part of the active architecture.

---

### `client.py`
**Reason:** `LLMClient` class providing a provider-agnostic LLM interface. Depends on `providers_openai` and `providers_llama` — neither module exists in the workspace. Also depends on `types` (custom module, not stdlib).  
**Broken Imports:** `types` (custom), `providers_openai`, `providers_llama`  
**Recommendation:** Discard. LLM client functionality is now provided via the `llm_advisor` pattern or external SDK directly.

---

### `deploy_full_stack.py`
**Reason:** Full-stack deployment orchestrator implementing Docker and local process management. Superseded by deployment helpers in `System_Stack` and `Utilities/deploy_full_stack.py` / `deploy_full_stack.py` at the workspace root.  
**Note:** The `signal` import was flagged as missing by the classifier but `signal` is part of Python stdlib — this is a classifier false positive.  
**Recommendation:** Discard. Functionally duplicated by current deployment infrastructure.

---

### `llm_advisor.py`
**Reason:** `LLMAdvisor` class that proxies OpenAI/Anthropic APIs and sanitizes LLM proposals. Imports `scripts.evidence` — a path that references the `scripts.llm_interface_suite` archived path. The `importlib` import is stdlib but the broader dependency on `scripts.*` paths is obsolete.  
**Broken Imports:** `scripts.evidence` (legacy path)  
**Recommendation:** Discard. LLM advisory functionality should be rebuilt against current protocol-mediated tool evaluation layer (`GOVERNANCE_ENFORCEMENT/Protocol_Mediated_Tool_Evaluation/`).

---

### `logos_agent_system.py`
**Reason:** Monolithic agent system implementing `SystemAgent`, `UserAgent`, `ProtocolOrchestrator`, and `AgentRegistry`. Inner boot logic depends on `boot_system`, `runtime_operations`, `local_scp` — all missing modules from the pre-protocol-layer architecture.  
**Broken Imports:** `boot_system`, `runtime_operations`, `local_scp`  
**Recommendation:** Discard. Superseded by `GOVERNANCE_ENFORCEMENT/Agent_Invocation/` and `GOVERNANCE_ENFORCEMENT/Runtime_Enforcement/Runtime_Spine/Agent_Orchestration/`.

---

### `logos_agi_adapter.py`
**Reason:** Legacy `LogosAgiNexus` adapter referencing `Logos_AGI.*` package paths (`Logos_AGI.Advanced_Reasoning_Protocol.arp_bootstrap`, `Logos_AGI.Synthetic_Cognition_Protocol.*`, `Logos_AGI.System_Operations_Protocol.*`). The `Logos_AGI` package namespace no longer exists — the architecture was reorganized into `LOGOS_SYSTEM` with separate protocol layers.  
**Broken Imports:** `LOGOS_SYSTEM.System_Stack.Protocol_Resources.schemas` (System_Stack path archived), `logos.evaluator`, `logos.uwm`, `logos.proof_refs`, `logos.policy`, `Logos_AGI.Advanced_Reasoning_Protocol.arp_bootstrap`, `Logos_AGI.Synthetic_Cognition_Protocol.system_utilities.nexus.scp_nexus`, `Logos_AGI.System_Operations_Protocol.infrastructure.agent_system.base_nexus`  
**Recommendation:** Discard. The adapter pre-dates the current protocol layer separation. Working memory and belief logic may have partial counterparts in `RUNTIME_BRIDGE` — review separately.

---

### `logos_gpt_chat.py`
**Reason:** Command-line GPT chat interface depending on `logos.uwm`, `logos.ledger`, `logos.proof_refs`, `scripts.llm_interface_suite.llm_advisor`, `LOGOS_SYSTEM.System_Stack.Protocol_Resources.*`. `System_Stack` is an archived path hierarchy.  
**Broken Imports:** `logos.uwm`, `logos.ledger`, `logos.proof_refs`, `scripts.llm_interface_suite.llm_advisor`, `LOGOS_SYSTEM.System_Stack.Protocol_Resources.schemas`, `scripts.start_agent`, `logos.tool_registry_loader`, `LOGOS_SYSTEM.System_Stack.Protocol_Resources.attestation`  
**Recommendation:** Discard. Chat interface functionality is not part of the current runtime architecture.

---

### `logos_gpt_server.py`
**Reason:** FastAPI-based GPT server with WebSocket chat. Depends on the full legacy `scripts.llm_interface_suite.*` and `LOGOS_SYSTEM.System_Stack.Protocol_Resources.*` hierarchies — both archived.  
**Broken Imports:** `scripts.llm_interface_suite.logos_gpt_chat`, `logos.ledger`, `logos.proof_refs`, `logos.uwm`, `scripts.llm_interface_suite.llm_advisor`, `scripts.evidence`, `LOGOS_SYSTEM.System_Stack.Protocol_Resources.schemas`, `scripts.start_agent`, `logos.tool_registry_loader`, `scripts.nexus_manager`, `attestation` (standalone), `LOGOS_SYSTEM.System_Stack.Protocol_Resources.attestation`  
**Recommendation:** Discard. FastAPI server entrypoints are no longer part of the LOGOS runtime surface.

---

### `mvs_adapter.py`
**Reason:** MVS (Multi-Vector Subsystem?) adapter stub implementing `IMVSAdapter` protocol. Depends on `mvs_types` module — removed external dependency with no replacement.  
**Broken Imports:** `mvs_types`  
**Recommendation:** Discard. MVS subsystem has been removed from the architecture.

---

### `run_logos_gpt_acceptance.py`
**Reason:** Acceptance test script for the deprecated GPT server interface. Spawns processes and validates GPT server behavior. The GPT server itself (`logos_gpt_server.py`) is classified OBSOLETE_MODULE.  
**Imports:** Stdlib only — `hashlib`, `json`, `os`, `subprocess`, `sys`, `datetime`, `pathlib`, `typing` — no broken imports.  
**Note:** No broken deps, but the target system under test is obsolete.  
**Recommendation:** Discard. The tested surface no longer exists.

---

### `simple_julia.py`
**Reason:** Julia set fractal generator using `numpy` and `matplotlib`. No corresponding computation or visualization layer in the LOGOS architecture. This is a standalone mathematical demo with no protocol-layer relevance.  
**Imports:** `numpy`, `matplotlib.pyplot`, `matplotlib.colors`, `argparse`  
**Recommendation:** Discard. No LOGOS runtime surface.

---

### `start_agent.py`
**Reason:** Legacy monolithic agent boot script with ~80+ functions covering sandbox isolation, tool dispatch, attestation loading, proof compilation, integrity baseline enforcement, and agent identity management. Imports from `external.Logos_AGI.*`, `JUNK_DRAWER.*`, `logos_core.*`, `Logos_Agent.*`, `plugins.*`, `System_Stack.*` — all obsolete address spaces.  
**Broken Imports:** `external.Logos_AGI.identity_paths`, `external.Logos_AGI.System_Operations_Protocol.alignment_protocols.safety.integrity_framework.integrity_safeguard`, `plugins.uip_integration_plugin`, `JUNK_DRAWER.scripts.runtime.need_to_distribute.logos_agi_adapter`, `logos_core.governance.agent_identity`, `logos_core.governance.commitment_ledger`, `logos_core.governance.prioritization`, `Logos_Agent.scripts.genesis_capsule`, `plugins.guardrails`, `JUNK_DRAWER.scripts.need_to_distribute.cycle_ledger`, `need_to_distribute.logos_agi_adapter`, `System_Stack.Logos_Protocol.Protocol_Core.Runtime_Operations.tools.implementations`, `logos_core.world_model.uwm`  
**Recommendation:** Discard as a module. **Individual functions** (`_sha256`-based hashing utilities, `dispatch_tool` dispatch table, `configure_sandbox` isolation pattern) may be worth reviewing for extraction into `GOVERNANCE_ENFORCEMENT` if not already re-implemented.

---

## SECTION 5 — DEPENDENCY RISKS

### 5.1 Intra-Utils Dependencies (modules that import other utils modules)

| Module | Depends On (within utils) | Risk |
|--------|--------------------------|------|
| `client.py` | `config` | Low — both are EXTRACT_LOGIC; migrate together |
| `iterative_loop.py` | `transform_registry` | Low — both are EXTRACT_LOGIC; migrate together |
| `start_agent.py` | `llm_advisor` | High — both are OBSOLETE_MODULE; do not migrate |

### 5.2 Broken External Dependencies (imports that resolve to no existing module)

| Module | Broken Import(s) | Classification Impact |
|--------|-----------------|----------------------|
| `LOGOS.py` | `entry` | Confirms OBSOLETE |
| `Visualization_Wrapper_Matplotlib.py` | `Logos_System.System_Entry_Point.Orchestration_Tools`, `Logos_System.System_Stack.Logos_Protocol.External_Enhancements.Constraint_Stubs` | Confirms OBSOLETE |
| `bdn_adapter.py` | `bdn_types` | Confirms OBSOLETE |
| `causal_chain_node_predictor.py` | `causallearn.search.ConstraintBased.PC`, `causallearn.utils.GraphUtils`, `causallearn.utils.cit` | Mitigable — install `causallearn` |
| `check_imports.py` | `importlib.util` | False positive — stdlib |
| `check_run_cycle_prereqs.py` | `LOGOS_AGI.settings`, `LOGOS_AGI.analytics` | Must validate against SOP |
| `client.py` | `types` (custom), `providers_openai`, `providers_llama` | Confirms OBSOLETE |
| `deploy_full_stack.py` | `signal` | False positive — stdlib |
| `guardrails.py` | `Logos_System.System_Stack.System_Operations_Protocol.infrastructure.agent_system.agent_nexus` | Not in LOGOS_SYSTEM; only in STAGING |
| `iel_integration.py` | `iel_registry` | Must resolve from IEL layer |
| `iel_registryv1.py` | `iel_generator`, `iel_evaluator` | Must resolve from IEL layer |
| `iterative_loop.py` | `transform_types` | Must define type interface |
| `llm_advisor.py` | `importlib` | False positive — stdlib (but `scripts.evidence` is broken) |
| `logos_agent_system.py` | `boot_system`, `runtime_operations`, `local_scp` | Confirms OBSOLETE |
| `logos_agi_adapter.py` | `LOGOS_SYSTEM.System_Stack.*`, `Logos_AGI.*`, `logos.*` | Confirms OBSOLETE — multiple archived paths |
| `logos_gpt_chat.py` | `logos.uwm`, `logos.ledger`, `logos.proof_refs`, `scripts.*`, `LOGOS_SYSTEM.System_Stack.*` | Confirms OBSOLETE |
| `logos_gpt_server.py` | `scripts.llm_interface_suite.*`, `logos.*`, `LOGOS_SYSTEM.System_Stack.*` | Confirms OBSOLETE |
| `ontology_inducer.py` | `logos_validator_hub`, `async_workers`, `config_loader` | Broken stubs — replace with current interfaces |
| `progressive_router.py` | `uip_protocol.core_processing.registry`, `input.input_handler`, `output.response_formatter`, `system_utilities.system_utils` | All broken — extract routing logic only |
| `router.py` | `input_output_processing.parser`, `metadata_filters.response_engine`, `core_processing.sanitizer` | All broken — extract queue logic only |
| `schema_utils.py` | `errors` (custom) | Replace with current error surface |
| `self_diagnosis.py` | `psutil` | Add to `requirements.txt` |
| `skill_acquisition.py` | `core.logos_validator_hub`, `core.async_workers`, `core.config_loader` | All broken — extract pattern only |
| `smp_intake.py` | `I1_Agent.config.hashing`, `I1_Agent.config.schema_utils`, `I1_Agent.diagnostics.errors` | I1_Agent subpackage removed — replace |
| `start_agent.py` | 13+ broken imports across `JUNK_DRAWER`, `logos_core`, `plugins`, `Logos_Agent`, `external.Logos_AGI`, `System_Stack` | Confirms OBSOLETE |
| `stress_sop_runtime.py` | `importlib`, `importlib.util` | False positive — stdlib |
| `system_utils.py` | `structlog`, `prometheus_client` | Add to `requirements.txt` |
| `task_intake.py` | `I3_Agent.config.schema_utils`, `I3_Agent.diagnostics.errors` | I3_Agent subpackage removed — replace |
| `transform_registry.py` | `transform_types` | Must define type interface |
| `worker_kernel.py` | `unified_classes` | Must resolve — `LOGOS_SYSTEM.RUNTIME_SHARED_UTILS.system_imports` is live |

### 5.3 Circular Import Risk

**No circular imports detected** within the utils directory.  
The only intra-utils dependency chain is:  
`iterative_loop` → `transform_registry` → `transform_types` (external, missing)  
This chain is linear, not circular.

`start_agent` → `llm_advisor` is also linear.

---

## SECTION 6 — SUMMARY

| Classification | Count | Percentage |
|---------------|-------|-----------|
| ACTIVE_MODULE | 7 | 14.6% |
| EXTRACT_LOGIC | 26 | 54.2% |
| OBSOLETE_MODULE | 15 | 31.3% |
| **TOTAL** | **48** | **100%** |
| Parse Errors | 0 | — |
| Files Modified | 0 | — |

### Active Module Targets (7)

| Module | Target Protocol Surface |
|--------|------------------------|
| `check_run_cycle_prereqs` | SOP prerequisite gate |
| `iel_integration` | Internal_Emergent_Logics (IEL) |
| `iel_registryv1` | IEL registry subsystem (consolidate with v2) |
| `iel_registryv2` | IEL registry subsystem (preferred candidate) |
| `logos_monitor` | System_Operations_Protocol monitoring |
| `stress_sop_runtime` | SOP runtime stress suite |
| `worker_kernel` | RUNTIME_SHARED_UTILS worker layer |

### Priority EXTRACT_LOGIC Candidates

The following are highest-priority for logic extraction based on clean imports and generic utility value:

| Module | Priority | Target Layer |
|--------|----------|-------------|
| `sanitizer` | HIGH | Any intake layer |
| `io_normalizer` | HIGH | Protocol intake |
| `logging_utils` | HIGH | Any runtime layer |
| `cycle_ledger` | HIGH | Runtime accounting / provenance |
| `policy` | HIGH | Governance enforcement |
| `shared_resources` | HIGH | RUNTIME_SHARED_UTILS |
| `bridge` | MEDIUM | RUNTIME_BRIDGE |
| `transform_registry` | MEDIUM | Protocol transformation |
| `schema_utils` | MEDIUM | Schema validation |
| `self_diagnosis` | MEDIUM | SOP health monitoring |
| `router` | MEDIUM | SOP/ARP routing |
| `system_utils` | MEDIUM | SOP/UIP telemetry |
| `uip_operations` | MEDIUM | UIP interface |

### SCAN_ERRORS

None. All 48 modules parsed without error.

---

## VALIDATION

- [x] All 48 modules in the directory were analyzed
- [x] No files were modified (READ-ONLY scan)
- [x] Python AST used — no code execution of scanned modules
- [x] Report written to `/workspaces/Logos/_Reports/utils_recovery_scan_report.md`
- [x] Classification is deterministic — each module assigned exactly one category

---

*Report generated by static AST scan. Classification is based on import surface analysis against `/workspaces/Logos/LOGOS_SYSTEM` directory tree and known protocol layer namespaces. No module was executed during this scan.*

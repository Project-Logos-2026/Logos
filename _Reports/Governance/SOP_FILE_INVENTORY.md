# SOP File Inventory

Scope: SOP-owned files, SOP building blocks, SOP test references, and SOP governance references in documentation.

## Classification Key
- KEEP: Canonical or authoritative reference
- REFACTOR: Needs rewrite or relocation
- DEPRECATE: Legacy or superseded; retain only for audit
- DELETE: Explicitly obsolete

## SOP Runtime-Operations Layer
| Path | Type | Classification | Notes |
| --- | --- | --- | --- |
| [LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol](LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol) | Directory | REFACTOR | SOP root exists but only contains SOP_Nexus; missing canonical sub-areas. |
| [LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus](LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus) | Directory | REFACTOR | Contains execution-style nexus core; not SOP operations-side specific. |
| [LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py](LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/System_Operations_Protocol/SOP_Nexus/SOP_Nexus.py) | File | REFACTOR | Execution-side Nexus core copied into SOP; lacks SOP-specific ops-only constraints. |

## SOP Building Blocks (Design/Legacy)
| Path | Type | Classification | Notes |
| --- | --- | --- | --- |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS) | Directory | REFACTOR | Draft design assets; should migrate into SOP documentation. |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_BLUEPRINT_DRAFT.md) | File | KEEP | Design-only blueprint; needs alignment with current runtime paths. |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus) | Directory | REFACTOR | Placeholder SOP nexus orchestrator. |
| [BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py](BUILDING_BLOCKS/SOP_BUILDING_BLOCKS/SOP_Nexus/sop_nexus_orchestrator.py) | File | REFACTOR | Production header but only stub classes; should become real ops-side orchestrator or be replaced. |
| [BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1](BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1) | Directory | REFACTOR | Contains SOP-DRAC contract; should live in SOP contracts or governance references. |
| [BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md](BUILDING_BLOCKS/DRAC_BUILDING_BLOCKS/DRAC_PROTOCOL_V1/SOP_DRAC_CAPABILITY_REQUEST_CONTRACT.md) | File | KEEP | Contract definition; needs relocation to SOP governance or SOP docs. |

## SOP Legacy Rewrite Candidates (INVARIABLES)
| Path | Type | Classification | Notes |
| --- | --- | --- | --- |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus.py) | File | DEPRECATE | Marked legacy rewrite candidate; includes self-improvement and broad ops authority. |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_operations.py) | File | DEPRECATE | Legacy ops script; violates ops-only boundary and mixes protocol startup logic. |
| [BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus_orchestrator.py](BUILDING_BLOCKS/INVARIABLES/APPLICATION_FUNCTIONS/Utilities/sop_nexus_orchestrator.py) | File | DEPRECATE | Legacy stub with rewrite marker. |

## SOP Test References (Orphaned)
All SOP test stubs point to System_Stack paths that are not present in the repo; keep as references but mark for refactor.
| Path | Classification | Notes |
| --- | --- | --- |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_SOP_Nexus_sop_nexus_orchestrator.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_SOP_Nexus_sop_nexus_orchestrator.py) | REFACTOR | Points to Logos_System.System_Stack.System_Operations_Protocol.* which is absent. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_examples_demo_integrated_ml.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_examples_demo_integrated_ml.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_kernel.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_kernel.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_hardening.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_hardening.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_integration.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_integration.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_nexus_capability_governance.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_nexus_capability_governance.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_api_server.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_api_server.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_agent_planner.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_agent_planner.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_data_storage_system_memory.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_data_storage_system_memory.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_base_nexus.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_base_nexus.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_compliance_integration_harmonizer.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_compliance_integration_harmonizer.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_local_scp.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_local_scp.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_policies_privative_policies.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_policies_privative_policies.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_verify_pai.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_verify_pai.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_proposal_pipeline.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_proposal_pipeline.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_health_server.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_health_server.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_logos_monitor.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_logos_monitor.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_boot_extensions_loader.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_boot_extensions_loader.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_pai.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_pai.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_logos_agent_system.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_logos_agent_system.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_agent_nexus.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_agent_nexus.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_iel_integration.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_iel_integration.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_unified_classes.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_unified_classes.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_policy.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_policy.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_persistence_persistence.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_persistence_persistence.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_ultima_framework_ultima_safety.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_ultima_framework_ultima_safety.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_test_tool_fallback_proposal.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_test_tool_fallback_proposal.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_coherence_metrics.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_coherence_metrics.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_deploy_core_services.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_deploy_core_services.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_enhanced_reference_monitor.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_enhanced_reference_monitor.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_logos_agi_persistence_smoke.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_logos_agi_persistence_smoke.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_protocol_integration.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_protocol_integration.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_prioritization.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_prioritization.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_entry.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_entry.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_self_improvement_cycle.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_self_improvement_cycle.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_capabilities.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_capabilities.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_optimizer.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_optimizer.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_simulation_cli.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_simulation_cli.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_integration_test_suite.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_integration_test_suite.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_privative_policies.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_privative_policies.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_worker_kernel.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_worker_kernel.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_end_to_end_pipeline.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_end_to_end_pipeline.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_repair_proposal.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_repair_proposal.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_system_imports.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_system_imports.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_invention.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_invention.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_check_imports.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_check_imports.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_integrity_framework_integrity_safeguard.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_integrity_framework_integrity_safeguard.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_introspection.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_introspection.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_tests_test_self_improvement_cycle.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_tests_test_self_improvement_cycle.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_chain_executor.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tool_chain_executor.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_boot_system.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_boot_system.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_maintenance.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_maintenance.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_coherence_optimizer.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_coherence_coherence_optimizer.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_server.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_server.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_reference_monitor.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_test_reference_monitor.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_logos_agi_adapter.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_logos_agi_adapter.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_validate_production.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_validation_testing_validate_production.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_demo_gui.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_demo_gui.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_deploy_full_stack.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_monitoring_deploy_full_stack.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_reference_monitor.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_reference_monitor.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_io_normalizer.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_io_normalizer.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_perception_ingestors.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_perception_ingestors.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_bayesian_data_handler.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_tests_test_bayesian_data_handler.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_check_run_cycle_prereqs.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_Optimization_check_run_cycle_prereqs.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_shared_resources.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_shared_resources.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_initialize_agent_system.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_infrastructure_agent_system_initialize_agent_system.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_LOGOS.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_deployment_configuration_LOGOS.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_core_service.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_core_service.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_persistence.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_governance_persistence.py) | REFACTOR | Orphaned test path. |
| [LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_obdc_kernel.py](LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_System_Operations_Protocol_alignment_protocols_safety_obdc_kernel.py) | REFACTOR | Orphaned test path. |

## SOP Governance and Architecture References (Docs)
| Path | Type | Classification | Notes |
| --- | --- | --- | --- |
| [DOCUMENTS/RUNTIME_DIRECTORY_TREE.md](DOCUMENTS/RUNTIME_DIRECTORY_TREE.md) | File | KEEP | Authoritative runtime layout includes SOP directories not present in repo. |
| [DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md](DOCUMENTS/GOVERNANCE_ENFORCEMENT_INDEX.md) | File | KEEP | Maps governance to SOP enforcement points. |
| [DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md](DOCUMENTS/RUNTIME_DEPENDENCY_AND_GOVERNANCE_MAPPING.md) | File | KEEP | Defines SOP authority role and dependency flow. |
| [DOCUMENTS/FAIL-CLOSED_RUNTIME_CHECKLIST.md](DOCUMENTS/FAIL-CLOSED_RUNTIME_CHECKLIST.md) | File | KEEP | SOP_Nexus required for fail-closed runtime. |
| [DOCUMENTS/MEMORY_DOMAIN_SEPARATION.md](DOCUMENTS/MEMORY_DOMAIN_SEPARATION.md) | File | KEEP | SOP memory domain separation and audit constraints. |
| [DOCUMENTS/RUNTIME_IMPORT_AND_AUTHORITY_GRAPH.md](DOCUMENTS/RUNTIME_IMPORT_AND_AUTHORITY_GRAPH.md) | File | KEEP | SOP observability-only role and audit path. |
| [DOCUMENTS/RUNTIME_GOVERNANCE_ALIGNMENT.md](DOCUMENTS/RUNTIME_GOVERNANCE_ALIGNMENT.md) | File | KEEP | SOP mapped to ops-only governance role. |

## Notable Missing SOP Directories (Referenced in Docs)
- System_Operations_Protocol/Governance_Enforcement
- System_Operations_Protocol/Deployment_Control
- System_Operations_Protocol/Telemetry
- System_Operations_Protocol/Fail_Closed_Mechanisms

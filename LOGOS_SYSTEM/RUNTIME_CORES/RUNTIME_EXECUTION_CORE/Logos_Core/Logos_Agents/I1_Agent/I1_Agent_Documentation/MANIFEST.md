# I1_Agent Documentation Manifest

Entity: I1_Agent
Type: Agent
Domain: Execution
Canonical Root: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/I1_Agent

Directory inventory (files only):
- I1_Nexus.py
- __init__.py
- _core/OmniProperty_Integration.py
- _core/Sign_Principal_Operator.py
- _core/__init__.py
- config/__init__.py
- config/constants.py
- config/hashing.py
- config/logging_utils.py
- config/packet_types.py
- config/schema_utils.py
- config/time_utils.py
- connections/__init__.py
- connections/id_handler.py
- connections/router.py
- diagnostics/__init__.py
- diagnostics/errors.py
- diagnostics/health.py
- protocol_operations/__init__.py
- protocol_operations/scp_analysis/__init__.py
- protocol_operations/scp_analysis/analysis_runner.py
- protocol_operations/scp_analysis/trajectory_types.py
- protocol_operations/scp_bdn_adapter/__init__.py
- protocol_operations/scp_bdn_adapter/bdn_adapter.py
- protocol_operations/scp_bdn_adapter/bdn_types.py
- protocol_operations/scp_cycle/__init__.py
- protocol_operations/scp_cycle/cycle_runner.py
- protocol_operations/scp_cycle/policy.py
- protocol_operations/scp_integrations/__init__.py
- protocol_operations/scp_integrations/iterative_loop.py
- protocol_operations/scp_integrations/pipeline_runner.py
- protocol_operations/scp_mvs_adapter/__init__.py
- protocol_operations/scp_mvs_adapter/mvs_adapter.py
- protocol_operations/scp_mvs_adapter/mvs_types.py
- protocol_operations/scp_predict/__init__.py
- protocol_operations/scp_predict/predict_integration.py
- protocol_operations/scp_predict/risk_estimator.py
- protocol_operations/scp_runtime/__init__.py
- protocol_operations/scp_runtime/result_packet.py
- protocol_operations/scp_runtime/smp_intake.py
- protocol_operations/scp_runtime/work_order.py
- protocol_operations/scp_tests/__init__.py
- protocol_operations/scp_tests/run_pipeline_smoke.py
- protocol_operations/scp_tests/sample_smp.py
- protocol_operations/scp_transform/__init__.py
- protocol_operations/scp_transform/iterative_loop.py
- protocol_operations/scp_transform/transform_registry.py
- protocol_operations/scp_transform/transform_types.py

Scope boundaries:
- Covers I1 Nexus routing and I1 core deterministic integrations.
- Protocol operations are included as execution modules.
- Documentation is descriptive only.

No undocumented interfaces.

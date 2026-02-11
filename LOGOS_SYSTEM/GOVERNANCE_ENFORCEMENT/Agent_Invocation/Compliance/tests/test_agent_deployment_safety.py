# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_agent_deployment_safety
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tests/test_agent_deployment_safety.py.
agent_binding: None
protocol_binding: None
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tests/test_agent_deployment_safety.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import importlib
import pytest


def test_autonomy_not_available():
    # Autonomy interfaces must not exist
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("Logos_System.System_Stack.Autonomy")


def test_planning_runtime_not_available():
    # Planning runtime must not be importable or callable
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("Logos_System.System_Stack.Planning_Runtime")


def test_execution_requires_policy():
    from Logos_System.Governance.policy_checks import require_multi_tick_policy
    with pytest.raises(Exception):
        require_multi_tick_policy(None)

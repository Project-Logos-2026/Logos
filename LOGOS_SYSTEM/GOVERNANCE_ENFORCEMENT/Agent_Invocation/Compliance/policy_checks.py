# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: policy_checks
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tests/policy_checks.py.
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
  source: LOGOS_SYSTEM/GOVERNANCE_ENFORCEMENT/Agent_Invocation/Compliance/tests/policy_checks.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
Governance Policy Checks (Phase-J, minimal)

Read-only helpers to validate explicit authorization.
No runtime enablement occurs here.
"""

from LOGOS_SYSTEM.Governance.exceptions import GovernanceDenied


def require_multi_tick_policy(policy: dict):
    if not isinstance(policy, dict):
        raise GovernanceDenied("Missing multi-tick policy")

    if policy.get("authorized") is not True:
        raise GovernanceDenied("Multi-tick not authorized")

    max_ticks = policy.get("max_ticks")
    if not isinstance(max_ticks, int) or max_ticks <= 0:
        raise GovernanceDenied("Invalid max_ticks in policy")

    return max_ticks

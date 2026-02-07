# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_Agent_Safety_Shims_Capability_Router
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/Tests/test_Agent_Safety_Shims_Capability_Router.py.
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
  source: LOGOS_SYSTEM/TEST_SUITE/Tests/test_Agent_Safety_Shims_Capability_Router.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.Agent_Safety_Shims.Capability_Router"
PUBLIC_FUNCTIONS = ['validate_authz_memory_bounded', 'enable_bounded_memory_writes', 'disable_bounded_memory_writes', 'router_allows_memory_write']
PUBLIC_CLASSES = ['CapabilityRouter']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

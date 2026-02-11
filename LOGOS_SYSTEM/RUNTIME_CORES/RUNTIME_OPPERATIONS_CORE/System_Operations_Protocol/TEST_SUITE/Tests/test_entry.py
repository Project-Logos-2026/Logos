# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_entry
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/Tests/test_entry.py.
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
  source: LOGOS_SYSTEM/TEST_SUITE/Tests/test_entry.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.entry"
PUBLIC_FUNCTIONS = ['get_status', 'start_agent', 'initialize_logos_core', 'get_logos_core', 'evaluate_modal', 'evaluate_iel']
PUBLIC_CLASSES = ['LogosCoreFacade']
ENTRY_POINTS = ['get_status', 'start_agent', 'initialize_logos_core', 'get_logos_core', 'evaluate_modal', 'evaluate_iel']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

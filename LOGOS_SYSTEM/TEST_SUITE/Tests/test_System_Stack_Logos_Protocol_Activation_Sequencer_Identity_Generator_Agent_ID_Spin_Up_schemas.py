# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_System_Stack_Logos_Protocol_Activation_Sequencer_Identity_Generator_Agent_ID_Spin_Up_schemas
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Logos_Protocol_Activation_Sequencer_Identity_Generator_Agent_ID_Spin_Up_schemas.py.
agent_binding: None
protocol_binding: Logos_Protocol
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Logos_Protocol_Activation_Sequencer_Identity_Generator_Agent_ID_Spin_Up_schemas.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.schemas"
PUBLIC_FUNCTIONS = ['canonical_json_hash', 'validate_truth_annotation', 'validate_goal_candidate', 'validate_tool_proposal', 'validate_tool_validation_report', 'validate_plan_history_scored', 'validate_scp_state', 'validate_grounded_reply']
PUBLIC_CLASSES = ['SchemaError']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

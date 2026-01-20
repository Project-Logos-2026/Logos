# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.schemas"
PUBLIC_FUNCTIONS = ['canonical_json_hash', 'validate_truth_annotation', 'validate_goal_candidate', 'validate_tool_proposal', 'validate_tool_validation_report', 'validate_plan_history_scored', 'validate_scp_state', 'validate_grounded_reply']
PUBLIC_CLASSES = ['SchemaError']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

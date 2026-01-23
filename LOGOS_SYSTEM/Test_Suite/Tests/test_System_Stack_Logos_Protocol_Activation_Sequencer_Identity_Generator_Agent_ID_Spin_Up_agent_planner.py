# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.agent_planner"
PUBLIC_FUNCTIONS = ['append_digest_to_log', 'snapshot_digest_log', 'latest_digest_archive']
PUBLIC_CLASSES = ['PlannedAction', 'Goal', 'AlignmentRequiredError', 'AlignmentAwarePlanner']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.identity_loader"
PUBLIC_FUNCTIONS = ['load_persisted_identity', 'load_persisted_agent_id', 'initialize_agent_identity']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

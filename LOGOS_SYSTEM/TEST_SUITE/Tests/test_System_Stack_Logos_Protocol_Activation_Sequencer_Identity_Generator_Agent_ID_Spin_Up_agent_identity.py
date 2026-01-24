# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.agent_identity"
PUBLIC_FUNCTIONS = ['load_or_create_identity', 'validate_identity', 'update_identity', 'identity_hash', 'check_identity']
PUBLIC_CLASSES = ['PersistentAgentIdentity']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

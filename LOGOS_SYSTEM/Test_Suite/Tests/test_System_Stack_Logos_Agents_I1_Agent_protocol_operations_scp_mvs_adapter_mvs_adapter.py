# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I1_Agent.protocol_operations.scp_mvs_adapter.mvs_adapter"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['IMVSAdapter', 'StubMVSAdapter']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

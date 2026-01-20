# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.Reasoning_Engines.PXL_Engine.coherence"
PUBLIC_FUNCTIONS = ['get_consistency_check']
PUBLIC_CLASSES = ['ConsistencyLevel', 'LogicalStatement', 'ConsistencyCheck', 'CoherenceEngine']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

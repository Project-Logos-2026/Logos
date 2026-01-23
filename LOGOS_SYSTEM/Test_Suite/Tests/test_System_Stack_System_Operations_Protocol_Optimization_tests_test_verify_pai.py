# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.Optimization.tests.test_verify_pai"
PUBLIC_FUNCTIONS = ['test_fresh_start', 'test_continuity', 'test_capability_updates', 'test_policy_blocking', 'run_all_tests']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

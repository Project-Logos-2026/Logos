# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.deployment.configuration.entry"
PUBLIC_FUNCTIONS = ['initialize_logos_core', 'get_logos_core', 'shutdown_logos_core', 'evaluate_modal', 'evaluate_iel', 'evaluate_batch', 'get_status']
PUBLIC_CLASSES = ['LOGOSCore']
ENTRY_POINTS = ['initialize_logos_core', 'get_logos_core', 'evaluate_modal', 'evaluate_iel', 'get_status']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

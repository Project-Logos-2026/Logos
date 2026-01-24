# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.entry"
PUBLIC_FUNCTIONS = ['get_status', 'start_agent', 'initialize_logos_core', 'get_logos_core', 'evaluate_modal', 'evaluate_iel']
PUBLIC_CLASSES = ['LogosCoreFacade']
ENTRY_POINTS = ['get_status', 'start_agent', 'initialize_logos_core', 'get_logos_core', 'evaluate_modal', 'evaluate_iel']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

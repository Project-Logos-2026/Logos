# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.deployment.configuration.iel_integration"
PUBLIC_FUNCTIONS = ['get_iel_integration', 'initialize_iel_system']
PUBLIC_CLASSES = ['IELIntegration']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

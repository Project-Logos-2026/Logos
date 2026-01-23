# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I1_Agent.diagnostics.errors"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['LogosCoreError', 'SchemaError', 'RoutingError', 'IntegrationError']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I3_Agent._core.Omni_Property_Integration"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['OmnipresenceMetrics', 'OmnipresenceIntegration']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

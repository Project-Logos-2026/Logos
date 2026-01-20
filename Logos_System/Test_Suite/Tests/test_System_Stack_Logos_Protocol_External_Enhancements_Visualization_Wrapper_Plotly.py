# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.External_Enhancements.Visualization_Wrapper_Plotly"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['Visualization_Wrapper_Plotly']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

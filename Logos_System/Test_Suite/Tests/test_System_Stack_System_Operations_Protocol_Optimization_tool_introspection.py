# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.Optimization.tool_introspection"
PUBLIC_FUNCTIONS = ['build_capability_records', 'build_introspection_summary', 'main']
PUBLIC_CLASSES = ['ToolCapability']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

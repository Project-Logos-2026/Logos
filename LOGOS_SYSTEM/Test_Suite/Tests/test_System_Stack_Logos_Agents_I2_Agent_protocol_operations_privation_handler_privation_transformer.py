# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I2_Agent.protocol_operations.privation_handler.privation_transformer"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TransformResult', 'PrivationTransformer']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

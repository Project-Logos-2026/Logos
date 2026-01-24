# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.module_generator.development_environment"
PUBLIC_FUNCTIONS = ['get_code_environment_status', 'generate_improvement']
PUBLIC_CLASSES = ['CodeGenerationRequest', 'SOPCodeEnvironment']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

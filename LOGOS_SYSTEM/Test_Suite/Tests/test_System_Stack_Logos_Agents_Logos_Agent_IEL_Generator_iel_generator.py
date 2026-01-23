# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.IEL_Generator.iel_generator"
PUBLIC_FUNCTIONS = ['main']
PUBLIC_CLASSES = ['IELCandidate', 'GenerationConfig', 'IELGenerator', 'SafetyChecker', 'ConsistencyChecker']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

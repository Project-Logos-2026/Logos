# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.IEL_Generator.iel_registryv1"
PUBLIC_FUNCTIONS = ['main']
PUBLIC_CLASSES = ['IELRegistryEntry', 'RegistryConfig', 'RegistryStats', 'IELRegistry']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.Agent_Safety_Shims.Phase_E_Memory_Substrate"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['MemorySubstrate']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

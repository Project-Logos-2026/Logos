# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.Phase_E.Phase_E_Capability_Router"
PUBLIC_FUNCTIONS = ['validate_authz_memory_bounded', 'enable_bounded_memory_writes', 'disable_bounded_memory_writes', 'router_allows_memory_write']
PUBLIC_CLASSES = ['CapabilityRouter']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.alignment_protocols.safety.privative_policies"
PUBLIC_FUNCTIONS = ['Good', 'TrueP', 'Coherent', 'obligation_for', 'preserves_invariants']
PUBLIC_CLASSES = ['PrivativePolicies']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

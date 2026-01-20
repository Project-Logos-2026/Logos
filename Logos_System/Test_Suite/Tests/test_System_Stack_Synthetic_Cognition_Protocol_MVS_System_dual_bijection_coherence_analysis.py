# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.dual_bijection_coherence_analysis"
PUBLIC_FUNCTIONS = ['f', 'f_inv', 'g', 'g_inv', 'demonstrate_dual_bijection_fix']
PUBLIC_CLASSES = ['DualBijectionSystem']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

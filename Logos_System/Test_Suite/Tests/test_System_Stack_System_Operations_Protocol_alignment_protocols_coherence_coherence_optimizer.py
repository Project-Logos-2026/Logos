# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.alignment_protocols.coherence.coherence_optimizer"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['OptimizationMethod', 'Parameter', 'OptimizationResult', 'OptimizerConfig', 'CoherenceOptimizer', 'SafetyChecker', 'VerificationGate']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

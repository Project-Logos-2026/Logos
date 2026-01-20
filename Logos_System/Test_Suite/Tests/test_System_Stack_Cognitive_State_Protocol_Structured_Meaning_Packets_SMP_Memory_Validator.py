# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.Structured_Meaning_Packets.SMP_Memory_Validator"
PUBLIC_FUNCTIONS = ['initialize_system_b']
PUBLIC_CLASSES = ['RefinedSMP', 'ConstraintReport', 'TLMToken', 'ConstraintResult', 'MeshHolismValidator', 'TrinitarianOptimizationEngine', 'TLMKeyManager', 'SignConstraint', 'MindConstraint', 'BridgeConstraint', 'MeshHolism', 'TrinitarianOptimizer', 'TranscendentalLockingMechanism', 'ConstraintPipeline']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.Structured_Meaning_Packets.SMP_Evaluator"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['EvaluationPerspective', 'TriuneCommutationResult', 'SMPGroundingLevel', 'PXLIELSEvaluator', 'ETGCEvaluator', 'PrivationEvaluator', 'TriuneCommutationEngine', 'SystemMemoryRouter']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.trinity_framework"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TrinitarianMode', 'TrinitarianState', 'TrinitarianStructure', 'DialecticEngine', 'ModalIntegrator', 'GodelianDesireDriver', 'IncompletenessHandler', 'DesireOptimizer', 'SelfReferenceDetector', 'FractalOntology', 'ScalingEngine', 'TrinityFramework']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.three_pillars_framework"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['MeshDomain', 'Transcendental', 'LogicLaw', 'CoreAxiom', 'AxiomValidator', 'LogosOperator', 'BanachTarskiProbabilityOperator', 'MandelbrotOperator', 'TrinityOptimizer', 'MESHIntegrator', 'OBDCKernel', 'EmpiricalPredictor', 'PhilosophicalProblemResolver', 'ThreePillarsSystem']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

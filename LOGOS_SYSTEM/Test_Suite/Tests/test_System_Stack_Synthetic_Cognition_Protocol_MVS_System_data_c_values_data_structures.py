# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.data_c_values.data_structures"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['MVSRegionType', 'BDNTransformationType', 'NoveltyLevel', 'MVSCoordinate', 'BDNGenealogy', 'ModalInferenceResult', 'CreativeHypothesis', 'NovelProblem']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

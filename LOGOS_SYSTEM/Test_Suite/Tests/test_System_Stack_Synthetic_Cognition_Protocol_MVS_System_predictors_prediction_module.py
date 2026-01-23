# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.predictors.prediction_module"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TrinityPredictionEngine']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

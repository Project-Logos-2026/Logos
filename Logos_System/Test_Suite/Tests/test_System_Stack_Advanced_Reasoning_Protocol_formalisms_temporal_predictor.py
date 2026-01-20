# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.temporal_predictor"
PUBLIC_FUNCTIONS = ['example_temporal_prediction']
PUBLIC_CLASSES = ['TemporalEvent', 'TemporalOperation', 'TemporalPrediction', 'TemporalSequenceModel', 'TemporalPredictor']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

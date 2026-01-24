# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.Temporal_Flow_Analyzer"
PUBLIC_FUNCTIONS = ['get_temporal_analysis']
PUBLIC_CLASSES = ['TemporalEvent', 'TFATIntegration']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

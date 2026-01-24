# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.Reasoning_Engines.Bayesian_Engine.bayesian_inference"
PUBLIC_FUNCTIONS = ['update_posteriors', 'example_unified_inference', 'TrueP', 'FalseP', 'UncertainP']
PUBLIC_CLASSES = ['TrinityVector', 'IELEpistemicState', 'UnifiedBayesianInferencer', 'ProbabilisticResult', 'TrueP', 'BayesianInterface', 'ProbabilisticResult', 'BayesianNetwork', 'BayesianTrinityInferencer', 'BayesianNexus']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

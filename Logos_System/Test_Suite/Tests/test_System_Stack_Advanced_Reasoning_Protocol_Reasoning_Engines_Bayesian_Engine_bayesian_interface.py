# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.Reasoning_Engines.Bayesian_Engine.bayesian_interface"
PUBLIC_FUNCTIONS = ['TrueP', 'FalseP', 'UncertainP']
PUBLIC_CLASSES = ['ProbabilisticResult', 'TrueP', 'BayesianInterface', 'ProbabilisticResult', 'BayesianNetwork']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

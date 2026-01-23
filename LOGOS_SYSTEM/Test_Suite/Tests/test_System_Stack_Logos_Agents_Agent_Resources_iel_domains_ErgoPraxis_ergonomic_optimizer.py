# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Agent_Resources.iel_domains.ErgoPraxis.ergonomic_optimizer"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['OptimizationGoal', 'ErgonomicConstraint', 'OptimizationVariable', 'ErgonomicOptimizer']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

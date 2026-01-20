# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Agent_Resources.iel_domains.ChronoPraxis.chronopraxis.temporal_logic"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TemporalLogic']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

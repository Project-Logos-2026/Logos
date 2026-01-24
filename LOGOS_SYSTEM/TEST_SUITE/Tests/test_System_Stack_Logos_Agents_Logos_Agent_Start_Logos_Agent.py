# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.Start_Logos_Agent"
PUBLIC_FUNCTIONS = ['start_logos_agent']
PUBLIC_CLASSES = ['LogosAgentStartupHalt']
ENTRY_POINTS = ['start_logos_agent']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

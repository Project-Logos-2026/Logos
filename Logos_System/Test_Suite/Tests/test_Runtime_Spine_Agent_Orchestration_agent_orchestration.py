# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.Runtime_Spine.Agent_Orchestration.agent_orchestration"
PUBLIC_FUNCTIONS = ['prepare_agent_orchestration']
PUBLIC_CLASSES = ['OrchestrationHalt']
ENTRY_POINTS = ['prepare_agent_orchestration']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

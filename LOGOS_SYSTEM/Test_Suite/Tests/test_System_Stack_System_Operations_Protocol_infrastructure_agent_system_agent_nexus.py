# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.infrastructure.agent_system.agent_nexus"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['PlanningType', 'GapType', 'LinguisticOperation', 'PlanningRequest', 'GapDetectionRequest', 'LinguisticRequest', 'LOGOSAgentNexus']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

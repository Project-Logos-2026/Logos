# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I2_Agent.protocol_operations.smp"
PUBLIC_FUNCTIONS = ['build_smp']
PUBLIC_CLASSES = ['TriageVector', 'StructuredMeaningPacket']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

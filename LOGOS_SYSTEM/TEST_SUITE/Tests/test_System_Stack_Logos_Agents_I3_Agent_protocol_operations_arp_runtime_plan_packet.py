# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I3_Agent.protocol_operations.arp_runtime.plan_packet"
PUBLIC_FUNCTIONS = ['emit_plan_packet']
PUBLIC_CLASSES = ['PlanPacket']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

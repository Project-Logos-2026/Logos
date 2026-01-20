# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I3_Agent.protocol_operations.arp_cycle.policy"
PUBLIC_FUNCTIONS = ['decide_policy']
PUBLIC_CLASSES = ['ARPPolicyDecision']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Agent_Integration.dispatch"
PUBLIC_FUNCTIONS = ['dispatch_to_scp', 'dispatch_to_arp']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

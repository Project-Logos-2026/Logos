# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.core_processing.registry"
PUBLIC_FUNCTIONS = ['register_uip_handler']
PUBLIC_CLASSES = ['UIPStep', 'UIPStatus', 'UIPContext', 'StepHandler', 'UIPRegistry']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

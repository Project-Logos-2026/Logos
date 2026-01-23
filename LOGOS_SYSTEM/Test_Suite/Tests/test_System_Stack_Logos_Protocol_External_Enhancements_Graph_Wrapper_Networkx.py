# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.External_Enhancements.Graph_Wrapper_Networkx"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['Graph_Wrapper_Networkx']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

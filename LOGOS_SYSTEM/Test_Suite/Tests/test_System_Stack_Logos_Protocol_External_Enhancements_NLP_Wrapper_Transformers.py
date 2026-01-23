# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.External_Enhancements.NLP_Wrapper_Transformers"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['NLP_Wrapper_Transformers']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

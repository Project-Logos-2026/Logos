# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.Receiver_Nexus.LLM_Interface.reasoning_agent"
PUBLIC_FUNCTIONS = ['load_env', 'main']
PUBLIC_CLASSES = ['ReasoningAgent']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

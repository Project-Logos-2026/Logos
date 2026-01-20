# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.Receiver_Nexus.LLM_Interface.plugins.llm_backend"
PUBLIC_FUNCTIONS = ['create_tool_definitions']
PUBLIC_CLASSES = ['LLMConfig', 'LLMBackend']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

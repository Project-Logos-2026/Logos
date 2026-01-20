# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.Receiver_Nexus.LLM_Interface.plugins.enhanced_uip_integration_plugin"
PUBLIC_FUNCTIONS = ['available', 'readiness_reason', 'readiness_diagnostics', 'get_connector_factory', 'get_enhanced_uip_integration_plugin', 'initialize_enhanced_uip_integration']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

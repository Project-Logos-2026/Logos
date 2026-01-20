# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.Receiver_Nexus.LLM_Interface.plugins._uip_connector_stubs"
PUBLIC_FUNCTIONS = ['build_standard_connector', 'build_enhanced_connector']
PUBLIC_CLASSES = ['ConnectorValidationError', 'ConnectorMetadata', 'ConnectorResponse', 'StaticUIPConnector', 'StaticEnhancedUIPConnector']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

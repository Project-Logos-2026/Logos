# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.BDN_System.integration.logos_bridge"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['IntegrationMetrics', 'IntegrationException', 'LegacyCompatibilityLayer', 'MVSBDNBridge']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

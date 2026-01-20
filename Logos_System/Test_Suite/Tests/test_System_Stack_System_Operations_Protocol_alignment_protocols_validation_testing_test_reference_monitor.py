# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.alignment_protocols.validation.testing.test_reference_monitor"
PUBLIC_FUNCTIONS = ['run_safety_tests']
PUBLIC_CLASSES = ['TestConsistencyValidator', 'TestAnomalyDetector', 'TestEnhancedReferenceMonitor', 'TestAnomalyInjection', 'TestIntegrationWithEntry', 'TestThreadSafety']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.alignment_protocols.safety.integrity_framework.integrity_safeguard"
PUBLIC_FUNCTIONS = ['get_global_safety_system', 'set_global_safety_system', 'check_operation_safety', 'emergency_halt']
PUBLIC_CLASSES = ['SafeguardState', 'ViolationContext', 'SafeguardConfiguration', 'IntegrityValidator', 'ParadoxDetector', 'BoundaryEnforcer', 'CrashDumpGenerator', 'SafeguardStateMachine']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

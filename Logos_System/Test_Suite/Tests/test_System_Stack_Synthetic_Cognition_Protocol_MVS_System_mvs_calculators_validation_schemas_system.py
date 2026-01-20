# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.mvs_calculators.validation_schemas_system"
PUBLIC_FUNCTIONS = ['validate_request', 'get_schemas_status', 'test_schemas_implementation']
PUBLIC_CLASSES = ['ValidationType', 'ValidationResult', 'TrinityInvariants', 'ETGCValidationSchema', 'MESHValidationSchema', 'CommutationValidationSchema', 'TLMTokenSchema', 'LOGOSValidationOrchestrator']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

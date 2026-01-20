# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.World_Modeling.world_model"
PUBLIC_FUNCTIONS = ['canonical_json', 'sha256_bytes', 'atomic_write_json', 'load_snapshot', 'validate_snapshot', 'build_snapshot', 'write_snapshot', 'update_world_model']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

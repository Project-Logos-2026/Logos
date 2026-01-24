# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.Runtime_Spine.Lock_And_Key.lock_and_key"
PUBLIC_FUNCTIONS = ['execute_lock_and_key']
PUBLIC_CLASSES = ['LockAndKeyFailure']
ENTRY_POINTS = ['execute_lock_and_key']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.infrastructure.agent_system.shared_resources"
PUBLIC_FUNCTIONS = ['configure_runtime_state_dir', 'runtime_log_path', 'stream_snapshots']
PUBLIC_CLASSES = ['ResourceSpec', 'ResourceSnapshot', 'ResourceLease', 'ResourceManager']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

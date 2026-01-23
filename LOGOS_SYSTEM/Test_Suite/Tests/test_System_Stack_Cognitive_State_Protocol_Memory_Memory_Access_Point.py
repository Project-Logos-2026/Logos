# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.Memory.Memory_Access_Point"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['StorageTier', 'StorageFormat', 'StorageConfiguration', 'TieredMemoryStorage', 'MemoryIndexSystem', 'MemoryRetrievalEngine', 'MemoryConsolidationScheduler', 'MemoryForgettingManager', 'MetamemorySystem', 'CompleteMemorySystem']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.Memory.Logos_Memory_Nexus"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['MemoryConsolidationStage', 'MemoryRecallType', 'MemoryTrace', 'MemoryConsolidator', 'MemoryRecallSystem', 'AbstractionEngine', 'MemoryApplicationSystem', 'LivingMemorySystem']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

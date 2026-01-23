# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.Memory.Memory_State_Persistence"
PUBLIC_FUNCTIONS = ['create_replay_infrastructure', 'quick_replay_analysis']
PUBLIC_CLASSES = ['ReplayEventType', 'ReplayGranularity', 'ReplayEvent', 'DeterministicReplayLogger', 'DeterministicReplayEngine', 'UWMRebuilder', 'SMPRebuilder', 'MemoryRebuilder', 'ForensicAnalyzer', 'ReplayValidator', 'CompleteReplayInfrastructure']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

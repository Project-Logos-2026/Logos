# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.safety_formalisms"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['ObjectiveGoodnessValidator', 'EvilPrivationHandler', 'MoralSetValidator', 'ObjectiveTruthValidator', 'FalsehoodPrivationHandler', 'TruthSetValidator', 'InfinityBoundaryEnforcer', 'EternityTemporalEnforcer', 'BoundarySetValidator', 'ObjectiveBeingValidator', 'NothingPrivationHandler', 'ExistenceSetValidator', 'ResurrectionProofValidator', 'HypostaticUnionValidator', 'RelationalSetValidator', 'UnifiedFormalismValidator']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

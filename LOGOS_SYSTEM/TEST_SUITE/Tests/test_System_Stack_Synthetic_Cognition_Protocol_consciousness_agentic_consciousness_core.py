# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.consciousness.agentic_consciousness_core"
PUBLIC_FUNCTIONS = ['bayesian_self_model', 'hypothesis_self_test', 'causal_self_discovery', 'causal_intervention_analysis', 'modal_self_reasoning', 'consistency_self_check', 'semantic_experience_clustering', 'semantic_similarity_self_analysis', 'symbolic_self_representation', 'lambda_self_evaluation', 'integrated_consciousness_state']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.System_Operations_Protocol.alignment_protocols.validation.examples.demo_integrated_ml"
PUBLIC_FUNCTIONS = ['demo_ml_integration', 'demo_nlp_embeddings', 'demo_graph_reasoning', 'demo_kalman_filtering', 'demo_pytorch_tensors', 'demo_integrated_system', 'main']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

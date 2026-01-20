# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.BDN_System.mvf_node_operator"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TrinityDimension', 'FractalPosition', 'OntologicalNode', 'KDNode', 'KDTree', 'FractalKnowledgeDatabase']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

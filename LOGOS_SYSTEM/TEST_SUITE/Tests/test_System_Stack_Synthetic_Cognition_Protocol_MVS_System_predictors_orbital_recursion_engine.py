# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.predictors.orbital_recursion_engine"
PUBLIC_FUNCTIONS = ['extract_factor', 'map_query_to_ontology', 'extract_factor', 'map_query_to_ontology']
PUBLIC_CLASSES = ['OntologicalSpace', 'OntologicalSpace']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

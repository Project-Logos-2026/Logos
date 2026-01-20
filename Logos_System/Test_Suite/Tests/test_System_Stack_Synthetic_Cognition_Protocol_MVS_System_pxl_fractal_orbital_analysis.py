# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.pxl_fractal_orbital_analysis"
PUBLIC_FUNCTIONS = ['analyze_logos_agent_ontology', 'create_orbital_visualization', 'main']
PUBLIC_CLASSES = ['ModalOperator', 'OntologicalRider', 'OntologicalPrimitive', 'DualBijectiveSystem', 'PrivativeBoundaryEnforcer', 'ModalNecessityOverlay', 'OntologicalRiderEnforcer', 'PXLLogicStack']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

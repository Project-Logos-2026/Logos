# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.pxl_modal_fractal_boundary_analysis"
PUBLIC_FUNCTIONS = ['analyze_privative_modal_boundaries', 'interpret_privative_boundaries', 'assess_ontological_coherence', 'main']
PUBLIC_CLASSES = ['ModalOperator', 'OntologicalRider', 'ModalFractalPoint', 'OntologicalPrimitive', 'PrivativeBoundaryFractal']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

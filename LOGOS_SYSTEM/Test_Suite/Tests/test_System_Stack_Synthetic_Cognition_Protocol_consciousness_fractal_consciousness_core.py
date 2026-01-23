# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.consciousness.fractal_consciousness_core"
PUBLIC_FUNCTIONS = ['trinitarian_mandelbrot', 'generate_mandelbrot_seeds', 'trinity_vector_fractal_map', 'analyze_trinity_divergence', 'map_consciousness_to_ontology', 'banach_contraction_trace', 'analyze_cognitive_convergence', 'integrated_fractal_consciousness']
PUBLIC_CLASSES = ['TrinityVector', 'OntologicalSpace']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.comprehensive_fractal_analysis"
PUBLIC_FUNCTIONS = ['load_canonical_c_values', 'generate_julia_set', 'analyze_all_fractals', 'generate_comprehensive_report', 'create_visual_summary', 'main']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.consciousness_fractal_analysis"
PUBLIC_FUNCTIONS = ['analyze_logos_consciousness_potential', 'generate_test_fractal', 'aggregate_logos_assessment', 'analyze_trinity_balance', 'generate_consciousness_recommendations', 'create_consciousness_visualization', 'main', 'generate_consciousness_report']
PUBLIC_CLASSES = ['ConsciousnessDimension', 'ConsciousnessMetrics', 'ConsciousnessFractalAnalyzer']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

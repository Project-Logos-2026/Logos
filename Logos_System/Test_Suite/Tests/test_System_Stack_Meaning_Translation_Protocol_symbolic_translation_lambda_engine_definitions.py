# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.symbolic_translation.lambda_engine_definitions"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['LambdaExpression', 'LambdaType', 'TranslationResult', 'FractalPosition', 'ITypeSystem', 'IEvaluator', 'IModalBridge', 'IFractalMapper', 'ITranslationBridge', 'IPersistenceBridge', 'ILambdaEngine']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.language_modules.semantic_transformers"
PUBLIC_FUNCTIONS = ['encode_semantics', 'detect_concept_drift', 'example_semantic_transformation']
PUBLIC_CLASSES = ['SemanticEmbedding', 'SemanticTransformation', 'UnifiedSemanticTransformer']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.core_processing.language_processor"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['TrinityVector', 'LogosExpr', 'LambdaEngine', 'OntologicalType', 'IntentCategory', 'EntityType', 'SemanticRelation', 'NamedEntity', 'SemanticTriple', 'IntentClassification', 'SemanticParse', 'NLPProcessingResult', 'TranslationResult', 'LanguageProcessor']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

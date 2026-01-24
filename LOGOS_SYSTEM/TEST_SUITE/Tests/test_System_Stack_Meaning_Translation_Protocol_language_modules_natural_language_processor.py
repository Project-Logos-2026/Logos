# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Meaning_Translation_Protocol.language_modules.natural_language_processor"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['ConversationContext', 'LogicTranslator', 'CoqTranslator', 'NaturalLanguageProcessor']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

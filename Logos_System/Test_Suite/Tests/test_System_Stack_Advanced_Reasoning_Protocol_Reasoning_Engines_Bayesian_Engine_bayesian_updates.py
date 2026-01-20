# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.Reasoning_Engines.Bayesian_Engine.bayesian_updates"
PUBLIC_FUNCTIONS = ['resolve_priors_path', 'load_priors', 'load_static_priors', 'save_priors', 'score_data_point', 'assign_confidence', 'filter_and_score', 'predictive_refinement', 'run_BERT_pipeline', 'query_intent_analyzer', 'preprocess_query', 'run_HBN_analysis', 'execute_HBN']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.Reasoning_Engines.Bayesian_Engine.bayes_update_real_time"
PUBLIC_FUNCTIONS = ['resolve_priors_path', 'load_priors', 'save_priors', 'score_data_point', 'assign_confidence', 'filter_and_score', 'predictive_refinement', 'run_BERT_pipeline']
PUBLIC_CLASSES = []
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

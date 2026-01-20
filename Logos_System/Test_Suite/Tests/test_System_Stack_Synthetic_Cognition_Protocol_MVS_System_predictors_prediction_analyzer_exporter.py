# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.predictors.prediction_analyzer_exporter"
PUBLIC_FUNCTIONS = ['load_predictions', 'summarize', 'plot_coherence', 'filter_predictions', 'export_predictions', 'run_ols', 'run_logit', 'run_partial']
PUBLIC_CLASSES = ['FractalKnowledgeStore']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

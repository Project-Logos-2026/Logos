# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_System_Stack_Synthetic_Cognition_Protocol_MVS_System_predictors_prediction_analyzer_exporter
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Synthetic_Cognition_Protocol_MVS_System_predictors_prediction_analyzer_exporter.py.
agent_binding: None
protocol_binding: Synthetic_Cognition_Protocol
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Synthetic_Cognition_Protocol_MVS_System_predictors_prediction_analyzer_exporter.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Synthetic_Cognition_Protocol.MVS_System.predictors.prediction_analyzer_exporter"
PUBLIC_FUNCTIONS = ['load_predictions', 'summarize', 'plot_coherence', 'filter_predictions', 'export_predictions', 'run_ols', 'run_logit', 'run_partial']
PUBLIC_CLASSES = ['FractalKnowledgeStore']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

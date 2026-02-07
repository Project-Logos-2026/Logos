# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
"""
LOGOS_MODULE_METADATA
---------------------
module_name: test_System_Stack_Advanced_Reasoning_Protocol_formalisms_pxl_schema
runtime_layer: inferred
role: Test module
responsibility: Defines runtime tests for LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Advanced_Reasoning_Protocol_formalisms_pxl_schema.py.
agent_binding: None
protocol_binding: Advanced_Reasoning_Protocol
runtime_classification: test_module
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: LOGOS_SYSTEM/TEST_SUITE/Tests/test_System_Stack_Advanced_Reasoning_Protocol_formalisms_pxl_schema.py
  rewrite_phase: Header_Injection
  rewrite_timestamp: 2026-02-07T00:00:00Z
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema"
PUBLIC_FUNCTIONS = ['validate_trinity_vector', 'create_default_analysis_config', 'merge_validation_results', 'relation_to_json', 'relation_from_json']
PUBLIC_CLASSES = ['PXLRelationType', 'PXLConsistencyLevel', 'PXLAnalysisScope', 'TrinityDimension', 'ModalOperator', 'ValidationSeverity', 'PXLValidatable', 'PXLAnalyzable', 'TrinityVectorizable', 'ModalAnalyzable', 'TrinityVector', 'ModalProperties', 'ValidationIssue', 'ValidationResult', 'PXLRelationModel', 'PXLRelation', 'ConsistencyViolation', 'ConsistencyReport', 'PXLAnalysisConfig', 'PXLAnalysisResult', 'PXLRelationMapper', 'PXLConsistencyChecker', 'PXLPostprocessor', 'PXLSchemaValidator']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

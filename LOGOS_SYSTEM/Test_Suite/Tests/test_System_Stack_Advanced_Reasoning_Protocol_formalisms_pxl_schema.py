# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.formalisms.pxl_schema"
PUBLIC_FUNCTIONS = ['validate_trinity_vector', 'create_default_analysis_config', 'merge_validation_results', 'relation_to_json', 'relation_from_json']
PUBLIC_CLASSES = ['PXLRelationType', 'PXLConsistencyLevel', 'PXLAnalysisScope', 'TrinityDimension', 'ModalOperator', 'ValidationSeverity', 'PXLValidatable', 'PXLAnalyzable', 'TrinityVectorizable', 'ModalAnalyzable', 'TrinityVector', 'ModalProperties', 'ValidationIssue', 'ValidationResult', 'PXLRelationModel', 'PXLRelation', 'ConsistencyViolation', 'ConsistencyReport', 'PXLAnalysisConfig', 'PXLAnalysisResult', 'PXLRelationMapper', 'PXLConsistencyChecker', 'PXLPostprocessor', 'PXLSchemaValidator']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

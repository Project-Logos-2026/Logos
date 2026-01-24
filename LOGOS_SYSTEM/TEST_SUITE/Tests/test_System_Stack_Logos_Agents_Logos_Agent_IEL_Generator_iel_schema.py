# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.IEL_Generator.iel_schema"
PUBLIC_FUNCTIONS = ['create_iel_processing_context', 'validate_iel_knowledge', 'merge_iel_validation_results', 'create_iel_health_check', 'serialize_iel_result', 'deserialize_iel_result']
PUBLIC_CLASSES = ['IELProcessingPhase', 'IELDataType', 'IELIntegrationLevel', 'IELValidationLevel', 'IELValidatable', 'IELProcessable', 'IELSynthesizable', 'IELRecoverable', 'IELConfigurable', 'IELMonitorable', 'IELValidationIssue', 'IELValidationResult', 'IELProcessingContext', 'IELComponentStatus', 'IELHealthCheck', 'IELKnowledgeModel', 'IELSynthesisConfigModel', 'IELErrorModel', 'IELDomainSynthesizer', 'IELErrorHandler', 'IELModalAnalyzer', 'IELTrinityProcessor', 'IELOntologyIntegrator', 'IELFrameworkComponent', 'IELIntegratedSystem', 'IELSynthesisResult', 'IELErrorHandlingResult', 'IELPipelineResult', 'IELSchemaValidator']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

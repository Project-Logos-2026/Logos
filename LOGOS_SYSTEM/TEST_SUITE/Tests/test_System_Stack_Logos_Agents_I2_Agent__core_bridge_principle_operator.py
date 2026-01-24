# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.I2_Agent._core.bridge_principle_operator"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['Origin', 'Channel', 'IntentClass', 'EntityType', 'Polarity', 'Modality', 'RelationType', 'DomainHint', 'PrivationDomain', 'PrivationAction', 'RiskLevel', 'TraceStage', 'TraceActor', 'Source', 'Entity', 'Proposition', 'Relation', 'Ontology', 'Payload', 'PrivationMetadata', 'Risk', 'Security', 'TraceEntry', 'UIPArtifacts', 'Provenance', 'Enrichment', 'Routing', 'StructuredMeaningPacket', 'OntologyMapper', 'IntentClassifier', 'ModalityExtractor', 'PrivationDetector', 'DomainClassifier', 'SMPBuilder']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

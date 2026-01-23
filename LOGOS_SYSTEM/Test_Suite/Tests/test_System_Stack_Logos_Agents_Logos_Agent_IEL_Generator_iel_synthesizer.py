# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Agents.Logos_Agent.IEL_Generator.iel_synthesizer"
PUBLIC_FUNCTIONS = []
PUBLIC_CLASSES = ['DomainType', 'SynthesisStrategy', 'KnowledgeLevel', 'SynthesisQuality', 'DomainKnowledge', 'SynthesisResult', 'ModalKnowledgeAnalyzer', 'OntologicalIntegrator', 'DualBijectiveSynthesisEngine', 'IELDomainSynthesizer']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

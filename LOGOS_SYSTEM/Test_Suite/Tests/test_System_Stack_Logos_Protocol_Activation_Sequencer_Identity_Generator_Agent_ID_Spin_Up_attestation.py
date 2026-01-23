# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Logos_Protocol.Activation_Sequencer.Identity_Generator.Agent_ID_Spin_Up.attestation"
PUBLIC_FUNCTIONS = ['validate_attestation', 'load_alignment_attestation', 'compute_attestation_hash', 'validate_mission_profile', 'load_mission_profile']
PUBLIC_CLASSES = ['AlignmentGateError']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

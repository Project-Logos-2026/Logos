# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Entry_Point.Agent_Orchestration.Lem_Discharge"
PUBLIC_FUNCTIONS = ['discharge_lem']
PUBLIC_CLASSES = ['LemDischargeHalt']
ENTRY_POINTS = ['discharge_lem']

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

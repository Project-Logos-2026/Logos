# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Cognitive_State_Protocol.World_Modeling.commitment_ledger"
PUBLIC_FUNCTIONS = ['canonical_json', 'sha256_bytes', 'compute_ledger_hash', 'atomic_write_json', 'load_or_create_ledger', 'validate_ledger', 'record_event', 'upsert_commitment', 'set_active_commitment', 'mark_commitment_status', 'write_ledger', 'ensure_active_commitment', 'mark_cycle_outcome']
PUBLIC_CLASSES = ['LedgerUpdateResult']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

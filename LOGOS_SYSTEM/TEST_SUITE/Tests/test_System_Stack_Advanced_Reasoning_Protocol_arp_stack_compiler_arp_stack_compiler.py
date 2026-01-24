# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
from Test_Suite.Tests.common import run_module_tests

MODULE_PATH = "Logos_System.System_Stack.Advanced_Reasoning_Protocol.arp_stack_compiler.arp_stack_compiler"
PUBLIC_FUNCTIONS = ['get_arp_compiler_stats']
PUBLIC_CLASSES = ['DataOrigin', 'CompilationResult', 'CompiledDataObject', 'ARPStackCompilation', 'ARPStackCompiler']
ENTRY_POINTS = []

def run_tests():
    return run_module_tests(MODULE_PATH, PUBLIC_FUNCTIONS, PUBLIC_CLASSES, ENTRY_POINTS)

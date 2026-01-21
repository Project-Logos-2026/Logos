
"""
LEGACY PACKAGE SHIM: LOGOS_SYSTEM.System_Stack
Forwards to canonical Logos_System.System_Stack.
"""
import importlib, sys
canonical = importlib.import_module("Logos_System.System_Stack")
sys.modules[__name__] = canonical

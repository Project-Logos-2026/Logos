# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: GOVERNED
# EXECUTION: NONE
# ROLE: PACKAGE_BOUNDARY

"""
Canonical package initializer.

This file establishes import boundaries and package identity
for the LOGOS System Rebuild. It contains no executable logic.
"""

import importlib
import sys

_il = importlib
_sys = sys

# Legacy namespace alias: LOGOS_SYSTEM → Logos_System
sys.modules.setdefault(
	"LOGOS_SYSTEM",
	importlib.import_module(__name__),
)

# Legacy import surfaces for orchestration and governance callers
try:
	_sys.modules.setdefault(
		"System_Operations_Protocol",
		_il.import_module("Logos_System.System_Stack.System_Operations_Protocol"),
	)
except ImportError:
	pass

try:
	_sys.modules.setdefault(
		"Logos_Protocol",
		_il.import_module("Logos_System.System_Stack.Logos_Protocol"),
	)
except ImportError:
	pass

try:
	_sys.modules.setdefault(
		"Logos_System.System_Stack.System_Operations_Protocol.governance.pxl_client",
		_il.import_module(
			"Logos_System.System_Stack.System_Operations_Protocol.governance.pxl_client"
		),
	)
except ImportError:
	pass


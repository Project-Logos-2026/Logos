"""
RUNTIME_TOOL_METADATA
---------------------

tool_name: test_import_base_reasoning_registry.py
tool_category: Dev_Utilities
tool_subcategory: unspecified

purpose:
Auto-generated placeholder. Tool function description should be updated manually.

authoritative_scope:
LOGOS_SYSTEM

mutation_capability: false
destructive_capability: false
requires_repo_context: true

cli_entrypoint:
python test_import_base_reasoning_registry.py

output_artifacts:
none

dependencies:
standard_library

safety_classification:
READ_ONLY
"""

import traceback
try:
    from logos.imports.protocols import base_reasoning_registry
from pathlib import Path

OUTPUT_ROOT = Path("/workspaces/Logos/_Dev_Resources/Reports/Tool_Outputs/Runtime")
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def write_report(name: str, data) -> None:
    path = OUTPUT_ROOT / name
    with open(path, "w", encoding="utf-8") as f:
        import json as _json
        _json.dump(data, f, indent=2)
    print(f"  Report written: {path}")

    print("Imported base_reasoning_registry OK")
except Exception as e:
    print("Import failed:")
    traceback.print_exc()

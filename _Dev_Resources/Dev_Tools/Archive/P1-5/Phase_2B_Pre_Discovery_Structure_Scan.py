# PHASE_2B_PRE_DISCOVERY_STRUCTURE_SCAN
# Branch: pre-import-repair-stabilization
# Mode: READ-ONLY
# DRAC EXCLUDED
#
# Purpose:
#   Discover actual on-disk namespace locations before Phase 2B relocation.
#   No files are mutated.

import os
import json
from pathlib import Path

ROOT = Path(".").resolve()

TARGET_DIRS = [
    "Activation_Sequencer",
    "External_Enhancements",
    "System_Stack",
    "LOGOS_AGI",
    "Advanced_Reasoning_Protocol",
    "Synthetic_Cognition_Protocol",
    "Multi_Process_Signal_Compiler",
    "System_Operations_Protocol"
]

results = {name: [] for name in TARGET_DIRS}

for root, dirs, files in os.walk(ROOT):
    # Exclude DRAC subtree completely
    if "Dynamic_Reconstruction_Adaptive_Compilation_Protocol" in root:
        continue

    for d in dirs:
        if d in TARGET_DIRS:
            full_path = Path(root) / d
            results[d].append(str(full_path.relative_to(ROOT)))

report = {
    "phase": "Phase_2B_Pre_Discovery_Structure_Scan",
    "results": results
}

reports_dir = Path("_Reports")
reports_dir.mkdir(exist_ok=True)

output_path = reports_dir / "Phase_2B_Pre_Discovery_Structure.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Structure scan complete.")
print(f"Results written to: {output_path}")

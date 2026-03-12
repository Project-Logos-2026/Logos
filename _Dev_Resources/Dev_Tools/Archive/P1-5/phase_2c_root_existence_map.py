"""
PHASE_2C_ROOT_EXISTENCE_MAP
Classify all unique Rule_2 root prefixes by verifying whether they physically exist on disk within runtime scope.
READ-ONLY analysis. Do not mutate any source files.
"""
import os
import json
from pathlib import Path

INPUT_PATH = Path("_Reports/Phase_2A_Rule2_Classification.json")
OUTPUT_PATH = Path("_Reports/Phase_2C_Root_Existence_Map.json")
RUNTIME_DIRS = ["STARTUP", "LOGOS_SYSTEM"]
EXCLUDE = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"
BRANCH = "pre-import-repair-stabilization"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

root_dist = data["root_prefix_distribution"]
unique_roots = list(root_dist.keys())

results = []
roots_found = 0
roots_missing = 0

for root in unique_roots:
    found = []
    for base in RUNTIME_DIRS:
        for dirpath, dirs, files in os.walk(base):
            if EXCLUDE in dirpath:
                continue
            for d in dirs:
                if d == root:
                    found.append(str(Path(dirpath) / d))
    exists = bool(found)
    if exists:
        roots_found += 1
    else:
        roots_missing += 1
    results.append({
        "root": root,
        "violation_count": root_dist[root],
        "exists_on_disk": exists,
        "locations": found
    })

artifact = {
    "phase": "Phase_2C_Root_Existence_Map",
    "branch": BRANCH,
    "roots": results,
    "excluded_directory": EXCLUDE
}

OUTPUT_PATH.parent.mkdir(exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(artifact, f, indent=2)

print(f"total_unique_roots: {len(unique_roots)}")
print(f"roots_found: {roots_found}")
print(f"roots_missing: {roots_missing}")
print(f"Artifact written: {OUTPUT_PATH}")

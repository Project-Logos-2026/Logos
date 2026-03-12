"""
PHASE_2E_RULE2_FULL_PREFIX_GROUPING
Group remaining Rule_2 violations by full prefix (first 3 segments).
"""
import json
from pathlib import Path
from collections import defaultdict

INPUT_PATH = Path("_Reports/Import_Linter_Report.json")
OUTPUT_PATH = Path("_Reports/Phase_2E_Rule2_Prefix_Grouping.json")

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

violations = data["violations"]
rule2 = [v for v in violations if v["rule"] == "Rule_2"]

groups = defaultdict(lambda: {"occurrence_count": 0, "files": set()})

for v in rule2:
    import_str = v["import"]
    prefix_3 = ".".join(import_str.split(".")[:3])
    groups[prefix_3]["occurrence_count"] += 1
    groups[prefix_3]["files"].add(v["file"])

prefix_groups = []
for prefix, info in groups.items():
    prefix_groups.append({
        "prefix_3": prefix,
        "occurrence_count": info["occurrence_count"],
        "unique_files": len(info["files"])
    })

artifact = {
    "phase": "Phase_2E_Rule2_Full_Prefix_Grouping",
    "total_rule2_violations": len(rule2),
    "prefix_groups": prefix_groups
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(artifact, f, indent=2)

print(f"Phase 2E grouping complete. Rule_2 violations: {len(rule2)}. Groups: {len(prefix_groups)}.")

import json
from pathlib import Path
from collections import defaultdict

REPORT_PATH = Path("_Reports/Import_Linter_Report.json")

if not REPORT_PATH.exists():
    raise FileNotFoundError("Import_Linter_Report.json not found in _Reports/")

with open(REPORT_PATH, "r", encoding="utf-8") as f:
    report = json.load(f)

violations = report.get("violations", [])

rule2 = [v for v in violations if v.get("rule") == "Rule_2"]

root_groups = defaultdict(list)
module_groups = defaultdict(list)

for entry in rule2:
    module = entry.get("import", "")
    if not module:
        continue

    first_segment = module.split(".")[0]
    root_groups[first_segment].append(entry)
    module_groups[module].append(entry)

root_summary = {
    root: {
        "total_violations": len(entries),
        "unique_modules": len(set(e["import"] for e in entries))
    }
    for root, entries in root_groups.items()
}

module_summary = {
    module: len(entries)
    for module, entries in sorted(
        module_groups.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
}

output = {
    "phase": "Phase_2B_A_Rule2_Root_Grouping",
    "total_rule2_violations": len(rule2),
    "root_summary": root_summary,
    "module_frequency_sorted": module_summary,
}

output_path = Path("_Reports/Phase_2B_Root_Grouping.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("Phase 2B-A grouping complete.")
print("Total Rule_2 violations:", len(rule2))
print("Roots detected:", list(root_summary.keys()))

import json
from pathlib import Path

BASE = Path("/workspaces/Logos/_Governance/Audit_Artifacts")

categorized_path = BASE / "print_call_categorized.json"
refined_path = BASE / "m5_refined_report.json"

if not categorized_path.exists():
    raise FileNotFoundError("print_call_categorized.json not found")

if not refined_path.exists():
    raise FileNotFoundError("m5_refined_report.json not found")

with categorized_path.open() as f:
    categorized = json.load(f)

with refined_path.open() as f:
    refined = json.load(f)

# Extract refined production print set
refined_entries = refined.get("occurrences") or refined.get("prints") or refined.get("production_surface_prints") or refined
refined_set = set(
    (entry["file"], entry.get("line") or entry.get("line_number"))
    for entry in refined_entries
)

# Extract categorized print set
categorized_entries = categorized.get("classified_prints") or categorized.get("prints") or categorized.get("categorized_prints") or categorized.get("occurrences") or categorized
categorized_set = set(
    (entry["file"], entry.get("line") or entry.get("line_number"))
    for entry in categorized_entries
)

# Comparison metrics
missing_from_categorized = refined_set - categorized_set
extra_in_categorized = categorized_set - refined_set

report = {
    "refined_count": len(refined_set),
    "categorized_count": len(categorized_set),
    "aligned": refined_set == categorized_set,
    "missing_from_categorized_count": len(missing_from_categorized),
    "extra_in_categorized_count": len(extra_in_categorized),
    "sample_missing_from_categorized": list(missing_from_categorized)[:10],
    "sample_extra_in_categorized": list(extra_in_categorized)[:10],
}

print("=== PRINT CLASSIFICATION ALIGNMENT REPORT ===")
print(json.dumps(report, indent=2))

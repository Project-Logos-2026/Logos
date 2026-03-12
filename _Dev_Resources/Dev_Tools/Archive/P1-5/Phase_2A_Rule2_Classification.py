import json
import os
from collections import defaultdict

# --- Locate Linter Artifact ---
CANDIDATES = [
    "Import_Linter_Report.json",
    "_Reports/Import_Linter_Report.json",
    "Phase_2A_Post_Mutation_Lint.json",
]

report_path = None
for candidate in CANDIDATES:
    if os.path.exists(candidate):
        report_path = candidate
        break

if not report_path:
    raise FileNotFoundError("No linter JSON artifact found.")

print(f"Using linter artifact: {report_path}")

# --- Load Artifact ---
with open(report_path, "r") as f:
    data = json.load(f)

# --- Extract Rule_2 Violations ---
rule2_entries = []
if "violations" in data:
    for entry in data["violations"]:
        if entry.get("rule") == "Rule_2" or entry.get("rule") == 2:
            rule2_entries.append(entry)

# Some linter formats store rule buckets separately
if not rule2_entries and "Rule_2" in data:
    rule2_entries = data["Rule_2"]

if not rule2_entries:
    print("No Rule_2 violations found.")
    exit(0)

# --- Classification ---
prefix_counts = defaultdict(int)
file_counts = defaultdict(int)
unique_files = set()

for entry in rule2_entries:
    import_string = entry.get("import", "") or entry.get("import_string", "")
    file_path = entry.get("file", "UNKNOWN")

    if not import_string:
        continue

    root = import_string.split(".")[0]
    prefix_counts[root] += 1

    unique_files.add(file_path)
    file_counts[file_path] += 1

# --- Build Output Artifact ---
classification = {
    "source_artifact": report_path,
    "total_rule2_violations": len(rule2_entries),
    "unique_files_affected": len(unique_files),
    "root_prefix_distribution": dict(sorted(prefix_counts.items(), key=lambda x: x[1], reverse=True)),
    "files_with_violation_counts": dict(sorted(file_counts.items(), key=lambda x: x[1], reverse=True)),
}

# --- Ensure Reports Directory ---
os.makedirs("_Reports", exist_ok=True)

output_path = "_Reports/Phase_2A_Rule2_Classification.json"

with open(output_path, "w") as f:
    json.dump(classification, f, indent=2)

print(f"Classification written to: {output_path}")
print("Done.")

import os
import re
import json

ROOT = "."
EXCLUDE_DIR = "Dynamic_Reconstruction_Adaptive_Compilation_Protocol"

pattern_from = re.compile(r'^(\s*from\s+)Logos_System(\.)', re.MULTILINE)
pattern_import = re.compile(r'^(\s*import\s+)Logos_System(\.)', re.MULTILINE)

files_modified = []
rewrites = []

for root, dirs, files in os.walk(ROOT):
    if EXCLUDE_DIR in root:
        continue

    for file in files:
        if not file.endswith(".py"):
            continue

        path = os.path.join(root, file)


        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # Skip non-UTF8 files
            if 'skipped_files' not in locals():
                skipped_files = []
            skipped_files.append(path)
            continue

        new_content = content
        new_content = pattern_from.sub(r'\1LOGOS_SYSTEM\2', new_content)
        new_content = pattern_import.sub(r'\1LOGOS_SYSTEM\2', new_content)

        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

            files_modified.append(path)

            rewrites.append({
                "file": path,
                "change": "Logos_System → LOGOS_SYSTEM (root case normalization)"
            })


report = {
    "phase": "Phase_2A_Corrected",
    "files_modified": files_modified,
    "total_files_modified": len(files_modified),
    "total_rewrites": len(files_modified),
    "skipped_files_due_to_encoding": locals().get('skipped_files', []),
    "excluded_directory": EXCLUDE_DIR
}

os.makedirs("_Reports", exist_ok=True)

with open("_Reports/Phase_2A_Corrected_Mutation_Report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Phase 2A-Corrected complete.")
print("Files modified:", len(files_modified))

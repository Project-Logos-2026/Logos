import os
import json
import re
from collections import Counter, defaultdict


# Load Rule_2 violations from Import_Linter_Report.json
with open('_Reports/Import_Linter_Report.json', 'r') as f:
    report = json.load(f)

# Only keep Rule_2 violations from the 'violations' list
violations = report.get('violations', [])
rule2 = [entry for entry in violations if entry.get('rule') == 'Rule_2']

# Helper: extract literal import prefix (up to 4 segments)
def extract_import_prefix(import_line):
    # Match 'import x.y.z' or 'from x.y.z import ...'
    m = re.match(r'\s*(from|import)\s+([\w\.]+)', import_line)
    if m:
        prefix = m.group(2)
        # Only keep up to 4 segments
        return '.'.join(prefix.split('.')[:4])
    return None

prefix_counter = Counter()
prefix_examples = defaultdict(list)

for entry in rule2:
    file_path = entry['file']
    line_no = entry['line']
    # Defensive: skip DRAC subtree
    if 'DRAC_Core/DRAC_Invariables' in file_path:
        continue
    # Defensive: skip missing files
    if not os.path.exists(file_path):
        continue
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Defensive: line numbers are 1-based
        import_line = lines[line_no-1].strip()
        prefix = extract_import_prefix(import_line)
        if prefix:
            prefix_counter[prefix] += 1
            if len(prefix_examples[prefix]) < 3:
                prefix_examples[prefix].append({'file': file_path, 'line': line_no, 'import_line': import_line})
    except Exception as e:
        continue

# Write output artifact
output = {
    'unique_prefixes': len(prefix_counter),
    'prefix_counts': prefix_counter,
    'prefix_examples': prefix_examples
}

with open('_Reports/Phase_2F_Prefix_String_Verification.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"Wrote _Reports/Phase_2F_Prefix_String_Verification.json with {len(prefix_counter)} unique prefixes.")

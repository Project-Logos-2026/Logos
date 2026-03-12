import json
from pathlib import Path

ROOT = Path(".").resolve()

RUNTIME_DIRS = [
    ROOT / "STARTUP",
    ROOT / "LOGOS_SYSTEM",
    ROOT / "Runtime_Spine",
    ROOT / "RUNTIME_CORES",
]

EXCLUDE_KEYWORDS = [
    "Tests",
    "test_",
    "__pycache__",
    "_Dev_Resources",
    "scripts",
    "migrations",
]

def is_excluded(path: Path) -> bool:
    return any(k in str(path) for k in EXCLUDE_KEYWORDS)

def scan_for_prints():
    results = []
    for base in RUNTIME_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if is_excluded(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, start=1):
                    if "print(" in line:
                        results.append({
                            "file": str(path.relative_to(ROOT)),
                            "line_number": i,
                        })
    return results

# ---- EXECUTION ----

current_inventory = scan_for_prints()

inventory_path = ROOT / "_Governance" / "Audit_Artifacts" / "runtime_print_inventory.json"

if not inventory_path.exists():
    print("ERROR: runtime_print_inventory.json not found.")
    exit(1)

with open(inventory_path, "r", encoding="utf-8") as f:
    data = json.load(f)

previous_inventory = data.get("occurrences", [])

prev_set = {(item["file"], item["line_number"]) for item in previous_inventory}
curr_set = {(item["file"], item["line_number"]) for item in current_inventory}

added = curr_set - prev_set
removed = prev_set - curr_set

print("=== M5.0 VALIDATION REPORT ===")
print(f"Previous count: {len(prev_set)}")
print(f"Current count:  {len(curr_set)}")
print(f"Added:   {len(added)}")
print(f"Removed: {len(removed)}")

if added:
    print("\nNew print locations detected:")
    for file, line in sorted(added):
        print(f"{file}:{line}")

if removed:
    print("\nPreviously recorded prints missing:")
    for file, line in sorted(removed):
        print(f"{file}:{line}")

if not added and not removed:
    print("\nInventory matches HEAD. Safe to proceed to M5 execution.")

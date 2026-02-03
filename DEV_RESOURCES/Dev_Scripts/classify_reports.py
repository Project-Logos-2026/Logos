#!/usr/bin/env python3
"""
Report Classification Ledger Generator

Status: MAINTENANCE-ONLY | NON-CANONICAL
Writes output ONLY to a specified maintenance sink directory.
Performs NO deletions, NO moves, NO edits of source files.
"""

import json
from pathlib import Path

def classify(path: str) -> str:
    name = path.lower()
    if "autonomy" in name or "phase" in name:
        return "REVIEW_HIGH_VALUE"
    if "audit" in name or "normalize" in name:
        return "LIKELY_DUPLICATE"
    if "log" in name or "boot" in name:
        return "EXECUTION_LOG"
    return "UNCLASSIFIED"

def main():
    sink = Path("DEV_RESOURCES/REPO_CLEANOUT").resolve()
    pass_dirs = sorted(p for p in sink.iterdir() if p.is_dir() and p.name.startswith("report_cleanup_pass_"))
    if not pass_dirs:
        raise RuntimeError("No cleanup pass directory found")

    latest = pass_dirs[-1]
    index_path = latest / "report_index.json"
    out_path = latest / "report_classification_ledger.json"

    data = json.loads(index_path.read_text())
    ledger = {}

    for canon, src in data.items():
        ledger[canon] = {
            "source": src,
            "classification": classify(src),
        }

    out_path.write_text(json.dumps(ledger, indent=2))
    print(f"Wrote classification ledger: {out_path}")

if __name__ == "__main__":
    main()

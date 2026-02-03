#!/usr/bin/env python3
"""
Report Collection Tool — Canonical Aggregation Pass

Status: DESIGN-SAFE | NON-DESTRUCTIVE
Scope: Reports only
Location: DEV_RESOURCES/Dev_Scripts

Function:
- Scan repository for report directories/files
- Aggregate them into a single target directory
- Preserve provenance via symlinks or copies
- Emit an index mapping canonical path -> original source(s)

NO deletions.
NO modifications of originals.
Fail-closed on collision.
"""

import argparse
import json
import os
from pathlib import Path

REPORT_MARKERS = ["_Reports", "_reports", "REPORTS", "SYSTEM_AUDIT_LOGS", "test_logs", "proof_logs"]

def is_report_path(path: Path) -> bool:
    return any(marker in path.parts for marker in REPORT_MARKERS)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--emit-index", required=True)
    parser.add_argument("--link-mode", choices=["symlink", "copy"], default="symlink")
    args = parser.parse_args()

    scan_root = Path(args.scan_root).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    index = {}
    seen = set()

    for root, dirs, files in os.walk(scan_root):
        root_path = Path(root)
        if is_report_path(root_path):
            for f in files:
                src = root_path / f
                rel = src.relative_to(scan_root)
                dest = output_root / rel

                if dest in seen:
                    raise RuntimeError(f"Collision detected: {dest}")

                dest.parent.mkdir(parents=True, exist_ok=True)

                if args.link_mode == "symlink":
                    os.symlink(src, dest)
                else:
                    dest.write_bytes(src.read_bytes())

                index[str(dest)] = str(src)
                seen.add(dest)

    Path(args.emit_index).write_text(json.dumps(index, indent=2))
    print(f"Report aggregation complete. Index written to {args.emit_index}")

if __name__ == "__main__":
    main()

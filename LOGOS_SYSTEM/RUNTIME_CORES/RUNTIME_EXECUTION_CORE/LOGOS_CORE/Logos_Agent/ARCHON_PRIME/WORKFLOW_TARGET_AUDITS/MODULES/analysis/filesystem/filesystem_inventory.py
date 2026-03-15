#!/usr/bin/env python3
"""
ARCHON PRIME — Filesystem Inventory
====================================
Walks the target directory and produces a complete file inventory:
  - file paths, sizes, extensions, modification times
  - directory counts and totals by extension
Writes: filesystem_inventory.json
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache", ".pytest_cache"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon filesystem inventory scanner")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."),
                   help="Target repository path")
    p.add_argument("--output", default=str(OUTPUT_ROOT),
                   help="Output directory (overrides ARCHON_OUTPUT_ROOT)")
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def run(target: Path, out_dir: Path) -> None:
    print(f"[filesystem_inventory] Scanning: {target}")
    files = []
    ext_counts: dict[str, int] = {}
    total_bytes = 0

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fname in sorted(fnames):
            fp = Path(root) / fname
            try:
                st = fp.stat()
                rel = str(fp.relative_to(target))
                ext = fp.suffix.lower() or "(none)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
                total_bytes += st.st_size
                files.append({
                    "path": rel,
                    "extension": ext,
                    "size_bytes": st.st_size,
                    "modified": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
                })
            except OSError:
                continue

    write_json(out_dir, "filesystem_inventory.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_files": len(files),
        "total_bytes": total_bytes,
        "extension_counts": dict(sorted(ext_counts.items(), key=lambda x: -x[1])),
        "files": files,
    })
    print(f"  Files scanned: {len(files)}  Total: {total_bytes:,} bytes")


def main() -> None:
    args = parse_args()
    target = Path(args.target).resolve()
    out_dir = Path(args.output)
    if not target.exists():
        print(f"[FATAL] Target not found: {target}", file=sys.stderr)
        sys.exit(1)
    run(target, out_dir)


if __name__ == "__main__":
    main()

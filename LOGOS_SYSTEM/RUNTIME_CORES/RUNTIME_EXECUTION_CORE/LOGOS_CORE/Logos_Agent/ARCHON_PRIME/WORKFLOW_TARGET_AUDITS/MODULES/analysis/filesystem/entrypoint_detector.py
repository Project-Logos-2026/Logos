#!/usr/bin/env python3
"""
ARCHON PRIME — Entrypoint Detector
=====================================
Identifies all executable entry points in the target repository:
  - Python __main__.py and if __name__ == "__main__" blocks
  - setup.py / pyproject.toml console_scripts
  - CLI scripts and Dockerfile CMD/ENTRYPOINT
  - Makefile targets
Writes: entrypoint_report.json
"""
import argparse
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTPUT_ROOT = "_Dev_Resources/Reports/ARCHON_DIAGNOSTICS"
OUTPUT_ROOT = Path(os.environ.get("ARCHON_OUTPUT_ROOT", DEFAULT_OUTPUT_ROOT))
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
RUN_TS = datetime.now(timezone.utc).isoformat()

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon entrypoint detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def has_main_block(path: Path) -> bool:
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                test = node.test
                if isinstance(test, ast.Compare):
                    if (isinstance(test.left, ast.Name) and test.left.id == "__name__"
                            and len(test.comparators) == 1
                            and isinstance(test.comparators[0], ast.Constant)
                            and test.comparators[0].value == "__main__"):
                        return True
    except Exception:
        pass
    return False


def scan_pyproject(path: Path) -> list[dict]:
    entries = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        # Naive TOML scan for console_scripts
        in_scripts = False
        for line in content.splitlines():
            stripped = line.strip()
            if "[project.scripts]" in stripped or "[tool.poetry.scripts]" in stripped:
                in_scripts = True
                continue
            if in_scripts:
                if stripped.startswith("["):
                    in_scripts = False
                    continue
                if "=" in stripped:
                    name, _, target = stripped.partition("=")
                    entries.append({"type": "console_script",
                                    "name": name.strip(),
                                    "target": target.strip().strip('"\'')})
    except Exception:
        pass
    return entries


def run(target: Path, out_dir: Path) -> None:
    print(f"[entrypoint_detector] Scanning: {target}")
    entrypoints: list[dict] = []

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        rel_root = Path(root).relative_to(target)

        for fname in sorted(fnames):
            fp = Path(root) / fname
            rel = str(rel_root / fname)

            if fname == "__main__.py":
                entrypoints.append({"type": "python_main_module", "path": rel,
                                    "description": "Python package __main__.py"})
            elif fname.endswith(".py") and has_main_block(fp):
                entrypoints.append({"type": "python_main_block", "path": rel,
                                    "description": "if __name__ == '__main__' block"})
            elif fname == "setup.py":
                entrypoints.append({"type": "setup_py", "path": rel,
                                    "description": "setuptools entry point"})
            elif fname == "pyproject.toml":
                scripts = scan_pyproject(fp)
                for s in scripts:
                    s["path"] = rel
                    entrypoints.append(s)
            elif fname.lower() in ("dockerfile", "dockerfile.prod", "dockerfile.dev"):
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    for line in content.splitlines():
                        if re.match(r"^\s*(CMD|ENTRYPOINT)\s", line):
                            entrypoints.append({"type": "docker_entrypoint",
                                                "path": rel, "directive": line.strip()})
                except Exception:
                    pass
            elif fname == "Makefile":
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    targets = re.findall(r"^([a-zA-Z0-9_-]+)\s*:", content, re.MULTILINE)
                    if targets:
                        entrypoints.append({"type": "makefile_targets",
                                            "path": rel, "targets": targets[:20]})
                except Exception:
                    pass

    write_json(out_dir, "entrypoint_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_entrypoints": len(entrypoints),
        "entrypoints": entrypoints,
    })
    print(f"  Entrypoints found: {len(entrypoints)}")


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

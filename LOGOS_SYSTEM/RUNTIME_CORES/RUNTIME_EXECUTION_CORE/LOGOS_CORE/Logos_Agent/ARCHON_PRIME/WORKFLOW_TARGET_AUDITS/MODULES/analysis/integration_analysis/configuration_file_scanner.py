#!/usr/bin/env python3
"""
ARCHON PRIME — Configuration File Scanner
==========================================
Scans the target repository for configuration files in common formats:
YAML, TOML, JSON, INI/CFG, dotenv, and Docker/CI configurations.
Builds a structured inventory of all configuration surfaces.
Writes: configuration_files.json
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

CONFIG_PROFILES: dict[str, dict] = {
    "yaml":       {"extensions": {".yaml", ".yml"},    "format": "YAML",   "category": "application"},
    "toml":       {"extensions": {".toml"},             "format": "TOML",   "category": "application"},
    "json_conf":  {"extensions": {".json"},             "format": "JSON",   "category": "application"},
    "ini_cfg":    {"extensions": {".ini", ".cfg"},      "format": "INI",    "category": "application"},
    "env":        {"extensions": {".env"},              "format": "dotenv", "category": "environment"},
    "dockerfile": {"names": {"Dockerfile", "dockerfile"}, "format": "Docker", "category": "deployment"},
    "makefile":   {"names": {"Makefile", "makefile"},     "format": "Make",   "category": "build"},
    "pyproject":  {"names": {"pyproject.toml"},           "format": "TOML",   "category": "python"},
    "setup_cfg":  {"names": {"setup.cfg"},                "format": "INI",    "category": "python"},
    "setup_py":   {"names": {"setup.py"},                 "format": "Python", "category": "python"},
    "requirements": {"names_prefix": "requirements",      "format": "pip",    "category": "python"},
    "ci":         {"dir_names": {".github", ".circleci", ".gitlab"},
                   "extensions": {".yml", ".yaml"},      "format": "YAML",   "category": "ci"},
}

# Well-known config file names
KNOWN_CONFIG_NAMES = {
    "pytest.ini", "tox.ini", ".flake8", ".mypy.ini", "mypy.ini", ".isort.cfg",
    ".coveragerc", "codecov.yml", "codecov.yaml", ".pre-commit-config.yaml",
    "docker-compose.yml", "docker-compose.yaml", ".dockerignore", ".gitignore",
    ".env", ".env.example", ".env.sample", "pyrightconfig.json", ".pylintrc",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon configuration file scanner")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def categorize_file(path: Path) -> dict | None:
    name = path.name
    ext = path.suffix.lower()
    rel_parts = [p.lower() for p in path.parts]

    # Well-known names
    if name in KNOWN_CONFIG_NAMES:
        return {"format": "config", "category": "tooling"}

    # requirements*.txt
    if name.startswith("requirements") and name.endswith(".txt"):
        return {"format": "pip", "category": "python"}

    # Docker Compose
    if name.startswith("docker-compose") and ext in (".yml", ".yaml"):
        return {"format": "Docker-Compose", "category": "deployment"}

    # YAML/TOML/JSON/INI
    if ext in (".yaml", ".yml"):
        # Check if in CI directory
        if any(d in rel_parts for d in [".github", ".circleci", ".gitlab-ci"]):
            return {"format": "YAML", "category": "ci"}
        return {"format": "YAML", "category": "application"}
    if ext == ".toml":
        return {"format": "TOML", "category": "application"}
    if ext == ".json" and not name.endswith(".lock") and name not in {"package-lock.json"}:
        return {"format": "JSON", "category": "application"}
    if ext in (".ini", ".cfg"):
        return {"format": "INI", "category": "tooling"}
    if ext == ".env" or name.startswith(".env"):
        return {"format": "dotenv", "category": "environment"}

    return None


def run(target: Path, out_dir: Path) -> None:
    print(f"[configuration_file_scanner] Scanning: {target}")
    found: list[dict] = []
    by_category: dict[str, list[str]] = {}
    by_format: dict[str, int] = {}

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            cat_info = categorize_file(fp)
            if cat_info is None:
                continue
            try:
                size_bytes = fp.stat().st_size
            except OSError:
                size_bytes = 0
            entry = {
                "file": rel,
                "name": fn,
                "format": cat_info["format"],
                "category": cat_info["category"],
                "size_bytes": size_bytes,
            }
            found.append(entry)
            by_category.setdefault(cat_info["category"], []).append(rel)
            fmt = cat_info["format"]
            by_format[fmt] = by_format.get(fmt, 0) + 1

    write_json(out_dir, "configuration_files.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "total_config_files": len(found),
        "by_category_counts": {k: len(v) for k, v in by_category.items()},
        "by_format_counts": by_format,
        "categories": by_category,
        "files": found,
    })
    print(f"  Config files: {len(found)}  Categories: {list(by_category.keys())}")


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

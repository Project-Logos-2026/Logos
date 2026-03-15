#!/usr/bin/env python3
"""
ARCHON PRIME — Dependency License Scanner
==========================================
Scans Python dependency manifests (requirements.txt, pyproject.toml,
setup.py, setup.cfg) to extract declared dependencies and attempt to
identify their license type from common known-license databases.
Writes: dependency_licenses.json
"""
import argparse
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

SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}

# Known-license lookup for common packages (best-effort static mapping)
KNOWN_LICENSES: dict[str, str] = {
    "numpy": "BSD-3-Clause", "pandas": "BSD-3-Clause", "scipy": "BSD-3-Clause",
    "matplotlib": "PSF", "pillow": "MIT-CMU", "requests": "Apache-2.0",
    "pydantic": "MIT", "fastapi": "MIT", "uvicorn": "BSD-3-Clause",
    "flask": "BSD-3-Clause", "django": "BSD-3-Clause", "sqlalchemy": "MIT",
    "pytest": "MIT", "click": "BSD-3-Clause", "typer": "MIT",
    "networkx": "BSD-3-Clause", "sklearn": "BSD-3-Clause",
    "scikit-learn": "BSD-3-Clause", "torch": "BSD-3-Clause",
    "transformers": "Apache-2.0", "openai": "MIT", "anthropic": "MIT",
    "pyyaml": "MIT", "toml": "MIT", "tomli": "MIT", "tomllib": "Apache-2.0",
    "attrs": "MIT", "cattrs": "MIT", "rich": "MIT", "loguru": "MIT",
    "aiohttp": "Apache-2.0", "httpx": "BSD-3-Clause", "starlette": "BSD-3-Clause",
    "celery": "BSD-3-Clause", "redis": "MIT", "pika": "BSD-3-Clause",
    "boto3": "Apache-2.0", "google-cloud": "Apache-2.0",
    "cryptography": "Apache-2.0", "paramiko": "LGPL-2.1",
    "setuptools": "MIT", "wheel": "MIT", "pip": "MIT",
    "black": "MIT", "flake8": "MIT", "mypy": "MIT", "pylint": "GPL-2.0",
    "isort": "MIT", "bandit": "Apache-2.0",
}

# License compatibility classifications for governance
LICENSE_TIERS: dict[str, str] = {
    "MIT": "PERMISSIVE",
    "BSD-3-Clause": "PERMISSIVE",
    "BSD-2-Clause": "PERMISSIVE",
    "Apache-2.0": "PERMISSIVE",
    "ISC": "PERMISSIVE",
    "PSF": "PERMISSIVE",
    "MIT-CMU": "PERMISSIVE",
    "LGPL-2.1": "WEAK_COPYLEFT",
    "LGPL-3.0": "WEAK_COPYLEFT",
    "MPL-2.0": "WEAK_COPYLEFT",
    "GPL-2.0": "STRONG_COPYLEFT",
    "GPL-3.0": "STRONG_COPYLEFT",
    "AGPL-3.0": "STRONG_COPYLEFT",
    "SSPL": "RESTRICTED",
    "PROPRIETARY": "RESTRICTED",
    "UNKNOWN": "UNKNOWN",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon dependency license scanner")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def parse_requirements_txt(path: Path) -> list[str]:
    """Extract package names from requirements.txt format files."""
    pkgs: list[str] = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Strip version specifiers: pkg>=1.0 → pkg
            name = re.split(r"[>=<!;@\[]", line)[0].strip().lower()
            if name:
                pkgs.append(name)
    except Exception:
        pass
    return pkgs


def parse_pyproject_toml(path: Path) -> list[str]:
    """Best-effort TOML extraction of dependencies without a TOML parser."""
    pkgs: list[str] = []
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        # Find dependency lines in project.dependencies or tool.poetry.dependencies
        for m in re.finditer(r'"([a-zA-Z0-9_\-]+)\s*[>=<!\[]', src):
            pkgs.append(m.group(1).lower())
    except Exception:
        pass
    return pkgs


def get_license(pkg_name: str) -> tuple[str, str]:
    """Return (license_id, tier) for a package name."""
    normalized = pkg_name.lower().replace("-", "_")
    for key, lic in KNOWN_LICENSES.items():
        if key.replace("-", "_") == normalized:
            tier = LICENSE_TIERS.get(lic, "UNKNOWN")
            return lic, tier
    return "UNKNOWN", "UNKNOWN"


def run(target: Path, out_dir: Path) -> None:
    print(f"[dependency_license_scanner] Scanning: {target}")
    all_deps: dict[str, dict] = {}  # pkg → {license, tier, sources}
    manifest_files: list[str] = []

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fn in sorted(fnames):
            fp = Path(root) / fn
            rel = str(fp.relative_to(target))
            pkgs: list[str] = []

            if fn.startswith("requirements") and fn.endswith(".txt"):
                pkgs = parse_requirements_txt(fp)
                manifest_files.append(rel)
            elif fn == "pyproject.toml":
                pkgs = parse_pyproject_toml(fp)
                manifest_files.append(rel)
            elif fn == "setup.cfg":
                pkgs = parse_requirements_txt(fp)  # similar format in install_requires
                manifest_files.append(rel)

            for pkg in pkgs:
                if pkg not in all_deps:
                    lic, tier = get_license(pkg)
                    all_deps[pkg] = {"license": lic, "tier": tier, "sources": []}
                all_deps[pkg]["sources"].append(rel)

    tier_counts: dict[str, int] = {}
    dep_list = []
    for pkg, info in sorted(all_deps.items()):
        tier_counts[info["tier"]] = tier_counts.get(info["tier"], 0) + 1
        dep_list.append({"package": pkg, **info})

    flagged = [d for d in dep_list if d["tier"] in ("STRONG_COPYLEFT", "RESTRICTED", "UNKNOWN")]

    write_json(out_dir, "dependency_licenses.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "manifest_files_scanned": manifest_files,
        "total_dependencies": len(all_deps),
        "tier_distribution": tier_counts,
        "flagged_for_review": [d["package"] for d in flagged],
        "dependencies": dep_list,
    })
    print(f"  Manifests: {len(manifest_files)}  Packages: {len(all_deps)}  "
          f"Flagged: {len(flagged)}  Tiers: {tier_counts}")


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

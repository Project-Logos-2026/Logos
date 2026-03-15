#!/usr/bin/env python3
"""
ARCHON PRIME — Language Detector
==================================
Detects programming languages present in the target repository
by extension mapping and shebang analysis.
Writes: language_detection_report.json
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

EXTENSION_MAP: dict[str, str] = {
    ".py": "Python", ".pyx": "Cython", ".pxd": "Cython",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".java": "Java", ".kt": "Kotlin", ".scala": "Scala",
    ".c": "C", ".h": "C", ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++",
    ".rs": "Rust", ".go": "Go", ".rb": "Ruby",
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell",
    ".yaml": "YAML", ".yml": "YAML",
    ".json": "JSON", ".toml": "TOML", ".ini": "INI", ".cfg": "INI",
    ".md": "Markdown", ".rst": "reStructuredText",
    ".sql": "SQL", ".r": "R", ".jl": "Julia",
    ".ex": "Elixir", ".exs": "Elixir",
    ".hs": "Haskell", ".ml": "OCaml",
    ".v": "Coq/Verilog", ".vo": "Coq",
    ".dockerfile": "Docker", ".proto": "Protobuf",
}

SHEBANG_MAP: dict[str, str] = {
    "python": "Python", "python3": "Python", "node": "JavaScript",
    "ruby": "Ruby", "perl": "Perl", "bash": "Shell", "sh": "Shell",
    "zsh": "Shell", "env": None,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Archon language detector")
    p.add_argument("--target", default=os.environ.get("ARCHON_TARGET", "."))
    p.add_argument("--output", default=str(OUTPUT_ROOT))
    return p.parse_args()


def write_json(out_dir: Path, name: str, data: object) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [✓] {name}")


def detect_shebang(path: Path) -> str | None:
    try:
        with open(path, "rb") as f:
            first = f.read(128).decode("utf-8", errors="replace")
        if not first.startswith("#!"):
            return None
        line = first.splitlines()[0][2:].strip()
        parts = line.split()
        interp = Path(parts[-1]).name if parts else ""
        if "env" in interp and len(parts) > 1:
            interp = Path(parts[-1]).name
        return SHEBANG_MAP.get(interp, interp) if interp else None
    except Exception:
        return None


def run(target: Path, out_dir: Path) -> None:
    print(f"[language_detector] Scanning: {target}")
    lang_counts: dict[str, int] = {}
    lang_files: dict[str, list[str]] = {}
    unknown: list[str] = []

    for root, dirs, fnames in os.walk(target):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for fname in sorted(fnames):
            fp = Path(root) / fname
            rel = str(fp.relative_to(target))
            ext = fp.suffix.lower()
            lang = EXTENSION_MAP.get(ext)
            if lang is None and not ext:
                lang = detect_shebang(fp)
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
                lang_files.setdefault(lang, []).append(rel)
            else:
                unknown.append(rel)

    write_json(out_dir, "language_detection_report.json", {
        "generated_at": RUN_TS,
        "target": str(target),
        "language_counts": dict(sorted(lang_counts.items(), key=lambda x: -x[1])),
        "language_files": lang_files,
        "unknown_files": unknown,
        "primary_language": max(lang_counts, key=lang_counts.get) if lang_counts else None,
    })
    print(f"  Languages detected: {len(lang_counts)}")
    for lang, cnt in sorted(lang_counts.items(), key=lambda x: -x[1])[:8]:
        print(f"    {lang}: {cnt}")


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

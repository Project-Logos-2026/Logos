"""
generate_symbol_import_index.py

Read-only AST audit: extracts symbol-level import data from all Python files
in the repository (discovered via os.walk) and writes the result to
_Reports/Canonical_Import_Facade/repo_symbol_imports.json.

Also writes/refreshes repo_python_files.json in the repo root as a side-effect
so downstream tooling has an up-to-date index.

No other repository files are modified.
"""

import ast
import json
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

PYTHON_FILES_INDEX = os.path.join(REPO_ROOT, "repo_python_files.json")
OUTPUT_FILE = os.path.join(REPO_ROOT, "_Reports", "Canonical_Import_Facade", "repo_symbol_imports.json")

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}


def should_skip(rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    return any(part in IGNORE_DIRS for part in parts)


def discover_python_files() -> list[str]:
    """Walk the repo and return relative paths of all .py files, refreshing the index."""
    files = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fname in filenames:
            if fname.endswith(".py"):
                rel = os.path.relpath(os.path.join(dirpath, fname), REPO_ROOT)
                files.append(rel)
    # Refresh index file
    with open(PYTHON_FILES_INDEX, "w", encoding="utf-8") as f:
        json.dump({"python_files": files}, f, indent=2)
    return files


def load_python_files() -> list[str]:
    if os.path.exists(PYTHON_FILES_INDEX):
        with open(PYTHON_FILES_INDEX, "r", encoding="utf-8") as f:
            data = json.load(f)
        files = [p for p in data["python_files"] if not should_skip(p)]
        if files:
            return files
    # Fall back to discovery
    return discover_python_files()


def read_source_lines(abs_path: str) -> list[str]:
    try:
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            return f.readlines()
    except OSError:
        return []


def parse_imports(rel_path: str, source_lines: list[str]) -> list[dict]:
    source = "".join(source_lines)
    records = []

    try:
        tree = ast.parse(source, filename=rel_path)
    except SyntaxError:
        return records

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # import module.submodule [as alias]
            for alias in node.names:
                line_text = source_lines[node.lineno - 1].rstrip() if node.lineno <= len(source_lines) else ""
                records.append({
                    "symbol": alias.name.split(".")[0],
                    "source_module": alias.name,
                    "imported_by_file": rel_path,
                    "import_line_number": node.lineno,
                    "import_statement": line_text,
                    "alias": alias.asname,
                })

        elif isinstance(node, ast.ImportFrom):
            # from module.submodule import Symbol [as Alias]
            module = node.module or ""
            level = node.level  # relative import dots
            module_str = ("." * level) + module if level else module

            for alias in node.names:
                line_text = source_lines[node.lineno - 1].rstrip() if node.lineno <= len(source_lines) else ""
                records.append({
                    "symbol": alias.name,
                    "source_module": module_str,
                    "imported_by_file": rel_path,
                    "import_line_number": node.lineno,
                    "import_statement": line_text,
                    "alias": alias.asname,
                })

    return records


def main() -> None:
    print(f"Repo root: {REPO_ROOT}")
    python_files = load_python_files()
    print(f"Python files found: {len(python_files)}")
    all_symbols: list[dict] = []
    files_scanned = 0

    for rel_path in python_files:
        abs_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.isfile(abs_path):
            continue
        source_lines = read_source_lines(abs_path)
        records = parse_imports(rel_path, source_lines)
        all_symbols.extend(records)
        files_scanned += 1

    unique_symbols = len({r["symbol"] for r in all_symbols})

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"symbols": all_symbols}, f, indent=2)

    print(f"Files scanned:    {files_scanned}")
    print(f"Total imports:    {len(all_symbols)}")
    print(f"Unique symbols:   {unique_symbols}")
    print(f"Output written:   {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

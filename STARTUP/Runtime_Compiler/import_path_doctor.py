
"""Import path doctor for LOGOS.

What it does:
1) Scans Python files for import statements.
2) Flags likely dead imports (unresolvable via importlib).
3) Rewrites legacy `Logos_System` import prefixes to `LOGOS_SYSTEM` (optional).
4) Optionally runs `ruff --fix --select F401` to drop unused imports.

This is designed as a practical migration utility for import-path normalization.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(REPO_ROOT))

LEGACY_PREFIXES = {
	"Logos_System": "LOGOS_SYSTEM",
	"logos_system": "LOGOS_SYSTEM",
}


class ImportCollector(ast.NodeVisitor):
	def __init__(self) -> None:
		self.imports: List[Tuple[str, int, str, int]] = []

	def visit_Import(self, node: ast.Import) -> None:
		for alias in node.names:
			self.imports.append((alias.name, node.lineno, "import", 0))

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
		if node.module:
			self.imports.append((node.module, node.lineno, "from", node.level))


def iter_python_files(paths: Iterable[Path]) -> Iterable[Path]:
	for base in paths:
		if base.is_file() and base.suffix == ".py":
			yield base
			continue
		for py_file in base.rglob("*.py"):
			if any(part in {".git", "__pycache__", ".pytest_cache"} for part in py_file.parts):
				continue
			yield py_file


def normalize_module_name(name: str) -> str:
	for legacy, canonical in LEGACY_PREFIXES.items():
		if name == legacy or name.startswith(f"{legacy}."):
			return canonical + name[len(legacy):]
	return name


def is_resolvable(module_name: str) -> bool:
	if module_name.startswith("."):
		return True
	check_name = normalize_module_name(module_name)
	try:
		return importlib.util.find_spec(check_name) is not None
	except Exception:
		return False


def rewrite_legacy_import_prefixes(file_path: Path) -> bool:
	original = file_path.read_text(encoding="utf-8")
	updated = original
	patterns = [
		(re.compile(r"(^\s*from\s+)Logos_System(?=\.|\s)", flags=re.MULTILINE), r"\1LOGOS_SYSTEM"),
		(re.compile(r"(^\s*import\s+)Logos_System(?=\.|\s|$)", flags=re.MULTILINE), r"\1LOGOS_SYSTEM"),
		(re.compile(r"(^\s*from\s+)logos_system(?=\.|\s)", flags=re.MULTILINE), r"\1LOGOS_SYSTEM"),
		(re.compile(r"(^\s*import\s+)logos_system(?=\.|\s|$)", flags=re.MULTILINE), r"\1LOGOS_SYSTEM"),
	]
	for pattern, replacement in patterns:
		updated = pattern.sub(replacement, updated)

	if updated != original:
		file_path.write_text(updated, encoding="utf-8")
		return True
	return False


def run_ruff_fix_unused(files: List[Path]) -> Tuple[int, str]:
	if not files:
		return 0, ""
	cmd = [
		sys.executable,
		"-m",
		"ruff",
		"check",
		"--fix",
		"--select",
		"F401",
		*[str(p) for p in files],
	]
	proc = subprocess.run(cmd, capture_output=True, text=True)
	output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
	return proc.returncode, output.strip()


def scan_file(path: Path) -> Dict[str, object]:
	result: Dict[str, object] = {
		"file": str(path),
		"parse_error": None,
		"imports": [],
		"dead_imports": [],
	}

	try:
		source = path.read_text(encoding="utf-8")
		tree = ast.parse(source)
	except Exception as exc:
		result["parse_error"] = str(exc)
		return result

	collector = ImportCollector()
	collector.visit(tree)

	imports = []
	dead = []
	for module_name, lineno, kind, level in collector.imports:
		normalized = normalize_module_name(module_name)
		ok = True if level > 0 else is_resolvable(module_name)
		row = {
			"module": module_name,
			"normalized": normalized,
			"line": lineno,
			"kind": kind,
			"level": level,
			"resolvable": ok,
		}
		imports.append(row)
		if not ok:
			dead.append(row)

	result["imports"] = imports
	result["dead_imports"] = dead
	return result


def main() -> None:
	parser = argparse.ArgumentParser(description="Import normalization + dead import scanner")
	parser.add_argument(
		"paths",
		nargs="*",
		default=["LOGOS_SYSTEM", "STARTUP"],
		help="Paths to scan (files or directories).",
	)
	parser.add_argument("--rewrite-legacy", action="store_true", help="Rewrite legacy Logos_System imports.")
	parser.add_argument("--ruff-fix-unused", action="store_true", help="Run ruff F401 autofix after rewriting.")
	parser.add_argument(
		"--report",
		default="_Reports/Audit_And_Normalization_Reports/import_path_doctor_report.json",
		help="Path for JSON report output.",
	)
	args = parser.parse_args()

	targets = [Path(p).resolve() for p in args.paths]
	all_files = sorted(set(iter_python_files(targets)))

	rewritten: List[str] = []
	if args.rewrite_legacy:
		for file_path in all_files:
			if rewrite_legacy_import_prefixes(file_path):
				rewritten.append(str(file_path))

	ruff_output = ""
	if args.ruff_fix_unused:
		code, ruff_output = run_ruff_fix_unused([Path(p) for p in rewritten])
		if code not in (0, 1):
			raise SystemExit(f"ruff failed with exit code {code}\n{ruff_output}")

	scan_results = [scan_file(path) for path in all_files]
	dead_count = sum(len(row["dead_imports"]) for row in scan_results)
	parse_errors = sum(1 for row in scan_results if row["parse_error"])

	report = {
		"scanned_files": len(all_files),
		"rewritten_files": len(rewritten),
		"dead_import_count": dead_count,
		"parse_errors": parse_errors,
		"results": scan_results,
		"ruff_output": ruff_output,
	}

	report_path = Path(args.report)
	report_path.parent.mkdir(parents=True, exist_ok=True)
	report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

	print(
		f"Scanned={report['scanned_files']} rewritten={report['rewritten_files']} "
		f"dead_imports={report['dead_import_count']} parse_errors={report['parse_errors']}"
	)
	print(f"Report: {report_path}")

if __name__ == "__main__":
	main()
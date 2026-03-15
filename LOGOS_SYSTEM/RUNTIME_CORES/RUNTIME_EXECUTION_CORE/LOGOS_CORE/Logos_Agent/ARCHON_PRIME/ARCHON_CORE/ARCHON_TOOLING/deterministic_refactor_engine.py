"""
Deterministic Refactor Engine
Provides deterministic, idempotent code transformations.

SAFETY — dry_run=True (default)
    All methods return a preview of what would change without writing files.
    Pass dry_run=False explicitly to commit writes to disk.
    This protects Logos from unintended mass-modification.
"""

from pathlib import Path
from typing import List, Dict


class DeterministicRefactorEngine:

    def __init__(self, repo_root: str, dry_run: bool = True):
        self.repo_root = Path(repo_root)
        self.dry_run = dry_run

    def normalize_imports(self) -> List[Dict]:
        """
        Sort import lines (import / from...import) to the top of each file,
        ahead of all other content, in lexicographic order.

        When dry_run=True (default): returns a list of change-preview dicts,
        no files are modified.

        When dry_run=False: writes transformed content to disk and returns the
        same list of change dicts.

        Returns
        -------
        list of dicts:
            { "file": str, "status": "changed"|"unchanged",
              "original_imports": list[str], "sorted_imports": list[str] }
        """
        results = []

        for file in self.repo_root.rglob("*.py"):
            try:
                original = file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            lines = original.splitlines()
            import_lines = sorted(
                l for l in lines
                if l.startswith("import ") or l.startswith("from ")
            )
            other_lines = [
                l for l in lines
                if not (l.startswith("import ") or l.startswith("from "))
            ]
            new_content = "\n".join(import_lines + [""] + other_lines)

            changed = new_content != original
            entry = {
                "file": str(file),
                "status": "changed" if changed else "unchanged",
                "original_imports": [l for l in lines if l.startswith(("import ", "from "))],
                "sorted_imports": import_lines,
            }
            results.append(entry)

            if changed and not self.dry_run:
                file.write_text(new_content, encoding="utf-8")

        return results

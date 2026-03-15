# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-008
# module_name:          crawl_engine
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/crawler/core/crawl_engine.py
# responsibility:       Utility module: crawl engine
# runtime_stage:        utility
# execution_entry:      run
# allowed_targets:      []
# forbidden_targets:    ["SYSTEM", "WORKFLOW_NEXUS"]
# allowed_imports:      []
# forbidden_imports:    []
# spec_reference:       [SPEC-AP-V2.1]
# implementation_phase: PHASE_2
# authoring_authority:  ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================
from WORKFLOW_NEXUS.Governance.workflow_gate import enforce_runtime_gate

enforce_runtime_gate()

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

"""
ARCHON PRIME — Crawl Engine
Stage 4: Crawler System Implementation

Responsibilities:
  - Load target repository paths from targets/logos_targets.yaml
  - Traverse repository directories up to configured max_depth
  - Identify Python modules and supported file types
  - Produce deterministic traversal order
  - Generate module discovery metadata
  - Enforce dry_run / read-only constraints (no mutations)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml

    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


SUPPORTED_EXTENSIONS = {".py", ".json", ".yaml", ".yml", ".md"}
IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    ".eggs",
}


class CrawlEngine:
    """
    Deterministic repository crawler.
    Operates in read-only mode; produces traversal plans and module metadata.
    """

    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.targets: List[Dict[str, Any]] = []
        self.traversal_plan: Dict[str, Any] = {}
        self.discovered_modules: List[Dict[str, Any]] = []
        self.max_depth: int = 1000
        self.mutation_allowed: bool = False

    # ------------------------------------------------------------------
    # Target loading
    # ------------------------------------------------------------------

    def load_targets(self, targets_path: str = None) -> List[Dict[str, Any]]:
        """
        Load target repository definitions from logos_targets.yaml.
        Falls back to a minimal default if yaml is unavailable.
        """
        if targets_path is None:
            targets_path = str(self.root / "targets" / "logos_targets.yaml")

        if not os.path.exists(targets_path):
            self.targets = []
            return self.targets

        if _YAML_AVAILABLE:
            with open(targets_path) as f:
                data = yaml.safe_load(f) or {}
            self.targets = data.get("targets", [])
        else:
            # Minimal fallback parser for the expected simple YAML format
            self.targets = self._parse_targets_minimal(targets_path)

        return self.targets

    def _parse_targets_minimal(self, path: str) -> List[Dict[str, Any]]:
        """Minimal line-by-line YAML parser for targets file (no PyYAML)."""
        targets = []
        current: Dict[str, Any] = {}
        with open(path) as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith("- name:"):
                    if current:
                        targets.append(current)
                    current = {"name": stripped.split(":", 1)[1].strip()}
                elif stripped.startswith("path:") and current is not None:
                    current["path"] = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("branch:") and current is not None:
                    current["branch"] = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("language:") and current is not None:
                    current["language"] = stripped.split(":", 1)[1].strip()
        if current:
            targets.append(current)
        return targets

    # ------------------------------------------------------------------
    # File discovery
    # ------------------------------------------------------------------

    def discover_files(self, target_repo: str) -> List[Dict[str, Any]]:
        """
        Recursively scan target_repo up to max_depth.
        Returns structured file index (read-only; no writes).
        """
        target_path = Path(target_repo)
        if not target_path.exists():
            return []

        files = []
        base_depth = len(target_path.parts)

        for dirpath, dirnames, filenames in os.walk(target_path):
            current_path = Path(dirpath)
            current_depth = len(current_path.parts) - base_depth

            if current_depth > self.max_depth:
                dirnames.clear()
                continue

            # Prune ignored directories in-place to prevent descent
            dirnames[:] = sorted(
                d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")
            )

            for filename in sorted(filenames):
                file_path = current_path / filename
                ext = file_path.suffix.lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    continue

                rel_path = str(file_path.relative_to(target_path))
                files.append(
                    {
                        "path": rel_path,
                        "absolute_path": str(file_path),
                        "extension": ext,
                        "type": self._classify_file(ext, filename),
                        "depth": current_depth,
                        "size_bytes": (
                            file_path.stat().st_size if file_path.exists() else 0
                        ),
                    }
                )

        return files

    def _classify_file(self, ext: str, filename: str) -> str:
        if ext == ".py":
            return "python_module"
        if ext in {".json"}:
            return "config_json"
        if ext in {".yaml", ".yml"}:
            return "config_yaml"
        if ext == ".md":
            return "documentation"
        return "unknown"

    # ------------------------------------------------------------------
    # Module discovery
    # ------------------------------------------------------------------

    def discover_modules(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter file index to Python modules and enrich with module metadata.
        """
        modules = []
        for f in files:
            if f["type"] != "python_module":
                continue
            rel = f["path"]
            # Derive dotted import path from relative file path
            import_path = rel.replace(os.sep, ".").replace("/", ".").removesuffix(".py")
            is_package = rel.endswith("__init__.py")
            modules.append(
                {
                    "path": rel,
                    "absolute_path": f["absolute_path"],
                    "import_path": import_path,
                    "is_package_init": is_package,
                    "depth": f["depth"],
                    "size_bytes": f["size_bytes"],
                }
            )
        self.discovered_modules = modules
        return modules

    # ------------------------------------------------------------------
    # Traversal plan
    # ------------------------------------------------------------------

    def build_traversal_plan(
        self,
        target_repo: str = None,
        files: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Build a deterministic traversal plan over all discovered files.
        Modules are ordered depth-first, shallowest first.
        No mutations are performed regardless of crawl_config.
        """
        if files is None:
            if target_repo is None:
                target_repo = str(self.root)
            files = self.discover_files(target_repo)

        modules = self.discover_modules(files)

        # Sort deterministically: depth ASC, then path ASC
        ordered = sorted(modules, key=lambda m: (m["depth"], m["path"]))

        # Identify orphan modules (depth > 0, not inside a package)
        package_dirs = {
            os.path.dirname(m["path"]) for m in modules if m["is_package_init"]
        }
        orphans = [
            m
            for m in ordered
            if not m["is_package_init"]
            and os.path.dirname(m["path"]) not in package_dirs
            and m["depth"] > 0
        ]

        self.traversal_plan = {
            "target_repo": str(target_repo),
            "total_files_discovered": len(files),
            "total_modules_discovered": len(modules),
            "traversal_order": ordered,
            "orphan_modules": orphans,
            "orphan_count": len(orphans),
            "file_type_summary": self._summarize_types(files),
        }

        return self.traversal_plan

    def _summarize_types(self, files: List[Dict[str, Any]]) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for f in files:
            t = f["type"]
            summary[t] = summary.get(t, 0) + 1
        return summary

    # ------------------------------------------------------------------
    # Full crawl (entry point used by CrawlerController)
    # ------------------------------------------------------------------

    def run(self, target_repo: str = None) -> Dict[str, Any]:
        """
        Execute full discovery flow and return traversal plan.
        Read-only — no mutations ever occur here.
        """
        if target_repo is None:
            if self.targets:
                target_repo = self.targets[0].get("path", str(self.root))
            else:
                target_repo = str(self.root)

        return self.build_traversal_plan(target_repo=target_repo)


if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    engine = CrawlEngine(root)
    engine.load_targets()
    plan = engine.run()
    print(
        json.dumps(
            {k: v for k, v in plan.items() if k != "traversal_order"},
            indent=2,
        )
    )

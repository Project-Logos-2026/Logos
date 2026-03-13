# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-004
# module_name:          crawler_controller
# subsystem:            mutation_tooling
# module_role:          orchestration
# canonical_path:       WORKFLOW_MUTATION_TOOLING/controllers/crawler_controller.py
# responsibility:       Orchestration module: crawler controller
# runtime_stage:        orchestration
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
ARCHON PRIME — Crawler Controller
Stage 4: Crawler System Implementation

Responsibilities:
  - Load crawl_config.json and targets/logos_targets.yaml via ConfigLoader
  - Instantiate CrawlEngine and CrawlMonitor
  - Execute deterministic repository traversal
  - Route traversal artifacts to AP_SYSTEM_AUDIT/
  - Enforce dry_run and mutation_allowed constraints
  - Provide traversal plan to downstream repair and orchestration systems
  - Validate imports of all crawler modules before execution
"""

import importlib
import json
import os
import sys
import traceback
from typing import Any, Dict, List, Optional

from controllers.config_loader import ConfigLoader
from crawler.core.crawl_engine import CrawlEngine
from crawler.core.crawl_monitor import CrawlMonitor
from crawler.utils.file_scanner import scan_directory, summarize_index

ARTIFACT_OUTPUT_DIR = "AP_SYSTEM_AUDIT"
IMPORT_ERROR_ARTIFACT = "AP_SYSTEM_AUDIT/CRAWLER_IMPORT_ERRORS.json"

CRAWLER_MODULES = [
    "crawler.core.crawl_engine",
    "crawler.core.crawl_monitor",
    "crawler.utils.file_scanner",
]

ARTIFACT_MAP = {
    "traversal_plan": "AP_SYSTEM_AUDIT/crawler_traversal_plan.json",
    "file_index": "AP_SYSTEM_AUDIT/crawler_file_index.json",
    "crawl_summary": "AP_SYSTEM_AUDIT/crawler_crawl_summary.json",
    "orphan_report": "AP_SYSTEM_AUDIT/crawler_orphan_report.json",
}


class CrawlerController:
    """
    Orchestrates deterministic repository crawling.
    Enforces read-only operation while dry_run is active.
    """

    def __init__(self, root_path: str):
        self.root = root_path
        self.config_loader = ConfigLoader(root_path)
        self.crawl_config: Dict[str, Any] = {}
        self.targets: List[Dict[str, Any]] = []
        self.import_errors: List[Dict[str, Any]] = []
        self._engine: Optional[CrawlEngine] = None
        self._monitor: Optional[CrawlMonitor] = None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def load_configs(self) -> Dict[str, Any]:
        """Load crawl configuration. Enforces dry_run and constraint flags."""
        self.crawl_config = self.config_loader.load_crawl_config()
        return self.crawl_config

    def load_targets(self) -> List[Dict[str, Any]]:
        """Load target repository definitions from logos_targets.yaml."""
        targets_path = os.path.join(self.root, "targets", "logos_targets.yaml")
        engine = CrawlEngine(self.root)
        self.targets = engine.load_targets(targets_path)
        return self.targets

    @property
    def dry_run(self) -> bool:
        return self.crawl_config.get("crawl_mode") == "dry_run"

    @property
    def mutation_allowed(self) -> bool:
        return bool(self.crawl_config.get("mutation_allowed", False))

    @property
    def max_depth(self) -> int:
        return int(self.crawl_config.get("max_depth", 1000))

    # ------------------------------------------------------------------
    # Import validation
    # ------------------------------------------------------------------

    def _ensure_root_on_path(self):
        if self.root not in sys.path:
            sys.path.insert(0, self.root)

    def validate_imports(self) -> List[Dict[str, Any]]:
        """
        Attempt to import all crawler modules.
        Failures written to CRAWLER_IMPORT_ERRORS.json; execution continues.
        """
        self._ensure_root_on_path()
        self.import_errors = []

        for module_path in CRAWLER_MODULES:
            try:
                importlib.import_module(module_path)
            except Exception:
                self.import_errors.append(
                    {
                        "module": module_path,
                        "error": traceback.format_exc().strip(),
                    }
                )

        error_path = os.path.join(self.root, IMPORT_ERROR_ARTIFACT)
        os.makedirs(os.path.dirname(error_path), exist_ok=True)
        with open(error_path, "w") as f:
            json.dump(
                {
                    "stage": "Crawler System Implementation",
                    "import_errors": self.import_errors,
                    "total_errors": len(self.import_errors),
                },
                f,
                indent=2,
            )

        return self.import_errors

    # ------------------------------------------------------------------
    # Crawl execution
    # ------------------------------------------------------------------

    def _resolve_target_repo(self) -> str:
        """Return the primary target repo path, falling back to root."""
        if self.targets:
            return self.targets[0].get("path", self.root)
        return self.root

    def run_crawl(self, target_repo: str = None) -> Dict[str, Any]:
        """
        Execute a full deterministic crawl of target_repo.
        In dry_run mode, traversal is read-only and no mutations occur.
        Returns the traversal plan dict.
        """
        if target_repo is None:
            target_repo = self._resolve_target_repo()

        # --- Engine ---
        self._engine = CrawlEngine(self.root)
        self._engine.max_depth = self.max_depth
        self._engine.mutation_allowed = False  # Always enforce read-only

        self._engine.load_targets()

        # --- Monitor ---
        self._monitor = CrawlMonitor()
        self._monitor.start()

        # --- File scan (always via file_scanner for the AP root) ---
        ap_file_index = scan_directory(self.root, max_depth=self.max_depth)
        ap_summary = summarize_index(ap_file_index)

        # --- Target repo traversal ---
        plan = self._engine.run(target_repo=target_repo)
        self._monitor.ingest_traversal_plan(plan)
        self._monitor.stop()

        crawl_summary = self._monitor.generate_summary()

        # --- Artifact routing ---
        self._write_artifacts(plan, ap_file_index, crawl_summary)

        return {
            "traversal_plan": plan,
            "crawl_summary": crawl_summary,
            "ap_file_index_summary": ap_summary,
            "dry_run": self.dry_run,
            "mutation_allowed": self.mutation_allowed,
        }

    def _write_artifacts(
        self,
        plan: Dict[str, Any],
        file_index: List[Dict[str, Any]],
        crawl_summary: Dict[str, Any],
    ):
        """Route all crawl artifacts to AP_SYSTEM_AUDIT/."""
        artifact_dir = os.path.join(self.root, ARTIFACT_OUTPUT_DIR)
        os.makedirs(artifact_dir, exist_ok=True)

        # Traversal plan (exclude large traversal_order list for file artifact)
        plan_artifact = {k: v for k, v in plan.items() if k != "traversal_order"}
        plan_artifact["traversal_order_count"] = len(plan.get("traversal_order", []))

        self._write_json(
            os.path.join(self.root, ARTIFACT_MAP["traversal_plan"]),
            plan_artifact,
        )
        self._write_json(
            os.path.join(self.root, ARTIFACT_MAP["file_index"]),
            file_index,
        )
        self._write_json(
            os.path.join(self.root, ARTIFACT_MAP["crawl_summary"]),
            crawl_summary,
        )
        self._write_json(
            os.path.join(self.root, ARTIFACT_MAP["orphan_report"]),
            {
                "orphan_modules": plan.get("orphan_modules", []),
                "orphan_count": plan.get("orphan_count", 0),
            },
        )

    @staticmethod
    def _write_json(path: str, data: Any):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # Full pipeline entry point
    # ------------------------------------------------------------------

    def run(self, target_repo: str = None) -> Dict[str, Any]:
        """
        Full controller pipeline:
          1. Load configs
          2. Load targets
          3. Validate imports
          4. Execute crawl
          5. Return results
        """
        self.load_configs()
        self.load_targets()
        self.validate_imports()
        return self.run_crawl(target_repo=target_repo)

    # ------------------------------------------------------------------
    # Accessor for downstream systems
    # ------------------------------------------------------------------

    def get_traversal_plan(self) -> Optional[Dict[str, Any]]:
        """Return the most recent traversal plan (for repair / orchestration)."""
        plan_path = os.path.join(self.root, ARTIFACT_MAP["traversal_plan"])
        if os.path.exists(plan_path):
            with open(plan_path) as f:
                return json.load(f)
        return None


# ---------------------------------------------------------------------------
# CLI entry point (read-only / dry_run safe)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/ARCHON_PRIME"
    controller = CrawlerController(root)
    results = controller.run()
    summary = results.get("crawl_summary", {})
    print(json.dumps(summary, indent=2))

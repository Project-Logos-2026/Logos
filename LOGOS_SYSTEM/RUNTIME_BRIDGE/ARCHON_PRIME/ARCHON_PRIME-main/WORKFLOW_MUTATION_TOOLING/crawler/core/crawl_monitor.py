# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-009
# module_name:          crawl_monitor
# subsystem:            mutation_tooling
# module_role:          utility
# canonical_path:       WORKFLOW_MUTATION_TOOLING/crawler/core/crawl_monitor.py
# responsibility:       Utility module: crawl monitor
# runtime_stage:        utility
# execution_entry:      None
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
ARCHON PRIME — Crawl Monitor
Stage 4: Crawler System Implementation

Responsibilities:
  - Monitor crawler progress during traversal
  - Detect traversal anomalies (stalls, depth violations, unexpected types)
  - Track module processing counts
  - Record timing and throughput metrics
  - Produce crawl summary artifact
"""

import json
import os
import time
from typing import Any, Dict, List, Optional


class CrawlMonitor:
    """
    Non-blocking crawl monitor.
    Receives events from CrawlEngine and accumulates a summary.
    Does not execute any traversal itself — observation only.
    """

    def __init__(self):
        self.modules_discovered: int = 0
        self.directories_scanned: int = 0
        self.files_scanned: int = 0
        self.orphans_detected: int = 0
        self.anomalies: List[Dict[str, Any]] = []
        self.module_log: List[str] = []
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self):
        """Mark crawl start time."""
        self._start_time = time.time()
        self._end_time = None

    def stop(self):
        """Mark crawl end time."""
        self._end_time = time.time()

    @property
    def elapsed_seconds(self) -> float:
        if self._start_time is None:
            return 0.0
        end = self._end_time if self._end_time is not None else time.time()
        return round(end - self._start_time, 4)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def log_module(self, module_path: str):
        """Record a discovered module."""
        self.modules_discovered += 1
        self.module_log.append(module_path)

    def log_directory(self, dir_path: str):
        """Record a scanned directory."""
        self.directories_scanned += 1

    def log_file(self, file_path: str):
        """Record a scanned file."""
        self.files_scanned += 1

    def log_orphan(self, module_path: str):
        """Record a detected orphan module."""
        self.orphans_detected += 1
        self.log_anomaly(
            "orphan_module", module_path, "Module has no package __init__.py"
        )

    def log_anomaly(self, anomaly_type: str, path: str, detail: str = ""):
        """Record a traversal anomaly."""
        self.anomalies.append(
            {
                "type": anomaly_type,
                "path": path,
                "detail": detail,
                "elapsed_at": self.elapsed_seconds,
            }
        )

    def ingest_traversal_plan(self, plan: Dict[str, Any]):
        """
        Consume a completed traversal plan dict from CrawlEngine
        and populate monitor counters from it.
        """
        self.modules_discovered = plan.get("total_modules_discovered", 0)
        self.files_scanned = plan.get("total_files_discovered", 0)
        self.orphans_detected = plan.get("orphan_count", 0)

        for orphan in plan.get("orphan_modules", []):
            path = orphan.get("path", "")
            if path not in [a["path"] for a in self.anomalies]:
                self.log_anomaly(
                    "orphan_module", path, "No package __init__.py in parent dir"
                )

    # ------------------------------------------------------------------
    # Summary generation
    # ------------------------------------------------------------------

    def generate_summary(self) -> Dict[str, Any]:
        """
        Produce a structured crawl summary dict.
        """
        return {
            "modules_discovered": self.modules_discovered,
            "directories_scanned": self.directories_scanned,
            "files_scanned": self.files_scanned,
            "orphans_detected": self.orphans_detected,
            "anomalies": self.anomalies,
            "anomaly_count": len(self.anomalies),
            "elapsed_seconds": self.elapsed_seconds,
            "status": "complete",
        }

    def write_summary(self, output_path: str) -> Dict[str, Any]:
        """Write crawl summary to a JSON artifact."""
        summary = self.generate_summary()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)
        return summary

    def reset(self):
        """Reset all counters for a fresh crawl run."""
        self.__init__()


if __name__ == "__main__":
    monitor = CrawlMonitor()
    monitor.start()
    monitor.log_module("tools/runtime_analysis/dependency_graph.py")
    monitor.log_directory("tools/runtime_analysis")
    monitor.stop()
    print(json.dumps(monitor.generate_summary(), indent=2))

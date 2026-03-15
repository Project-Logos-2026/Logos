# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-018
# module_name:          module_relocation_operator
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/module_relocation_operator.py
# responsibility:       Mutation module: module relocation operator
# runtime_stage:        repair
# execution_entry:      None
# allowed_targets:      ["WORKFLOW_TARGET_PROCESSING/PROCESSING"]
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
ARCHON PRIME — Module Relocation Operator
Stage 5: Repair System Implementation

Plans and applies corrections for misplaced modules — Python files
located outside their canonical package directory, identified as
orphans by the crawler subsystem.

SAFETY CONTRACT:
  - plan_repair() is always safe — read-only analysis only.
  - apply_repair() MUST NOT be called while mutation_allowed = false
    or crawl_mode = dry_run. The RepairController enforces this gate.
"""

import os
import shutil
from typing import Any, Dict


class ModuleRelocationOperator:
    """
    Detects orphaned or misplaced Python modules and plans/applies
    relocation to canonical package directories.
    """

    ISSUE_TYPE = "module_misplacement"

    def plan_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse a module_misplacement issue and produce a repair plan.
        Read-only — no file modifications occur here.

        Parameters
        ----------
        issue : dict with keys:
            module, current_path, canonical_path, reason

        Returns
        -------
        Repair plan dict.
        """
        module = issue.get("module", "unknown")
        current_path = issue.get("current_path", "")
        canonical_path = issue.get("canonical_path", "")
        reason = issue.get("reason", "orphan_detected")

        return {
            "operator": self.__class__.__name__,
            "issue_type": self.ISSUE_TYPE,
            "module": module,
            "action": "relocate_module",
            "current_path": current_path,
            "canonical_path": canonical_path,
            "reason": reason,
            "reversible": True,
            "mutation_required": True,
            "status": "planned",
            "applied": False,
            "note": (
                "Relocation requires __init__.py creation in target package. "
                "Verify canonical_path before applying."
            ),
        }

    def apply_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Relocate a misplaced module to its canonical path.

        THIS METHOD MUST ONLY BE CALLED WHEN mutation_allowed = true.
        Only moves files — never deletes originals without confirmation.
        """
        if not issue.get("_mutation_authorized", False):
            raise RuntimeError(
                "ModuleRelocationOperator.apply_repair() called without "
                "mutation_authorized flag."
            )

        current_path = issue.get("current_path", "")
        canonical_path = issue.get("canonical_path", "")

        if not current_path or not canonical_path:
            return {
                "status": "failed",
                "reason": "current_path or canonical_path missing",
            }

        if not os.path.exists(current_path):
            return {"status": "failed", "reason": f"Source not found: {current_path}"}

        if os.path.exists(canonical_path):
            return {
                "status": "skipped",
                "reason": f"Target already exists: {canonical_path}",
            }

        try:
            os.makedirs(os.path.dirname(canonical_path), exist_ok=True)
            shutil.move(current_path, canonical_path)
            return {
                "status": "applied",
                "from": current_path,
                "to": canonical_path,
            }
        except OSError as exc:
            return {"status": "failed", "reason": str(exc)}

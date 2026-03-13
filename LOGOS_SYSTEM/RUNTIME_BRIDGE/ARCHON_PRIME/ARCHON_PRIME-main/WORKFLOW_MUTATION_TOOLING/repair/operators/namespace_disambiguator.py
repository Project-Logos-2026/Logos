# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-019
# module_name:          namespace_disambiguator
# subsystem:            mutation_tooling
# module_role:          mutation
# canonical_path:       WORKFLOW_MUTATION_TOOLING/repair/operators/namespace_disambiguator.py
# responsibility:       Mutation module: namespace disambiguator
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
ARCHON PRIME — Namespace Disambiguator Operator
Stage 5: Repair System Implementation

Plans and applies corrections for namespace shadowing conflicts —
Python modules sharing identical `stem` names across different
package directories, identified by the namespace shadow auditor.

SAFETY CONTRACT:
  - plan_repair() is always safe — read-only analysis only.
  - apply_repair() MUST NOT be called while mutation_allowed = false
    or crawl_mode = dry_run. The RepairController enforces this gate.
"""

import os
from typing import Any, Dict


class NamespaceDisambiguatorOperator:
    """
    Detects namespace shadow conflicts and plans/applies
    disambiguation via module renaming or package restructuring.
    """

    ISSUE_TYPE = "namespace_collision"

    def plan_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse a namespace_collision issue and produce a repair plan.
        Read-only — no file modifications occur here.

        Parameters
        ----------
        issue : dict with keys:
            module (stem), file_a, file_b, suggested_rename_a, suggested_rename_b

        Returns
        -------
        Repair plan dict.
        """
        module = issue.get("module", "unknown")
        file_a = issue.get("file_a", "")
        file_b = issue.get("file_b", "")
        suggested_rename_a = issue.get(
            "suggested_rename_a",
            self._suggest_rename(file_a, module),
        )
        suggested_rename_b = issue.get(
            "suggested_rename_b",
            self._suggest_rename(file_b, module),
        )

        return {
            "operator": self.__class__.__name__,
            "issue_type": self.ISSUE_TYPE,
            "module_stem": module,
            "action": "disambiguate_namespace",
            "conflicting_files": [file_a, file_b],
            "proposed_rename_a": suggested_rename_a,
            "proposed_rename_b": suggested_rename_b,
            "reversible": True,
            "mutation_required": True,
            "status": "planned",
            "applied": False,
            "note": (
                "Renaming modules changes their import paths across the codebase. "
                "Run ImportScanner after apply to detect downstream breakage."
            ),
        }

    def apply_repair(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rename the lower-priority conflicting module to resolve namespace shadow.

        THIS METHOD MUST ONLY BE CALLED WHEN mutation_allowed = true.
        Renames file_b only; file_a (first-registered) keeps its name.
        """
        if not issue.get("_mutation_authorized", False):
            raise RuntimeError(
                "NamespaceDisambiguatorOperator.apply_repair() called without "
                "mutation_authorized flag."
            )

        file_b = issue.get("file_b", "")
        suggested_rename_b = issue.get("suggested_rename_b", "")

        if not file_b or not suggested_rename_b:
            return {
                "status": "failed",
                "reason": "file_b or suggested_rename_b missing",
            }

        if not os.path.exists(file_b):
            return {"status": "failed", "reason": f"Source not found: {file_b}"}

        if os.path.exists(suggested_rename_b):
            return {
                "status": "skipped",
                "reason": f"Target already exists: {suggested_rename_b}",
            }

        try:
            os.rename(file_b, suggested_rename_b)
            return {
                "status": "applied",
                "renamed_from": file_b,
                "renamed_to": suggested_rename_b,
            }
        except OSError as exc:
            return {"status": "failed", "reason": str(exc)}

    @staticmethod
    def _suggest_rename(file_path: str, stem: str) -> str:
        """Derive a disambiguated filename by prepending the parent package name."""
        if not file_path:
            return ""
        parts = file_path.replace("\\", "/").split("/")
        if len(parts) >= 2:
            pkg = parts[-2]
            new_stem = f"{pkg}_{stem}.py"
            return "/".join(parts[:-1] + [new_stem])
        return file_path

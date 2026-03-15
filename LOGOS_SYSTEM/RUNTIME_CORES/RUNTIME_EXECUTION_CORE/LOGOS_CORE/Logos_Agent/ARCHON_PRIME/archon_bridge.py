"""
ARCHON PRIME BRIDGE ADAPTER
Minimal interface allowing LOGOS runtime to invoke Archon Prime pipelines.

ADAPTATION NOTES (deviations from nominal spec required for correctness)
------------------------------------------------------------------------
1. DEFERRED IMPORT — GOVERNANCE GATE INCOMPATIBILITY
   enforce_runtime_gate() is called at module level inside pipeline_controller.py.
   That gate checks for pre-migration paths at /workspaces/ARCHON_PRIME/ which do
   not exist in the LOGOS environment. It calls sys.exit(1) on any missing
   condition, which would terminate the LOGOS process on import.

   To prevent this, PipelineController is imported lazily inside
   _load_pipeline_controller() and the resulting SystemExit is caught and
   re-raised as ImportError so LOGOS callers receive a meaningful error rather
   than a silent process termination.

   Archon Prime source code is NOT modified. The gate remains intact.
   This adapter absorbs the gate failure at the LOGOS boundary.

2. CONSTRUCTOR ARGUMENT
   PipelineController.__init__ requires root_path: str.
   ARCHON_ROOT from the path bootstrap is supplied as that argument.

3. LAZY PIPELINE INITIALIZATION
   The PipelineController instance is created on first call to
   run_archon_analysis(), not at ArchonBridge construction time, so that
   construction of the bridge object never triggers the gate.
"""

import logging

from .archon_path_bootstrap import ARCHON_ROOT  # ensures sys.path registration

logger = logging.getLogger(__name__)

_PipelineController = None


def _load_pipeline_controller():
    """
    Deferred import of PipelineController with governance gate isolation.

    AP's enforce_runtime_gate() raises SystemExit when AP's runtime
    prerequisites are not satisfied.  That SystemExit is caught here and
    converted to ImportError so LOGOS processes are never terminated by
    an AP gate failure.
    """
    global _PipelineController
    if _PipelineController is not None:
        return _PipelineController

    try:
        from WORKFLOW_MUTATION_TOOLING.controllers.pipeline_controller import (  # noqa: PLC0415
            PipelineController,
        )
        _PipelineController = PipelineController
        logger.info("ArchonBridge: PipelineController loaded successfully.")
        return _PipelineController

    except SystemExit as exc:
        raise ImportError(
            "Archon Prime governance gate blocked PipelineController import. "
            "AP runtime prerequisites (processing directory, execution envelopes, "
            "engagement confirmation) are not satisfied in the current environment. "
            f"Gate exit code: {exc.code}. "
            "Ensure AP's WORKFLOW_TARGET_PROCESSING/PROCESSING and "
            "WORKFLOW_EXECUTION_ENVELOPES/ACTIVE_ENVELOPES directories exist "
            "and contain the required artifacts before invoking the pipeline."
        ) from None


class ArchonBridge:
    """
    Adapter exposing Archon functionality to the LOGOS runtime.
    """

    def __init__(self):
        self.pipeline = None

    def _ensure_pipeline(self) -> None:
        """Lazily initialize the PipelineController on first use."""
        if self.pipeline is None:
            PipelineController = _load_pipeline_controller()
            self.pipeline = PipelineController(root_path=str(ARCHON_ROOT))

    def run_archon_analysis(self, target_path: str):
        """
        Execute Archon analysis pipeline against a target path.
        """
        self._ensure_pipeline()
        return self.pipeline.run_pipeline(target_path)

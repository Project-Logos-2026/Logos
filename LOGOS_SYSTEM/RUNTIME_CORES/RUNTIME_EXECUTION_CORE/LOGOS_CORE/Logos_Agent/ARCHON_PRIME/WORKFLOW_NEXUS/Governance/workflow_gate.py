# ============================================================
# ARCHON PRIME MODULE HEADER
# module_id:            M-083
# module_name:          workflow_gate
# subsystem:            workflow_nexus
# module_role:          utility
# canonical_path:       WORKFLOW_NEXUS/Governance/workflow_gate.py
# responsibility:       Utility module: workflow gate
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
# NOTE: This is the workflow_gate governance module; gate self-call omitted.

# ------------------------------------------------------------
# END ARCHON PRIME MODULE HEADER
# ------------------------------------------------------------

# ============================================================
# ARCHON PRIME GOVERNANCE MODULE
# module_name:          workflow_gate
# subsystem:            workflow_nexus
# responsibility:       fail-closed runtime gate for workflow execution
# authority:            ARCHON_PRIME
# version:              1.0
# status:               canonical
# ============================================================

"""
Workflow Gate

Central governance enforcement module for Archon Prime workflow execution.

All tooling modules call this gate at runtime via header injection.

The gate enforces four conditions:

1. Workflow runtime context exists
2. Execution envelope is present
3. Engagement approval exists
4. Mutation targets are authorized

Failure of any condition immediately halts execution.
"""

import sys
from pathlib import Path

ARCHON_ROOT = Path("/workspaces/ARCHON_PRIME")

PROCESSING_DIR = ARCHON_ROOT / "WORKFLOW_TARGET_PROCESSING" / "PROCESSING"
ENVELOPE_DIR = ARCHON_ROOT / "WORKFLOW_EXECUTION_ENVELOPES" / "ACTIVE_ENVELOPES"
REPORT_DIR = ARCHON_ROOT / "WORKFLOW_TARGET_PROCESSING" / "PROCESSING_REPORTS"


class WorkflowGateError(RuntimeError):
    """Raised when workflow governance rules are violated."""


def _detect_workflow_runtime() -> None:
    """
    Determine whether execution is occurring inside
    an active workflow processing environment.
    """
    if not PROCESSING_DIR.exists():
        raise WorkflowGateError(
            "Workflow runtime invalid: PROCESSING directory missing."
        )


def _detect_execution_envelope() -> None:
    """
    Ensure at least one execution envelope Design Specification exists.
    Envelopes live in subdirectories of ACTIVE_ENVELOPES, so rglob is used.
    """
    if not ENVELOPE_DIR.exists():
        raise WorkflowGateError("Execution envelope directory missing.")

    envelopes = list(ENVELOPE_DIR.rglob("*_DS.md"))
    if not envelopes:
        raise WorkflowGateError("No execution envelope detected.")


def _detect_engagement_approval() -> None:
    """
    Confirm engagement confirmation artifact exists and no denial is present.
    Confirmation artifacts: *_EC.md
    Denial artifacts:       *_ED.md
    """
    if not REPORT_DIR.exists():
        raise WorkflowGateError("Processing report directory missing.")

    denials = list(ENVELOPE_DIR.rglob("*_ED.md"))
    if denials:
        raise WorkflowGateError(
            "Execution denied: engagement denial artifact detected."
        )

    approvals = list(ENVELOPE_DIR.rglob("*_EC.md"))
    if not approvals:
        raise WorkflowGateError("Execution blocked: engagement confirmation missing.")


def _validate_mutation_surface() -> None:
    """
    Ensure mutation operations occur only inside
    the authorized processing surface.
    """
    cwd = Path.cwd().resolve()
    processing_resolved = PROCESSING_DIR.resolve()

    if cwd != processing_resolved and processing_resolved not in cwd.parents:
        raise WorkflowGateError(
            "Mutation attempted outside authorized processing surface."
        )


def enforce_runtime_gate() -> None:
    """
    Primary governance entrypoint invoked by module headers.
    Calls all four gate checks in sequence. Fail-closed on any violation.
    """
    try:
        _detect_workflow_runtime()
        _detect_execution_envelope()
        _detect_engagement_approval()
        _validate_mutation_surface()
    except WorkflowGateError as err:
        print("\nARCHON PRIME WORKFLOW GATE FAILURE\n")
        print(str(err))
        print("\nExecution halted.\n")
        sys.exit(1)

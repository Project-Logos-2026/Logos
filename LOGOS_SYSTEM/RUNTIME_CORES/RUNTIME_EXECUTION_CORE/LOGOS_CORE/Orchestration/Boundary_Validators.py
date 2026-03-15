"""
Boundary Validators for P4.6
Implements LOGOS_V1_P4_Hardening_Validation_Spec.md §7.2–§7.4
"""
from typing import Dict, Any

class RuntimeActivationHalt(Exception):
    """Raised when the runtime spine fails an invariant."""
    pass

class ClassificationError(Exception):
    """Raised when classification ladder is violated."""
    pass

class SMPCreationError(Exception):
    """Raised when SMP boundary is violated."""
    pass

def validate_startup_context(ctx: Dict[str, Any]) -> None:
    """
    Validates LOGOS_AGENT_READY dict shape.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    required_keys = [
        "status", "logos_identity", "logos_session",
        "constructive_compile_output", "agent_orchestration_plan"
    ]
    for key in required_keys:
        if key not in ctx:
            raise RuntimeActivationHalt(f"Missing startup context key: {key}")
    if ctx["status"] != "LOGOS_AGENT_READY":
        raise RuntimeActivationHalt(f"Invalid startup status: {ctx['status']}")
    identity = ctx["logos_identity"]
    if not isinstance(identity.get("logos_agent_id"), str):
        raise RuntimeActivationHalt("logos_agent_id must be string")
    if not isinstance(identity.get("session_id"), str):
        raise RuntimeActivationHalt("session_id must be string")

def validate_task(task: Dict[str, Any]) -> None:
    """
    Validates task dict shape.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    if "task_id" not in task:
        raise ValueError("Task missing required field: task_id")
    if "input" not in task:
        raise ValueError("Task missing required field: input")

def validate_route_packet(packet_payload: Dict[str, Any]) -> None:
    """
    Validates routing StatePacket payload.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    if "type" not in packet_payload:
        raise ValueError("Route packet missing type")
    if "content" not in packet_payload:
        raise ValueError("Route packet missing content")
    if "smp_id" not in packet_payload["content"]:
        raise ValueError("Route packet content missing smp_id")

def validate_tick_result(result: Dict[str, Any]) -> None:
    """
    Validates tick result against P1-IF-07.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    required = ["tick_id", "session_id", "task_id", "status"]
    for key in required:
        if key not in result:
            raise ValueError(f"Tick result missing required field: {key}")
    if result["status"] not in ("completed", "halted", "no_output"):
        raise ValueError(f"Invalid tick result status: {result['status']}")

def validate_agent_write_boundary(smp_id: str, aa_type: str) -> None:
    """
    Validates agent write boundary for AA append.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    if not isinstance(smp_id, str) or not smp_id:
        raise SMPCreationError("smp_id must be non-empty string")
    if not isinstance(aa_type, str) or not aa_type:
        raise SMPCreationError("aa_type must be non-empty string")

def validate_promotion_boundary(current_state: str, target_state: str) -> None:
    """
    Validates promotion boundary for classification ladder.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    if current_state == "canonical":
        raise ClassificationError("Cannot promote canonical SMP")
    allowed_forward = {"rejected", "conditional", "provisional", "canonical"}
    if target_state not in allowed_forward:
        raise ClassificationError(f"Invalid target state: {target_state}")
    # No regression: must move forward only
    ladder = ["rejected", "conditional", "provisional", "canonical"]
    if ladder.index(target_state) < ladder.index(current_state):
        raise ClassificationError("Classification regression not allowed")

def validate_mtp_result(result_obj: Any) -> None:
    """
    Validates MTP result object.
    [Blueprint: LOGOS_V1_P4_Hardening_Validation_Spec.md §7.3]
    """
    if not hasattr(result_obj, "status"):
        raise ValueError("MTP result missing status attribute")
    if not hasattr(result_obj, "emitted_text") or not callable(result_obj.emitted_text):
        raise ValueError("MTP result missing emitted_text() callable")

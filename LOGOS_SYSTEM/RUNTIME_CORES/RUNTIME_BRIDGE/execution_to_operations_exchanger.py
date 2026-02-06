"""
Execution ↔ Operations Exchanger
================================

This module defines the **ExecutionToOperationsExchanger**, a runtime bridge
component that connects the operations side of the Logos runtime (e.g. SOP,
ARP, MTP) with the execution side (the Nexus).  It is responsible for
translating high–level operations into execution‐side state packets and
delivering execution outcomes back to the operations layer.  The bridge enforces
strict structural and causal rules: nothing is emitted until the PXL gate has
discharged, and every operation is paired with exactly one corresponding
execution result.  This ensures that execution and operations remain in
lockstep, preventing orphaned states or unconsumed operations.

Key responsibilities:

* **Operation dispatch** – accept operations from the operations layer and
  forward them into the execution Nexus as state packets.
* **Result ingestion** – listen for execution‐side state packets and deliver
  them back to the operations layer as responses.
* **Bijective mapping enforcement** – use the
  :class:`DualBijectiveCommutationValidator` to guarantee that every
  operation maps to exactly one result and vice versa.
* **PXL gate coordination** – refuse to dispatch any operations until the
  provided PXL gate indicates that runtime initialization has completed.

This module contains only infrastructure.  It does not perform any agent
reasoning, policy enforcement, or persistence decisions.  All authorities
remain on their respective sides of the runtime bifurcation.

"""

from __future__ import annotations

import uuid
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Deque, List
from collections import deque

# Import execution‐side types.  These are defined in the authoritative Nexus
# module.  They are reimported here for type checking and payload
# construction only.
try:
    from Nexus import StatePacket, StandardNexus, NexusParticipant
except ImportError:
    # If Nexus is not available on the import path, define minimal stubs for
    # type checking.  These stubs do not implement any functionality but
    # prevent type errors when this module is imported in isolation.
    @dataclass(frozen=True)
    class StatePacket:  # pragma: no cover
        source_id: str
        payload: Dict[str, object]
        timestamp: float
        causal_intent: Optional[str] = None

    class NexusParticipant:  # pragma: no cover
        participant_id: str
        def register(self, nexus_handle: object) -> None:
            raise NotImplementedError
        def project_state(self) -> Optional[StatePacket]:
            raise NotImplementedError
        def receive_state(self, packet: StatePacket) -> None:
            raise NotImplementedError
        def execute_tick(self, context: Dict[str, object]) -> None:
            raise NotImplementedError

    class StandardNexus:  # pragma: no cover
        pass

from dual_bijective_commutation_validator import (
    DualBijectiveCommutationValidator,
)


class PXLGate:
    """
    Simple stub representing the PXL discharge gate.

    In a complete implementation, this class would communicate with the
    physical/virtual proof gate responsible for ensuring that all runtime
    prerequisites (proof validation, compilation phases, etc.) have completed
    before operations can be dispatched.  Here we expose a minimal API that
    callers can use to check readiness.
    """

    def __init__(self) -> None:
        self._discharged: bool = False

    def discharge(self) -> None:
        """Mark the gate as discharged.  Once called, the gate remains
        discharged for the lifetime of the process."""
        self._discharged = True

    def is_discharged(self) -> bool:
        """Return ``True`` if the gate has been discharged."""
        return self._discharged


@dataclass
class OperationRequest:
    """
    Data class representing a high–level operation originating from the
    operations layer.  Each operation must carry a unique identifier so that
    responses can be correlated.  The ``type`` field denotes the kind of
    operation being performed (e.g. "compile", "persist"), while the
    ``content`` field holds the operation's payload.
    """

    op_id: str
    type: str
    content: Dict[str, object]
    causal_intent: Optional[str] = None


@dataclass
class OperationResponse:
    """
    Data class representing the result of an executed operation.  The
    ``op_id`` field matches the originating operation, the ``type`` field
    mirrors that of the request for traceability, and the ``content`` field
    contains whatever output the execution side produced.
    """

    op_id: str
    type: str
    content: Dict[str, object]


class ExecutionToOperationsExchanger(NexusParticipant):
    """
    Bridge participant responsible for translating operations into execution
    requests and delivering execution results back to the operations layer.

    This class implements the :class:`NexusParticipant` protocol so that it
    can be registered with a :class:`StandardNexus`.  It maintains an
    internal queue of pending operations.  On each execution tick, if the
    PXL gate has discharged, it emits the next operation as a state packet
    through the Nexus handle.  When it receives state packets from other
    participants, it inspects them for an ``operation_id`` field; if present,
    it treats the packet as the result of a previously queued operation.
    """

    participant_id = "RuntimeBridge"

    def __init__(
        self,
        operations_consumer: Callable[[OperationResponse], None],
        validator: Optional[DualBijectiveCommutationValidator] = None,
        gating: Optional[PXLGate] = None,
    ) -> None:
        """
        Create a new runtime bridge.

        Args:
            operations_consumer: A callback invoked whenever a completed
                operation response is ready to be consumed by the operations
                layer.  This callback should accept a single
                :class:`OperationResponse` argument.
            validator: Optional instance of
                :class:`DualBijectiveCommutationValidator`.  If provided, it
                will be used to enforce bijective mappings between operations
                and execution results.  If omitted, a new validator will be
                created automatically.
            gating: Optional PXL gate instance.  If provided, operations will
                not be dispatched until ``gating.is_discharged()`` returns
                ``True``.
        """
        self.operations_consumer = operations_consumer
        self.validator = validator or DualBijectiveCommutationValidator()
        self.gating = gating or PXLGate()
        self._pending_operations: Deque[OperationRequest] = deque()
        self._handle: Optional[object] = None

    # ------------------------------------------------------------------
    # NexusParticipant interface
    # ------------------------------------------------------------------

    def register(self, nexus_handle: object) -> None:
        """
        Register the runtime bridge with the execution nexus.  The nexus
        provides a handle through which state packets can be emitted.  This
        method is called automatically by the nexus during participant
        registration.
        """
        self._handle = nexus_handle

    def execute_tick(self, context: Dict[str, object]) -> None:
        """
        Called on each nexus tick.  If the PXL gate has discharged and there
        is at least one pending operation, emit the next operation as a state
        packet via the nexus handle.  Each emitted packet includes the
        operation's unique identifier so that the corresponding result can be
        correlated later.
        """
        if not self._handle:
            # If we have not been registered yet, do nothing.
            return

        # Only dispatch operations after the PXL gate is ready.
        if not self.gating.is_discharged():
            return

        if not self._pending_operations:
            return

        # Pop one operation off the queue and emit it.
        op_request = self._pending_operations.popleft()
        # Record the operation ID with the validator before dispatch.
        self.validator.register_operation(op_request.op_id)
        payload: Dict[str, object] = {
            "type": op_request.type,
            "content": op_request.content,
            "operation_id": op_request.op_id,
        }
        # The causal intent (if provided) is used to annotate the state
        # packet.  This allows downstream participants to correlate causal
        # chains through the runtime.
        self._handle.emit(payload, causal_intent=op_request.causal_intent)

    def receive_state(self, packet: StatePacket) -> None:
        """
        Receive a state packet from another nexus participant.  If the packet
        includes an ``operation_id`` field, treat it as the result of a
        previously dispatched operation.  Validate the bijection, record the
        mapping, and forward the result back to the operations consumer.
        """
        # Extract the operation identifier from the payload, if present.
        op_id = packet.payload.get("operation_id")
        if not op_id:
            # This packet is not related to an operation dispatched by the
            # bridge, so ignore it.
            return

        # Generate a unique state identifier for bijection tracking.  If the
        # execution side has provided a state identifier, use it; otherwise
        # synthesize one from the timestamp and source ID.
        state_id: str = (
            packet.payload.get("state_id")
            or packet.payload.get("result_id")
            or f"{packet.source_id}:{packet.timestamp}"
        )

        # Record the mapping between the operation and the state.  This will
        # raise if the mapping is invalid (e.g. duplicate assignments).
        self.validator.assign_state(op_id, state_id)

        # Construct an OperationResponse object.  The response mirrors the
        # operation type for clarity and includes the raw payload content.
        op_response = OperationResponse(
            op_id=op_id,
            type=packet.payload.get("type", ""),
            content=packet.payload.get("content", {}),
        )

        # Deliver the response back to the operations layer via the
        # user-provided callback.  The consumer is responsible for any
        # further handling, including policy enforcement or persistence.
        try:
            self.operations_consumer(op_response)
        except Exception as exc:
            # Do not let consumer exceptions propagate into the runtime loop.
            # Log them or rewrap as needed.
            raise RuntimeError(f"Operations consumer raised an exception: {exc}")

    def project_state(self) -> Optional[StatePacket]:
        """
        The runtime bridge does not project its own state into the nexus.
        It returns ``None`` here, indicating that no additional state
        packets should be enqueued at the end of the tick.
        """
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def queue_operation(
        self,
        op_type: str,
        content: Dict[str, object],
        *,
        causal_intent: Optional[str] = None,
    ) -> str:
        """
        Enqueue a new operation for dispatch.  This method can be called by
        the operations layer at any time.  If the PXL gate has not yet
        discharged, the operation will remain queued until it is safe to
        dispatch.

        Args:
            op_type: Human-readable operation type (e.g. "compile", "persist").
            content: Arbitrary payload describing the operation.
            causal_intent: Optional string used to annotate the emitted
                state packet with a causal context.  Downstream participants
                may choose to propagate or interpret this value.

        Returns:
            The unique identifier assigned to the queued operation.  This
            identifier can be used to correlate future results.
        """
        op_id = str(uuid.uuid4())
        op_request = OperationRequest(
            op_id=op_id,
            type=op_type,
            content=content,
            causal_intent=causal_intent,
        )
        self._pending_operations.append(op_request)
        return op_id

    def pending_operations(self) -> List[str]:
        """
        Return a list of operation identifiers that are currently queued but
        have not yet been dispatched.  This can be used for introspection
        during audits or unit tests.
        """
        return [op.op_id for op in list(self._pending_operations)]
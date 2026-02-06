"""
Dual Bijective Commutation Validator
====================================

This module defines a utility class used by the runtime bridge to enforce a
strict one-to-one correspondence between operations and execution results.  In
the Logos runtime, every operation emitted by the operations side must
eventually produce exactly one result packet from the execution side.  This
bijective mapping is critical for auditability and causality: if multiple
results are linked to the same operation, or if a result is produced with no
corresponding operation, it indicates a severe integrity violation.

The **DualBijectiveCommutationValidator** class maintains two dictionaries
tracking operations and state packets.  When an operation is registered, it
must not already exist in the mapping.  When a state packet is assigned to
an operation, both the operation and the state must be previously unbound.
If any of these invariants are violated, a ``RuntimeError`` is raised.

This validator does not perform any semantic checks on the contents of
operations or states; it only guarantees referential integrity.  Higher‐level
policy enforcement belongs elsewhere in the runtime.
"""

from typing import Dict, Optional


class DualBijectiveCommutationValidator:
    """Enforce bijective mapping between operation identifiers and state identifiers."""

    def __init__(self) -> None:
        # Maps operation IDs to their corresponding state IDs.  A value of
        # ``None`` indicates that the operation has been registered but has
        # not yet received a result.
        self._operation_to_state: Dict[str, Optional[str]] = {}
        # Reverse mapping from state IDs to operation IDs.  Once populated,
        # every state ID must map to exactly one operation ID.
        self._state_to_operation: Dict[str, str] = {}

    def register_operation(self, op_id: str) -> None:
        """Register a new operation identifier.

        Args:
            op_id: The unique identifier of the operation being registered.

        Raises:
            RuntimeError: If the operation has already been registered.
        """
        if op_id in self._operation_to_state:
            raise RuntimeError(f"Operation '{op_id}' is already registered")
        self._operation_to_state[op_id] = None

    def assign_state(self, op_id: str, state_id: str) -> None:
        """
        Record the association between an operation and a state.

        This method is called when the runtime bridge receives a result from
        the execution side.  It ensures that:

        * The operation has been previously registered via
          :meth:`register_operation`.
        * The operation has not already been assigned a state.
        * The state has not already been assigned to another operation.

        Args:
            op_id: The operation identifier to assign.
            state_id: The state identifier corresponding to the result.

        Raises:
            RuntimeError: If any bijection invariant is violated.
        """
        if op_id not in self._operation_to_state:
            raise RuntimeError(f"Unknown operation '{op_id}' cannot be assigned a state")
        if self._operation_to_state[op_id] is not None:
            existing_state = self._operation_to_state[op_id]
            raise RuntimeError(
                f"Operation '{op_id}' is already mapped to state '{existing_state}'"
            )
        if state_id in self._state_to_operation:
            existing_op = self._state_to_operation[state_id]
            raise RuntimeError(
                f"State '{state_id}' is already mapped to operation '{existing_op}'"
            )
        # Record the mapping in both directions.
        self._operation_to_state[op_id] = state_id
        self._state_to_operation[state_id] = op_id

    def operation_state(self, op_id: str) -> Optional[str]:
        """Return the state identifier associated with the given operation, or ``None``.

        Args:
            op_id: The operation identifier to look up.

        Returns:
            The associated state identifier, or ``None`` if the operation has not
            yet received a result.
        """
        return self._operation_to_state.get(op_id)

    def state_operation(self, state_id: str) -> Optional[str]:
        """
        Return the operation identifier associated with the given state, or
        ``None`` if the state has not been assigned.

        Args:
            state_id: The state identifier to look up.

        Returns:
            The associated operation identifier, or ``None`` if unassigned.
        """
        return self._state_to_operation.get(state_id)

    def validate_bijection(self) -> None:
        """
        Validate that the operation→state and state→operation mappings are
        perfectly bijective.  Raises a ``RuntimeError`` if any mapping is
        incomplete or inconsistent.  This method can be called during audits
        or shutdown to verify the integrity of the runtime bridge.
        """
        # Every registered operation must have a state assigned.
        for op_id, state_id in self._operation_to_state.items():
            if state_id is None:
                raise RuntimeError(f"Operation '{op_id}' has no assigned state")
            # Ensure reverse mapping exists and is correct.
            if self._state_to_operation.get(state_id) != op_id:
                raise RuntimeError(
                    f"Bijective violation: operation '{op_id}' → state '{state_id}',"
                    f" but reverse mapping is '{self._state_to_operation.get(state_id)}'"
                )
        # Every state must map back to exactly one operation.
        for state_id, op_id in self._state_to_operation.items():
            if self._operation_to_state.get(op_id) != state_id:
                raise RuntimeError(
                    f"Bijective violation: state '{state_id}' → operation '{op_id}',"
                    f" but forward mapping is '{self._operation_to_state.get(op_id)}'"
                )
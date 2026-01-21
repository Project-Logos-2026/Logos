"""
Governance Exceptions

Typed, auditable denial surfaces used across governance layers.
Defining exceptions here introduces no runtime behavior changes.
"""


class GovernanceDenied(Exception):
    """
    Raised when an action is explicitly denied by governance policy.

    Semantics:
    - Deterministic
    - Fail-closed
    - Non-recoverable without explicit authorization
    """

    pass

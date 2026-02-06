"""Hash validation stubs for SOP boot-time checks."""

from __future__ import annotations

from typing import Dict


def validate_kernel_hash(expected: str, actual: str) -> Dict[str, object]:
    """Validate the kernel hash with a fail-closed default."""

    if not expected or not actual:
        return {"ok": False, "reason": "missing_hash", "expected": expected, "actual": actual}
    if expected != actual:
        return {"ok": False, "reason": "hash_mismatch", "expected": expected, "actual": actual}
    return {"ok": True, "reason": "hash_match", "expected": expected, "actual": actual}


def validate_identity_hash(expected: str, actual: str) -> Dict[str, object]:
    """Validate the identity hash with a fail-closed default."""

    return validate_kernel_hash(expected, actual)

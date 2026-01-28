"""
A3 Authorization Gate — Deny by Default (validation + deny-by-default signature)

Purpose:
- Enforce that autonomous execution is denied unless a valid A3 authorization artifact is present.
- This module does NOT enable autonomy; it fails closed on any issue.
- Adds validation for required fields, expiry, and pluggable signature check that denies by default.
"""

from datetime import datetime, timezone
from typing import Optional

try:
    from .crypto.signature_verifier import SignatureVerifier, SignatureVerificationDenied
except Exception:
    class SignatureVerificationDenied(Exception):
        pass

    class SignatureVerifier:
        def verify(self, artifact: dict) -> None:
            raise SignatureVerificationDenied(
                "Signature verification unavailable; denied by default."
            )


class A3AuthorizationDenied(Exception):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_utc(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        raise A3AuthorizationDenied("Invalid UTC timestamp format.")


def _basic_schema_check(artifact: dict) -> None:
    required = {
        "artifact_type",
        "issuer",
        "issued_at_utc",
        "expires_at_utc",
        "scope",
        "bounds",
        "revocable",
        "audit",
        "signature",
    }
    missing = required - set(artifact.keys())
    if missing:
        raise A3AuthorizationDenied(f"Missing required fields: {sorted(missing)}")


def _expiry_check(artifact: dict) -> None:
    now = _utcnow()
    issued = _parse_utc(artifact["issued_at_utc"])
    expires = _parse_utc(artifact["expires_at_utc"])

    if issued > now:
        raise A3AuthorizationDenied("Authorization artifact not yet valid.")

    if expires <= now:
        raise A3AuthorizationDenied("Authorization artifact expired.")


def _signature_stub_check(artifact: dict) -> None:
    sig = artifact.get("signature", {})
    if not isinstance(sig, dict):
        raise A3AuthorizationDenied("Invalid signature block.")

    # Stub only: cryptographic verification deferred until explicitly approved.
    if "alg" not in sig or "value" not in sig:
        raise A3AuthorizationDenied("Incomplete signature block.")


def _verify_signature(artifact: dict) -> None:
    try:
        SignatureVerifier().verify(artifact)
    except SignatureVerificationDenied as exc:
        raise A3AuthorizationDenied(str(exc))


def check_a3_authorization(artifact: Optional[dict]) -> None:
    """
    Deny-by-default A3 authorization gate.
    Raises A3AuthorizationDenied on any failure. No side effects. No enablement.
    """
    if artifact is None:
        raise A3AuthorizationDenied("A3 authorization artifact missing.")

    if artifact.get("artifact_type") != "A3_DELEGATED_AUTONOMY_AUTHORIZATION":
        raise A3AuthorizationDenied("Invalid artifact type.")

    if artifact.get("revocable") is not True:
        raise A3AuthorizationDenied("Artifact must be explicitly revocable.")

    _basic_schema_check(artifact)
    _expiry_check(artifact)
    _signature_stub_check(artifact)
    _verify_signature(artifact)

    # All checks passed; permission is still NOT granted here.
    return

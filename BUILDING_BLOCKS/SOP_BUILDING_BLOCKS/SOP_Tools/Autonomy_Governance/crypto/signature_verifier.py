"""
Signature Verification Interface — DENY BY DEFAULT

Purpose:
- Define a pluggable interface for verifying A3 authorization signatures.
- This implementation trusts NO keys and verifies NOTHING.
- All calls deny unless explicitly replaced with an approved verifier.

Security posture:
- Fail closed
- Non-enabling
"""


class SignatureVerificationDenied(Exception):
    pass


class SignatureVerifier:
    """
    Interface for signature verification.
    """

    def verify(self, artifact: dict) -> None:
        """
        Verify the signature on an authorization artifact.

        MUST raise SignatureVerificationDenied on failure.
        MUST return None on success.

        Default behavior: always deny.
        """
        raise SignatureVerificationDenied(
            "No signature verifier installed; verification denied by default."
        )

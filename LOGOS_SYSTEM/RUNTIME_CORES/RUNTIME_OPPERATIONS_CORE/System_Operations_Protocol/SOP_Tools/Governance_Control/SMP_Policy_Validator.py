"""
SOP Governance Control — SMP Policy Validator (Hardened)
"""

import json
import hashlib


class SMPPolicyValidator:

    @staticmethod
    def canonical_hash(payload: dict) -> str:
        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":")
        )
        return hashlib.sha256(serialized.encode()).hexdigest()

    @staticmethod
    def verify_hash(payload: dict, provided_hash: str):
        calculated = SMPPolicyValidator.canonical_hash(payload)
        if calculated != provided_hash:
            raise RuntimeError("[FAIL-CLOSED] SMP hash mismatch.")

    @staticmethod
    def enforce_zero_trust(origin: str):
        if origin == "P1":
            return "ZERO_TRUST_CLASSIFIED"
        return "INTERNAL"

    @staticmethod
    def validate_smp(smp: dict):
        required = ["origin", "payload", "hash", "phase"]
        for field in required:
            if field not in smp:
                raise RuntimeError(f"[FAIL-CLOSED] Missing SMP field: {field}")

        SMPPolicyValidator.verify_hash(
            smp["payload"],
            smp["hash"]
        )

        return SMPPolicyValidator.enforce_zero_trust(smp["origin"])

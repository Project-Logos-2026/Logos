"""
SOP Governance Control — Invariant Enforcer (Attestation Hardened)
Fail-Closed Default
"""

import os
import json
import hashlib
from datetime import datetime


class InvariantEnforcer:

    DRAC_INVARIANT_PATH = (
        "LOGOS_SYSTEM/RUNTIME_CORES/"
        "RUNTIME_OPPERATIONS_CORE/"
        "Dynamic_Reconstruction_Adaptive_Compilation_Protocol/"
        "DRAC_Core/DRAC_Assembly_Invariants.md"
    )

    ATTESTATION_PATH = (
        "_Governance/Attestations/"
        "DRAC_Assembly_Invariants_Attestation.json"
    )

    @staticmethod
    def file_hash(path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    @classmethod
    def _write_attestation(cls, hash_value: str):
        record = {
            "Artifact": "DRAC_Assembly_Invariants.md",
            "Hash_Model": "SHA-256",
            "Canonical_Hash": hash_value,
            "Last_Attested_UTC": datetime.utcnow().isoformat(),
            "Attested_By": "BOOTSTRAP_MODE"
        }
        with open(cls.ATTESTATION_PATH, "w") as f:
            json.dump(record, f, indent=2)

    @classmethod
    def enforce(cls):

        if not os.path.exists(cls.DRAC_INVARIANT_PATH):
            raise RuntimeError("[FAIL-CLOSED] DRAC invariant file missing.")

        live_hash = cls.file_hash(cls.DRAC_INVARIANT_PATH)

        if not os.path.exists(cls.ATTESTATION_PATH):
            if os.getenv("BOOTSTRAP_ALLOW_NEW_INVARIANT") == "true":
                cls._write_attestation(live_hash)
                return live_hash
            else:
                raise RuntimeError(
                    "[FAIL-CLOSED] No invariant attestation found."
                )

        with open(cls.ATTESTATION_PATH, "r") as f:
            record = json.load(f)

        stored_hash = record.get("Canonical_Hash")

        if stored_hash != live_hash:
            raise RuntimeError(
                "[FAIL-CLOSED] DRAC invariant drift detected."
            )

        return live_hash

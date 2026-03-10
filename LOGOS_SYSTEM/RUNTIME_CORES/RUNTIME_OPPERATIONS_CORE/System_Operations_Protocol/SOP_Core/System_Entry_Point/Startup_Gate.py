"""
SOP System Entry Point — Startup Gate (Attestation Enforced)
"""

import os
import hashlib
from datetime import datetime

from logos.imports.governance import InvariantEnforcer


class StartupGate:

    REQUIRED_DIRECTORIES = [
        "LOGOS_SYSTEM",
        "_Reports",
        "LOGOS_EXTERNALIZATION"
    ]

    @staticmethod
    def verify_directories():
        for directory in StartupGate.REQUIRED_DIRECTORIES:
            if not os.path.exists(directory):
                raise RuntimeError(f"[FAIL-CLOSED] Missing required directory: {directory}")

    @staticmethod
    def attest_environment():
        fingerprint = hashlib.sha256(
            str(datetime.utcnow()).encode()
        ).hexdigest()
        return fingerprint

    @classmethod
    def boot(cls):
        cls.verify_directories()
        InvariantEnforcer.enforce()
        return cls.attest_environment()

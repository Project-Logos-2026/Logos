"""
DRAC Orchestration Bridge
Converts authorized compile request into DRAC compile intent.
No runtime execution occurs here.
Fail-Closed.
"""

import hashlib
import os
import time


class DRACOrchestrationBridge:

    CANONICAL_CORE_PATH = (
        "LOGOS_SYSTEM/RUNTIME_CORES/"
        "RUNTIME_OPPERATIONS_CORE/"
        "Dynamic_Reconstruction_Adaptive_Compilation_Protocol/"
        "DRAC_Core/Documentation/Canonical_FunctionBlockCores.json"
    )

    @staticmethod
    def _manifest_snapshot_hash():
        if not os.path.exists(DRACOrchestrationBridge.CANONICAL_CORE_PATH):
            raise RuntimeError("[FAIL-CLOSED] Canonical core manifest missing.")

        with open(DRACOrchestrationBridge.CANONICAL_CORE_PATH, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    @classmethod
    def build_compile_intent(cls, authorization: dict):

        manifest_hash = cls._manifest_snapshot_hash()

        return {
            "compile_intent": True,
            "core": authorization["core"],
            "phase": authorization["phase"],
            "trust_level": authorization["trust_level"],
            "manifest_snapshot_hash": manifest_hash,
            "timestamp": time.time(),
        }

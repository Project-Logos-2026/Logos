"""
Validates that requested Core_Block_ID exists in canonical manifest.
"""

import json
import os


class CoreBindingValidator:

    CANONICAL_CORE_PATH = (
        "LOGOS_SYSTEM/RUNTIME_CORES/"
        "RUNTIME_OPPERATIONS_CORE/"
        "Dynamic_Reconstruction_Adaptive_Compilation_Protocol/"
        "DRAC_Core/Documentation/Canonical_FunctionBlockCores.json"
    )

    @classmethod
    def validate(cls, core_id: str):

        if not os.path.exists(cls.CANONICAL_CORE_PATH):
            raise RuntimeError("[FAIL-CLOSED] Canonical core manifest missing.")

        with open(cls.CANONICAL_CORE_PATH, "r") as f:
            data = json.load(f)

        valid_ids = {entry["Core_Block_ID"] for entry in data.get("FunctionBlockCores", [])}

        if core_id not in valid_ids:
            raise RuntimeError(f"[FAIL-CLOSED] Unknown Core_Block_ID: {core_id}")

        return True

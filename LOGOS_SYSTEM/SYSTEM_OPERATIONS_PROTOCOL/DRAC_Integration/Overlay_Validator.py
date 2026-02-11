"""
Validates overlays are permitted for given Core_Block_ID.
"""

import json
import os


class OverlayValidator:

    CANONICAL_CORE_PATH = (
        "LOGOS_SYSTEM/RUNTIME_CORES/"
        "RUNTIME_OPPERATIONS_CORE/"
        "Dynamic_Reconstruction_Adaptive_Compilation_Protocol/"
        "DRAC_Core/Documentation/Canonical_FunctionBlockCores.json"
    )

    @classmethod
    def validate(cls, core_id: str, overlays: list):

        if not os.path.exists(cls.CANONICAL_CORE_PATH):
            raise RuntimeError("[FAIL-CLOSED] Canonical core manifest missing.")

        with open(cls.CANONICAL_CORE_PATH, "r") as f:
            data = json.load(f)

        for entry in data.get("FunctionBlockCores", []):
            if entry["Core_Block_ID"] == core_id:
                allowed = set(entry.get("Allowed_Overlays", []))
                for overlay in overlays:
                    if overlay not in allowed:
                        raise RuntimeError(
                            f"[FAIL-CLOSED] Overlay {overlay} not allowed for {core_id}"
                        )
                return True

        raise RuntimeError("[FAIL-CLOSED] Core not found during overlay validation.")

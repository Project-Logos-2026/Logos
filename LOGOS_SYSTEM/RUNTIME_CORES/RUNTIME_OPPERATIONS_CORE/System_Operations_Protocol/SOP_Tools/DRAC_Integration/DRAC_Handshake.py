"""
DRAC Handshake Layer (Expanded)
Adds:
- Policy metadata
- Phase enforcement
- Quota enforcement
Fail-Closed
"""

import time

from logos.imports.governance import SOPPolicyMatrix
from logos.imports.governance import CompileQuotaGuard
from logos.imports.governance import CoreBindingValidator
from logos.imports.governance import OverlayValidator


class DRACHandshake:

    @staticmethod
    def authorize(request: dict):

        # Policy check + metadata return
        policy_meta = SOPPolicyMatrix.evaluate(request)

        # Quota enforcement
        CompileQuotaGuard.enforce()

        # Core binding validation
        CoreBindingValidator.validate(request["Core_Block_ID"])

        # Overlay validation
        OverlayValidator.validate(request["Core_Block_ID"], request["Overlays"])

        return {
            "status": "AUTHORIZED_FOR_COMPILE",
            "core": request["Core_Block_ID"],
            "phase": policy_meta["phase_validated"],
            "trust_level": policy_meta["trust_level"],
            "timestamp": time.time(),
        }

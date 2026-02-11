"""
DRAC Handshake Layer (Expanded)
Adds:
- Policy metadata
- Phase enforcement
- Quota enforcement
Fail-Closed
"""

import time

from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.Policy_Matrix.SOP_Policy_Matrix import (
    SOPPolicyMatrix,
)
from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.Policy_Matrix.Compile_Quota_Guard import (
    CompileQuotaGuard,
)
from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.DRAC_Integration.Core_Binding_Validator import (
    CoreBindingValidator,
)
from LOGOS_SYSTEM.SYSTEM_OPERATIONS_PROTOCOL.DRAC_Integration.Overlay_Validator import (
    OverlayValidator,
)


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

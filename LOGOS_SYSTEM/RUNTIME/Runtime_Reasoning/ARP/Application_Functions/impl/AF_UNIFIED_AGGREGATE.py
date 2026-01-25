# ============================================================================
# LOGOS SYSTEM — APPLICATION FUNCTION (DESIGN-ONLY)
# ============================================================================
# Function:          ${af}
# Layer:             ARP — Application Function
# Posture:           Design-only, deny-by-default
# Authority:         None
# Autonomy:          Forbidden
# Proof Projection:  Not authorized
#
# Description:
#   Governed application-function container.
#   This file defines the only legal surface for future logic.
#
# Constraints:
#   - No logic permitted
#   - No execution permitted
#   - Enforced by Runtime_Control
# ============================================================================

def invoke(*args, **kwargs):
    raise NotImplementedError(
        "Design-only stub. Implementation is not authorized."
    )

"""
Radial_Genesis_Engine - RGE_Packet_Types
Enumeration of packet type identifiers for the RGE recursion field.

Passive schema definition only. No routing logic, no reasoning logic.
Reference: RGE_Design_Spec.md Section 3; RGE_Implementation_Guide.md Stage 3
"""

from enum import Enum


class RGEPacketType(str, Enum):
    PROOF_FRAGMENT = "proof_fragment"
    SEMANTIC_FRAGMENT = "semantic_fragment"
    TELEMETRY_SIGNAL = "telemetry_signal"
    CONFIGURATION_PROPOSAL = "configuration_proposal"
    IEL_OVERLAY = "iel_overlay"
    COGNITION_SIGNAL = "cognition_signal"

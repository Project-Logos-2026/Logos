"""
Governance Policy Checks (Phase-J, minimal)

Read-only helpers to validate explicit authorization.
No runtime enablement occurs here.
"""

from Logos_System.Governance.exceptions import GovernanceDenied


def require_multi_tick_policy(policy: dict):
    if not isinstance(policy, dict):
        raise GovernanceDenied("Missing multi-tick policy")

    if policy.get("authorized") is not True:
        raise GovernanceDenied("Multi-tick not authorized")

    max_ticks = policy.get("max_ticks")
    if not isinstance(max_ticks, int) or max_ticks <= 0:
        raise GovernanceDenied("Invalid max_ticks in policy")

    return max_ticks

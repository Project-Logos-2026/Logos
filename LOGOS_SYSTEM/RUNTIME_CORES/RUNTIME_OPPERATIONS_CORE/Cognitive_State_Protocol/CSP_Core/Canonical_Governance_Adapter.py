# ===============================================================================
# LOGOS SYSTEM — CANONICAL GOVERNANCE ADAPTER
# -------------------------------------------------------------------------------
# Phase: P2.4 — Canonical Governance Adapter (Step 1)
# File: Canonical_Governance_Adapter.py
# Location: LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/Cognitive_State_Protocol/CSP_Core/
# Description: Provides a read-only adapter for canonical governance state access.
# Author: Project-Logos-2026
# Date: 2026-03-03
# -------------------------------------------------------------------------------
# DO NOT IMPLEMENT WRITE METHODS OR EXPOSE INTERNAL REFERENCES
# ===============================================================================



from typing import Optional, List, TYPE_CHECKING
import copy

from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_OPPERATIONS_CORE.\
Cognitive_State_Protocol.CSP_Core.CSP_Canonical_Store import CSPCanonicalStore

if TYPE_CHECKING:
    from typing import Any as SMP  # Forward reference only for type hints

class CanonicalGovernanceAdapter:
    def __init__(self, canonical_store: CSPCanonicalStore):
        self.__canonical_store = canonical_store

    def get_canonical(self, csmp_id: str) -> Optional["SMP"]:
        smp = self.__canonical_store.get(csmp_id)
        if smp is None:
            return None
        return copy.deepcopy(smp)

    def list_canonical_ids(self) -> List[str]:
        canonical_objects = self.__canonical_store.list_all()
        ids = []
        for obj in canonical_objects:
            smp_id = getattr(obj, "smp_id", None)
            if smp_id is None:
                raise AttributeError("Canonical SMP missing required attribute 'smp_id'")
            ids.append(smp_id)
        return sorted(ids)

    def count(self) -> int:
        return self.__canonical_store.count()

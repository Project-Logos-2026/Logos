# RGE_Governance_Context.py
# Provides governance context for RGERuntime emission (status_context, parent_hash_reference, router)

from typing import Optional

class RGEGovernanceContext:
    def __init__(self, status_context: str, parent_hash_reference: str, router):
        self.status_context = status_context
        self.parent_hash_reference = parent_hash_reference
        self.router = router

    def get_status_context(self) -> str:
        return self.status_context

    def get_parent_hash_reference(self) -> str:
        return self.parent_hash_reference

    def get_router(self):
        return self.router

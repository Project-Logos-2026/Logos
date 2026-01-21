"""
PACKAGE: Unified_Working_Memory
STATUS: STRUCTURAL STUB (UWM PHASE-INCOMPLETE)

Purpose:
Defines the minimal public surface for Unified Working Memory (UWM)
expected by tests and protocol wiring.

No persistence, recall, or governance logic is implemented.
"""

__all__ = [
    "UWMContext",
    "UWMStore",
    "read",
    "write",
]


class UWMContext:
    def __init__(self, *args, **kwargs):
        pass


class UWMStore:
    def __init__(self, *args, **kwargs):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value


def read(*args, **kwargs):
    raise NotImplementedError("UWM.read is not implemented (stub).")


def write(*args, **kwargs):
    raise NotImplementedError("UWM.write is not implemented (stub).")

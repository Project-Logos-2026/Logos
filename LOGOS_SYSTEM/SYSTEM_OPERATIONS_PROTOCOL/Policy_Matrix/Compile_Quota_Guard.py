"""
Compile Quota Guard
Simple in-memory rate limiter (Phase 1 implementation)
Fail-Closed
"""

import time


class CompileQuotaGuard:

    MAX_COMPILES_PER_MINUTE = 20
    _timestamps = []

    @classmethod
    def enforce(cls):

        now = time.time()

        # Drop timestamps older than 60 seconds
        cls._timestamps = [t for t in cls._timestamps if now - t < 60]

        if len(cls._timestamps) >= cls.MAX_COMPILES_PER_MINUTE:
            raise RuntimeError("[FAIL-CLOSED] Compile quota exceeded.")

        cls._timestamps.append(now)
        return True

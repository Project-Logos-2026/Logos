"""
SOP Audit Spine — Hash-Chained Audit Logger
"""

import json
import hashlib
import os
from datetime import datetime


class AuditLogger:

    LOG_PATH = "_Reports/SOP_Audit_Log.jsonl"

    @staticmethod
    def _canonical_hash(data: dict) -> str:
        serialized = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":")
        )
        return hashlib.sha256(serialized.encode()).hexdigest()

    @classmethod
    def _get_previous_hash(cls):
        if not os.path.exists(cls.LOG_PATH):
            return "GENESIS"

        with open(cls.LOG_PATH, "rb") as f:
            lines = f.readlines()
            if not lines:
                return "GENESIS"
            last = json.loads(lines[-1])
            return last.get("event_hash", "GENESIS")

    @classmethod
    def log(cls, event: dict):
        event["timestamp"] = datetime.utcnow().isoformat()
        event["previous_hash"] = cls._get_previous_hash()

        event_hash = cls._canonical_hash(event)
        event["event_hash"] = event_hash

        with open(cls.LOG_PATH, "a") as f:
            f.write(json.dumps(event) + "\n")

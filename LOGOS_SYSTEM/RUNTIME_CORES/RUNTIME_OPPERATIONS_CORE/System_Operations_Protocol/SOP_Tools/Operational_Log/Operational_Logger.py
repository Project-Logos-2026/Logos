"""
HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
AUTHORITY: LOGOS_SYSTEM
GOVERNANCE: ENABLED
EXECUTION: CONTROLLED
MUTABILITY: IMMUTABLE_LOGIC
VERSION: 1.0.0

LOGOS_MODULE_METADATA
---------------------
module_name: Operational_Logger
runtime_layer: SOP_Tools
role: Operational logging subsystem
agent_binding: None
protocol_binding: None
runtime_classification: runtime_module
boot_phase: v1_startup_migration
expected_imports: [os, json, uuid, time, typing, enum]
provides: [Operational_Logger, Channel, Severity, canonical_json]
depends_on_runtime_state: False
failure_mode:
  type: fail-open
  notes: "Ratified per _Governance/Contracts/Section_10_Fail_Open_Exception_Ratification.md"
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import os
import json
import uuid
import time
from typing import Optional, Dict, Any
from enum import Enum


class Channel(Enum):
    STARTUP = "STARTUP"
    SOP = "SOP"
    GOVERNANCE = "GOVERNANCE"
    AGENT = "AGENT"
    PROTOCOL = "PROTOCOL"
    BRIDGE = "BRIDGE"
    MEMORY = "MEMORY"
    COMPILER = "COMPILER"
    EXTERNALIZATION = "EXTERNALIZATION"


class Severity(Enum):
    HALT = 0
    ERROR = 1
    WARN = 2
    STATUS = 3
    TRACE = 4


_ALLOWED_OPTIONAL = {
    "tick_number",
    "agent_id",
    "protocol_id",
    "module_path",
    "error_type",
    "error_detail",
    "correlation_id",
    "detail",
}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class Operational_Logger:
    """
    Non-authoritative operational logging subsystem.
    Domain: Operational Memory (SOP-owned).
    Spec: Governance_Log_Spec_v1.
    Ratification: Section_10_Fail_Open_Exception_Ratification.md.

    This logger:
    - Is append-only.
    - Carries no authority.
    - Cannot influence execution.
    - Exposes no read API.
    - Must not mutate configuration, governance, or execution state.
    """

    def __init__(
        self,
        log_dir: str,
        session_id: str,
        min_severity: Severity = Severity.STATUS,
    ):
        self._session_id = session_id if session_id else "NO_SESSION"
        self._log_dir = log_dir
        self._min_severity = min_severity
        self._drop_count = 0
        self._error_count = 0
        self._degraded = False
        self._degradation_reported = False
        self._file_handle: Optional[Any] = None

        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        filename = "session_{}_{}.jsonl".format(self._session_id, timestamp)
        self._log_path = os.path.join(self._log_dir, filename)

        if not os.path.isdir(self._log_dir):
            self._degraded = True

    def _ensure_handle(self) -> None:
        if self._file_handle is None and not self._degraded:
            try:
                self._file_handle = open(self._log_path, "a", encoding="utf-8")
            except Exception:
                self._set_degraded()

    def _set_degraded(self) -> None:
        if self._degraded:
            return
        self._degraded = True
        self._error_count += 1
        self._emit_degradation_report()

    def _emit_degradation_report(self) -> None:
        """
        Non-recursive degradation self-report.
        Writes directly to file handle. Does NOT invoke self.log().
        Per Section_10_Fail_Open_Exception_Ratification.md:
        degradation self-report must use a non-recursive internal write path.
        """
        if self._degradation_reported:
            return
        if self._file_handle is None:
            return

        entry = {
            "entry_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "session_id": self._session_id,
            "channel": Channel.SOP.name,
            "severity": Severity.STATUS.value,
            "severity_name": Severity.STATUS.name,
            "message": "Operational logger degraded: filesystem unavailable",
        }

        try:
            self._file_handle.write(canonical_json(entry) + "\n")
            self._file_handle.flush()
            self._degradation_reported = True
        except Exception:
            pass

    def log(
        self,
        channel: Channel,
        severity: Severity,
        message: str,
        optional: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not isinstance(channel, Channel):
            self._error_count += 1
            return

        if not isinstance(severity, Severity):
            self._error_count += 1
            return

        if severity.value > self._min_severity.value:
            return

        if self._degraded:
            self._drop_count += 1
            return

        entry: Dict[str, Any] = {
            "entry_id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "session_id": self._session_id,
            "channel": channel.name,
            "severity": severity.value,
            "severity_name": severity.name,
            "message": message,
        }

        if optional:
            for key in _ALLOWED_OPTIONAL:
                if key in optional:
                    entry[key] = optional[key]

        try:
            self._ensure_handle()
            if self._file_handle is None:
                self._drop_count += 1
                return

            self._file_handle.write(canonical_json(entry) + "\n")
            self._file_handle.flush()
        except Exception:
            self._error_count += 1
            self._drop_count += 1
            self._set_degraded()

    def halt(self, channel: Channel, message: str, **kwargs: Any) -> None:
        self.log(channel, Severity.HALT, message, optional=kwargs if kwargs else None)

    def error(self, channel: Channel, message: str, **kwargs: Any) -> None:
        self.log(channel, Severity.ERROR, message, optional=kwargs if kwargs else None)

    def warn(self, channel: Channel, message: str, **kwargs: Any) -> None:
        self.log(channel, Severity.WARN, message, optional=kwargs if kwargs else None)

    def status(self, channel: Channel, message: str, **kwargs: Any) -> None:
        self.log(channel, Severity.STATUS, message, optional=kwargs if kwargs else None)

    def trace(self, channel: Channel, message: str, **kwargs: Any) -> None:
        self.log(channel, Severity.TRACE, message, optional=kwargs if kwargs else None)

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "drop_count": self._drop_count,
            "error_count": self._error_count,
            "degraded": self._degraded,
            "min_severity": self._min_severity.name,
            "session_id": self._session_id,
        }

    def close(self) -> None:
        """
        Must be invoked explicitly by LOGOS_SYSTEM shutdown sequence.
        No reliance on interpreter finalizers.
        """
        if self._file_handle is not None:
            try:
                self._file_handle.flush()
                self._file_handle.close()
            except Exception:
                pass
            self._file_handle = None
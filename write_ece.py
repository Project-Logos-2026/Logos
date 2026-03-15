"""Bootstrap script — writes Epistemic_Convergence_Engine.py then self-deletes."""
import pathlib, os

ECE = pathlib.Path(
    "/workspaces/Logos/LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_OPPERATIONS_CORE/"
    "Dynamic_Reconstruction_Adaptive_Compilation_Protocol/DRAC_Core/"
    "Epistemic_Convergence_Engine.py"
)

CONTENT = r'''# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: CONTROLLED
# VERSION: 1.0.0

"""
Epistemic_Convergence_Engine
=============================
Computes epistemic weights from EMP + PCCRE telemetry and updates the
DRAC axiom registry metadata under registry lock.

Constraints
-----------
- Fail closed on malformed telemetry (raises ConvergenceError before any write)
- No mutation of admitted axiom identity fields
- Registry lock required for all weight writes
- Append-only audit log (convergence_audit.jsonl)
- All weight updates produce structured audit entries
- Rollback + integrity alert on write failure

Output artifacts (written to report_dir)
-----------------------------------------
  epistemic_weight_updates.json
  axiom_convergence_report.json
  quarantined_axioms.json
  convergence_audit.jsonl  (append-only)
"""

from __future__ import annotations

import copy
import json
import logging
import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

logger = logging.getLogger("drac.convergence")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

QUARANTINE_WEIGHT_THRESHOLD: float = 0.10
QUARANTINE_STABILITY_THRESHOLD: float = 0.20
WEIGHT_MIN: float = 0.0
WEIGHT_MAX: float = 1.0

IMMUTABLE_AXIOM_FIELDS = frozenset({
    "module_name", "file_path", "fbc_id", "taxonomy_class",
    "entrypoint", "role_in_cores", "dependencies",
    "compatibility_markers", "catalog_presence",
})

REQUIRED_TELEMETRY_FIELDS = frozenset({
    "axiom_id", "usage_count", "successful_proofs",
    "contradictions", "convergence_score", "stability_factor",
})

# ---------------------------------------------------------------------------
# Exceptions (Fail-Closed)
# ---------------------------------------------------------------------------

class ConvergenceError(RuntimeError):
    """Raised for malformed telemetry or computation failures."""


class RegistryLockError(RuntimeError):
    """Raised when the registry lock cannot be acquired within the timeout."""


class RegistryIntegrityError(RuntimeError):
    """Raised when the registry cannot be restored after a write failure."""

# ---------------------------------------------------------------------------
# Data Types
# ---------------------------------------------------------------------------

@dataclass
class AxiomTelemetry:
    """
    Telemetry record for one axiom, supplied jointly by EMP and PCCRE.
    All float fields are expected in [0.0, 1.0].
    """
    axiom_id: str
    usage_count: int
    successful_proofs: int
    contradictions: int
    convergence_score: float   # from PCCRE reasoning loop
    stability_factor: float    # from EMP monitoring pipeline

    def validate(self) -> None:
        if not self.axiom_id or not isinstance(self.axiom_id, str):
            raise ConvergenceError("axiom_id must be a non-empty string")
        if self.usage_count < 0:
            raise ConvergenceError(
                f"[{self.axiom_id}] usage_count must be >= 0, got {self.usage_count}")
        if self.successful_proofs < 0:
            raise ConvergenceError(
                f"[{self.axiom_id}] successful_proofs must be >= 0")
        if self.contradictions < 0:
            raise ConvergenceError(
                f"[{self.axiom_id}] contradictions must be >= 0")
        if not (0.0 <= self.convergence_score <= 1.0):
            raise ConvergenceError(
                f"[{self.axiom_id}] convergence_score must be in [0,1], "
                f"got {self.convergence_score}")
        if not (0.0 <= self.stability_factor <= 1.0):
            raise ConvergenceError(
                f"[{self.axiom_id}] stability_factor must be in [0,1], "
                f"got {self.stability_factor}")


@dataclass
class WeightUpdateEntry:
    """Single audit record for one axiom weight mutation."""
    timestamp: str
    axiom_id: str
    previous_weight: Optional[float]
    new_weight: float
    previous_status: Optional[str]
    new_status: str
    quarantined: bool
    telemetry_snapshot: Dict[str, Any]


@dataclass
class ConvergenceResult:
    """Return value of EpistemicConvergenceEngine.update_weights()."""
    run_timestamp: str
    total_processed: int
    total_updated: int
    total_quarantined: int
    total_skipped: int
    weight_updates: List[WeightUpdateEntry]
    quarantined_axioms: List[str]
    skipped_axioms: List[str]
    report_dir: str

# ---------------------------------------------------------------------------
# Weight formula
# ---------------------------------------------------------------------------

def _compute_epistemic_weight(tel: AxiomTelemetry) -> float:
    """
    Compute bounded epistemic weight in [0.0, 1.0].

    Formula
    -------
    proof_ratio   = successful_proofs / max(usage_count, 1)
    contra_ratio  = contradictions    / max(usage_count, 1)
    safety_factor = 1.0 - clamp(contra_ratio, 0, 1)
    component     = 0.35*proof_ratio + 0.35*convergence_score + 0.30*stability_factor
    weight        = component * safety_factor   clamped to [WEIGHT_MIN, WEIGHT_MAX]

    The safety_factor multiplicatively penalises contradictions: an axiom
    whose every invocation contradicts is driven to weight 0.0 regardless
    of convergence_score or stability_factor.
    """
    denom = max(tel.usage_count, 1)
    proof_ratio = tel.successful_proofs / denom
    safety_factor = max(0.0, 1.0 - min(tel.contradictions / denom, 1.0))
    component = (
        0.35 * proof_ratio
        + 0.35 * tel.convergence_score
        + 0.30 * tel.stability_factor
    )
    return max(WEIGHT_MIN, min(WEIGHT_MAX, component * safety_factor))


def _should_quarantine(tel: AxiomTelemetry, weight: float) -> bool:
    """
    Quarantine rules (any one condition triggers quarantine).

    R1: weight < QUARANTINE_WEIGHT_THRESHOLD       (0.10 default)
    R2: stability_factor < QUARANTINE_STABILITY_THRESHOLD  (0.20 default)
    R3: contradictions > successful_proofs         (reliability inversion)
    """
    if weight < QUARANTINE_WEIGHT_THRESHOLD:
        return True
    if tel.stability_factor < QUARANTINE_STABILITY_THRESHOLD:
        return True
    if tel.contradictions > tel.successful_proofs:
        return True
    return False

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class EpistemicConvergenceEngine:
    """
    Computes and applies epistemic weight updates to the DRAC axiom registry.

    Parameters
    ----------
    registry_path : str — path to drac_axiom_registry.json
    report_dir    : str — directory for output artifacts and audit log
    lock          : threading.Lock or None — shared lock for registry access;
                    a private lock is created when None is provided
    """

    def __init__(
        self,
        registry_path: str,
        report_dir: str,
        lock: Optional[threading.Lock] = None,
    ) -> None:
        self._registry_path = Path(registry_path)
        self._report_dir = Path(report_dir)
        self._lock: threading.Lock = lock if lock is not None else threading.Lock()
        self._audit_log: List[Dict[str, Any]] = []

        if not self._registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self._registry_path}")
        self._report_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update_weights(
        self, telemetry_batch: Sequence[Dict[str, Any]]
    ) -> ConvergenceResult:
        """
        Process a batch of telemetry records and update registry weights.

        All telemetry is validated BEFORE the registry lock is acquired,
        so a malformed batch raises ConvergenceError without any registry
        mutation.

        Parameters
        ----------
        telemetry_batch : list of dicts, each with the six required fields:
            axiom_id, usage_count, successful_proofs, contradictions,
            convergence_score, stability_factor

        Returns
        -------
        ConvergenceResult with full audit trail and artifact paths.

        Raises
        ------
        ConvergenceError       : malformed or missing telemetry
        RegistryLockError      : lock not acquired within 10 s
        RegistryIntegrityError : write failed and rollback also failed
        """
        run_ts = _iso_now()

        # 1. Validate and parse — fail-closed before any lock or write
        parsed: List[AxiomTelemetry] = [
            self._parse_telemetry(raw) for raw in telemetry_batch
        ]

        # 2. Acquire registry lock
        acquired = self._lock.acquire(timeout=10.0)
        if not acquired:
            raise RegistryLockError("Could not acquire registry lock within 10 s")

        try:
            registry = self._load_registry()
            snapshot = copy.deepcopy(registry)            # rollback point
            idx = self._index_registry(registry)

            weight_updates: List[WeightUpdateEntry] = []
            quarantined: List[str] = []
            skipped: List[str] = []

            for tel in parsed:
                if tel.axiom_id not in idx:
                    logger.warning(
                        "Axiom '%s' not found in registry — skipped", tel.axiom_id)
                    skipped.append(tel.axiom_id)
                    continue

                entry = idx[tel.axiom_id]
                new_weight = _compute_epistemic_weight(tel)
                quarantine = _should_quarantine(tel, new_weight)
                new_status = "QUARANTINED" if quarantine else "ACTIVE"

                # Fetch prior values before mutation
                meta = entry.setdefault("epistemic_metadata", {})
                prev_weight: Optional[float] = meta.get("epistemic_weight")
                prev_status: Optional[str] = meta.get("convergence_status")

                # Only touch epistemic_metadata — never alter identity fields
                meta["epistemic_weight"] = new_weight
                meta["convergence_status"] = new_status
                meta["last_updated"] = run_ts
                meta["usage_count"] = tel.usage_count
                meta["successful_proofs"] = tel.successful_proofs
                meta["contradictions"] = tel.contradictions
                meta["convergence_score"] = tel.convergence_score
                meta["stability_factor"] = tel.stability_factor

                upd = WeightUpdateEntry(
                    timestamp=run_ts,
                    axiom_id=tel.axiom_id,
                    previous_weight=prev_weight,
                    new_weight=new_weight,
                    previous_status=prev_status,
                    new_status=new_status,
                    quarantined=quarantine,
                    telemetry_snapshot=asdict(tel),
                )
                weight_updates.append(upd)
                self._append_audit(upd)

                if quarantine:
                    quarantined.append(tel.axiom_id)
                    logger.warning(
                        "Axiom '%s' QUARANTINED weight=%.4f stability=%.4f "
                        "contradictions=%d successful=%d",
                        tel.axiom_id, new_weight, tel.stability_factor,
                        tel.contradictions, tel.successful_proofs,
                    )
                else:
                    logger.info(
                        "Axiom '%s' weight %.4f -> %.4f status=%s",
                        tel.axiom_id, prev_weight or 0.0, new_weight, new_status,
                    )

            # 3. Write updated registry (rollback on failure)
            try:
                self._write_registry(registry)
            except Exception as exc:
                logger.error("Registry write failed (%s). Attempting rollback.", exc)
                try:
                    self._write_registry(snapshot)
                    logger.warning("Registry restored from pre-run snapshot.")
                except Exception as rb_exc:
                    alert_path = self._report_dir / "registry_integrity_alert.json"
                    self._write_json(alert_path, {
                        "alert": "REGISTRY_INTEGRITY_FAILURE",
                        "timestamp": run_ts,
                        "write_error": str(exc),
                        "rollback_error": str(rb_exc),
                        "action_required": (
                            "Restore registry from last known-good snapshot. "
                            "Disable EpistemicConvergenceEngine until resolved."
                        ),
                    })
                    raise RegistryIntegrityError(
                        f"Write and rollback both failed. Alert written: {alert_path}"
                    ) from rb_exc
                raise RegistryIntegrityError(
                    "Registry write failed; state rolled back successfully."
                ) from exc

        finally:
            self._lock.release()

        # 4. Emit output artifacts
        result = ConvergenceResult(
            run_timestamp=run_ts,
            total_processed=len(parsed),
            total_updated=len(weight_updates),
            total_quarantined=len(quarantined),
            total_skipped=len(skipped),
            weight_updates=weight_updates,
            quarantined_axioms=quarantined,
            skipped_axioms=skipped,
            report_dir=str(self._report_dir),
        )
        self._emit_artifacts(result)
        self._write_run_log(run_ts, result)
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_telemetry(raw: Dict[str, Any]) -> AxiomTelemetry:
        missing = REQUIRED_TELEMETRY_FIELDS - set(raw.keys())
        if missing:
            raise ConvergenceError(
                f"Telemetry record missing required fields: {sorted(missing)}")
        try:
            tel = AxiomTelemetry(
                axiom_id=str(raw["axiom_id"]),
                usage_count=int(raw["usage_count"]),
                successful_proofs=int(raw["successful_proofs"]),
                contradictions=int(raw["contradictions"]),
                convergence_score=float(raw["convergence_score"]),
                stability_factor=float(raw["stability_factor"]),
            )
        except (TypeError, ValueError) as exc:
            raise ConvergenceError(
                f"Telemetry coercion failed for "
                f"axiom_id={raw.get('axiom_id')!r}: {exc}"
            ) from exc
        tel.validate()
        return tel

    def _load_registry(self) -> Dict[str, Any]:
        try:
            with self._registry_path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ConvergenceError(f"Registry JSON malformed: {exc}") from exc
        if "entries" not in data:
            raise ConvergenceError(
                "Registry missing 'entries' key — aborting to preserve integrity")
        return data

    @staticmethod
    def _index_registry(registry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Build lookup by module_name AND fbc_id so either resolves."""
        idx: Dict[str, Dict[str, Any]] = {}
        for entry in registry.get("entries", []):
            name = entry.get("module_name")
            fbc = entry.get("fbc_id")
            if name:
                idx[name] = entry
            if fbc:
                idx[fbc] = entry
        return idx

    def _write_registry(self, registry: Dict[str, Any]) -> None:
        registry["last_convergence_run"] = _iso_now()
        with self._registry_path.open("w", encoding="utf-8") as fh:
            json.dump(registry, fh, indent=2)

    def _append_audit(self, update: WeightUpdateEntry) -> None:
        self._audit_log.append(asdict(update))

    def _emit_artifacts(self, result: ConvergenceResult) -> None:
        self._write_json(
            self._report_dir / "epistemic_weight_updates.json",
            {
                "generated_at": result.run_timestamp,
                "total_updated": result.total_updated,
                "updates": [asdict(u) for u in result.weight_updates],
            },
        )
        self._write_json(
            self._report_dir / "axiom_convergence_report.json",
            {
                "generated_at": result.run_timestamp,
                "total_processed": result.total_processed,
                "total_updated": result.total_updated,
                "total_quarantined": result.total_quarantined,
                "total_skipped": result.total_skipped,
                "skipped_axioms": result.skipped_axioms,
                "weight_summary": [
                    {
                        "axiom_id": u.axiom_id,
                        "previous_weight": u.previous_weight,
                        "new_weight": u.new_weight,
                        "status": u.new_status,
                    }
                    for u in result.weight_updates
                ],
            },
        )
        self._write_json(
            self._report_dir / "quarantined_axioms.json",
            {
                "generated_at": result.run_timestamp,
                "quarantined_count": result.total_quarantined,
                "quarantined_axioms": [
                    asdict(u) for u in result.weight_updates if u.quarantined
                ],
            },
        )

    def _write_run_log(self, run_ts: str, result: ConvergenceResult) -> None:
        """Append-only JSONL log — one record per run, never overwritten."""
        log_path = self._report_dir / "convergence_audit.jsonl"
        record = {
            "timestamp": run_ts,
            "total_processed": result.total_processed,
            "total_updated": result.total_updated,
            "total_quarantined": result.total_quarantined,
            "total_skipped": result.total_skipped,
            "weight_entries": [
                {
                    "timestamp": u.timestamp,
                    "axiom_id": u.axiom_id,
                    "previous_weight": u.previous_weight,
                    "new_weight": u.new_weight,
                    "status_changes": {
                        "from": u.previous_status,
                        "to": u.new_status,
                    },
                    "quarantined": u.quarantined,
                }
                for u in result.weight_updates
            ],
        }
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()
'''

ECE.write_text(CONTENT, encoding="utf-8")
print(f"Written {ECE} — {ECE.stat().st_size} bytes, {CONTENT.count(chr(10))} lines")

import os
os.remove(__file__)
print("Bootstrap script deleted.")

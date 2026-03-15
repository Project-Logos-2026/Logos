# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: CONTROLLED
# VERSION: 1.0.0
"""
Epistemic Convergence Engine (ECE)

Computes epistemic weights from EMP+PCCRE telemetry and updates the DRAC
axiom registry.  Only the ``epistemic_metadata`` sub-dict of each registry
entry is mutated; all identity fields are preserved.

Fail-closed: any validation failure aborts the entire batch before acquiring
the registry lock.
"""
from __future__ import annotations
import copy, json, logging, threading
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

logger = logging.getLogger("drac.convergence")

QUARANTINE_WEIGHT_THRESHOLD: float = 0.10
QUARANTINE_STABILITY_THRESHOLD: float = 0.20
WEIGHT_MIN: float = 0.0
WEIGHT_MAX: float = 1.0
REQUIRED_TELEMETRY_FIELDS = frozenset({
    "axiom_id", "usage_count", "successful_proofs",
    "contradictions", "convergence_score", "stability_factor",
})


class ConvergenceError(RuntimeError):
    """Raised when telemetry is invalid or registry update cannot proceed."""


class RegistryLockError(RuntimeError):
    """Raised when the registry lock cannot be acquired within the timeout."""


class RegistryIntegrityError(RuntimeError):
    """Raised when both the registry write and the rollback write fail."""


@dataclass
class AxiomTelemetry:
    axiom_id: str
    usage_count: int
    successful_proofs: int
    contradictions: int
    convergence_score: float
    stability_factor: float

    def validate(self) -> None:
        if not self.axiom_id:
            raise ConvergenceError("axiom_id must be a non-empty string")
        if self.usage_count < 0:
            raise ConvergenceError(f"[{self.axiom_id}] usage_count must be >= 0")
        if self.successful_proofs < 0:
            raise ConvergenceError(f"[{self.axiom_id}] successful_proofs must be >= 0")
        if self.contradictions < 0:
            raise ConvergenceError(f"[{self.axiom_id}] contradictions must be >= 0")
        if not (0.0 <= self.convergence_score <= 1.0):
            raise ConvergenceError(
                f"[{self.axiom_id}] convergence_score {self.convergence_score} not in [0, 1]"
            )
        if not (0.0 <= self.stability_factor <= 1.0):
            raise ConvergenceError(
                f"[{self.axiom_id}] stability_factor {self.stability_factor} not in [0, 1]"
            )


@dataclass
class WeightUpdateEntry:
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
    run_timestamp: str
    total_processed: int
    total_updated: int
    total_quarantined: int
    total_skipped: int
    weight_updates: List[WeightUpdateEntry]
    quarantined_axioms: List[str]
    skipped_axioms: List[str]
    report_dir: str


def _compute_epistemic_weight(tel: AxiomTelemetry) -> float:
    denom = max(tel.usage_count, 1)
    proof_ratio = tel.successful_proofs / denom
    safety = max(0.0, 1.0 - min(tel.contradictions / denom, 1.0))
    component = (
        0.35 * proof_ratio
        + 0.35 * tel.convergence_score
        + 0.30 * tel.stability_factor
    )
    return max(WEIGHT_MIN, min(WEIGHT_MAX, component * safety))


def _should_quarantine(tel: AxiomTelemetry, weight: float) -> bool:
    if weight < QUARANTINE_WEIGHT_THRESHOLD:
        return True
    if tel.stability_factor < QUARANTINE_STABILITY_THRESHOLD:
        return True
    if tel.contradictions > tel.successful_proofs:
        return True
    return False


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


class EpistemicConvergenceEngine:
    """Updates DRAC axiom registry weights from telemetry in a single locked transaction."""

    def __init__(
        self,
        registry_path: str,
        report_dir: str,
        lock: Optional[threading.Lock] = None,
    ) -> None:
        self._registry_path = Path(registry_path)
        self._report_dir = Path(report_dir)
        self._lock: threading.Lock = lock if lock is not None else threading.Lock()
        if not self._registry_path.exists():
            raise FileNotFoundError(f"Axiom registry not found: {self._registry_path}")
        self._report_dir.mkdir(parents=True, exist_ok=True)

    def update_weights(
        self, telemetry_batch: Sequence[Dict[str, Any]]
    ) -> ConvergenceResult:
        """Process telemetry_batch and update axiom registry weights. Fail-closed."""
        run_ts = _iso_now()
        parsed: List[AxiomTelemetry] = [
            self._parse_telemetry(raw) for raw in telemetry_batch
        ]
        acquired = self._lock.acquire(timeout=10.0)
        if not acquired:
            raise RegistryLockError("Registry lock not acquired within 10 s; aborting.")
        try:
            registry = self._load_registry()
            snapshot = copy.deepcopy(registry)
            idx = self._index_registry(registry)
            weight_updates: List[WeightUpdateEntry] = []
            quarantined: List[str] = []
            skipped: List[str] = []
            for tel in parsed:
                if tel.axiom_id not in idx:
                    logger.warning("Axiom not found in registry - skipped: %s", tel.axiom_id)
                    skipped.append(tel.axiom_id)
                    continue
                entry = idx[tel.axiom_id]
                new_weight = _compute_epistemic_weight(tel)
                quarantine = _should_quarantine(tel, new_weight)
                new_status = "QUARANTINED" if quarantine else "ACTIVE"
                meta: Dict[str, Any] = entry.setdefault("epistemic_metadata", {})
                prev_weight: Optional[float] = meta.get("epistemic_weight")
                prev_status: Optional[str] = meta.get("convergence_status")
                meta.update({
                    "epistemic_weight": new_weight,
                    "convergence_status": new_status,
                    "last_updated": run_ts,
                    "usage_count": tel.usage_count,
                    "successful_proofs": tel.successful_proofs,
                    "contradictions": tel.contradictions,
                    "convergence_score": tel.convergence_score,
                    "stability_factor": tel.stability_factor,
                })
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
                if quarantine:
                    quarantined.append(tel.axiom_id)
                    logger.warning("QUARANTINED %s  weight=%.4f", tel.axiom_id, new_weight)
                else:
                    logger.info(
                        "Updated %s  %.4f -> %.4f  status=%s",
                        tel.axiom_id, prev_weight or 0.0, new_weight, new_status,
                    )
            try:
                self._write_registry(registry)
            except Exception as exc:
                logger.error("Registry write failed: %s. Attempting rollback.", exc)
                try:
                    self._write_registry(snapshot)
                    logger.warning("Rollback succeeded.")
                except Exception as rb_exc:
                    alert_path = self._report_dir / "registry_integrity_alert.json"
                    _write_json(alert_path, {
                        "alert": "REGISTRY_INTEGRITY_FAILURE",
                        "timestamp": run_ts,
                        "write_error": str(exc),
                        "rollback_error": str(rb_exc),
                        "action_required": "Manually restore registry from backup and disable ECE.",
                    })
                    raise RegistryIntegrityError(
                        f"Write and rollback both failed. Alert written to {alert_path}"
                    ) from rb_exc
                raise RegistryIntegrityError(
                    "Registry write failed; rollback succeeded."
                ) from exc
        finally:
            self._lock.release()
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

    @staticmethod
    def _parse_telemetry(raw: Dict[str, Any]) -> AxiomTelemetry:
        missing = REQUIRED_TELEMETRY_FIELDS - set(raw.keys())
        if missing:
            raise ConvergenceError(
                f"Missing required telemetry fields: {sorted(missing)}"
            )
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
                f"Type coercion failed for axiom {raw.get('axiom_id', '<unknown>')}: {exc}"
            ) from exc
        tel.validate()
        return tel

    def _load_registry(self) -> Dict[str, Any]:
        try:
            with self._registry_path.open("r", encoding="utf-8") as fh:
                data: Dict[str, Any] = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ConvergenceError(f"Axiom registry JSON is malformed: {exc}") from exc
        if "entries" not in data:
            raise ConvergenceError("Axiom registry is missing the required 'entries' key.")
        return data

    @staticmethod
    def _index_registry(registry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        idx: Dict[str, Dict[str, Any]] = {}
        for entry in registry.get("entries", []):
            module_name = entry.get("module_name")
            fbc_id = entry.get("fbc_id")
            if module_name:
                idx[module_name] = entry
            if fbc_id:
                idx[fbc_id] = entry
        return idx

    def _write_registry(self, registry: Dict[str, Any]) -> None:
        registry["last_convergence_run"] = _iso_now()
        with self._registry_path.open("w", encoding="utf-8") as fh:
            json.dump(registry, fh, indent=2)

    def _emit_artifacts(self, result: ConvergenceResult) -> None:
        _write_json(
            self._report_dir / "epistemic_weight_updates.json",
            {
                "generated_at": result.run_timestamp,
                "total_updated": result.total_updated,
                "updates": [asdict(u) for u in result.weight_updates],
            },
        )
        _write_json(
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
        _write_json(
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
        """Append-only JSONL audit log; never overwritten."""
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
                    "status_change": {"from": u.previous_status, "to": u.new_status},
                    "quarantined": u.quarantined,
                }
                for u in result.weight_updates
            ],
        }
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")

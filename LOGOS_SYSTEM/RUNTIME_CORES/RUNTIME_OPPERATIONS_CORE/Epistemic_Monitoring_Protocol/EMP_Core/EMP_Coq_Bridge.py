# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: EMP_Coq_Bridge
runtime_layer: operations
role: Runtime module
responsibility: Manages Coq subprocess lifecycle for mechanical proof verification.
    Submits .v content for compilation, parses structured output, enforces
    compilation timeouts, and maintains loadpath configuration matching
    PXL_Gate _CoqProject semantics. Fail-closed on all error paths.
agent_binding: None
protocol_binding: Epistemic_Monitoring_Protocol
runtime_classification: runtime_module
boot_phase: E1
expected_imports:
  - typing
  - dataclasses
  - subprocess
  - tempfile
  - hashlib
  - pathlib
  - re
  - time
provides:
  - CoqVerificationResult
  - CompilationResult
  - TheoremStatus
  - EMP_Coq_Bridge
depends_on_runtime_state: False
failure_mode:
  type: fail_closed
  notes: Any subprocess failure, timeout, or parse error returns verified=False
    with structured error. No partial success states.
rewrite_provenance:
  source: EMP_NATIVE_COQ_PROOF_ENGINE_BLUEPRINT_AND_ROADMAP.md
  rewrite_phase: Phase_E1
  rewrite_timestamp: 2026-02-11T00:00:00Z
observability:
  log_channel: EMP
  metrics: disabled
---------------------
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import tempfile
import hashlib
import shutil
import time
import re
import os


# =============================================================================
# Exceptions (Fail-Closed)
# =============================================================================

class CoqBridgeError(Exception):
    pass


class CoqTimeoutError(CoqBridgeError):
    pass


class CoqEnvironmentError(CoqBridgeError):
    pass


class CoqCompilationError(CoqBridgeError):
    pass


# =============================================================================
# Data Structures
# =============================================================================

@dataclass(frozen=True)
class CoqVerificationResult:
    verified: bool
    admits_count: int
    axiom_dependencies: List[str]
    proof_steps: int
    compilation_time_ms: int
    error_message: Optional[str] = None
    vo_artifact_hash: Optional[str] = None
    raw_output: Optional[str] = None


@dataclass(frozen=True)
class CompilationResult:
    success: bool
    file_path: str
    verification: CoqVerificationResult
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class TheoremStatus:
    name: str
    exists: bool
    proven: bool
    admitted: bool
    axiom_footprint: List[str] = field(default_factory=list)


# =============================================================================
# PXL Kernel Axiom Registry
# =============================================================================

PXL_KERNEL_AXIOMS = frozenset({
    "ax_K", "ax_T", "ax_4", "ax_5", "ax_Nec",
    "ax_ident_refl", "ax_ident_symm", "ax_ident_trans",
    "ax_nonequiv_irrefl", "ax_inter_comm",
    "ax_imp_intro", "ax_imp_elim",
    "ax_mequiv_intro", "ax_mequiv_elim",
    "imaginary_boundary", "omega_operator",
    "modal_decidability", "pxl_equation_encodes_structure",
    "privative_boundary_detectable",
})


# =============================================================================
# Coq Output Parsers
# =============================================================================

def _parse_admits(output: str) -> int:
    count = output.lower().count("admitted.")
    axiom_pattern = re.findall(r"Axiom\s+\w+", output)
    return count


def _parse_axiom_dependencies(output: str) -> List[str]:
    axioms = re.findall(r"(?:Axiom|Parameter)\s+(\w+)", output)
    return sorted(set(axioms))


def _parse_proof_steps(output: str) -> int:
    steps = re.findall(
        r"\b(?:Proof|Qed|intros|apply|exact|destruct|split|exists|"
        r"rewrite|unfold|simpl|auto|trivial|assumption|contradiction|"
        r"induction|inversion|discriminate|subst|reflexivity)\b",
        output,
    )
    return len(steps)


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# =============================================================================
# EMP Coq Bridge
# =============================================================================

class EMP_Coq_Bridge:
    """
    Manages Coq subprocess lifecycle for mechanical proof verification.

    Environment selection order:
    1. Native coqc (if available on system PATH)
    2. Fail-closed with CoqEnvironmentError

    jsCoq WebAssembly integration is deferred to browser-side implementation.
    This module handles server-side / CLI verification only.

    NO REASONING. NO INFERENCE. MECHANICAL VERIFICATION ONLY.
    """

    def __init__(
        self,
        pxl_gate_root: Optional[Path] = None,
        timeout_seconds: int = 30,
        coqc_path: Optional[str] = None,
    ):
        self._pxl_gate_root = pxl_gate_root
        self._timeout = timeout_seconds
        self._coqc_path = coqc_path or self._detect_coqc()
        self._loadpath_args: List[str] = []

        if self._pxl_gate_root is not None:
            self._configure_loadpath()

    # -------------------------------------------------------------------------
    # Environment Detection
    # -------------------------------------------------------------------------

    @staticmethod
    def _detect_coqc() -> Optional[str]:
        path = shutil.which("coqc")
        return path

    def _configure_loadpath(self) -> None:
        coq_project = self._pxl_gate_root / "coq" / "_CoqProject"
        if not coq_project.exists():
            self._loadpath_args = []
            return

        lines = coq_project.read_text().splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("-Q ") or line.startswith("-R "):
                parts = line.split()
                if len(parts) == 3:
                    flag, rel_path, logical_name = parts
                    resolved = (self._pxl_gate_root / "coq" / rel_path).resolve()
                    if resolved.is_dir():
                        self._loadpath_args.extend([flag, str(resolved), logical_name])

    # -------------------------------------------------------------------------
    # Core Verification
    # -------------------------------------------------------------------------

    def verify(self, coq_source: str) -> CoqVerificationResult:
        if self._coqc_path is None:
            return CoqVerificationResult(
                verified=False,
                admits_count=0,
                axiom_dependencies=[],
                proof_steps=0,
                compilation_time_ms=0,
                error_message="No Coq environment available",
            )

        with tempfile.NamedTemporaryFile(
            suffix=".v", mode="w", delete=False
        ) as tmp:
            tmp.write(coq_source)
            tmp_path = Path(tmp.name)

        try:
            return self._compile_and_parse(tmp_path, coq_source)
        finally:
            tmp_path.unlink(missing_ok=True)
            vo_path = tmp_path.with_suffix(".vo")
            vo_path.unlink(missing_ok=True)
            glob_path = tmp_path.with_suffix(".glob")
            glob_path.unlink(missing_ok=True)

    def compile_file(self, file_path: str) -> CompilationResult:
        path = Path(file_path)
        if not path.exists():
            return CompilationResult(
                success=False,
                file_path=file_path,
                verification=CoqVerificationResult(
                    verified=False,
                    admits_count=0,
                    axiom_dependencies=[],
                    proof_steps=0,
                    compilation_time_ms=0,
                    error_message=f"File not found: {file_path}",
                ),
            )

        source = path.read_text()
        verification = self._compile_and_parse(path, source)
        return CompilationResult(
            success=verification.verified,
            file_path=file_path,
            verification=verification,
        )

    def check_theorem(self, theorem_name: str, file_path: str) -> TheoremStatus:
        path = Path(file_path)
        if not path.exists():
            return TheoremStatus(
                name=theorem_name, exists=False, proven=False, admitted=False
            )

        source = path.read_text()

        name_pattern = re.compile(
            rf"\b(?:Theorem|Lemma|Definition|Corollary)\s+{re.escape(theorem_name)}\b"
        )
        exists = bool(name_pattern.search(source))
        if not exists:
            return TheoremStatus(
                name=theorem_name, exists=False, proven=False, admitted=False
            )

        admitted_pattern = re.compile(
            rf"(?:Theorem|Lemma|Definition|Corollary)\s+{re.escape(theorem_name)}\b"
            r".*?(?:Admitted\.)",
            re.DOTALL,
        )
        admitted = bool(admitted_pattern.search(source))

        qed_pattern = re.compile(
            rf"(?:Theorem|Lemma|Definition|Corollary)\s+{re.escape(theorem_name)}\b"
            r".*?(?:Qed\.|Defined\.)",
            re.DOTALL,
        )
        proven = bool(qed_pattern.search(source))

        axiom_deps = _parse_axiom_dependencies(source)

        return TheoremStatus(
            name=theorem_name,
            exists=True,
            proven=proven,
            admitted=admitted,
            axiom_footprint=axiom_deps,
        )

    def get_axiom_footprint(self, file_path: str) -> List[str]:
        path = Path(file_path)
        if not path.exists():
            return []
        source = path.read_text()
        return _parse_axiom_dependencies(source)

    # -------------------------------------------------------------------------
    # Internal Compilation
    # -------------------------------------------------------------------------

    def _compile_and_parse(
        self, file_path: Path, source: str
    ) -> CoqVerificationResult:
        cmd = [self._coqc_path, "-verbose"]
        cmd.extend(self._loadpath_args)
        cmd.append(str(file_path))

        start_ms = int(time.time() * 1000)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                cwd=str(file_path.parent),
            )
        except subprocess.TimeoutExpired:
            elapsed = int(time.time() * 1000) - start_ms
            return CoqVerificationResult(
                verified=False,
                admits_count=0,
                axiom_dependencies=[],
                proof_steps=0,
                compilation_time_ms=elapsed,
                error_message=f"Coq compilation timed out after {self._timeout}s",
            )
        except Exception as exc:
            elapsed = int(time.time() * 1000) - start_ms
            return CoqVerificationResult(
                verified=False,
                admits_count=0,
                axiom_dependencies=[],
                proof_steps=0,
                compilation_time_ms=elapsed,
                error_message=f"Coq subprocess error: {exc}",
            )

        elapsed = int(time.time() * 1000) - start_ms
        combined_output = result.stdout + "\n" + result.stderr

        if result.returncode != 0:
            return CoqVerificationResult(
                verified=False,
                admits_count=_parse_admits(source),
                axiom_dependencies=_parse_axiom_dependencies(source),
                proof_steps=_parse_proof_steps(source),
                compilation_time_ms=elapsed,
                error_message=result.stderr.strip() or "Coq compilation failed",
                raw_output=combined_output,
            )

        admits = _parse_admits(source)
        axioms = _parse_axiom_dependencies(source)
        steps = _parse_proof_steps(source)

        vo_path = file_path.with_suffix(".vo")
        vo_hash = _hash_file(vo_path) if vo_path.exists() else None

        return CoqVerificationResult(
            verified=True,
            admits_count=admits,
            axiom_dependencies=axioms,
            proof_steps=steps,
            compilation_time_ms=elapsed,
            vo_artifact_hash=vo_hash,
            raw_output=combined_output,
        )

    # -------------------------------------------------------------------------
    # PXL Kernel Check
    # -------------------------------------------------------------------------

    @staticmethod
    def axioms_within_pxl_kernel(axiom_list: List[str]) -> bool:
        return all(ax in PXL_KERNEL_AXIOMS for ax in axiom_list)

    # -------------------------------------------------------------------------
    # Introspection (Safe)
    # -------------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        return {
            "coqc_available": self._coqc_path is not None,
            "coqc_path": self._coqc_path,
            "pxl_gate_root": str(self._pxl_gate_root) if self._pxl_gate_root else None,
            "loadpath_args": self._loadpath_args,
            "timeout_seconds": self._timeout,
            "pxl_kernel_axiom_count": len(PXL_KERNEL_AXIOMS),
        }

# File: MSPC_Output_Contract.py
# Protocol: Multi_Process_Signal_Compiler (MSPC)
# Layer: Runtime_Execution_Core
# Phase: Phase_5
# Authority: LOGOS_SYSTEM
# Status: Design-Complete / Runtime-Operational
# Description:
#   Defines the output contract for the MSPC protocol. All MSPC
#   outputs conform to one of three artifact classes: Compiled
#   Meaning Artifacts, Execution-Eligible Descriptions, or
#   Runtime Contracts. This module provides validation and
#   classification for emitted outputs.
#
# Invariants:
#   - No mutation of Axiom Contexts
#   - No mutation of Application Functions
#   - No mutation of Orchestration Overlays
#   - Fail-closed on invariant violation

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from Multi_Process_Signal_Compiler.Compilation.Artifact_Emitter import EmittedArtifact


class OutputClass(Enum):
    COMPILED_MEANING = "compiled_meaning"
    EXECUTION_ELIGIBLE = "execution_eligible"
    RUNTIME_CONTRACT = "runtime_contract"
    UNCLASSIFIED = "unclassified"


_CLASS_INDICATORS = {
    OutputClass.COMPILED_MEANING: {"smp", "semantic_graph", "af_bundle", "meaning"},
    OutputClass.EXECUTION_ELIGIBLE: {"plan", "constraint", "precondition", "execution"},
    OutputClass.RUNTIME_CONTRACT: {"exists", "coherent", "supersedes", "contract"},
}


def classify_output(artifact: EmittedArtifact) -> OutputClass:
    artifact_type = artifact.content.get("type", "")
    artifact_domain = artifact.content.get("domain", "")
    combined = f"{artifact_type} {artifact_domain}".lower()

    for output_class, indicators in _CLASS_INDICATORS.items():
        for indicator in indicators:
            if indicator in combined:
                return output_class

    return OutputClass.UNCLASSIFIED


def validate_output(artifact: EmittedArtifact) -> List[str]:
    violations: List[str] = []

    if not artifact.emission_id:
        violations.append("missing emission_id")
    if not artifact.artifact_id:
        violations.append("missing artifact_id")
    if not artifact.artifact_hash:
        violations.append("missing artifact_hash")
    if not isinstance(artifact.content, dict):
        violations.append("content is not a dict")
    if not isinstance(artifact.provenance, dict):
        violations.append("provenance is not a dict")
    if artifact.emitted_at <= 0:
        violations.append("invalid emitted_at timestamp")

    return violations


def build_contract_summary(artifacts: List[EmittedArtifact]) -> Dict[str, Any]:
    classified: Dict[str, int] = {}
    invalid: List[str] = []

    for art in artifacts:
        cls = classify_output(art)
        classified[cls.value] = classified.get(cls.value, 0) + 1
        violations = validate_output(art)
        if violations:
            invalid.append(art.emission_id)

    return {
        "total_outputs": len(artifacts),
        "classification_counts": classified,
        "invalid_output_ids": invalid,
        "all_valid": len(invalid) == 0,
    }

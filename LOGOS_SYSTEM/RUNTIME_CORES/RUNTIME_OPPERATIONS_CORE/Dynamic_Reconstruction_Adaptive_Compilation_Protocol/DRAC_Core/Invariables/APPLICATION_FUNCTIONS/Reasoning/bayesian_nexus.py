# HEADER_TYPE: LEGACY_REWRITE_CANDIDATE
# EXECUTION: FORBIDDEN
# IMPORT: FORBIDDEN
# AUTHORITY: NONE
# DESTINATION: Logos_System_Rebuild
# ARCHIVE_AFTER_REWRITE: REQUIRED


# bayesian_nexus.py
"""
bayesian_nexus.py

Toolkit-level Nexus orchestrator for Bayesian Predictor.
"""
import json
import traceback
from typing import Dict, List


# =============================================================================
# Provisional PXL Proof Tagging (Egress Only)
# =============================================================================

PROVISIONAL_DISCLAIMER = "Requires EMP compilation"
PROVISIONAL_STATUS = "PROVISIONAL"


def _payload_is_smp(payload: Dict[str, object]) -> bool:
    return isinstance(payload, dict) and any(
        key in payload for key in ("smp_id", "smp", "raw_input", "header")
    )


def _pxl_key_match(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("pxl", "formal_logic", "wff", "axiom", "proof"))


def _contains_pxl_fragments(obj: object) -> bool:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if _pxl_key_match(str(key)) or _contains_pxl_fragments(value):
                return True
        return False
    if isinstance(obj, list):
        return any(_contains_pxl_fragments(item) for item in obj)
    if isinstance(obj, str):
        return _pxl_key_match(obj)
    return False


def _extract_proof_refs(obj: Dict[str, object]) -> Dict[str, Optional[str]]:
    proof_id = obj.get("proof_id") or obj.get("pxl_proof_id")
    proof_hash = obj.get("proof_hash") or obj.get("pxl_proof_hash")
    proof_index = obj.get("proof_index") or obj.get("pxl_proof_index")
    proof_refs = obj.get("proof_refs") or obj.get("pxl_refs")

    if not proof_id and isinstance(proof_index, dict):
        proof_id = proof_index.get("proof_id")
        proof_hash = proof_hash or proof_index.get("proof_hash")

    if not proof_id and isinstance(proof_refs, dict):
        proof_id = proof_refs.get("proof_id")
        proof_hash = proof_hash or proof_refs.get("proof_hash")

    return {
        "proof_id": str(proof_id) if proof_id else None,
        "proof_hash": str(proof_hash) if proof_hash else None,
    }


def _build_span_mapping(obj: Dict[str, object]) -> Dict[str, object]:
    if "span_mapping" in obj and isinstance(obj["span_mapping"], dict):
        return obj["span_mapping"]
    return {
        "smp_section": obj.get("smp_section", "unknown"),
        "clause_range": obj.get("clause_range", "unknown"),
    }


def _derive_polarity(obj: Dict[str, object]) -> str:
    candidate = str(obj.get("polarity") or obj.get("verdict") or "proven_true").lower()
    if candidate in {"proven_true", "true", "yes"}:
        return "proven_true"
    if candidate in {"proven_false", "false", "no"}:
        return "proven_false"
    return "proven_true"


def _tag_append_artifact(aa_payload: Dict[str, object]) -> Dict[str, object]:
    if "PROVISIONAL_PROOF_TAG" in aa_payload:
        return aa_payload

    content = aa_payload.get("content") if isinstance(aa_payload.get("content"), dict) else {}
    if not _contains_pxl_fragments(content) and not _contains_pxl_fragments(aa_payload):
        return aa_payload

    refs = _extract_proof_refs(content) if content else _extract_proof_refs(aa_payload)
    if not refs.get("proof_id") and not refs.get("proof_hash"):
        return aa_payload

    tag = {
        "proof_id": refs.get("proof_id"),
        "proof_hash": refs.get("proof_hash"),
        "polarity": _derive_polarity(content or aa_payload),
        "span_mapping": _build_span_mapping(content or aa_payload),
        "confidence_uplift": 0.05,
        "status": PROVISIONAL_STATUS,
        "disclaimer": PROVISIONAL_DISCLAIMER,
    }

    aa_payload["PROVISIONAL_PROOF_TAG"] = tag
    return aa_payload


def _apply_provisional_proof_tagging(payload: object) -> object:
    try:
        if not isinstance(payload, dict):
            return payload
        if _payload_is_smp(payload):
            return payload

        if {"aa_id", "aa_type"}.issubset(payload.keys()):
            return _tag_append_artifact(payload)

        for key in ("append_artifact", "append_artifacts", "aa", "aa_list"):
            if key in payload:
                aa_block = payload.get(key)
                if isinstance(aa_block, dict):
                    payload[key] = _tag_append_artifact(aa_block)
                elif isinstance(aa_block, list):
                    payload[key] = [
                        _tag_append_artifact(item) if isinstance(item, dict) else item
                        for item in aa_block
                    ]
        return payload
    except Exception:
        return payload

from .bayes_update_real_time import resolve_priors_path, run_BERT_pipeline
from .bayesian_inferencer import BayesianTrinityInferencer
from .bayesian_recursion import BayesianMLModel
from .hierarchical_bayes_network import execute_HBN
# from .mcmc_engine import example_model, run_mcmc_model


class BayesianNexus:
    def __init__(self, priors_path: str):
        resolved = resolve_priors_path(priors_path)
        self.priors_path = resolved
        self.inferencer = BayesianTrinityInferencer(prior_path=str(resolved))
        self.recursion_model = BayesianMLModel()

    def run_real_time(self, query: str) -> Dict:
        try:
            ok, log = run_BERT_pipeline(self.priors_path, query)
            return _apply_provisional_proof_tagging({"output": {"success": ok, "log": log}, "error": None})
        except Exception:
            return _apply_provisional_proof_tagging({"output": None, "error": traceback.format_exc()})

    def run_inferencer(self, query: str) -> Dict:
        try:
            res = self.inferencer.infer(query.split())
            return _apply_provisional_proof_tagging({"output": res, "error": None})
        except Exception:
            return _apply_provisional_proof_tagging({"output": None, "error": traceback.format_exc()})

    def run_hbn(self, query: str) -> Dict:
        try:
            res = execute_HBN(query)
            # ensure only numeric prediction
            pred = float(res.get("prediction", 0.0))
            return _apply_provisional_proof_tagging({"output": {"prediction": pred}, "error": None})
        except Exception:
            return _apply_provisional_proof_tagging({"output": None, "error": traceback.format_exc()})

    def run_recursion(self, evidence: Dict) -> Dict:
        try:
            pred = self.recursion_model.update_belief("hypothesis", evidence)
            return _apply_provisional_proof_tagging({"output": {"prediction": pred.prediction}, "error": None})
        except Exception:
            return _apply_provisional_proof_tagging({"output": None, "error": traceback.format_exc()})

    # def run_mcmc(self) -> Dict:
    #     try:
    #         trace = run_mcmc_model(example_model)
    #         return {
    #             "output": {"n_samples": len(getattr(trace, "posterior", []))},
    #             "error": None,
    #         }
    #     except Exception:
    #         return {"output": None, "error": traceback.format_exc()}

    def run_pipeline(self, query: str) -> List[Dict]:
        report = []
        # Stage 1: Real-Time
        r1 = self.run_real_time(query)
        report.append({"stage": "real_time", **r1})

        # Stage 2: Inferencer
        r2 = self.run_inferencer(query)
        report.append({"stage": "inferencer", **r2})

        # Stage 3: HBN
        r3 = self.run_hbn(query)
        report.append({"stage": "hbn", **r3})

        # Stage 4: Recursion (uses trinity from inferencer)
        evidence = r2["output"] if r2["output"] else {}
        r4 = self.run_recursion(evidence)
        report.append({"stage": "recursion", **r4})

        # Stage 5: MCMC
        r5 = self.run_mcmc()
        report.append({"stage": "mcmc", **r5})

        return report


if __name__ == "__main__":
    import pprint
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bayesian_nexus.py '<query>'")
        sys.exit(1)

    query = sys.argv[1]
    resolved_priors = resolve_priors_path("config/bayes_priors.json")
    nexus = BayesianNexus(priors_path=str(resolved_priors))
    result = nexus.run_pipeline(query)
    pprint.pprint(result)
    # Optionally write to JSON
    with open("bayesian_nexus_report.json", "w") as f:
        json.dump(result, f, indent=2)

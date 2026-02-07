# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: fractal_nexus
runtime_layer: inferred
role: inferred
agent_binding: None
protocol_binding: None
boot_phase: inferred
expected_imports: []
provides: []
depends_on_runtime_state: False
failure_mode:
  type: unknown
  notes: ""
rewrite_provenance:
  source: System_Stack/Synthetic_Cognition_Protocol/MVS_System/predictors/fractal_nexus.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

"""
fractal_nexus.py

Toolkit-level Nexus orchestrator for Fractal Orbital Predictor.
"""
import json
import traceback
from typing import Dict, List, Optional, Tuple


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

# Optional dependency guard: LOGOS_AGI may be absent in minimal environments.
try:
    from LOGOS_AGI.Synthetic_Cognition_Protocol.MVS_System.fractal_orbital.predictors.class_fractal_orbital_predictor import (  # type: ignore
        TrinityPredictionEngine,
    )
    from LOGOS_AGI.Synthetic_Cognition_Protocol.MVS_System.predictors.divergence_calculator import (  # type: ignore
        DivergenceEngine,
    )
except ImportError:
    class TrinityPredictionEngine:  # pragma: no cover - stub placeholder
        def __init__(self, *_args, **_kwargs):
            raise ImportError("LOGOS_AGI is not available in this environment")

        def predict(self, *_args, **_kwargs):
            raise ImportError("LOGOS_AGI is not available in this environment")

    class DivergenceEngine:  # pragma: no cover - stub placeholder
        def analyze_divergence(self, *_args, **_kwargs):
            raise ImportError("LOGOS_AGI is not available in this environment")

try:
    from LOGOS_AGI.Synthetic_Cognition_Protocol.BDN_System.core.fractal_orbital_node_generator import (
        FractalNodeGenerator,
    )
except ImportError:  # pragma: no cover - fallback to sibling import when package path absent
    try:
        from Synthetic_Cognition_Protocol.BDN_System.core.fractal_orbital_node_generator import (
            FractalNodeGenerator,
        )
    except ImportError:
        class FractalNodeGenerator:  # pragma: no cover - stub placeholder
            def __init__(self, *_args, **_kwargs):
                raise ImportError("FractalNodeGenerator is not available")

            def generate(self, *_args, **_kwargs):
                raise ImportError("FractalNodeGenerator is not available")

try:
    from LOGOS_AGI.Synthetic_Cognition_Protocol.MVS_System.predictors.orbital_recursion_engine import (
        OntologicalSpace,
    )
except ImportError:  # pragma: no cover - fallback to relative import when executed as script
    try:
        from Synthetic_Cognition_Protocol.MVS_System.predictors.orbital_recursion_engine import (
            OntologicalSpace,
        )
    except ImportError:
        class OntologicalSpace:  # pragma: no cover - stub placeholder
            def __init__(self, *_args, **_kwargs):
                raise ImportError("OntologicalSpace is not available")

            def compute_fractal_position(self, *_args, **_kwargs):
                raise ImportError("OntologicalSpace is not available")

class FractalNexus:
    def __init__(self, prior_path: str):
        self.predictor = TrinityPredictionEngine(prior_path)
        self.divergence = DivergenceEngine()
        self.generator = FractalNodeGenerator()
        self.mapper    = OntologicalSpace()

    def run_predict(self, keywords: List[str]) -> Dict:
        try:
            res = self.predictor.predict(keywords)
            return _apply_provisional_proof_tagging({'output': res, 'error': None})
        except Exception:
            return _apply_provisional_proof_tagging({'output': None, 'error': traceback.format_exc()})

    def run_divergence(self, trinity_vector: Tuple[float, float, float]) -> Dict:
        try:
            variants = self.divergence.analyze_divergence(trinity_vector)
            return _apply_provisional_proof_tagging({'output': variants, 'error': None})
        except Exception:
            return _apply_provisional_proof_tagging({'output': None, 'error': traceback.format_exc()})

    def run_generate(self, c_value: complex) -> Dict:
        try:
            nodes = self.generator.generate(c_value)
            return _apply_provisional_proof_tagging({'output': nodes, 'error': None})
        except Exception:
            return _apply_provisional_proof_tagging({'output': None, 'error': traceback.format_exc()})

    def run_map(self, query_vector: Tuple[float, float, float]) -> Dict:
        try:
            pos = self.mapper.compute_fractal_position(query_vector)
            return _apply_provisional_proof_tagging({'output': pos, 'error': None})
        except Exception:
            return _apply_provisional_proof_tagging({'output': None, 'error': traceback.format_exc()})

    def run_pipeline(self, keywords: List[str]) -> List[Dict]:
        report = []
        # 1) Predict
        p = self.run_predict(keywords)
        report.append({'step': 'predict', **p})
        if p['error'] or not p['output']:
            return report

        # Extract trinity & c_value
        trinity = p['output'].get('trinity')
        c_val   = p['output'].get('c_value')

        # 2) Divergence on trinity
        d = self.run_divergence(trinity)
        report.append({'step': 'divergence', **d})

        # 3) Generate nodes from c_value
        try:
            # convert c_value string to complex if needed
            c = complex(c_val) if isinstance(c_val, str) else c_val
        except:
            c = c_val
        g = self.run_generate(c)
        report.append({'step': 'generate', **g})

        # 4) Map trinity -> position (using first variant if available)
        if d['output']:
            first_tv = d['output'][0].get('trinity_vector')
            m = self.run_map(first_tv)
            report.append({'step': 'map', **m})

        return report

if __name__ == '__main__':
    import sys
    import pprint

    if len(sys.argv) < 3:
        print("Usage: python fractal_nexus.py <prior_path> <keyword1> [keyword2 ...]")
        sys.exit(1)

    prior = sys.argv[1]
    keywords = sys.argv[2:]
    nexus = FractalNexus(prior)
    result = nexus.run_pipeline(keywords)
    pprint.pprint(result)
    with open('fractal_nexus_report.json', 'w') as f:
        json.dump(result, f, indent=2)

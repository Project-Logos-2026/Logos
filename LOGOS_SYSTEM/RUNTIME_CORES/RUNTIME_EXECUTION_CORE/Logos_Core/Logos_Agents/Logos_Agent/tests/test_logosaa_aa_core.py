
import pytest

@pytest.fixture(autouse=True)
def _inject_example_family(monkeypatch):
    from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.I2_Agent.I2_Agent_Tools import aa as aa_module

    def _mock_load_semantic_projection_families():
        return {"EXAMPLE_FAMILY": {}}

    monkeypatch.setattr(
        aa_module,
        "_load_semantic_projection_families",
        _mock_load_semantic_projection_families,
    )
import pytest
import os
import json
from pathlib import Path

@pytest.fixture
def example_family_fixture(monkeypatch):
    """
    Inject EXAMPLE_FAMILY into a test-scoped manifest copy.
    Does NOT modify canonical manifest file.
    """
    # Locate canonical manifest
    manifest_path = None
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "Semantic_Projection_Manifest.json":
                manifest_path = os.path.join(root, file)
    if not manifest_path:
        raise RuntimeError("Semantic_Projection_Manifest.json not found")
    with open(manifest_path, "r", encoding="utf-8") as mf:
        manifest = json.load(mf)
    # Inject EXAMPLE_FAMILY into copy only
    manifest_copy = dict(manifest)
    families = dict(manifest_copy.get("families", {}))
    families["EXAMPLE_FAMILY"] = {}
    manifest_copy["families"] = families
    # Monkeypatch loader if identifiable
    try:
        import aa
        monkeypatch.setattr(aa, "_load_semantic_projection_families", lambda: families)
    except Exception:
        pass
    return manifest_copy
import time
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Agents.Logos_Agent.Logos_Agent_Tools.logos_aa_builder import build_logos_aa

def minimal_smp():
    return {"id": "SMP-LOGOS-001", "data": {"foo": "bar"}}

def test_logosaa_promotion_and_rejection():
    smp = minimal_smp()
    bound_smp_id = smp["id"]
    bound_smp_hash = "dummyhash1234567890abcdef"
    source_aa_ids = ["AA-1", "AA-2"]
    # Promotion (CANONICAL)
    aa_prom = build_logos_aa(
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        decision_type="promotion",
        source_aa_ids=source_aa_ids,
        resulting_state="CANONICAL",
        semantic_projection=[],
        proof_coverage="FULLY_PROVEN"
    )
    # Rejection (REJECTED)
    aa_rej = build_logos_aa(
        bound_smp_id=bound_smp_id,
        bound_smp_hash=bound_smp_hash,
        decision_type="rejection",
        source_aa_ids=source_aa_ids,
        resulting_state="REJECTED",
        semantic_projection=["EXAMPLE_FAMILY"],
        proof_coverage="PROVEN_FALSE"
    )
    required_keys = [
        "aa_id", "aa_type", "aa_origin_type", "originating_entity", "bound_smp_id", "bound_smp_hash", "creation_timestamp", "aa_hash", "classification_state", "promotion_context", "origin_signature", "cross_validation_signatures", "verification_stage", "metadata_header", "content", "diff_references"
    ]
    for aa, state, proof, sem_proj, vstage in [
        (aa_prom, "canonical", "FULLY_PROVEN", [], "pre-canonicalization"),
        (aa_rej, "rejected", "PROVEN_FALSE", ["EXAMPLE_FAMILY"], "pre-canonicalization")
    ]:
        for k in required_keys:
            assert k in aa, f"Missing AA_CORE key: {k}"
        assert aa["aa_type"] == "LogosAA"
        assert aa["classification_state"] == state
        assert aa["verification_stage"] == vstage
        header = aa["metadata_header"]
        assert header["epistemic_status"] == state.upper()
        assert header["proof_coverage"] == proof
        assert isinstance(header["semantic_projection"], list)
        if sem_proj:
            assert header["semantic_projection"] == [x.upper() for x in sem_proj]
        else:
            assert header["semantic_projection"] == []

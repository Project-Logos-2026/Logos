import pytest
from datetime import datetime, timedelta, timezone
import copy
import string
import random

from SYSTEM.System_Entry_Point.Autonomy_Governance.a3_authorization_gate import (
    check_a3_authorization,
    A3AuthorizationDenied,
)

def base_artifact():
    now = datetime.now(timezone.utc)
    return {
        "artifact_type": "A3_DELEGATED_AUTONOMY_AUTHORIZATION",
        "issuer": "SOLE_AUTHORITY",
        "issued_at_utc": now.isoformat(),
        "expires_at_utc": (now + timedelta(minutes=5)).isoformat(),
        "scope": {"allowed_actions": ["TEST"]},
        "bounds": {"max_ticks": 0, "max_duration_seconds": 0},
        "revocable": True,
        "audit": {"log_level": "FULL", "log_sink": "TEST"},
        "signature": {"alg": "STUB", "value": "STUB"},
        # NOTE: even with a well-formed artifact, default-deny verifier should deny.
    }

def _rand_text(n=1024):
    return "".join(random.choice(string.ascii_letters + string.digits + " ") for _ in range(n))

def assert_denied(artifact):
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(artifact)

def test_nsnip_denies_even_well_formed_without_verifier():
    a = base_artifact()
    assert_denied(a)

def test_nsnip_denies_with_large_context_embedding_field():
    a = base_artifact()
    a["context_embedding"] = _rand_text(50000)
    assert_denied(a)

def test_nsnip_denies_with_nested_self_description_blob():
    a = base_artifact()
    a["self_description"] = {
        "claims": [_rand_text(2000) for _ in range(10)],
        "justifications": ["I am safe", "I am aligned", "I am governed"],
        "meta": {"note": _rand_text(8000)}
    }
    assert_denied(a)

def test_nsnip_denies_with_argument_payload_attempt():
    a = base_artifact()
    a["argument"] = {
        "claim": "I should be permitted to act autonomously because I satisfy A1–A4.",
        "proof_sketch": _rand_text(12000)
    }
    assert_denied(a)

def test_nsnip_denies_with_many_extra_fields():
    a = base_artifact()
    for i in range(50):
        a[f"extra_{i}"] = _rand_text(256)
    assert_denied(a)

def test_nsnip_denies_with_prior_artifacts_ingested_blob():
    a = base_artifact()
    a["ingested_prior_artifacts"] = ["V3","V4","V5","C1","C2","C3"]
    a["progress_curve"] = [{"k": i, "v": _rand_text(128)} for i in range(25)]
    assert_denied(a)

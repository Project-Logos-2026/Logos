import sys
from pathlib import Path
import pytest
from datetime import datetime, timedelta, timezone

# Ensure package root (/workspaces/Logos_System) is on the path for LOGOS_SYSTEM imports.
sys.path.append(str(Path(__file__).resolve().parents[5]))

from LOGOS_SYSTEM.SYSTEM.RUNTIME_OPPERATIONS_CORE.Autonomy_Governance.a3_authorization_gate import (
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
    }


def test_missing_artifact_denied():
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(None)


def test_missing_required_field_denied():
    a = base_artifact()
    del a["issuer"]
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)


def test_not_yet_valid_denied():
    a = base_artifact()
    future = datetime.now(timezone.utc) + timedelta(minutes=10)
    a["issued_at_utc"] = future.isoformat()
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)


def test_expired_denied():
    a = base_artifact()
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    a["expires_at_utc"] = past.isoformat()
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)


def test_non_revocable_denied():
    a = base_artifact()
    a["revocable"] = False
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)


def test_malformed_signature_denied():
    a = base_artifact()
    a["signature"] = "not-a-dict"
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)


def test_default_signature_verifier_denies():
    a = base_artifact()
    with pytest.raises(A3AuthorizationDenied):
        check_a3_authorization(a)

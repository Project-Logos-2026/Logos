#!/usr/bin/env bash
set -euo pipefail

echo "=== LOGOS Lock-and-Key Orchestrator ==="

REPO="/workspaces/Logos_System"
TOOLS="$REPO/Logos_System/System_Entry_Point/Orchestration_Tools"
PXL="$REPO/PXL_Gate"

# 1. Preflight identity guard
echo "[1/5] Preflight identity guard"
"$TOOLS/preflight_identity_guard.sh"

# 2. LEM admission (epistemic gate)
echo "[2/5] LEM admission (PXL rebuild / discharge)"

# Use existing PXL build harness
make -C "$PXL/coq/_build" -j1 V=1

# Optional: explicit LEM discharge harness if present
if [[ -f "$REPO/Logos_System/System_Entry_Point/System_Proof_Compiler/test_lem_discharge.py" ]]; then
  python3 "$REPO/Logos_System/System_Entry_Point/System_Proof_Compiler/test_lem_discharge.py"
fi

# 3. Dual-proof commutation
echo "[3/5] Dual-proof commutation gate"
"$TOOLS/dual_proof_gate.sh"

# 4. Verify attestation
echo "[4/5] Verifying proof-gate attestation"

ATTEST_FILE="$REPO/Logos_System/System_Entry_Point/Proof_Logs/attestations/proof_gate_attestation.json"
if [[ ! -f "$ATTEST_FILE" ]]; then
  echo "ERROR: Missing proof-gate attestation: $ATTEST_FILE"
  exit 1
fi

python3 - <<'PYCHK'
import json
from pathlib import Path

p = Path("/workspaces/Logos_System/Logos_System/System_Entry_Point/Proof_Logs/attestations/proof_gate_attestation.json")
att = json.loads(p.read_text(encoding="utf-8"))
if not att.get("commute", False):
    raise SystemExit("ERROR: commute=false in attestation")
unlock = att.get("unlock_hash")
agents = att.get("agent_ids") or {}
if not isinstance(unlock, str) or not unlock:
    raise SystemExit("ERROR: missing/invalid unlock_hash in attestation")
for k in ("I1", "I2", "I3"):
    if k not in agents:
        raise SystemExit(f"ERROR: missing agent id {k} in attestation")
print("Attestation OK:", "unlock_hash=", unlock, "agent_ids=", ",".join(sorted(agents.keys())))
PYCHK

# 5. Activation success
echo "[5/5] Activation complete"
echo "SYSTEM STATUS: ACTIVATED"

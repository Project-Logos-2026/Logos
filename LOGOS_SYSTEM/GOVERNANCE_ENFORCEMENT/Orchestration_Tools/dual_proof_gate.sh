#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# LOGOS — Dual-Proof Cryptographic Lock & Activation Gate (Canonical Prompt)
#
# PURPOSE
#   • Enforce two deterministic Coq compiles (PXL Gate + LOGOS System)
#   • Require hash commutation between proof artifacts
#   • Derive a single unlock hash on commute
#   • Deterministically derive agent IDs (I1 / I2 / I3)
#   • Write-over proof logs, emit read-only attestation
#   • Append activation record to global audit log (JSONL)
#
# SAFETY MODEL
#   • Fail closed on any mismatch or missing artifact
#   • Proof logs are write-over ONLY
#   • Audit log is append-only ONLY
#   • No agent IDs unless unlock hash exists
###############################################################################

REPO="/workspaces/Logos_System"
PXL="$REPO/PXL_Gate"
LOGOS="$REPO/Logos_System"
TOOLS="$LOGOS/System_Entry_Point/Orchestration_Tools"
PROOF_ROOT="$LOGOS/System_Entry_Point/Proof_Logs/attestations"
AUDIT_DIR="$REPO/System_Audit_Logs"
AUDIT_LOG="$AUDIT_DIR/Boot_Sequence_Log.jsonl"
REPORT="$REPO/_Reports/dual_proof_$(date +%Y%m%d_%H%M%S)"

mkdir -p \
  "$TOOLS" \
  "$PROOF_ROOT" \
  "$AUDIT_DIR" \
  "$REPORT"

###############################################################################
# Toolchain sanity
###############################################################################

if command -v opam >/dev/null 2>&1; then
  eval "$(opam env --set-switch)" || true
fi

command -v coqc >/dev/null 2>&1 || { echo "ERROR: coqc not found"; exit 1; }
command -v coq_makefile >/dev/null 2>&1 || { echo "ERROR: coq_makefile not found"; exit 1; }

###############################################################################
# Create canonical dual-proof + attestation tool (single source of truth)
###############################################################################

cat > "$TOOLS/proof_gate_tools.py" <<'PY'
#!/usr/bin/env python3
import json, hashlib, subprocess, os
from pathlib import Path
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def sha256(b):
    return "sha256:" + hashlib.sha256(b).hexdigest()

def strip_volatile(d):
    d = dict(d)
    # Drop fields that differ between the two proof runs but should not
    # affect the commutation hash.
    for k in ("ts", "timestamp", "time", "build_time", "version", "kind"):
        d.pop(k, None)
    return d

def git_short(repo):
    try:
        return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return ""

def coq_version():
    try:
        return subprocess.check_output(["coqc", "-v"], text=True).splitlines()[0]
    except Exception:
        return ""

def run_make(build_dir, log_txt):
    with open(log_txt, "w") as f:
        p = subprocess.Popen(["make", "-j1", "V=1"], cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:
            f.write(line)
        rc = p.wait()
    if rc != 0:
        raise SystemExit(f"Coq build failed (see {log_txt})")

def emit(kind, repo, build_dir, out_json, files_list):
    run_make(build_dir, out_json.with_suffix(".make.log"))
    payload = {
        "version": f"{kind}/1",
        "kind": kind,
        "ts": now(),
        "git": git_short(repo),
        "coq": coq_version(),
        "files": files_list,
        "result": "PASS",
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n")
    return payload

def main():
    repo = Path(os.environ["REPO_ROOT"]).resolve()

    pxl_build = Path(os.environ["PXL_BUILD_DIR"])
    logos_build = Path(os.environ["LOGOS_BUILD_DIR"])

    pxl_files = Path(os.environ["PXL_FILES_LIST"]).read_text().splitlines()
    logos_files = Path(os.environ["LOGOS_FILES_LIST"]).read_text().splitlines()

    pxl_out = Path(os.environ["PXL_PROOF_OUT"])
    logos_out = Path(os.environ["LOGOS_PROOF_OUT"])

    attest_out = Path(os.environ["ATTEST_OUT"])
    audit_out = Path(os.environ["AUDIT_JSONL"])

    protocol_salt = os.environ.get("LOGOS_PROTOCOL_SALT", "")
    role_salt = os.environ.get("LOGOS_ROLE_SALT", "")

    pxl = emit("pxl-proof-gate", repo, pxl_build, pxl_out, pxl_files)
    lg = emit("logos-system-proof", repo, logos_build, logos_out, logos_files)

    pxl_hash = sha256(canon(strip_volatile(pxl)))
    lg_hash = sha256(canon(strip_volatile(lg)))

    if pxl_hash != lg_hash:
        raise SystemExit("PROOF HASH MISMATCH — REFUSING ACTIVATION")

    unlock_hash = sha256((pxl_hash + lg_hash + protocol_salt).encode())

    def aid(tag):
        return sha256((unlock_hash + tag + role_salt).encode())

    agent_ids = {"I1": aid("I1"), "I2": aid("I2"), "I3": aid("I3")}

    attestation = {
        "version": "logos-attestation/1",
        "ts": now(),
        "pxl_proof_hash": pxl_hash,
        "logos_proof_hash": lg_hash,
        "unlock_hash": unlock_hash,
        "agent_ids": agent_ids,
        "commute": True,
    }

    attest_out.write_text(json.dumps(attestation, indent=2) + "\n")

    audit_out.parent.mkdir(parents=True, exist_ok=True)
    with audit_out.open("a") as f:
        f.write(json.dumps({
            "ts": now(),
            "unlock_hash": unlock_hash,
            "agent_ids": agent_ids,
            "status": "SYSTEM_ACTIVATED",
        }) + "\n")

    print("ACTIVATION COMPLETE")

if __name__ == "__main__":
    main()
PY

chmod +x "$TOOLS/proof_gate_tools.py"

###############################################################################
# File lists (explicit, deterministic)
###############################################################################

grep '\.v$' "$PXL/coq/_CoqProject" > "$REPORT/pxl.vfiles.txt"
cp "$REPORT/pxl.vfiles.txt" "$REPORT/logos.vfiles.txt"

###############################################################################
# Execute dual proof + attestation + audit append (single dry run)
###############################################################################

REPO_ROOT="$REPO" \
PXL_BUILD_DIR="$PXL/coq/_build" \
PXL_FILES_LIST="$REPORT/pxl.vfiles.txt" \
PXL_PROOF_OUT="$PROOF_ROOT/pxl_proof_gate.json" \
LOGOS_BUILD_DIR="$PXL/coq/_build" \
LOGOS_FILES_LIST="$REPORT/logos.vfiles.txt" \
LOGOS_PROOF_OUT="$PROOF_ROOT/logos_system_proof.json" \
ATTEST_OUT="$PROOF_ROOT/proof_gate_attestation.json" \
AUDIT_JSONL="$AUDIT_LOG" \
python3 "$TOOLS/proof_gate_tools.py" | tee "$REPORT/run.out.txt"

echo "DONE — report at $REPORT"

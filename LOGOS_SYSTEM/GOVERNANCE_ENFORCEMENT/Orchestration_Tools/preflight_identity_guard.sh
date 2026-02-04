#!/usr/bin/env bash
set -euo pipefail

REPO="/workspaces/Logos_System"
GUARD="$REPO/Logos_System/System_Entry_Point/Orchestration_Tools/pxl_identity_guard.sh"

PXL_SRC="$REPO/PXL_Gate/coq/src"
 RUNTIME_SRC="$REPO/Logos_System/System_Entry_Point/Runtime_Compiler/coq/src"

if [[ ! -x "$GUARD" ]]; then
  echo "ERROR: identity guard not found or not executable"
  exit 1
fi

echo "Running PXL ↔ Runtime compiler identity guard..."
"$GUARD" "$PXL_SRC" "$RUNTIME_SRC"

echo "Identity guard passed. Proceeding to dual proof gate."

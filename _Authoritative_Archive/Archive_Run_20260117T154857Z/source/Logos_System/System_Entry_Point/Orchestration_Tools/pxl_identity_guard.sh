#!/usr/bin/env bash
set -euo pipefail

PXL_SRC="$1"
RUNTIME_SRC="$2"

if [[ ! -d "$PXL_SRC" || ! -d "$RUNTIME_SRC" ]]; then
  echo "ERROR: One or both proof source directories missing"
  exit 1
fi

diff -rq "$PXL_SRC" "$RUNTIME_SRC" >/dev/null || {
  echo "ERROR: PXL Gate and Runtime Compiler sources have diverged"
  exit 1
}

echo "OK: PXL Gate and Runtime Compiler sources are identical"

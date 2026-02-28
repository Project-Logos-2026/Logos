#!/usr/bin/env bash
set -euo pipefail

STARTUP_FILES=(
  "STARTUP/LOGOS_SYSTEM.py"
  "LOGOS_SYSTEM/System_Entry_Point/System_Entry_Point.py"
  "LOGOS_SYSTEM/Runtime_Spine/Lock_And_Key/lock_and_key.py"
  "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/Logos_Agent_Core/Start_Logos_Agent.py"
  "LOGOS_SYSTEM/RUNTIME_CORES/RUNTIME_EXECUTION_CORE/Logos_Core/Logos_Agents/Logos_Agent/Logos_Agent_Core/Lem_Discharge.py"
  "LOGOS_SYSTEM/System_Entry_Point/Agent_Orchestration/agent_orchestration.py"
)

FAIL=0
for f in "${STARTUP_FILES[@]}"; do
  if grep -n 'print(' "$f" >/dev/null; then
    echo "FAIL: print() in $f"
    FAIL=1
  fi
done

if [[ "$FAIL" -ne 0 ]]; then
  exit 1
fi

grep -RIn --include="*.py" 'print(' LOGOS_SYSTEM STARTUP || true

import sys
import os
import json
import inspect
from pathlib import Path

REPORT_DIR = Path("_Reports/Phase6_Runtime_CallGraph")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CALL_TRACE_RAW = []
CALL_GRAPH = set()
DRAC_TOUCHPOINTS = set()
RUNTIME_BRIDGE_TOUCHPOINTS = set()
AGENT_BOOT_SEQUENCE = set()

MODULE_LOAD_BEFORE = set(sys.modules.keys())

# Utility

def is_logos_system_file(filename):
    return filename and "LOGOS_SYSTEM" in filename and "site-packages" not in filename and "lib/python" not in filename

def trace_func(frame, event, arg):
    if event != "call":
        return
    try:
        caller = frame.f_back
        callee = frame
        caller_file = caller.f_code.co_filename if caller else None
        callee_file = callee.f_code.co_filename
        if not is_logos_system_file(callee_file):
            return
        caller_mod = inspect.getmodule(caller)
        callee_mod = inspect.getmodule(callee)
        caller_mod_name = caller_mod.__name__ if caller_mod else None
        callee_mod_name = callee_mod.__name__ if callee_mod else None
        caller_func = caller.f_code.co_name if caller else None
        callee_func = callee.f_code.co_name
        edge = {
            "caller_module": caller_mod_name,
            "caller_function": caller_func,
            "callee_module": callee_mod_name,
            "callee_function": callee_func,
            "file": callee_file,
            "line": callee.f_lineno
        }
        CALL_TRACE_RAW.append(edge)
        CALL_GRAPH.add((caller_mod_name, caller_func, callee_mod_name, callee_func))
        if callee_mod_name and "DRAC" in callee_mod_name:
            DRAC_TOUCHPOINTS.add((callee_mod_name, callee_func, callee_file, callee.f_lineno))
        if callee_mod_name and "RUNTIME_BRIDGE" in callee_mod_name:
            RUNTIME_BRIDGE_TOUCHPOINTS.add((callee_mod_name, callee_func, callee_file, callee.f_lineno))
        if callee_mod_name and "Logos_Agent" in callee_mod_name:
            AGENT_BOOT_SEQUENCE.add((callee_mod_name, callee_func, callee_file, callee.f_lineno))
    except Exception:
        pass
    return trace_func

sys.setprofile(trace_func)

# Invoke START_LOGOS programmatically
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("START_LOGOS", str(Path("STARTUP/START_LOGOS.py")))
    start_logos = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(start_logos)
    start_logos.main()
except Exception as e:
    sys.setprofile(None)
    print(f"Runtime spine invocation failed: {e}", file=sys.stderr)
    sys.exit(1)

sys.setprofile(None)
MODULE_LOAD_AFTER = set(sys.modules.keys())
MODULE_LOAD_DIFF = sorted([m for m in MODULE_LOAD_AFTER - MODULE_LOAD_BEFORE if "LOGOS_SYSTEM" in m])

# Write artifacts
with open(REPORT_DIR/"PHASE6B_EXECUTION_CALL_TRACE_RAW.json", "w", encoding="utf-8") as f:
    json.dump(sorted(CALL_TRACE_RAW, key=lambda x: (x["caller_module"] or "", x["caller_function"] or "", x["callee_module"] or "", x["callee_function"] or "", x["file"])), f, indent=2)
with open(REPORT_DIR/"PHASE6B_EXECUTION_CALL_GRAPH.json", "w", encoding="utf-8") as f:
    json.dump(sorted([{
        "caller_module": c[0], "caller_function": c[1], "callee_module": c[2], "callee_function": c[3]
    } for c in CALL_GRAPH], key=lambda x: (x["caller_module"] or "", x["caller_function"] or "", x["callee_module"] or "", x["callee_function"] or "")), f, indent=2)
with open(REPORT_DIR/"PHASE6B_MODULE_LOAD_SEQUENCE.json", "w", encoding="utf-8") as f:
    json.dump(MODULE_LOAD_DIFF, f, indent=2)
with open(REPORT_DIR/"PHASE6B_DRAC_TOUCHPOINTS.json", "w", encoding="utf-8") as f:
    json.dump(sorted([{
        "module": t[0], "function": t[1], "file": t[2], "line": t[3]
    } for t in DRAC_TOUCHPOINTS], key=lambda x: (x["module"] or "", x["function"] or "", x["file"])), f, indent=2)
with open(REPORT_DIR/"PHASE6B_RUNTIME_BRIDGE_TOUCHPOINTS.json", "w", encoding="utf-8") as f:
    json.dump(sorted([{
        "module": t[0], "function": t[1], "file": t[2], "line": t[3]
    } for t in RUNTIME_BRIDGE_TOUCHPOINTS], key=lambda x: (x["module"] or "", x["function"] or "", x["file"])), f, indent=2)
with open(REPORT_DIR/"PHASE6B_AGENT_BOOT_SEQUENCE.json", "w", encoding="utf-8") as f:
    json.dump(sorted([{
        "module": t[0], "function": t[1], "file": t[2], "line": t[3]
    } for t in AGENT_BOOT_SEQUENCE], key=lambda x: (x["module"] or "", x["function"] or "", x["file"])), f, indent=2)

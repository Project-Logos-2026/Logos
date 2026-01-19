# HEADER_TYPE: PRODUCTION_RUNTIME_MODULE
# AUTHORITY: LOGOS_SYSTEM
# GOVERNANCE: ENABLED
# EXECUTION: CONTROLLED
# MUTABILITY: IMMUTABLE_LOGIC
# VERSION: 1.0.0

"""
LOGOS_MODULE_METADATA
---------------------
module_name: ontoprops_remap
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
  source: System_Stack/Logos_Agents/Logos_Agent/module_generator/ontoprops_remap.py
  rewrite_phase: Phase_B
  rewrite_timestamp: 2026-01-18T23:03:31.726474
observability:
  log_channel: None
  metrics: disabled
---------------------
"""

import json
import sys


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    if len(argv) < 2:
        print("[WARN] ontoprops_remap expects: <src> <out>")
        return

    src, out = argv[0], argv[1]

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    props = data.get("properties", {})
    gc = data.get("group_classifications", {})

    # Remap: Will -> Volitional
    if "Will" in props:
        props["Will"]["group"] = "Volitional"

    # Ensure group_classifications reflect the move
    # Remove Will from Causal list if present
    causal = gc.get("Causal", {}).get("properties", [])
    if "Will" in causal:
        causal = [x for x in causal if x != "Will"]
        gc.setdefault("Causal", {})["properties"] = causal

    # Add Will to Volitional list
    vol = gc.setdefault(
        "Volitional",
        {
            "description": "Attributes related to will, choice, and freedom",
            "properties": [],
            "characteristic_goodness_weight": "high",
        },
    )
    if "Will" not in vol.get("properties", []):
        vol.setdefault("properties", []).append("Will")

    # Keep Immanence under Spatial (no change)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("[OK] Remapped Will→Volitional in", out)


if __name__ == '__main__':
    main()

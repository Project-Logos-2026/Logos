import json
import os
import sys

REGISTRY_PATH = os.path.join("LOGOS_SYSTEM", "DRAC", "Registries")

FILES = [
    "DRAC_Meta_Registry.json",
    "AF_Family_Registry.json",
    "Core_Interface_Registry.json",
    "Compatibility_Matrix.json",
    "Injection_Signature_Registry.json",
    "Default_Bindings_Registry.json",
    "Coverage_Map_Registry.json",
]


def load_json(file_name):
    path = os.path.join(REGISTRY_PATH, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing registry file: {file_name}")
    with open(path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def validate_score_range(compatibility):
    for core, clusters in compatibility.items():
        for cluster, score in clusters.items():
            if not isinstance(score, int) or score < 0 or score > 5:
                raise ValueError(f"Invalid score for {core}->{cluster}: {score}")


def validate():
    meta = load_json("DRAC_Meta_Registry.json")
    load_json("AF_Family_Registry.json")
    load_json("Core_Interface_Registry.json")
    comp = load_json("Compatibility_Matrix.json")
    load_json("Injection_Signature_Registry.json")
    load_json("Default_Bindings_Registry.json")
    load_json("Coverage_Map_Registry.json")

    if meta["Global_Invariants"]["Score_Range"] != [0, 5]:
        raise ValueError("Score range invariant mismatch")

    validate_score_range(comp.get("Compatibility", {}))

    print("DRAC Registry Validation: PASS")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"DRAC Registry Validation: FAIL -> {exc}")
        sys.exit(1)

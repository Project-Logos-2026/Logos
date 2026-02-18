import json
from LOGOS_SYSTEM._Governance.Nexus_Validation.Nexus_AST_Validator import NexusASTValidator

if __name__ == "__main__":
    import os
    print("CWD:", os.getcwd())
    validator = NexusASTValidator("LOGOS_SYSTEM")
    result = validator.classify()
    classification = result["Classification"]
    violations = result["Violations"]
    total = result["Total_Nexus_Files"]
    report = {
        "Total_Nexus_Files": total,
        "EXECUTION_NEXUS": sorted(classification["EXECUTION_NEXUS"]),
        "BINDING_NEXUS": sorted(classification["BINDING_NEXUS"]),
        "NON_NEXUS": sorted(classification["NON_NEXUS"]),
        "Violations": {
            "Missing_MRE": sorted(violations["Missing_MRE"]),
            "Multiple_Primary_Classes": sorted(violations["Multiple_Primary_Classes"]),
            "Illegal_Dynamic_Import": sorted(violations["Illegal_Dynamic_Import"]),
            "Boundary_Violation": sorted(violations["Boundary_Violation"])
        }
    }
    os.makedirs("_Reports", exist_ok=True)
    json_path = "_Reports/NEXUS_STRUCTURAL_AUDIT_v1.json"
    output_path = os.path.abspath(json_path)
    print("Resolved output path:", output_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    print(f"Audit report written to {json_path}")
    print("File exists after write:", os.path.exists(output_path))
    print("Directory listing of _Reports:", os.listdir("_Reports"))
    print("Exit code: 0")
    print("Summary counts:")
    print({k: len(v) if isinstance(v, list) else v for k, v in report.items() if k != "Violations"})
    print("First 15 lines of JSON output:")
    with open(json_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < 15:
                print(line.rstrip())
            else:
                break
    file_size = os.path.getsize(json_path)
    print(f"File size: {file_size} bytes")

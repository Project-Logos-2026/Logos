import ast
import os
from pathlib import Path

NEXUS_SUFFIX = '_Nexus.py'

class NexusASTValidator:
    def __init__(self, root):
        self.root = Path(root)
        self.results = []
        self.violations = {
            'Missing_MRE': [],
            'Multiple_Primary_Classes': [],
            'Illegal_Dynamic_Import': [],
            'Boundary_Violation': []
        }

    def scan(self):
        nexus_files = sorted([str(p) for p in self.root.rglob(f'*{NEXUS_SUFFIX}')])
        filtered_files = []
        for file in nexus_files:
            # Exclusion filters
            if "TEST" in file or "TEST_SUITE" in file:
                continue
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    header = f.read(512)
                if "EXECUTION: FORBIDDEN" in header or "LEGACY_REWRITE_CANDIDATE" in header:
                    continue
            except Exception:
                continue
            filtered_files.append(file)
        self.results = []
        for file in filtered_files:
            self.results.append(self.analyze_file(file))
        return self.results

    def analyze_file(self, file):
        try:
            source = Path(file).read_text(encoding='utf-8')
            tree = ast.parse(source)
        except Exception:
            return {'file': file, 'classification': 'INVALID', 'parse_error': True}

        imports = set()
        classes = []
        method_map = {}
        illegal_dynamic = False
        sys_manipulation = False
        execution_marker = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name)
                    if n.name == 'importlib':
                        illegal_dynamic = True
                    if 'metered_reasoning_enforcer' in n.name:
                        execution_marker = True
                    if n.name == 'sys':
                        sys_manipulation = True
            if isinstance(node, ast.ImportFrom):
                if node.module and 'metered_reasoning_enforcer' in node.module:
                    execution_marker = True
                for n in node.names:
                    imports.add(n.name)
                    if node.module == 'importlib':
                        illegal_dynamic = True
                    if n.name == 'MeteredReasoningEnforcer':
                        execution_marker = True
                    if node.module == 'sys':
                        sys_manipulation = True
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in {'__import__', 'exec', 'eval'}:
                        illegal_dynamic = True
                    if node.func.id == 'MeteredReasoningEnforcer':
                        execution_marker = True
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and node.func.value.id == 'importlib' and node.func.attr == 'import_module'):
                        illegal_dynamic = True
                    if node.func.attr == 'MeteredReasoningEnforcer':
                        execution_marker = True
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        if (isinstance(target.value, ast.Name) and target.value.id == 'sys' and target.attr in {'path', 'modules'}):
                            illegal_dynamic = True
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
                method_map[node.name] = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
                    register_present = True
                    ingest_present = True
                if 'process' in method_names:
                    process_present = True
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        for sub in ast.walk(n):
                            if isinstance(sub, ast.Raise):
                                if hasattr(sub.exc, 'func') and isinstance(sub.exc.func, ast.Name):
                                    if sub.exc.func.id in {'NexusViolation', 'MeshRejection', 'MREHalt'}:
                                        fail_closed = True
            if isinstance(node, ast.Raise):
                if hasattr(node.exc, 'func') and isinstance(node.exc.func, ast.Name):
                    raises.add(node.exc.func.id)
                    if node.exc.func.id in {'NexusViolation', 'MeshRejection', 'MREHalt'}:
                        fail_closed = True
            if isinstance(node, ast.Attribute):
                if node.attr in {'path', 'modules'}:
                    sys_manipulation = True

        # Classification
        classification = 'INVALID'
        if len(primary_classes) > 1:
            self.violations['Multiple_Primary_Classes'].append(file)
        if illegal_dynamic or sys_manipulation:
            self.violations['Illegal_Dynamic_Import'].append(file)
        if other_nexus_calls:
            self.violations['Boundary_Violation'].append(file)
        if not mre_present and tick_present:
            self.violations['Missing_MRE'].append(file)

        if tick_present and register_present and ingest_present and mre_present and mesh_present and fail_closed:
            classification = 'TIER_1_EXECUTION'
        elif process_present and fail_closed:
            classification = 'TIER_1_PIPELINE'
        elif tick_present or register_present or ingest_present:
            classification = 'TIER_2_SUBNEXUS'
        elif 'MeshEnforcer' in imports or 'MRE' in imports:
            classification = 'INFRASTRUCTURE'
        else:
            classification = 'INVALID'

        return {
            'file': file,
            'imports': sorted(list(imports)),
            'classes': sorted(classes),
            'calls': sorted(list(calls)),
            'raises': sorted(list(raises)),
            'classification': classification
        }

    def classify(self):
        classification = {
            "EXECUTION_NEXUS": [],
            "BINDING_NEXUS": [],
            "NON_NEXUS": []
        }
        violations = {
            "Missing_MRE": [],
            "Multiple_Primary_Classes": [],
            "Illegal_Dynamic_Import": [],
            "Boundary_Violation": []
        }
        self.scan()
        for r in self.results:
            file = r.get('file', 'UNKNOWN')
            classes = r.get('classes', [])
            method_map = r.get('method_map', {})
            execution_marker = r.get('execution_marker', False)
            # Classification rules
            if execution_marker:
                classification["EXECUTION_NEXUS"].append(file)
            elif 'StandardNexus' in classes and {'tick', 'register_participant', 'ingest'}.issubset(method_map.get('StandardNexus', set())):
                classification["BINDING_NEXUS"].append(file)
            else:
                classification["NON_NEXUS"].append(file)
        for k in violations:
            violations[k] = sorted(set(self.violations.get(k, [])))
        total_files = len(classification["EXECUTION_NEXUS"] + classification["BINDING_NEXUS"] + classification["NON_NEXUS"])
        return {
            "Classification": classification,
            "Violations": violations,
            "Total_Nexus_Files": total_files
        }

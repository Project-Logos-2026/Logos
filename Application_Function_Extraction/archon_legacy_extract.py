#!/usr/bin/env python3
"""
ARCHON PRIME — Legacy Application Function Deep Semantic Extraction
Static Analysis Pipeline (Read-Only)
"""

import ast
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

TARGET_DIR = Path("/workspaces/Logos/_Dev_Resources/STAGING/APPLICATION_FUNCTIONS")
OUT_DIR = Path("/workspaces/Logos/Application_Function_Extraction")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDE_STEMS = {"test", "audit", "nexus", "boot"}

SEMANTIC_VERBS = {
    "infer", "translate", "predict", "gate", "inject", "compose",
    "reconstruct", "score", "select", "validate", "normalize",
    "orchestrate", "bootstrap", "compile", "execute", "resolve",
    "apply", "determine", "analyze", "evaluate", "dispatch",
    "transform", "generate", "compute", "build", "derive",
    "process", "parse", "encode", "decode", "route", "rank",
    "classify", "detect", "extract", "map", "merge", "plan",
    "optimize", "schedule", "emit", "filter", "check",
}

SUBSYSTEM_PATTERNS = {
    "RUNTIME_EXECUTION_CORE": re.compile(r"RUNTIME_EXECUTION_CORE|ARP|MTP|SCP|LP_Core|Logos_Core", re.I),
    "RUNTIME_OPPERATIONS_CORE": re.compile(r"RUNTIME_OPPERATIONS_CORE|CSP|CSP_Core", re.I),
    "RUNTIME_SHARED_UTILS": re.compile(r"RUNTIME_SHARED_UTILS|shared_utils", re.I),
    "MTP_Core": re.compile(r"\bMTP\b|MTP_Core|meaning_translation", re.I),
    "CSP_Core": re.compile(r"\bCSP\b|CSP_Core|cognitive_state", re.I),
    "ARP": re.compile(r"\bARP\b|advanced_reasoning|arp_", re.I),
    "DRAC": re.compile(r"\bDRAC\b", re.I),
    "RGE": re.compile(r"\bRGE\b|radial_genesis", re.I),
    "IEL": re.compile(r"\bIEL\b|epistemic_lib", re.I),
    "PXL": re.compile(r"\bPXL\b|privation_", re.I),
    "BDN": re.compile(r"\bBDN\b|banach_data", re.I),
    "MVS": re.compile(r"\bMVS\b|multi_modal|mvs_", re.I),
    "Agent": re.compile(r"agent_|logos_agent|I2_Agent|I3_Agent", re.I),
    "SMP": re.compile(r"\bSMP\b|smp_", re.I),
}

ROLE_SIGNALS = {
    "semantic inference": ["infer", "inference", "bayesian", "belief", "abductive", "deductive", "inductive"],
    "translation engine": ["translate", "translation", "mtp", "language", "encode", "decode"],
    "runtime orchestration": ["orchestrate", "orchestration", "pipeline", "runner", "coordinator", "dispatch"],
    "state manager": ["state", "persist", "memory", "ledger", "cache", "session"],
    "prediction engine": ["predict", "predictor", "forecast", "temporal", "causal"],
    "safety guard": ["gate", "safety", "validate", "validate", "guard", "constraint", "ethics", "policy"],
    "analysis engine": ["analyze", "analysis", "analyzer", "score", "metric", "evaluate"],
    "utility library": ["util", "helper", "wrapper", "adapter", "schema", "type", "constant"],
    "reasoning engine": ["reason", "reasoning", "logic", "modal", "proof", "axiom", "coherence"],
    "identity/agent core": ["agent", "identity", "consciousness", "principal", "sign"],
}

SALVAGE_CRITERIA_VERBS = {
    "infer", "translate", "predict", "gate", "inject", "compose",
    "reconstruct", "score", "select", "validate", "normalize",
    "orchestrate", "compile", "evaluate", "dispatch", "transform",
    "compute", "derive", "rank", "classify", "optimize", "filter",
}

# Subsystem keywords for cluster assignment
CLUSTER_KEYWORDS = {
    "arp_reasoning": ["arp", "reasoning", "abductive", "deductive", "inductive", "bayesian", "meta_reason"],
    "mtp_translation": ["mtp", "translation", "translate", "language", "encode", "decode", "semantic"],
    "csp_memory": ["csp", "memory", "state", "persist", "recall", "fractal_memory"],
    "agent_identity": ["agent", "identity", "consciousness", "principal", "sign", "axiom_system"],
    "pxl_privation": ["pxl", "privation", "gate", "filter", "privation_classifier"],
    "bdn_mvs": ["bdn", "banach", "mvs", "multi_modal", "fractal_orbit"],
    "tooling": ["tool", "adapter", "wrapper", "export", "introspection", "invention"],
    "safety_validation": ["safety", "validate", "constraint", "ethics", "policy", "guard", "coherence"],
    "orchestration": ["orchestrat", "pipeline", "runner", "coordinator", "dispatch", "scheduler"],
    "prediction_temporal": ["predict", "temporal", "causal", "time_model", "forecast"],
    "utility": ["util", "helper", "schema", "type", "constant", "loader", "registry"],
    "rge_genesis": ["rge", "genesis", "radial", "topology", "divergence"],
    "iel_epistemic": ["iel", "epistemic", "knowledge", "catalog", "ontoprops"],
}


# ---------------------------------------------------------------------------
# HELPER — exclusion
# ---------------------------------------------------------------------------

def should_exclude(path: Path) -> bool:
    stem = path.stem.lower()
    for excl in EXCLUDE_STEMS:
        if excl in stem:
            return True
    return False


# ---------------------------------------------------------------------------
# STEP 1+2 — FILE DISCOVERY + AST PARSING
# ---------------------------------------------------------------------------

class ModuleAnalysis:
    def __init__(self, path: Path):
        self.path = path
        self.rel = str(path.relative_to(TARGET_DIR))
        self.module_name = path.stem
        self.subsystem = path.parent.name  # Agents / Memory / Reasoning / Tooling / Utilities
        self.parse_error = None

        # Extraction results
        self.module_doc = ""
        self.classes = []
        self.functions = []
        self.imports = []
        self.constants = []
        self.decorators = []
        self.type_hints = []
        self.try_except_count = 0
        self.context_manager_count = 0
        self.call_targets = []
        self.comments = []

    def parse(self):
        try:
            source = self.path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            self.parse_error = f"read error: {e}"
            return

        # Extract inline comments
        for line in source.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#"):
                comment = stripped.lstrip("#").strip()
                if len(comment) > 3:
                    self.comments.append(comment)

        try:
            tree = ast.parse(source, filename=str(self.path))
        except SyntaxError as e:
            self.parse_error = f"SyntaxError line {e.lineno}: {e.msg}"
            # Still try to extract comments (done above)
            return
        except Exception as e:
            self.parse_error = str(e)
            return

        self._walk(tree, source)

    def _walk(self, tree, source):
        # Module docstring
        self.module_doc = ast.get_docstring(tree, clean=True) or ""

        for node in ast.walk(tree):

            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    self.imports.append(f"{mod}.{alias.name}" if mod else alias.name)

            # Classes
            elif isinstance(node, ast.ClassDef):
                cls_doc = ast.get_docstring(node, clean=True) or ""
                decs = [self._decorator_name(d) for d in node.decorator_list]
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        m_doc = ast.get_docstring(item, clean=True) or ""
                        m_dec = [self._decorator_name(d) for d in item.decorator_list]
                        args = self._extract_args(item)
                        ret = self._annotation_str(item.returns)
                        methods.append({
                            "name": item.name,
                            "docstring": m_doc,
                            "args": args,
                            "return_type": ret,
                            "decorators": m_dec,
                            "line": item.lineno,
                        })
                        self.decorators.extend(m_dec)
                self.classes.append({
                    "name": node.name,
                    "docstring": cls_doc,
                    "decorators": decs,
                    "methods": methods,
                    "line": node.lineno,
                })
                self.decorators.extend(decs)

            # Top-level functions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Only top-level (parent is Module)
                fn_doc = ast.get_docstring(node, clean=True) or ""
                decs = [self._decorator_name(d) for d in node.decorator_list]
                args = self._extract_args(node)
                ret = self._annotation_str(node.returns)
                self.functions.append({
                    "name": node.name,
                    "docstring": fn_doc,
                    "args": args,
                    "return_type": ret,
                    "decorators": decs,
                    "line": node.lineno,
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                })
                self.decorators.extend(decs)

            # Constants (top-level assignments to ALL_CAPS or typed)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        val = self._const_value(node.value)
                        self.constants.append({"name": target.id, "value": val})
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    ann = self._annotation_str(node.annotation)
                    if ann:
                        self.type_hints.append({"name": node.target.id, "type": ann})

            # Try/except
            elif isinstance(node, ast.Try):
                self.try_except_count += 1

            # With statements
            elif isinstance(node, ast.With):
                self.context_manager_count += 1

            # Call targets
            elif isinstance(node, ast.Call):
                target = self._call_target(node.func)
                if target:
                    self.call_targets.append(target)

    def _decorator_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._decorator_name(node.value)}.{node.attr}"
        if isinstance(node, ast.Call):
            return self._decorator_name(node.func)
        return "<decorator>"

    def _extract_args(self, node) -> list:
        args = []
        for arg in node.args.args:
            ann = self._annotation_str(arg.annotation) if arg.annotation else ""
            args.append({"name": arg.arg, "type": ann})
        return args

    def _annotation_str(self, node) -> str:
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._annotation_str(node.value)}.{node.attr}"
        if isinstance(node, ast.Subscript):
            return f"{self._annotation_str(node.value)}[{self._annotation_str(node.slice)}]"
        if isinstance(node, ast.Constant):
            return str(node.value)
        if isinstance(node, ast.Tuple):
            return ", ".join(self._annotation_str(e) for e in node.elts)
        if isinstance(node, ast.BinOp):
            return f"{self._annotation_str(node.left)} | {self._annotation_str(node.right)}"
        return ""

    def _const_value(self, node) -> str:
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return f"[{len(node.elts)} items]"
        if isinstance(node, ast.Dict):
            return f"{{{len(node.keys)} keys}}"
        return "<expr>"

    def _call_target(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._call_target(node.value)}.{node.attr}"
        return ""


# ---------------------------------------------------------------------------
# STEPS 3–6 — SEMANTIC ANALYSIS, DEPENDENCY, CALL GRAPH, PURPOSE INFERENCE
# ---------------------------------------------------------------------------

def extract_signal_keywords(analysis: ModuleAnalysis) -> dict:
    text_sources = [
        analysis.module_doc,
        " ".join(c["name"] for c in analysis.classes),
        " ".join(f["name"] for f in analysis.functions),
        " ".join(m["name"] for cls in analysis.classes for m in cls["methods"]),
        " ".join(analysis.comments[:50]),
    ]
    combined = " ".join(text_sources).lower()
    words = re.findall(r'\b[a-z_][a-z0-9_]*\b', combined)

    freq = Counter()
    for word in words:
        for verb in SEMANTIC_VERBS:
            if verb in word:
                freq[verb] += 1

    return dict(freq.most_common())


def classify_subsystems(analysis: ModuleAnalysis) -> list:
    import_str = " ".join(analysis.imports)
    matched = []
    for subsys, pattern in SUBSYSTEM_PATTERNS.items():
        if pattern.search(import_str) or pattern.search(analysis.rel):
            matched.append(subsys)
    # Also check the directory name
    dir_name = analysis.path.parent.name
    matched.append(f"staging:{dir_name}")
    return list(set(matched))


def infer_runtime_role(analysis: ModuleAnalysis, signals: dict) -> str:
    combined = (
        analysis.module_name.lower() + " " +
        analysis.module_doc.lower() + " " +
        " ".join(signals.keys())
    )
    best_role = "utility library"
    best_score = 0
    for role, keywords in ROLE_SIGNALS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_score:
            best_score = score
            best_role = role
    return best_role


def infer_purpose(analysis: ModuleAnalysis, signals: dict, role: str) -> str:
    if analysis.module_doc:
        first_line = analysis.module_doc.strip().split("\n")[0][:120]
        return first_line
    # Construct from module name + role
    name_clean = analysis.module_name.replace("_", " ")
    if signals:
        top_verbs = list(signals.keys())[:3]
        return f"{name_clean} — {role} [{', '.join(top_verbs)}]"
    return f"{name_clean} — {role}"


def deduplicate_calls(calls: list) -> list:
    seen = set()
    result = []
    for c in calls:
        if c and c not in seen and not c.startswith("self") and len(c) > 2:
            seen.add(c)
            result.append(c)
    return result[:30]  # cap at 30 to keep JSON manageable


def extract_exports(analysis: ModuleAnalysis) -> list:
    exports = []
    # All class names
    for cls in analysis.classes:
        exports.append(cls["name"])
    # Top-level non-private functions
    for fn in analysis.functions:
        if not fn["name"].startswith("_"):
            exports.append(fn["name"])
    # __all__ from constants (check if defined)
    return exports


# ---------------------------------------------------------------------------
# STEP 7 — SALVAGEABLE FUNCTION DETECTION
# ---------------------------------------------------------------------------

def assess_salvageability(fn: dict, module_analysis: ModuleAnalysis) -> dict | None:
    name = fn["name"].lower()
    doc = fn.get("docstring", "").lower()
    args = fn.get("args", [])

    # Check for semantic verb signal
    verb_matches = [v for v in SALVAGE_CRITERIA_VERBS if v in name or v in doc]
    if not verb_matches:
        return None

    # Prefer parameterized functions (>1 non-self arg)
    real_args = [a for a in args if a["name"] not in ("self", "cls")]
    if len(real_args) < 1 and not doc:
        return None  # no inputs, no doc = likely trivial

    # Assign candidate cluster
    combined = name + " " + doc + " " + module_analysis.module_name.lower()
    best_cluster = "general"
    best_score = 0
    for cluster, kws in CLUSTER_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in combined)
        if score > best_score:
            best_score = score
            best_cluster = cluster

    # Compatible subsystems from parent module
    subsystems = assess_subsystem_compat(module_analysis)

    return {
        "function_name": fn["name"],
        "module": module_analysis.rel,
        "module_name": module_analysis.module_name,
        "line": fn.get("line", 0),
        "is_async": fn.get("is_async", False),
        "docstring": fn.get("docstring", ""),
        "return_type": fn.get("return_type", ""),
        "arg_count": len(real_args),
        "semantic_verbs": verb_matches,
        "semantic_role": verb_matches[0] if verb_matches else "unknown",
        "candidate_cluster": best_cluster,
        "compatible_subsystems": subsystems,
    }


def assess_method_salvageability(method: dict, cls: dict, module_analysis: ModuleAnalysis) -> dict | None:
    # Same as function but qualified with class name
    fn_like = dict(method)
    fn_like["name"] = f"{cls['name']}.{method['name']}"
    result = assess_salvageability(fn_like, module_analysis)
    if result:
        result["class_context"] = cls["name"]
    return result


def assess_subsystem_compat(analysis: ModuleAnalysis) -> list:
    subsystems = classify_subsystems(analysis)
    return [s for s in subsystems if not s.startswith("staging:")][:5]


# ---------------------------------------------------------------------------
# STEP 10 — CORE COMPATIBILITY HINTS
# ---------------------------------------------------------------------------

CORE_PATTERNS = {
    "RUNTIME_EXECUTION_CORE": ["arp", "reasoning", "mtp", "translate", "pxl", "modal", "mvs", "scp", "predict"],
    "RUNTIME_OPPERATIONS_CORE": ["csp", "memory", "state", "smp", "persist", "recall"],
    "AGENT_SYSTEM": ["agent", "identity", "principal", "consciousness", "sign", "axiom"],
    "DRAC": ["gate", "validate", "safety", "constraint", "policy", "ethics", "guard"],
    "RGE": ["rge", "genesis", "radial", "topology", "divergence", "commutation"],
    "IEL": ["iel", "epistemic", "knowledge", "catalog", "ontoprops"],
    "TOOLING": ["tool", "adapter", "wrapper", "export", "introspect", "invention"],
    "UTILITY": ["util", "helper", "schema", "type", "constant", "loader", "registry", "config"],
}


def core_compatibility(analysis: ModuleAnalysis, signals: dict) -> list:
    combined = (
        analysis.module_name.lower() + " " +
        " ".join(analysis.imports).lower() + " " +
        " ".join(signals.keys())
    )
    compat = []
    for core, kws in CORE_PATTERNS.items():
        if any(kw in combined for kw in kws):
            compat.append(core)
    return compat or ["UNRESOLVED"]


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def run():
    print("=" * 60)
    print("ARCHON PRIME — Legacy Application Function Deep Semantic Extraction")
    print("=" * 60)

    # Step 1 — File discovery
    print("\n=== STEP 1: MODULE DISCOVERY ===")
    all_py = list(TARGET_DIR.rglob("*.py"))
    all_py = [p for p in all_py if "__pycache__" not in p.parts]
    to_analyze = [p for p in all_py if not should_exclude(p)]
    excluded = [p for p in all_py if should_exclude(p)]

    print(f"  Total Python files found: {len(all_py)}")
    print(f"  Excluded (test/audit/nexus/boot): {len(excluded)}")
    print(f"  Modules to analyze: {len(to_analyze)}")

    # Steps 2–6 — Parse + analyze each module
    print("\n=== STEPS 2–6: AST PARSING + SEMANTIC ANALYSIS ===")
    analyses = []
    for p in sorted(to_analyze):
        ma = ModuleAnalysis(p)
        ma.parse()
        analyses.append(ma)

    parse_errors = [a for a in analyses if a.parse_error]
    parse_ok = [a for a in analyses if not a.parse_error]
    print(f"  Parsed successfully: {len(parse_ok)}")
    print(f"  Parse errors (included with partial data): {len(parse_errors)}")

    # Build profiles
    print("\n=== STEP 3–6: PROFILE GENERATION ===")
    profiles = []
    for ma in analyses:
        signals = extract_signal_keywords(ma)
        role = infer_runtime_role(ma, signals)
        purpose = infer_purpose(ma, signals, role)
        subsystems = classify_subsystems(ma)
        calls = deduplicate_calls(ma.call_targets)
        exports = extract_exports(ma)
        compat = core_compatibility(ma, signals)

        profile = {
            "module_path": ma.rel,
            "module_name": ma.module_name,
            "staging_group": ma.path.parent.name,
            "purpose": purpose,
            "runtime_role": role,
            "subsystem": subsystems,
            "core_compatibility": compat,
            "module_docstring": ma.module_doc[:500] if ma.module_doc else "",
            "imports": sorted(set(ma.imports))[:40],
            "call_targets": calls,
            "exports": exports[:30],
            "signal_keywords": signals,
            "class_count": len(ma.classes),
            "function_count": len(ma.functions),
            "try_except_count": ma.try_except_count,
            "context_manager_count": ma.context_manager_count,
            "constants": [c["name"] for c in ma.constants][:15],
            "decorators": list(set(ma.decorators))[:15],
            "parse_error": ma.parse_error or None,
        }
        profiles.append(profile)

    out_profiles = OUT_DIR / "module_semantic_profiles.json"
    out_profiles.write_text(json.dumps(profiles, indent=2, ensure_ascii=False))
    print(f"  Profiles written: {len(profiles)}")
    print(f"  Written: {out_profiles}")

    # Step 7 — Salvageable function detection
    print("\n=== STEP 7: SALVAGEABLE FUNCTION DETECTION ===")
    salvageable = []
    for ma in analyses:
        for fn in ma.functions:
            result = assess_salvageability(fn, ma)
            if result:
                salvageable.append(result)
        for cls in ma.classes:
            for method in cls["methods"]:
                if method["name"].startswith("_") and method["name"] != "__call__":
                    continue
                result = assess_method_salvageability(method, cls, ma)
                if result:
                    salvageable.append(result)

    print(f"  Salvageable function blocks identified: {len(salvageable)}")
    out_salvage = OUT_DIR / "salvageable_function_blocks.json"
    out_salvage.write_text(json.dumps(salvageable, indent=2, ensure_ascii=False))
    print(f"  Written: {out_salvage}")

    # Step 10 — Core compatibility hints
    print("\n=== STEP 10: CORE COMPATIBILITY HINTS ===")
    compat_hints = {}
    for ma in analyses:
        signals = extract_signal_keywords(ma)
        compat = core_compatibility(ma, signals)
        for core in compat:
            if core not in compat_hints:
                compat_hints[core] = []
            compat_hints[core].append({
                "module": ma.rel,
                "module_name": ma.module_name,
                "staging_group": ma.path.parent.name,
                "signal_keywords": list(signals.keys())[:8],
            })

    out_compat = OUT_DIR / "core_compatibility_hints.json"
    out_compat.write_text(json.dumps(compat_hints, indent=2, ensure_ascii=False))
    print(f"  Cores mapped: {len(compat_hints)}")
    print(f"  Written: {out_compat}")

    # Step 11 — Salvage report
    print("\n=== STEP 11: SALVAGE REPORT ===")
    _generate_report(analyses, to_analyze, excluded, profiles, salvageable, compat_hints, parse_errors)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print(f"  Modules analyzed:          {len(analyses)}")
    print(f"  Modules excluded:          {len(excluded)}")
    print(f"  Profiles generated:        {len(profiles)}")
    print(f"  Salvageable functions:     {len(salvageable)}")
    print(f"  Core compat entries:       {sum(len(v) for v in compat_hints.values())}")
    print("=" * 60)

    return profiles, salvageable, compat_hints


def _generate_report(analyses, analyzed_files, excluded_files, profiles, salvageable, compat_hints, parse_errors):
    # Aggregate metrics
    total_analyzed = len(analyses)
    total_excluded = len(excluded_files)
    total_functions = sum(p["function_count"] for p in profiles)
    total_class_methods = sum(
        sum(len(cls["methods"]) for cls in a.classes)
        for a in analyses
    )
    total_detected = total_functions + total_class_methods
    total_salvageable = len(salvageable)

    # Role distribution
    role_counts = Counter(p["runtime_role"] for p in profiles)

    # Signal keyword frequency
    all_signals = Counter()
    for p in profiles:
        for k, v in p["signal_keywords"].items():
            all_signals[k] += v

    # Cluster distribution over salvageable
    cluster_dist = Counter(f["candidate_cluster"] for f in salvageable)

    # Core compat summary
    core_sizes = {k: len(v) for k, v in compat_hints.items()}

    # Top-density modules (by salvageable function count)
    module_salvage_counts = Counter(f["module"] for f in salvageable)
    top_modules = module_salvage_counts.most_common(10)

    # Group excluded by reason
    excl_by_reason = Counter()
    for p in excluded_files:
        stem = p.stem.lower()
        for reason in ("test", "audit", "nexus", "boot"):
            if reason in stem:
                excl_by_reason[reason] += 1
                break

    lines = [
        "# ARCHON PRIME — Legacy Application Function Salvage Report",
        "**Generated:** 2026-03-10  ",
        "**Mode:** Static Analysis — Read-Only  ",
        f"**Target:** `_Dev_Resources/STAGING/APPLICATION_FUNCTIONS`  ",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Python files in target | {len(analyzed_files) + len(excluded_files)} |",
        f"| Modules analyzed | {total_analyzed} |",
        f"| Modules ignored (exclusion rules) | {total_excluded} |",
        f"| Total functions + methods detected | {total_detected} |",
        f"| Salvageable function blocks | {total_salvageable} |",
        f"| Parse errors (partial extraction) | {len(parse_errors)} |",
        "",
        "---",
        "",
        "## Staging Groups",
        "",
        "| Group | Files Analyzed |",
        "|-------|---------------|",
    ]

    group_counts = Counter(a.path.parent.name for a in analyses)
    for group, count in sorted(group_counts.items()):
        lines.append(f"| `{group}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Excluded Files by Rule",
        "",
        "| Rule | Files Excluded |",
        "|------|---------------|",
    ]
    for reason, count in sorted(excl_by_reason.items(), key=lambda x: -x[1]):
        lines.append(f"| `{reason}` in filename | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Runtime Role Distribution",
        "",
        "| Runtime Role | Module Count |",
        "|-------------|-------------|",
    ]
    for role, count in role_counts.most_common():
        lines.append(f"| {role} | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Semantic Signal Frequency",
        "",
        "| Signal Keyword | Total Occurrences |",
        "|---------------|------------------|",
    ]
    for kw, count in all_signals.most_common(20):
        lines.append(f"| `{kw}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Salvageable Function Cluster Distribution",
        "",
        "| Candidate Cluster | Function Count |",
        "|------------------|---------------|",
    ]
    for cluster, count in cluster_dist.most_common():
        lines.append(f"| `{cluster}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Top 10 Modules by Salvageable Function Density",
        "",
        "| Module | Salvageable Functions |",
        "|--------|-----------------------|",
    ]
    for mod, count in top_modules:
        lines.append(f"| `{mod}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Core Compatibility Hints",
        "",
        "| Runtime Core | Compatible Modules |",
        "|-------------|-------------------|",
    ]
    for core, count in sorted(core_sizes.items(), key=lambda x: -x[1]):
        lines.append(f"| `{core}` | {count} |")

    lines += [
        "",
        "---",
        "",
        "## Parse Errors (Partial Extraction)",
        "",
        "The following modules had syntax errors. Partial data was captured where possible.",
        "",
        "| Module | Error |",
        "|--------|-------|",
    ]
    for a in parse_errors:
        lines.append(f"| `{a.rel}` | {a.parse_error} |")

    lines += [
        "",
        "---",
        "",
        "## Recommended Deletions",
        "",
        "The following categories of files are safe candidates for deletion",
        "after confirming their content is captured in the output artifacts:",
        "",
        "1. **Excluded files** (test/audit/nexus/boot) — these are non-functional stubs or test harnesses.",
        "2. **`__init__.py` files** with no content — pure package markers, no logic.",
        "3. **Duplicate reasoning engines** — pairs like `abductive_engine.py` + `abductive_reasoning_engine.py` should be reviewed; the shorter name is likely the legacy version.",
        "",
        "> **Governance Note:** No deletions are performed by this pass. All recommendations require human review.",
        "",
        "---",
        "",
        "## Output Artifacts",
        "",
        "| File | Description |",
        "|------|-------------|",
        "| `module_semantic_profiles.json` | Full per-module profile: purpose, role, imports, signals, exports |",
        "| `salvageable_function_blocks.json` | Candidate DRAC application functions extracted from all modules |",
        "| `core_compatibility_hints.json` | Mapping of modules to compatible runtime cores |",
        "| `module_salvage_report.md` | This report |",
    ]

    report = "\n".join(lines)
    out = OUT_DIR / "module_salvage_report.md"
    out.write_text(report, encoding="utf-8")
    print(f"  Written: {out}")


if __name__ == "__main__":
    run()

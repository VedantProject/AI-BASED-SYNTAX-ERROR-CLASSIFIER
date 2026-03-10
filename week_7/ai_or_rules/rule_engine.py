"""
Week 7 · AI / Rule Engine → Heuristic Rule Engine
===================================================
A lightweight, rule-based decision system that evaluates the analysis results
produced by the Week 7 passes and emits structured recommendations.

Design
------
Every "rule" is a small Python object with:
  • name          – unique identifier
  • description   – human-readable intent
  • severity      – INFO | WARNING | ERROR
  • check(ctx)    – predicate over a RuleContext; returns True when the rule fires
  • message(ctx)  – generates a recommendation string

Rules are evaluated against a RuleContext that bundles:
  • language, filename
  • AST (transformed)
  • semantic_result  (from SemanticAnalyzer.analyze)
  • cfa_result       (from ControlFlowAnalyzer.analyze)
  • dfa_result       (from DataFlowAnalyzer.analyze)
  • complexity_result(from ComplexityAnalyzer.analyze)
  • transformation_log (combined log of all three transformation passes)

Public API
----------
    engine = RuleEngine()
    result = engine.process(ctx)
    # result is a JSON-serialisable dict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ══════════════════════════════════════════════════════════════════════════════
# Rule context
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RuleContext:
    """Bundles all analysis artefacts for rule evaluation."""
    language:           str         = "unknown"
    filename:           str         = "unknown"
    source_code:        str         = ""
    semantic:           Dict        = field(default_factory=dict)
    control_flow:       Dict        = field(default_factory=dict)
    data_flow:          Dict        = field(default_factory=dict)
    complexity:         Dict        = field(default_factory=dict)
    transformation_log: List[Dict]  = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
# Rule definition
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Rule:
    """A single heuristic rule."""
    name:        str
    description: str
    severity:    str                           # INFO | WARNING | ERROR
    check:       Callable[[RuleContext], bool]
    message:     Callable[[RuleContext], str]
    category:    str = "general"               # complexity | data_flow | cfg | quality


# ══════════════════════════════════════════════════════════════════════════════
# Built-in rules
# ══════════════════════════════════════════════════════════════════════════════

def _make_rules() -> List[Rule]:
    """Factory for all built-in rules."""

    rules: List[Rule] = []

    # ── Complexity rules ──────────────────────────────────────────────────────

    rules.append(Rule(
        name        = "HIGH_CYCLOMATIC_COMPLEXITY",
        description = "Cyclomatic complexity exceeds 10, indicating the code is hard to test.",
        severity    = "WARNING",
        category    = "complexity",
        check       = lambda ctx: (ctx.complexity.get("cyclomatic_complexity", 0) > 10),
        message     = lambda ctx: (
            f"Cyclomatic complexity is {ctx.complexity['cyclomatic_complexity']} "
            f"(rating: {ctx.complexity.get('complexity_rating', '?')}). "
            "Consider splitting large functions into smaller, focused ones."
        ),
    ))

    rules.append(Rule(
        name        = "VERY_HIGH_CYCLOMATIC_COMPLEXITY",
        description = "Cyclomatic complexity exceeds 20 – very difficult to maintain.",
        severity    = "ERROR",
        category    = "complexity",
        check       = lambda ctx: (ctx.complexity.get("cyclomatic_complexity", 0) > 20),
        message     = lambda ctx: (
            f"Cyclomatic complexity is {ctx.complexity['cyclomatic_complexity']}. "
            "This code is extremely difficult to test and maintain. "
            "Refactor immediately."
        ),
    ))

    rules.append(Rule(
        name        = "DEEP_NESTING",
        description = "Nesting depth > 4 reduces readability.",
        severity    = "WARNING",
        category    = "complexity",
        check       = lambda ctx: (ctx.complexity.get("max_nesting_depth", 0) > 4),
        message     = lambda ctx: (
            f"Maximum nesting depth is {ctx.complexity['max_nesting_depth']}. "
            "Deeply nested code is hard to read. "
            "Consider early returns, guard clauses, or helper functions."
        ),
    ))

    rules.append(Rule(
        name        = "FUNCTION_TOO_LONG",
        description = "A function with > 50 LOC is harder to understand.",
        severity    = "WARNING",
        category    = "complexity",
        check       = lambda ctx: any(
            f.get("estimated_loc", 0) > 50
            for f in ctx.complexity.get("per_function", [])
        ),
        message     = lambda ctx: (
            "Functions: " + ", ".join(
                f"'{f['name']}' ({f['estimated_loc']} LOC)"
                for f in ctx.complexity.get("per_function", [])
                if f.get("estimated_loc", 0) > 50
            ) + " exceed 50 LOC. Consider splitting them."
        ),
    ))

    # ── Data-flow rules ───────────────────────────────────────────────────────

    rules.append(Rule(
        name        = "UNINITIALIZED_VARIABLE_USE",
        description = "A variable is used before it has been assigned a value.",
        severity    = "ERROR",
        category    = "data_flow",
        check       = lambda ctx: len(ctx.data_flow.get("uninitialized_vars", [])) > 0,
        message     = lambda ctx: (
            "Potentially uninitialized variables detected: " +
            ", ".join(
                f"'{u['name']}' (line {u['line']})"
                for u in ctx.data_flow.get("uninitialized_vars", [])
            ) + ". Ensure all variables are initialised before use."
        ),
    ))

    rules.append(Rule(
        name        = "DEAD_VARIABLE_DEFINITION",
        description = "A variable is assigned but its value is never read.",
        severity    = "WARNING",
        category    = "data_flow",
        check       = lambda ctx: len(ctx.data_flow.get("dead_definitions", [])) > 0,
        message     = lambda ctx: (
            "Dead (unused) variable definitions: " +
            ", ".join(
                f"'{d['name']}' (line {d['line']})"
                for d in ctx.data_flow.get("dead_definitions", [])
            ) + ". Remove or use these definitions."
        ),
    ))

    # ── Control-flow rules ────────────────────────────────────────────────────

    rules.append(Rule(
        name        = "UNREACHABLE_CODE",
        description = "There are basic blocks in the CFG that can never be executed.",
        severity    = "WARNING",
        category    = "cfg",
        check       = lambda ctx: len(ctx.control_flow.get("unreachable_block_ids", [])) > 0,
        message     = lambda ctx: (
            f"{len(ctx.control_flow['unreachable_block_ids'])} unreachable code block(s) detected "
            f"(block IDs: {ctx.control_flow['unreachable_block_ids']}). "
            "Remove dead branches/statements for cleaner code."
        ),
    ))

    rules.append(Rule(
        name        = "TOO_MANY_BRANCHES",
        description = "Excessive branching makes control flow hard to follow.",
        severity    = "WARNING",
        category    = "cfg",
        check       = lambda ctx: (ctx.control_flow.get("branch_count", 0) > 8),
        message     = lambda ctx: (
            f"File has {ctx.control_flow['branch_count']} branch points. "
            "Consider simplifying the logic using polymorphism, early returns, "
            "or look-up tables."
        ),
    ))

    rules.append(Rule(
        name        = "LOOP_DETECTED",
        description = "One or more loops were identified (informational).",
        severity    = "INFO",
        category    = "cfg",
        check       = lambda ctx: len(ctx.control_flow.get("loops", [])) > 0,
        message     = lambda ctx: (
            f"{len(ctx.control_flow['loops'])} loop(s) detected. "
            "Ensure loop bounds are always reachable and that exit conditions are correct."
        ),
    ))

    # ── Semantic rules ────────────────────────────────────────────────────────

    rules.append(Rule(
        name        = "SEMANTIC_ERRORS",
        description = "Semantic errors (e.g., undeclared identifiers) were found.",
        severity    = "ERROR",
        category    = "quality",
        check       = lambda ctx: len(ctx.semantic.get("errors", [])) > 0,
        message     = lambda ctx: (
            f"{len(ctx.semantic['errors'])} semantic error(s): " +
            "; ".join(
                f"[{e['code']}] {e['message']} (line {e['line']})"
                for e in ctx.semantic.get("errors", [])[:5]   # cap at 5 in summary
            ) + ("…" if len(ctx.semantic.get("errors", [])) > 5 else "")
        ),
    ))

    rules.append(Rule(
        name        = "SEMANTIC_WARNINGS",
        description = "Semantic warnings (e.g., type mismatches) were found.",
        severity    = "WARNING",
        category    = "quality",
        check       = lambda ctx: len(ctx.semantic.get("warnings", [])) > 0,
        message     = lambda ctx: (
            f"{len(ctx.semantic['warnings'])} semantic warning(s). "
            "Review the semantic analysis output for details."
        ),
    ))

    # ── Transformation info ───────────────────────────────────────────────────

    rules.append(Rule(
        name        = "OPTIMIZATIONS_APPLIED",
        description = "The transformation passes folded or simplified code.",
        severity    = "INFO",
        category    = "quality",
        check       = lambda ctx: len(ctx.transformation_log) > 0,
        message     = lambda ctx: (
            f"{len(ctx.transformation_log)} optimisation(s) were applied "
            "by constant folding, dead-code elimination, and simplification passes."
        ),
    ))

    # ── Heuristic AI: code-smell detector ────────────────────────────────────

    rules.append(Rule(
        name        = "MAGIC_NUMBERS_DETECTED",
        description = "Heuristic: many numeric literals suggest 'magic numbers'.",
        severity    = "INFO",
        category    = "quality",
        check       = lambda ctx: _count_magic_numbers(ctx) > 5,
        message     = lambda ctx: (
            f"Detected {_count_magic_numbers(ctx)} raw numeric literals in the source. "
            "Consider replacing them with named constants for readability."
        ),
    ))

    rules.append(Rule(
        name        = "HIGH_SYMBOL_DENSITY",
        description = "Heuristic: many symbols per estimated LOC may indicate overly complex code.",
        severity    = "INFO",
        category    = "quality",
        check       = lambda ctx: _symbol_density(ctx) > 2.0,
        message     = lambda ctx: (
            f"Symbol density is {_symbol_density(ctx):.2f} symbols/LOC "
            f"({ctx.semantic.get('statistics', {}).get('total_symbols', 0)} symbols, "
            f"{ctx.complexity.get('estimated_loc', 1)} estimated LOC). "
            "High density may indicate overly terse or complex code."
        ),
    ))

    return rules


# ══════════════════════════════════════════════════════════════════════════════
# Rule Engine
# ══════════════════════════════════════════════════════════════════════════════

class RuleEngine:
    """
    Evaluates all built-in heuristic rules against the analysis context and
    returns a JSON-serialisable result dict.
    """

    SEVERITY_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}

    def __init__(self):
        self.rules: List[Rule] = _make_rules()

    def process(self, ctx: RuleContext) -> Dict[str, Any]:
        """
        Evaluate every rule.

        Returns a dict with keys:
          applied_rules, skipped_rules, recommendations,
          severity_counts, overall_grade, summary
        """
        applied: List[Dict]  = []
        skipped: List[str]   = []

        for rule in self.rules:
            try:
                if rule.check(ctx):
                    applied.append({
                        "rule":        rule.name,
                        "severity":    rule.severity,
                        "category":    rule.category,
                        "description": rule.description,
                        "message":     rule.message(ctx),
                    })
                else:
                    skipped.append(rule.name)
            except Exception as exc:
                # Never let a broken rule crash the pipeline
                skipped.append(rule.name)
                applied.append({
                    "rule":     rule.name,
                    "severity": "INFO",
                    "category": rule.category,
                    "message":  f"[Rule evaluation error: {exc}]",
                })

        # Sort: errors first, then warnings, then info
        applied.sort(key=lambda r: self.SEVERITY_ORDER.get(r["severity"], 9))

        severity_counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
        for r in applied:
            severity_counts[r["severity"]] = severity_counts.get(r["severity"], 0) + 1

        grade = self._grade(severity_counts)

        recommendations = [r["message"] for r in applied if r["severity"] != "INFO"]

        return {
            "applied_rules":    applied,
            "skipped_rules":    skipped,
            "recommendations":  recommendations,
            "severity_counts":  severity_counts,
            "overall_grade":    grade,
            "summary": {
                "total_rules_evaluated": len(self.rules),
                "rules_fired":           len(applied),
                "errors":    severity_counts["ERROR"],
                "warnings":  severity_counts["WARNING"],
                "info":      severity_counts["INFO"],
                "grade":     grade,
            },
        }

    @staticmethod
    def _grade(counts: Dict[str, int]) -> str:
        """A / B / C / D / F based on error/warning counts."""
        e = counts.get("ERROR", 0)
        w = counts.get("WARNING", 0)
        if e == 0 and w == 0:            return "A"
        if e == 0 and w <= 2:            return "B"
        if e == 0 and w <= 5:            return "C"
        if e <= 2:                        return "D"
        return "F"


# ── heuristic helpers ─────────────────────────────────────────────────────────

def _count_magic_numbers(ctx: RuleContext) -> int:
    """Count bare integer/float literals in source (crude regex approach)."""
    import re
    return len(re.findall(r'\b(?<!\w)\d+(?:\.\d+)?\b', ctx.source_code))


def _symbol_density(ctx: RuleContext) -> float:
    total_symbols = ctx.semantic.get("statistics", {}).get("total_symbols", 0)
    loc = max(ctx.complexity.get("estimated_loc", 1), 1)
    return total_symbols / loc

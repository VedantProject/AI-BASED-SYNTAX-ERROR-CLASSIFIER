"""
Week 7 – Advanced Compiler Passes
Extends the existing Multi-Language Parser Framework with:
  • Semantic analysis   (symbol table, scope tracking, type checks)
  • Control-flow analysis (CFG, loop/branch detection, unreachable code)
  • Data-flow analysis   (reaching definitions, live vars, uninitialised vars)
  • Complexity analysis  (cyclomatic, nesting depth, LOC)
  • Transformation passes (constant folding, dead-code elimination, simplification)
  • Rule / heuristic engine (code-quality warnings and recommendations)

All passes operate on the real AST node objects produced by the existing
parsers so no logic is duplicated.

Usage:
    python week_7/run_week7.py --file <source> [--language c|java|python]
"""

__version__ = "1.0.0"
__author__  = "Week 7 Compiler Passes"

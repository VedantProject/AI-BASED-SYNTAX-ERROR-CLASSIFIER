"""
analysis/ — Program Analysis package
=====================================
Runs all analysis passes over an IRProgram and returns a list
of Diagnostic objects (compatible with ErrorNode display in analyze_code.py).

Public API:
    from analysis import run_all_analyses
    diagnostics = run_all_analyses(ir_program, ast_tree, source)
"""

from analysis.runner import run_all_analyses

__all__ = ["run_all_analyses"]

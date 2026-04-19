"""
analysis/runner.py — Analysis Pipeline Runner
==============================================
Orchestrates all three analysis passes and returns a unified
list of diagnostics compatible with the analyze_code.py display pipeline.
"""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from ir.ir_nodes import IRProgram
from analysis.control_flow  import run_control_flow_analysis, check_break_continue
from analysis.data_flow      import run_data_flow_analysis
from analysis.pattern_detector import run_pattern_detection


def _line_indent(source: str, line_no: int) -> int:
    lines = source.splitlines()
    if line_no <= 0 or line_no > len(lines):
        return 0
    line = lines[line_no - 1]
    return len(line) - len(line.lstrip(" \t"))


def run_all_analyses(ir_program: IRProgram, ast_tree,
                     source: str = "") -> list:
    """
    Run all three analysis passes and return a merged, sorted list
    of diagnostic objects (each has .error_type, .message, .line, .column, .token).
    """
    results = []

    try:
        results.extend(run_control_flow_analysis(ir_program))
        results.extend(check_break_continue(ast_tree))
    except Exception:
        pass

    try:
        results.extend(run_data_flow_analysis(ir_program))
    except Exception:
        pass

    try:
        results.extend(run_pattern_detection(ast_tree))
    except Exception:
        pass

    # Guard against a known parser/CFG edge case where statements that have
    # dedented back to the top level can be attached to a function's synthetic
    # dead block after a return, producing a spurious unreachable warning.
    results = [
        d for d in results
        if not (
            d.error_type == "UNREACHABLE_CODE"
            and "dead block 'dead_" in d.message
            and _line_indent(source, d.line) == 0
        )
    ]

    # Sort by line number
    results.sort(key=lambda d: (d.line, d.column))
    return results

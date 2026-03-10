"""
analysis/control_flow.py — CFG-based Control Flow Analysis
===========================================================
Detects:
  - UNREACHABLE_CODE  : basic blocks with no predecessors (except entry)
  - MISSING_RETURN    : function CFG paths that reach exit without RETURN
  - BREAK_OUTSIDE_LOOP / CONTINUE_OUTSIDE_LOOP : detected from AST walk
  - INFINITE_LOOP     : while/for loop with no reachable break edge to exit
"""

from __future__ import annotations
from typing import List
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ir.ir_nodes import Op, IRProgram, IRFunction, CFG, BasicBlock
from syntax_tree import ast_nodes as ast


# ─── Diagnostic namedtuple (mirrors ErrorNode interface) ─────────────────────

class CFADiagnostic:
    """Lightweight diagnostic produced by control flow analysis."""
    def __init__(self, error_type: str, message: str, line: int,
                 token: str = None, column: int = 0):
        self.error_type = error_type
        self.message    = message
        self.line       = line
        self.column     = column
        self.token      = token


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _first_line_of_block(block: BasicBlock) -> int:
    for instr in block.instrs:
        if instr.line > 0:
            return instr.line
    return 0


def _block_has_return(block: BasicBlock) -> bool:
    return any(i.op == Op.RETURN for i in block.instrs)


def _all_paths_have_return(cfg: CFG) -> bool:
    """
    Checks if every path from entry to exit passes through a RETURN instruction.
    Uses DFS; returns True only if every path leading to 'exit' has a RETURN.
    """
    # For each path from entry → exit, at least one block must contain RETURN
    visited = set()

    def _dfs(bid: str, seen_return: bool) -> bool:
        """Returns True if every path from bid to exit has a return."""
        if bid == "exit":
            return seen_return
        if bid in visited:
            return True  # assume good (break cycles)
        visited.add(bid)

        block = cfg.blocks.get(bid)
        if block is None:
            return seen_return

        has_ret = seen_return or _block_has_return(block)

        succs = block.successors
        if not succs:
            return has_ret

        result = True
        for succ in succs:
            if not _dfs(succ, has_ret):
                result = False
        visited.discard(bid)
        return result

    return _dfs(cfg.entry, False)


# ─── Main analysis functions ──────────────────────────────────────────────────

def analyse_cfg(name: str, cfg: CFG, is_function: bool = False,
                fn_line: int = 0) -> List[CFADiagnostic]:
    """Run control flow analysis on one CFG and return diagnostics."""
    diagnostics: List[CFADiagnostic] = []
    reachable = cfg.reachable_from_entry()

    for bid, block in cfg.blocks.items():
        if bid in ("entry", "exit"):
            continue

        # ── Unreachable code ──────────────────────────────────────────────
        if bid not in reachable:
            line = _first_line_of_block(block)
            if line > 0:
                diagnostics.append(CFADiagnostic(
                    error_type="UNREACHABLE_CODE",
                    message=f"Unreachable code detected (dead block '{bid}')",
                    line=line,
                ))

        # ── Infinite loop: loop header reachable, exit block not ──────────
        # A loop header has a back-edge (successor that is itself or an ancestor)
        # and no path to a non-loop exit other than through 'exit' directly.
        # Simplified heuristic: block named while_hdr/for_hdr with only one
        # outgoing edge (back to itself or body) and exit_id not reachable
        if ("while_hdr" in bid or "for_hdr" in bid) and bid in reachable:
            # Check if the corresponding exit block is reachable
            # Derive exit id: while_hdr_N → while_exit_N
            idx = bid.split("_")[-1]
            loop_exit_id = f"while_exit_{idx}" if "while" in bid else f"for_exit_{idx}"
            if loop_exit_id not in reachable:
                line = _first_line_of_block(block)
                if line > 0:
                    diagnostics.append(CFADiagnostic(
                        error_type="INFINITE_LOOP",
                        message="Potential infinite loop: loop body has no reachable exit "
                                "(no 'break' or always-true condition)",
                        line=line,
                    ))

    # ── Missing return in function ────────────────────────────────────────
    if is_function:
        if not _all_paths_have_return(cfg):
            diagnostics.append(CFADiagnostic(
                error_type="MISSING_RETURN",
                message=f"Function '{name}' does not return a value on all code paths",
                line=fn_line,
            ))

    return diagnostics


def run_control_flow_analysis(ir_program: IRProgram) -> List[CFADiagnostic]:
    """Run CFA on the module + all functions. Return merged diagnostics."""
    results: List[CFADiagnostic] = []

    # Module-level (not a function, so skip missing-return check)
    results.extend(analyse_cfg("<module>", ir_program.module_cfg, is_function=False))

    for ir_fn in ir_program.functions:
        results.extend(analyse_cfg(ir_fn.name, ir_fn.cfg,
                                   is_function=True, fn_line=ir_fn.line))

    return results


# ─── AST-level break/continue context check ──────────────────────────────────

def check_break_continue(ast_tree) -> List[CFADiagnostic]:
    """
    Walk the AST and detect break/continue statements outside a loop.
    This is simpler to do on the AST than on the CFG.
    """
    diagnostics: List[CFADiagnostic] = []

    def _walk(node, in_loop: bool):
        if node is None:
            return
        if isinstance(node, (ast.WhileStmt, ast.ForStmt)):
            _walk_block(getattr(node, "body", None), in_loop=True)
            return
        if isinstance(node, ast.BreakStmt):
            if not in_loop:
                diagnostics.append(CFADiagnostic(
                    error_type="BREAK_OUTSIDE_LOOP",
                    message="'break' used outside a loop",
                    line=node.line,
                ))
        if isinstance(node, ast.ContinueStmt):
            if not in_loop:
                diagnostics.append(CFADiagnostic(
                    error_type="CONTINUE_OUTSIDE_LOOP",
                    message="'continue' used outside a loop",
                    line=node.line,
                ))
        # Recurse into children
        for attr in vars(node).values():
            if isinstance(attr, ast.ASTNode):
                _walk(attr, in_loop)
            elif isinstance(attr, list):
                for item in attr:
                    if isinstance(item, ast.ASTNode):
                        _walk(item, in_loop)

    def _walk_block(block, in_loop: bool):
        if block is None:
            return
        for stmt in getattr(block, "statements", []):
            _walk(stmt, in_loop)

    for stmt in getattr(ast_tree, "statements", []):
        _walk(stmt, in_loop=False)

    return diagnostics

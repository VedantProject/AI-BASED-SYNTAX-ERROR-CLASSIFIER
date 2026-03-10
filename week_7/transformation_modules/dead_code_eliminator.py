"""
Week 7 · Transformation Modules → Dead-Code Eliminator
========================================================
Removes provably *unreachable* statements inside a Block:

  • Any statement that follows a ReturnStmt, BreakStmt, or ContinueStmt
    in the same flat statement list is removed (intra-block dead code).

  • Constant-condition branches:
      if (true)  { A } else { B }  →  A
      if (false) { A } else { B }  →  B
      while (false) { body }        →  removed

The original AST is NOT modified; a deep-copy is returned.

Public API
----------
    dce = DeadCodeEliminator()
    new_ast, log = dce.transform(ast_root)
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt,
    ExpressionStmt, VariableDecl,
    Literal,
)

# Terminals: any statement after one of these in a flat list is dead
_TERMINATING = (ReturnStmt, BreakStmt, ContinueStmt)


class DeadCodeEliminator:
    """Dead-code elimination pass."""

    def __init__(self):
        self._log: List[Dict] = []

    # ── public ────────────────────────────────────────────────────────────────

    def transform(self, root: ASTNode) -> Tuple[ASTNode, List[Dict]]:
        """Return (cleaned_ast, change_log)."""
        self._log = []
        new_root = copy.deepcopy(root)
        self._visit(new_root)
        return new_root, self._log

    # ── in-place visitor ──────────────────────────────────────────────────────

    def _visit(self, node: Any):
        if node is None or not isinstance(node, ASTNode):
            return

        method = f"_visit_{type(node).__name__}"
        getattr(self, method, self._visit_generic)(node)

    def _visit_Program(self, node: Program):
        node.statements = self._clean_stmts(node.statements)
        for s in node.statements:
            self._visit(s)

    def _visit_Block(self, node: Block):
        node.statements = self._clean_stmts(node.statements)
        for s in node.statements:
            self._visit(s)

    def _visit_FunctionDecl(self, node: FunctionDecl):
        if node.body:
            self._visit(node.body)

    def _visit_ClassDecl(self, node: ClassDecl):
        for m in node.methods:
            self._visit(m)

    def _visit_IfStmt(self, node: IfStmt):
        """Fold constant conditions."""
        cond_val = _literal_bool(node.condition)

        if cond_val is True:
            # Always-true: keep then-branch, discard else
            self._record("const_if_true", "if(true){…}else{…}", "kept then-branch", node.line)
            if node.then_block:
                self._visit(node.then_block)
            node.else_block = None

        elif cond_val is False:
            # Always-false: discard then-branch, promote else
            self._record("const_if_false", "if(false){…}else{…}", "kept else-branch", node.line)
            node.then_block = node.else_block or Block(statements=[], line=node.line)
            node.else_block = None
            self._visit(node.then_block)

        else:
            # Normal: recurse into both branches
            if node.then_block:
                self._visit(node.then_block)
            if node.else_block:
                self._visit(node.else_block)

    def _visit_WhileStmt(self, node: WhileStmt):
        cond_val = _literal_bool(node.condition)
        if cond_val is False:
            # while(false) is always dead
            self._record("const_while_false", "while(false){…}", "removed body", node.line)
            node.body = Block(statements=[], line=node.line)
        elif node.body:
            self._visit(node.body)

    def _visit_ForStmt(self, node: ForStmt):
        if node.body:
            self._visit(node.body)

    def _visit_generic(self, node: ASTNode):
        for val in vars(node).values():
            if isinstance(val, ASTNode):
                self._visit(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, ASTNode):
                        self._visit(item)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _clean_stmts(self, stmts: List[ASTNode]) -> List[ASTNode]:
        """
        Remove statements that follow a terminating statement
        (return / break / continue) in the same flat list.
        """
        result: List[ASTNode] = []
        for stmt in stmts:
            result.append(stmt)
            if isinstance(stmt, _TERMINATING):
                # Everything that would follow is dead
                remaining = stmts[len(result):]
                for dead in remaining:
                    self._record(
                        "post_terminator_dead",
                        type(stmt).__name__,
                        f"removed {type(dead).__name__}(line {dead.line})",
                        dead.line,
                    )
                break
        return result

    def _record(self, elim_type: str, original: str, action: str, line: int):
        self._log.append({
            "elimination_type": elim_type,
            "original":         original,
            "action":           action,
            "line":             line,
        })


# ── utility ───────────────────────────────────────────────────────────────────

def _literal_bool(node: Optional[ASTNode]) -> Optional[bool]:
    """
    If *node* is a Literal with a clearly boolean/numeric value,
    return True/False; otherwise return None (unknown at compile time).
    """
    if not isinstance(node, Literal):
        return None
    v = node.value
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        if v.lower() in ("true",  "1"): return True
        if v.lower() in ("false", "0"): return False
    return None

"""
Week 7 · Transformation Modules → Constant Folder
===================================================
Performs *constant folding* on the deep-copied AST:

  • BinaryOp(Literal, op, Literal)  →  Literal(result)     e.g.  3 + 5  → 8
  • UnaryOp (op, Literal)           →  Literal(result)     e.g.  -7     → -7
  • BinaryOp with one side Literal 0/1 (strength reduction):
        x + 0 → x,   x - 0 → x,   x * 1 → x,   x / 1 → x
        x * 0 → 0,   0 * x → 0,   0 + x → x,   0 - x → UnaryOp(-,x)

The original AST is NOT modified; a deep-copy is returned.

Public API
----------
    folder = ConstantFolder()
    new_ast, log = folder.transform(ast_root)
    # log is a list of dicts describing each fold applied
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt, ReturnStmt, ExpressionStmt, VariableDecl,
    BinaryOp, UnaryOp, AssignmentExpr,
    FunctionCall, Literal, ArrayAccess, MemberAccess,
    ErrorNode,
)


class ConstantFolder:
    """Constant-folding optimisation pass."""

    def __init__(self):
        self._log: List[Dict] = []

    # ── public ────────────────────────────────────────────────────────────────

    def transform(self, root: ASTNode) -> Tuple[ASTNode, List[Dict]]:
        """
        Return (folded_ast, change_log).
        The returned AST is an independent deep-copy of *root*.
        """
        self._log = []
        new_root = copy.deepcopy(root)
        self._visit(new_root)
        return new_root, self._log

    # ── in-place mutating visitor ─────────────────────────────────────────────

    def _visit(self, node: Any) -> Any:
        """Recursively fold *node* in-place; return the (possibly new) node."""
        if node is None:
            return node
        if isinstance(node, list):
            return [self._visit(item) for item in node]
        if not isinstance(node, ASTNode):
            return node

        method = f"_visit_{type(node).__name__}"
        return getattr(self, method, self._visit_generic)(node)

    # ── node visitors ─────────────────────────────────────────────────────────

    def _visit_Program(self, node: Program) -> Program:
        node.statements = [self._visit(s) for s in node.statements]
        return node

    def _visit_Block(self, node: Block) -> Block:
        node.statements = [self._visit(s) for s in node.statements]
        return node

    def _visit_FunctionDecl(self, node: FunctionDecl) -> FunctionDecl:
        if node.body:
            node.body = self._visit(node.body)
        return node

    def _visit_ClassDecl(self, node: ClassDecl) -> ClassDecl:
        node.methods = [self._visit(m) for m in node.methods]
        node.fields  = [self._visit(f) for f in node.fields]
        return node

    def _visit_IfStmt(self, node: IfStmt) -> IfStmt:
        node.condition  = self._visit(node.condition)
        node.then_block = self._visit(node.then_block)
        node.else_block = self._visit(node.else_block)
        return node

    def _visit_WhileStmt(self, node: WhileStmt) -> WhileStmt:
        node.condition = self._visit(node.condition)
        node.body      = self._visit(node.body)
        return node

    def _visit_ForStmt(self, node: ForStmt) -> ForStmt:
        node.init      = self._visit(node.init)
        node.condition = self._visit(node.condition)
        node.increment = self._visit(node.increment)
        node.body      = self._visit(node.body)
        return node

    def _visit_ReturnStmt(self, node: ReturnStmt) -> ReturnStmt:
        node.value = self._visit(node.value)
        return node

    def _visit_ExpressionStmt(self, node: ExpressionStmt) -> ExpressionStmt:
        node.expression = self._visit(node.expression)
        return node

    def _visit_VariableDecl(self, node: VariableDecl) -> VariableDecl:
        if node.initializer:
            node.initializer = self._visit(node.initializer)
        return node

    def _visit_AssignmentExpr(self, node: AssignmentExpr) -> AssignmentExpr:
        node.value = self._visit(node.value)
        return node

    def _visit_FunctionCall(self, node: FunctionCall) -> FunctionCall:
        node.arguments = [self._visit(a) for a in node.arguments]
        return node

    def _visit_ArrayAccess(self, node: ArrayAccess) -> ArrayAccess:
        node.array = self._visit(node.array)
        node.index = self._visit(node.index)
        return node

    def _visit_MemberAccess(self, node: MemberAccess) -> MemberAccess:
        node.object = self._visit(node.object)
        return node

    def _visit_UnaryOp(self, node: UnaryOp) -> ASTNode:
        node.operand = self._visit(node.operand)
        if isinstance(node.operand, Literal):
            result = self._fold_unary(node.operator, node.operand.value)
            if result is not None:
                self._record("unary_fold",
                             f"{node.operator}{node.operand.value}", result, node.line)
                return Literal(value=result,
                               literal_type=node.operand.literal_type,
                               line=node.line, column=node.column)
        return node

    def _visit_BinaryOp(self, node: BinaryOp) -> ASTNode:
        # Fold children first (bottom-up)
        node.left  = self._visit(node.left)
        node.right = self._visit(node.right)

        # Both sides are literals → fully evaluate
        if isinstance(node.left, Literal) and isinstance(node.right, Literal):
            lv, rv = node.left.value, node.right.value
            result = self._fold_binary(node.operator, lv, rv)
            if result is not None:
                self._record("binary_fold",
                             f"{lv} {node.operator} {rv}", result, node.line)
                ltype = node.left.literal_type or node.right.literal_type
                return Literal(value=result, literal_type=ltype,
                               line=node.line, column=node.column)

        # Strength reductions
        return self._strength_reduce(node)

    def _visit_generic(self, node: ASTNode) -> ASTNode:
        for attr, val in vars(node).items():
            if isinstance(val, ASTNode):
                setattr(node, attr, self._visit(val))
            elif isinstance(val, list):
                setattr(node, attr, [self._visit(item) for item in val])
        return node

    # ── folding helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _fold_binary(op: str, lv: Any, rv: Any) -> Optional[Any]:
        try:
            lv, rv = _to_num(lv), _to_num(rv)
            if op == "+":  return lv + rv
            if op == "-":  return lv - rv
            if op == "*":  return lv * rv
            if op == "/" and rv != 0:  return lv / rv
            if op == "%" and rv != 0:  return int(lv) % int(rv)
            if op == "**": return lv ** rv
        except (TypeError, ValueError):
            pass
        return None

    @staticmethod
    def _fold_unary(op: str, v: Any) -> Optional[Any]:
        try:
            num = _to_num(v)
            if op == "-":  return -num
            if op == "+":  return +num
            if op in ("!", "not"): return not bool(num)
        except (TypeError, ValueError):
            pass
        return None

    def _strength_reduce(self, node: BinaryOp) -> ASTNode:
        """Apply algebraic identities when exactly one operand is a Literal."""
        op = node.operator
        llit = isinstance(node.left,  Literal)
        rlit = isinstance(node.right, Literal)

        if rlit:
            rv = _to_num(node.right.value, default=None)
            if rv is not None:
                if op in ("+", "-") and rv == 0:
                    self._record("strength_reduce", f"x {op} 0", "x", node.line)
                    return node.left
                if op in ("*", "/") and rv == 1:
                    self._record("strength_reduce", f"x {op} 1", "x", node.line)
                    return node.left
                if op == "*" and rv == 0:
                    self._record("strength_reduce", "x * 0", "0", node.line)
                    return Literal(value=0, literal_type="int",
                                   line=node.line, column=node.column)

        if llit:
            lv = _to_num(node.left.value, default=None)
            if lv is not None:
                if op == "+" and lv == 0:
                    self._record("strength_reduce", "0 + x", "x", node.line)
                    return node.right
                if op == "*" and lv == 0:
                    self._record("strength_reduce", "0 * x", "0", node.line)
                    return Literal(value=0, literal_type="int",
                                   line=node.line, column=node.column)
                if op == "*" and lv == 1:
                    self._record("strength_reduce", "1 * x", "x", node.line)
                    return node.right

        return node

    def _record(self, fold_type: str, original: str, result: Any, line: int):
        self._log.append({
            "fold_type": fold_type,
            "original":  str(original),
            "result":    str(result),
            "line":      line,
        })


# ── module-level utility ──────────────────────────────────────────────────────

def _to_num(v: Any, default: Any = 0) -> Any:
    """Convert a literal value to a Python number."""
    if isinstance(v, (int, float)):
        return v
    try:
        return int(v)
    except (TypeError, ValueError):
        pass
    try:
        return float(v)
    except (TypeError, ValueError):
        pass
    return default

"""
Week 7 · Transformation Modules → Code Simplifier
===================================================
Applies algebraic and structural simplifications to the AST that are not
covered by the constant folder:

  • Double-negation elimination:  !!x   → x,   not not x → x
  • Redundant parentheses / unary +:  +x  → x
  • Boolean tautologies:
        x && true   → x
        x || false  → x
        x && false  → false
        x || true   → true
  • String / list concatenation of two adjacent literals:
        "foo" + "bar" → "foobar"

The original AST is NOT modified; a deep-copy is returned.

Public API
----------
    simplifier = CodeSimplifier()
    new_ast, log = simplifier.transform(ast_root)
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

_LOGICAL_AND = {"&&", "and"}
_LOGICAL_OR  = {"||", "or"}
_NEGATION    = {"!", "not"}


class CodeSimplifier:
    """Algebraic/structural simplification pass."""

    def __init__(self):
        self._log: List[Dict] = []

    # ── public ────────────────────────────────────────────────────────────────

    def transform(self, root: ASTNode) -> Tuple[ASTNode, List[Dict]]:
        """Return (simplified_ast, change_log)."""
        self._log = []
        new_root = copy.deepcopy(root)
        self._visit(new_root)
        return new_root, self._log

    # ── in-place visitor ──────────────────────────────────────────────────────

    def _visit(self, node: Any) -> Any:
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

    # ── expression simplifiers ────────────────────────────────────────────────

    def _visit_UnaryOp(self, node: UnaryOp) -> ASTNode:
        node.operand = self._visit(node.operand)

        # Double negation: !!x → x,   not not x → x
        if node.operator in _NEGATION:
            if isinstance(node.operand, UnaryOp) and node.operand.operator in _NEGATION:
                self._record("double_negation", f"{node.operator}{node.operator}x",
                             "x", node.line)
                return node.operand.operand

        # Unary + is identity: +x → x
        if node.operator == "+":
            self._record("unary_plus",  "+x", "x", node.line)
            return node.operand

        return node

    def _visit_BinaryOp(self, node: BinaryOp) -> ASTNode:
        node.left  = self._visit(node.left)
        node.right = self._visit(node.right)

        op = node.operator

        # String / list concat: "a" + "b" → "ab"
        if (op == "+" and isinstance(node.left,  Literal)
                      and isinstance(node.right, Literal)
                      and isinstance(node.left.value,  str)
                      and isinstance(node.right.value, str)):
            concat = node.left.value + node.right.value
            self._record("string_concat",
                         f'"{node.left.value}" + "{node.right.value}"',
                         f'"{concat}"', node.line)
            return Literal(value=concat, literal_type="string",
                           line=node.line, column=node.column)

        # Boolean tautologies with logical AND
        if op in _LOGICAL_AND:
            if _is_literal_true(node.right):
                self._record("bool_tautology", "x && true",  "x", node.line)
                return node.left
            if _is_literal_true(node.left):
                self._record("bool_tautology", "true && x",  "x", node.line)
                return node.right
            if _is_literal_false(node.right) or _is_literal_false(node.left):
                self._record("bool_tautology", "x && false", "false", node.line)
                return Literal(value=False, literal_type="bool",
                               line=node.line, column=node.column)

        # Boolean tautologies with logical OR
        if op in _LOGICAL_OR:
            if _is_literal_false(node.right):
                self._record("bool_tautology", "x || false", "x", node.line)
                return node.left
            if _is_literal_false(node.left):
                self._record("bool_tautology", "false || x", "x", node.line)
                return node.right
            if _is_literal_true(node.right) or _is_literal_true(node.left):
                self._record("bool_tautology", "x || true",  "true", node.line)
                return Literal(value=True, literal_type="bool",
                               line=node.line, column=node.column)

        return node

    def _visit_ErrorNode(self, node: ErrorNode) -> ErrorNode:
        return node

    def _visit_generic(self, node: ASTNode) -> ASTNode:
        for attr, val in vars(node).items():
            if isinstance(val, ASTNode):
                setattr(node, attr, self._visit(val))
            elif isinstance(val, list):
                setattr(node, attr, [self._visit(item) for item in val])
        return node

    # ── record ────────────────────────────────────────────────────────────────

    def _record(self, simp_type: str, original: str, result: str, line: int):
        self._log.append({
            "simplification_type": simp_type,
            "original":            original,
            "result":              result,
            "line":                line,
        })


# ── utility ───────────────────────────────────────────────────────────────────

def _is_literal_true(node: Any) -> bool:
    if not isinstance(node, Literal):
        return False
    v = node.value
    return v is True or v == 1 or (isinstance(v, str) and v.lower() == "true")


def _is_literal_false(node: Any) -> bool:
    if not isinstance(node, Literal):
        return False
    v = node.value
    return v is False or v == 0 or (isinstance(v, str) and v.lower() == "false")

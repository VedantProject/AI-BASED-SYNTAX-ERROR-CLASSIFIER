"""
Week 7 · Analysis Modules → Complexity Analyser
=================================================
Computes standard code-complexity metrics from the real AST nodes:

  • Cyclomatic complexity – M = E − N + 2P  (approximated via decision-point
                            counting: 1 + one per branch/loop/case/logical-op)
  • Maximum nesting depth – deepest nesting of control structures
  • Statement count        – total non-declaration, non-trivial statements
  • Function count         – number of function/method declarations
  • Estimated LOC          – count of non-empty AST lines referenced
  • Per-function metrics   – the above computed per function for fine-grained reporting
  • Complexity rating       – low / moderate / high / very_high based on CC

The analyser is read-only; the AST is never mutated.

Public API
----------
    ca = ComplexityAnalyzer()
    result = ca.analyze(ast_program_node)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt,
    ExpressionStmt, VariableDecl, ReturnStmt,
    BinaryOp, ErrorNode,
)


class ComplexityAnalyzer:
    """Computes complexity metrics over the AST."""

    # Operator names that count as extra decision points
    _LOGICAL_OPS = {"&&", "||", "and", "or", "&amp;&amp;"}

    def __init__(self):
        self._global_cc    = 1    # start at 1 per McCabe
        self._max_depth    = 0
        self._stmt_count   = 0
        self._func_count   = 0
        self._lines_seen: Set[int] = set()
        self._per_func: List[Dict] = []

    # ── public entry point ────────────────────────────────────────────────────

    def analyze(self, root: ASTNode) -> Dict[str, Any]:
        self._global_cc  = 1
        self._max_depth  = 0
        self._stmt_count = 0
        self._func_count = 0
        self._lines_seen = set()
        self._per_func   = []

        self._visit(root, depth=0)

        rating = self._rate(self._global_cc)

        return {
            "cyclomatic_complexity": self._global_cc,
            "max_nesting_depth":     self._max_depth,
            "statement_count":       self._stmt_count,
            "function_count":        self._func_count,
            "estimated_loc":         len(self._lines_seen),
            "complexity_rating":     rating,
            "per_function":          self._per_func,
            "thresholds": {
                "low":       "CC ≤ 10",
                "moderate":  "CC 11-20",
                "high":      "CC 21-50",
                "very_high": "CC > 50",
            },
        }

    # ── visitor dispatcher ────────────────────────────────────────────────────

    def _visit(self, node: Any, depth: int):
        if node is None:
            return
        if isinstance(node, list):
            for item in node:
                self._visit(item, depth)
            return
        if not isinstance(node, ASTNode):
            return

        # Track source lines for LOC estimate
        if hasattr(node, "line") and node.line:
            self._lines_seen.add(node.line)

        self._max_depth = max(self._max_depth, depth)

        method = f"_visit_{type(node).__name__}"
        getattr(self, method, self._visit_generic)(node, depth)

    # ── node visitors ─────────────────────────────────────────────────────────

    def _visit_Program(self, node: Program, depth: int):
        for s in node.statements:
            self._visit(s, depth)

    def _visit_Block(self, node: Block, depth: int):
        for s in node.statements:
            self._visit(s, depth)

    def _visit_FunctionDecl(self, node: FunctionDecl, depth: int):
        self._func_count += 1

        # Analyse the function body in isolation
        sub = ComplexityAnalyzer()
        if node.body:
            # Wrap body statements so sub-analyser sees them
            dummy = Program(statements=node.body.statements, language="")
            sub_result = sub.analyze(dummy)
        else:
            sub_result = {
                "cyclomatic_complexity": 1, "max_nesting_depth": 0,
                "statement_count": 0, "estimated_loc": 0,
            }

        self._per_func.append({
            "name":                   node.name,
            "line":                   node.line,
            "cyclomatic_complexity":  sub_result["cyclomatic_complexity"],
            "max_nesting_depth":      sub_result["max_nesting_depth"],
            "statement_count":        sub_result["statement_count"],
            "estimated_loc":          sub_result["estimated_loc"],
            "complexity_rating":      self._rate(sub_result["cyclomatic_complexity"]),
        })

        # Also fold into global CC
        self._global_cc += sub_result["cyclomatic_complexity"] - 1   # -1 to avoid double-counting base

        if node.body:
            self._visit(node.body, depth + 1)

    def _visit_ClassDecl(self, node: ClassDecl, depth: int):
        for m in node.methods:
            self._visit(m, depth)

    def _visit_IfStmt(self, node: IfStmt, depth: int):
        self._global_cc  += 1         # one decision point
        self._stmt_count += 1
        self._visit(node.condition, depth)
        if node.then_block:
            self._visit(node.then_block, depth + 1)
        if node.else_block:
            self._global_cc += 1      # else branch is another decision
            self._visit(node.else_block, depth + 1)

    def _visit_WhileStmt(self, node: WhileStmt, depth: int):
        self._global_cc  += 1
        self._stmt_count += 1
        self._visit(node.condition, depth)
        if node.body:
            self._visit(node.body, depth + 1)

    def _visit_ForStmt(self, node: ForStmt, depth: int):
        self._global_cc  += 1
        self._stmt_count += 1
        self._visit(node.init,      depth)
        self._visit(node.condition, depth)
        self._visit(node.increment, depth)
        if node.body:
            self._visit(node.body, depth + 1)

    def _visit_ExpressionStmt(self, node: ExpressionStmt, depth: int):
        self._stmt_count += 1
        self._visit(node.expression, depth)

    def _visit_ReturnStmt(self, node: ReturnStmt, depth: int):
        self._stmt_count += 1
        self._visit(node.value, depth)

    def _visit_VariableDecl(self, node: VariableDecl, depth: int):
        # Declaration counts as a statement
        self._stmt_count += 1
        if node.initializer:
            self._visit(node.initializer, depth)

    def _visit_BinaryOp(self, node: BinaryOp, depth: int):
        # Logical operators add to CC (short-circuit paths)
        if node.operator in self._LOGICAL_OPS:
            self._global_cc += 1
        self._visit(node.left,  depth)
        self._visit(node.right, depth)

    def _visit_ErrorNode(self, node: ErrorNode, depth: int):
        pass   # ignore error nodes

    def _visit_generic(self, node: ASTNode, depth: int):
        for val in vars(node).values():
            if isinstance(val, (ASTNode, list)):
                self._visit(val, depth)

    # ── helper ────────────────────────────────────────────────────────────────

    @staticmethod
    def _rate(cc: int) -> str:
        if cc <= 10:
            return "low"
        if cc <= 20:
            return "moderate"
        if cc <= 50:
            return "high"
        return "very_high"

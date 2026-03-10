"""
Week 7 · Core Engine → Semantic Analyzer
=========================================
Walks the real AST node objects produced by the existing parsers and performs:

  1. Symbol-table construction  – tracks every declaration with type, scope level
                                  and declaration site.
  2. Scope tracking             – enters / exits scopes for blocks and functions.
  3. Undeclared-identifier check – reports identifiers used without a prior decl.
  4. Redeclaration check        – reports names declared twice in the same scope.
  5. Type-consistency check      – basic type mismatch detection on assignments.

The analysis is read-only: the AST is never modified here.

Public API
----------
    analyzer = SemanticAnalyzer(language="c")
    result   = analyzer.analyze(ast_program_node)
    # result is a plain dict, JSON-serialisable via main.utils.write_json
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# ── Reuse existing AST node types ──────────────────────────────────────────────
from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, Parameter, VariableDecl, ClassDecl,
    IfStmt, WhileStmt, ForStmt, ReturnStmt,
    ExpressionStmt, ImportStmt,
    BinaryOp, UnaryOp, AssignmentExpr,
    FunctionCall, Literal, Identifier, ArrayAccess, MemberAccess,
    ErrorNode,
)


# ══════════════════════════════════════════════════════════════════════════════
# Symbol table
# ══════════════════════════════════════════════════════════════════════════════

class SymbolTable:
    """Scoped symbol table implemented as a stack of dicts."""

    def __init__(self):
        # Each entry in the stack is  {name: symbol_info_dict}
        self._scopes: List[Dict[str, Dict]] = [{}]
        self.all_symbols: List[Dict] = []        # flat list for reporting

    # ── scope management ──────────────────────────────────────────────────────

    def enter_scope(self):
        self._scopes.append({})

    def exit_scope(self):
        if len(self._scopes) > 1:
            self._scopes.pop()

    @property
    def depth(self) -> int:
        return len(self._scopes) - 1  # 0 = global

    # ── declaration ───────────────────────────────────────────────────────────

    def declare(self, name: str, sym_type: str, line: int, column: int = 0
                ) -> Optional[Dict]:
        """
        Declare a symbol in the current scope.
        Returns the *existing* symbol dict on redeclaration, None on success.
        """
        current_scope = self._scopes[-1]
        if name in current_scope:
            return current_scope[name]  # signals redeclaration

        sym = {
            "name":        name,
            "sym_type":    sym_type,
            "scope_level": self.depth,
            "declared_at": line,
            "column":      column,
        }
        current_scope[name] = sym
        self.all_symbols.append(sym)
        return None  # success

    # ── lookup ────────────────────────────────────────────────────────────────

    def lookup(self, name: str) -> Optional[Dict]:
        """Walk scopes inner-to-outer; return symbol dict or None."""
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None


# ══════════════════════════════════════════════════════════════════════════════
# Semantic Analyser
# ══════════════════════════════════════════════════════════════════════════════

class SemanticAnalyzer:
    """
    Performs semantic analysis on the AST produced by the existing parsers.

    Parameters
    ----------
    language : str
        One of 'c', 'java', 'python'.  Used for language-specific heuristics.
    """

    def __init__(self, language: str = "c"):
        self.language = language
        self.symbol_table = SymbolTable()
        self.errors:   List[Dict] = []
        self.warnings: List[Dict] = []

    # ── public entry point ────────────────────────────────────────────────────

    def analyze(self, root: ASTNode) -> Dict[str, Any]:
        """
        Analyse the AST rooted at *root*.

        Returns a JSON-serialisable dict with keys:
          symbols, errors, warnings, statistics
        """
        self.symbol_table = SymbolTable()
        self.errors   = []
        self.warnings = []

        self._visit(root)

        return {
            "language":   self.language,
            "symbols":    self.symbol_table.all_symbols,
            "errors":     self.errors,
            "warnings":   self.warnings,
            "statistics": {
                "total_symbols":    len(self.symbol_table.all_symbols),
                "unique_names":     len({s["name"] for s in self.symbol_table.all_symbols}),
                "semantic_errors":  len(self.errors),
                "semantic_warnings": len(self.warnings),
            },
        }

    # ── visitor dispatcher ────────────────────────────────────────────────────

    def _visit(self, node: Any):
        if node is None:
            return
        if isinstance(node, list):
            for item in node:
                self._visit(item)
            return
        if not isinstance(node, ASTNode):
            return

        method = f"_visit_{type(node).__name__}"
        visitor = getattr(self, method, self._visit_generic)
        visitor(node)

    # ── node visitors ─────────────────────────────────────────────────────────

    def _visit_Program(self, node: Program):
        for stmt in node.statements:
            self._visit(stmt)

    def _visit_Block(self, node: Block):
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self._visit(stmt)
        self.symbol_table.exit_scope()

    def _visit_FunctionDecl(self, node: FunctionDecl):
        sym_type = f"function({node.return_type or 'void'})"
        collision = self.symbol_table.declare(node.name, sym_type, node.line, node.column)
        if collision:
            self._add_error("REDECLARATION",
                            f"Function '{node.name}' already declared at line {collision['declared_at']}",
                            node.line, node.column)

        # Function body gets its own scope; parameters live in that scope
        self.symbol_table.enter_scope()
        for param in node.parameters:
            self._visit(param)
        if node.body:
            # Visit body statements directly (Block would double-enter a scope)
            for stmt in node.body.statements:
                self._visit(stmt)
        self.symbol_table.exit_scope()

    def _visit_Parameter(self, node: Parameter):
        collision = self.symbol_table.declare(
            node.name, node.param_type or "unknown", node.line, node.column)
        if collision:
            self._add_error("REDECLARATION",
                            f"Parameter '{node.name}' already declared",
                            node.line, node.column)

    def _visit_VariableDecl(self, node: VariableDecl):
        sym_type = node.var_type or "unknown"
        if node.is_const:
            sym_type = f"const {sym_type}"
        collision = self.symbol_table.declare(node.name, sym_type, node.line, node.column)
        if collision:
            self._add_error("REDECLARATION",
                            f"Variable '{node.name}' already declared at line {collision['declared_at']}",
                            node.line, node.column)
        # Visit the initialiser expression
        if node.initializer:
            self._visit(node.initializer)

    def _visit_ClassDecl(self, node: ClassDecl):
        collision = self.symbol_table.declare(node.name, "class", node.line, node.column)
        if collision:
            self._add_error("REDECLARATION",
                            f"Class '{node.name}' already declared",
                            node.line, node.column)
        self.symbol_table.enter_scope()
        for field in node.fields:
            self._visit(field)
        for method in node.methods:
            self._visit(method)
        self.symbol_table.exit_scope()

    def _visit_IfStmt(self, node: IfStmt):
        self._visit(node.condition)
        if node.then_block:
            self._visit(node.then_block)
        if node.else_block:
            self._visit(node.else_block)

    def _visit_WhileStmt(self, node: WhileStmt):
        self._visit(node.condition)
        if node.body:
            self._visit(node.body)

    def _visit_ForStmt(self, node: ForStmt):
        self.symbol_table.enter_scope()
        self._visit(node.init)
        self._visit(node.condition)
        self._visit(node.increment)
        if node.body:
            for stmt in node.body.statements:
                self._visit(stmt)
        self.symbol_table.exit_scope()

    def _visit_ExpressionStmt(self, node: ExpressionStmt):
        self._visit(node.expression)

    def _visit_ReturnStmt(self, node: ReturnStmt):
        self._visit(node.value)

    def _visit_ImportStmt(self, node: ImportStmt):
        # Register imported module name as a symbol (scope 0)
        self.symbol_table.declare(node.module or "?", "import", node.line, node.column)

    # ── expression visitors ───────────────────────────────────────────────────

    def _visit_AssignmentExpr(self, node: AssignmentExpr):
        # Target must be declared (we do a simple string lookup)
        target_name = node.target
        if target_name and not self.symbol_table.lookup(target_name):
            self._add_warning("UNDECLARED_ASSIGN",
                              f"Assignment to potentially undeclared variable '{target_name}'",
                              node.line, node.column)
        self._visit(node.value)

    def _visit_Identifier(self, node: Identifier):
        if node.name and not self.symbol_table.lookup(node.name):
            self._add_error("UNDECLARED_IDENTIFIER",
                            f"Identifier '{node.name}' used without prior declaration",
                            node.line, node.column)

    def _visit_BinaryOp(self, node: BinaryOp):
        self._visit(node.left)
        self._visit(node.right)
        # Rudimentary type-consistency: compare literal types if both sides are literals
        if isinstance(node.left, Literal) and isinstance(node.right, Literal):
            if (node.left.literal_type and node.right.literal_type
                    and node.left.literal_type != node.right.literal_type
                    and node.operator not in {'+', '-', '*', '/'}):
                self._add_warning("TYPE_MISMATCH",
                                  f"Operands of '{node.operator}' have different types "
                                  f"('{node.left.literal_type}' vs '{node.right.literal_type}')",
                                  node.line, node.column)

    def _visit_UnaryOp(self, node: UnaryOp):
        self._visit(node.operand)

    def _visit_FunctionCall(self, node: FunctionCall):
        # Check that the function was declared
        if node.name and not self.symbol_table.lookup(node.name):
            self._add_warning("UNDECLARED_FUNCTION",
                              f"Call to undeclared function '{node.name}'",
                              node.line, node.column)
        for arg in node.arguments:
            self._visit(arg)

    def _visit_ArrayAccess(self, node: ArrayAccess):
        self._visit(node.array)
        self._visit(node.index)

    def _visit_MemberAccess(self, node: MemberAccess):
        self._visit(node.object)

    def _visit_Literal(self, node: Literal):
        pass  # Literals are always valid

    def _visit_ErrorNode(self, node: ErrorNode):
        pass  # Already captured by parser; ignore in semantic pass

    def _visit_generic(self, node: ASTNode):
        """Fallback: visit any child fields that are ASTNodes."""
        for val in vars(node).values():
            if isinstance(val, (ASTNode, list)):
                self._visit(val)

    # ── helpers ───────────────────────────────────────────────────────────────

    def _add_error(self, code: str, message: str, line: int, column: int = 0):
        self.errors.append({"code": code, "message": message,
                            "line": line, "column": column})

    def _add_warning(self, code: str, message: str, line: int, column: int = 0):
        self.warnings.append({"code": code, "message": message,
                              "line": line, "column": column})

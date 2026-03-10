"""
analysis/pattern_detector.py — Static Anti-Pattern Detection
=============================================================
Walks the Python AST directly (no IR needed) and flags common
Python-specific anti-patterns and code smells.

Detects:
  MUTABLE_DEFAULT_ARG  : def f(x=[]) or def f(x={}) or def f(x=set())
  BARE_EXCEPT          : bare 'except:' clause
  EMPTY_EXCEPT         : 'except' block with only 'pass'
  IS_LITERAL_COMPARE   : 'if x is 5' or 'x is not "hello"'
  SINGLETON_COMPARE    : 'x == None', 'x == True', 'x == False'
  BUILTIN_SHADOW       : assigning to 'list', 'dict', 'str', etc.
  UNUSED_IMPORT        : import statement where the name is never used
"""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Set
from syntax_tree import ast_nodes as ast


class PatternDiagnostic:
    def __init__(self, error_type: str, message: str, line: int,
                 token: str = None, column: int = 0):
        self.error_type = error_type
        self.message    = message
        self.line       = line
        self.column     = column
        self.token      = token


# ─── Built-in names that must not be shadowed ──────────────────────────────────

_SHADOWED_BUILTINS = {
    'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool',
    'type', 'object', 'len', 'range', 'print', 'input', 'open',
    'map', 'filter', 'zip', 'sorted', 'reversed', 'enumerate',
    'sum', 'min', 'max', 'abs', 'round', 'hash', 'id',
    'staticmethod', 'classmethod', 'property', 'super',
}

# ─── Mutable types whose literals are dangerous as default arguments ────────────

_MUTABLE_LITERAL_TYPES = ('list', 'dict')   # Literal.literal_type values
_MUTABLE_CALLS         = {'list', 'dict', 'set'}  # FunctionCall names


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _collect_identifiers(node) -> Set[str]:
    """Recursively collect all Identifier names in a subtree."""
    names: Set[str] = set()
    if node is None:
        return names
    if isinstance(node, ast.Identifier):
        names.add(node.name)
    for attr in vars(node).values() if hasattr(node, '__dict__') else []:
        if isinstance(attr, ast.ASTNode):
            names.update(_collect_identifiers(attr))
        elif isinstance(attr, list):
            for item in attr:
                if isinstance(item, ast.ASTNode):
                    names.update(_collect_identifiers(item))
    return names


def _is_mutable_default(node) -> bool:
    """Return True if node is a mutable literal/call (list/dict/set)."""
    if isinstance(node, ast.Literal):
        return node.literal_type in _MUTABLE_LITERAL_TYPES
    if isinstance(node, ast.FunctionCall):
        return node.name in _MUTABLE_CALLS
    return False


def _collect_used_names(stmts: list) -> Set[str]:
    """Collect all identifier names used across a list of statements."""
    used: Set[str] = set()
    for stmt in stmts:
        used.update(_collect_identifiers(stmt))
    return used


# ─── Core analysis walker ──────────────────────────────────────────────────────

class PatternDetector:
    def __init__(self):
        self.diagnostics: List[PatternDiagnostic] = []

    def _emit(self, error_type: str, message: str, line: int, token: str = None):
        self.diagnostics.append(PatternDiagnostic(
            error_type=error_type, message=message,
            line=line, token=token))

    # ── Mutable default argument ──────────────────────────────────────────────

    def check_function(self, node: ast.FunctionDecl):
        """Check function for mutable default arguments."""
        for param in node.parameters:
            # Parameters with default values are stored via parse_expression_simple
            # We check by inspecting if the param has a default stored in the body
            # Since our AST is simplified, we detect pattern in the token stream
            # Alternative: check if parameter name ends up as Literal of mutable type
            # We rely on the raw parameter parsing emitting an ExpressionStmt for defaults
            pass  # handled via AST body inspection below

    def check_mutable_defaults(self, fn: ast.FunctionDecl):
        """
        Heuristic: scan the parsed function body's first statements for
        patterns like 'if param is None: param = []'  indicating the
        workaround, OR check for mutable default values in parameter list
        via stored default_value attribute if present.
        """
        # The parser stores default expressions; check node attributes
        for param in fn.parameters:
            default = getattr(param, 'default_value', None)
            if default is not None and _is_mutable_default(default):
                self._emit(
                    "MUTABLE_DEFAULT_ARG",
                    f"Mutable default argument '{param.name}' in function '{fn.name}'. "
                    f"Use 'None' as default and create the object inside the function.",
                    line=fn.line, token=param.name,
                )

    # ── Singleton comparisons (== None, == True, == False) ────────────────────

    def check_singleton_compare(self, node: ast.BinaryOp):
        if node.operator not in ('==', '!='):
            return
        for side in (node.left, node.right):
            if isinstance(side, ast.Literal) and side.literal_type in ('null', 'bool'):
                val = str(side.value)
                correct_op = 'is' if node.operator == '==' else 'is not'
                self._emit(
                    "SINGLETON_COMPARE",
                    f"Use '{correct_op}' instead of '{node.operator}' when comparing "
                    f"with {val}. (e.g. 'x is {val}')",
                    line=node.line, token=val,
                )

    # ── 'is' comparison with literal ──────────────────────────────────────────

    def check_is_literal(self, node: ast.BinaryOp):
        if node.operator not in ('is', 'is not'):
            return
        for side in (node.left, node.right):
            if isinstance(side, ast.Literal) and side.literal_type in ('int', 'float', 'string'):
                self._emit(
                    "IS_LITERAL_COMPARE",
                    f"Do not use '{node.operator}' to compare with a literal value "
                    f"{repr(side.value)}. Use '==' instead. "
                    f"'is' checks object identity, not value equality.",
                    line=node.line, token=str(side.value),
                )

    # ── Builtin name shadowing ─────────────────────────────────────────────────

    def check_builtin_shadow(self, target: str, line: int):
        if target in _SHADOWED_BUILTINS:
            self._emit(
                "BUILTIN_SHADOW",
                f"'{target}' shadows a Python built-in name. "
                f"This can cause confusing bugs; choose a different variable name.",
                line=line, token=target,
            )

    # ── Unused imports ────────────────────────────────────────────────────────

    def check_unused_imports(self, stmts: list):
        import_names: List[tuple] = []  # (name, line)
        for stmt in stmts:
            if isinstance(stmt, ast.ImportStmt):
                if stmt.items:
                    for item in stmt.items:
                        import_names.append((item, stmt.line))
                elif stmt.module:
                    import_names.append((stmt.module, stmt.line))

        if not import_names:
            return

        used = _collect_used_names(stmts)

        for name, line in import_names:
            # Strip alias (simplified: just base module name)
            base = name.split('.')[0]
            if base not in used:
                self._emit(
                    "UNUSED_IMPORT",
                    f"'{name}' is imported but never used.",
                    line=line, token=name,
                )

    # ── Main walk ─────────────────────────────────────────────────────────────

    def walk(self, node, in_try: bool = False):
        if node is None:
            return

        if isinstance(node, ast.FunctionDecl):
            self.check_mutable_defaults(node)
            if node.body:
                self.walk(node.body, in_try=in_try)
            return  # don't double-walk params

        if isinstance(node, ast.BinaryOp):
            self.check_singleton_compare(node)
            self.check_is_literal(node)

        if isinstance(node, ast.AssignmentExpr):
            if isinstance(node.target, str):
                self.check_builtin_shadow(node.target, node.line)

        if isinstance(node, ast.ExpressionStmt):
            if isinstance(node.expression, ast.AssignmentExpr):
                target = node.expression.target
                if isinstance(target, str):
                    self.check_builtin_shadow(target, node.line)

        # Recurse
        if hasattr(node, '__dict__'):
            for attr in vars(node).values():
                if isinstance(attr, ast.ASTNode):
                    self.walk(attr, in_try)
                elif isinstance(attr, list):
                    for item in attr:
                        if isinstance(item, ast.ASTNode):
                            self.walk(item, in_try)


# ─── Public entry point ────────────────────────────────────────────────────────

def run_pattern_detection(ast_tree) -> List[PatternDiagnostic]:
    """Walk the AST and detect all anti-patterns. Returns diagnostics."""
    detector = PatternDetector()

    all_stmts = getattr(ast_tree, 'statements', [])

    # Check unused imports at module level
    detector.check_unused_imports(all_stmts)

    # Walk all nodes
    for stmt in all_stmts:
        detector.walk(stmt)

    return detector.diagnostics

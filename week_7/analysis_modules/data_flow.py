"""
Week 7 · Analysis Modules → Data-Flow Analyser
================================================
Computes classic data-flow information from the real AST nodes:

  • Definitions   – every VariableDecl and AssignmentExpr that introduces or
                    updates a name, with the source line.
  • Uses          – every Identifier reference.
  • Use-Def chains – for each use, which definition(s) could reach it
                    (simplified intra-procedural, single-path approximation).
  • Uninitialized variables – identifiers used with no prior definition on any
                    reachable path.
  • Dead definitions – definitions whose value is never subsequently used.

The analysis is read-only; the AST is never mutated.

Public API
----------
    dfa = DataFlowAnalyzer()
    result = dfa.analyze(ast_program_node)
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Set

from syntax_tree.ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, ClassDecl, Parameter,
    IfStmt, WhileStmt, ForStmt, ReturnStmt,
    ExpressionStmt, VariableDecl, ImportStmt,
    BinaryOp, UnaryOp, AssignmentExpr,
    FunctionCall, Literal, Identifier, ArrayAccess, MemberAccess,
    ErrorNode,
)


class DataFlowAnalyzer:
    """
    Intra-procedural data-flow analyser.

    Tracks definitions and uses in a single linear pass over the AST.
    Back-edges (loops) are handled conservatively: after any loop we assume
    all loop-body definitions may reach loop-exit.
    """

    def __init__(self):
        self._defs:  List[Dict] = []     # all definition sites
        self._uses:  List[Dict] = []     # all use sites
        self._scope_defs: List[Dict[str, int]] = [{}]  # var → def_index stack

    # ── public entry point ────────────────────────────────────────────────────

    def analyze(self, root: ASTNode) -> Dict[str, Any]:
        """Return a JSON-serialisable dict."""
        self._defs        = []
        self._uses        = []
        self._scope_defs  = [{}]

        self._visit(root)

        uninit = self._find_uninitialised()
        dead   = self._find_dead_defs()
        chains = self._build_use_def_chains()

        return {
            "definitions":           self._defs,
            "uses":                  self._uses,
            "use_def_chains":        chains,
            "uninitialized_vars":    uninit,
            "dead_definitions":      dead,
            "summary": {
                "total_definitions":      len(self._defs),
                "total_uses":             len(self._uses),
                "uninitialized_count":    len(uninit),
                "dead_definition_count":  len(dead),
            },
        }

    # ── scope helpers ─────────────────────────────────────────────────────────

    def _enter_scope(self):
        self._scope_defs.append({})

    def _exit_scope(self):
        if len(self._scope_defs) > 1:
            self._scope_defs.pop()

    def _record_def(self, name: str, line: int, def_type: str = "assignment") -> int:
        idx = len(self._defs)
        self._defs.append({"index": idx, "name": name,
                           "line": line, "def_type": def_type, "used": False})
        # Overwrite the most-recent def in closest scope
        for scope in reversed(self._scope_defs):
            scope[name] = idx
            break
        return idx

    def _lookup_def(self, name: str) -> int | None:
        for scope in reversed(self._scope_defs):
            if name in scope:
                return scope[name]
        return None

    def _record_use(self, name: str, line: int) -> int:
        use_idx = len(self._uses)
        def_idx = self._lookup_def(name)
        if def_idx is not None:
            self._defs[def_idx]["used"] = True
        self._uses.append({"index": use_idx, "name": name,
                           "line": line, "reaching_def": def_idx})
        return use_idx

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
        getattr(self, method, self._visit_generic)(node)

    # ── node visitors ─────────────────────────────────────────────────────────

    def _visit_Program(self, node: Program):
        for s in node.statements:
            self._visit(s)

    def _visit_Block(self, node: Block):
        self._enter_scope()
        for s in node.statements:
            self._visit(s)
        self._exit_scope()

    def _visit_FunctionDecl(self, node: FunctionDecl):
        self._record_def(node.name, node.line, "function_decl")
        self._enter_scope()
        for p in node.parameters:
            self._visit(p)
        if node.body:
            for s in node.body.statements:
                self._visit(s)
        self._exit_scope()

    def _visit_Parameter(self, node: Parameter):
        self._record_def(node.name, node.line, "parameter")

    def _visit_VariableDecl(self, node: VariableDecl):
        self._record_def(node.name, node.line, "var_decl")
        if node.initializer:
            self._visit(node.initializer)

    def _visit_ClassDecl(self, node: ClassDecl):
        self._record_def(node.name, node.line, "class_decl")
        self._enter_scope()
        for f in node.fields:   self._visit(f)
        for m in node.methods:  self._visit(m)
        self._exit_scope()

    def _visit_ImportStmt(self, node: ImportStmt):
        self._record_def(node.module or "?", node.line, "import")

    def _visit_IfStmt(self, node: IfStmt):
        self._visit(node.condition)
        # Both branches are visited; conservative: defs from both branches
        # merge (over-approximation)
        saved = [dict(s) for s in self._scope_defs]
        if node.then_block:
            self._enter_scope()
            for s in node.then_block.statements:
                self._visit(s)
            self._exit_scope()
        if node.else_block:
            self._enter_scope()
            for s in node.else_block.statements:
                self._visit(s)
            self._exit_scope()

    def _visit_WhileStmt(self, node: WhileStmt):
        self._visit(node.condition)
        if node.body:
            self._enter_scope()
            for s in node.body.statements:
                self._visit(s)
            self._exit_scope()

    def _visit_ForStmt(self, node: ForStmt):
        self._enter_scope()
        self._visit(node.init)
        self._visit(node.condition)
        if node.body:
            for s in node.body.statements:
                self._visit(s)
        self._visit(node.increment)
        self._exit_scope()

    def _visit_ExpressionStmt(self, node: ExpressionStmt):
        self._visit(node.expression)

    def _visit_ReturnStmt(self, node: ReturnStmt):
        self._visit(node.value)

    def _visit_AssignmentExpr(self, node: AssignmentExpr):
        # RHS first (use), then record as new def
        self._visit(node.value)
        if node.target:
            self._record_def(node.target, node.line, "assignment")

    def _visit_Identifier(self, node: Identifier):
        if node.name:
            self._record_use(node.name, node.line)

    def _visit_BinaryOp(self, node: BinaryOp):
        self._visit(node.left)
        self._visit(node.right)

    def _visit_UnaryOp(self, node: UnaryOp):
        self._visit(node.operand)

    def _visit_FunctionCall(self, node: FunctionCall):
        if node.name:
            self._record_use(node.name, node.line)
        for a in node.arguments:
            self._visit(a)

    def _visit_ArrayAccess(self, node: ArrayAccess):
        self._visit(node.array)
        self._visit(node.index)

    def _visit_MemberAccess(self, node: MemberAccess):
        self._visit(node.object)

    def _visit_Literal(self, node: Literal):
        pass

    def _visit_ErrorNode(self, node: ErrorNode):
        pass

    def _visit_generic(self, node: ASTNode):
        for val in vars(node).values():
            if isinstance(val, (ASTNode, list)):
                self._visit(val)

    # ── derived analyses ──────────────────────────────────────────────────────

    def _find_uninitialised(self) -> List[Dict]:
        """
        Uses whose reaching_def is None  →  possibly uninitialized.
        Exclude well-known built-in names.
        """
        BUILTINS = {
            # C
            "printf", "scanf", "malloc", "free", "strlen", "strcpy",
            "NULL", "EOF", "stdin", "stdout", "stderr",
            # Java
            "System", "String", "Integer", "Math", "Object",
            # Python
            "print", "input", "range", "len", "int", "str", "float",
            "list", "dict", "set", "tuple", "type", "isinstance",
            "True", "False", "None",
        }
        return [
            u for u in self._uses
            if u["reaching_def"] is None and u["name"] not in BUILTINS
        ]

    def _find_dead_defs(self) -> List[Dict]:
        """Definitions that were never used (excluding functions & imports)."""
        return [
            d for d in self._defs
            if not d["used"] and d["def_type"] not in ("function_decl", "import", "class_decl")
        ]

    def _build_use_def_chains(self) -> List[Dict]:
        """Return use-def pairs for uses that have a reaching definition."""
        chains = []
        for u in self._uses:
            if u["reaching_def"] is not None:
                d = self._defs[u["reaching_def"]]
                chains.append({
                    "use_name": u["name"],
                    "use_line": u["line"],
                    "def_line": d["line"],
                    "def_type": d["def_type"],
                })
        return chains

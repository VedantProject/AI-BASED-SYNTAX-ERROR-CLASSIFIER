"""
ir/ir_builder.py — AST to Three-Address Code + CFG Builder
============================================================
Walks the Python AST produced by parsers/python_parser.py and generates:
  - A sequence of TACInstr (Three-Address Code) per basic block
  - A Control Flow Graph (CFG) of BasicBlocks per function
  - An IRProgram wrapping everything
"""

from __future__ import annotations

from typing import Optional, List
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ir.ir_nodes import (
    Op, TACInstr, BasicBlock, CFG, IRFunction, IRProgram
)
from syntax_tree import ast_nodes as ast


class _IRBuilder:
    """Translates one function (or module) to an IRFunction."""

    def __init__(self, name: str, line: int = 0):
        self.name = name
        self.line = line
        self._tmp_count  = 0
        self._lbl_count  = 0
        self._cfg        = CFG()
        self._current_id: Optional[str] = None
        self._loop_exits: List[str] = []   # stack of loop-exit block IDs (for break)
        self._loop_headers: List[str] = [] # stack of loop-header IDs (for continue)

        # Create entry block
        self._new_block("entry")
        self._cfg.entry = "entry"
        # Placeholder exit block
        exit_blk = BasicBlock(id="exit")
        self._cfg.blocks["exit"] = exit_blk
        self._cfg.exit = "exit"

    # ── helpers ───────────────────────────────────────────────────────────────

    def _tmp(self) -> str:
        t = f"_t{self._tmp_count}"
        self._tmp_count += 1
        return t

    def _lbl(self, prefix: str = "L") -> str:
        l = f"{prefix}{self._lbl_count}"
        self._lbl_count += 1
        return l

    def _new_block(self, bid: str) -> BasicBlock:
        blk = BasicBlock(id=bid)
        self._cfg.blocks[bid] = blk
        self._current_id = bid
        return blk

    def _cur(self) -> BasicBlock:
        return self._cfg.blocks[self._current_id]

    def _emit(self, instr: TACInstr):
        self._cur().instrs.append(instr)

    def _link(self, from_id: str, to_id: str):
        self._cfg.link(from_id, to_id)

    def _is_terminated(self) -> bool:
        """True if the current block already ends with JUMP/RETURN/CJUMP."""
        instrs = self._cur().instrs
        if not instrs:
            return False
        return instrs[-1].op in (Op.JUMP, Op.RETURN, Op.CJUMP)

    # ── Statement translation ─────────────────────────────────────────────────

    def build_stmts(self, stmts, params: List[str] = None):
        if params:
            for p in params:
                self._emit(TACInstr(Op.PARAM, dest=p, arg1=p, line=0))

        for stmt in (stmts or []):
            self._build_stmt(stmt)

        # Fall through to exit
        if not self._is_terminated():
            prev = self._current_id
            self._link(prev, "exit")
            self._emit(TACInstr(Op.JUMP, label="exit", line=0))

    def _build_stmt(self, node):
        if node is None:
            return

        if isinstance(node, ast.FunctionDecl):
            # Nested function — register as defined name; don't recurse here
            self._emit(TACInstr(Op.ASSIGN, dest=node.name,
                                arg1=f"<func {node.name}>", line=node.line))

        elif isinstance(node, ast.ClassDecl):
            self._emit(TACInstr(Op.ASSIGN, dest=node.name,
                                arg1=f"<class {node.name}>", line=node.line))

        elif isinstance(node, ast.ImportStmt):
            name = node.items[0] if node.items else node.module
            self._emit(TACInstr(Op.ASSIGN, dest=name or "_import",
                                arg1=f"import({node.module})", line=node.line))

        elif isinstance(node, ast.ReturnStmt):
            val = self._build_expr(node.value) if node.value else "None"
            self._emit(TACInstr(Op.RETURN, arg1=val, line=node.line))
            # link to exit
            prev = self._current_id
            self._link(prev, "exit")
            # Start a new (possibly unreachable) block
            dead_id = self._lbl("dead_")
            self._new_block(dead_id)

        elif isinstance(node, ast.BreakStmt):
            if self._loop_exits:
                target = self._loop_exits[-1]
                self._emit(TACInstr(Op.JUMP, label=target, line=node.line))
                self._link(self._current_id, target)
            else:
                self._emit(TACInstr(Op.NOP, line=node.line))  # detached break
            dead_id = self._lbl("dead_")
            self._new_block(dead_id)

        elif isinstance(node, ast.ContinueStmt):
            if self._loop_headers:
                target = self._loop_headers[-1]
                self._emit(TACInstr(Op.JUMP, label=target, line=node.line))
                self._link(self._current_id, target)
            else:
                self._emit(TACInstr(Op.NOP, line=node.line))
            dead_id = self._lbl("dead_")
            self._new_block(dead_id)

        elif isinstance(node, ast.IfStmt):
            self._build_if(node)

        elif isinstance(node, ast.WhileStmt):
            self._build_while(node)

        elif isinstance(node, ast.ForStmt):
            self._build_for(node)

        elif isinstance(node, ast.ExpressionStmt):
            self._build_expr(node.expression)

        elif isinstance(node, ast.Block):
            for s in node.statements:
                self._build_stmt(s)

        elif isinstance(node, ast.ErrorNode):
            pass  # skip error nodes

    # ── Control-flow structures ───────────────────────────────────────────────

    def _build_if(self, node: ast.IfStmt):
        cond = self._build_expr(node.condition)
        then_id  = self._lbl("if_then_")
        else_id  = self._lbl("if_else_")
        merge_id = self._lbl("if_merge_")

        prev = self._current_id
        self._emit(TACInstr(Op.CJUMP, arg1=cond,
                             label=then_id, arg2=else_id, line=node.line))
        self._link(prev, then_id)
        self._link(prev, else_id)

        # Then block
        self._new_block(then_id)
        self._build_stmt(node.then_block)
        if not self._is_terminated():
            self._link(self._current_id, merge_id)
            self._emit(TACInstr(Op.JUMP, label=merge_id, line=node.line))

        # Else block
        self._new_block(else_id)
        if node.else_block:
            self._build_stmt(node.else_block)
        if not self._is_terminated():
            self._link(self._current_id, merge_id)
            self._emit(TACInstr(Op.JUMP, label=merge_id, line=node.line))

        self._new_block(merge_id)

    def _build_while(self, node: ast.WhileStmt):
        header_id = self._lbl("while_hdr_")
        body_id   = self._lbl("while_body_")
        exit_id   = self._lbl("while_exit_")

        prev = self._current_id
        self._link(prev, header_id)
        self._emit(TACInstr(Op.JUMP, label=header_id, line=node.line))

        self._new_block(header_id)
        cond = self._build_expr(node.condition)
        self._emit(TACInstr(Op.CJUMP, arg1=cond,
                             label=body_id, arg2=exit_id, line=node.line))
        self._link(header_id, body_id)
        self._link(header_id, exit_id)

        self._loop_headers.append(header_id)
        self._loop_exits.append(exit_id)

        self._new_block(body_id)
        self._build_stmt(node.body)
        if not self._is_terminated():
            self._link(self._current_id, header_id)
            self._emit(TACInstr(Op.JUMP, label=header_id, line=node.line))

        self._loop_headers.pop()
        self._loop_exits.pop()

        self._new_block(exit_id)

    def _build_for(self, node: ast.ForStmt):
        header_id = self._lbl("for_hdr_")
        body_id   = self._lbl("for_body_")
        exit_id   = self._lbl("for_exit_")

        iter_tmp = self._tmp()
        iterable = self._build_expr(node.iterable)
        self._emit(TACInstr(Op.ASSIGN, dest=iter_tmp, arg1=f"iter({iterable})",
                             line=node.line))

        prev = self._current_id
        self._link(prev, header_id)
        self._emit(TACInstr(Op.JUMP, label=header_id, line=node.line))

        self._new_block(header_id)
        next_tmp = self._tmp()
        self._emit(TACInstr(Op.ASSIGN, dest=next_tmp,
                             arg1=f"next({iter_tmp})", line=node.line))
        cond_tmp = self._tmp()
        self._emit(TACInstr(Op.ASSIGN, dest=cond_tmp,
                             arg1=f"not_exhausted({next_tmp})", line=node.line))
        self._emit(TACInstr(Op.CJUMP, arg1=cond_tmp,
                             label=body_id, arg2=exit_id, line=node.line))
        self._link(header_id, body_id)
        self._link(header_id, exit_id)

        self._loop_headers.append(header_id)
        self._loop_exits.append(exit_id)

        self._new_block(body_id)
        if node.iterator:
            self._emit(TACInstr(Op.ASSIGN, dest=node.iterator,
                                 arg1=next_tmp, line=node.line))
        self._build_stmt(node.body)
        if not self._is_terminated():
            self._link(self._current_id, header_id)
            self._emit(TACInstr(Op.JUMP, label=header_id, line=node.line))

        self._loop_headers.pop()
        self._loop_exits.pop()

        self._new_block(exit_id)

    # ── Expression translation ─────────────────────────────────────────────────

    def _build_expr(self, node) -> str:
        if node is None:
            return "None"

        if isinstance(node, ast.Literal):
            t = self._tmp()
            val = repr(node.value)
            self._emit(TACInstr(Op.ASSIGN, dest=t, arg1=val, line=node.line))
            return t

        if isinstance(node, ast.Identifier):
            t = self._tmp()
            self._emit(TACInstr(Op.LOAD, dest=t, arg1=node.name, line=node.line))
            return t

        if isinstance(node, ast.BinaryOp):
            l = self._build_expr(node.left)
            r = self._build_expr(node.right)
            t = self._tmp()
            self._emit(TACInstr(Op.BINOP, dest=t, arg1=l,
                                 arg2=f"{node.operator} {r}", line=node.line))
            return t

        if isinstance(node, ast.UnaryOp):
            a = self._build_expr(node.operand)
            t = self._tmp()
            self._emit(TACInstr(Op.UNOP, dest=t, arg1=a,
                                 arg2=node.operator, line=node.line))
            return t

        if isinstance(node, ast.AssignmentExpr):
            rhs = self._build_expr(node.value)
            self._emit(TACInstr(Op.ASSIGN, dest=node.target,
                                 arg1=rhs, line=node.line))
            return node.target

        if isinstance(node, ast.FunctionCall):
            args = [self._build_expr(a) for a in node.arguments]
            for a in args:
                self._emit(TACInstr(Op.PARAM, arg1=a, line=node.line))
            t = self._tmp()
            self._emit(TACInstr(Op.CALL, dest=t, arg1=node.name,
                                 arg2=",".join(args), line=node.line))
            return t

        if isinstance(node, ast.MemberAccess):
            obj = self._build_expr(node.object)
            t = self._tmp()
            self._emit(TACInstr(Op.LOAD, dest=t,
                                 arg1=f"{obj}.{node.member}", line=node.line))
            return t

        if isinstance(node, ast.ArrayAccess):
            arr = self._build_expr(node.array)
            idx = self._build_expr(node.index)
            t = self._tmp()
            self._emit(TACInstr(Op.LOAD, dest=t,
                                 arg1=f"{arr}[{idx}]", line=node.line))
            return t

        return "_unknown"

    def finish(self, params: List[str] = None) -> IRFunction:
        ir_fn = IRFunction(name=self.name, params=params or [],
                           cfg=self._cfg, line=self.line)
        return ir_fn


# ─── Public entry point ────────────────────────────────────────────────────────

def build_ir(ast_tree) -> IRProgram:
    """
    Convert a Python AST (Program node) into an IRProgram.
    Returns an IRProgram with module-level CFG + one IRFunction per def.
    """
    program = IRProgram()

    if ast_tree is None:
        return program

    # Collect top-level statements (excluding function defs — they get own CFGs)
    module_stmts = []
    fn_nodes = []

    for stmt in getattr(ast_tree, "statements", []):
        if isinstance(stmt, ast.FunctionDecl):
            fn_nodes.append(stmt)
        elif isinstance(stmt, ast.ClassDecl):
            # Build IRFunctions for each method
            for method in stmt.methods:
                fn_nodes.append(method)
            module_stmts.append(stmt)  # register class name at module level
        else:
            module_stmts.append(stmt)

    # Module-level CFG
    mod_builder = _IRBuilder("<module>")
    mod_builder.build_stmts(module_stmts)
    program.module_cfg = mod_builder._cfg

    # Per-function CFGs
    for fn in fn_nodes:
        params = [p.name.lstrip("*") for p in fn.parameters]
        fn_builder = _IRBuilder(fn.name, line=fn.line)
        body_stmts = []
        if fn.body and hasattr(fn.body, "statements"):
            body_stmts = fn.body.statements
        fn_builder.build_stmts(body_stmts, params=params)
        ir_fn = fn_builder.finish(params=params)
        program.functions.append(ir_fn)

    return program

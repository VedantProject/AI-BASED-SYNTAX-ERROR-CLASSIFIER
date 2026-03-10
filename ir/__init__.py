"""
ir/ — Intermediate Representation package
==========================================
Converts a Python AST (from parsers/python_parser.py) into:
  - Three-Address Code (TAC) instructions
  - A Control Flow Graph (CFG) of BasicBlocks

Public API:
    from ir import build_ir
    ir_program = build_ir(ast_tree)
"""

from ir.ir_builder import build_ir

__all__ = ["build_ir"]

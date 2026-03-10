"""AST module for Multi-Language Parser Framework"""

from .ast_nodes import (
    ASTNode, Program, Block,
    FunctionDecl, Parameter, VariableDecl, ClassDecl,
    Statement, ExpressionStmt, IfStmt, WhileStmt, ForStmt,
    ReturnStmt, BreakStmt, ContinueStmt, ImportStmt,
    Expression, BinaryOp, UnaryOp, AssignmentExpr,
    FunctionCall, Literal, Identifier, ArrayAccess, MemberAccess,
    ErrorNode, ast_to_dict
)

__all__ = [
    'ASTNode', 'Program', 'Block',
    'FunctionDecl', 'Parameter', 'VariableDecl', 'ClassDecl',
    'Statement', 'ExpressionStmt', 'IfStmt', 'WhileStmt', 'ForStmt',
    'ReturnStmt', 'BreakStmt', 'ContinueStmt', 'ImportStmt',
    'Expression', 'BinaryOp', 'UnaryOp', 'AssignmentExpr',
    'FunctionCall', 'Literal', 'Identifier', 'ArrayAccess', 'MemberAccess',
    'ErrorNode', 'ast_to_dict'
]

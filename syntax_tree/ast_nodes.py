"""
AST Node Structures for Multi-Language Parser
Defines abstract syntax tree node classes used across all language parsers
"""

from typing import List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}(line={self.line})"


# Program Structure Nodes

@dataclass
class Program(ASTNode):
    """Root node representing entire program"""
    statements: List[ASTNode] = field(default_factory=list)
    language: str = ""
    
    def __repr__(self):
        return f"Program({self.language}, {len(self.statements)} statements)"


@dataclass
class Block(ASTNode):
    """Code block (braces or indentation-based)"""
    statements: List[ASTNode] = field(default_factory=list)


# Declaration Nodes

@dataclass
class FunctionDecl(ASTNode):
    """Function/method declaration"""
    return_type: Optional[str] = None
    name: str = ""
    parameters: List['Parameter'] = field(default_factory=list)
    body: Optional[Block] = None
    modifiers: List[str] = field(default_factory=list)  # public, static, etc.


@dataclass
class Parameter(ASTNode):
    """Function parameter"""
    param_type: Optional[str] = None
    name: str = ""


@dataclass
class VariableDecl(ASTNode):
    """Variable declaration"""
    var_type: Optional[str] = None
    name: str = ""
    initializer: Optional['Expression'] = None
    is_const: bool = False


@dataclass
class ClassDecl(ASTNode):
    """Class declaration (Java, C++)"""
    name: str = ""
    methods: List[FunctionDecl] = field(default_factory=list)
    fields: List[VariableDecl] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    parent: Optional[str] = None


# Statement Nodes

@dataclass
class Statement(ASTNode):
    """Base class for statements"""
    pass


@dataclass
class ExpressionStmt(Statement):
    """Statement containing an expression"""
    expression: Optional['Expression'] = None


@dataclass
class IfStmt(Statement):
    """If statement"""
    condition: Optional['Expression'] = None
    then_block: Optional[Block] = None
    else_block: Optional[Block] = None


@dataclass
class WhileStmt(Statement):
    """While loop"""
    condition: Optional['Expression'] = None
    body: Optional[Block] = None


@dataclass
class ForStmt(Statement):
    """For loop"""
    init: Optional[Statement] = None
    condition: Optional['Expression'] = None
    increment: Optional['Expression'] = None
    body: Optional[Block] = None
    
    # Python-style for loop
    iterator: Optional[str] = None
    iterable: Optional['Expression'] = None


@dataclass
class ReturnStmt(Statement):
    """Return statement"""
    value: Optional['Expression'] = None


@dataclass
class BreakStmt(Statement):
    """Break statement"""
    pass


@dataclass
class ContinueStmt(Statement):
    """Continue statement"""
    pass


@dataclass
class ImportStmt(Statement):
    """Import/include statement"""
    module: str = ""
    items: List[str] = field(default_factory=list)


# Expression Nodes

@dataclass
class Expression(ASTNode):
    """Base class for expressions"""
    pass


@dataclass
class BinaryOp(Expression):
    """Binary operation (a + b, a == b, etc.)"""
    left: Optional[Expression] = None
    operator: str = ""
    right: Optional[Expression] = None


@dataclass
class UnaryOp(Expression):
    """Unary operation (!a, -b, ++c, etc.)"""
    operator: str = ""
    operand: Optional[Expression] = None


@dataclass
class AssignmentExpr(Expression):
    """Assignment expression"""
    target: str = ""
    value: Optional[Expression] = None
    operator: str = "="  # =, +=, -=, etc.


@dataclass
class FunctionCall(Expression):
    """Function call"""
    name: str = ""
    arguments: List[Expression] = field(default_factory=list)


@dataclass
class Literal(Expression):
    """Literal value (number, string, boolean, null)"""
    value: Any = None
    literal_type: str = ""  # 'int', 'float', 'string', 'bool', 'null'


@dataclass
class Identifier(Expression):
    """Variable/identifier reference"""
    name: str = ""


@dataclass
class ArrayAccess(Expression):
    """Array element access"""
    array: Optional[Expression] = None
    index: Optional[Expression] = None


@dataclass
class MemberAccess(Expression):
    """Object member access (obj.field)"""
    object: Optional[Expression] = None
    member: str = ""


# Error Handling Node

@dataclass
class ErrorNode(ASTNode):
    """Represents a syntax error in the AST"""
    error_type: str = ""
    message: str = ""
    token: Optional[str] = None
    
    def __repr__(self):
        return f"ErrorNode({self.error_type}, line={self.line}, msg='{self.message}')"



@dataclass
class RepairNote:
    """
    Attached to an ErrorNode after the self-healing pass to record the
    repair that was (or was not) applied.
    """
    applied:        bool  = False   # True if a patch was written
    verified:       bool  = False   # True if re-parse confirmed improvement
    description:    str   = ""      # Human-readable summary of the action
    original_line:  str   = ""      # Source text before repair
    repaired_line:  str   = ""      # Source text after repair
    confidence:     float = 0.0     # 0.0 – 1.0
    skipped:        bool  = False
    skip_reason:    str   = ""


def ast_to_dict(node: ASTNode) -> dict:

    """Convert AST node to dictionary for JSON serialization"""
    if node is None:
        return None
    
    result = {
        'node_type': node.__class__.__name__,
        'line': node.line,
        'column': node.column
    }
    
    for field_name, field_value in node.__dict__.items():
        if field_name in ['line', 'column']:
            continue
        
        if isinstance(field_value, list):
            result[field_name] = [ast_to_dict(item) if isinstance(item, ASTNode) else item 
                                 for item in field_value]
        elif isinstance(field_value, ASTNode):
            result[field_name] = ast_to_dict(field_value)
        else:
            result[field_name] = field_value
    
    return result

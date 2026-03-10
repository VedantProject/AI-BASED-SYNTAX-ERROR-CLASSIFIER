"""
Simplified Python Grammar Specification
Defines grammar rules, keywords, operators, and syntax patterns for Python parsing
"""

# Keywords
KEYWORDS = {
    # Control flow
    'if', 'elif', 'else', 'while', 'for', 'break', 'continue', 'pass',
    'return', 'yield', 'raise', 'try', 'except', 'finally', 'with', 'as',
    
    # Definition
    'def', 'class', 'lambda',
    
    # Import
    'import', 'from',
    
    # Logical
    'and', 'or', 'not', 'is', 'in',
    
    # Literals
    'True', 'False', 'None',
    
    # Others
    'del', 'global', 'nonlocal', 'assert', 'async', 'await'
}

# Operators
OPERATORS = {
    # Arithmetic
    'ARITHMETIC': ['+', '-', '*', '/', '//', '%', '**'],
    
    # Comparison
    'COMPARISON': ['==', '!=', '<', '>', '<=', '>='],
    
    # Logical
    'LOGICAL': ['and', 'or', 'not'],
    
    # Bitwise
    'BITWISE': ['&', '|', '^', '~', '<<', '>>'],
    
    # Assignment
    'ASSIGNMENT': ['=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', '&=', '|=', '^=', '<<=', '>>='],
    
    # Membership/Identity
    'MEMBERSHIP': ['in', 'is'],
    
    # Member access
    'MEMBER': ['.'],
    
    # Other
    'OTHER': [':', '@']
}

# Delimiters
DELIMITERS = {
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'COMMA': ',',
    'COLON': ':',
    'SEMICOLON': ';',  # Rarely used in Python
    'AT': '@',  # For decorators
    'ARROW': '->'  # For type hints
}

# Grammar Rules (Simplified BNF-style)
GRAMMAR_RULES = """
# Simplified Python Grammar (indentation-sensitive)

program ::= (NEWLINE | statement)*

statement ::= simple_statement
            | compound_statement

simple_statement ::= small_statement (';' small_statement)* NEWLINE

small_statement ::= expression_statement
                  | assignment_statement
                  | pass_statement
                  | break_statement
                  | continue_statement
                  | return_statement
                  | raise_statement
                  | import_statement
                  | global_statement
                  | nonlocal_statement
                  | del_statement
                  | assert_statement

expression_statement ::= expression

assignment_statement ::= target ('=' | augmented_assign_op) expression

augmented_assign_op ::= '+=' | '-=' | '*=' | '/=' | '//=' | '%=' | '**=' | '&=' | '|=' | '^=' | '<<=' | '>>='

pass_statement ::= 'pass'

break_statement ::= 'break'

continue_statement ::= 'continue'

return_statement ::= 'return' expression?

raise_statement ::= 'raise' expression?

import_statement ::= 'import' module ('as' identifier)?
                   | 'from' module 'import' (identifier | '*') ('as' identifier)?

global_statement ::= 'global' identifier (',' identifier)*

nonlocal_statement ::= 'nonlocal' identifier (',' identifier)*

del_statement ::= 'del' target_list

assert_statement ::= 'assert' expression (',' expression)?

compound_statement ::= if_statement
                     | while_statement
                     | for_statement
                     | try_statement
                     | with_statement
                     | function_definition
                     | class_definition

if_statement ::= 'if' expression ':' suite 
                ('elif' expression ':' suite)*
                ('else' ':' suite)?

while_statement ::= 'while' expression ':' suite ('else' ':' suite)?

for_statement ::= 'for' target 'in' expression ':' suite ('else' ':' suite)?

try_statement ::= 'try' ':' suite
                 (except_clause ':' suite)+
                 ('else' ':' suite)?
                 ('finally' ':' suite)?

except_clause ::= 'except' (expression ('as' identifier)?)?

with_statement ::= 'with' with_item (',' with_item)* ':' suite

with_item ::= expression ('as' identifier)?

function_definition ::= decorator* 'def' identifier '(' parameter_list? ')' ('->' expression)? ':' suite

class_definition ::= decorator* 'class' identifier ('(' argument_list? ')')? ':' suite

decorator ::= '@' dotted_name ('(' argument_list? ')')? NEWLINE

suite ::= simple_statement 
        | NEWLINE INDENT statement+ DEDENT

parameter_list ::= parameter (',' parameter)* (',' ('*' parameter | '**' parameter))?

parameter ::= identifier (':' expression)? ('=' expression)?

expression ::= conditional_expression
             | lambda_expression
             | binary_expression
             | unary_expression
             | primary_expression

conditional_expression ::= expression 'if' expression 'else' expression

lambda_expression ::= 'lambda' parameter_list? ':' expression

binary_expression ::= expression binary_op expression

unary_expression ::= unary_op expression

primary_expression ::= identifier
                     | literal
                     | '(' expression ')'
                     | '[' expression_list? ']'
                     | '{' (key_value_list | expression_list)? '}'
                     | function_call
                     | subscription
                     | member_access
                     | comprehension

function_call ::= expression '(' argument_list? ')'

subscription ::= expression '[' expression ']'

member_access ::= expression '.' identifier

comprehension ::= '[' expression 'for' target 'in' expression ('if' expression)* ']'
                | '{' expression 'for' target 'in' expression ('if' expression)* '}'

literal ::= number | string | 'True' | 'False' | 'None'

# Special tokens for indentation tracking
INDENT ::= <increase in indentation>
DEDENT ::= <decrease in indentation>
"""

# Token Types
TOKEN_TYPES = [
    'KEYWORD',
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'OPERATOR',
    'DELIMITER',
    'COMMENT',
    'INDENT',
    'DEDENT',
    'NEWLINE',
    'WHITESPACE',
    'EOF'
]

# Common Syntax Error Patterns
COMMON_ERRORS = {
    'MISSING_COLON': 'Missing colon at end of statement header',
    'INDENTATION_ERROR': 'Unexpected indentation level',
    'INCONSISTENT_INDENTATION': 'Inconsistent use of tabs and spaces',
    'MISSING_PAREN': 'Missing opening or closing parenthesis',
    'MISSING_BRACKET': 'Missing opening or closing bracket',
    'MISSING_BRACE': 'Missing opening or closing brace',
    'INVALID_SYNTAX': 'Invalid syntax',
    'INVALID_EXPRESSION': 'Malformed expression',
    'KEYWORD_MISUSE': 'Keyword used incorrectly',
    'INCOMPLETE_STATEMENT': 'Incomplete statement',
    'UNMATCHED_DELIMITER': 'Unmatched delimiter',
    'INVALID_IMPORT': 'Invalid import statement',
    'INVALID_FUNCTION_DEF': 'Invalid function definition',
    'INVALID_CLASS_DEF': 'Invalid class definition',
    'UNEXPECTED_EOF': 'Unexpected end of file',
    'INVALID_DECORATOR': 'Invalid decorator syntax'
}

# Indentation settings
INDENT_SIZE = 4  # Standard Python indentation
ALLOW_TABS = False  # PEP 8 recommends spaces only


def is_keyword(word: str) -> bool:
    """Check if a word is a Python keyword"""
    return word in KEYWORDS


def is_builtin_type(word: str) -> bool:
    """Check if a word is a built-in type"""
    builtin_types = {'int', 'float', 'str', 'bool', 'list', 'dict', 
                     'tuple', 'set', 'frozenset', 'bytes', 'bytearray'}
    return word in builtin_types


def get_operator_type(op: str) -> str:
    """Get the category of an operator"""
    for op_type, operators in OPERATORS.items():
        if op in operators:
            return op_type
    return 'UNKNOWN'


def calculate_indent_level(line: str) -> int:
    """Calculate indentation level of a line"""
    indent_count = 0
    for char in line:
        if char == ' ':
            indent_count += 1
        elif char == '\t':
            indent_count += INDENT_SIZE  # Count tab as INDENT_SIZE spaces
        else:
            break
    return indent_count // INDENT_SIZE


def is_blank_or_comment(line: str) -> bool:
    """Check if line is blank or only contains a comment"""
    stripped = line.strip()
    return not stripped or stripped.startswith('#')

"""
Simplified C/C++ Grammar Specification
Defines grammar rules, keywords, operators, and syntax patterns for C/C++ parsing
"""

# Keywords
KEYWORDS = {
    # Type keywords
    'int', 'float', 'double', 'char', 'void', 'bool', 'long', 'short',
    'unsigned', 'signed', 'struct', 'enum', 'union', 'typedef',
    
    # Control flow
    'if', 'else', 'switch', 'case', 'default', 'break', 'continue',
    'for', 'while', 'do', 'goto', 'return',
    
    # Storage class
    'auto', 'static', 'extern', 'register', 'const', 'volatile',
    
    # Others
    'sizeof', 'typedef',
    
    # C++ specific
    'class', 'public', 'private', 'protected', 'namespace', 'using',
    'new', 'delete', 'this', 'virtual', 'override', 'template',
    'try', 'catch', 'throw', 'true', 'false', 'nullptr'
}

# Operators (ordered by precedence, highest to lowest)
OPERATORS = {
    # Arithmetic
    'ARITHMETIC': ['+', '-', '*', '/', '%'],
    
    # Comparison
    'COMPARISON': ['==', '!=', '<', '>', '<=', '>='],
    
    # Logical
    'LOGICAL': ['&&', '||', '!'],
    
    # Bitwise
    'BITWISE': ['&', '|', '^', '~', '<<', '>>'],
    
    # Assignment
    'ASSIGNMENT': ['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>='],
    
    # Increment/Decrement
    'INCREMENT': ['++', '--'],
    
    # Member access
    'MEMBER': ['.', '->'],
    
    # Pointer
    'POINTER': ['*', '&'],
    
    # Other
    'OTHER': ['?', ':']
}

# Delimiters
DELIMITERS = {
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'SEMICOLON': ';',
    'COMMA': ',',
    'COLON': ':',
    'HASH': '#'
}

# Grammar Rules (Simplified BNF-style)
GRAMMAR_RULES = """
# Simplified C/C++ Grammar

program ::= (declaration | function_definition | preprocessor)*

preprocessor ::= '#' 'include' '<' identifier '>' 
               | '#' 'include' '"' identifier '"'
               | '#' 'define' identifier value?

declaration ::= type identifier ('=' expression)? ';'
              | type identifier '[' number ']' ';'
              | 'struct' identifier '{' (declaration)* '}' ';'
              | 'class' identifier '{' class_body '}' ';'

class_body ::= (access_specifier ':')? (declaration | method_definition)*

access_specifier ::= 'public' | 'private' | 'protected'

function_definition ::= type identifier '(' parameter_list? ')' block

parameter_list ::= parameter (',' parameter)*

parameter ::= type identifier ('=' expression)?

block ::= '{' statement* '}'

statement ::= expression_statement
            | declaration
            | if_statement
            | while_statement
            | for_statement
            | return_statement
            | break_statement
            | continue_statement
            | block

expression_statement ::= expression? ';'

if_statement ::= 'if' '(' expression ')' block ('else' block)?

while_statement ::= 'while' '(' expression ')' block

for_statement ::= 'for' '(' (declaration | expression)? ';' expression? ';' expression? ')' block

return_statement ::= 'return' expression? ';'

break_statement ::= 'break' ';'

continue_statement ::= 'continue' ';'

expression ::= assignment_expression
             | binary_expression
             | unary_expression
             | primary_expression

assignment_expression ::= identifier assignment_op expression

binary_expression ::= expression binary_op expression

unary_expression ::= unary_op expression
                   | expression '++'
                   | expression '--'

primary_expression ::= identifier
                     | literal
                     | '(' expression ')'
                     | function_call
                     | array_access
                     | member_access

function_call ::= identifier '(' argument_list? ')'

argument_list ::= expression (',' expression)*

array_access ::= identifier '[' expression ']'

member_access ::= expression '.' identifier
                | expression '->' identifier

type ::= 'int' | 'float' | 'double' | 'char' | 'void' | 'bool' 
       | 'long' | 'short' | identifier

literal ::= number | string | character | 'true' | 'false' | 'nullptr'
"""

# Token Types
TOKEN_TYPES = [
    'KEYWORD',
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'CHAR',
    'OPERATOR',
    'DELIMITER',
    'COMMENT',
    'PREPROCESSOR',
    'WHITESPACE',
    'NEWLINE',
    'EOF'
]

# Common Syntax Error Patterns
COMMON_ERRORS = {
    'MISSING_SEMICOLON': 'Missing semicolon at end of statement',
    'MISSING_BRACE': 'Missing opening or closing brace',
    'MISSING_PAREN': 'Missing opening or closing parenthesis',
    'MISSING_BRACKET': 'Missing opening or closing bracket',
    'INVALID_DECLARATION': 'Invalid variable or function declaration',
    'INVALID_EXPRESSION': 'Malformed expression',
    'KEYWORD_MISUSE': 'Keyword used incorrectly',
    'INCOMPLETE_STATEMENT': 'Incomplete statement',
    'UNMATCHED_DELIMITER': 'Unmatched delimiter',
    'INVALID_TYPE': 'Invalid or missing type specifier',
    'MISSING_RETURN_TYPE': 'Function missing return type',
    'INVALID_PREPROCESSOR': 'Invalid preprocessor directive'
}


def is_keyword(word: str) -> bool:
    """Check if a word is a C/C++ keyword"""
    return word in KEYWORDS


def is_type_keyword(word: str) -> bool:
    """Check if a word is a type keyword"""
    type_keywords = {'int', 'float', 'double', 'char', 'void', 'bool', 
                     'long', 'short', 'unsigned', 'signed', 'struct', 'class'}
    return word in type_keywords


def get_operator_type(op: str) -> str:
    """Get the category of an operator"""
    for op_type, operators in OPERATORS.items():
        if op in operators:
            return op_type
    return 'UNKNOWN'

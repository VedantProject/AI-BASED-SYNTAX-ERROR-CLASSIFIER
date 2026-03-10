"""
Simplified Java Grammar Specification
Defines grammar rules, keywords, operators, and syntax patterns for Java parsing
"""

# Keywords
KEYWORDS = {
    # Type keywords
    'byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'void',
    
    # Class/Object
    'class', 'interface', 'extends', 'implements', 'new', 'this', 'super',
    'instanceof', 'enum', 'package', 'import',
    
    # Access modifiers
    'public', 'private', 'protected', 'default',
    
    # Modifiers
    'static', 'final', 'abstract', 'synchronized', 'volatile', 'transient',
    'native', 'strictfp',
    
    # Control flow
    'if', 'else', 'switch', 'case', 'default', 'break', 'continue',
    'for', 'while', 'do', 'return',
    
    # Exception handling
    'try', 'catch', 'finally', 'throw', 'throws', 'assert',
    
    # Literals
    'true', 'false', 'null',
    
    # Others
    'const', 'goto'  # Reserved but not used
}

# Operators
OPERATORS = {
    # Arithmetic
    'ARITHMETIC': ['+', '-', '*', '/', '%'],
    
    # Comparison
    'COMPARISON': ['==', '!=', '<', '>', '<=', '>='],
    
    # Logical
    'LOGICAL': ['&&', '||', '!'],
    
    # Bitwise
    'BITWISE': ['&', '|', '^', '~', '<<', '>>', '>>>'],
    
    # Assignment
    'ASSIGNMENT': ['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '>>>='],
    
    # Increment/Decrement
    'INCREMENT': ['++', '--'],
    
    # Member access
    'MEMBER': ['.'],
    
    # Other
    'OTHER': ['?', ':', '::']
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
    'AT': '@'  # For annotations
}

# Grammar Rules (Simplified BNF-style)
GRAMMAR_RULES = """
# Simplified Java Grammar

program ::= package_declaration? import_declaration* type_declaration*

package_declaration ::= 'package' qualified_name ';'

import_declaration ::= 'import' 'static'? qualified_name ('.' '*')? ';'

type_declaration ::= class_declaration
                   | interface_declaration
                   | enum_declaration

class_declaration ::= modifier* 'class' identifier 
                     ('extends' type)? 
                     ('implements' type_list)?
                     '{' class_body '}'

interface_declaration ::= modifier* 'interface' identifier 
                        ('extends' type_list)?
                        '{' interface_body '}'

enum_declaration ::= modifier* 'enum' identifier '{' enum_constants '}'

class_body ::= (field_declaration | method_declaration | constructor_declaration)*

field_declaration ::= modifier* type identifier ('=' expression)? ';'

method_declaration ::= modifier* type identifier '(' parameter_list? ')' 
                      ('throws' type_list)? 
                      (block | ';')

constructor_declaration ::= modifier* identifier '(' parameter_list? ')' 
                          ('throws' type_list)? block

parameter_list ::= parameter (',' parameter)*

parameter ::= 'final'? type identifier

block ::= '{' statement* '}'

statement ::= local_variable_declaration
            | expression_statement
            | if_statement
            | while_statement
            | for_statement
            | enhanced_for_statement
            | return_statement
            | break_statement
            | continue_statement
            | try_statement
            | throw_statement
            | block
            | ';'

local_variable_declaration ::= type identifier ('=' expression)? ';'

expression_statement ::= expression ';'

if_statement ::= 'if' '(' expression ')' statement ('else' statement)?

while_statement ::= 'while' '(' expression ')' statement

for_statement ::= 'for' '(' (type identifier '=' expression | expression)? ';' 
                             expression? ';' 
                             expression? ')' statement

enhanced_for_statement ::= 'for' '(' type identifier ':' expression ')' statement

return_statement ::= 'return' expression? ';'

break_statement ::= 'break' identifier? ';'

continue_statement ::= 'continue' identifier? ';'

try_statement ::= 'try' block catch_clause* finally_clause?

catch_clause ::= 'catch' '(' type identifier ')' block

finally_clause ::= 'finally' block

throw_statement ::= 'throw' expression ';'

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
                     | 'this'
                     | 'super'
                     | '(' expression ')'
                     | 'new' type '(' argument_list? ')'
                     | method_call
                     | array_access
                     | member_access

method_call ::= identifier '(' argument_list? ')'

array_access ::= identifier '[' expression ']'

member_access ::= expression '.' identifier

type ::= primitive_type ('[' ']')*
       | reference_type ('[' ']')*

primitive_type ::= 'byte' | 'short' | 'int' | 'long' | 'float' | 'double' | 'boolean' | 'char'

modifier ::= 'public' | 'private' | 'protected' | 'static' | 'final' | 'abstract' 
           | 'synchronized' | 'volatile' | 'transient' | 'native'

literal ::= number | string | character | 'true' | 'false' | 'null'
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
    'ANNOTATION',
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
    'INVALID_DECLARATION': 'Invalid variable, method, or class declaration',
    'INVALID_EXPRESSION': 'Malformed expression',
    'KEYWORD_MISUSE': 'Keyword used incorrectly',
    'INCOMPLETE_STATEMENT': 'Incomplete statement',
    'UNMATCHED_DELIMITER': 'Unmatched delimiter',
    'INVALID_TYPE': 'Invalid or missing type specifier',
    'MISSING_RETURN_TYPE': 'Method missing return type',
    'INVALID_MODIFIER': 'Invalid or conflicting modifier',
    'MISSING_CLASS_NAME': 'Class declaration missing name',
    'INVALID_PACKAGE': 'Invalid package declaration',
    'INVALID_IMPORT': 'Invalid import statement'
}


def is_keyword(word: str) -> bool:
    """Check if a word is a Java keyword"""
    return word in KEYWORDS


def is_primitive_type(word: str) -> bool:
    """Check if a word is a primitive type"""
    primitive_types = {'byte', 'short', 'int', 'long', 'float', 
                       'double', 'boolean', 'char', 'void'}
    return word in primitive_types


def is_modifier(word: str) -> bool:
    """Check if a word is an access/class modifier"""
    modifiers = {'public', 'private', 'protected', 'static', 'final', 
                 'abstract', 'synchronized', 'volatile', 'transient', 'native'}
    return word in modifiers


def get_operator_type(op: str) -> str:
    """Get the category of an operator"""
    for op_type, operators in OPERATORS.items():
        if op in operators:
            return op_type
    return 'UNKNOWN'

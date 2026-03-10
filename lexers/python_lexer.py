"""
Python Lexer (Tokenizer)
Converts Python source code into a stream of tokens with indentation tracking
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass
from grammars import python_grammar


@dataclass
class Token:
    """Represents a single token"""
    type: str
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"


class PythonLexer:
    """Lexical analyzer for Python with indentation tracking"""
    
    def __init__(self, source: str):
        self.source = source
        self.lines = source.split('\n')
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack = [0]  # Track indentation levels
        
    def error(self, message: str) -> Token:
        """Create an error token"""
        return Token('ERROR', message, self.line, self.column)
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead at character without consuming"""
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        """Consume and return current character"""
        if self.position >= len(self.source):
            return None
        
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace_inline(self):
        """Skip whitespace on current line (not including newline)"""
        while self.peek() and self.peek() in ' \t':
            self.advance()
    
    def skip_line_comment(self):
        """Skip # style comment"""
        while self.peek() and self.peek() != '\n':
            self.advance()
    
    def get_line_indentation(self, line_str: str) -> Tuple[int, bool, bool]:
        """
        Get indentation level of a line
        Returns: (indent_level, has_tabs, has_spaces)
        """
        indent_count = 0
        has_tabs = False
        has_spaces = False
        
        for char in line_str:
            if char == ' ':
                indent_count += 1
                has_spaces = True
            elif char == '\t':
                indent_count += python_grammar.INDENT_SIZE
                has_tabs = True
            else:
                break
        
        return indent_count, has_tabs, has_spaces
    
    def handle_indentation(self, line_str: str) -> List[Token]:
        """Handle indentation tokens for a new line"""
        indent_tokens = []
        
        # Skip blank lines and comments for indentation purposes
        if python_grammar.is_blank_or_comment(line_str):
            return indent_tokens
        
        indent_count, has_tabs, has_spaces = self.get_line_indentation(line_str)
        
        # Check for mixed tabs and spaces
        if has_tabs and has_spaces:
            indent_tokens.append(self.error("Inconsistent use of tabs and spaces in indentation"))
            return indent_tokens
        
        current_indent = self.indent_stack[-1]
        
        if indent_count > current_indent:
            # Increase in indentation
            self.indent_stack.append(indent_count)
            indent_tokens.append(Token('INDENT', f'<+{indent_count - current_indent}>', 
                                      self.line, 1))
        elif indent_count < current_indent:
            # Decrease in indentation
            while self.indent_stack and indent_count < self.indent_stack[-1]:
                old_indent = self.indent_stack.pop()
                indent_tokens.append(Token('DEDENT', f'<-{old_indent - indent_count}>', 
                                          self.line, 1))
            
            # Check if dedent doesn't match any previous indentation level
            if self.indent_stack and indent_count != self.indent_stack[-1]:
                indent_tokens.append(self.error("Unindent does not match any outer indentation level"))
        
        return indent_tokens
    
    def read_number(self) -> Token:
        """Read numeric literal"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        # Handle hex numbers
        if self.peek() == '0' and self.peek(1) in 'xX':
            num_str += self.advance()  # 0
            num_str += self.advance()  # x
            while self.peek() and self.peek() in '0123456789abcdefABCDEF_':
                num_str += self.advance()
            return Token('NUMBER', num_str, start_line, start_col)
        
        # Handle binary numbers
        if self.peek() == '0' and self.peek(1) in 'bB':
            num_str += self.advance()  # 0
            num_str += self.advance()  # b
            while self.peek() and self.peek() in '01_':
                num_str += self.advance()
            return Token('NUMBER', num_str, start_line, start_col)
        
        # Handle octal numbers
        if self.peek() == '0' and self.peek(1) in 'oO':
            num_str += self.advance()  # 0
            num_str += self.advance()  # o
            while self.peek() and self.peek() in '01234567_':
                num_str += self.advance()
            return Token('NUMBER', num_str, start_line, start_col)
        
        # Regular numbers
        has_dot = False
        while self.peek() and (self.peek().isdigit() or self.peek() in '._'):
            if self.peek() == '.':
                if has_dot or (self.peek(1) and not self.peek(1).isdigit()):
                    break
                has_dot = True
            num_str += self.advance()
        
        # Handle scientific notation
        if self.peek() and self.peek() in 'eE':
            num_str += self.advance()
            if self.peek() and self.peek() in '+-':
                num_str += self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.advance()
        
        # Handle imaginary numbers
        if self.peek() and self.peek() in 'jJ':
            num_str += self.advance()
        
        return Token('NUMBER', num_str, start_line, start_col)
    
    def read_string(self, quote: str) -> Token:
        """Read string literal (including triple-quoted strings)"""
        start_line = self.line
        start_col = self.column
        
        # Check for triple-quoted string
        if self.peek(1) == quote and self.peek(2) == quote:
            return self.read_triple_quoted_string(quote)
        
        string_val = quote
        self.advance()  # Skip opening quote
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                string_val += self.advance()  # Backslash
                if self.peek():
                    string_val += self.advance()  # Escaped char
            elif self.peek() == '\n':
                # Unterminated string
                return self.error(f"Unterminated string literal")
            else:
                string_val += self.advance()
        
        if self.peek() == quote:
            string_val += self.advance()  # Closing quote
        else:
            return self.error(f"Unterminated string literal")
        
        return Token('STRING', string_val, start_line, start_col)
    
    def read_triple_quoted_string(self, quote: str) -> Token:
        """Read triple-quoted string (can span multiple lines)"""
        start_line = self.line
        start_col = self.column
        string_val = quote + quote + quote
        
        # Skip opening quotes
        self.advance()
        self.advance()
        self.advance()
        
        while self.peek():
            if self.peek() == quote and self.peek(1) == quote and self.peek(2) == quote:
                string_val += self.advance()
                string_val += self.advance()
                string_val += self.advance()
                return Token('STRING', string_val, start_line, start_col)
            elif self.peek() == '\\':
                string_val += self.advance()
                if self.peek():
                    string_val += self.advance()
            else:
                string_val += self.advance()
        
        return self.error("Unterminated triple-quoted string")
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        
        token_type = 'KEYWORD' if python_grammar.is_keyword(ident) else 'IDENTIFIER'
        return Token(token_type, ident, start_line, start_col)
    
    def read_operator(self) -> Token:
        """Read operator"""
        start_line = self.line
        start_col = self.column
        
        # Try to match multi-character operators first
        two_char = self.peek() + (self.peek(1) or '')
        three_char = two_char + (self.peek(2) or '')
        
        # Three-character operators
        if three_char in ['//=', '**=', '<<=', '>>=']:
            op = ''
            for _ in range(3):
                op += self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        # Two-character operators
        two_char_ops = ['//', '**', '<<', '>>', '<=', '>=', '==', '!=', 
                       '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '->']
        if two_char in two_char_ops:
            op = self.advance() + self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        # Single-character operators
        single_ops = ['+', '-', '*', '/', '%', '&', '|', '^', '~', 
                     '!', '=', '<', '>', '.', '@']
        if self.peek() in single_ops:
            op = self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        return None
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        self.tokens = []
        line_start = True
        
        while self.position < len(self.source):
            # Handle indentation at start of line
            if line_start and self.peek() != '\n':
                current_line_num = self.line - 1
                if current_line_num < len(self.lines):
                    indent_tokens = self.handle_indentation(self.lines[current_line_num])
                    self.tokens.extend(indent_tokens)
                line_start = False
            
            # Skip inline whitespace (not at line start)
            if not line_start:
                self.skip_whitespace_inline()
            
            if self.peek() is None:
                break
            
            # Newline
            if self.peek() == '\n':
                token = Token('NEWLINE', '\\n', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                line_start = True
                continue
            
            # Comments
            if self.peek() == '#':
                self.skip_line_comment()
                continue
            
            # Numbers
            if self.peek().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings (plain or with prefix: f"", r"", b"", u"", rb"", br"", fr"", rf"")
            if self.peek() in '"\'':
                self.tokens.append(self.read_string(self.peek()))
                continue

            # String with leading prefix letter  f / r / b / u  (+ optional 2nd prefix)
            if self.peek() and self.peek().lower() in ('f', 'r', 'b', 'u'):
                p1 = self.peek(1) or ''
                p2 = self.peek(2) or ''
                is_str_prefix = (p1 in ('"', "'")) or \
                                (p1.lower() in ('r', 'b', 'f') and p2 in ('"', "'"))
                if is_str_prefix:
                    self.advance()                    # skip first prefix char
                    if self.peek() not in ('"', "'"):
                        self.advance()                # skip second prefix char
                    self.tokens.append(self.read_string(self.peek()))
                    continue

            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Delimiters
            if self.peek() in '(){}[];,:':
                delim = self.advance()
                self.tokens.append(Token('DELIMITER', delim, self.line, self.column - 1))
                continue
            
            # Operators
            op_token = self.read_operator()
            if op_token:
                self.tokens.append(op_token)
                continue
            
            # Unknown character
            unknown_char = self.advance()
            self.tokens.append(self.error(f"Unexpected character: '{unknown_char}'"))
        
        # Add remaining DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token('DEDENT', '<dedent>', self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token('EOF', '', self.line, self.column))
        return self.tokens
    
    def get_tokens(self) -> List[Token]:
        """Get the list of tokens"""
        if not self.tokens:
            self.tokenize()
        return self.tokens


def tokenize_python(source: str) -> List[Token]:
    """Convenience function to tokenize Python source code"""
    lexer = PythonLexer(source)
    return lexer.tokenize()

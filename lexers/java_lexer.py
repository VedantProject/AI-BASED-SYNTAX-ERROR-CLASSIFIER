"""
Java Lexer (Tokenizer)
Converts Java source code into a stream of tokens
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass
from grammars import java_grammar


@dataclass
class Token:
    """Represents a single token"""
    type: str
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"


class JavaLexer:
    """Lexical analyzer for Java"""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
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
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_line_comment(self):
        """Skip // style comment"""
        while self.peek() and self.peek() != '\n':
            self.advance()
    
    def skip_block_comment(self):
        """Skip /* */ style comment"""
        self.advance()  # Skip *
        while self.peek():
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()  # Skip *
                self.advance()  # Skip /
                return
            self.advance()
    
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
        
        # Handle binary numbers (Java 7+)
        if self.peek() == '0' and self.peek(1) in 'bB':
            num_str += self.advance()  # 0
            num_str += self.advance()  # b
            while self.peek() and self.peek() in '01_':
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
        
        # Handle suffixes (L, l, F, f, D, d)
        if self.peek() and self.peek() in 'lLfFdD':
            num_str += self.advance()
        
        return Token('NUMBER', num_str, start_line, start_col)
    
    def read_string(self, quote: str) -> Token:
        """Read string or character literal"""
        start_line = self.line
        start_col = self.column
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
        
        token_type = 'CHAR' if quote == "'" else 'STRING'
        return Token(token_type, string_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() in '_$'):
            ident += self.advance()
        
        token_type = 'KEYWORD' if java_grammar.is_keyword(ident) else 'IDENTIFIER'
        return Token(token_type, ident, start_line, start_col)
    
    def read_annotation(self) -> Token:
        """Read annotation"""
        start_line = self.line
        start_col = self.column
        annotation = self.advance()  # @
        
        # Read annotation name
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            annotation += self.advance()
        
        return Token('ANNOTATION', annotation, start_line, start_col)
    
    def read_operator(self) -> Token:
        """Read operator"""
        start_line = self.line
        start_col = self.column
        
        # Try to match multi-character operators first
        two_char = self.peek() + (self.peek(1) or '')
        three_char = two_char + (self.peek(2) or '')
        
        # Three-character operators
        if three_char in ['>>>', '<<=', '>>=']:
            op = ''
            for _ in range(3):
                op += self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        # Four-character operators
        four_char = three_char + (self.peek(3) or '')
        if four_char == '>>>=':
            op = ''
            for _ in range(4):
                op += self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        # Two-character operators
        two_char_ops = ['++', '--', '<<', '>>', '<=', '>=', '==', '!=', 
                       '&&', '||', '+=', '-=', '*=', '/=', '%=', '&=', 
                       '|=', '^=', '::']
        if two_char in two_char_ops:
            op = self.advance() + self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        # Single-character operators
        single_ops = ['+', '-', '*', '/', '%', '&', '|', '^', '~', 
                     '!', '=', '<', '>', '?', '.']
        if self.peek() in single_ops:
            op = self.advance()
            return Token('OPERATOR', op, start_line, start_col)
        
        return None
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source code"""
        self.tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.peek() is None:
                break
            
            # Newline
            if self.peek() == '\n':
                token = Token('NEWLINE', '\\n', self.line, self.column)
                self.tokens.append(token)
                self.advance()
                continue
            
            # Comments
            if self.peek() == '/' and self.peek(1) == '/':
                self.advance()
                self.advance()
                self.skip_line_comment()
                continue
            
            if self.peek() == '/' and self.peek(1) == '*':
                self.advance()
                self.skip_block_comment()
                continue
            
            # Annotations
            if self.peek() == '@':
                self.tokens.append(self.read_annotation())
                continue
            
            # Numbers
            if self.peek().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings and characters
            if self.peek() in '"\'':
                self.tokens.append(self.read_string(self.peek()))
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() in '_$':
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
        
        # Add EOF token
        self.tokens.append(Token('EOF', '', self.line, self.column))
        return self.tokens
    
    def get_tokens(self) -> List[Token]:
        """Get the list of tokens"""
        if not self.tokens:
            self.tokenize()
        return self.tokens


def tokenize_java(source: str) -> List[Token]:
    """Convenience function to tokenize Java source code"""
    lexer = JavaLexer(source)
    return lexer.tokenize()

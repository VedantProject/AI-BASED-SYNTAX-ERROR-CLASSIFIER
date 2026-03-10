"""
C/C++ Parser
Parses tokens into an Abstract Syntax Tree and detects syntax errors
"""

from typing import List, Optional, Union
from lexers.c_lexer import Token
from syntax_tree import ast_nodes as ast
from grammars import c_grammar

# Maximum errors before stopping parsing
MAX_ERRORS = 10

class CParser:
    """Recursive descent parser for C/C++"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors: List[ast.ErrorNode] = []
        self.error_count = 0
        
    def error(self, message: str, error_type: str = "SyntaxError") -> ast.ErrorNode:
        """Create and record an error node"""
        current = self.current_token()
        err = ast.ErrorNode(
            error_type=error_type,
            message=message,
            token=current.value if current else None,
            line=current.line if current else 0,
            column=current.column if current else 0
        )
        self.errors.append(err)
        self.error_count += 1
        return err
    
    def current_token(self) -> Optional[Token]:
        """Get current token without consuming"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at token"""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        """Consume and return current token"""
        token = self.current_token()
        if token and token.type != 'EOF':
            self.position += 1
        return token
    
    def expect(self, token_type: str, value: Optional[str] = None) -> Optional[Token]:
        """Expect a specific token type/value"""
        current = self.current_token()
        
        if not current:
            self.error(f"Expected {token_type}, got end of file")
            return None
        
        if current.type != token_type:
            self.error(f"Expected {token_type}, got {current.type} '{current.value}'")
            self.advance()  # Always advance to prevent infinite loops
            return None
        
        if value and current.value != value:
            self.error(f"Expected '{value}', got '{current.value}'")
            self.advance()  # Always advance to prevent infinite loops
            return None
        
        return self.advance()
    
    def panic_mode_recovery(self):
        """Panic mode: skip tokens until we find a synchronization point"""
        sync_points = {';', '}', '\n'}
        max_skip = 100  # Prevent infinite loops
        skipped = 0
        
        while self.current_token() and self.current_token().type != 'EOF' and skipped < max_skip:
            current = self.current_token()
            
            # Found a sync point
            if current.value in sync_points or current.type == 'NEWLINE':
                if current.value in [';', '}']:
                    self.advance()  # Consume the sync token
                return
            
            self.advance()
            skipped += 1
    
    def skip_to_delimiter(self, delimiters: List[str]):
        """Skip tokens until we hit one of the delimiters"""
        max_skip = 100  # Prevent infinite loops
        skipped = 0
        while self.current_token() and self.current_token().type != 'EOF' and skipped < max_skip:
            if self.current_token().type == 'DELIMITER' and self.current_token().value in delimiters:
                return
            self.advance()
            skipped += 1
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
    
    def parse(self) -> ast.Program:
        """Parse the entire program"""
        program = ast.Program(language="C/C++")
        
        while self.current_token() and self.current_token().type != 'EOF':
            # Check error limit
            if self.error_count >= MAX_ERRORS:
                self.error(f"Too many errors ({MAX_ERRORS}), stopping parse", "MAX_ERRORS_EXCEEDED")
                break
            
            self.skip_newlines()
            
            if not self.current_token() or self.current_token().type == 'EOF':
                break
            
            prev_pos = self.position
            stmt = self.parse_top_level()
            
            # Safety check: if no progress, use panic mode recovery
            if self.position == prev_pos:
                if self.current_token() and self.current_token().type != 'EOF':
                    self.error(f"Unexpected token at top level: {self.current_token().value}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                else:
                    break
                continue
            
            if stmt:
                program.statements.append(stmt)
        
        return program
    
    def parse_top_level(self) -> Optional[ast.ASTNode]:
        """Parse top-level declarations"""
        self.skip_newlines()
        current = self.current_token()
        
        if not current or current.type == 'EOF':
            return None
        
        # Preprocessor directives
        if current.type == 'PREPROCESSOR':
            return self.parse_preprocessor()
        
        # Function or variable declaration
        if current.type == 'KEYWORD':
            if current.value in ['struct', 'enum', 'union']:
                return self.parse_struct_declaration()
            elif current.value == 'class':
                return self.parse_class_declaration()
            elif c_grammar.is_type_keyword(current.value):
                return self.parse_declaration_or_function()
        
        # Type followed by identifier (declaration)
        if current.type == 'IDENTIFIER':
            # Could be a custom type
            return self.parse_declaration_or_function()
        
        self.error(f"Unexpected token at top level: {current.type} '{current.value}'")
        self.advance()
        return None
    
    def parse_preprocessor(self) -> ast.ImportStmt:
        """Parse preprocessor directive"""
        token = self.advance()
        return ast.ImportStmt(module=token.value.strip(), line=token.line, column=token.column)
    
    def parse_struct_declaration(self) -> ast.ClassDecl:
        """Parse struct/enum declaration"""
        keyword_token = self.advance()
        struct_decl = ast.ClassDecl(line=keyword_token.line, column=keyword_token.column)
        
        # Struct name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            struct_decl.name = self.advance().value
        
        # Struct body
        if self.current_token() and self.current_token().value == '{':
            self.advance()  # {
            
            iteration_count = 0
            max_iterations = 500
            
            while self.current_token() and self.current_token().value != '}' and iteration_count < max_iterations:
                iteration_count += 1
                self.skip_newlines()
                if self.current_token() and self.current_token().value == '}':
                    break
                
                if self.error_count >= MAX_ERRORS:
                    break
                
                # Save position before parsing
                prev_pos = self.position
                field = self.parse_declaration()
                
                # Safety check: if no progress was made, use panic recovery
                if self.position == prev_pos:
                    self.error(f"Unexpected token in struct body: {self.current_token().value if self.current_token() else 'EOF'}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                    continue
                    
                if field:
                    struct_decl.fields.append(field)
            
            if not self.expect('DELIMITER', '}'):
                self.error("Missing closing brace in struct declaration", "MISSING_BRACE")
        
        # Expect semicolon
        if self.current_token() and self.current_token().value != ';':
            self.error("Missing semicolon after struct declaration", "MISSING_SEMICOLON")
        else:
            self.advance()
        
        return struct_decl
    
    def parse_class_declaration(self) -> ast.ClassDecl:
        """Parse class declaration (C++)"""
        keyword_token = self.advance()  # class
        class_decl = ast.ClassDecl(line=keyword_token.line, column=keyword_token.column)
        
        # Class name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            class_decl.name = self.advance().value
        else:
            self.error("Missing class name", "MISSING_CLASS_NAME")
        
        # Inheritance
        if self.current_token() and self.current_token().value == ':':
            self.advance()
            if self.current_token() and self.current_token().type == 'KEYWORD':
                if self.current_token().value in ['public', 'private', 'protected']:
                    self.advance()  # Access specifier
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                class_decl.parent = self.advance().value
        
        # Class body
        if self.current_token() and self.current_token().value == '{':
            self.advance()  # {
            
            iteration_count = 0
            max_iterations = 500
            
            while self.current_token() and self.current_token().value != '}' and iteration_count < max_iterations:
                iteration_count += 1
                self.skip_newlines()
                if self.current_token() and self.current_token().value == '}':
                    break
                
                if self.error_count >= MAX_ERRORS:
                    break
                
                # Access specifiers
                if self.current_token() and self.current_token().value in ['public', 'private', 'protected']:
                    class_decl.modifiers.append(self.advance().value)
                    if self.current_token() and self.current_token().value == ':':
                        self.advance()
                    continue
                
                # Save position before parsing
                prev_pos = self.position
                member = self.parse_class_member()
                
                # Safety check: if no progress was made, use panic recovery
                if self.position == prev_pos:
                    self.error(f"Unexpected token in class body: {self.current_token().value if self.current_token() else 'EOF'}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                    continue
                    
                if isinstance(member, ast.FunctionDecl):
                    class_decl.methods.append(member)
                elif isinstance(member, ast.VariableDecl):
                    class_decl.fields.append(member)
            
            if not self.expect('DELIMITER', '}'):
                self.error("Missing closing brace in class declaration", "MISSING_BRACE")
        
        # Expect semicolon
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        
        return class_decl
    
    def parse_class_member(self) -> Optional[Union[ast.FunctionDecl, ast.VariableDecl]]:
        """Parse class member (method or field)"""
        return self.parse_declaration_or_function()
    
    def parse_declaration_or_function(self) -> Optional[Union[ast.FunctionDecl, ast.VariableDecl]]:
        """Parse variable declaration or function definition"""
        start_token = self.current_token()
        if not start_token:
            return None
        
        # Read type
        type_name = None
        if start_token.type == 'KEYWORD' and c_grammar.is_type_keyword(start_token.value):
            type_name = self.advance().value
        elif start_token.type == 'IDENTIFIER':
            type_name = self.advance().value
        else:
            self.error(f"Expected type specifier, got {start_token.type}", "INVALID_TYPE")
            self.advance()
            return None
        
        # Check for pointer/reference
        while self.current_token() and self.current_token().value in ['*', '&']:
            type_name += self.advance().value
        
        # Read identifier
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after type", "INVALID_DECLARATION")
            return None
        
        name_token = self.advance()
        name = name_token.value
        
        # Check if it's a function (has parentheses)
        if self.current_token() and self.current_token().value == '(':
            return self.parse_function_definition(type_name, name, start_token.line)
        else:
            return self.parse_variable_declaration_rest(type_name, name, start_token.line)
    
    def parse_function_definition(self, return_type: str, name: str, line: int) -> ast.FunctionDecl:
        """Parse function definition"""
        func = ast.FunctionDecl(return_type=return_type, name=name, line=line)
        
        # Parameters
        if not self.expect('DELIMITER', '('):
            self.error("Missing opening parenthesis in function definition", "MISSING_PAREN")
        
        # Parse parameters
        iteration_count = 0
        max_iterations = 100
        
        while self.current_token() and self.current_token().value != ')' and iteration_count < max_iterations:
            iteration_count += 1
            self.skip_newlines()
            if self.current_token() and self.current_token().value == ')':
                break
            
            prev_pos = self.position
            param = self.parse_parameter()
            if param:
                func.parameters.append(param)
            
            # Safety check
            if self.position == prev_pos:
                if self.current_token() and self.current_token().value != ')':
                    self.error(f"Unexpected token in parameter list: {self.current_token().value}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                continue
            
            if self.current_token() and self.current_token().value == ',':
                self.advance()
            elif self.current_token() and self.current_token().value != ')':
                self.error("Expected ',' or ')' in parameter list")
                break
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing closing parenthesis in function definition", "MISSING_PAREN")
        
        # Function body or semicolon
        if self.current_token() and self.current_token().value == '{':
            func.body = self.parse_block()
        elif self.current_token() and self.current_token().value == ';':
            self.advance()  # Function declaration without body
        else:
            self.error("Expected '{' or ';' after function signature", "INVALID_SYNTAX")
        
        return func
    
    def parse_parameter(self) -> Optional[ast.Parameter]:
        """Parse function parameter"""
        # Type
        if not self.current_token():
            return None
        
        param_type = None
        if self.current_token().type == 'KEYWORD':
            param_type = self.advance().value
        elif self.current_token().type == 'IDENTIFIER':
            param_type = self.advance().value
        else:
            return None
        
        # Pointer/reference
        while self.current_token() and self.current_token().value in ['*', '&']:
            param_type += self.advance().value
        
        # Name (optional in declarations)
        param_name = ""
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            param_name = self.advance().value
        
        # Arrays
        if self.current_token() and self.current_token().value == '[':
            self.advance()
            if self.current_token() and self.current_token().value == ']':
                self.advance()
                param_type += '[]'
        
        return ast.Parameter(param_type=param_type, name=param_name)
    
    def parse_variable_declaration_rest(self, var_type: str, name: str, line: int) -> ast.VariableDecl:
        """Parse rest of variable declaration"""
        var_decl = ast.VariableDecl(var_type=var_type, name=name, line=line)
        
        # Array declaration
        if self.current_token() and self.current_token().value == '[':
            self.advance()
            # Array size
            if self.current_token() and self.current_token().type == 'NUMBER':
                self.advance()
            if not self.expect('DELIMITER', ']'):
                self.error("Missing closing bracket in array declaration", "MISSING_BRACKET")
        
        # Initialization
        if self.current_token() and self.current_token().value == '=':
            self.advance()
            var_decl.initializer = self.parse_expression()
        
        # Expect semicolon
        if self.current_token() and self.current_token().value != ';':
            self.error("Missing semicolon after variable declaration", "MISSING_SEMICOLON")
        else:
            self.advance()
        
        return var_decl
    
    def parse_declaration(self) -> Optional[ast.VariableDecl]:
        """Parse variable declaration in struct/class"""
        if not self.current_token():
            return None
        
        # Type
        var_type = None
        if self.current_token().type in ['KEYWORD', 'IDENTIFIER']:
            var_type = self.advance().value
        else:
            return None
        
        # Name
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            return None
        
        name = self.advance().value
        
        var_decl = ast.VariableDecl(var_type=var_type, name=name)
        
        # Semicolon
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        
        return var_decl
    
    def parse_block(self) -> ast.Block:
        """Parse code block"""
        block = ast.Block()
        
        if not self.expect('DELIMITER', '{'):
            self.error("Missing opening brace", "MISSING_BRACE")
            self.panic_mode_recovery()
            return block
        
        iteration_count = 0
        max_iterations = 1000  # Prevent infinite loops
        
        while self.current_token() and self.current_token().value != '}' and iteration_count < max_iterations:
            iteration_count += 1
            
            # Check error limit
            if self.error_count >= MAX_ERRORS:
                break
            
            self.skip_newlines()
            if self.current_token() and self.current_token().value == '}':
                break
            
            if not self.current_token() or self.current_token().type == 'EOF':
                break
            
            # Safety check: track position to avoid infinite loop
            prev_pos = self.position
            stmt = self.parse_statement()
            
            # If no progress was made, use panic mode recovery
            if self.position == prev_pos:
                if self.current_token():
                    self.error(f"Unexpected token in block: {self.current_token().value}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                else:
                    break  # EOF reached
                continue
            
            if stmt:
                block.statements.append(stmt)
        
        if not self.expect('DELIMITER', '}'):
            self.error("Missing closing brace", "MISSING_BRACE")
        
        return block
    
    def parse_statement(self) -> Optional[ast.Statement]:
        """Parse a statement"""
        current = self.current_token()
        if not current or current.type == 'EOF':
            return None
        
        # Control flow keywords
        if current.type == 'KEYWORD':
            if current.value == 'if':
                return self.parse_if_statement()
            elif current.value == 'while':
                return self.parse_while_statement()
            elif current.value == 'for':
                return self.parse_for_statement()
            elif current.value == 'return':
                return self.parse_return_statement()
            elif current.value == 'break':
                return self.parse_break_statement()
            elif current.value == 'continue':
                return self.parse_continue_statement()
            elif c_grammar.is_type_keyword(current.value):
                # Local variable declaration
                return self.parse_declaration_or_function()
        
        # Block
        if current.type == 'DELIMITER' and current.value == '{':
            return self.parse_block()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_if_statement(self) -> ast.IfStmt:
        """Parse if statement"""
        if_token = self.advance()  # if
        if_stmt = ast.IfStmt(line=if_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'if'", "MISSING_PAREN")
        
        if_stmt.condition = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after if condition", "MISSING_PAREN")
        
        # Then block
        if self.current_token() and self.current_token().value == '{':
            if_stmt.then_block = self.parse_block()
        else:
            # Single statement
            stmt = self.parse_statement()
            if_stmt.then_block = ast.Block(statements=[stmt] if stmt else [])
        
        # Else block
        if self.current_token() and self.current_token().value == 'else':
            self.advance()  # else
            if self.current_token() and self.current_token().value == '{':
                if_stmt.else_block = self.parse_block()
            else:
                stmt = self.parse_statement()
                if_stmt.else_block = ast.Block(statements=[stmt] if stmt else [])
        
        return if_stmt
    
    def parse_while_statement(self) -> ast.WhileStmt:
        """Parse while statement"""
        while_token = self.advance()  # while
        while_stmt = ast.WhileStmt(line=while_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'while'", "MISSING_PAREN")
        
        while_stmt.condition = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after while condition", "MISSING_PAREN")
        
        if self.current_token() and self.current_token().value == '{':
            while_stmt.body = self.parse_block()
        else:
            stmt = self.parse_statement()
            while_stmt.body = ast.Block(statements=[stmt] if stmt else [])
        
        return while_stmt
    
    def parse_for_statement(self) -> ast.ForStmt:
        """Parse for statement"""
        for_token = self.advance()  # for
        for_stmt = ast.ForStmt(line=for_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'for'", "MISSING_PAREN")
        
        # Init
        if self.current_token() and self.current_token().value != ';':
            for_stmt.init = self.parse_statement()
        else:
            self.advance()  # ;
        
        # Condition
        if self.current_token() and self.current_token().value != ';':
            for_stmt.condition = self.parse_expression()
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        
        # Increment
        if self.current_token() and self.current_token().value != ')':
            for_stmt.increment = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after for clause", "MISSING_PAREN")
        
        if self.current_token() and self.current_token().value == '{':
            for_stmt.body = self.parse_block()
        else:
            stmt = self.parse_statement()
            for_stmt.body = ast.Block(statements=[stmt] if stmt else [])
        
        return for_stmt
    
    def parse_return_statement(self) -> ast.ReturnStmt:
        """Parse return statement"""
        return_token = self.advance()  # return
        return_stmt = ast.ReturnStmt(line=return_token.line)
        
        if self.current_token() and self.current_token().value != ';':
            return_stmt.value = self.parse_expression()
        
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after return statement", "MISSING_SEMICOLON")
        
        return return_stmt
    
    def parse_break_statement(self) -> ast.BreakStmt:
        """Parse break statement"""
        break_token = self.advance()  # break
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after break", "MISSING_SEMICOLON")
        return ast.BreakStmt(line=break_token.line)
    
    def parse_continue_statement(self) -> ast.ContinueStmt:
        """Parse continue statement"""
        continue_token = self.advance()  # continue
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after continue", "MISSING_SEMICOLON")
        return ast.ContinueStmt(line=continue_token.line)
    
    def parse_expression_statement(self) -> ast.ExpressionStmt:
        """Parse expression statement"""
        expr_stmt = ast.ExpressionStmt()
        expr_stmt.expression = self.parse_expression()
        
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        else:
            self.error("Missing semicolon after expression", "MISSING_SEMICOLON")
        
        return expr_stmt
    
    def parse_expression(self) -> Optional[ast.Expression]:
        """Parse expression (simplified)"""
        return self.parse_assignment_expression()
    
    def parse_assignment_expression(self) -> Optional[ast.Expression]:
        """Parse assignment expression"""
        expr = self.parse_logical_or_expression()
        
        # Assignment operators
        if self.current_token() and self.current_token().value in ['=', '+=', '-=', '*=', '/=', '%=']:
            op = self.advance().value
            right = self.parse_assignment_expression()
            if isinstance(expr, ast.Identifier):
                return ast.AssignmentExpr(target=expr.name, operator=op, value=right)
        
        return expr
    
    def parse_logical_or_expression(self) -> Optional[ast.Expression]:
        """Parse logical OR expression"""
        left = self.parse_logical_and_expression()
        
        while self.current_token() and self.current_token().value == '||':
            op = self.advance().value
            right = self.parse_logical_and_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_logical_and_expression(self) -> Optional[ast.Expression]:
        """Parse logical AND expression"""
        left = self.parse_equality_expression()
        
        while self.current_token() and self.current_token().value == '&&':
            op = self.advance().value
            right = self.parse_equality_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_equality_expression(self) -> Optional[ast.Expression]:
        """Parse equality expression"""
        left = self.parse_relational_expression()
        
        while self.current_token() and self.current_token().value in ['==', '!=']:
            op = self.advance().value
            right = self.parse_relational_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_relational_expression(self) -> Optional[ast.Expression]:
        """Parse relational expression"""
        left = self.parse_additive_expression()
        
        while self.current_token() and self.current_token().value in ['<', '>', '<=', '>=']:
            op = self.advance().value
            right = self.parse_additive_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_additive_expression(self) -> Optional[ast.Expression]:
        """Parse additive expression"""
        left = self.parse_multiplicative_expression()
        
        while self.current_token() and self.current_token().value in ['+', '-']:
            op = self.advance().value
            right = self.parse_multiplicative_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_multiplicative_expression(self) -> Optional[ast.Expression]:
        """Parse multiplicative expression"""
        left = self.parse_unary_expression()
        
        while self.current_token() and self.current_token().value in ['*', '/', '%']:
            op = self.advance().value
            right = self.parse_unary_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_unary_expression(self) -> Optional[ast.Expression]:
        """Parse unary expression"""
        current = self.current_token()
        
        if current and current.value in ['!', '-', '+', '++', '--', '*', '&', '~']:
            op = self.advance().value
            operand = self.parse_unary_expression()
            return ast.UnaryOp(operator=op, operand=operand)
        
        return self.parse_postfix_expression()
    
    def parse_postfix_expression(self) -> Optional[ast.Expression]:
        """Parse postfix expression"""
        expr = self.parse_primary_expression()
        
        iteration_count = 0
        max_iterations = 50
        
        while self.current_token() and iteration_count < max_iterations:
            iteration_count += 1
            current = self.current_token()
            
            # Function call
            if current.value == '(':
                self.advance()
                args = []
                arg_count = 0
                max_args = 100
                
                while self.current_token() and self.current_token().value != ')' and arg_count < max_args:
                    arg_count += 1
                    args.append(self.parse_expression())
                    if self.current_token() and self.current_token().value == ',':
                        self.advance()
                    elif self.current_token() and self.current_token().value != ')':
                        break
                
                if self.current_token() and self.current_token().value == ')':
                    self.advance()
                else:
                    self.error("Missing ')' in function call", "MISSING_PAREN")
                
                if isinstance(expr, ast.Identifier):
                    expr = ast.FunctionCall(name=expr.name, arguments=args)
            
            # Array access
            elif current.value == '[':
                self.advance()
                index = self.parse_expression()
                if not self.expect('DELIMITER', ']'):
                    self.error("Missing ']' in array access", "MISSING_BRACKET")
                expr = ast.ArrayAccess(array=expr, index=index)
            
            # Member access
            elif current.value in ['.', '->']:
                op = self.advance().value
                if self.current_token() and self.current_token().type == 'IDENTIFIER':
                    member = self.advance().value
                    expr = ast.MemberAccess(object=expr, member=member)
                else:
                    self.error("Expected identifier after member access operator")
            
            # Postfix increment/decrement
            elif current.value in ['++', '--']:
                op = self.advance().value
                expr = ast.UnaryOp(operator=op + '_post', operand=expr)
            
            else:
                break
        
        return expr
    
    def parse_primary_expression(self) -> Optional[ast.Expression]:
        """Parse primary expression"""
        current = self.current_token()
        
        if not current:
            return None
        
        # Parenthesized expression
        if current.value == '(':
            self.advance()
            expr = self.parse_expression()
            if not self.expect('DELIMITER', ')'):
                self.error("Missing closing parenthesis", "MISSING_PAREN")
            return expr
        
        # Literals
        if current.type == 'NUMBER':
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='number', line=token.line)
        
        if current.type == 'STRING':
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='string', line=token.line)
        
        if current.type == 'CHAR':
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='char', line=token.line)
        
        if current.type == 'KEYWORD' and current.value in ['true', 'false']:
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='bool', line=token.line)
        
        if current.type == 'KEYWORD' and current.value in ['NULL', 'nullptr']:
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='null', line=token.line)
        
        # Identifier
        if current.type == 'IDENTIFIER':
            token = self.advance()
            return ast.Identifier(name=token.value, line=token.line)
        
        self.error(f"Unexpected token in expression: {current.type} '{current.value}'", "INVALID_EXPRESSION")
        self.advance()
        return None


def parse_c(tokens: List[Token]) -> tuple:
    """Parse C/C++ tokens into AST"""
    parser = CParser(tokens)
    ast_tree = parser.parse()
    return ast_tree, parser.errors

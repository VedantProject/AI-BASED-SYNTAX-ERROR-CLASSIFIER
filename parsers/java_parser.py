"""
Java Parser
Parses tokens into an Abstract Syntax Tree and detects syntax errors
"""

from typing import List, Optional, Union
from lexers.java_lexer import Token
from syntax_tree import ast_nodes as ast
from grammars import java_grammar

# Maximum errors before stopping parsing
MAX_ERRORS = 10

class JavaParser:
    """Recursive descent parser for Java"""
    
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
        """Get current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead"""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Token:
        """Consume current token"""
        token = self.current_token()
        if token and token.type != 'EOF':
            self.position += 1
        return token
    
    def expect(self, token_type: str, value: Optional[str] = None) -> Optional[Token]:
        """Expect specific token"""
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
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
    
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
    
    def parse(self) -> ast.Program:
        """Parse entire program"""
        program = ast.Program(language="Java")
        
        # Skip package and imports
        self.skip_newlines()
        if self.current_token() and self.current_token().value == 'package':
            self.parse_package_declaration()
        
        while self.current_token() and self.current_token().value == 'import':
            program.statements.append(self.parse_import_declaration())
        
        # Parse classes
        while self.current_token() and self.current_token().type != 'EOF':
            # Check error limit
            if self.error_count >= MAX_ERRORS:
                self.error(f"Too many errors ({MAX_ERRORS}), stopping parse", "MAX_ERRORS_EXCEEDED")
                break
            
            self.skip_newlines()
            
            if not self.current_token() or self.current_token().type == 'EOF':
                break
            
            prev_pos = self.position
            stmt = self.parse_type_declaration()
            
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
    
    def parse_package_declaration(self) -> ast.ImportStmt:
        """Parse package declaration"""
        pkg_token = self.advance()  # package
        package_name = ""
        
        while self.current_token() and self.current_token().type == 'IDENTIFIER':
            package_name += self.advance().value
            if self.current_token() and self.current_token().value == '.':
                package_name += self.advance().value
        
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        else:
            self.error("Missing semicolon after package declaration", "MISSING_SEMICOLON")
        
        return ast.ImportStmt(module=package_name, line=pkg_token.line)
    
    def parse_import_declaration(self) -> ast.ImportStmt:
        """Parse import declaration"""
        import_token = self.advance()  # import
        import_stmt = ast.ImportStmt(line=import_token.line)
        
        # static import
        if self.current_token() and self.current_token().value == 'static':
            self.advance()
        
        # Build import path
        import_path = ""
        while self.current_token() and self.current_token().type == 'IDENTIFIER':
            import_path += self.advance().value
            if self.current_token() and self.current_token().value == '.':
                import_path += self.advance().value
        
        # Wildcard
        if self.current_token() and self.current_token().value == '*':
            import_path += self.advance().value
        
        import_stmt.module = import_path
        
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        else:
            self.error("Missing semicolon after import", "MISSING_SEMICOLON")
        
        return import_stmt
    
    def parse_type_declaration(self) -> Optional[ast.ClassDecl]:
        """Parse class/interface declaration"""
        self.skip_newlines()
        current = self.current_token()
        
        if not current or current.type == 'EOF':
            return None
        
        # Collect modifiers
        modifiers = []
        while current and current.type == 'KEYWORD' and java_grammar.is_modifier(current.value):
            modifiers.append(self.advance().value)
            current = self.current_token()
        
        # Class or interface
        if current and current.value == 'class':
            return self.parse_class_declaration(modifiers)
        elif current and current.value == 'interface':
            return self.parse_interface_declaration(modifiers)
        elif current and current.value == 'enum':
            return self.parse_enum_declaration(modifiers)
        
        self.error(f"Expected class, interface, or enum declaration")
        self.advance()
        return None
    
    def parse_class_declaration(self, modifiers: List[str]) -> ast.ClassDecl:
        """Parse class declaration"""
        class_token = self.advance()  # class
        class_decl = ast.ClassDecl(modifiers=modifiers, line=class_token.line)
        
        # Class name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            class_decl.name = self.advance().value
        else:
            self.error("Missing class name", "MISSING_CLASS_NAME")
        
        # Extends
        if self.current_token() and self.current_token().value == 'extends':
            self.advance()
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                class_decl.parent = self.advance().value
        
        # Implements
        if self.current_token() and self.current_token().value == 'implements':
            self.advance()
            # Skip interface names
            while self.current_token() and self.current_token().type == 'IDENTIFIER':
                self.advance()
                if self.current_token() and self.current_token().value == ',':
                    self.advance()
        
        # Class body
        if self.current_token() and self.current_token().value == '{':
            self.parse_class_body(class_decl)
        else:
            self.error("Missing class body", "MISSING_BRACE")
        
        return class_decl
    
    def parse_interface_declaration(self, modifiers: List[str]) -> ast.ClassDecl:
        """Parse interface declaration"""
        interface_token = self.advance()  # interface
        interface_decl = ast.ClassDecl(modifiers=modifiers + ['interface'], line=interface_token.line)
        
        # Interface name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            interface_decl.name = self.advance().value
        
        # Body
        if self.current_token() and self.current_token().value == '{':
            self.parse_class_body(interface_decl)
        
        return interface_decl
    
    def parse_enum_declaration(self, modifiers: List[str]) -> ast.ClassDecl:
        """Parse enum declaration"""
        enum_token = self.advance()  # enum
        enum_decl = ast.ClassDecl(modifiers=modifiers + ['enum'], line=enum_token.line)
        
        # Enum name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            enum_decl.name = self.advance().value
        
        # Skip enum body for simplicity
        if self.current_token() and self.current_token().value == '{':
            self.advance()
            depth = 1
            while self.current_token() and depth > 0:
                if self.current_token().value == '{':
                    depth += 1
                elif self.current_token().value == '}':
                    depth -= 1
                self.advance()
        
        return enum_decl
    
    def parse_class_body(self, class_decl: ast.ClassDecl):
        """Parse class body members"""
        if not self.expect('DELIMITER', '{'):
            return
        
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
            self.error("Missing closing brace in class body", "MISSING_BRACE")
    
    def parse_class_member(self) -> Optional[Union[ast.FunctionDecl, ast.VariableDecl]]:
        """Parse class member"""
        # Collect modifiers
        modifiers = []
        while self.current_token() and self.current_token().type == 'KEYWORD' and java_grammar.is_modifier(self.current_token().value):
            modifiers.append(self.advance().value)
        
        # Type or constructor
        if not self.current_token():
            return None
        
        start_token = self.current_token()
        
        # Could be type or constructor name
        type_or_name = None
        if start_token.type in ['KEYWORD', 'IDENTIFIER']:
            type_or_name = self.advance().value
        else:
            self.advance()
            return None
        
        # Check for generic type
        if self.current_token() and self.current_token().value == '<':
            # Skip generic type parameters
            self.advance()
            depth = 1
            while self.current_token() and depth > 0:
                if self.current_token().value == '<':
                    depth += 1
                elif self.current_token().value == '>':
                    depth -= 1
                self.advance()
        
        # Array type
        while self.current_token() and self.current_token().value == '[':
            self.advance()
            if self.current_token() and self.current_token().value == ']':
                self.advance()
                type_or_name += '[]'
        
        # Name
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            return None
        
        name = self.advance().value
        
        # Method or field?
        if self.current_token() and self.current_token().value == '(':
            # Method
            return self.parse_method_definition(type_or_name, name, modifiers, start_token.line)
        else:
            # Field
            return self.parse_field_declaration(type_or_name, name, modifiers, start_token.line)
    
    def parse_method_definition(self, return_type: str, name: str, modifiers: List[str], line: int) -> ast.FunctionDecl:
        """Parse method definition"""
        method = ast.FunctionDecl(return_type=return_type, name=name, modifiers=modifiers, line=line)
        
        # Parameters
        if not self.expect('DELIMITER', '('):
            return method
        
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
                method.parameters.append(param)
            
            # Safety check
            if self.position == prev_pos:
                if self.current_token() and self.current_token().value != ')':
                    self.error(f"Unexpected token in parameter list: {self.current_token().value}", "UNEXPECTED_TOKEN")
                    self.panic_mode_recovery()
                continue
            
            if self.current_token() and self.current_token().value == ',':
                self.advance()
            elif self.current_token() and self.current_token().value != ')':
                break  # Unexpected token, exit loop
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' in method signature", "MISSING_PAREN")
        
        # Throws clause
        if self.current_token() and self.current_token().value == 'throws':
            self.advance()
            while self.current_token() and self.current_token().type == 'IDENTIFIER':
                self.advance()
                if self.current_token() and self.current_token().value == ',':
                    self.advance()
        
        # Method body or semicolon
        if self.current_token() and self.current_token().value == '{':
            method.body = self.parse_block()
        elif self.current_token() and self.current_token().value == ';':
            self.advance()
        else:
            self.error("Expected '{' or ';' after method signature")
        
        return method
    
    def parse_field_declaration(self, field_type: str, name: str, modifiers: List[str], line: int) -> ast.VariableDecl:
        """Parse field declaration"""
        field = ast.VariableDecl(var_type=field_type, name=name, line=line)
        
        # Initialization
        if self.current_token() and self.current_token().value == '=':
            self.advance()
            field.initializer = self.parse_expression()
        
        # Semicolon
        if self.current_token() and self.current_token().value != ';':
            self.error("Missing semicolon after field declaration", "MISSING_SEMICOLON")
        else:
            self.advance()
        
        return field
    
    def parse_parameter(self) -> Optional[ast.Parameter]:
        """Parse method parameter"""
        # Final modifier
        if self.current_token() and self.current_token().value == 'final':
            self.advance()
        
        # Type
        if not self.current_token() or self.current_token().type not in ['KEYWORD', 'IDENTIFIER']:
            return None
        
        param_type = self.advance().value
        
        # Array type
        while self.current_token() and self.current_token().value == '[':
            self.advance()
            if self.current_token() and self.current_token().value == ']':
                self.advance()
                param_type += '[]'
        
        # Varargs
        if self.current_token() and self.current_token().value == '.':
            if self.peek() and self.peek().value == '.':
                if self.peek(2) and self.peek(2).value == '.':
                    self.advance()
                    self.advance()
                    self.advance()
                    param_type += '...'
        
        # Name
        param_name = ""
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            param_name = self.advance().value
        
        return ast.Parameter(param_type=param_type, name=param_name)
    
    def parse_block(self) -> ast.Block:
        """Parse code block"""
        block = ast.Block()
        
        if not self.expect('DELIMITER', '{'):
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
        """Parse statement"""
        current = self.current_token()
        if not current or current.type == 'EOF':
            return None
        
        # Control flow
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
            elif current.value == 'try':
                return self.parse_try_statement()
            elif current.value == 'throw':
                return self.parse_throw_statement()
            elif java_grammar.is_primitive_type(current.value) or current.value == 'final':
                # Local variable declaration
                return self.parse_local_variable_declaration()
        
        # Block
        if current.type == 'DELIMITER' and current.value == '{':
            return self.parse_block()
        
        # Type name (local variable)
        if current.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'IDENTIFIER':
            return self.parse_local_variable_declaration()
        
        # Expression statement
        return self.parse_expression_statement()
    
    def parse_local_variable_declaration(self) -> ast.VariableDecl:
        """Parse local variable declaration"""
        # Final modifier
        if self.current_token() and self.current_token().value == 'final':
            self.advance()
        
        # Type
        var_type = self.advance().value
        
        # Name
        var_name = ""
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            var_name = self.advance().value
        
        var_decl = ast.VariableDecl(var_type=var_type, name=var_name)
        
        # Initialization
        if self.current_token() and self.current_token().value == '=':
            self.advance()
            var_decl.initializer = self.parse_expression()
        
        # Semicolon
        if self.current_token() and self.current_token().value != ';':
            self.error("Missing semicolon after variable declaration", "MISSING_SEMICOLON")
        else:
            self.advance()
        
        return var_decl
    
    def parse_if_statement(self) -> ast.IfStmt:
        """Parse if statement"""
        if_token = self.advance()
        if_stmt = ast.IfStmt(line=if_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'if'", "MISSING_PAREN")
        
        if_stmt.condition = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after if condition", "MISSING_PAREN")
        
        # Then statement
        then_stmt = self.parse_statement()
        if_stmt.then_block = ast.Block(statements=[then_stmt] if then_stmt else [])
        
        # Else
        if self.current_token() and self.current_token().value == 'else':
            self.advance()
            else_stmt = self.parse_statement()
            if_stmt.else_block = ast.Block(statements=[else_stmt] if else_stmt else [])
        
        return if_stmt
    
    def parse_while_statement(self) -> ast.WhileStmt:
        """Parse while statement"""
        while_token = self.advance()
        while_stmt = ast.WhileStmt(line=while_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'while'", "MISSING_PAREN")
        
        while_stmt.condition = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after while condition", "MISSING_PAREN")
        
        body_stmt = self.parse_statement()
        while_stmt.body = ast.Block(statements=[body_stmt] if body_stmt else [])
        
        return while_stmt
    
    def parse_for_statement(self) -> ast.ForStmt:
        """Parse for statement (regular or enhanced)"""
        for_token = self.advance()
        for_stmt = ast.ForStmt(line=for_token.line)
        
        if not self.expect('DELIMITER', '('):
            self.error("Missing '(' after 'for'", "MISSING_PAREN")
        
        # Check for enhanced for loop (for (Type var : collection))
        pos_save = self.position
        is_enhanced = False
        
        # Try to detect enhanced for
        if self.current_token() and self.current_token().type in ['KEYWORD', 'IDENTIFIER']:
            self.advance()  # type
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                self.advance()  # var
                if self.current_token() and self.current_token().value == ':':
                    is_enhanced = True
        
        # Restore position
        self.position = pos_save
        
        if is_enhanced:
            # Enhanced for loop
            type_tok = self.advance()
            var_tok = self.advance()
            self.advance()  # :
            for_stmt.iterator = var_tok.value
            for_stmt.iterable = self.parse_expression()
        else:
            # Regular for loop
            if self.current_token() and self.current_token().value != ';':
                for_stmt.init = self.parse_statement()
            else:
                self.advance()
            
            if self.current_token() and self.current_token().value != ';':
                for_stmt.condition = self.parse_expression()
            if self.current_token() and self.current_token().value == ';':
                self.advance()
            
            if self.current_token() and self.current_token().value != ')':
                for_stmt.increment = self.parse_expression()
        
        if not self.expect('DELIMITER', ')'):
            self.error("Missing ')' after for clause", "MISSING_PAREN")
        
        body_stmt = self.parse_statement()
        for_stmt.body = ast.Block(statements=[body_stmt] if body_stmt else [])
        
        return for_stmt
    
    def parse_return_statement(self) -> ast.ReturnStmt:
        """Parse return statement"""
        return_token = self.advance()
        return_stmt = ast.ReturnStmt(line=return_token.line)
        
        if self.current_token() and self.current_token().value != ';':
            return_stmt.value = self.parse_expression()
        
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after return", "MISSING_SEMICOLON")
        
        return return_stmt
    
    def parse_break_statement(self) -> ast.BreakStmt:
        """Parse break statement"""
        break_token = self.advance()
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after break", "MISSING_SEMICOLON")
        return ast.BreakStmt(line=break_token.line)
    
    def parse_continue_statement(self) -> ast.ContinueStmt:
        """Parse continue statement"""
        continue_token = self.advance()
        if not self.expect('DELIMITER', ';'):
            self.error("Missing semicolon after continue", "MISSING_SEMICOLON")
        return ast.ContinueStmt(line=continue_token.line)
    
    def parse_try_statement(self) -> ast.Statement:
        """Parse try-catch statement (simplified)"""
        try_token = self.advance()
        # Parse try block
        try_block = self.parse_block()
        
        # Parse catch clauses
        while self.current_token() and self.current_token().value == 'catch':
            self.advance()
            if self.current_token() and self.current_token().value == '(':
                self.advance()
                # Skip exception type and variable
                while self.current_token() and self.current_token().value != ')':
                    self.advance()
                if self.current_token() and self.current_token().value == ')':
                    self.advance()
            self.parse_block()
        
        # Finally
        if self.current_token() and self.current_token().value == 'finally':
            self.advance()
            self.parse_block()
        
        return try_block
    
    def parse_throw_statement(self) -> ast.ExpressionStmt:
        """Parse throw statement"""
        self.advance()  # throw
        expr = self.parse_expression()
        
        if self.current_token() and self.current_token().value == ';':
            self.advance()
        else:
            self.error("Missing semicolon after throw", "MISSING_SEMICOLON")
        
        return ast.ExpressionStmt(expression=expr)
    
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
        """Parse expression"""
        return self.parse_assignment_expression()
    
    def parse_assignment_expression(self) -> Optional[ast.Expression]:
        """Parse assignment"""
        expr = self.parse_ternary_expression()
        
        if self.current_token() and self.current_token().value in ['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=']:
            op = self.advance().value
            right = self.parse_assignment_expression()
            if isinstance(expr, ast.Identifier):
                return ast.AssignmentExpr(target=expr.name, operator=op, value=right)
        
        return expr
    
    def parse_ternary_expression(self) -> Optional[ast.Expression]:
        """Parse ternary expression"""
        expr = self.parse_logical_or_expression()
        
        if self.current_token() and self.current_token().value == '?':
            self.advance()
            true_expr = self.parse_expression()
            if self.current_token() and self.current_token().value == ':':
                self.advance()
                false_expr = self.parse_expression()
                # For simplicity, return as binary op
                return ast.BinaryOp(left=expr, operator='?:', right=true_expr)
        
        return expr
    
    def parse_logical_or_expression(self) -> Optional[ast.Expression]:
        """Parse logical OR"""
        left = self.parse_logical_and_expression()
        
        while self.current_token() and self.current_token().value == '||':
            op = self.advance().value
            right = self.parse_logical_and_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_logical_and_expression(self) -> Optional[ast.Expression]:
        """Parse logical AND"""
        left = self.parse_equality_expression()
        
        while self.current_token() and self.current_token().value == '&&':
            op = self.advance().value
            right = self.parse_equality_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_equality_expression(self) -> Optional[ast.Expression]:
        """Parse equality"""
        left = self.parse_relational_expression()
        
        while self.current_token() and self.current_token().value in ['==', '!=']:
            op = self.advance().value
            right = self.parse_relational_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_relational_expression(self) -> Optional[ast.Expression]:
        """Parse relational"""
        left = self.parse_additive_expression()
        
        while self.current_token() and self.current_token().value in ['<', '>', '<=', '>=']:
            op = self.advance().value
            right = self.parse_additive_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_additive_expression(self) -> Optional[ast.Expression]:
        """Parse addition/subtraction"""
        left = self.parse_multiplicative_expression()
        
        while self.current_token() and self.current_token().value in ['+', '-']:
            op = self.advance().value
            right = self.parse_multiplicative_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_multiplicative_expression(self) -> Optional[ast.Expression]:
        """Parse multiplication/division"""
        left = self.parse_unary_expression()
        
        while self.current_token() and self.current_token().value in ['*', '/', '%']:
            op = self.advance().value
            right = self.parse_unary_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_unary_expression(self) -> Optional[ast.Expression]:
        """Parse unary expression"""
        current = self.current_token()
        
        if current and current.value in ['!', '-', '+', '++', '--', '~']:
            op = self.advance().value
            operand = self.parse_unary_expression()
            return ast.UnaryOp(operator=op, operand=operand)
        
        # Cast expression
        if current and current.value == '(' and self.peek() and self.peek().type in ['KEYWORD', 'IDENTIFIER']:
            # Could be cast or parenthesized expression
            # Simplified: treat as parenthesized
            pass
        
        return self.parse_postfix_expression()
    
    def parse_postfix_expression(self) -> Optional[ast.Expression]:
        """Parse postfix expression"""
        expr = self.parse_primary_expression()
        
        iteration_count = 0
        max_iterations = 50
        
        while self.current_token() and iteration_count < max_iterations:
            iteration_count += 1
            current = self.current_token()
            
            # Method call
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
                    self.error("Missing ')' in method call", "MISSING_PAREN")
                
                if isinstance(expr, ast.Identifier):
                    expr = ast.FunctionCall(name=expr.name, arguments=args)
            
            # Array access
            elif current.value == '[':
                self.advance()
                index = self.parse_expression()
                if not self.expect('DELIMITER', ']'):
                    self.error("Missing ']'", "MISSING_BRACKET")
                expr = ast.ArrayAccess(array=expr, index=index)
            
            # Member access
            elif current.value == '.':
                self.advance()
                if self.current_token() and self.current_token().type == 'IDENTIFIER':
                    member = self.advance().value
                    expr = ast.MemberAccess(object=expr, member=member)
            
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
        
        # Parenthesized
        if current.value == '(':
            self.advance()
            expr = self.parse_expression()
            if not self.expect('DELIMITER', ')'):
                self.error("Missing ')'", "MISSING_PAREN")
            return expr
        
        # Object creation
        if current.value == 'new':
            self.advance()
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                type_name = self.advance().value
                if self.current_token() and self.current_token().value == '(':
                    self.advance()
                    args = []
                    while self.current_token() and self.current_token().value != ')':
                        args.append(self.parse_expression())
                        if self.current_token() and self.current_token().value == ',':
                            self.advance()
                    if self.current_token() and self.current_token().value == ')':
                        self.advance()
                    return ast.FunctionCall(name='new ' + type_name, arguments=args)
        
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
        
        if current.value in ['true', 'false']:
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='bool', line=token.line)
        
        if current.value == 'null':
            token = self.advance()
            return ast.Literal(value='null', literal_type='null', line=token.line)
        
        # this, super
        if current.value in ['this', 'super']:
            token = self.advance()
            return ast.Identifier(name=token.value, line=token.line)
        
        # Identifier
        if current.type == 'IDENTIFIER':
            token = self.advance()
            return ast.Identifier(name=token.value, line=token.line)
        
        self.error(f"Unexpected token: {current.type} '{current.value}'", "INVALID_EXPRESSION")
        self.advance()
        return None


def parse_java(tokens: List[Token]) -> tuple:
    """Parse Java tokens into AST"""
    parser = JavaParser(tokens)
    ast_tree = parser.parse()
    return ast_tree, parser.errors

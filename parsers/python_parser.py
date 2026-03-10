"""
Python Parser
Parses tokens into an Abstract Syntax Tree and detects syntax errors
Handles indentation-based syntax
"""

from typing import List, Optional, Union
from lexers.python_lexer import Token
from syntax_tree import ast_nodes as ast
from grammars import python_grammar

# Maximum errors before stopping parsing
MAX_ERRORS = 10

# Module-level caches populated after every parse_python() call.
# analyze_code.py reads these to get scope info without changing the
# (ast_tree, errors) return signature of parse_python().
_last_defined_names: set = set()
_last_used_cols: dict = {}   # name -> column of first use

class PythonParser:
    """Recursive descent parser for Python"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors: List[ast.ErrorNode] = []
        self.error_count = 0
        self.indent_level = 0
        # Track lines already reported to suppress cascading duplicates
        self._reported_lines: set = set()
        # Track defined names for undefined-variable detection
        self._defined_names: set = set()
        # Track used names: name -> (line, column) of first use
        self._used_names: dict = {}
        
    def error(self, message: str, error_type: str = "SyntaxError",
              force: bool = False) -> ast.ErrorNode:
        """Create and record an error node. Suppresses duplicate line errors."""
        current = self.current_token()
        line   = current.line   if current else 0
        column = current.column if current else 0

        # Suppress cascading errors: only one error per source line
        # unless force=True (used for high-confidence primary errors)
        if not force and line in self._reported_lines:
            return ast.ErrorNode(error_type=error_type, message=message,
                                 token=None, line=line, column=column)

        self._reported_lines.add(line)
        err = ast.ErrorNode(
            error_type=error_type,
            message=message,
            token=current.value if current else None,
            line=line,
            column=column
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
            # Do NOT advance — leave the unexpected token for the caller to handle
            return None

        if value and current.value != value:
            self.error(f"Expected '{value}', got '{current.value}'")
            # Do NOT advance — caller will decide what to do
            return None

        return self.advance()

    def _expect_colon(self, keyword: str, header_line: int, header_col: int) -> bool:
        """Consume ':' for a compound-statement header.
        If missing, emits a precise MISSING_COLON error attached to the
        *header* line (not the next line) and returns False.
        Always advances past stray tokens so subsequent parsing stays on track."""
        tok = self.current_token()
        if tok and tok.value == ':':
            self.advance()
            return True
        # Emit the error at the position of the last token on the header
        # line (we pass header_line / header_col from the caller)
        if header_line not in self._reported_lines or True:  # always report
            err = ast.ErrorNode(
                error_type='MISSING_COLON',
                message=f"Missing ':' after `{keyword}` statement",
                token=tok.value if tok else None,
                line=header_line,
                column=header_col,
            )
            self._reported_lines.add(header_line)
            self.errors.append(err)
            self.error_count += 1
        # Skip to end-of-line so the suite parser starts fresh
        while self.current_token() and self.current_token().type not in (
                'NEWLINE', 'INDENT', 'DEDENT', 'EOF'):
            self.advance()
        return False
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
    
    def panic_mode_recovery(self):
        """Skip tokens until end of current line (NEWLINE/DEDENT/EOF).
        This discards the broken statement without polluting subsequent lines."""
        max_skip = 200
        skipped = 0
        while self.current_token() and self.current_token().type != 'EOF' and skipped < max_skip:
            tok = self.current_token()
            if tok.type in ('NEWLINE', 'DEDENT'):
                # Consume the NEWLINE so the outer loop sees a fresh line
                if tok.type == 'NEWLINE':
                    self.advance()
                return
            self.advance()
            skipped += 1
    
    def parse(self) -> ast.Program:
        """Parse entire program"""
        program = ast.Program(language="Python")
        
        while self.current_token() and self.current_token().type != 'EOF':
            # Check error limit
            if self.error_count >= MAX_ERRORS:
                self.error(f"Too many errors ({MAX_ERRORS}), stopping parse", "MAX_ERRORS_EXCEEDED")
                break
            
            self.skip_newlines()
            
            if not self.current_token() or self.current_token().type == 'EOF':
                break
            
            prev_pos = self.position
            stmt = self.parse_statement()
            
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
    
    def parse_statement(self) -> Optional[ast.Statement]:
        """Parse statement"""
        current = self.current_token()
        if not current or current.type == 'EOF':
            return None

        # Classify lexer ERROR tokens immediately (e.g., bad indentation)
        if current.type == 'ERROR':
            msg = current.value
            err_type = ('INDENTATION_ERROR'
                        if 'indent' in msg.lower()
                        else 'INVALID_EXPRESSION')
            self.error(msg, err_type)
            self.advance()
            return None

        # Compound statements
        if current.type == 'KEYWORD':
            if current.value == 'def':
                return self.parse_function_definition()
            elif current.value == 'class':
                return self.parse_class_definition()
            elif current.value == 'if':
                return self.parse_if_statement()
            elif current.value == 'while':
                return self.parse_while_statement()
            elif current.value == 'for':
                return self.parse_for_statement()
            elif current.value == 'try':
                return self.parse_try_statement()
            elif current.value == 'with':
                return self.parse_with_statement()
            elif current.value == 'return':
                return self.parse_return_statement()
            elif current.value == 'break':
                return self.parse_break_statement()
            elif current.value == 'continue':
                return self.parse_continue_statement()
            elif current.value == 'pass':
                return self.parse_pass_statement()
            elif current.value == 'raise':
                return self.parse_raise_statement()
            elif current.value in ['import', 'from']:
                return self.parse_import_statement()
            elif current.value in ['global', 'nonlocal']:
                return self.parse_global_statement()
            elif current.value == 'del':
                return self.parse_del_statement()
            elif current.value == 'assert':
                return self.parse_assert_statement()
        
        # Decorator
        if current.type == 'OPERATOR' and current.value == '@':
            # Decorator for function/class that follows
            decorators = self.parse_decorators()
            if self.current_token() and self.current_token().value == 'def':
                return self.parse_function_definition(decorators)
            elif self.current_token() and self.current_token().value == 'class':
                return self.parse_class_definition(decorators)
        
        # Expression statement or assignment
        return self.parse_simple_statement()
    
    def parse_decorators(self) -> List[str]:
        """Parse decorators"""
        decorators = []
        while self.current_token() and self.current_token().value == '@':
            self.advance()  # @
            decorator = ""
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                decorator = self.advance().value
                # Decorator with arguments
                if self.current_token() and self.current_token().value == '(':
                    decorator += '()'  # Simplified
                    self.advance()
                    # Skip arguments
                    depth = 1
                    while self.current_token() and self.current_token().type != 'EOF' and depth > 0:
                        if self.current_token().value == '(':
                            depth += 1
                        elif self.current_token().value == ')':
                            depth -= 1
                        if depth > 0:
                            self.advance()
                    if self.current_token() and self.current_token().value == ')':
                        self.advance()
            decorators.append(decorator)
            self.skip_newlines()
        return decorators
    
    def parse_function_definition(self, decorators: List[str] = None) -> ast.FunctionDecl:
        """Parse function definition"""
        def_token = self.advance()  # def
        func = ast.FunctionDecl(line=def_token.line)
        if decorators:
            func.modifiers = decorators
        
        # Function name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            func.name = self.advance().value
            # Register function name as defined so calls to it aren't flagged
            self._defined_names.add(func.name)
        else:
            self.error("Missing function name", "INVALID_FUNCTION_DEF")
        
        # Parameters
        if self.current_token() and self.current_token().value == '(':
            self.advance()  # consume '('
        else:
            self.error(
                f"Missing '(' in function definition of '{func.name}'",
                "MISSING_PAREN", force=True
            )

        iteration_count = 0
        max_iterations = 100

        while self.current_token() and self.current_token().value != ')' and iteration_count < max_iterations:
            iteration_count += 1
            if self.current_token() and self.current_token().value == ')':
                break
            # Stop if we hit end-of-line — the ')' is just missing
            if self.current_token() and self.current_token().type in ('NEWLINE', 'DEDENT', 'EOF'):
                break

            prev_pos = self.position
            param = self.parse_parameter()
            if param:
                func.parameters.append(param)
                # Record parameter name as defined
                self._defined_names.add(param.name.lstrip('*'))

            if self.position == prev_pos:
                if self.current_token() and self.current_token().value not in (')', ):
                    self.advance()  # skip stuck token silently
                continue

            if self.current_token() and self.current_token().value == ',':
                self.advance()
            elif self.current_token() and self.current_token().value != ')':
                break

        # Consume ')' once — the duplicate call was the bug
        if self.current_token() and self.current_token().value == ')':
            self.advance()
        # If ')' is missing, skip — do NOT emit an error here; the real error
        # is likely the missing ':' which we will report below.

        # Return type hint
        if self.current_token() and self.current_token().value == '->':
            self.advance()
            func.return_type = self.parse_expression_simple()

        # Colon — this is the primary structural error to report
        if self.current_token() and self.current_token().value == ':':
            self.advance()  # good — consume it
        else:
            fn_line = func.line if hasattr(func, 'line') else 0
            # Report on the def line (force=True so it always appears)
            tok = self.current_token()
            col = tok.column if tok else 0
            err = ast.ErrorNode(
                error_type='MISSING_COLON',
                message=f"Missing ':' after function definition of '{func.name}'",
                token=tok.value if tok else None,
                line=fn_line,
                column=col,
            )
            # Always record — this is the root cause
            self._reported_lines.add(fn_line)
            self.errors.append(err)
            self.error_count += 1
        
        # Body
        func.body = self.parse_suite()
        
        return func
    
    def parse_parameter(self) -> Optional[ast.Parameter]:
        """Parse function parameter"""
        if not self.current_token() or self.current_token().type != 'IDENTIFIER':
            # Could be *args or **kwargs
            if self.current_token() and self.current_token().value in ['*', '**']:
                star = self.advance().value
                if self.current_token() and self.current_token().type == 'IDENTIFIER':
                    name = star + self.advance().value
                    return ast.Parameter(name=name)
            return None
        
        param_name = self.advance().value
        param = ast.Parameter(name=param_name)
        
        # Type hint
        if self.current_token() and self.current_token().value == ':':
            self.advance()
            # Skip type expression
            self.parse_expression_simple()
        
        # Default value
        if self.current_token() and self.current_token().value == '=':
            self.advance()
            # Skip default value
            self.parse_expression_simple()
        
        return param
    
    def parse_class_definition(self, decorators: List[str] = None) -> ast.ClassDecl:
        """Parse class definition"""
        class_token = self.advance()  # class
        class_decl = ast.ClassDecl(line=class_token.line)
        if decorators:
            class_decl.modifiers = decorators
        
        # Class name
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            class_decl.name = self.advance().value
            self._defined_names.add(class_decl.name)
        else:
            self.error("Missing class name", "INVALID_CLASS_DEF")
        
        # Base classes
        if self.current_token() and self.current_token().value == '(':
            self.advance()
            # Parse base classes (simplified)
            while self.current_token() and self.current_token().type != 'EOF' and self.current_token().value != ')':
                if self.current_token().type == 'IDENTIFIER':
                    if not class_decl.parent:
                        class_decl.parent = self.advance().value
                    else:
                        self.advance()
                else:
                    self.advance()
                
                if self.current_token() and self.current_token().value == ',':
                    self.advance()
            
            if self.current_token() and self.current_token().value == ')':
                self.advance()
        
        # Colon
        tok_before = self.current_token()
        self._expect_colon('class', class_token.line,
                           tok_before.column if tok_before else class_token.column)
        
        # Body
        body = self.parse_suite()
        if body and isinstance(body, ast.Block):
            for stmt in body.statements:
                if isinstance(stmt, ast.FunctionDecl):
                    class_decl.methods.append(stmt)
                elif isinstance(stmt, ast.VariableDecl):
                    class_decl.fields.append(stmt)
        
        return class_decl
    
    def parse_suite(self) -> ast.Block:
        """Parse suite (indented block or simple statement)"""
        block = ast.Block()

        self.skip_newlines()

        # If we never got a colon the INDENT token won't appear — just return
        # an empty block so parent keeps parsing cleanly.
        if not self.current_token() or self.current_token().type == 'EOF':
            return block

        if self.current_token().type == 'INDENT':
            self.advance()  # INDENT

            iteration_count = 0
            max_iterations = 1000

            while (self.current_token() and
                   self.current_token().type not in ('DEDENT', 'EOF') and
                   iteration_count < max_iterations):
                iteration_count += 1

                if self.error_count >= MAX_ERRORS:
                    break

                self.skip_newlines()
                if self.current_token() and self.current_token().type in ('DEDENT', 'EOF'):
                    break

                prev_pos = self.position
                stmt = self.parse_statement()

                if self.position == prev_pos:
                    # Stuck — skip the token silently; error already on this line
                    self.advance()
                    continue

                if stmt:
                    block.statements.append(stmt)

            if self.current_token() and self.current_token().type == 'DEDENT':
                self.advance()
            # Do NOT emit INDENTATION_ERROR for missing DEDENT — it is almost
            # always a cascade of an earlier missing-colon error.
        else:
            stmt = self.parse_simple_statement()
            if stmt:
                block.statements.append(stmt)

        return block
    
    def parse_if_statement(self) -> ast.IfStmt:
        """Parse if statement"""
        if_token = self.advance()  # if
        if_stmt = ast.IfStmt(line=if_token.line)

        # Condition
        if_stmt.condition = self.parse_expression()

        # Find the column of the last token consumed (for MISSING_COLON position)
        tok_before_colon = self.current_token()
        colon_col = (tok_before_colon.column if tok_before_colon else if_token.column)
        self._expect_colon('if', if_token.line, colon_col)

        # Then block
        if_stmt.then_block = self.parse_suite()

        # Elif/else
        self.skip_newlines()
        if self.current_token() and self.current_token().value == 'elif':
            elif_tok = self.current_token()
            else_if = self.parse_if_statement()
            if_stmt.else_block = ast.Block(statements=[else_if])
        elif self.current_token() and self.current_token().value == 'else':
            else_tok = self.advance()  # else
            tok_before = self.current_token()
            self._expect_colon('else', else_tok.line,
                               tok_before.column if tok_before else else_tok.column)
            if_stmt.else_block = self.parse_suite()

        return if_stmt
    
    def parse_while_statement(self) -> ast.WhileStmt:
        """Parse while statement"""
        while_token = self.advance()  # while
        while_stmt = ast.WhileStmt(line=while_token.line)

        # Condition
        while_stmt.condition = self.parse_expression()

        tok_before = self.current_token()
        self._expect_colon('while', while_token.line,
                           tok_before.column if tok_before else while_token.column)

        # Body
        while_stmt.body = self.parse_suite()

        return while_stmt
    
    def parse_for_statement(self) -> ast.ForStmt:
        """Parse for statement"""
        for_token = self.advance()  # for
        for_stmt = ast.ForStmt(line=for_token.line)

        # Iterator variable
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            for_stmt.iterator = self.advance().value
            # Register loop variable so it isn't flagged as undefined inside body
            self._defined_names.add(for_stmt.iterator)

        # 'in' keyword
        if self.current_token() and self.current_token().type == 'KEYWORD' and self.current_token().value == 'in':
            self.advance()
        else:
            tok = self.current_token()
            self.error("Missing 'in' in for statement",
                       "INVALID_EXPRESSION", force=True)

        # Iterable
        for_stmt.iterable = self.parse_expression()

        tok_before = self.current_token()
        self._expect_colon('for', for_token.line,
                           tok_before.column if tok_before else for_token.column)

        # Body
        for_stmt.body = self.parse_suite()

        return for_stmt
    
    def parse_try_statement(self) -> ast.Statement:
        """Parse try-except statement"""
        try_token = self.advance()  # try

        tok_before = self.current_token()
        self._expect_colon('try', try_token.line,
                           tok_before.column if tok_before else try_token.column)

        # Try block
        try_block = self.parse_suite()

        # Except clauses
        while self.current_token() and self.current_token().value == 'except':
            except_tok = self.advance()  # except

            # Exception type (optional)
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                self.advance()  # Exception type
                if self.current_token() and self.current_token().value == 'as':
                    self.advance()
                    if self.current_token() and self.current_token().type == 'IDENTIFIER':
                        exc_var = self.advance().value
                        self._defined_names.add(exc_var)

            tok_before = self.current_token()
            self._expect_colon('except', except_tok.line,
                               tok_before.column if tok_before else except_tok.column)
            self.parse_suite()

        # Finally clause
        if self.current_token() and self.current_token().value == 'finally':
            fin_tok = self.advance()
            tok_before = self.current_token()
            self._expect_colon('finally', fin_tok.line,
                               tok_before.column if tok_before else fin_tok.column)
            self.parse_suite()

        return try_block
    
    def parse_with_statement(self) -> ast.Statement:
        """Parse with statement"""
        with_token = self.advance()  # with

        # Context expression
        expr = self.parse_expression()

        # as variable
        if self.current_token() and self.current_token().value == 'as':
            self.advance()
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                ctx_var = self.advance().value
                self._defined_names.add(ctx_var)

        tok_before = self.current_token()
        self._expect_colon('with', with_token.line,
                           tok_before.column if tok_before else with_token.column)

        # Body
        body = self.parse_suite()

        return ast.ExpressionStmt(expression=expr)
    
    def parse_return_statement(self) -> ast.ReturnStmt:
        """Parse return statement"""
        return_token = self.advance()  # return
        return_stmt = ast.ReturnStmt(line=return_token.line)
        
        # Return value (optional)
        if self.current_token() and self.current_token().type not in ['NEWLINE', 'EOF']:
            return_stmt.value = self.parse_expression()
        
        # Expect newline
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return return_stmt
    
    def parse_break_statement(self) -> ast.BreakStmt:
        """Parse break statement"""
        break_token = self.advance()  # break
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        return ast.BreakStmt(line=break_token.line)
    
    def parse_continue_statement(self) -> ast.ContinueStmt:
        """Parse continue statement"""
        continue_token = self.advance()  # continue
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        return ast.ContinueStmt(line=continue_token.line)
    
    def parse_pass_statement(self) -> ast.Statement:
        """Parse pass statement"""
        pass_token = self.advance()  # pass
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        return ast.ExpressionStmt()
    
    def parse_raise_statement(self) -> ast.Statement:
        """Parse raise statement"""
        self.advance()  # raise
        
        # Exception (optional)
        if self.current_token() and self.current_token().type not in ['NEWLINE', 'EOF']:
            expr = self.parse_expression()
        
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return ast.ExpressionStmt()
    
    def parse_import_statement(self) -> ast.ImportStmt:
        """Parse import statement"""
        import_token = self.advance()  # import or from
        import_stmt = ast.ImportStmt(line=import_token.line)
        
        if import_token.value == 'from':
            # from ... import ...
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                module_name = self.advance().value
                import_stmt.module = module_name
                self._defined_names.add(module_name)
            
            if self.current_token() and self.current_token().value == 'import':
                self.advance()
                
                # Import names
                while self.current_token() and self.current_token().type == 'IDENTIFIER':
                    name = self.advance().value
                    import_stmt.items.append(name)
                    self._defined_names.add(name)
                    if self.current_token() and self.current_token().value == ',':
                        self.advance()
                    else:
                        break
        else:
            # import ...
            if self.current_token() and self.current_token().type == 'IDENTIFIER':
                name = self.advance().value
                import_stmt.module = name
                self._defined_names.add(name)
                # Handle aliases:  import os.path as p
                if self.current_token() and self.current_token().value == 'as':
                    self.advance()
                    if self.current_token() and self.current_token().type == 'IDENTIFIER':
                        alias = self.advance().value
                        self._defined_names.add(alias)
        
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return import_stmt
    
    def parse_global_statement(self) -> ast.Statement:
        """Parse global/nonlocal statement"""
        self.advance()  # global/nonlocal
        
        # Variable names
        while self.current_token() and self.current_token().type == 'IDENTIFIER':
            self.advance()
            if self.current_token() and self.current_token().value == ',':
                self.advance()
        
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return ast.ExpressionStmt()
    
    def parse_del_statement(self) -> ast.Statement:
        """Parse del statement"""
        self.advance()  # del
        self.parse_expression()
        
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return ast.ExpressionStmt()
    
    def parse_assert_statement(self) -> ast.Statement:
        """Parse assert statement"""
        self.advance()  # assert
        self.parse_expression()
        
        if self.current_token() and self.current_token().value == ',':
            self.advance()
            self.parse_expression()
        
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()
        
        return ast.ExpressionStmt()
    
    def parse_simple_statement(self) -> ast.Statement:
        """Parse simple statement (expression or assignment)"""
        expr = self.parse_expression()

        # Track identifier usage for undefined-name detection
        if isinstance(expr, ast.Identifier):
            self._used_names.setdefault(expr.name, expr.line
                                        if hasattr(expr, 'line') else 0)

        # Check for assignment
        if self.current_token() and self.current_token().value in [
                '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=']:
            op = self.advance().value
            right = self.parse_expression()

            if isinstance(expr, ast.Identifier):
                # Record the assigned name as defined
                self._defined_names.add(expr.name)
                stmt = ast.ExpressionStmt(
                    expression=ast.AssignmentExpr(
                        target=expr.name, operator=op, value=right))
            else:
                stmt = ast.ExpressionStmt(expression=expr)
        else:
            # Detect missing comma: two expressions with no operator between them
            # e.g.  print("text"  result)  — result appears right after a string
            if (self.current_token() and
                    self.current_token().type not in (
                        'NEWLINE', 'DEDENT', 'EOF') and
                    self.current_token().value not in (
                        ')', ']', '}', ',', ':', '.', '(') and
                    expr is not None):
                # Only flag when the next token looks like a standalone expression
                # (identifier or literal) with nothing connecting them
                next_tok = self.current_token()
                if next_tok.type in ('IDENTIFIER', 'NUMBER', 'STRING'):
                    self.error(
                        f"Missing ',' or operator before '{next_tok.value}'",
                        "INVALID_EXPRESSION", force=True)
            stmt = ast.ExpressionStmt(expression=expr)

        # Expect newline
        if self.current_token() and self.current_token().type == 'NEWLINE':
            self.advance()

        return stmt
    
    def parse_expression(self) -> Optional[ast.Expression]:
        """Parse expression"""
        return self.parse_conditional_expression()
    
    def parse_expression_simple(self) -> str:
        """Parse expression and return as string (for type hints, etc.)"""
        # Simplified: just consume identifier or basic expression
        result = ""
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            result = self.advance().value
        return result
    
    def parse_conditional_expression(self) -> Optional[ast.Expression]:
        """Parse conditional expression (ternary)"""
        expr = self.parse_logical_or_expression()
        
        if self.current_token() and self.current_token().value == 'if':
            self.advance()
            condition = self.parse_logical_or_expression()
            if self.current_token() and self.current_token().value == 'else':
                self.advance()
                false_expr = self.parse_expression()
                # Simplified representation
                return ast.BinaryOp(left=expr, operator='if_else', right=false_expr)
        
        return expr
    
    def parse_logical_or_expression(self) -> Optional[ast.Expression]:
        """Parse logical OR"""
        left = self.parse_logical_and_expression()
        
        while self.current_token() and self.current_token().value == 'or':
            op = self.advance().value
            right = self.parse_logical_and_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_logical_and_expression(self) -> Optional[ast.Expression]:
        """Parse logical AND"""
        left = self.parse_not_expression()
        
        while self.current_token() and self.current_token().value == 'and':
            op = self.advance().value
            right = self.parse_not_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_not_expression(self) -> Optional[ast.Expression]:
        """Parse NOT expression"""
        if self.current_token() and self.current_token().value == 'not':
            op = self.advance().value
            operand = self.parse_not_expression()
            return ast.UnaryOp(operator=op, operand=operand)
        
        return self.parse_comparison_expression()
    
    def parse_comparison_expression(self) -> Optional[ast.Expression]:
        """Parse comparison"""
        left = self.parse_additive_expression()
        
        while self.current_token() and self.current_token().value in ['==', '!=', '<', '>', '<=', '>=', 'in', 'is']:
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
        
        while self.current_token() and self.current_token().value in ['*', '/', '//', '%', '**']:
            op = self.advance().value
            right = self.parse_unary_expression()
            left = ast.BinaryOp(left=left, operator=op, right=right)
        
        return left
    
    def parse_unary_expression(self) -> Optional[ast.Expression]:
        """Parse unary expression"""
        current = self.current_token()
        
        if current and current.value in ['-', '+', '~']:
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

                while (self.current_token() and
                       self.current_token().type != 'EOF' and
                       self.current_token().value != ')' and
                       arg_count < max_args):
                    arg_count += 1
                    arg = self.parse_expression()
                    args.append(arg)

                    tok = self.current_token()
                    if tok and tok.value == ',':
                        self.advance()
                    elif tok and tok.value == ')':
                        break
                    elif tok and tok.type in ('IDENTIFIER', 'NUMBER', 'STRING'):
                        # Adjacent expression without comma — missing comma error
                        self.error(
                            f"Missing ',' before '{tok.value}' in function call",
                            "INVALID_EXPRESSION", force=True)
                        # Continue parsing the next arg so we capture it
                    else:
                        break

                if self.current_token() and self.current_token().value == ')':
                    self.advance()
                else:
                    # Missing ')' — emit error at the opening-paren line
                    # so the caret lands on the call site, not the next statement
                    open_line = expr.line if hasattr(expr, 'line') else (
                        self.current_token().line if self.current_token() else 0)
                    tok = self.current_token()
                    col  = tok.column if tok else 0
                    if open_line not in self._reported_lines:
                        err = ast.ErrorNode(
                            error_type='MISSING_PAREN',
                            message=(
                                f"Missing ')' to close function call"
                                + (f" to '{expr.name}'" if isinstance(expr, ast.Identifier) else "")
                            ),
                            token=tok.value if tok else None,
                            line=open_line,
                            column=col,
                        )
                        self._reported_lines.add(open_line)
                        self.errors.append(err)
                        self.error_count += 1
                
                if isinstance(expr, ast.Identifier):
                    expr = ast.FunctionCall(name=expr.name, arguments=args)
            
            # Subscription
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
            open_tok = self.advance()   # consume '('
            expr = self.parse_expression()
            if self.current_token() and self.current_token().value == ')':
                self.advance()
            else:
                tok = self.current_token()
                if open_tok.line not in self._reported_lines:
                    err = ast.ErrorNode(
                        error_type='MISSING_PAREN',
                        message="Missing ')' — unclosed parenthesis in expression",
                        token=tok.value if tok else None,
                        line=open_tok.line,
                        column=open_tok.column,
                    )
                    self._reported_lines.add(open_tok.line)
                    self.errors.append(err)
                    self.error_count += 1
            return expr
        
        # List
        if current.value == '[':
            self.advance()
            # Skip list contents
            while self.current_token() and self.current_token().type != 'EOF' and self.current_token().value != ']':
                self.advance()
            if self.current_token() and self.current_token().value == ']':
                self.advance()
            return ast.Literal(value='[]', literal_type='list')
        
        # Dict
        if current.value == '{':
            self.advance()
            # Skip dict contents
            while self.current_token() and self.current_token().type != 'EOF' and self.current_token().value != '}':
                self.advance()
            if self.current_token() and self.current_token().value == '}':
                self.advance()
            return ast.Literal(value='{}', literal_type='dict')
        
        # Literals
        if current.type == 'NUMBER':
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='number', line=token.line)
        
        if current.type == 'STRING':
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='string', line=token.line)
        
        if current.value in ['True', 'False']:
            token = self.advance()
            return ast.Literal(value=token.value, literal_type='bool', line=token.line)
        
        if current.value == 'None':
            token = self.advance()
            return ast.Literal(value='None', literal_type='null', line=token.line)
        
        # Lambda
        if current.value == 'lambda':
            self.advance()
            # Skip lambda for simplicity
            while self.current_token() and self.current_token().type != 'EOF' and self.current_token().value != ':':
                self.advance()
            if self.current_token() and self.current_token().value == ':':
                self.advance()
                self.parse_expression()
            return ast.Literal(value='lambda', literal_type='lambda')
        
        # Identifier
        if current.type == 'IDENTIFIER':
            token = self.advance()
            # Record every identifier use so we can check for undefined names
            # Store (line, column) of the first occurrence
            if token.value not in self._used_names:
                self._used_names[token.value] = (token.line, token.column)
            return ast.Identifier(name=token.value, line=token.line)

        self.error(f"Unexpected token: {current.type} '{current.value}'",
                   "INVALID_EXPRESSION")

# Built-in names that are always defined in Python
_BUILTINS: set = {
    'print', 'len', 'range', 'int', 'float', 'str', 'bool', 'list', 'dict',
    'set', 'tuple', 'type', 'isinstance', 'issubclass', 'hasattr', 'getattr',
    'setattr', 'delattr', 'input', 'open', 'format', 'repr', 'abs', 'all',
    'any', 'bin', 'bytes', 'callable', 'chr', 'compile', 'complex', 'dir',
    'divmod', 'enumerate', 'eval', 'exec', 'filter', 'frozenset', 'globals',
    'hash', 'help', 'hex', 'id', 'iter', 'locals', 'map', 'max', 'min',
    'next', 'object', 'oct', 'ord', 'pow', 'property', 'reversed', 'round',
    'slice', 'sorted', 'staticmethod', 'sum', 'super', 'vars', 'zip',
    'True', 'False', 'None', 'NotImplemented', 'Ellipsis',
    'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
    'AttributeError', 'ImportError', 'OSError', 'RuntimeError',
    'StopIteration', 'GeneratorExit', 'SystemExit', 'KeyboardInterrupt',
    '__name__', '__file__', '__doc__', '__package__', '__spec__',
    '__builtins__', '__import__', '__loader__', '__build_class__',
}


def _check_undefined_names(parser: 'PythonParser') -> None:
    """
    Post-parse pass: report used names that were never defined in this file
    and are not Python built-ins.
    Only one NameError per name (the first use location).
    """
    for name, loc in parser._used_names.items():
        if name in parser._defined_names:
            continue
        if name in _BUILTINS:
            continue
        line, col = loc if isinstance(loc, tuple) else (loc, 0)
        err = ast.ErrorNode(
            error_type='UNDEFINED_NAME',
            message=f"NameError: name '{name}' is not defined",
            token=name,
            line=line,
            column=col,
        )
        parser.errors.append(err)
        parser.error_count += 1


def parse_python(tokens: List[Token]) -> tuple:
    """Parse Python tokens into AST.
    Returns (ast_tree, errors) and also populates _last_defined_names
    and _last_used_cols module-level caches for the diagnostics layer.
    """
    global _last_defined_names, _last_used_cols
    parser = PythonParser(tokens)
    ast_tree = parser.parse()
    # Post-parse: check for undefined names (basic NameError detection)
    _check_undefined_names(parser)
    # Sort errors by line number for clean output
    parser.errors.sort(key=lambda e: (e.line, e.column))
    # Expose parser scope info for the diagnostics layer
    _last_defined_names = set(parser._defined_names)
    _last_used_cols = {
        name: loc[1] if isinstance(loc, tuple) else 0
        for name, loc in parser._used_names.items()
    }
    return ast_tree, parser.errors

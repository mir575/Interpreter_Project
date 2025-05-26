import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer  # Import the Lexer class

class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return f"<ASTNode type={self.type}, value={self.value}, left={self.left}, right={self.right}>"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def current_token(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else ('EOF', None)

    def expect(self, token_type):
        token = self.current_token()
        if token[0] == token_type:
            self.current += 1
            return token
        raise SyntaxError(f"Expected {token_type}, found: {token}")

    def parse(self):
        statements = []
        while self.current < len(self.tokens):
            statements.append(self.parse_statement())
        return ASTNode(type='BLOCK', value=statements) if len(statements) > 1 else statements[0] if statements else None

    def parse_statement(self):
        if self.current < len(self.tokens):
            if self.tokens[self.current][0] == 'IF':
                return self.if_statement()
            elif self.tokens[self.current][0] == 'WHILE':
                return self.while_statement()
            elif self.tokens[self.current][0] == 'INPUT':
                return self.input_statement()
            elif self.tokens[self.current][0] == 'PRINT':
                self.current += 1
                value = self.or_expression()
                return ASTNode(type='PRINT', left=value)
            elif self.tokens[self.current][0] == 'IDENTIFIER':
                start_pos = self.current
                node = self.index_expression()
                if self.current < len(self.tokens) and self.current_token()[0] == 'ASSIGN':
                    self.current += 1
                    if self.current < len(self.tokens) and self.current_token()[0] == 'INPUT':
                        value = self.input_statement()
                    else:
                        value = self.or_expression()
                    return ASTNode(type='ASSIGN', left=node, right=value)
                elif node.type == 'METHOD_CALL':
                    return node
                else:
                    self.current = start_pos  # Rewind
                    if self.current + 1 < len(self.tokens) and self.tokens[self.current + 1][0] == 'ASSIGN':
                        return self.assignment()
                    else:
                        token = self.tokens[self.current]
                        self.current += 1
                        return ASTNode(type='IDENTIFIER', value=token[1])
            else:
                return self.or_expression()
        raise SyntaxError(f"Expected a statement or expression, found: {self.current_token()}")

    def parse_block(self):
        if self.current < len(self.tokens) and self.current_token()[0] == 'LBRACE':
            self.current += 1
            statements = []
            while self.current < len(self.tokens) and self.current_token()[0] != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.expect('RBRACE')
            return ASTNode(type='BLOCK', value=statements)
        else:
            return self.parse_statement()

    def assignment(self):
        token = self.tokens[self.current]
        if token[0] == 'IDENTIFIER':
            self.current += 1
            if self.current + 1 < len(self.tokens) and self.tokens[self.current][0] == 'LBRACKET':
                # Handle index assignment (e.g., list[0] = 5)
                self.current -= 1
                left = self.index_expression()
                self.expect('ASSIGN')
                value = self.or_expression()
                return ASTNode(type='ASSIGN', left=left, right=value)
            elif self.current < len(self.tokens) and self.tokens[self.current][0] == 'ASSIGN':
                self.current += 1
                if self.current < len(self.tokens) and self.current_token()[0] == 'INPUT':
                    value = self.input_statement()
                else:
                    value = self.or_expression()
                return ASTNode(type='ASSIGN', left=ASTNode(type='IDENTIFIER', value=token[1]), right=value)
            else:
                raise SyntaxError("Expected '=' or '[' after variable name")
        else:
            raise SyntaxError("Expected variable name")

    def if_statement(self):
        self.expect('IF')
        condition = self.or_expression()
        self.expect('THEN')
        then_branch = self.parse_block()
        else_branch = None
        if self.current < len(self.tokens) and self.current_token()[0] == 'ELSE':
            self.current += 1
            else_branch = self.parse_block()
            return ASTNode(type='IF', left=condition, right=ASTNode(type='BRANCH', left=then_branch, right=else_branch))
        return ASTNode(type='IF', left=condition, right=then_branch)

    def while_statement(self):
        self.expect('WHILE')
        condition = self.or_expression()
        self.expect('DO')
        body = self.parse_block()
        return ASTNode(type='WHILE', left=condition, right=body)

    def input_statement(self):
        self.expect('INPUT')
        self.expect('LPAREN')
        prompt = self.or_expression()
        self.expect('RPAREN')
        return ASTNode(type='INPUT', left=prompt)

    def or_expression(self):
        node = self.and_expression()
        while self.current < len(self.tokens) and self.current_token()[0] == 'OR':
            self.current += 1
            node = ASTNode(type='OR', left=node, right=self.and_expression())
        return node

    def and_expression(self):
        node = self.equality_expression()
        while self.current < len(self.tokens) and self.current_token()[0] == 'AND':
            self.current += 1
            node = ASTNode(type='AND', left=node, right=self.equality_expression())
        return node

    def equality_expression(self):
        node = self.comparison_expression()
        while self.current < len(self.tokens) and self.current_token()[0] in ('EQUAL', 'NOTEQUAL'):
            op = self.current_token()[0]
            self.current += 1
            node = ASTNode(type=op, left=node, right=self.comparison_expression())
        return node

    def comparison_expression(self):
        node = self.additive_expression()
        while self.current < len(self.tokens) and self.current_token()[0] in ('LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'):
            op = self.current_token()[0]
            self.current += 1
            node = ASTNode(type=op, left=node, right=self.comparison_expression())
        return node

    def additive_expression(self):
        node = self.multiplicative_expression()
        while self.current < len(self.tokens) and self.current_token()[0] in ('PLUS', 'MINUS'):
            op = self.current_token()[0]
            self.current += 1
            node = ASTNode(type=op, left=node, right=self.multiplicative_expression())
        return node

    def multiplicative_expression(self):
        node = self.unary_expression()
        while self.current < len(self.tokens) and self.current_token()[0] in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token()[0]
            self.current += 1
            node = ASTNode(type=op, left=node, right=self.unary_expression())
        return node

    def unary_expression(self):
        if self.current < len(self.tokens) and self.current_token()[0] in ('MINUS', 'NOT'):
            op = self.current_token()[0]
            self.current += 1
            right = self.unary_expression()
            return ASTNode(type='NEGATE' if op == 'MINUS' else 'NOT', left=right)
        return self.index_expression()

    def index_expression(self):
        node = self.primary_expression()
        while self.current < len(self.tokens) and self.current_token()[0] in ('LBRACKET', 'DOT'):
            if self.current_token()[0] == 'LBRACKET':
                self.current += 1
                index = self.or_expression()
                self.expect('RBRACKET')
                node = ASTNode(type='INDEX', left=node, right=index)
            elif self.current_token()[0] == 'DOT':
                self.current += 1
                method = self.expect('IDENTIFIER')
                self.expect('LPAREN')
                args = []
                if self.current < len(self.tokens) and self.current_token()[0] != 'RPAREN':
                    args.append(self.or_expression())
                    while self.current < len(self.tokens) and self.current_token()[0] == 'COMMA':
                        self.current += 1
                        args.append(self.or_expression())
                self.expect('RPAREN')
                node = ASTNode(type='METHOD_CALL', left=node, value=method[1], right=args)
        return node

    def primary_expression(self):
        token = self.current_token()
        if token[0] == 'NUMBER':
            self.current += 1
            return ASTNode(type='NUMBER', value=float(token[1]))
        elif token[0] == 'STRING':
            self.current += 1
            return ASTNode(type='STRING', value=token[1])
        elif token[0] == 'TRUE':
            self.current += 1
            return ASTNode(type='TRUE', value=True)
        elif token[0] == 'FALSE':
            self.current += 1
            return ASTNode(type='FALSE', value=False)
        elif token[0] == 'IDENTIFIER':
            self.current += 1
            return ASTNode(type='IDENTIFIER', value=token[1])
        elif token[0] == 'LPAREN':
            self.current += 1
            node = self.or_expression()
            self.expect('RPAREN')
            return node
        elif token[0] == 'LBRACKET':
            return self.list_expression()
        raise SyntaxError(f"Unexpected token: {token}")

    def list_expression(self):
        self.expect('LBRACKET')
        elements = []
        if self.current < len(self.tokens) and self.current_token()[0] != 'RBRACKET':
            elements.append(self.or_expression())
            while self.current < len(self.tokens) and self.current_token()[0] == 'COMMA':
                self.current += 1
                elements.append(self.or_expression())
        self.expect('RBRACKET')
        return ASTNode(type='LIST', value=elements)
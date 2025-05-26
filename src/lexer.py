import re

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0

    def tokenize(self):
        # Define keywords
        KEYWORDS = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'while': 'WHILE',
            'do': 'DO',
            'print': 'PRINT',
            'true': 'TRUE',
            'false': 'FALSE',
            'and': 'AND',
            'or': 'OR',
            'input': 'INPUT'
        }

        # Define token specification
        token_specification = [
            ('COMMENT', r'//[^\n]*'),                   # Single-line comment (// until newline)
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Variable names and keywords
            ('NUMBER', r'\d+(\.\d+)?'),                 # Integer or decimal number
            ('STRING', r'"[^"]*"|\'[^\']*\''),          # String literal
            ('GREATEREQUAL', r'>='),                    # Greater than or equal
            ('LESSEQUAL', r'<='),                       # Less than or equal
            ('NOTEQUAL', r'!='),                        # Not equal
            ('EQUAL', r'=='),                           # Equality
            ('GREATER', r'>'),                          # Greater than
            ('LESS', r'<'),                             # Less than
            ('ASSIGN', r'='),                           # Assignment operator
            ('PLUS', r'\+'),                            # Addition
            ('MINUS', r'-'),                            # Subtraction
            ('MULTIPLY', r'\*'),                        # Multiplication
            ('DIVIDE', r'/'),                           # Division
            ('LPAREN', r'\('),                          # Left parenthesis
            ('RPAREN', r'\)'),                          # Right parenthesis
            ('LBRACKET', r'\['),                        # Left bracket for lists
            ('RBRACKET', r'\]'),                        # Right bracket for lists
            ('COMMA', r','),                            # Comma for list elements
            ('DOT', r'\.'),                             # Dot for method calls
            ('NOT', r'!'),                              # Logical NOT
            ('WHITESPACE', r'\s+'),                     # Whitespace (ignored)
            ('LBRACE', r'\{'),                          # Left brace
            ('RBRACE', r'\}'),                          # Right brace
        ]

        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        for match in re.finditer(token_regex, self.source):
            kind = match.lastgroup
            value = match.group()
            if kind == 'COMMENT':
                continue  # Skip comments
            elif kind == 'IDENTIFIER' and value in KEYWORDS:
                # Convert identifiers that match keywords into their respective token types
                kind = KEYWORDS[value]
            elif kind == 'STRING':
                value = value[1:-1]  # Remove surrounding quotes
            if kind != 'WHITESPACE':  # Ignore whitespace
                self.tokens.append((kind, value))
        return self.tokens
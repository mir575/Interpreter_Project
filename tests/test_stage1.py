import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def print_ast(node, level=0):
    indent = "  " * level
    if node is not None:
        print(f"{indent}{node.type}: {node.value if node.value is not None else ''}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)

def test_expression(expression):
    print(f"Testing: {expression}")
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:")
    print_ast(ast)  # Print the AST for debugging
    interpreter = Interpreter()
    result = interpreter.evaluate(ast)
    print(f"Result: {result}\n")

if __name__ == "__main__":
    # Test cases
    test_expression("1 + 2 * 3")          # Expected: 7
    test_expression("(1 + 2) * 3")        # Expected: 9
    test_expression("10 / 2 + 3 * 4")     # Expected: 14
    test_expression("-(3 + 4) * 2")       # Expected: -14
    test_expression("-5 + 3")             # Expected: -2
    test_expression("1 + -2 * (3 + 4)")   # Expected: -13
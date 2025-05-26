import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def test_expression(expression):
    print(f"Testing: {expression}")
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f"AST: {ast}")  # Debug: Print AST
    interpreter = Interpreter()
    result = interpreter.evaluate(ast)
    print(f"Result: {result}\n")

if __name__ == "__main__":
    # Test cases for Stage 2
    test_expression("1 == 1")             # Expected: True
    test_expression("1 != 2")             # Expected: True
    test_expression("3 < 5")              # Expected: True
    test_expression("5 >= 5")             # Expected: True
    test_expression("true and false")     # Expected: False
    test_expression("true or false")      # Expected: True
    test_expression("!(1 == 2)")          # Expected: True
    test_expression("1 + 2 > 3 and 4 < 5") # Expected: False
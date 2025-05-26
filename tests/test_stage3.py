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
    interpreter = Interpreter()
    result = interpreter.evaluate(ast)
    print(f"Result: {result}\n")

if __name__ == "__main__":
    # Test cases for Stage 3
    test_expression('"hello" + " world"')  # Expected: "hello world"
    test_expression('"foo" == "foo"')     # Expected: True
    test_expression('"foo" != "bar"')     # Expected: True
    test_expression('"10" + "20"')        # Expected: "1020"
    test_expression('"hello" + 10')        # Expected: "error"
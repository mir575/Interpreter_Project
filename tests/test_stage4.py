import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def test_expression(expression, interpreter):
    print(f"Testing: {expression}")
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    result = interpreter.evaluate(ast)
    print(f"Result: {result}\n")

if __name__ == "__main__":
    # Create a single instance of the Interpreter
    interpreter = Interpreter()

    # Test cases for Stage 4
    test_expression("quickMaths = 10", interpreter)              # Expected: 10
    test_expression("quickMaths = quickMaths + 2", interpreter)  # Expected: 12
    test_expression("print quickMaths", interpreter)             # Expected: 12

    test_expression("floatTest = 1.0", interpreter)              # Expected: 1.0
    test_expression("floatTest = floatTest + 5", interpreter)    # Expected: 6.0
    test_expression("print floatTest", interpreter)              # Expected: 6.0

    test_expression('stringCatTest = "10 corgis"', interpreter)  # Expected: "10 corgis"
    test_expression('stringCatTest = stringCatTest + 5 + " more corgis"', interpreter)  # Expected: TypeError
    test_expression("print stringCatTest", interpreter)          # Expected: "10 corgis"

    test_expression("errorTest = 5", interpreter)                # Expected: 5
    try:
        test_expression('errorTest = errorTest + "insert string here"', interpreter)  # Expected: TypeError
    except TypeError as e:
        print(f"Caught expected error: {e}")
import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def test_expression(expression, expected=None):
    print(f"Testing: {expression}")
    try:
        lexer = Lexer(expression)
        tokens = lexer.tokenize()
        print(f"Tokens: {tokens}")
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST: {ast}")
        interpreter = Interpreter()
        result = interpreter.evaluate(ast)
        print(f"Result: {result}")
        if expected is not None:
            assert result == expected, f"Expected {expected}, got {result}"
            print(f"Passed: Result matches expected value {expected}")
    except Exception as e:
        print(f"Error: {str(e)}")
        if expected == "error":
            print("Passed: Expected error occurred")
        else:
            print("Failed: Unexpected error")
    print()

if __name__ == "__main__":
    # Test cases for List Data Structure
    # 1. List literal and index access
    test_expression('[1, 2, 3][0]', expected=1)
    test_expression('[1, "hello", true][1]', expected="hello")

    # 2. List creation and appending
    test_expression('l = [1, 2]; l.append(3); l', expected=[1, 2, 3])
    test_expression('l = []; l.append("test"); l', expected=["test"])

    # 3. List index assignment
    test_expression('l = [1, 2, 3]; l[0] = 5; l', expected=[5, 2, 3])
    test_expression('l = ["a", "b"]; l[1] = "c"; l', expected=["a", "c"])

    # 4. List element removal
    test_expression('l = [1, 2, 3]; l.remove(1); l', expected=[1, 3])
    test_expression('l = ["a", "b", "c"]; l.remove(0); l', expected=["b", "c"])

    # 5. Error cases
    test_expression('l = [1, 2]; l[3]', expected="Error: Index out of range")
    test_expression('l = [1, 2]; l.remove(5)', expected="Error: Index out of range")
    test_expression('x = "not"; x.append(1)', expected="Error: Method call on non-list")
    test_expression('x = [1, 2]; x.invalid(42)', expected="Error: Unknown list method")
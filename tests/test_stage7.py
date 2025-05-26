import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def run_test(code, expected, description=""):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        result = interpreter.evaluate(ast)
        print(f"\nTesting: {description or code}")
        print(f"Tokens: {tokens}")
        print(f"AST: {ast}")
        print(f"Result: {result}")
        assert result == expected, f"Expected {expected}, got {result}"
        print("Passed")
    except Exception as e:
        print(f"\nTesting: {description or code}")
        print(f"Error: {str(e)}")
        print(f"Failed: Unexpected error: {str(e)}")
        raise

def run_error_test(code, expected_error, description=""):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        print(f"\nTesting: {description or code}")
        print(f"Failed: Expected error containing '{expected_error}', got none")
        assert False, "Expected error, got none"
    except Exception as e:
        print(f"\nTesting: {description or code}")
        print(f"Error: {str(e)}")
        assert expected_error in str(e), f"Expected error containing '{expected_error}', got '{str(e)}'"
        print("Passed")

# String method tests
run_test('s = "hello"; s.upper()', "HELLO", "String upper method")
run_test('s = "HELLO"; s.lower()', "hello", "String lower method")
run_test('s = "hi"; s.len()', 2.0, "String len method")
run_test('s = ""; s.len()', 0.0, "Empty string len method")
run_test('s = "hi"; print(s.upper()); s', "hi", "Non-mutating upper method (prints HI)")

# Comment tests
run_test('// comment\n x = 1; x', 1.0, "Comment before statement")
run_test('x = 1; // comment\n x', 1.0, "Comment after statement")
run_test('x = "test"; x // comment', "test", "Comment after expression")
run_test('// comment\n s = "hi"; s.upper()', "HI", "Comment before string method")

# Error tests
run_error_test('s = "hello"; s.invalid()', "String has no method 'invalid'", "Invalid string method")
run_error_test('x = 42; x.upper()', "'float' object has no attribute 'upper'", "Method call on number")


if __name__ == "__main__":
    print("Running Stage 7 tests...")
    print("All tests completed.")
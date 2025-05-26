import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def test_expression(expression, interpreter):
    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)  # Debug: Print the tokens
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)  # Debug: Print the AST
    result = interpreter.evaluate(ast)
    return result  # Return the result to avoid re-evaluation

if __name__ == "__main__":
    interpreter = Interpreter()

    # Test if-then-else
    test_expression("if (1 == 1) then print 'True' else print 'False'", interpreter)

    # Test nested if-then-else
    test_expression("""
        if (1 == 1) then
            if (2 == 2) then print 'Nested True' else print 'Nested False'
        else
            print 'Outer False'
    """, interpreter)

    # Test while loop
    test_expression("""
        x = 0
        while (x < 3) do {
            print x
            x = x + 1
        }
    """, interpreter)

    # Test nested while loops
    test_expression("""
        x = 0
        while (x < 2) do {
            y = 0
            while (y < 2) do {
                print x + y
                y = y + 1
            }
            x = x + 1
        }
    """, interpreter)

    # Test input and print
    test_expression("""
        name = input("Enter your name: ")
        print name
    """, interpreter)

    # Test shopping list example
    test_expression("""
        is_running = true
        shopping_list = ""
        while (is_running == true) do {
            item = input("add an item to the shopping list: ")
            if (item == "") then {
                is_running = false
            } else {
                if (shopping_list == "") then {
                    shopping_list = item
                } else {
                    shopping_list = shopping_list + ", " + item
                }
            }
        }
        print shopping_list
    """, interpreter)
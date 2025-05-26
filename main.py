import sys
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    file_path = sys.argv[1]
    with open(file_path, 'r') as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    result = interpreter.evaluate(ast)
    print(result)

if __name__ == "__main__":
    main()
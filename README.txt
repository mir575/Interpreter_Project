# Interpreter Project - Language Design Assignment

This project is a simple interpreter implemented in Python that parses and executes a custom programming language. The interpreter supports various features such as arithmetic operations, logical expressions, control flow, input/output, list data structures, and string methods.

---

## Features

### 1. Arithmetic Operations
- Supports addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`).
- Handles operator precedence and parentheses for grouping expressions.
- Example:
1 + 2 * 3 # Result: 7 (1 + 2) * 3 # Result: 9


### 2. Logical Expressions
- Supports comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`).
- Logical operators (`and`, `or`, `not`) are supported for boolean expressions.
- Example: 1 == 1 # Result: true 
true and false # Result: false


### 3. Strings
- Supports string concatenation using the `+` operator.
- Allows comparison of strings using `==` and `!=`.
- Includes string methods such as `upper()`, `lower()`, and `len()`.
- Example: "hello".upper() # Result: "HELLO" 
"foo" == "foo" # Result: true


### 4. Control Flow
- **If-Then-Else Statements**:
- Supports conditional branching with `if`, `then`, and `else`.
- Example:
  ```
  if (1 == 1) then print "True" else print "False"
  ```
- **While Loops**:
- Supports looping with `while` and `do`.
- Example:
  ```
  x = 0
  while (x < 3) do {
      print x
      x = x + 1
  }
  ```

### 5. Input/Output
- Supports user input using the `input` function.
- Allows printing values using the `print` statement.
- Example: name = input("Enter your name: ") 
            print name


### 6. Variables
- Variables can store numbers, strings, booleans, and lists.
- Variables can be reassigned and used in expressions.
- Example: x = 10 x = x + 5 print x # Result: 15


### 7. List Data Structures
- Supports list literals, indexing, and methods such as `append` and `remove`.
- Example: x = 10 x = x + 5 print x # Result: 15


### 8. Comments
- Supports single-line comments using `//`.
- Example: // This is a comment x = 1 + 2 // Another comment



---

## Project Structure

### 1. **Source Code**
- **`src/lexer.py`**:
- Tokenizes the input source code into a list of tokens.
- Supports keywords, operators, numbers, strings, and list syntax.
- **`src/parser.py`**:
- Parses the tokens into an Abstract Syntax Tree (AST).
- Handles expressions, statements, and control flow constructs.
- **`src/interpreter.py`**:
- Evaluates the AST and executes the program.
- Implements the logic for arithmetic, logical operations, control flow, and list handling.
- **`src/tokens.py`**:
- Defines the token types used by the lexer.

### 2. **Tests**
- **`tests/test_stage1.py`**:
- Tests basic arithmetic operations and operator precedence.
- **`tests/test_stage2.py`**:
- Tests logical expressions and boolean operations.
- **`tests/test_stage3.py`**:
- Tests string operations, comparisons, and methods.
- **`tests/test_stage4.py`**:
- Tests variable assignments and reassignments.
- **`tests/test_stage5.py`**:
- Tests control flow constructs such as `if-then-else` and `while` loops.
- Includes a shopping list example that demonstrates input handling and loops.
- **`tests/test_stage6.py`**:
- Tests list data structures, including indexing, appending, removing elements, and error handling.
- **`tests/test_stage7.py`**:
- Tests string methods, comments, and error handling for invalid operations.

---

## How to Run

### 1. Running the Interpreter
To run the interpreter on a source file:


### 2. Running Tests
To run the test cases for each stage:
python test_stage1.py 
python test_stage2.py 
python test_stage3.py 
python test_stage4.py 
python test_stage5.py 
python test_stage6.py 
python test_stage7.py



---

## Future Improvements
- Add support for functions and recursion.
- Extend the language with more data types (e.g., dictionaries).
- Improve error messages for better debugging.

---

## Credits
This project was developed as part of a language design assignment. It demonstrates the implementation of a custom interpreter with a focus on parsing, AST construction, and execution.

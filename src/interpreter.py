import sys
import os

# Add the project directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import ASTNode

class Interpreter:
    def __init__(self):
        self.variables = {}  # Symbol table for global variables

    def evaluate(self, node):
        if node.type == 'IF':  # Handle if statements
            condition = self.evaluate(node.left)  # Evaluate the condition
            print(f"IF condition result: {condition}")  # Debug: Print condition result
            if condition:
                return self.evaluate(node.right.left)  # Evaluate the 'then' branch
            elif node.right and node.right.right:  # Evaluate the 'else' branch if it exists
                return self.evaluate(node.right.right)
            return None  # Explicit return for IF with no else branch
        elif node.type == 'WHILE':  # Handle while loops
            print("Entering WHILE loop.")  # Debug: Print loop entry
            while self.evaluate(node.left):  # Evaluate the condition
                print(f"WHILE condition is True. Variables: {self.variables}")  # Debug
                self.evaluate(node.right)  # Evaluate the body of the loop
            print("Exiting WHILE loop.")  # Debug
            return None  # Explicitly return None to avoid returning the node
        elif node.type == 'INPUT':
            prompt = self.evaluate(node.left)
            print(f"Prompting user with: {prompt}")
            user_input = input(prompt)
            print(f"User entered: {user_input}")
            return user_input
        elif node.type == 'LIST':
            return [self.evaluate(elem) for elem in node.value]
        elif node.type == 'INDEX':
            list_val = self.evaluate(node.left)
            index = self.evaluate(node.right)
            print(f"Indexing: {list_val}[{index}]")  # Debug
            if not isinstance(list_val, list):
                raise TypeError("Index operation on non-list")
            if not isinstance(index, (int, float)):
                raise TypeError("Index must be a number")
            index = int(index)
            if index < 0 or index >= len(list_val):
                raise IndexError(f"Index {index} out of range")
            return list_val[index]
        elif node.type == 'METHOD_CALL':
            obj = self.evaluate(node.left)
            method = node.value
            args = [self.evaluate(arg) for arg in node.right]
            print(f"Method call: {obj}.{method}({args})")  # Debug
            if isinstance(obj, list):
                if method == 'append' and len(args) == 1:
                    obj.append(args[0])
                    return None
                elif method == 'remove' and len(args) == 1:
                    try:
                        obj.remove(args[0])
                        return None
                    except ValueError:
                        raise ValueError(f"Value {args[0]} not in list")
                else:
                    raise AttributeError(f"List has no method '{method}'")
            elif isinstance(obj, str):
                if method == 'upper' and len(args) == 0:
                    return obj.upper()
                elif method == 'lower' and len(args) == 0:
                    return obj.lower()
                elif method == 'len' and len(args) == 0:
                    return float(len(obj))  # Return as float to match NUMBER type
                else:
                    raise AttributeError(f"String has no method '{method}'")
            else:
                raise AttributeError(f"{type(obj).__name__} has no method '{method}'")

        # Debug: Print node type and value
        print(f"Evaluating: {node.type}, {node.value}")

        if node.type == 'NUMBER':  # Handle numbers
            return node.value
        elif node.type == 'STRING':  # Handle strings
            return node.value
        elif node.type == 'TRUE':  # Handle Boolean true
            return True
        elif node.type == 'FALSE':  # Handle Boolean false
            return False
        elif node.type == 'IDENTIFIER':  # Handle variable usage
            var_name = node.value
            if var_name in self.variables:
                value = self.variables[var_name]
                print(f"IDENTIFIER: {var_name}={value}")  # Debug
                return value
            else:
                raise NameError(f"Variable '{var_name}' is not defined")
        elif node.type == 'BLOCK':
            result = None
            for stmt in node.value:
                result = self.evaluate(stmt)
            return result
        elif node.type == 'ASSIGN':  # Handle variable assignment
            if node.left.type == 'INDEX':
                list_val = self.evaluate(node.left.left)
                index = self.evaluate(node.left.right)
                if not isinstance(list_val, list):
                    raise TypeError("Index operation on non-list")
                if not isinstance(index, (int, float)):
                    raise TypeError("Index must be a number")
                index = int(index)
                if index < 0 or index >= len(list_val):
                    raise IndexError(f"Index {index} out of range")
                value = self.evaluate(node.right)
                list_val[index] = value
                return value
            else:
                var_name = node.left.value
                value = self.evaluate(node.right)
                self.variables[var_name] = value
                print(f"ASSIGN: {var_name}={value}")  # Debug
                return value
        elif node.type == 'PRINT':  # Handle print statements
            value = self.evaluate(node.left)
            print(value)
            return value
        elif node.type == 'PLUS':  # Handle addition or concatenation
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            print(f"PLUS Operation: left={left}, right={right}")  # Debug
            if isinstance(left, str) and isinstance(right, str):
                # Concatenate strings
                return left + right
            elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                # Add numbers
                return left + right
            else:
                raise TypeError(f"Unsupported operand types for +: '{type(left).__name__}' and '{type(right).__name__}'")
        elif node.type == 'MINUS':  # Handle subtraction
            return self.evaluate(node.left) - self.evaluate(node.right)
        elif node.type == 'MULTIPLY':  # Handle multiplication
            return self.evaluate(node.left) * self.evaluate(node.right)
        elif node.type == 'DIVIDE':  # Handle division
            return self.evaluate(node.left) / self.evaluate(node.right)
        elif node.type == 'NEGATE':  # Handle negation
            return -self.evaluate(node.left)
        elif node.type == 'AND':  # Handle logical AND
            return self.evaluate(node.left) and self.evaluate(node.right)
        elif node.type == 'OR':  # Handle logical OR
            return self.evaluate(node.left) or self.evaluate(node.right)
        elif node.type == 'NOT':  # Handle logical NOT
            return not self.evaluate(node.left)
        elif node.type == 'EQUAL':  # Handle equality
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            print(f"EQUAL: {left} == {right}")  # Debug
            return left == right
        elif node.type == 'NOTEQUAL':  # Handle inequality
            return self.evaluate(node.left) != self.evaluate(node.right)
        elif node.type == 'LESS':  # Handle less than
            return self.evaluate(node.left) < self.evaluate(node.right)
        elif node.type == 'LESSEQUAL':  # Handle less than or equal
            return self.evaluate(node.left) <= self.evaluate(node.right)
        elif node.type == 'GREATER':  # Handle greater than
            return self.evaluate(node.left) > self.evaluate(node.right)
        elif node.type == 'GREATEREQUAL':  # Handle greater than or equal
            return self.evaluate(node.left) >= self.evaluate(node.right)
        else:
            raise ValueError(f"Unknown node type: {node.type}")
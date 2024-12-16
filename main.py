from typing import List, Dict, Any, Union
import re
from ollama import chat
from ollama import ChatResponse

def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The sum of the two numbers
    """
    return a + b

def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The difference of the two numbers
    """
    return a - b

def multiply_two_numbers(a: int, b: int) -> int:
    """
    Multiply two numbers
    Args:
        a (int): The first number
        b (int): The second number
    Returns:
        int: The product of the two numbers
    """
    return a * b

def divide_two_numbers(a: int, b: int) -> float:
    """
    Divide two numbers
    Args:
        a (int): The numerator
        b (int): The denominator
    Returns:
        float: The quotient of the two numbers
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def floor_divide_two_numbers(a: int, b: int) -> int:
    """
    Floor divide two numbers
    Args:
        a (int): The numerator
        b (int): The denominator
    Returns:
        int: The floor division result of the two numbers
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a // b

def power_two_numbers(a: int, b: int) -> int:
    """
    Raise first number to the power of second number
    Args:
        a (int): The base number
        b (int): The exponent
    Returns:
        int: The result of a raised to the power of b
    """
    return a ** b

def modulo_two_numbers(a: int, b: int) -> int:
    """
    Get remainder of division of two numbers
    Args:
        a (int): The dividend
        b (int): The divisor
    Returns:
        int: The remainder of a divided by b
    """
    if b == 0:
        raise ValueError("Cannot perform modulo with zero")
    return a % b

# Define tool specifications
def create_math_tool(name: str, description: str) -> Dict[str, Any]:
    """
    Create a tool specification for mathematical operations
    """
    return {
        'type': 'function',
        'function': {
            'name': name,
            'description': description,
            'parameters': {
                'type': 'object',
                'required': ['a', 'b'],
                'properties': {
                    'a': {'type': 'integer', 'description': 'The first number'},
                    'b': {'type': 'integer', 'description': 'The second number'},
                },
            },
        },
    }

# Create tool specifications for all operations
math_tools = {
    'add_two_numbers': create_math_tool('add_two_numbers', 'Add two numbers'),
    'subtract_two_numbers': create_math_tool('subtract_two_numbers', 'Subtract two numbers'),
    'multiply_two_numbers': create_math_tool('multiply_two_numbers', 'Multiply two numbers'),
    'divide_two_numbers': create_math_tool('divide_two_numbers', 'Divide two numbers'),
    'floor_divide_two_numbers': create_math_tool('floor_divide_two_numbers', 'Floor divide two numbers'),
    'power_two_numbers': create_math_tool('power_two_numbers', 'Raise first number to the power of second number'),
    'modulo_two_numbers': create_math_tool('modulo_two_numbers', 'Get remainder of division of two numbers'),
}

def evaluate_expression(expression: str) -> Dict[str, Any]:
    """
    Evaluates a complex mathematical expression following PEMDAS rules.
    Now includes step tracking.
    """
    steps = []

    def add_step(expr: str, result: float) -> None:
        steps.append({
            'expression': expr,
            'result': result
        })

    def tokenize(expr: str) -> List[str]:
        expr = re.sub(r'([\+\-\*/\(\)])', r' \1 ', expr)
        return [token for token in expr.split() if token]
    
    def parse_number(token: str) -> float:
        try:
            return float(token)
        except ValueError:
            raise ValueError(f"Invalid number: {token}")

    def apply_operation(op: str, a: float, b: float) -> float:
        result = None
        if op == '+': result = a + b
        if op == '-': result = a - b
        if op == '*': result = a * b
        if op == '/':
            if b == 0:
                raise ValueError("Division by zero")
            result = a / b
        add_step(f"{a} {op} {b}", result)
        return result

    def precedence(op: str) -> int:
        if op in {'+', '-'}: return 1
        if op in {'*', '/'}: return 2
        return 0

    def evaluate_inner(expr: str) -> float:
        tokens = tokenize(expr)
        values = []
        operators = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token in {'+', '-', '*', '/'}:
                while (operators and operators[-1] != '(' and 
                       precedence(operators[-1]) >= precedence(token)):
                    op = operators.pop()
                    b = values.pop()
                    a = values.pop()
                    values.append(apply_operation(op, a, b))
                operators.append(token)
            
            elif token == '(':
                operators.append(token)
            
            elif token == ')':
                while operators and operators[-1] != '(':
                    op = operators.pop()
                    b = values.pop()
                    a = values.pop()
                    values.append(apply_operation(op, a, b))
                if operators and operators[-1] == '(':
                    operators.pop()
                else:
                    raise ValueError("Mismatched parentheses")
            
            else:
                values.append(parse_number(token))
            
            i += 1

        while operators:
            op = operators.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            b = values.pop()
            a = values.pop()
            values.append(apply_operation(op, a, b))

        if len(values) != 1:
            raise ValueError("Invalid expression")
        return values[0]

    try:
        # Handle parentheses evaluation
        while '(' in expression:
            # Find the innermost parentheses
            start = 0
            while start < len(expression):
                if expression[start] == '(':
                    # Find matching closing parenthesis
                    count = 1
                    end = start + 1
                    while count > 0 and end < len(expression):
                        if expression[end] == '(': count += 1
                        if expression[end] == ')': count -= 1
                        end += 1
                    
                    if count > 0:
                        raise ValueError("Mismatched parentheses")
                    
                    # Evaluate the content within these parentheses
                    inner_expr = expression[start+1:end-1]
                    result = evaluate_inner(inner_expr)
                    
                    # Add this step to our tracking
                    add_step(f"({inner_expr})", result)
                    
                    # Replace the parentheses expression with its result
                    expression = expression[:start] + str(result) + expression[end:]
                    break
                start += 1
        
        # Evaluate the final expression without parentheses
        final_result = evaluate_inner(expression)
        
        return {
            "result": final_result,
            "steps": steps,
            "error": None
        }
    except Exception as e:
        return {
            "result": None,
            "steps": steps,
            "error": str(e)
        }

def evaluate_math_expression(expression: str) -> Dict[str, Any]:
    """
    Tool function to evaluate complex mathematical expressions.
    Args:
        expression (str): Mathematical expression as string
    Returns:
        Dict[str, Any]: Result and details of the evaluation
    """
    try:
        result = evaluate_expression(expression)
        return {
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "result": None,
            "error": str(e)
        }

# Define the tool specification for complex expressions
evaluate_expression_tool = {
    'type': 'function',
    'function': {
        'name': 'evaluate_math_expression',
        'description': 'Evaluate a complex mathematical expression following PEMDAS rules',
        'parameters': {
            'type': 'object',
            'required': ['expression'],
            'properties': {
                'expression': {
                    'type': 'string',
                    'description': 'The mathematical expression to evaluate (e.g., "3*4+5*6")'
                }
            }
        }
    }
}

# Update the available functions dictionary
available_functions = {
    'add_two_numbers': add_two_numbers,
    'subtract_two_numbers': subtract_two_numbers,
    'multiply_two_numbers': multiply_two_numbers,
    'divide_two_numbers': divide_two_numbers,
    'floor_divide_two_numbers': floor_divide_two_numbers,
    'power_two_numbers': power_two_numbers,
    'modulo_two_numbers': modulo_two_numbers,
    'evaluate_math_expression': evaluate_math_expression
}

def process_math_operation(messages: list, model: str = 'llama3.1') -> None:
    """
    Process mathematical operations using the Ollama chat API
    Args:
        messages (list): List of chat messages
        model (str): Name of the model to use
    """
    print('Prompt:', messages[0]['content'])
    print('\nCalculating...')
    
    # Add the evaluate_expression_tool to the list of tools
    all_tools = list(math_tools.values()) + [evaluate_expression_tool]
    
    response: ChatResponse = chat(
        model,
        messages=messages,
        tools=all_tools,
    )
    
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := available_functions.get(tool.function.name):
                try:
                    output = function_to_call(**tool.function.arguments)
                    
                    # Handle the nested structure
                    if isinstance(output, dict) and 'result' in output:
                        result_data = output['result']  # Get the inner result dictionary
                        if isinstance(result_data, dict) and 'steps' in result_data:
                            print("\nStep-by-Step Evaluation:")
                            print("-----------------------")
                            for i, step in enumerate(result_data['steps'], 1):
                                print(f"Step {i:2d}: {step['expression']} = {step['result']}")
                            print("-----------------------")
                            print(f"Final Result: {result_data['result']:,.0f}")
                        
                except ValueError as e:
                    print(f'Error: {str(e)}')
                    output = str(e)
            else:
                print('Function', tool.function.name, 'not found')
                continue

            messages.append(response.message)
            messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})
    else:
        print('No calculations performed')

if __name__ == "__main__":
    calculations_to_be_done = [{'role': 'user', 'content': 'What is (3*4+5*6) * (120/5 - 3) * ((6-3)*(5-2)*(8*2))?'}]
    process_math_operation(calculations_to_be_done)
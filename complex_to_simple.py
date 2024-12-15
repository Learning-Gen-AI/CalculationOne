import sympy as sp

def break_down_formula(expression_str):
    """
    Converts a mathematical expression into basic arithmetic operations
    and shows the step-by-step calculation process.
    
    Args:
        expression_str (str): Mathematical expression as a string
    """
    # Convert string to SymPy expression
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    expr = sp.sympify(expression_str)
    
    # Get the expression tree
    def print_operation_tree(expr, level=0):
        indent = "  " * level
        
        if expr.is_Add or expr.is_Mul or expr.is_Pow:
            print(f"{indent}Operation: {expr.__class__.__name__}")
            for arg in expr.args:
                print_operation_tree(arg, level + 1)
        else:
            print(f"{indent}Value: {expr}")

    # Example usage
    print("Breaking down the expression:", expression_str)
    print("\nOperation tree:")
    print_operation_tree(expr)
    
    # Convert to basic operations
    print("\nBasic arithmetic steps:")
    
    def generate_basic_steps(expr):
        if expr.is_number:
            return str(expr)
            
        if expr.is_Pow and expr.args[1].is_number:
            base = expr.args[0]
            exp = expr.args[1]
            if exp.is_integer and exp > 0:
                return f"({' * '.join([generate_basic_steps(base)] * int(exp))})"
            
        if expr.is_Add:
            return f"({' + '.join(generate_basic_steps(arg) for arg in expr.args)})"
        if expr.is_Mul:
            return f"({' * '.join(generate_basic_steps(arg) for arg in expr.args)})"
            
        return str(expr)
    
    print(generate_basic_steps(expr))

# Example usage
expressions = [
    "x**2 + 2*x + 1",           # Quadratic expression
    "x**3 - y**2",              # Expression with multiple variables
    "(x + 1)**2",               # Binomial expansion
    "(1+5/100)^(-12)"
]

for expr in expressions:
    print("\n" + "="*50)
    break_down_formula(expr)
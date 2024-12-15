from decimal import Decimal, getcontext
from typing import Union, Tuple
import re

class PreciseCalculator:
    """
    A calculator class that ensures exact precision for basic arithmetic operations.
    Uses Decimal for all calculations to avoid floating point errors.
    """
    
    def __init__(self, precision: int = 28):
        """
        Initialize calculator with specified precision.
        
        Args:
            precision: Number of significant digits to maintain (default: 28)
        """
        getcontext().prec = precision
    
    def parse_expression(self, expression: str) -> Tuple[Union[Decimal, str], bool]:
        """
        Safely parses and evaluates a basic arithmetic expression.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            Tuple of (result as Decimal or error message as str, success boolean)
        """
        # Clean and validate the expression
        expression = expression.strip()
        if not expression:
            return "Empty expression", False
            
        # Only allow basic arithmetic operations and numbers
        allowed_chars = set("0123456789+-*/.()")
        if not all(c in allowed_chars for c in expression):
            return "Invalid characters in expression", False
            
        try:
            # Convert all numbers to Decimal for precise calculation
            parsed_expr = re.sub(r'\d*\.?\d+', lambda m: f'Decimal("{m.group()}")', expression)
            result = eval(parsed_expr, {"Decimal": Decimal}, {})
            return result, True
        except Exception as e:
            return f"Error evaluating expression: {str(e)}", False
    
    def calculate(self, expression: str) -> Union[Decimal, str]:
        """
        Main interface for calculating expressions.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            Decimal result or error message string
        """
        result, success = self.parse_expression(expression)
        return result if success else f"Error: {result}"

    def add(self, a: Union[int, float, str], b: Union[int, float, str]) -> Decimal:
        """Precise addition of two numbers"""
        return Decimal(str(a)) + Decimal(str(b))
    
    def subtract(self, a: Union[int, float, str], b: Union[int, float, str]) -> Decimal:
        """Precise subtraction of two numbers"""
        return Decimal(str(a)) - Decimal(str(b))
    
    def multiply(self, a: Union[int, float, str], b: Union[int, float, str]) -> Decimal:
        """Precise multiplication of two numbers"""
        return Decimal(str(a)) * Decimal(str(b))
    
    def divide(self, a: Union[int, float, str], b: Union[int, float, str]) -> Decimal:
        """Precise division of two numbers"""
        if Decimal(str(b)) == 0:
            raise ValueError("Division by zero")
        return Decimal(str(a)) / Decimal(str(b))
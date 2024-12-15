import requests
import json
import re
from typing import Dict, Any, List, Tuple
from decimal import Decimal
from precise_calculator import PreciseCalculator

class LLMMathProcessor:
    """
    A workflow that processes mathematical expressions in LLM responses
    using precise calculation methods.
    """
    
    def __init__(self, model_name: str = "llama3.1", base_url: str = "http://localhost:11434"):
        """
        Initialize the processor with specific model and connection details.
        
        Args:
            model_name: Name of the Ollama model to use
            base_url: Base URL for Ollama API
        """
        self.model_name = model_name
        self.base_url = base_url
        self.calculator = PreciseCalculator()
        
    def extract_math_expressions(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Find mathematical expressions in text and return them with their positions.
        
        Args:
            text: Input text to process
            
        Returns:
            List of tuples containing (expression, start_pos, end_pos)
        """
        # Pattern matches basic arithmetic expressions
        pattern = r'\b\d+\.?\d*\s*[\+\-\*\/]\s*\d+\.?\d*(?:\s*[\+\-\*\/]\s*\d+\.?\d*)*\b'
        matches = []
        
        for match in re.finditer(pattern, text):
            matches.append((match.group(), match.start(), match.end()))
            
        return matches

    def process_math(self, text: str) -> str:
        """
        Replace all mathematical expressions in text with precise calculations.
        
        Args:
            text: Input text containing mathematical expressions
            
        Returns:
            Processed text with precise calculations
        """
        expressions = self.extract_math_expressions(text)
        
        # Process expressions from end to start to maintain string indices
        for expr, start, end in sorted(expressions, key=lambda x: x[1], reverse=True):
            try:
                result = self.calculator.calculate(expr)
                if isinstance(result, Decimal):
                    # Replace the expression with the precise result
                    text = text[:start] + str(result) + text[end:]
            except Exception as e:
                print(f"Error processing expression '{expr}': {str(e)}")
                
        return text

    def query_ollama(self, prompt: str) -> Dict[str, Any]:
        """
        Send a query to Ollama API and get the response.
        
        Args:
            prompt: The input prompt for the model
            
        Returns:
            Parsed JSON response from Ollama
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")

    def process_query(self, prompt: str) -> str:
        """
        Main workflow: Query LLM and process any math in the response.
        
        Args:
            prompt: User's input prompt
            
        Returns:
            Processed response with precise calculations
        """
        try:
            # Get response from LLM
            response = self.query_ollama(prompt)
            
            # Extract the response text
            if 'response' in response:
                llm_response = response['response']
                
                # Process any mathematical expressions
                processed_response = self.process_math(llm_response)
                
                return processed_response
            else:
                return "Error: No response from LLM"
                
        except Exception as e:
            return f"Error processing query: {str(e)}"

def main():
    """
    Example usage of the LLMMathProcessor
    """
    # Initialize the processor
    processor = LLMMathProcessor(model_name="llama3.1")
    
    # Example prompts that might involve calculations
    example_prompts = [
        "What is 23.5 + 45.7?",
        "If I have 127.35 dollars and spend 45.80 dollars, how much do I have left?",
        "Calculate 15.7 * 3.14",
        "If I have seven apples and sell 3 of them and eat one, how many apples are left?",
        "What is 6 + 4 + 3 - 2 * 12 / 5",
        "What is (1+5/100)^(-12)"
    ]
    
    print("Testing LLM Math Processing Workflow:")
    print("-" * 50)
    
    for prompt in example_prompts:
        print(f"\nPrompt: {prompt}")
        result = processor.process_query(prompt)
        print(f"Processed Response: {result}")
        print("-" * 50)

if __name__ == "__main__":
    main()
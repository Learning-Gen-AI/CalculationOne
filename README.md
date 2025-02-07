# CalculationOne

A practical approach to improving calculation accuracy in language models by providing them with precise calculation tools.

## Overview
CalculationOne combines language models with Python tools to perform precise calculations. While currently limited to basic arithmetic operations, I hope this work provides a starting point for the community to develop more capable approaches to precise calculations in language models.

## Features
- Precise arithmetic operations using Python's Decimal class
- Basic operations: addition, subtraction, multiplication, division
- Power operations using both ^ and ** notation
- Local LLM integration using Ollama
- Regex-based mathematical expression detection
- Built-in safety checks for power operations

## Installation
```bash
# Clone the repository
git clone https://github.com/TheMachineIsLearning/calculationone.git
cd calculationone

# Install required packages
pip install requests ollama
```

## Prerequisites

- Python 3.7+
- Ollama installed and running locally
- A compatible LLM model loaded in Ollama (e.g., llama3.1)

## Limitations
- Currently only processes explicit mathematical expressions
- Does not handle word-form calculations (e.g., "twenty-three plus forty-five")
- Basic arithmetic and power operations only
- Synchronous processing only

## Future enhancements
- Support for word-form calculations
- Support for more complex mathematical expressions

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
- Thanks to the Ollama team for their excellent local LLM runtime
- Python's Decimal class for precise arithmetic operations

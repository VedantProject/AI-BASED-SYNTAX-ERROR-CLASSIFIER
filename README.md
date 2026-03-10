# AI-Based Syntax Error Classification - Phase 1
## Multi-Language Parser Framework

A scalable syntax parsing and validation system supporting multiple programming languages using grammar-driven parsing.

## Supported Languages
- C / C++
- Java
- Python

## Project Structure

```
Parser/
├── grammars/           # Grammar specifications for each language
│   ├── c_grammar.py
│   ├── java_grammar.py
│   └── python_grammar.py
├── lexers/             # Tokenizer modules
│   ├── c_lexer.py
│   ├── java_lexer.py
│   └── python_lexer.py
├── parsers/            # Parser modules
│   ├── c_parser.py
│   ├── java_parser.py
│   └── python_parser.py
├── syntax_tree/        # AST data structures
│   └── ast_nodes.py
├── datasets/           # Generated sample code
│   ├── c/
│   ├── java/
│   └── python/
├── results/            # Parsing results and diagnostics
├── main/               # Controller and utilities
│   ├── controller.py
│   ├── error_classifier.py
│   └── utils.py
├── dataset_generator.py
├── main.py
└── requirements.txt
```

## Features

✔ Grammar-driven parsing for multiple languages  
✔ Modular lexer/parser architecture  
✔ AST generation  
✔ Comprehensive syntax error detection and classification  
✔ Batch processing of large datasets  
✔ Synthetic dataset generation  
✔ Structured diagnostic output  

## Error Classification

The system detects and classifies:
- Missing delimiters (semicolons, braces, parentheses)
- Malformed expressions
- Keyword misuse
- Incomplete statements
- Indentation errors (Python)
- Type declaration errors
- And more...

## Usage

```bash
# Run single file parsing
python main.py --file path/to/file.c --language c

# Batch process datasets
python main.py --batch datasets/c/ --language c

# Generate datasets
python dataset_generator.py --language all --count 500
```

## Requirements

- Python 3.8+
- See requirements.txt for dependencies

## Output Format

```json
{
  "language": "Python",
  "error_type": "IndentationError",
  "line": 6,
  "message": "Unexpected indentation block"
}
```

## Future Work

Phase 2 will incorporate machine learning for intelligent error classification and correction suggestions.

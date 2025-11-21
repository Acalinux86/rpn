# Reverse Polish Notation (RPN) Evaluator (Interpreter)

This project implements a simple Reverse Polish Notation (postfix) calculator in Python.
It reads an input file containing space-separated tokens, converts them into typed tokens using enums, and evaluates the expression using a stack-based algorithm.

## Features

* Stack-based RPN evaluation
* Support for multi-digit and floating-point numbers
* Proper operand order handling (left/right)
* Enum-based token types for clarity and extensibility
* Error handling for invalid tokens, stack underflow, and malformed expressions

## Usage

### Reading From a File
``` bash
$ ./rpn.py --file <input_file>
```

###### Example test file 4 in test/:
``` bash
13 12 +
```

Example output:
``` bash
[INFO] Token: RPN_Token(token_type=<RPN_TokenType.TOKEN_DIGIT: 1>, token='25.0')
```

### Reading From the Standard Input
``` bash
$ rpn> 3 5 +
$ [INFO] Token: RPN_Token(token_type=<RPN_TokenType.TOKEN_DIGIT: 1>, token='8.0')
$ rpn>
```

## Input Format

* Tokens must be space-separated
* Supported operators: `+`, `-`, `*`, `/`
* Any valid floating-point number is allowed (e.g., `3`, `12`, `7.5`, `-2`)

## How It Works

1. The input file is split into individual tokens.
2. Tokens are converted into typed tokens using the enum `RPN_TokenType`.
3. The evaluator loops through the tokens:

   * Numbers are pushed onto the stack
   * Operators pop two operands, apply the operation, and push the result
4. At the end, the stack should contain exactly one value: the result

## Requirements

* Python 3.10 or later

#!/usr/bin/env python3

import sys
from typing import List, Tuple, Optional
from enum import Enum, auto
from dataclasses import dataclass

# Trace Debug Prints
TRACE = False

# Initial Stack Capacity
RPN_INITIAL_STACK_CAP = 256

# Shifts Command-Line Arguments
def rpn_shift_args(argv) -> Tuple[int , str]:
    if (len(argv) == 0):
        return 1 , " "
    else:
        return 0, argv.pop(0)

# Returns True when a token is operation code
def rpn_token_op(token: str) -> bool:
    return token == '+' or token == '*' or token == '/' or token == '-'

# Returns True when a token is number
def rpn_token_digit(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

# Read a file and turns it into list of chars
def rpn_read_entire_file(path: str) -> List[str]:
    with open(path, "r") as f:
        file_read = f.read()
    return file_read.split()

# Token Types
class RPN_TokenType(Enum):
    TOKEN_DIGIT = auto()
    TOKEN_PLUS = auto()
    TOKEN_MINUS = auto()
    TOKEN_DIV = auto()
    TOKEN_MULT = auto()

# Token Data Structure
@dataclass
class RPN_Token:
    token_type: RPN_TokenType
    token:      str

# Stack Data Structure
@dataclass
class RPN_Stack:
    stack_slots:    List[RPN_Token]
    stack_count:    int = 0
    stack_capacity: int = RPN_INITIAL_STACK_CAP

# Function that creates and returns a RPN_Token
def rpn_create_token(token_type: RPN_TokenType, token: str) -> RPN_Token:
    return RPN_Token(token_type, token)

# Function that pushes a token onto stack
def rpn_stack_push(stack: RPN_Stack, token: RPN_Token) -> bool:
    if (stack.stack_count >= stack.stack_capacity):
        stack.stack_capacity *= 2
    stack.stack_slots.append(token)
    stack.stack_count += 1
    if TRACE:
        print(f"[PUSH] {token}")
    return True

# Function that Pops a token from stack
def rpn_stack_pop(stack: RPN_Stack) -> Optional[RPN_Token]:
    if (stack.stack_count <= 0):
        print(f"[ERROR] Attempting to Pop from Empty Stack: count: {stack.stack_count}")
        return None
    stack.stack_count = stack.stack_count - 1
    res = stack.stack_slots.pop(stack.stack_count)
    if TRACE:
        print(f"[POP]  {res}")
    return res

# Function that Dumps Stack into stdout
def rpn_dump_stack(stack: RPN_Stack) -> None:
    if stack.stack_count == 0:
        print("Stack Empty")
        exit(1)
    for i in range(stack.stack_count):
        token = stack.stack_slots[i]
        print(f"[INFO] Token: {token}")

# Tokenize the Raw Character List
def rpn_tokenize_raw_list(char_list: List[str]) -> Optional[List[RPN_Token]]:
    tokens = []
    for i in char_list:
        if rpn_token_digit(i):
            token = rpn_create_token(RPN_TokenType.TOKEN_DIGIT, i)
        elif rpn_token_op(i):
            match i:
                case '+':
                    token = rpn_create_token(RPN_TokenType.TOKEN_PLUS, i)
                case '-':
                    token = rpn_create_token(RPN_TokenType.TOKEN_MINUS, i)
                case '/':
                    token = rpn_create_token(RPN_TokenType.TOKEN_DIV, i)
                case '*':
                    token = rpn_create_token(RPN_TokenType.TOKEN_MULT, i)
                case _:
                    print(f"[ERROR] Unknown Opcode: `{i}`") # Exit with non-zero when no known opcode is encountered
                    return None
        else:
            print(f"[ERROR] Unknown operation code: {i}")
            return None
        tokens.append(token)

    return tokens

# The Reverse Polish Notation Algorithm
def rpn(stack: RPN_Stack, test_list: List[RPN_Token]) -> bool:
    # Iterate Over Character Test List
    for token in test_list:
        # Push Digits
        if token.token_type == RPN_TokenType.TOKEN_DIGIT:
            if rpn_stack_push(stack, token) == False:
                return False

        elif rpn_token_op(token.token):
            # When Encountered a opcode
            right  = rpn_stack_pop(stack) # pop top
            left   = rpn_stack_pop(stack) # pop top - 1
            result = 0.0 # var to hold result
            if right is not None and left is not None:
                if token.token_type == RPN_TokenType.TOKEN_PLUS:
                    result = float(left.token) + float(right.token) # Add
                    if TRACE:
                        print(f"[INFO] Adding {float(left.token)} to {float(right.token)}")
                elif token.token_type == RPN_TokenType.TOKEN_MINUS:
                    result = float(left.token) - float(right.token) # subtract
                    if TRACE:
                        print(f"[INFO] Subtracting {float(left.token)} from {float(right.token)}")
                elif token.token_type == RPN_TokenType.TOKEN_DIV:
                    if float(right.token) == 0:
                        print("[ERROR] Division By Zero")
                        return False
                    result = float(left.token) / float(right.token) # divide
                    if TRACE:
                        print(f"[INFO] Dividing {float(left.token)} by {float(right.token)}")
                elif token.token_type == RPN_TokenType.TOKEN_MULT:
                    result = float(left.token) * float(right.token) # Multiply
                    if TRACE:
                        print(f"[INFO] Multiplying {float(left.token)} by {float(right.token)}")
                else:
                    print(f"[ERROR] Unknown Opcode: `{token}`") # Exit with non-zero when no known opcode is encountered
                    return False
            else:
                print(f"[ERROR] Token None")
                return False

            # Push the Result
            if rpn_stack_push(stack, rpn_create_token(RPN_TokenType.TOKEN_DIGIT, str(result))) == False:
                return False
        else:
            print(f"[ERROR] Unknown Character Encountered: {token}") # Exit if no known char encountered
            return False

    return True # Exit With Success

def rpn_usage(subcommand: str) -> None:
    print("[USAGE] %s <arg> [input-file]" % subcommand)
    print("[USAGE] arg:")
    print("[USAGE]     --read              -- Read From Stdin")
    print("[USAGE]     --file <input-file> -- Read From a Input File")

# The Entry Point of the Program
def main() -> int:
    argv = sys.argv[:] # The Command line args list

    err, subcommand = rpn_shift_args(argv) # Extract Program Name
    if err > 0:
        rpn_usage(subcommand)
        return err

    # If No Test File is provided Exit and print Usage
    if len(sys.argv) <= 0:
        rpn_usage(subcommand)
        return 1

    err, arg = rpn_shift_args(argv) # Extract Arg Name
    if err > 0:
        rpn_usage(subcommand)
        return err

    match arg:
        case "--file": # Provide Input File
            err, path = rpn_shift_args(argv) # Extract Input File Name
            if err > 0:
                rpn_usage(subcommand)
                print(f"\n[ERROR] No Input File: Input File Required")
                return err

            # Read the Entire test file into list in memory
            char_list = rpn_read_entire_file(path)

            # Tokenize the List
            token_list = rpn_tokenize_raw_list(char_list)

            # Initialize Empty Stack With Enough Capacity
            stack = RPN_Stack([])

            # Execute the Algorithm
            if token_list is not None:
                rpn(stack, token_list)
            else:
                print("[ERROR] Token list is None")
                return 1

            # Dump the Stack, Should Contain Final Answer
            rpn_dump_stack(stack)

        case "--read": # Interactive Mode
            # Read From stdin
            print("rpn> " , end="")
            sys.stdout.flush()
            for line in sys.stdin:
                sys.stdout.flush()
                # Remove Leading and Trailing Spaces
                line = line.strip().split()

                # Tokenize the line
                token_list = rpn_tokenize_raw_list(line)

                # Initialize Empty Stack
                stack = RPN_Stack([])

                # Execute the Algorithm
                if token_list is not None:
                    if rpn(stack, token_list) == False:
                        return 1
                else:
                    print("[ERROR] Token list is None")
                    return 1

                # Dump the Stack, Should Contain Final Answer
                rpn_dump_stack(stack)
                print("rpn> " , end="")
                sys.stdout.flush()

        case _:
            rpn_usage(subcommand)
            print(f"\n[ERROR] Unknown Argument: {arg}")
            return 1

    return 0 # return Zero

if __name__ == "__main__":
    exit(main())

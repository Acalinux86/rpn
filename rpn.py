#!/usr/bin/env python3

import sys
import os


# Trace Debug Prints
TRACE = False


# Initial Stack Capacity
RPN_INITIAL_STACK_CAP = 256


# Returns True when a token is operation code
def rpn_token_op(token):
    return token == '+' or token == '*' or token == '/' or token == '-'


# Returns True when a token is number
def rpn_token_digit(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


# Read a file and turns it into list of chars
def rpn_read_entire_file(path):
    with open(path, "r") as f:
        file_read = f.read()
    return file_read.split()


# Token Types
class RPNTokenType():
    TOKEN_DIGIT = 0
    TOKEN_PLUS = 1
    TOKEN_MINUS = 2
    TOKEN_DIV = 3
    TOKEN_MULT = 4


class RPNToken:
    def __init__(self, token_type, token):
        self.token_type = token_type  # Assigned to the instance
        self.token = token            # Assigned to the instance


# Stack Data Structure
class RPNStack:
    def __init__(self, stack_slots):
        self.stack_slots = stack_slots
        self.stack_count = 0
        self.stack_capacity = RPN_INITIAL_STACK_CAP


# Function that creates and returns a RPN_Token
def rpn_create_token(token_type, token):
    return RPNToken(token_type, token)


# Function that pushes a token onto stack
def rpn_stack_push(stack, token):
    if stack.stack_count >= stack.stack_capacity:
        stack.stack_capacity *= 2
    stack.stack_slots.append(token)
    stack.stack_count += 1
    if TRACE:
        print(f"[PUSH] {token.token}")
    return True


# Function that Pops a token from stack
def rpn_stack_pop(stack):
    if stack.stack_count <= 0:
        print("[ERROR] Attempting to Pop from Empty Stack: count: ", stack.stack_count)
        return None
    stack.stack_count = stack.stack_count - 1
    res = stack.stack_slots.pop(stack.stack_count)
    if TRACE:
        print(f"[POP]  {res.token}")
    return res


# Function that Dumps Stack into stdout
def rpn_dump_stack(stack):
    if stack.stack_count == 0:
        print("Stack Empty")
        os._exit(1)
    for token in stack.stack_slots:
        print("[INFO] Token: ", token.token)


# Tokenize the Raw Character List
def rpn_tokenize_raw_list(char_list):
    tokens = []
    for i in char_list:
        if rpn_token_digit(i):
            token = rpn_create_token(RPNTokenType.TOKEN_DIGIT, i)
        elif rpn_token_op(i):
            if i ==  '+':
                token = rpn_create_token(RPNTokenType.TOKEN_PLUS, i)
            elif i ==  '-':
                token = rpn_create_token(RPNTokenType.TOKEN_MINUS, i)
            elif i ==  '/':
                    token = rpn_create_token(RPNTokenType.TOKEN_DIV, i)
            elif i ==  '*':
                    token = rpn_create_token(RPNTokenType.TOKEN_MULT, i)
            else:
                print("[ERROR] Unknown Opcode: ", i) # Exit with non-zero when no known opcode is encountered
                return None
        else:
            print("[ERROR] Unknown operation code: ", i)
            return None
        tokens.append(token)

    return tokens


# The Reverse Polish Notation Algorithm
def rpn(stack, test_list):
    # Iterate Over Character Test List
    for token in test_list:
        # Push Digits
        if token.token_type == RPNTokenType.TOKEN_DIGIT:
            if not rpn_stack_push(stack, token):
                return False

        elif rpn_token_op(token.token):
            # When Encountered a opcode
            right  = rpn_stack_pop(stack) # pop top
            left   = rpn_stack_pop(stack) # pop top - 1
            result = 0.0 # var to hold result
            if right is not None and left is not None:
                if token.token_type == RPNTokenType.TOKEN_PLUS:
                    result = float(left.token) + float(right.token) # Add
                    if TRACE:
                        print(f"[INST] Add")
                        pass
                elif token.token_type == RPNTokenType.TOKEN_MINUS:
                    result = float(left.token) - float(right.token) # subtract
                    if TRACE:
                        print(f"[INST] Subtract")
                        pass
                elif token.token_type == RPNTokenType.TOKEN_DIV:
                    if float(right.token) == 0:
                        print("[ERROR] Division By Zero")
                        return False
                    result = float(left.token) / float(right.token) # divide
                    if TRACE:
                        print(f"[INST] Divide")
                        pass
                elif token.token_type == RPNTokenType.TOKEN_MULT:
                    result = float(left.token) * float(right.token) # Multiply
                    if TRACE:
                        print(f"[INST] Multiply")
                        pass
                else:
                    print("[ERROR] Unknown Opcode: ", token) # Exit with non-zero when no known opcode is encountered
                    return False
            else:
                print("[ERROR] Token None")
                return False

            # Push the Result
            if not rpn_stack_push(stack, rpn_create_token(RPNTokenType.TOKEN_DIGIT, str(result))):
                return False
        else:
            print("[ERROR] Unknown Character Encountered: ", token) # Exit if no known char encountered
            return False

    return True # Exit With Success


def rpn_usage(subcommand):
    print("USAGE] %s <options> [input-file]" % subcommand)
    print("Options:")
    print("--help              -- Display this Help Message")
    print("--file <input-file> -- Read From a Input File")


def repl():
    print("RPN REPL - Reverse Polish Notation Evaluator REPL")

    while True:
        print("rpn> " , end=" ")
        sys.stdout.flush()

        # Remove Leading and Trailing Spaces
        line = sys.stdin.readline().strip().split()
        if len(line) == 1 and line[0] == "exit":
            break

        # Tokenize the line
        token_list = rpn_tokenize_raw_list(line)
        if len(token_list) == 0:
            continue

        # Initialize Empty Stack
        stack = RPNStack([])

        # Execute the Algorithm
        if token_list is not None:
            if not rpn(stack, token_list):
                continue
        else:
            print("[ERROR] failed to process input")
            continue

        # Dump the Stack, Should Contain Final Answer
        rpn_dump_stack(stack)


def run_file(filename):
    src = rpn_read_entire_file(filename)
    tokens = rpn_tokenize_raw_list(src)
    stack = RPNStack([])
    rpn(stack, tokens)
    rpn_dump_stack(stack)


# The Entry Point of the Program
def main():
    program, *argv = sys.argv
    
    # Check For options
    if len(argv) == 0:
        repl()
        return 0
    elif len(argv) == 1:
        if argv[0] == "--help":
            rpn_usage(program)
            return 1
        else:
            rpn_usage(program)
            print("")
            print(f"[ERROR] Unrecognized Option: {argv[0]}")
            return 1
    elif len(argv) == 2:
        if argv[0] == "--file":
            run_file(argv[1])
            return 1
        else:
            rpn_usage(program)
            print("")
            print(f"[ERROR] Unrecognized Option: {argv[0]}")
            return 1
    else:
        return 1


if __name__ == "__main__":
    os._exit(main())

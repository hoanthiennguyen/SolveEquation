import unittest

from typing import List

from convert_to_token_list import convert_to_token_list
from util import peek, check_is_a_number


def get_precedence(operator):
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "^": 3
    }
    return precedence.get(operator, 0)


def is_right_associative(operator):
    return operator in ["^"]


def is_left_associative(operator):
    return not is_right_associative(operator)


def is_operand(token: str):
    return check_is_a_number(token) or token.isalpha()


def is_opening_bracket(token: str):
    return token in ["(", "[", "{"]


def is_closing_bracket(token: str):
    return token in [")", "]", "}"]


def is_bracket(token: str):
    return token in ["(", "[", "{", "}", "]", ")"]


def get_corresponding_closing_bracket(opening_bracket):
    if opening_bracket == "(":
        return ")"
    elif opening_bracket == "[":
        return "]"
    else:
        return "}"


def get_corresponding_opening_bracket(closing_bracket):
    if closing_bracket == ")":
        return "("
    elif closing_bracket == "]":
        return "["
    else:
        return "{"


def contain_opening_bracket(operator_stack: List[str]):
    return "(" in operator_stack or "[" in operator_stack or "{" in operator_stack


def is_operator(token):
    return token in ["+", "-", "*", "/", "^"]


def convert_infix_to_postfix(token_list: List[str]):
    # Reference: https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/
    result = []
    operator_stack = []
    for token in token_list:
        if is_operand(token):
            result.append(token)
        elif is_opening_bracket(token):
            operator_stack.append(token)
        elif is_closing_bracket(token):
            while len(operator_stack) > 0 and peek(operator_stack) != get_corresponding_opening_bracket(token):
                result.append(operator_stack.pop())
            # discard opening bracket
            if len(operator_stack) > 0:
                operator_stack.pop()
        else:
            while len(operator_stack) > 0 and \
                    (is_left_associative(token) and get_precedence(token) <= get_precedence(peek(operator_stack))
                     or is_right_associative(token) and get_precedence(token) < get_precedence(peek(operator_stack))):
                result.append(operator_stack.pop())
            operator_stack.append(token)

    while len(operator_stack) > 0:
        result.append(operator_stack.pop())

    return result


def convert_infix_to_postfix_testing_wrapper(expression):
    token_list = convert_to_token_list(expression)
    postfix_list = convert_infix_to_postfix(token_list)
    result = ""
    for item in postfix_list:
        result += " " + item
    return result[1:]


class Test(unittest.TestCase):
    # Reference: https://www.mathblog.dk/tools/infix-postfix-converter/
    def test_convert_to_postfix(self):
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("4"), "4")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("x"), "x")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("4+5"), "4 5 +")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("3+4*5"), "3 4 5 * +")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("1+2^2^3"), "1 2 2 3 ^ ^ +")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("3+4*5-2*6"), "3 4 5 * + 2 6 * -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("3+2*(x+1)-7"), "3 2 x 1 + * + 7 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("3+2*x^2-1"), "3 2 x 2 ^ * + 1 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("(x+1)^2-3"), "x 1 + 2 ^ 3 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("x-(x+1)*(x+2)-10"), "x x 1 + x 2 + * - 10 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("(x+1)*(x+2)-10"), "x 1 + x 2 + * 10 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("(x+10)^2-3"), "x 10 + 2 ^ 3 -")
        self.assertEqual(convert_infix_to_postfix_testing_wrapper("(2.5*x+10)^2-3"), "2.5 x * 10 + 2 ^ 3 -")

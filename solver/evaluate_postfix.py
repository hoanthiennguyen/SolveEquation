import unittest
from typing import List

from polynomial import Polynomial
from convert_to_postfix import is_operand, convert_to_token_list, convert_infix_to_postfix
from error import EvaluationError


def parse_operand(operand: str):
    if operand == 'x':
        dictionary = {1: 1}
    else:
        dictionary = {0: float(operand)}
    return Polynomial(dictionary)


def evaluate_postfix(token_list: List[str]):
    operand_stack = []
    for token in token_list:
        if is_operand(token):
            operand_stack.append(parse_operand(token))
        else:
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            if token == "+":
                result = op1.plus(op2)
            elif token == "-":
                result = op1.minus(op2)
            elif token == "*":
                result = op1.multiply(op2)
            elif token == "/":
                result = op1.divide(op2)
            elif token == "^":
                result = op1.power(op2)
            else:
                raise EvaluationError("Not supported operator: " + token)

            operand_stack.append(result)

    return operand_stack.pop()


def evaluate_postfix_testing_wrapper(expression):
    token_list = convert_to_token_list(expression)
    postfix_token_list = convert_infix_to_postfix(token_list)
    return evaluate_postfix(postfix_token_list)


class Tests(unittest.TestCase):
    def test_evaluate(self):
        expression = "3+4*5"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.from_constant(23))

        expression = "3+4*5^2"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.from_constant(103))

        expression = "1+2^2^3"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.from_constant(257))

        expression = "2*x-5+3*x"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("5x-5"))

        expression = "10-2*(x+1)"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("8-2x"))

        expression = "(x+2)^2-4"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("x^2+4x"))

        expression = "2*(x+2)^2-4"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("2x^2+8x+4"))

        expression = "10-3*(x+1)^2"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("7-3*x^2-6*x"))

        expression = "(x+1)^3"
        self.assertEqual(evaluate_postfix_testing_wrapper(expression), Polynomial.parse("x^3+3*x^2+3*x+1"))

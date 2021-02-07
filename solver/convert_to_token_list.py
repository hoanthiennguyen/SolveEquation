import unittest

from util import peek, check_is_a_number


def convert_to_token_list(expression):
    # TODO: consider handling sign +/-
    result = []
    for i in range(len(expression)):
        character = expression[i]
        if check_is_part_of_number(character) and len(result) > 0:
            last_token = peek(result)
            if check_is_a_number(last_token):
                result[len(result) - 1] = last_token + character
            else:
                result.append(character)
        else:
            result.append(character)
    return result


def check_is_part_of_number(character):
    return character in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]


class Tests(unittest.TestCase):
    
    def test_check_is_part_of_digit(self):
        self.assertEqual(check_is_part_of_number("5"), True)
        self.assertEqual(check_is_part_of_number("0"), True)
        self.assertEqual(check_is_part_of_number("9"), True)
        self.assertEqual(check_is_part_of_number("."), True)
        self.assertEqual(check_is_part_of_number("x"), False)

    def test_convert_to_token_list(self):
        self.assertEqual(convert_to_token_list("x"), ["x"])
        self.assertEqual(convert_to_token_list("x+1"), ["x", "+", "1"])
        self.assertEqual(convert_to_token_list("x+10"), ["x", "+", "10"])
        self.assertEqual(convert_to_token_list("x^2+10"), ["x", "^", "2", "+", "10"])
        self.assertEqual(convert_to_token_list("1.2*x^2+10"), ["1.2", "*", "x", "^", "2", "+", "10"])
        self.assertEqual(convert_to_token_list("1.25*x^2+100"), ["1.25", "*", "x", "^", "2", "+", "100"])

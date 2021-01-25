import unittest
from math import log

from polynomial import Polynomial


def convert_from_epsilon_to_n_digit(epsilon):
    return round(-log(epsilon, 10)) - 1


def try_round_root(polynomial, raw_root, n_digits):
    root = round(raw_root, n_digits)
    if abs(polynomial.eval(root)) <= abs(polynomial.eval(raw_root)):
        if int(root) == root:
            return int(root)
        else:
            return root
    else:
        return raw_root


class Tests(unittest.TestCase):

    def test_convert_from_epsilon_to_n_digit(self):
        self.assertEqual(convert_from_epsilon_to_n_digit(0.00001), 4)

    def test_try_round_root(self):
        p = Polynomial.parse("x-0.9999")
        raw_root = 0.9999
        root = try_round_root(p, raw_root, 3)
        self.assertEqual(root, 0.9999)

        p = Polynomial.parse("x^2-1")
        raw_root = 0.9999
        root = try_round_root(p, raw_root, 3)
        self.assertEqual(root, 1)

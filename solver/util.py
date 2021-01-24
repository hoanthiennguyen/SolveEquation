import unittest
from math import log


def convert_from_epsilon_to_n_digit(epsilon):
    return round(-log(epsilon, 10)) - 1


class Tests(unittest.TestCase):

    def test_convert_from_epsilon_to_n_digit(self):
        self.assertEqual(convert_from_epsilon_to_n_digit(0.00001), 4)

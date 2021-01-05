import unittest
from enum import Enum
from math import sqrt
from parse import parse_to_dictionary


class Equation(Enum):
    Linear = 1,
    Quadratic = 2,
    Cubic = 3,
    Arbitrary = 4


class Root(Enum):
    SomeRoots = 1,
    InfiniteRoots = 2,
    NoRoot = 3


def get_equation_type(expression):
    dictionary = parse_to_dictionary(expression)
    max_degree = 0
    for k in dictionary.keys():
        if k > max_degree and dictionary.get(k) > 0:
            max_degree = k
    if max_degree <= 1:
        return Equation.Linear
    elif max_degree == 2:
        return Equation.Quadratic
    elif max_degree == 3:
        return Equation.Cubic
    else:
        return Equation.Arbitrary


def solve_linear_equation(a, b):
    if a == 0:
        if b == 0:
            return Root.InfiniteRoots, ()
        else:
            return Root.NoRoot, ()
    else:
        return Root.SomeRoots, (- b / a)


def solve_quadratic_equation(a, b, c):
    if a == 0:
        return solve_linear_equation(b, a)

    delta = b ** 2 - 4 * a * c
    if delta > 0:
        x1 = (-b + sqrt(delta)) / (2 * a)
        x2 = (-b - sqrt(delta) / (2 * a))
        return Root.SomeRoots, (x1, x2)
    else:
        if delta == 0:
            return Root.SomeRoots, (-b / (2 * a))
        else:
            return Root.NoRoot, ()



class Tests(unittest.TestCase):

    def test_equation_type(self):
        self.assertEqual(get_equation_type("-x+3x2+1"), Equation.Quadratic)
        self.assertEqual(get_equation_type("x+1"), Equation.Linear)
        self.assertEqual(get_equation_type("x3+1"), Equation.Cubic)


if __name__ == '__main__':
    unittest.main()


import unittest

from monomial import Monomial


def get_next_monomial(expression, start):
    for i in range(start + 1, len(expression)):
        if (expression[i] == "+" or expression[i] == "-") \
                and expression[i-1] != "*" and expression[i-1] != "/" \
                and expression[i-1] != "+" and expression[i-1] != "-"\
                and expression[i-1] != "^":
            return expression[start:i]

    return expression[start:]


class Polynomial:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.dictionary == other.dictionary
        else:
            return False

    def __str__(self):
        result = ""
        for degree in self.dictionary:
            result += "{}x^{} + ".format(self.dictionary[degree], degree)

        return result[0:len(result) - 3]

    def __repr__(self):
        return self.__str__()

    def plus(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Parameter is not a Polynomial")

        for degree in other.dictionary:
            self.dictionary[degree] = self.dictionary.get(degree, 0) + other.dictionary[degree]

        return self

    def minus(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Parameter is not a Polynomial")

        for degree in other.dictionary:
            self.dictionary[degree] = self.dictionary.get(degree, 0) - other.dictionary[degree]

        return self

    @staticmethod
    def parse(expression):
        dictionary = {}
        index = 0
        while index < len(expression):
            monomial_str = get_next_monomial(expression, index)
            monomial = Monomial.parse(monomial_str)
            degree = monomial.degree
            coefficient = monomial.coefficient
            dictionary[degree] = dictionary.get(degree, 0) + coefficient
            index = index + len(monomial_str)

        return Polynomial(dictionary)


class Tests(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(Polynomial.parse("1"), Polynomial({0: 1}))
        self.assertEqual(Polynomial.parse("x"), Polynomial({1: 1}))
        self.assertEqual(Polynomial.parse("-x"), Polynomial({1: -1}))
        self.assertEqual(Polynomial.parse("x-x"), Polynomial({1: 0}))
        self.assertEqual(Polynomial.parse("20x"), Polynomial({1: 20}))
        self.assertEqual(Polynomial.parse("3*20x"), Polynomial({1: 60}))
        self.assertEqual(Polynomial.parse("3*2x+-5x"), Polynomial({1: 1}))
        self.assertEqual(Polynomial.parse("-x+3x^2+1"), Polynomial({2: 3, 1: -1, 0: 1}))
        self.assertEqual(Polynomial.parse("3x^2-x+1"), Polynomial({2: 3, 1: -1, 0: 1}))
        self.assertEqual(Polynomial.parse("3x^2-x+1+9x-3"), Polynomial({2: 3, 1: 8, 0: -2}))

    def test_plus(self):
        self.assertEqual(Polynomial.parse("2x-3").plus(Polynomial.parse("3x+5")), Polynomial.parse("5x+2"))
        self.assertEqual(Polynomial.parse("-2x-3").plus(Polynomial.parse("3x+5-x^2")), Polynomial.parse("x+2-x^2"))

    def test_minus(self):
        self.assertEqual(Polynomial.parse("2x-3").minus(Polynomial.parse("3x+5")), Polynomial.parse("-x-8"))
        self.assertEqual(Polynomial.parse("-2x-3").minus(Polynomial.parse("3x+5-x^2")), Polynomial.parse("x^2-5x-8"))


if __name__ == '__main__':
    unittest.main()

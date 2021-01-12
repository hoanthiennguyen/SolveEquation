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
            return self.simplify().dictionary == other.simplify().dictionary
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

        return self.simplify()

    def minus(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Parameter is not a Polynomial")

        for degree in other.dictionary:
            self.dictionary[degree] = self.dictionary.get(degree, 0) - other.dictionary[degree]

        return self.simplify()

    def multiply(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("Parameter is not a Polynomial")
        result = {}
        for d1 in self.dictionary:
            for d2 in other.dictionary:
                result[d1 + d2] = result.get(d1+d2, 0) + self.dictionary.get(d1) * other.dictionary.get(d2)

        return Polynomial(result).simplify()

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

        return Polynomial(dictionary).simplify()
    
    def simplify(self):
        zero_coefficient = []
        for degree in self.dictionary:
            if self.dictionary[degree] == 0:
                zero_coefficient.append(degree)
        
        for degree in zero_coefficient:
            self.dictionary.pop(degree)

        return self

    def get_full_coefficient(self):
        coefficients = []
        max_degree = 0
        for degree in self.dictionary:
            if degree > max_degree:
                max_degree = degree

        for degree in reversed(range(0, max_degree + 1)):
            coefficients.append(self.dictionary.get(degree, 0))

        return coefficients


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

    def test_get_full_coefficient(self):
        self.assertEqual(Polynomial.parse("x^2-1").get_full_coefficient(), [1, 0, -1])

    def test_plus(self):
        self.assertEqual(Polynomial.parse("2x-3").plus(Polynomial.parse("3x+5")), Polynomial.parse("5x+2"))
        self.assertEqual(Polynomial.parse("2x+1").plus(Polynomial.parse("0")), Polynomial.parse("2x+1"))
        self.assertEqual(Polynomial.parse("0").plus(Polynomial.parse("2x+1")), Polynomial.parse("2x+1"))
        self.assertEqual(Polynomial.parse("0").plus(Polynomial.parse("0")), Polynomial.parse("0"))
        self.assertEqual(Polynomial.parse("-2x-3").plus(Polynomial.parse("3x+5-x^2")), Polynomial.parse("x+2-x^2"))

    def test_minus(self):
        self.assertEqual(Polynomial.parse("2x+1").minus(Polynomial.parse("0")), Polynomial.parse("2x+1"))
        self.assertEqual(Polynomial.parse("0").minus(Polynomial.parse("2x+1")), Polynomial.parse("-2x-1"))
        self.assertEqual(Polynomial.parse("0").minus(Polynomial.parse("0")), Polynomial.parse("0"))
        self.assertEqual(Polynomial.parse("2x-3").minus(Polynomial.parse("3x+5")), Polynomial.parse("-x-8"))
        self.assertEqual(Polynomial.parse("-2x-3").minus(Polynomial.parse("3x+5-x^2")), Polynomial.parse("x^2-5x-8"))

    def test_multiply(self):
        self.assertEqual(Polynomial.parse("2").multiply(Polynomial.parse("3")), Polynomial.parse("6"))
        self.assertEqual(Polynomial.parse("-2").multiply(Polynomial.parse("3")), Polynomial.parse("-6"))
        self.assertEqual(Polynomial.parse("2").multiply(Polynomial.parse("-3")), Polynomial.parse("-6"))
        self.assertEqual(Polynomial.parse("-2").multiply(Polynomial.parse("-3")), Polynomial.parse("6"))
        self.assertEqual(Polynomial.parse("2").multiply(Polynomial.parse("x")), Polynomial.parse("2x"))
        self.assertEqual(Polynomial.parse("-2").multiply(Polynomial.parse("x")), Polynomial.parse("-2x"))
        self.assertEqual(Polynomial.parse("2").multiply(Polynomial.parse("-x")), Polynomial.parse("-2x"))
        self.assertEqual(Polynomial.parse("-2").multiply(Polynomial.parse("-x")), Polynomial.parse("2x"))
        self.assertEqual(Polynomial.parse("x").multiply(Polynomial.parse("x+1")), Polynomial.parse("x^2+x"))
        self.assertEqual(Polynomial.parse("x+1").multiply(Polynomial.parse("x+2")), Polynomial.parse("x^2+3x+2"))
        self.assertEqual(Polynomial.parse("x+1").multiply(Polynomial.parse("x-1")), Polynomial.parse("x^2-1"))
        self.assertEqual(Polynomial.parse("x+1").multiply(Polynomial.parse("-x-1")), Polynomial.parse("-x^2-1-2x"))


if __name__ == '__main__':
    unittest.main()

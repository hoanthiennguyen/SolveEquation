import unittest

from monomial import Monomial


def get_next_monomial(expression, start):
    for i in range(start + 1, len(expression)):
        if (expression[i] == "+" or expression[i] == "-") \
                and expression[i - 1] != "*" and expression[i - 1] != "/" \
                and expression[i - 1] != "+" and expression[i - 1] != "-" \
                and expression[i - 1] != "^":
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
                result[d1 + d2] = result.get(d1 + d2, 0) + self.dictionary.get(d1) * other.dictionary.get(d2)

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

    def derivative(self):
        result = {}
        for degree, coefficient in self.dictionary.items():
            if degree >= 1:
                result[degree - 1] = coefficient * degree

        return Polynomial(result)

    def eval(self, x):
        if x == float('inf'):
            return self.get_lim_at_inf()
        if x == float('-inf'):
            return self.get_lim_at_minus_inf()
        
        result = 0
        for degree, coefficient in self.dictionary.items():
            result += coefficient * x ** degree

        return result

    def get_highest_degree(self):
        max_degree = 0
        for degree in self.dictionary:
            if degree > max_degree:
                max_degree = degree

        return max_degree

    def get_coefficient(self, degree):
        return self.dictionary.get(degree, 0)
    
    def get_lim_at_inf(self):
        highest_degree = self.get_highest_degree()
        if self.dictionary[highest_degree] > 0:
            return float('inf')
        else:
            return float('-inf')

    def get_lim_at_minus_inf(self):
        highest_degree = self.get_highest_degree()
        if highest_degree % 2 == 0:
            if self.dictionary[highest_degree] > 0:
                return float('inf')
            else:
                return float('-inf')
        else:
            if self.dictionary[highest_degree] > 0:
                return float('-inf')
            else:
                return float('inf')
            

class Tests(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(Polynomial.parse("1"), Polynomial({0: 1}))
        self.assertEqual(Polynomial.parse("x"), Polynomial({1: 1}))
        self.assertEqual(Polynomial.parse("-x"), Polynomial({1: -1}))
        self.assertEqual(Polynomial.parse("x-x"), Polynomial({}))
        self.assertEqual(Polynomial.parse("20x"), Polynomial({1: 20}))
        self.assertEqual(Polynomial.parse("3*20x"), Polynomial({1: 60}))
        self.assertEqual(Polynomial.parse("1/3*x^3-x"), Polynomial({3: 1 / 3, 1: -1}))
        self.assertEqual(Polynomial.parse("x^3/3-x"), Polynomial({3: 1 / 3, 1: -1}))
        self.assertEqual(Polynomial.parse("3*2x+-5x"), Polynomial({1: 1}))
        self.assertEqual(Polynomial.parse("-x+3x^2+1"), Polynomial({2: 3, 1: -1, 0: 1}))
        self.assertEqual(Polynomial.parse("3x^2-x+1"), Polynomial({2: 3, 1: -1, 0: 1}))
        self.assertEqual(Polynomial.parse("3x^2-x+1+9x-3"), Polynomial({2: 3, 1: 8, 0: -2}))

    def test_get_full_coefficient(self):
        self.assertEqual(Polynomial.parse("x^2-1").get_full_coefficient(), [1, 0, -1])
        self.assertEqual(Polynomial.parse("x^2-2x-1").get_full_coefficient(), [1, -2, -1])
        self.assertEqual(Polynomial.parse("x^2-2x").get_full_coefficient(), [1, -2, 0])
        self.assertEqual(Polynomial.parse("x^2").get_full_coefficient(), [1, 0, 0])

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
        self.assertEqual(Polynomial.parse("0").multiply(Polynomial.parse("-x-1")), Polynomial.parse("0"))
        self.assertEqual(Polynomial.parse("x+1").multiply(Polynomial.parse("0")), Polynomial.parse("0"))

    def test_diff(self):
        self.assertEqual(Polynomial.parse("10").derivative(), Polynomial.parse("0"))
        self.assertEqual(Polynomial.parse("x+1").derivative(), Polynomial.parse("1"))
        self.assertEqual(Polynomial.parse("2x^2+3x+1").derivative(), Polynomial.parse("4x+3"))

    def test_eval(self):
        self.assertEqual(Polynomial.parse("0").eval(10), 0)
        self.assertEqual(Polynomial.parse("x").eval(10), 10)
        self.assertEqual(Polynomial.parse("2x+10").eval(10), 30)
        self.assertEqual(Polynomial.parse("2.5x+10").eval(10), 35)
        self.assertEqual(Polynomial.parse("x^2+2x+1").eval(3), 16)
        self.assertEqual(Polynomial.parse("3x^4+8x^3-6x^2-24x").eval(float('inf')), float('inf'))
        self.assertEqual(Polynomial.parse("3x^4+8x^3-6x^2-24x").eval(float('-inf')), float('inf'))

    def test_lim_at_inf(self):
        self.assertEqual(Polynomial.parse("3x^4+8x^3-6x^2-24x").get_lim_at_inf(), float('inf'))
        self.assertEqual(Polynomial.parse("-3x^4+8x^3-6x^2-24x").get_lim_at_inf(), float('-inf'))

        self.assertEqual(Polynomial.parse("3x^3-6x^2-24x").get_lim_at_inf(), float('inf'))
        self.assertEqual(Polynomial.parse("-3x^3-6x^2-24x").get_lim_at_inf(), float('-inf'))

    def test_lim_at_minus_inf(self):
        self.assertEqual(Polynomial.parse("3x^4+8x^3-6x^2-24x").get_lim_at_minus_inf(), float('inf'))
        self.assertEqual(Polynomial.parse("-3x^4+8x^3-6x^2-24x").get_lim_at_minus_inf(), float('-inf'))

        self.assertEqual(Polynomial.parse("3x^3-6x^2-24x").get_lim_at_minus_inf(), float('-inf'))
        self.assertEqual(Polynomial.parse("-3x^3-6x^2-24x").get_lim_at_minus_inf(), float('inf'))

    def test_get_coefficient(self):
        self.assertEqual(Polynomial.parse("-x^2+1").get_coefficient(2), -1)
        self.assertEqual(Polynomial.parse("-x^2+1").get_coefficient(1), 0)
        self.assertEqual(Polynomial.parse("-x^2+1").get_coefficient(0), 1)


if __name__ == '__main__':
    unittest.main()

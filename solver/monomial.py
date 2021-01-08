import unittest

from atom import Atom


def get_next_atom(expression, start):
    for i in range(start + 1, len(expression)):
        if expression[i] == "*" or expression[i] == "/":
            return expression[start:i]

    return expression[start:]


class Monomial:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def __eq__(self, other):
        if isinstance(other, Monomial):
            return self.degree == other.degree and self.coefficient == other.coefficient
        else:
            return False

    @staticmethod
    def parse(expression):
        atom0_str = get_next_atom(expression, 0)
        atom0 = Atom.parse(atom0_str)

        if len(atom0_str) == len(expression):
            return Monomial(atom0.coefficient, atom0.degree)
        else:
            index = len(atom0_str) + 1
            while index < len(expression):
                next_atom_str = get_next_atom(expression, index)
                next_atom = Atom.parse(next_atom_str)
                if expression[index - 1] == "*":
                    atom0 = atom0.multiply(next_atom)
                else:
                    atom0 = atom0.divide(next_atom)
                
                index = index + len(next_atom_str) + 1

            return Monomial(atom0.coefficient, atom0.degree)


class Tests(unittest.TestCase):

    def test_parse(self):
        self.assertEqual(Monomial.parse("1"), Monomial(1, 0))
        self.assertEqual(Monomial.parse("x"), Monomial(1, 1))
        self.assertEqual(Monomial.parse("20x"), Monomial(20, 1))
        self.assertEqual(Monomial.parse("3*20x"), Monomial(60, 1))
        self.assertEqual(Monomial.parse("x*x"), Monomial(1, 2))
        self.assertEqual(Monomial.parse("x*-x"), Monomial(-1, 2))
        self.assertEqual(Monomial.parse("x*-2x"), Monomial(-2, 2))
        self.assertEqual(Monomial.parse("-x*x"), Monomial(-1, 2))
        self.assertEqual(Monomial.parse("-x*-x"), Monomial(1, 2))
        self.assertEqual(Monomial.parse("3*2x*x*2"), Monomial(12, 2))


if __name__ == '__main__':
    unittest.main()

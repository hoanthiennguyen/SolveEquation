import unittest


class ParseException(Exception):
    pass


class Atom:
    def __init__(self, coefficient, degree):
        self.coefficient = coefficient
        self.degree = degree

    def __eq__(self, other):
        if isinstance(other, Atom):
            return self.degree == other.degree and self.coefficient == other.coefficient
        else:
            return False

    @staticmethod
    def simple_validate(expression):
        if len(expression) == 0:
            return False
        if expression.find("*") >= 0 or expression.find("/") >= 0:
            return False
        return True

    @staticmethod
    def validate(expression):
        try:
            Atom.parse(expression)
        except ParseException:
            return False
        return True

    @staticmethod
    def find_sign(expression):
        sign = 1
        offset = 0
        while offset < len(expression):
            if expression[offset] == "+":
                sign = sign
            elif expression[offset] == "-":
                sign = -sign
            else:
                break
            offset = offset + 1
        return sign, offset

    @staticmethod
    def parse(expression):
        if not Atom.simple_validate(expression):
            raise ParseException("Invalid atom: " + expression)

        sign, offset = Atom.find_sign(expression)
        expression = expression[offset:]

        try:
            index_of_x = expression.find('x')
            if index_of_x < 0:
                coefficient = float(expression)
                degree = 0
            else:
                if index_of_x == 0:
                    coefficient = 1
                else:
                    coefficient = float(expression[0:index_of_x])

                if index_of_x == len(expression) - 1:
                    degree = 1
                else:
                    if expression[index_of_x + 1] == '^':
                        degree = int(expression[index_of_x + 2:])
                        if degree < 0:
                            raise ParseException("Degree cannot be negative")
                    else:
                        raise ParseException("Invalid atom: " + expression)

        except ValueError:
            raise ParseException("Invalid atom: " + expression)
        return Atom(sign * coefficient, degree)

    def multiply(self, other):
        if not isinstance(other, Atom):
            raise Exception("Parameter is not an atom")
        return Atom(self.coefficient * other.coefficient, self.degree + other.degree)

    def divide(self, other):
        if not isinstance(other, Atom):
            raise Exception("Parameter is not an atom")
        if other.coefficient == 0:
            raise Exception("Cannot divided by 0")
        return Atom(self.coefficient / other.coefficient, self.degree - other.degree)


class Tests(unittest.TestCase):

    def test_multiply(self):
        self.assertEqual(Atom(2, 2).multiply(Atom(2, 3)), Atom(4, 5))
        self.assertEqual(Atom(1, 0).multiply(Atom(2, 3)), Atom(2, 3))
        self.assertEqual(Atom(0, 0).multiply(Atom(2, 3)), Atom(0, 3))
        self.assertEqual(Atom(2, 3).multiply(Atom(1, 0)), Atom(2, 3))
        self.assertEqual(Atom(2, 3).multiply(Atom(0, 0)), Atom(0, 3))

    def test_parse(self):
        self.assertEqual(Atom.validate(""), False)
        self.assertEqual(Atom.validate("1"), True)
        self.assertEqual(Atom.validate("10"), True)
        self.assertEqual(Atom.validate("-10"), True)
        self.assertEqual(Atom.validate("+10"), True)
        self.assertEqual(Atom.validate("*10"), False)
        self.assertEqual(Atom.validate("/10"), False)
        self.assertEqual(Atom.validate("10-1"), False)
        self.assertEqual(Atom.validate("10+1"), False)
        self.assertEqual(Atom.validate("10/1"), False)
        self.assertEqual(Atom.validate("10*1"), False)
        self.assertEqual(Atom.validate("x"), True)
        self.assertEqual(Atom.validate("2x"), True)
        self.assertEqual(Atom.validate("-2x"), True)
        self.assertEqual(Atom.validate("+2x"), True)
        self.assertEqual(Atom.validate("2.x"), True)
        self.assertEqual(Atom.validate("2.1x"), True)
        self.assertEqual(Atom.validate("a"), False)
        self.assertEqual(Atom.validate("2a"), False)
        self.assertEqual(Atom.validate("-2a"), False)
        self.assertEqual(Atom.validate("+2a"), False)
        self.assertEqual(Atom.validate("xx"), False)
        self.assertEqual(Atom.validate("2xx"), False)
        self.assertEqual(Atom.validate("x2x"), False)
        self.assertEqual(Atom.validate("xx2"), False)
        self.assertEqual(Atom.validate("2.1.x"), False)
        self.assertEqual(Atom.validate("2x2"), False)
        self.assertEqual(Atom.validate("2x^2"), True)
        self.assertEqual(Atom.validate("2x^2/3"), False)
        self.assertEqual(Atom.validate("2x^2.1"), False)
        self.assertEqual(Atom.validate("2a^2"), False)
        self.assertEqual(Atom.validate("2xa^2"), False)
        self.assertEqual(Atom.validate("+2+2"), False)
        self.assertEqual(Atom.validate("++2"), True)
        self.assertEqual(Atom.validate("-+2"), True)
        self.assertEqual(Atom.validate("-+2x"), True)
        self.assertEqual(Atom.validate("-+20x^2"), True)
        self.assertEqual(Atom.validate("-+20x^-2"), False)
        self.assertEqual(Atom.parse("-+20x^2"), Atom(-20, 2))
        self.assertEqual(Atom.parse("+-20x^2"), Atom(-20, 2))
        self.assertEqual(Atom.parse("--20x^2"), Atom(20, 2))
        self.assertEqual(Atom.parse("++20x^2"), Atom(20, 2))


if __name__ == '__main__':
    unittest.main()

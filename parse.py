import unittest


def parse(expression):
    result = []
    index = 0
    while index < len(expression):
        monomial = get_next_monomial(expression, index)
        index = index + len(monomial)
        result.append(get_coefficient_and_degree(monomial))
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def parse_to_dictionary(expression):
    result = {}
    index = 0
    while index < len(expression):
        monomial = get_next_monomial(expression, index)
        index = index + len(monomial)
        degree = get_coefficient_and_degree(monomial)[1]
        coefficient = get_coefficient_and_degree(monomial)[0]
        result[degree] = result.get(degree, 0) + coefficient
    return result


def get_next_monomial(expression, start):
    for i in range(start + 1, len(expression)):
        if expression[i] == "+" or expression[i] == "-":
            return expression[start:i]

    return expression[start:]


def get_coefficient_and_degree(monomial):
    index_of_x = monomial.find('x')
    if index_of_x < 0:
        coefficient = eval(monomial)
        degree = 0
    else:
        if index_of_x == 0:
            coefficient = 1
        else:
            coefficient = monomial[0:index_of_x]
            if coefficient == "-":
                coefficient = -1
            elif coefficient == "+":
                coefficient = 1
            else:
                coefficient = eval(monomial[0:index_of_x])
        if index_of_x == len(monomial) - 1:
            degree = 1
        else:
            degree = eval(monomial[index_of_x + 1:])
    return coefficient, degree


class Tests(unittest.TestCase):

    def test_get_coefficient_and_degree(self):
        self.assertEqual(get_coefficient_and_degree("10"), (10, 0))
        self.assertEqual(get_coefficient_and_degree("+x"), (1, 1))
        self.assertEqual(get_coefficient_and_degree("-x"), (-1, 1))
        self.assertEqual(get_coefficient_and_degree("+2x"), (2, 1))
        self.assertEqual(get_coefficient_and_degree("-2x"), (-2, 1))
        self.assertEqual(get_coefficient_and_degree("20x"), (20, 1))
        self.assertEqual(get_coefficient_and_degree("1.2x"), (1.2, 1))
        self.assertEqual(get_coefficient_and_degree("x2"), (1, 2))
        self.assertEqual(get_coefficient_and_degree("-30x^2"), (-30, 2))

    def test_get_next_monomial(self):
        self.assertEqual(get_next_monomial("1", 0), "1")
        self.assertEqual(get_next_monomial("+1", 0), "+1")
        self.assertEqual(get_next_monomial("-1", 0), "-1")
        self.assertEqual(get_next_monomial("-2x2+3x-9", 0), "-2x2")
        self.assertEqual(get_next_monomial("2x2-3x-9", 3), "-3x")
        self.assertEqual(get_next_monomial("2x2+3x-9", 6), "-9")

    def test_parse(self):
        self.assertEqual(parse("1"), [(1, 0)])
        self.assertEqual(parse("x"), [(1, 1)])
        self.assertEqual(parse("x+1"), [(1, 1), (1, 0)])
        self.assertEqual(parse("3x+1"), [(3, 1), (1, 0)])
        self.assertEqual(parse("1+3x"), [(3, 1), (1, 0)])
        self.assertEqual(parse("-x+3x2+1"), [(3, 2), (-1, 1), (1, 0)])

    def test_parse_to_dictionary(self):
        self.assertEqual(parse_to_dictionary("-x+3x2+1"), {2: 3, 1: -1, 0: 1})
        self.assertEqual(parse_to_dictionary("3x2-x+1"), {2: 3, 1: -1, 0: 1})
        self.assertEqual(parse_to_dictionary("3x2-x+1+9x-3"), {2: 3, 1: 8, 0: -2})


if __name__ == '__main__':
    unittest.main()


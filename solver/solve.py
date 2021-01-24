import unittest

from polynomial import Polynomial

ROUND_UP_TO_N_DIGIT = 3


def find_root_using_bisection(polynomial, epsilon, lower, upper):
    if polynomial.eval(lower) * polynomial.eval(upper) > 0:
        return None

    middle = (lower + upper) / 2
    while abs(polynomial.eval(middle)) > epsilon:
        if polynomial.eval(middle) * polynomial.eval(upper) > 0:
            upper = middle
        else:
            lower = middle
        middle = (lower + upper) / 2

    middle = round_root(polynomial, middle, ROUND_UP_TO_N_DIGIT)
    if int(middle) == middle:
        middle = int(middle)
    return middle


def find_root(polynomial, epsilon, lower, upper):
    if abs(polynomial.eval(lower)) <= epsilon:
        return None
    if abs(polynomial.eval(upper)) <= epsilon:
        return upper
    if polynomial.eval(lower) * polynomial.eval(upper) > 0:
        return None

    if lower == float('-inf') and upper == float('inf'):
        lower = get_lower_bound_with_opposite_sign(polynomial, 0)
        upper = get_upper_bound_with_opposite_sign(polynomial, 0)
        
    elif lower == float('-inf'):
        lower = get_lower_bound_with_opposite_sign(polynomial, upper)
        
    elif upper == float('inf'):
        upper = get_upper_bound_with_opposite_sign(polynomial, lower)

    return find_root_using_bisection(polynomial, epsilon, lower, upper)


def get_lower_bound_with_opposite_sign(polynomial, upper, init_step=1):
    if polynomial.eval(float('-inf')) * polynomial.eval(upper) > 0:
        return None

    step = init_step
    lower = upper - step
    while polynomial.eval(lower) * polynomial.eval(upper) > 0:
        step = step * 2
        lower = lower - step

    return lower


def get_upper_bound_with_opposite_sign(polynomial, lower, init_step=1):
    if polynomial.eval(float('inf')) * polynomial.eval(lower) > 0:
        return None

    step = init_step
    upper = lower + step
    while polynomial.eval(lower) * polynomial.eval(upper) > 0:
        step = step * 2
        upper = upper + step

    return upper


def solve_from_derivative_roots(polynomial, epsilon, derivative_roots):
    roots = []
    check_points = derivative_roots.copy()
    check_points.insert(0, float('-inf'))
    check_points.append(float('inf'))

    for index in range(0, len(check_points) - 1):
        root = find_root(polynomial, epsilon, check_points[index], check_points[index + 1])
        if root is not None:
            roots.append(root)
        
    return roots


def solve_equation(polynomial, epsilon):
    if polynomial.get_highest_degree() == 0:
        if polynomial.get_coefficient(0) != 0:
            return []
        else:
            return ["Infinite roots"]

    if polynomial.get_highest_degree() == 1:
        [a, b] = polynomial.get_full_coefficient()
        return [-b / a]
    else:
        derivative = polynomial.derivative()
        derivative_roots = solve_equation(derivative, epsilon)
        return solve_from_derivative_roots(polynomial, epsilon, derivative_roots)


def parse_and_solve(expression, epsilon):
    if expression.find("=") < 0:
        return solve_equation(Polynomial.parse(expression), epsilon)
    else:
        if expression.endswith("=0"):
            return solve_equation(Polynomial.parse(expression[0:len(expression)-2]), epsilon)
        else:
            index_of_equal = expression.find("=")
            a = Polynomial.parse(expression[0:index_of_equal])
            b = Polynomial.parse(expression[index_of_equal+1:])
            return solve_equation(a.minus(b), epsilon)


def round_root(polynomial, raw_root, n_digits):
    ith = n_digits
    root = round(raw_root, ith)
    if abs(polynomial.eval(root)) < abs(polynomial.eval(raw_root)):
        return root
    else:
        return raw_root


class Tests(unittest.TestCase):

    def test_get_lower_bound_with_opposite_sign(self):
        self.assertEqual(get_lower_bound_with_opposite_sign(Polynomial.parse("x^3"), 1), 0)
        self.assertEqual(get_lower_bound_with_opposite_sign(Polynomial.parse("x^2+9"), -2), None)

    def test_get_upper_bound_with_opposite_sign(self):
        self.assertEqual(get_upper_bound_with_opposite_sign(Polynomial.parse("x^3"), 1), None)
        self.assertEqual(get_upper_bound_with_opposite_sign(Polynomial.parse("x^3"), -10), 5)

    def test_bisect(self):
        epsilon = 0.0001

        polynomial = Polynomial.parse("x^3/3-x")
        root = find_root_using_bisection(polynomial, epsilon, 1, 10)
        self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^2-x-2")
        root = find_root_using_bisection(polynomial, epsilon, -100, 0)
        self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^2-x-2")
        root = find_root_using_bisection(polynomial, epsilon, -100, -10)
        self.assertEqual(root, None)

    def test_solve_from_derivative_roots(self):
        epsilon = 0.0001

        polynomial = Polynomial.parse("x^3+x")
        derivative_roots = []
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^2-6x+1")
        derivative_roots = [3]
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^3-3x^2+2x-10")
        derivative_roots = [0.42, 1.57]
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

    def test_solve_equation(self):
        epsilon = 0.0001

        polynomial = Polynomial.parse("0x+6")
        roots = solve_equation(polynomial, epsilon)
        self.assertEqual(roots, [])

        polynomial = Polynomial.parse("0x+0")
        roots = solve_equation(polynomial, epsilon)
        self.assertEqual(roots, ["Infinite roots"])

        polynomial = Polynomial.parse("11x+6")
        roots = solve_equation(polynomial, epsilon)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("6x^2+11x+6")
        roots = solve_equation(polynomial, epsilon)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^3+6x^2+11x+6")
        roots = solve_equation(polynomial, epsilon)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^4-4x^2+20x-7")
        roots = solve_equation(polynomial, epsilon)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)

        polynomial = Polynomial.parse("x^2-1").multiply(Polynomial.parse("x^2-4"))
        roots = solve_equation(polynomial, epsilon)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) <= epsilon, True)
            
    def test_parse_and_solve(self):
        epsilon = 0.0001
        
        expression = "x^2-1"
        roots = parse_and_solve(expression, epsilon)
        for root in roots:
            print(root)

        expression = "x^2-1=0"
        roots = parse_and_solve(expression, epsilon)
        for root in roots:
            print(root)

        expression = "x^2-1=8"
        roots = parse_and_solve(expression, epsilon)
        for root in roots:
            print(root)

        expression = "x^2-1=-2x+2"
        roots = parse_and_solve(expression, epsilon)
        for root in roots:
            print(root)

        expression = "x^2+2.5x+1.5"
        roots = parse_and_solve(expression, epsilon)
        for root in roots:
            print(root)

    def test_round_root(self):
        p = Polynomial.parse("x-0.9999")
        raw_root = 0.9999
        root = round_root(p, raw_root, 3)
        print(root)

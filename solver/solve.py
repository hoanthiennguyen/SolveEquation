import unittest

from polynomial import Polynomial


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

    return middle


def find_root(polynomial, epsilon, lower, upper):
    if polynomial.eval(lower) == 0:
        return None
    if polynomial.eval(upper) == 0:
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
        self.assertEqual(abs(polynomial.eval(root)) < epsilon, True)

        polynomial = Polynomial.parse("x^2-x-2")
        root = find_root_using_bisection(polynomial, epsilon, -100, 0)
        self.assertEqual(abs(polynomial.eval(root)) < epsilon, True)

        polynomial = Polynomial.parse("x^2-x-2")
        root = find_root_using_bisection(polynomial, epsilon, -100, -10)
        self.assertEqual(root, None)

    def test_solve_from_derivative_roots(self):
        epsilon = 0.0001

        polynomial = Polynomial.parse("x^3+x")
        derivative_roots = []
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) < epsilon, True)

        polynomial = Polynomial.parse("x^2-6x+1")
        derivative_roots = [3]
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) < epsilon, True)

        polynomial = Polynomial.parse("x^3-3x^2+2x-10")
        derivative_roots = [0.42, 1.57]
        roots = solve_from_derivative_roots(polynomial, epsilon, derivative_roots)
        for root in roots:
            self.assertEqual(abs(polynomial.eval(root)) < epsilon, True)

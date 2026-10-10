"""Tests for the m1b_ambiguous_misc formulas in the mathematics domain.

Reference values come from independent oracles: the phase-2b oracle (50-digit mpmath, exact
fractions, brute force) and the phase-3 oracle script ``ambiguous_misc_oracle_values.py``
(mpmath at 300 digits from the exact double inputs: exact roots, eigenvalues from the
characteristic polynomial, the source's arccos forms for the angles, coordinate geometry for
Stewart, log-gamma for the large birthday cases, quadrature for the Gaussian integral). Exact
Fraction/integer arithmetic, brute-force enumeration and a trapezoid-rule quadrature are done in
the tests themselves. No reference value is produced by an evaluator under test.
"""

import itertools
import math
import random
import unittest
from fractions import Fraction

from sciengformulary.catalog.mathematics.angle_between_line_and_plane import (
    angle_between_line_and_plane,
)
from sciengformulary.catalog.mathematics.angle_between_lines_3d import angle_between_lines_3d
from sciengformulary.catalog.mathematics.birthday_distinct_probability import (
    birthday_distinct_probability,
)
from sciengformulary.catalog.mathematics.eigenvalue_2x2_larger_real import (
    eigenvalue_2x2_larger_real,
)
from sciengformulary.catalog.mathematics.eigenvalue_2x2_smaller_real import (
    eigenvalue_2x2_smaller_real,
)
from sciengformulary.catalog.mathematics.gamma_half_integer import gamma_half_integer
from sciengformulary.catalog.mathematics.gaussian_integral import gaussian_integral
from sciengformulary.catalog.mathematics.quadratic_root_minus import quadratic_root_minus
from sciengformulary.catalog.mathematics.quadratic_root_plus import quadratic_root_plus
from sciengformulary.catalog.mathematics.reciprocal_triangular_number_sum import (
    reciprocal_triangular_number_sum,
)
from sciengformulary.catalog.mathematics.stewart_cevian_length import stewart_cevian_length
from sciengformulary.catalog.mathematics.sum_of_squares_first_integers import (
    sum_of_squares_first_integers,
)
from sciengformulary.catalog.mathematics.total_probability_two_events import (
    total_probability_two_events,
)
from sciengformulary.core import FormulaSpec

DERIVED = (
    quadratic_root_plus,
    quadratic_root_minus,
    eigenvalue_2x2_larger_real,
    eigenvalue_2x2_smaller_real,
    angle_between_lines_3d,
    angle_between_line_and_plane,
    stewart_cevian_length,
    sum_of_squares_first_integers,
    reciprocal_triangular_number_sum,
    birthday_distinct_probability,
    gamma_half_integer,
    total_probability_two_events,
)
ALL = (*DERIVED, gaussian_integral)
BAD_NUMBERS = (math.nan, math.inf, -math.inf, True, "1", None)


def close(actual, expected, rel=1e-14, abs_=0.0):
    return math.isclose(actual, expected, rel_tol=rel, abs_tol=abs_)


class ConstructionTest(unittest.TestCase):
    """Importing a module runs validate() and verify(); check the catalog-level rules too."""

    def test_all_constructed_with_matching_ids(self):
        for formula in ALL:
            with self.subTest(formula=formula.id):
                self.assertIsInstance(formula, FormulaSpec)
                self.assertTrue(formula.id.startswith("mathematics."))

    def test_derived_formulas_carry_a_derived_result_assumption(self):
        for formula in DERIVED:
            with self.subTest(formula=formula.id):
                self.assertTrue(
                    any(line.startswith("Derived result:") for line in formula.assumptions)
                )
        self.assertFalse(
            any(line.startswith("Derived result:") for line in gaussian_integral.assumptions)
        )

    def test_assumptions_are_ascii(self):
        for formula in ALL:
            for line in (*formula.assumptions, formula.description):
                with self.subTest(formula=formula.id):
                    self.assertTrue(line.isascii())


class QuadraticRootsTest(unittest.TestCase):
    def evaluate(self, a, b, c):
        return (
            quadratic_root_plus.evaluate(a=a, b=b, c=c),
            quadratic_root_minus.evaluate(a=a, b=b, c=c),
        )

    def test_a_zero_raises(self):
        for a in (0, 0.0, -0.0):
            for formula in (quadratic_root_plus, quadratic_root_minus):
                with self.subTest(a=a), self.assertRaises(ValueError):
                    formula.evaluate(a=a, b=1.0, c=1.0)

    def test_negative_discriminant_raises(self):
        for formula in (quadratic_root_plus, quadratic_root_minus):
            with self.assertRaises(ValueError):
                formula.evaluate(a=1, b=0, c=1)
            with self.assertRaises(ValueError):
                formula.evaluate(a=1, b=1, c=0.25 + 1e-12)  # b^2 - 4ac = -4e-12

    def test_non_finite_and_non_numeric_inputs_raise(self):
        for formula in (quadratic_root_plus, quadratic_root_minus):
            for name in ("a", "b", "c"):
                for bad in BAD_NUMBERS:
                    inputs = {**dict(a=1.0, b=-3.0, c=2.0), name: bad}
                    with self.subTest(formula=formula.id, name=name, value=bad):
                        with self.assertRaises(ValueError):
                            formula.evaluate(**inputs)

    def test_branch_follows_the_sign_before_the_root_not_the_size(self):
        for a, b, c in ((1, -3, 2), (-1, 0, 4), (-2, 3, 5), (-0.5, 1.25, 3), (3, 2, -1)):
            plus, minus = self.evaluate(a, b, c)
            with self.subTest(a=a, b=b, c=c):
                if a > 0:
                    self.assertGreater(plus, minus)
                else:
                    self.assertLess(plus, minus)

    def test_double_root_is_the_same_on_both_branches(self):
        self.assertEqual(self.evaluate(1, 2, 1), (-1.0, -1.0))
        self.assertEqual(self.evaluate(-4, 4, -1), (0.5, 0.5))
        self.assertEqual(self.evaluate(2, 0, 0), (0.0, 0.0))

    def test_matches_exact_rational_roots(self):
        # Source form (-b +/- s) / (2a) in exact arithmetic wherever the discriminant is a
        # perfect square.
        checked = 0
        for a, b, c in itertools.product(range(-6, 7), range(-8, 9), range(-6, 7)):
            discriminant = b * b - 4 * a * c
            if a == 0 or discriminant < 0 or math.isqrt(discriminant) ** 2 != discriminant:
                continue
            s = math.isqrt(discriminant)
            plus, minus = Fraction(-b + s, 2 * a), Fraction(-b - s, 2 * a)
            with self.subTest(a=a, b=b, c=c):
                self.assertTrue(close(quadratic_root_plus.evaluate(a=a, b=b, c=c), plus, 1e-15))
                self.assertTrue(close(quadratic_root_minus.evaluate(a=a, b=b, c=c), minus, 1e-15))
            checked += 1
        self.assertGreater(checked, 100)

    def test_oracle_values_with_cancellation_and_extreme_scales(self):
        # mpmath roots of the exact double inputs (phase-3 oracle).
        cases = (
            (1.0, -1e8, 1.0, 99999999.99999999, 1e-08),
            (2.5, 4e7, 0.125, -3.1250000000000007e-09, -15999999.999999996),
            (-1.0, 1e8, -1.0, 1e-08, 99999999.99999999),
            (1.0, 2.0, 0.999999999999, -0.9999990000110609, -1.000000999988939),
            (1e-200, 3e-200, 1e-200, -0.38196601125010515, -2.618033988749895),
            (1e200, 3e200, 1e200, -0.38196601125010515, -2.618033988749895),
            (1.0, 1e15, 1e-3, -1e-18, -1000000000000000.0),
        )
        for a, b, c, plus, minus in cases:
            with self.subTest(a=a, b=b, c=c):
                got_plus, got_minus = self.evaluate(a, b, c)
                self.assertTrue(close(got_plus, plus, 1e-14), (got_plus, plus))
                self.assertTrue(close(got_minus, minus, 1e-14), (got_minus, minus))

    def test_vieta_relations(self):
        rng = random.Random(7)
        for _ in range(200):
            a = rng.uniform(0.1, 5) * rng.choice((-1, 1))
            r1, r2 = rng.uniform(-9, 9), rng.uniform(-9, 9)
            b, c = -a * (r1 + r2), a * r1 * r2
            plus, minus = self.evaluate(a, b, c)
            with self.subTest(a=a, r1=r1, r2=r2):
                self.assertTrue(close(plus + minus, -b / a, 1e-9, 1e-12))
                self.assertTrue(close(plus * minus, c / a, 1e-9, 1e-12))

    def test_accepts_integers_and_ints_in_floats(self):
        self.assertEqual(self.evaluate(1, -3, 2), self.evaluate(1.0, -3.0, 2.0))

    def test_unrepresentable_roots_raise_overflow(self):
        # Roots -b/a = -1e600 (outside the float range) and -c/b = -1e-300 (representable): only
        # the root outside the range raises.
        with self.assertRaises(OverflowError):
            quadratic_root_minus.evaluate(a=1e-300, b=1e300, c=1.0)
        self.assertTrue(
            close(quadratic_root_plus.evaluate(a=1e-300, b=1e300, c=1.0), -1e-300, 1e-15)
        )


class EigenvalueTest(unittest.TestCase):
    def evaluate(self, a11, a12, a21, a22):
        kwargs = dict(a11=a11, a12=a12, a21=a21, a22=a22)
        return (
            eigenvalue_2x2_larger_real.evaluate(**kwargs),
            eigenvalue_2x2_smaller_real.evaluate(**kwargs),
        )

    def test_complex_eigenvalues_raise(self):
        for formula in (eigenvalue_2x2_larger_real, eigenvalue_2x2_smaller_real):
            with self.assertRaises(ValueError):
                formula.evaluate(a11=0, a12=-1, a21=1, a22=0)  # rotation by 90 degrees
            with self.assertRaises(ValueError):
                formula.evaluate(a11=1, a12=-1, a21=1, a22=1)  # eigenvalues 1 +/- i

    def test_non_finite_and_non_numeric_inputs_raise(self):
        for formula in (eigenvalue_2x2_larger_real, eigenvalue_2x2_smaller_real):
            for name in ("a11", "a12", "a21", "a22"):
                for bad in BAD_NUMBERS:
                    inputs = {**dict(a11=2.0, a12=1.0, a21=1.0, a22=2.0), name: bad}
                    with self.subTest(formula=formula.id, name=name, value=bad):
                        with self.assertRaises(ValueError):
                            formula.evaluate(**inputs)

    def test_boundary_zero_discriminant_gives_a_repeated_eigenvalue(self):
        self.assertEqual(self.evaluate(2, 1, 0, 2), (2.0, 2.0))
        self.assertEqual(self.evaluate(3, 0, 0, 3), (3.0, 3.0))
        self.assertEqual(self.evaluate(1, 1, -0.25, 0), (0.5, 0.5))  # (1 - 0)^2 + 4*(-0.25) = 0

    def test_zero_and_nilpotent_matrices(self):
        self.assertEqual(self.evaluate(0, 0, 0, 0), (0.0, 0.0))
        self.assertEqual(self.evaluate(0, 1, 0, 0), (0.0, 0.0))
        self.assertEqual(self.evaluate(1, 1, -1, -1), (0.0, 0.0))

    def test_larger_is_not_below_smaller(self):
        rng = random.Random(3)
        for _ in range(300):
            entries = [rng.uniform(-5, 5) for _ in range(4)]
            entries[2] = entries[1] * rng.uniform(0.5, 2)  # keep same-sign off-diagonals real
            if entries[1] * entries[2] < 0:
                entries[2] = -entries[2]
            larger, smaller = self.evaluate(*entries)
            self.assertGreaterEqual(larger, smaller)

    def test_matches_exact_rational_eigenvalues(self):
        # Integer matrices whose discriminant is a perfect square have rational eigenvalues
        # (t +/- s) / 2; compare with exact arithmetic.
        rng = random.Random(11)
        checked = 0
        while checked < 150:
            a11, a12, a21, a22 = (rng.randint(-9, 9) for _ in range(4))
            disc = (a11 - a22) ** 2 + 4 * a12 * a21
            if disc < 0 or math.isqrt(disc) ** 2 != disc:
                continue
            s, t = math.isqrt(disc), a11 + a22
            larger, smaller = self.evaluate(a11, a12, a21, a22)
            with self.subTest(matrix=(a11, a12, a21, a22)):
                self.assertTrue(close(larger, Fraction(t + s, 2), 1e-15))
                self.assertTrue(close(smaller, Fraction(t - s, 2), 1e-15))
            checked += 1

    def test_oracle_values_including_near_singular_and_extreme_scales(self):
        # mpmath eigenvalues of the exact double entries (phase-3 oracle).
        cases = (
            ((1e8, 1.0, 1.0, 1e-8), 100000000.00000001, 2.092256083012847e-25),
            ((1.0, 2.0, 3.0, 4.0), 5.372281323269014, -0.3722813232690143),
            ((1e-200, 2e-200, 3e-200, 4e-200), 5.372281323269015e-200, -3.722813232690143e-201),
            ((1e200, 2e200, 3e200, 4e200), 5.372281323269014e200, -3.7228132326901434e199),
            ((1.0, 1.0, 1.0, 1.000000000001), 2.0000000000005, 5.000444502910455e-13),
            ((1.0, 1e10, 1e-10, 2.0), 2.618033988749895, 0.38196601125010515),
            ((-3.0, 1.0, 2.0, -4.0), -2.0, -5.0),
        )
        for matrix, larger, smaller in cases:
            got_larger, got_smaller = self.evaluate(*matrix)
            with self.subTest(matrix=matrix):
                self.assertTrue(close(got_larger, larger, 1e-14), (got_larger, larger))
                self.assertTrue(close(got_smaller, smaller, 1e-14), (got_smaller, smaller))

    def test_trace_and_determinant_identities(self):
        # Independent route for the derived closed form: the eigenvalues sum to the trace and
        # multiply to the determinant.
        rng = random.Random(5)
        for _ in range(200):
            a11, a22 = rng.uniform(-6, 6), rng.uniform(-6, 6)
            a12 = rng.uniform(-6, 6)
            a21 = rng.uniform(-6, 6) if rng.random() < 0.5 else a12
            if (a11 - a22) ** 2 + 4 * a12 * a21 < 0:
                continue
            larger, smaller = self.evaluate(a11, a12, a21, a22)
            with self.subTest(matrix=(a11, a12, a21, a22)):
                self.assertTrue(close(larger + smaller, a11 + a22, 1e-12, 1e-12))
                self.assertTrue(close(larger * smaller, a11 * a22 - a12 * a21, 1e-9, 1e-12))

    def test_eigenvalues_scale_with_the_matrix(self):
        base = (1.5, 0.5, 0.25, -1.0)
        larger, smaller = self.evaluate(*base)
        for factor in (2.0**-1000, 1e-30, 4.0, 1e100):
            scaled = self.evaluate(*(factor * v for v in base))
            with self.subTest(factor=factor):
                self.assertTrue(close(scaled[0], factor * larger, 1e-14))
                self.assertTrue(close(scaled[1], factor * smaller, 1e-14))

    def test_eigenvalue_beyond_the_float_range_raises_overflow(self):
        # Eigenvalues 3.4e308 (outside the float range) and 0 (representable).
        positive = dict(a11=1.7e308, a12=1.7e308, a21=1.7e308, a22=1.7e308)
        with self.assertRaises(OverflowError):
            eigenvalue_2x2_larger_real.evaluate(**positive)
        self.assertEqual(eigenvalue_2x2_smaller_real.evaluate(**positive), 0.0)
        # Eigenvalues 0 and -3.4e308.
        negative = dict(a11=-1.7e308, a12=1.7e308, a21=1.7e308, a22=-1.7e308)
        self.assertEqual(eigenvalue_2x2_larger_real.evaluate(**negative), 0.0)
        with self.assertRaises(OverflowError):
            eigenvalue_2x2_smaller_real.evaluate(**negative)


def _source_lines_angle(u, v):
    """Selinger's rule in plain floats: the smaller of theta and pi - theta (moderate values)."""
    dot = sum(p * q for p, q in zip(u, v))
    cos = dot / (math.sqrt(sum(p * p for p in u)) * math.sqrt(sum(p * p for p in v)))
    theta = math.acos(max(-1.0, min(1.0, cos)))
    return min(theta, math.pi - theta)


class AngleBetweenLinesTest(unittest.TestCase):
    def evaluate(self, u, v):
        return angle_between_lines_3d.evaluate(ux=u[0], uy=u[1], uz=u[2], vx=v[0], vy=v[1], vz=v[2])

    def test_zero_vector_raises(self):
        with self.assertRaises(ValueError):
            self.evaluate((0, 0, 0), (1, 2, 3))
        with self.assertRaises(ValueError):
            self.evaluate((1, 2, 3), (0.0, -0.0, 0.0))

    def test_non_finite_and_non_numeric_inputs_raise(self):
        for index in range(6):
            for bad in BAD_NUMBERS:
                values = [1.0, 2.0, 3.0, 4.0, -5.0, 6.0]
                values[index] = bad
                with self.subTest(index=index, value=bad), self.assertRaises(ValueError):
                    self.evaluate(values[:3], values[3:])

    def test_range_and_symmetries(self):
        rng = random.Random(1)
        for _ in range(300):
            u = [rng.uniform(-5, 5) for _ in range(3)]
            v = [rng.uniform(-5, 5) for _ in range(3)]
            angle = self.evaluate(u, v)
            with self.subTest(u=u, v=v):
                self.assertTrue(0.0 <= angle <= math.pi / 2)
                self.assertEqual(angle, self.evaluate(v, u))
                self.assertTrue(close(angle, self.evaluate([-p for p in u], v), 1e-13))
                self.assertTrue(close(angle, self.evaluate(u, [-2.5 * q for q in v]), 1e-13, 1e-15))
                self.assertTrue(close(angle, _source_lines_angle(u, v), 1e-9, 1e-12))

    def test_parallel_and_perpendicular_boundaries(self):
        self.assertEqual(self.evaluate((1, 2, 3), (-2, -4, -6)), 0.0)
        self.assertEqual(self.evaluate((1, 2, 3), (1, 2, 3)), 0.0)
        self.assertEqual(self.evaluate((1, 0, 0), (0, 5, 0)), math.pi / 2)
        self.assertEqual(self.evaluate((1, 1, 0), (-1, 1, 7)), math.pi / 2)

    def test_folds_the_obtuse_vector_angle(self):
        # Vector angle 2 pi / 3 (Selinger's example) becomes pi / 3; 3 pi / 4 becomes pi / 4.
        self.assertTrue(close(self.evaluate((-1, 1, 2), (2, 1, -1)), math.pi / 3, 1e-14))
        self.assertTrue(close(self.evaluate((1, 0, 0), (-1, 1, 0)), math.pi / 4, 1e-14))

    def test_oracle_values_near_the_ends_of_the_range_and_extreme_scales(self):
        # Source form (arccos with the smaller of theta, pi - theta) in 300-digit mpmath.
        cases = (
            ((1.0, 0.0, 0.0), (1.0, 1e-09, 0.0), 1e-09),
            ((1.0, 0.0, 0.0), (-1.0, 1e-09, 0.0), 1e-09),
            ((1.0, 0.0, 0.0), (1e-09, 1.0, 0.0), 1.5707963257948967),
            ((1.0, 0.0, 0.0), (-1e-09, 1.0, 0.0), 1.5707963257948967),
            ((3.0, -4.0, 12.0), (-5.0, 2.0, -1.0), 1.0569323198690264),
            ((1e-200, 2e-200, 3e-200), (-4e200, 5e200, 6e200), 0.7510483299035025),
            (
                (1.852825167802701, -0.7466788481238626, -4.287762544632183),
                (1.8528251678027077, -0.746678848124875, -4.287762544634846),
                2.5714464692299163e-13,
            ),
        )
        for u, v, expected in cases:
            with self.subTest(u=u, v=v):
                self.assertTrue(close(self.evaluate(u, v), expected, 1e-14))

    def test_accepts_integers_and_integral_floats(self):
        self.assertEqual(
            self.evaluate((1, 2, 3), (4, -5, 6)), self.evaluate((1.0, 2.0, 3.0), (4.0, -5.0, 6.0))
        )


class AngleBetweenLineAndPlaneTest(unittest.TestCase):
    def evaluate(self, d, n):
        return angle_between_line_and_plane.evaluate(
            dx=d[0], dy=d[1], dz=d[2], nx=n[0], ny=n[1], nz=n[2]
        )

    def test_zero_vector_raises(self):
        with self.assertRaises(ValueError):
            self.evaluate((0, 0, 0), (0, 0, 1))
        with self.assertRaises(ValueError):
            self.evaluate((1, 0, 0), (0, 0.0, -0.0))

    def test_non_finite_and_non_numeric_inputs_raise(self):
        for index in range(6):
            for bad in BAD_NUMBERS:
                values = [1.0, 2.0, 3.0, 4.0, -5.0, 6.0]
                values[index] = bad
                with self.subTest(index=index, value=bad), self.assertRaises(ValueError):
                    self.evaluate(values[:3], values[3:])

    def test_range_sign_invariance_and_complement_of_the_line_angle(self):
        rng = random.Random(2)
        for _ in range(300):
            d = [rng.uniform(-5, 5) for _ in range(3)]
            n = [rng.uniform(-5, 5) for _ in range(3)]
            angle = self.evaluate(d, n)
            with self.subTest(d=d, n=n):
                self.assertTrue(0.0 <= angle <= math.pi / 2)
                self.assertTrue(close(angle, self.evaluate([-p for p in d], n), 1e-13))
                self.assertTrue(close(angle, self.evaluate(d, [-3.0 * q for q in n]), 1e-13, 1e-15))
                # Source form: pi/2 - arccos(|n.d| / (|n||d|)) in plain floats.
                self.assertTrue(close(angle, math.pi / 2 - _source_lines_angle(d, n), 1e-9, 1e-12))
                # The line-plane angle and the line-normal angle are complementary.
                line_normal = angle_between_lines_3d.evaluate(
                    ux=d[0], uy=d[1], uz=d[2], vx=n[0], vy=n[1], vz=n[2]
                )
                self.assertTrue(close(angle + line_normal, math.pi / 2, 1e-14))

    def test_boundaries(self):
        self.assertEqual(self.evaluate((1, 0, 0), (0, 0, 1)), 0.0)  # parallel to the plane
        self.assertEqual(self.evaluate((1, 2, 0), (0, 0, 5)), 0.0)
        self.assertEqual(self.evaluate((0, 0, -3), (0, 0, 1)), math.pi / 2)  # along the normal
        self.assertEqual(self.evaluate((2, 4, 6), (1, 2, 3)), math.pi / 2)

    def test_reversed_direction_gives_the_same_acute_angle(self):
        # n . d = +4 and -4 both give pi/2 - arccos(4/9) = 0.4605539916813224 (mpmath).
        self.assertTrue(close(self.evaluate((2, -1, -2), (2, 2, -1)), 0.4605539916813224, 1e-14))
        self.assertTrue(close(self.evaluate((-2, 1, 2), (2, 2, -1)), 0.4605539916813224, 1e-14))

    def test_oracle_values_near_the_ends_of_the_range_and_extreme_scales(self):
        # Source form pi/2 - arccos(|n.d| / (|n||d|)) in 300-digit mpmath.
        cases = (
            ((1.0, 0.0, 1e-09), (0.0, 0.0, 1.0), 1e-09),
            ((-1.0, 0.0, -1e-09), (0.0, 0.0, 1.0), 1e-09),
            ((1e-09, 0.0, 1.0), (0.0, 0.0, 1.0), 1.5707963257948967),
            ((1e-09, 0.0, -1.0), (0.0, 0.0, 1.0), 1.5707963257948967),
            ((3.0, -4.0, 12.0), (-5.0, 2.0, -1.0), 0.5138640069258703),
            ((1e-200, 2e-200, 3e-200), (-4e200, 5e200, 6e200), 0.8197479968913941),
        )
        for d, n, expected in cases:
            with self.subTest(d=d, n=n):
                self.assertTrue(close(self.evaluate(d, n), expected, 1e-14))


class StewartCevianTest(unittest.TestCase):
    def evaluate(self, b, c, m, n):
        return stewart_cevian_length.evaluate(b=b, c=c, m=m, n=n)

    def test_non_positive_and_non_finite_inputs_raise(self):
        for name in ("b", "c", "m", "n"):
            for bad in (0, -1.0, math.nan, math.inf, True, "1"):
                inputs = {**dict(b=5.0, c=6.0, m=3.0, n=4.0), name: bad}
                with self.subTest(name=name, value=bad), self.assertRaises(ValueError):
                    stewart_cevian_length.evaluate(**inputs)

    def test_strict_triangle_inequality_is_required(self):
        with self.assertRaises(ValueError):
            self.evaluate(1.0, 1.0, 1.0, 1.0)  # base 2 = b + c: degenerate
        with self.assertRaises(ValueError):
            self.evaluate(3.0, 1.0, 1.0, 1.0)  # base 2 = b - c: degenerate
        with self.assertRaises(ValueError):
            self.evaluate(1.0, 1.0, 1.0, 1.5)  # base longer than b + c
        with self.assertRaises(ValueError):
            self.evaluate(5.0, 1.0, 1.0, 1.0)  # base shorter than b - c

    def test_median_special_case(self):
        # m = n: the median, m_a = sqrt(2 b^2 + 2 c^2 - a^2) / 2 with a = m + n.
        rng = random.Random(4)
        for _ in range(200):
            b, c = rng.uniform(1, 10), rng.uniform(1, 10)
            a = rng.uniform(abs(b - c) + 1e-3, b + c - 1e-3)
            expected = math.sqrt(2 * b * b + 2 * c * c - a * a) / 2
            with self.subTest(b=b, c=c, a=a):
                self.assertTrue(close(self.evaluate(b, c, a / 2, a / 2), expected, 1e-12))

    def test_isosceles_median_is_the_height(self):
        self.assertEqual(self.evaluate(13.0, 13.0, 5.0, 5.0), 12.0)

    def test_stewart_identity_holds(self):
        # The source's relation c^2 n + b^2 m = (m + n)(d^2 + m n), checked in exact arithmetic
        # on the rounded result up to the rounding of d.
        rng = random.Random(6)
        for _ in range(200):
            b, c = rng.uniform(1, 10), rng.uniform(1, 10)
            a = rng.uniform(abs(b - c) + 1e-3, b + c - 1e-3)
            m = a * rng.uniform(0.05, 0.95)
            n = a - m
            d = self.evaluate(b, c, m, n)
            fb, fc, fm, fn, fd = map(Fraction, (b, c, m, n, d))
            left, right = fc**2 * fn + fb**2 * fm, (fm + fn) * (fd**2 + fm * fn)
            with self.subTest(b=b, c=c, m=m, n=n):
                self.assertTrue(close(float(left), float(right), 1e-13))

    def test_angle_bisector_length(self):
        # Bisector from the apex: BP : PC = c : b, length sqrt(b c ((b + c)^2 - a^2)) / (b + c).
        rng = random.Random(8)
        for _ in range(100):
            b, c = rng.uniform(2, 9), rng.uniform(2, 9)
            a = rng.uniform(abs(b - c) + 0.1, b + c - 0.1)
            m, n = a * c / (b + c), a * b / (b + c)
            expected = math.sqrt(b * c * ((b + c) ** 2 - a * a)) / (b + c)
            with self.subTest(b=b, c=c, a=a):
                self.assertTrue(close(self.evaluate(b, c, m, n), expected, 1e-12))

    def test_swapping_the_pieces_and_sides_together_is_a_symmetry(self):
        self.assertEqual(self.evaluate(5.0, 6.0, 3.0, 4.0), self.evaluate(6.0, 5.0, 4.0, 3.0))

    def test_oracle_values_from_coordinate_geometry(self):
        # B = (0, 0), C = (m + n, 0), P = (m, 0), apex from the two sides (300-digit mpmath).
        cases = (
            ((1.0, 1.0, 1.0, 0.999999999999), 9.999889390787672e-07),
            ((13.0, 13.0, 5.0, 5.0), 12.0),
            ((7.0, 9.0, 2.0, 8.0), 7.655063683601855),
            ((3e-150, 4e-150, 2e-150, 3e-150), 2.6832815729997476e-150),
            ((5.0, 6.0, 6.999, 0.001), 4.999457213395413),
        )
        for inputs, expected in cases:
            with self.subTest(inputs=inputs):
                self.assertTrue(close(self.evaluate(*inputs), expected, 1e-14))

    def test_lengths_are_scale_invariant_without_overflow_or_underflow(self):
        # Powers of two scale exactly; squares of these lengths would leave the float range.
        for exponent in (900, -900):
            factor = 2.0**exponent
            with self.subTest(exponent=exponent):
                self.assertEqual(
                    self.evaluate(3 * factor, 4 * factor, 2.5 * factor, 2.5 * factor),
                    2.5 * factor,
                )
                self.assertTrue(
                    close(
                        self.evaluate(5 * factor, 6 * factor, 3 * factor, 4 * factor),
                        4.3915503282684 * factor,
                        1e-14,
                    )
                )


class SumOfSquaresTest(unittest.TestCase):
    def test_domain(self):
        for bad in (-1, 2.5, math.nan, math.inf, True, "3", None):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                sum_of_squares_first_integers.evaluate(n=bad)

    def test_matches_term_by_term_sum_and_is_exact(self):
        running = 0
        for n in range(0, 201):
            with self.subTest(n=n):
                self.assertEqual(sum_of_squares_first_integers.evaluate(n=n), running)
            running += (n + 1) ** 2

    def test_telescoping_difference_for_huge_n(self):
        # S(n) - S(n - 1) = n^2 holds exactly, with no float overflow.
        for n in (10**6, 10**30, 7 * 10**100 + 3):
            difference = sum_of_squares_first_integers.evaluate(
                n=n
            ) - sum_of_squares_first_integers.evaluate(n=n - 1)
            with self.subTest(n=n):
                self.assertEqual(difference, n * n)

    def test_returns_exact_integer_and_accepts_integral_float(self):
        self.assertIsInstance(sum_of_squares_first_integers.evaluate(n=100000), int)
        self.assertEqual(sum_of_squares_first_integers.evaluate(n=100000), 333338333350000)
        self.assertEqual(sum_of_squares_first_integers.evaluate(n=10.0), 385)


class ReciprocalTriangularSumTest(unittest.TestCase):
    def test_domain(self):
        for bad in (-1, 2.5, math.nan, math.inf, True, "3", None):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                reciprocal_triangular_number_sum.evaluate(n=bad)

    def test_matches_exact_fraction_sum(self):
        total = Fraction(0)
        for n in range(0, 301):
            with self.subTest(n=n):
                self.assertEqual(reciprocal_triangular_number_sum.evaluate(n=n), float(total))
            total += Fraction(2, (n + 1) * (n + 2))  # 1 / T_(n+1)

    def test_range_and_limit(self):
        self.assertEqual(reciprocal_triangular_number_sum.evaluate(n=0), 0.0)
        self.assertEqual(reciprocal_triangular_number_sum.evaluate(n=1), 1.0)
        self.assertLess(reciprocal_triangular_number_sum.evaluate(n=10**6), 2.0)
        self.assertTrue(close(reciprocal_triangular_number_sum.evaluate(n=10**20), 2.0, 1e-15))
        self.assertTrue(close(reciprocal_triangular_number_sum.evaluate(n=99), 1.98, 1e-15))
        self.assertEqual(
            reciprocal_triangular_number_sum.evaluate(n=7.0),
            reciprocal_triangular_number_sum.evaluate(n=7),
        )


def _birthday_enumeration(m, n):
    """Probability that all n assignments to m days differ, by listing all m^n assignments."""
    good = sum(1 for f in itertools.product(range(m), repeat=n) if len(set(f)) == n)
    return Fraction(good, m**n)


def _birthday_exact(m, n):
    return Fraction(math.perm(m, n), m**n)


class BirthdayTest(unittest.TestCase):
    def evaluate(self, m, n):
        return birthday_distinct_probability.evaluate(m=m, n=n)

    def test_domain(self):
        for name in ("m", "n"):
            for bad in (-1, 2.5, math.nan, math.inf, True, "3", None):
                inputs = {**dict(m=365, n=23), name: bad}
                with self.subTest(name=name, value=bad), self.assertRaises(ValueError):
                    birthday_distinct_probability.evaluate(**inputs)
        with self.assertRaises(ValueError):
            self.evaluate(0, 0)

    def test_matches_enumeration_of_all_assignments(self):
        for m in range(1, 6):
            for n in range(0, 6):
                with self.subTest(m=m, n=n):
                    self.assertTrue(
                        close(self.evaluate(m, n), float(_birthday_enumeration(m, n)), 1e-15)
                    )

    def test_boundaries(self):
        self.assertEqual(self.evaluate(365, 0), 1.0)
        self.assertEqual(self.evaluate(365, 1), 1.0)
        self.assertEqual(self.evaluate(1, 1), 1.0)
        self.assertEqual(self.evaluate(3, 4), 0.0)  # more people than days
        self.assertEqual(self.evaluate(10**6, 10**6 + 1), 0.0)
        self.assertEqual(self.evaluate(365, 366), 0.0)

    def test_classical_instance_and_exact_fractions(self):
        # The source's 23/22 instance, then exact integer quotients.
        self.assertLess(self.evaluate(365, 23), 0.5)
        self.assertGreater(self.evaluate(365, 22), 0.5)
        for m, n in ((365, 23), (365, 60), (365, 100), (10**6, 1000), (2**64, 5000), (50, 50)):
            with self.subTest(m=m, n=n):
                self.assertTrue(close(self.evaluate(m, n), float(_birthday_exact(m, n)), 1e-15))

    def test_probability_is_decreasing_in_n_and_complement_is_in_range(self):
        previous = 1.0
        for n in range(0, 101):
            value = self.evaluate(365, n)
            self.assertTrue(0.0 <= value <= previous)
            previous = value

    def test_series_branch_agrees_with_exact_integer_quotients(self):
        # n > 10000 uses the series; compare with the exact value of perm(m, n) / m^n.
        for m, n in ((10**5, 10_001), (10**5, 12_000), (10**6, 20_000), (10**7, 30_000)):
            with self.subTest(m=m, n=n):
                self.assertTrue(close(self.evaluate(m, n), float(_birthday_exact(m, n)), 2e-12))

    def test_series_and_exact_branches_meet_at_the_switch(self):
        # P(n + 1) = P(n) * (m - n) / m links n = 10000 (exact) to n = 10001 (series).
        m = 10**6
        exact = self.evaluate(m, 10_000)
        self.assertTrue(close(self.evaluate(m, 10_001), exact * (m - 10_000) / m, 2e-12))

    def test_large_arguments_against_mpmath_log_gamma(self):
        # mpmath exp(lgamma(m + 1) - lgamma(m - n + 1) - n log m) at 300 digits (phase-3 oracle).
        cases = (
            (10**9, 10**6, 6.033338300166272e-218),
            (10**12, 10**6, 0.6065308618896548),
            (2**64, 5 * 10**9, 0.5078209481887472),
            (2**64, 10**9, 0.9732589911255687),
            (2**128, 10**19, 0.8633485446270184),
            (10**30, 10**16, 1.928749847963606e-22),
            (10**6, 30_000, 3.889723911778072e-198),
            (10**5, 10_001, 1.6086169581404858e-225),
        )
        for m, n, expected in cases:
            with self.subTest(m=m, n=n):
                self.assertTrue(close(self.evaluate(m, n), expected, 2e-12))

    def test_huge_number_of_bins_uses_the_series_and_stays_fast(self):
        # m^n has millions of bits; the probability of a collision is far below float epsilon.
        self.assertEqual(self.evaluate(10**400, 10_000), 1.0)
        self.assertEqual(self.evaluate(2**100_000, 60), 1.0)
        self.assertEqual(self.evaluate(10**300, 2), 1.0)

    def test_probability_that_underflows_is_zero(self):
        self.assertEqual(self.evaluate(10**6, 100_000), 0.0)
        self.assertEqual(self.evaluate(10**5, 20_000), 0.0)

    def test_accepts_integral_floats(self):
        self.assertEqual(self.evaluate(365.0, 23.0), self.evaluate(365, 23))


class GammaHalfIntegerTest(unittest.TestCase):
    def test_domain(self):
        for bad in (-1, 2.5, math.nan, math.inf, True, "3", None):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                gamma_half_integer.evaluate(k=bad)

    def test_overflow_beyond_k_171(self):
        self.assertTrue(math.isfinite(gamma_half_integer.evaluate(k=171)))
        for k in (172, 1000, 10**9):  # the last must not try to build a huge factorial
            with self.subTest(k=k), self.assertRaises(OverflowError):
                gamma_half_integer.evaluate(k=k)

    def test_oracle_values(self):
        # mpmath gamma(k + 1/2) at 300 digits (phase-3 oracle).
        cases = (
            (2, 1.329340388179137),
            (5, 52.34277778455352),
            (20, 5.406242982335075e17),
            (50, 4.29046291235196e63),
            (100, 9.320963104082716e156),
            (150, 4.661072627097378e261),
            (170, 5.56209241456e305),
        )
        for k, expected in cases:
            with self.subTest(k=k):
                self.assertTrue(close(gamma_half_integer.evaluate(k=k), expected, 1e-14))

    def test_matches_the_double_factorial_form_in_the_source(self):
        # Mathlib: Gamma(k + 1/2) = (2k - 1)!! sqrt(pi) / 2^k, with the odd double factorial.
        for k in range(0, 30):
            double_factorial = math.prod(range(1, 2 * k, 2))  # (2k - 1)!!, empty product = 1
            expected = double_factorial / 2**k * math.sqrt(math.pi)
            with self.subTest(k=k):
                self.assertTrue(close(gamma_half_integer.evaluate(k=k), expected, 1e-14))

    def test_matches_math_gamma_and_the_recurrence(self):
        for k in range(0, 100):
            value = gamma_half_integer.evaluate(k=k)
            with self.subTest(k=k):
                self.assertTrue(close(value, math.gamma(k + 0.5), 1e-13))
        for k in range(1, 100):
            # Gamma(x + 1) = x Gamma(x) at x = k - 1/2.
            self.assertTrue(
                close(
                    gamma_half_integer.evaluate(k=k),
                    (k - 0.5) * gamma_half_integer.evaluate(k=k - 1),
                    1e-14,
                )
            )

    def test_accepts_integral_floats(self):
        self.assertEqual(gamma_half_integer.evaluate(k=3.0), gamma_half_integer.evaluate(k=3))


class GaussianIntegralTest(unittest.TestCase):
    def test_domain(self):
        for bad in (0, 0.0, -0.0, -1.0, math.nan, math.inf, -math.inf, True, "1", None):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                gaussian_integral.evaluate(b=bad)

    def test_trapezoid_rule_quadrature(self):
        # Independent route: the trapezoid rule converges geometrically for exp(-b x^2) on the
        # real line; step 0.25/sqrt(b), range +/- 9/sqrt(b) (the tail is below exp(-81)).
        for b in (0.25, 1.0, 2.0, 7.5, 1e-3, 1e4):
            h = 0.25 / math.sqrt(b)
            steps = int(9 / math.sqrt(b) / h)
            total = math.fsum(math.exp(-b * (j * h) ** 2) for j in range(-steps, steps + 1)) * h
            with self.subTest(b=b):
                self.assertTrue(close(gaussian_integral.evaluate(b=b), total, 1e-13))

    def test_oracle_quadrature_values(self):
        # mpmath.quad at 300 digits (phase-3 oracle).
        cases = (
            (0.25, 3.544907701811032),
            (2.0, 1.2533141373155003),
            (7.5, 0.6472086375185664),
            (1e-3, 56.049912163979286),
        )
        for b, expected in cases:
            with self.subTest(b=b):
                self.assertTrue(close(gaussian_integral.evaluate(b=b), expected, 1e-14))

    def test_scaling_law_and_special_values(self):
        # I(4 b) = I(b) / 2, I(1) = sqrt(pi).
        self.assertTrue(close(gaussian_integral.evaluate(b=1), math.sqrt(math.pi), 1e-15))
        for b in (1e-300, 3.3e-5, 12.5):
            with self.subTest(b=b):
                self.assertTrue(
                    close(
                        gaussian_integral.evaluate(b=4 * b),
                        gaussian_integral.evaluate(b=b) / 2,
                        1e-14,
                    )
                )

    def test_extreme_positive_values_stay_finite(self):
        smallest = gaussian_integral.evaluate(b=5e-324)
        self.assertTrue(math.isfinite(smallest) and smallest > 1e161)
        self.assertGreater(gaussian_integral.evaluate(b=1.7e308), 0.0)


class TotalProbabilityTest(unittest.TestCase):
    def evaluate(self, p_a_b, p_a_nb, p_b):
        return total_probability_two_events.evaluate(
            P_A_given_B=p_a_b, P_A_given_notB=p_a_nb, P_B=p_b
        )

    def test_conditionals_must_be_probabilities(self):
        for bad in (-0.1, 1.1, math.nan, math.inf, True, "0.5"):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                self.evaluate(bad, 0.2, 0.3)
            with self.subTest(value=bad), self.assertRaises(ValueError):
                self.evaluate(0.2, bad, 0.3)

    def test_p_b_must_be_strictly_between_zero_and_one(self):
        for bad in (0, 0.0, 1, 1.0, -0.1, 1.1, math.nan, math.inf, True, "0.5"):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                self.evaluate(0.2, 0.7, bad)

    def test_matches_exact_fraction_arithmetic(self):
        rng = random.Random(9)
        for _ in range(300):
            p_a_b, p_a_nb, p_b = (rng.random() for _ in range(3))
            if not 0 < p_b < 1:
                continue
            exact = Fraction(p_a_b) * Fraction(p_b) + Fraction(p_a_nb) * (1 - Fraction(p_b))
            with self.subTest(p_a_b=p_a_b, p_a_nb=p_a_nb, p_b=p_b):
                self.assertTrue(close(self.evaluate(p_a_b, p_a_nb, p_b), float(exact), 1e-14))

    def test_joint_table_route(self):
        # P(A) as the sum of the two joint cells containing A, in exact fractions.
        p_a_b, p_a_nb, p_b = Fraction("0.37"), Fraction("0.82"), Fraction("0.6125")
        cells = {
            ("A", "B"): p_a_b * p_b,
            ("notA", "B"): (1 - p_a_b) * p_b,
            ("A", "notB"): p_a_nb * (1 - p_b),
            ("notA", "notB"): (1 - p_a_nb) * (1 - p_b),
        }
        self.assertEqual(sum(cells.values()), 1)
        expected = float(cells[("A", "B")] + cells[("A", "notB")])
        self.assertTrue(close(self.evaluate(0.37, 0.82, 0.6125), expected, 1e-14))
        self.assertTrue(close(self.evaluate(0.9, 0.1, 0.01), 0.108, 1e-14))

    def test_result_stays_between_the_conditionals(self):
        rng = random.Random(10)
        for _ in range(500):
            p_a_b, p_a_nb, p_b = rng.random(), rng.random(), rng.random()
            if not 0 < p_b < 1:
                continue
            value = self.evaluate(p_a_b, p_a_nb, p_b)
            self.assertTrue(min(p_a_b, p_a_nb) <= value <= max(p_a_b, p_a_nb))

    def test_equal_conditionals_return_that_value_exactly(self):
        for p in (0.0, 0.3, 0.5, 0.1, 1.0):
            for p_b in (0.1, 0.3, 0.7, 1e-12, 1 - 1e-12):
                with self.subTest(p=p, p_b=p_b):
                    self.assertEqual(self.evaluate(p, p, p_b), p)

    def test_indicator_conditionals_return_p_b_and_its_complement(self):
        self.assertTrue(close(self.evaluate(1, 0, 0.25), 0.25, 1e-15))
        self.assertTrue(close(self.evaluate(0, 1, 0.25), 0.75, 1e-15))


class ExtremeScaleRegressionTest(unittest.TestCase):
    """Quadratic roots and 2x2 eigenvalues with wide ranges of scale.

    Reference values: 2000-digit mpmath roots of the exact double inputs (oracle scripts
    oracles.py and oracles3.py). Before the fix the discriminant, or the determinant, was
    converted to float directly and went subnormal or to zero.
    """

    ROOT_CASES = (
        # (a, b, c, plus, minus); the discriminant is far below max(b^2, 4ac) in the first rows.
        (1e-160, -2.000000002e-5, 1e150, 1.0000447223613393e155, 9.999552796386608e154),
        (1e-160, -2.0000000000000005e-5, 1e150, 1.0000000230856461e155, 9.999999769143545e154),
        (1.3e-156, -6.7e-5, 8.6e146, 2.7355040625237576e151, 2.4183420913223963e151),
        (1.0, -1.0, 1e-320, 1.0, 1e-320),  # subnormal root, correctly rounded
    )

    def test_roots_with_a_discriminant_far_below_the_coefficients_squared(self):
        for a, b, c, plus, minus in self.ROOT_CASES:
            with self.subTest(a=a, b=b, c=c):
                self.assertTrue(close(quadratic_root_plus.evaluate(a=a, b=b, c=c), plus, 3e-16))
                self.assertTrue(close(quadratic_root_minus.evaluate(a=a, b=b, c=c), minus, 3e-16))

    def test_representable_root_is_returned_when_the_other_root_overflows(self):
        # a = 1e-320 (subnormal), b = -1e10, c = 1: roots 1.0000111e330 and 1e-10 (mpmath).
        inputs = dict(a=1e-320, b=-1e10, c=1.0)
        self.assertTrue(close(quadratic_root_minus.evaluate(**inputs), 1e-10, 3e-16))
        with self.assertRaises(OverflowError):
            quadratic_root_plus.evaluate(**inputs)
        # a = 1e-300, b = 1e300, c = 1: roots -1e-300 and -1e600.
        inputs = dict(a=1e-300, b=1e300, c=1.0)
        self.assertTrue(close(quadratic_root_plus.evaluate(**inputs), -1e-300, 3e-16))
        with self.assertRaises(OverflowError):
            quadratic_root_minus.evaluate(**inputs)

    def test_eigenvalues_with_entry_ratios_beyond_1e150(self):
        # (matrix, larger, smaller) from mpmath; the smaller eigenvalue used to come out as 0.0
        # (first row) or 1.0000000014857302e-286 (second row).
        cases = (
            ((1e30, 0, 0, 1e-300), 1e30, 1e-300),
            ((1e-286, 0, 0, 1e30), 1e30, 1e-286),
            ((1e30, 1.0, 0, 1e-300), 1e30, 1e-300),
            ((3e300, 1e-300, 1e-300, 1e-5), 3e300, 1e-5),
        )
        for (a11, a12, a21, a22), larger, smaller in cases:
            with self.subTest(matrix=(a11, a12, a21, a22)):
                kwargs = dict(a11=a11, a12=a12, a21=a21, a22=a22)
                self.assertTrue(close(eigenvalue_2x2_larger_real.evaluate(**kwargs), larger, 3e-16))
                self.assertTrue(
                    close(eigenvalue_2x2_smaller_real.evaluate(**kwargs), smaller, 3e-16)
                )

    def test_random_wide_range_matrices_satisfy_the_exact_identities(self):
        # Independent exact check with Fractions: the returned (rounded) eigenvalues must
        # satisfy lambda^2 - trace*lambda + determinant = 0 up to their own rounding, i.e. the
        # relative residual |p(lambda)| / (lambda^2 + |trace*lambda| + |det|) stays near 1e-15.
        rng = random.Random(3)
        for _ in range(200):
            a11 = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            a22 = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            a12 = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            a21 = 0.0
            kwargs = dict(a11=a11, a12=a12, a21=a21, a22=a22)
            trace, det = Fraction(a11) + Fraction(a22), Fraction(a11) * Fraction(a22)
            for formula in (eigenvalue_2x2_larger_real, eigenvalue_2x2_smaller_real):
                try:
                    value = formula.evaluate(**kwargs)
                except OverflowError:
                    continue
                if value == 0.0 or abs(value) < 1e-290:
                    continue
                lam = Fraction(value)
                scale = lam * lam + abs(trace * lam) + abs(det)
                with self.subTest(formula=formula.id, matrix=tuple(kwargs.values())):
                    self.assertLess(abs(lam * lam - trace * lam + det) / scale, 1e-15)

    def test_triangular_matrix_eigenvalues_are_the_diagonal_entries(self):
        rng = random.Random(8)
        for _ in range(200):
            l1 = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            l2 = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            k = rng.choice((-1, 1)) * 10 ** rng.uniform(-300, 300)
            kwargs = dict(a11=l1, a12=k, a21=0.0, a22=l2)
            larger = eigenvalue_2x2_larger_real.evaluate(**kwargs)
            smaller = eigenvalue_2x2_smaller_real.evaluate(**kwargs)
            with self.subTest(matrix=tuple(kwargs.values())):
                self.assertTrue(close(larger, max(l1, l2), 3e-16), (larger, l1, l2))
                self.assertTrue(close(smaller, min(l1, l2), 3e-16), (smaller, l1, l2))


if __name__ == "__main__":
    unittest.main()

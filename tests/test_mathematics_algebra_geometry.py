"""Tests for the algebra and geometry formulas in the mathematics domain.

Extra numeric values come from independent references (exact hand arithmetic, mpmath at 50
digits with a second route such as root finding, coordinate constructions or closed forms),
never from the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog.mathematics.heron_triangle_area import heron_triangle_area
from sciengformulary.catalog.mathematics.law_of_cosines_side import law_of_cosines_side
from sciengformulary.catalog.mathematics.law_of_sines_side import law_of_sines_side
from sciengformulary.catalog.mathematics.logarithm_change_of_base import (
    logarithm_change_of_base,
)
from sciengformulary.catalog.mathematics.n_ball_volume import n_ball_volume
from sciengformulary.catalog.mathematics.quadratic_discriminant import quadratic_discriminant
from sciengformulary.catalog.mathematics.sphere_volume import sphere_volume
from sciengformulary.catalog.mathematics.triangle_median_length import triangle_median_length

NON_FINITE = (math.nan, math.inf, -math.inf)


class QuadraticDiscriminantTest(unittest.TestCase):
    formula = quadratic_discriminant

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.quadratic_discriminant")

    def test_rejects_zero_leading_coefficient(self):
        for a in (0, 0.0, -0.0):
            with self.subTest(a=a), self.assertRaises(ValueError):
                self.formula.evaluate(a=a, b=2.0, c=1.0)

    def test_rejects_non_finite_or_non_numeric(self):
        for name in ("a", "b", "c"):
            for value in (*NON_FINITE, True, "1"):
                inputs = {"a": 1.0, "b": 2.0, "c": 3.0, name: value}
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.formula.evaluate(**inputs)

    def test_independent_values(self):
        # Hand arithmetic: 7^2 - 4*3*(-2) = 73 and 1^2 - 4*1*1 = -3.
        self.assertEqual(self.formula.evaluate(a=3, b=7, c=-2), 73.0)
        self.assertEqual(self.formula.evaluate(a=1, b=1, c=1), -3.0)


class LogarithmChangeOfBaseTest(unittest.TestCase):
    formula = logarithm_change_of_base

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.logarithm_change_of_base")

    def test_rejects_non_positive_argument(self):
        for x in (0, 0.0, -1.0):
            with self.subTest(x=x), self.assertRaises(ValueError):
                self.formula.evaluate(b=2.0, x=x)

    def test_rejects_non_positive_base(self):
        for b in (0, -2.0):
            with self.subTest(b=b), self.assertRaises(ValueError):
                self.formula.evaluate(b=b, x=8.0)

    def test_rejects_base_one(self):
        for b in (1, 1.0):
            with self.subTest(b=b), self.assertRaises(ValueError):
                self.formula.evaluate(b=b, x=8.0)

    def test_rejects_non_finite(self):
        for value in NON_FINITE:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(b=value, x=8.0)
                with self.assertRaises(ValueError):
                    self.formula.evaluate(b=2.0, x=value)

    def test_independent_values(self):
        # Exact: 2^10 = 1024. mpmath 50 digits ln(50)/ln(3) = 3.5608767950073117714936...,
        # agreeing with the root of 3^y = 50.
        self.assertAlmostEqual(self.formula.evaluate(b=2, x=1024), 10.0, delta=1e-12)
        self.assertTrue(
            math.isclose(self.formula.evaluate(b=3, x=50), 3.560876795007312, rel_tol=1e-12)
        )


class LawOfCosinesSideTest(unittest.TestCase):
    formula = law_of_cosines_side

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.law_of_cosines_side")

    def test_rejects_non_positive_sides(self):
        for name in ("a", "b"):
            for value in (0.0, -1.0):
                inputs = {"a": 3.0, "b": 4.0, "gamma": 1.0, name: value}
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.formula.evaluate(**inputs)

    def test_rejects_angle_outside_open_interval(self):
        for gamma in (0.0, -0.1, math.pi, 3.2):
            with self.subTest(gamma=gamma), self.assertRaises(ValueError):
                self.formula.evaluate(a=3.0, b=4.0, gamma=gamma)

    def test_rejects_non_finite(self):
        for value in NON_FINITE:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(a=3.0, b=4.0, gamma=value)

    def test_independent_value(self):
        # mpmath 50 digits sqrt(25 + 49 - 70 cos 2) = 10.155307900713792099..., matched by the
        # distance between constructed vertices.
        self.assertTrue(
            math.isclose(
                self.formula.evaluate(a=5.0, b=7.0, gamma=2.0), 10.155307900713792, rel_tol=1e-12
            )
        )


class LawOfSinesSideTest(unittest.TestCase):
    formula = law_of_sines_side

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.law_of_sines_side")

    def test_rejects_non_positive_side(self):
        for b in (0.0, -1.0):
            with self.subTest(b=b), self.assertRaises(ValueError):
                self.formula.evaluate(b=b, alpha=1.0, beta=1.0)

    def test_rejects_angles_outside_open_interval(self):
        for name in ("alpha", "beta"):
            for value in (0.0, -0.5, math.pi, 4.0):
                inputs = {"b": 1.0, "alpha": 0.5, "beta": 0.5, name: value}
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.formula.evaluate(**inputs)

    def test_rejects_angle_sum_not_below_pi(self):
        for alpha, beta in ((2.0, 1.5), (math.pi / 2, math.pi / 2)):
            with self.subTest(alpha=alpha, beta=beta), self.assertRaises(ValueError):
                self.formula.evaluate(b=1.0, alpha=alpha, beta=beta)

    def test_rejects_non_finite(self):
        for value in NON_FINITE:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(b=value, alpha=1.0, beta=1.0)

    def test_independent_value(self):
        # mpmath 50 digits 3 sin(0.9) / sin(1.1) = 2.6368506749320991726..., matched by the
        # side length of a constructed triangle.
        self.assertTrue(
            math.isclose(
                self.formula.evaluate(b=3.0, alpha=0.9, beta=1.1), 2.636850674932099, rel_tol=1e-12
            )
        )


class TriangleSidesMixin:
    """Shared domain checks for formulas taking three side lengths a, b, c."""

    formula = None

    def test_rejects_non_positive_sides(self):
        for name in ("a", "b", "c"):
            for value in (0.0, -1.0):
                inputs = {"a": 3.0, "b": 4.0, "c": 5.0, name: value}
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.formula.evaluate(**inputs)

    def test_rejects_degenerate_triangle(self):
        # Equality in the triangle inequality: a flat triangle, excluded.
        for sides in ((1.0, 2.0, 3.0), (3.0, 1.0, 2.0), (2.0, 3.0, 1.0)):
            a, b, c = sides
            with self.subTest(sides=sides), self.assertRaises(ValueError):
                self.formula.evaluate(a=a, b=b, c=c)

    def test_rejects_impossible_triangle(self):
        for sides in ((1.0, 1.0, 5.0), (5.0, 1.0, 1.0), (1.0, 5.0, 1.0)):
            a, b, c = sides
            with self.subTest(sides=sides), self.assertRaises(ValueError):
                self.formula.evaluate(a=a, b=b, c=c)

    def test_rejects_non_finite(self):
        for value in (*NON_FINITE, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.formula.evaluate(a=value, b=4.0, c=5.0)


class HeronTriangleAreaTest(TriangleSidesMixin, unittest.TestCase):
    formula = heron_triangle_area

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.heron_triangle_area")

    def test_independent_values(self):
        # Hand arithmetic: 5-12-13 right triangle has area 5*12/2 = 30. mpmath 50 digits for
        # sides 2.5, 3.5, 4: 4.3301270189221932338... (= 2.5 sqrt(3)), matched by shoelace.
        self.assertTrue(math.isclose(self.formula.evaluate(a=5, b=12, c=13), 30.0, rel_tol=1e-12))
        self.assertTrue(
            math.isclose(
                self.formula.evaluate(a=2.5, b=3.5, c=4.0), 4.330127018922194, rel_tol=1e-12
            )
        )

    def test_symmetric_in_sides(self):
        values = {
            self.formula.evaluate(a=a, b=b, c=c)
            for a, b, c in ((7.0, 8.0, 9.0), (9.0, 7.0, 8.0), (8.0, 9.0, 7.0))
        }
        self.assertEqual(len(values), 1)


class TriangleMedianLengthTest(TriangleSidesMixin, unittest.TestCase):
    formula = triangle_median_length

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.triangle_median_length")

    def test_independent_value(self):
        # Hand arithmetic: isosceles 5-5-6, median to the base is the altitude sqrt(25 - 9) = 4;
        # radicand 2*25 + 2*25 - 36 = 64.
        self.assertTrue(
            math.isclose(self.formula.evaluate(a=6.0, b=5.0, c=5.0), 4.0, rel_tol=1e-12)
        )


class NBallVolumeTest(unittest.TestCase):
    formula = n_ball_volume

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.n_ball_volume")

    def test_rejects_dimension_below_one(self):
        for d in (0, -1):
            with self.subTest(d=d), self.assertRaises(ValueError):
                self.formula.evaluate(d=d, r=1.0)

    def test_rejects_non_integer_dimension(self):
        for d in (2.5, True, math.nan, math.inf):
            with self.subTest(d=d), self.assertRaises(ValueError):
                self.formula.evaluate(d=d, r=1.0)

    def test_rejects_negative_or_non_finite_radius(self):
        for r in (-1.0, *NON_FINITE):
            with self.subTest(r=r), self.assertRaises(ValueError):
                self.formula.evaluate(d=3, r=r)

    def test_independent_values(self):
        # mpmath 50 digits pi^(5/2) 1.5^5 / Gamma(7/2) = 39.971897824411902406..., matched by
        # the odd closed form 8 pi^2 / 15 * r^5.
        self.assertTrue(
            math.isclose(self.formula.evaluate(d=5, r=1.5), 39.971897824411904, rel_tol=1e-12)
        )

    def test_high_dimension_uses_log_space(self):
        # d = 400 is beyond math.gamma's range; mpmath 50 digits pi^200 / 200! * r^400 gives
        # 3.4126040259153335378e-276 (r = 1) and 8.8121963293787634692e-156 (r = 2), matched
        # by the even closed form. Log-space evaluation keeps about 13 significant digits.
        self.assertTrue(
            math.isclose(
                self.formula.evaluate(d=400, r=1.0), 3.4126040259153336e-276, rel_tol=1e-11
            )
        )
        self.assertTrue(
            math.isclose(self.formula.evaluate(d=400, r=2.0), 8.812196329878764e-156, rel_tol=1e-11)
        )

    def test_integral_float_dimension_accepted(self):
        # Integral floats are accepted for d, as by the shared integer check.
        self.assertTrue(
            math.isclose(self.formula.evaluate(d=3.0, r=1.0), 4.188790204786391, rel_tol=1e-12)
        )

    def test_zero_radius(self):
        for d in (1, 3, 400):
            with self.subTest(d=d):
                self.assertEqual(self.formula.evaluate(d=d, r=0.0), 0.0)


class SphereVolumeTest(unittest.TestCase):
    formula = sphere_volume

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mathematics.sphere_volume")

    def test_rejects_negative_or_non_finite_radius(self):
        for r in (-1.0, -1e-300, *NON_FINITE, True):
            with self.subTest(r=r), self.assertRaises(ValueError):
                self.formula.evaluate(r=r)

    def test_independent_value(self):
        # mpmath 50 digits 4000 pi / 3 = 4188.790204786390984..., matched by the slice integral
        # of pi (100 - z^2) over [-10, 10].
        self.assertTrue(
            math.isclose(self.formula.evaluate(r=10.0), 4188.790204786391, rel_tol=1e-12)
        )

    def test_zero_radius(self):
        self.assertEqual(self.formula.evaluate(r=0.0), 0.0)

    def test_matches_n_ball_at_three_dimensions(self):
        for r in (0.5, 1.0, 2.5):
            with self.subTest(r=r):
                self.assertTrue(
                    math.isclose(
                        self.formula.evaluate(r=r),
                        n_ball_volume.evaluate(d=3, r=r),
                        rel_tol=1e-14,
                    )
                )


if __name__ == "__main__":
    unittest.main()

"""Numerical edge cases for mathematics evaluators: extreme magnitudes and overflow.

Expected values are exact (pi/2, pi/4) or come from mpmath at 40 digits, never from the
evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog.mathematics._domain import finite, integer
from sciengformulary.catalog.mathematics.angle_between_vectors_3d import (
    angle_between_vectors_3d,
)
from sciengformulary.catalog.mathematics.binomial_probability_mass import (
    binomial_probability_mass,
)
from sciengformulary.catalog.mathematics.cramer_rule_2x2_x import cramer_rule_2x2_x
from sciengformulary.catalog.mathematics.determinant_2x2 import determinant_2x2
from sciengformulary.catalog.mathematics.geometric_probability_mass_failures import (
    geometric_probability_mass_failures,
)
from sciengformulary.catalog.mathematics.heron_triangle_area import heron_triangle_area


class AngleScaleInvarianceTest(unittest.TestCase):
    def test_tiny_orthogonal_vectors(self):
        angle = angle_between_vectors_3d.evaluate(ux=1e-200, uy=0, uz=0, vx=0, vy=1e-200, vz=0)
        self.assertTrue(math.isclose(angle, math.pi / 2, rel_tol=1e-15))

    def test_huge_vectors(self):
        angle = angle_between_vectors_3d.evaluate(ux=1e200, uy=0, uz=0, vx=1e200, vy=1e200, vz=0)
        self.assertTrue(math.isclose(angle, math.pi / 4, rel_tol=1e-15))


class SmallProbabilityTest(unittest.TestCase):
    def test_binomial_tiny_p(self):
        # mpmath: C(10, 3) * 1e-12^3 * (1 - 1e-12)^7
        value = binomial_probability_mass.evaluate(n=10, k=3, p=1e-12)
        self.assertTrue(math.isclose(value, 1.1999999999916e-34, rel_tol=1e-12))

    def test_geometric_tiny_p(self):
        # mpmath: 1e-12 * (1 - 1e-12)^(10^9)
        value = geometric_probability_mass_failures.evaluate(p=1e-12, k=10**9)
        self.assertTrue(math.isclose(value, 9.990004998333746e-13, rel_tol=1e-12))

    def test_binomial_large_n_uses_log_path(self):
        # Central term of Binomial(2e6, 1/2) is about 1 / sqrt(pi * n / 2) = 1 / sqrt(pi * 1e6).
        value = binomial_probability_mass.evaluate(n=2_000_000, k=1_000_000, p=0.5)
        self.assertTrue(math.isclose(value, 1 / math.sqrt(math.pi * 1e6), rel_tol=1e-6))


class OverflowTest(unittest.TestCase):
    def test_determinant_overflow_raises(self):
        with self.assertRaises(OverflowError):
            determinant_2x2.evaluate(a11=1e200, a12=0.0, a21=0.0, a22=1e200)

    def test_cramer_overflow_raises(self):
        with self.assertRaises(OverflowError):
            cramer_rule_2x2_x.evaluate(a11=1e-200, a12=0.0, a21=0.0, a22=1.0, b1=1e200, b2=0.0)

    def test_heron_overflow_raises(self):
        with self.assertRaises(OverflowError):
            heron_triangle_area.evaluate(a=1e300, b=1e300, c=1e300)


class DomainHelperTest(unittest.TestCase):
    def test_huge_integer_is_accepted(self):
        self.assertEqual(integer("n", 10**400, minimum=0), 10**400)
        self.assertEqual(finite("x", 10**400), 10**400)

    def test_bool_is_rejected(self):
        with self.assertRaises(ValueError):
            integer("n", True)


if __name__ == "__main__":
    unittest.main()

"""Tests for the E1 mechanics formulas (linear spring force, torque from a tangential force).

Reference values come from the independent oracle (exact rationals) and from hand
calculation. The spring law is a derived result, so it is also checked through the bar
stiffness k = A E / L of the source (a route that does not use the spring evaluator's own
form).
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.mechanics.linear_spring_force import linear_spring_force
from sciengformulary.catalog.mechanics.torque_from_tangential_force import (
    torque_from_tangential_force,
)

REL = 1e-12
NAN = math.nan
INF = math.inf


class LinearSpringForceTest(unittest.TestCase):
    formula = linear_spring_force
    base = {"k": 1000.0, "s_rel": 0.12, "s_0": 0.1}

    def assert_close(self, actual, expected, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=REL, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mechanics.linear_spring_force")

    def test_oracle_values(self):
        cases = [
            ({"k": 1000.0, "s_rel": 0.12, "s_0": 0.1}, 20.0),
            ({"k": 250.0, "s_rel": 0.08, "s_0": 0.08}, 0.0),
            ({"k": 250.0, "s_rel": 0.05, "s_0": 0.08}, -7.5),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, abs_tol=1e-9)

    def test_domain_rules(self):
        bad = [
            ("k", -1.0),
            ("k", NAN),
            ("k", INF),
            ("s_rel", NAN),
            ("s_rel", INF),
            ("s_rel", -INF),
            ("s_0", NAN),
            ("s_0", INF),
        ]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_boundary_zero_stiffness(self):
        # k = 0 is allowed (no restoring force) and gives zero force for any length.
        self.assertEqual(self.formula.evaluate(k=0.0, s_rel=5.0, s_0=1.0), 0.0)

    def test_sign_follows_extension(self):
        evaluate = self.formula.evaluate
        self.assertGreater(evaluate(k=10.0, s_rel=2.0, s_0=1.0), 0)  # stretched: tension
        self.assertLess(evaluate(k=10.0, s_rel=0.5, s_0=1.0), 0)  # compressed

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(k=1e308, s_rel=1e10, s_0=0.0)

    def test_independent_route_bar_stiffness(self):
        # A uniform bar of area A, modulus E and unstretched length L0 has stiffness
        # k = A E / L0, and its elongation under a load P is P L0 / (A E). Stretching it to a
        # length s_rel must therefore need the load P = A E (s_rel - L0) / L0 (exact Fractions).
        area, modulus, length = Fraction(3, 1000), Fraction(70_000_000), Fraction(3, 2)
        stiffness = area * modulus / length
        for stretched in (Fraction(151, 100), Fraction(3, 2), Fraction(149, 100)):
            with self.subTest(stretched=stretched):
                load = area * modulus * (stretched - length) / length
                got = self.formula.evaluate(
                    k=float(stiffness), s_rel=float(stretched), s_0=float(length)
                )
                self.assert_close(got, load, abs_tol=1e-9)


class TorqueFromTangentialForceTest(unittest.TestCase):
    formula = torque_from_tangential_force
    base = {"r": 0.3, "F": 500.0}

    def assert_close(self, actual, expected, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=REL, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def test_constructed(self):
        self.assertEqual(self.formula.id, "mechanics.torque_from_tangential_force")

    def test_oracle_values(self):
        cases = [
            ({"r": 0.3, "F": 500.0}, 150.0),
            ({"r": 0.3, "F": 0.0}, 0.0),
            ({"r": 0.05, "F": -12.5}, -0.625),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, abs_tol=1e-9)

    def test_domain_rules(self):
        bad = [("r", -0.1), ("r", NAN), ("r", INF), ("F", NAN), ("F", INF), ("F", -INF)]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_boundary_zero_arm(self):
        # r = 0: the force passes through the axis and produces no torque.
        self.assertEqual(self.formula.evaluate(r=0.0, F=123.0), 0.0)

    def test_sign_follows_force(self):
        evaluate = self.formula.evaluate
        self.assertEqual(evaluate(r=2.0, F=-3.0), -evaluate(r=2.0, F=3.0))

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(r=1e300, F=1e300)

    def test_power_balance_with_rim_speed(self):
        # Hand check of the lever relation: a rim force F moving the rim at speed v = omega r
        # delivers power F v, and the torque tau = r F acting through omega delivers tau omega.
        r, force, omega = Fraction(3, 10), Fraction(500), Fraction(8)
        torque = self.formula.evaluate(r=float(r), F=float(force))
        self.assert_close(torque * float(omega), force * (omega * r))


if __name__ == "__main__":
    unittest.main()

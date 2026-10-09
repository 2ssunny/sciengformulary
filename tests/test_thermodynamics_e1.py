"""Tests for the E1 thermodynamics formula (Antoine vapor pressure).

Reference values come from the independent oracle (50-digit mpmath arithmetic). The coefficients
are synthetic, not data for any substance. The base-10 form is also checked against the natural
logarithm form of Lienhard's equation with the converted constants.
"""

import math
import unittest

from sciengformulary.catalog.thermodynamics.antoine_vapor_pressure import antoine_vapor_pressure

REL = 1e-12
NAN = math.nan
INF = math.inf


class AntoineVaporPressureTest(unittest.TestCase):
    formula = antoine_vapor_pressure
    base = {"A": 5.0, "B": 1700.0, "C": -40.0, "T": 350.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "thermodynamics.antoine_vapor_pressure")

    def test_oracle_values(self):
        cases = [
            ({"A": 5.0, "B": 1700.0, "C": -40.0, "T": 350.0}, 0.3281927872511474),
            ({"A": 5.0, "B": 1000.0, "C": -50.0, "T": 250.0}, 1.0),
            ({"A": 4.2, "B": 1200.0, "C": 35.0, "T": 300.0}, 4.148684872471824),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                actual = self.formula.evaluate(**inputs)
                self.assertTrue(math.isclose(actual, expected, rel_tol=REL), f"got {actual!r}")

    def test_domain_rules(self):
        bad = [
            ("A", NAN),
            ("A", INF),
            ("B", NAN),
            ("B", -INF),
            ("C", NAN),
            ("C", INF),
            ("T", 0.0),
            ("T", -300.0),
            ("T", NAN),
            ("T", INF),
            ("C", -350.0),  # T + C == 0, the pole of the equation
            ("C", -350.5),  # T + C < 0, the wrong side of the pole
            ("C", -1000.0),
        ]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_wrong_side_of_pole_is_rejected(self):
        # With A = 5, B = 1700, C = -350 and T = 340, T + C = -10 and the formula would return
        # 10^(5 + 170) = 1e175, a meaningless number; it must raise instead.
        with self.assertRaises(ValueError):
            self.formula.evaluate(A=5.0, B=1700.0, C=-350.0, T=340.0)
        # A small positive T + C is accepted: T + C = 0.5 gives 10^(5 - 1 / 0.5) = 1000 by hand.
        self.assertAlmostEqual(self.formula.evaluate(A=5.0, B=1.0, C=-349.5, T=350.0), 1000.0)

    def test_non_finite_result_raises_overflow(self):
        # B / (T + C) overflows to -inf, so the exponent and the result are infinite.
        with self.assertRaises(OverflowError):
            self.formula.evaluate(A=1.0, B=-1e300, C=0.0, T=1e-300)

    def test_boundary_unit_pressure(self):
        # B / (T + C) == A makes the exponent exactly zero, so p == 1 (bar for NIST sets).
        self.assertEqual(self.formula.evaluate(A=5.0, B=1000.0, C=-50.0, T=250.0), 1.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(A=400.0, B=1.0, C=0.0, T=300.0)

    def test_underflow_raises(self):
        # 10^-400 is below the smallest float; returning 0.0 would look like a real pressure.
        with self.assertRaises(ValueError):
            self.formula.evaluate(A=-400.0, B=1.0, C=0.0, T=300.0)

    def test_pressure_rises_with_temperature_for_positive_b(self):
        evaluate = self.formula.evaluate
        values = [evaluate(A=5.0, B=1700.0, C=-40.0, T=T) for T in (320.0, 340.0, 360.0, 380.0)]
        self.assertEqual(values, sorted(values))
        self.assertGreater(values[0], 0)

    def test_independent_route_natural_log_form(self):
        # Lienhard's form is ln p = A' - B' / (C + T); with A' = A ln 10 and B' = B ln 10 it
        # reproduces the base-10 form, with C and T unchanged.
        ln10 = math.log(10.0)
        for A, B, C, T in (
            (5.0, 1700.0, -40.0, 350.0),
            (4.2, 1200.0, 35.0, 300.0),
            (3.9, 800.0, -20.0, 280.0),
            (6.1, 2200.0, -60.0, 410.0),
        ):
            with self.subTest(A=A, B=B, C=C, T=T):
                expected = math.exp(A * ln10 - (B * ln10) / (C + T))
                actual = self.formula.evaluate(A=A, B=B, C=C, T=T)
                self.assertTrue(math.isclose(actual, expected, rel_tol=1e-12), f"got {actual!r}")

    def test_clausius_clapeyron_limit_c_zero(self):
        # With C = 0 the logarithm of p is linear in 1/T: two temperatures give back B.
        A, B = 6.0, 1500.0
        p1 = self.formula.evaluate(A=A, B=B, C=0.0, T=300.0)
        p2 = self.formula.evaluate(A=A, B=B, C=0.0, T=360.0)
        slope = (math.log10(p2) - math.log10(p1)) / (1.0 / 360.0 - 1.0 / 300.0)
        self.assertTrue(math.isclose(-slope, B, rel_tol=1e-9))


if __name__ == "__main__":
    unittest.main()

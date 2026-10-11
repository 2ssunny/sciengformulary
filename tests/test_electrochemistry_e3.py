"""Tests for the E3 electrochemistry formulas (thermal voltage, Tafel current density).

Both formulas are derived results, so besides the oracle values (50-digit mpmath with the exact
SI-2019 constants) they are checked by routes that do not use the evaluator's arithmetic: exact
Fraction products of the defining constants, and the printed Tafel equations (2-20) and (2-21)
applied to the evaluator's output.
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.electrochemistry.tafel_current_density import (
    tafel_current_density,
)
from sciengformulary.catalog.electrochemistry.thermal_voltage import thermal_voltage
from sciengformulary.core import FormulaSpec

REL = 1e-12
NAN = math.nan
INF = math.inf

# Exact SI-2019 defining constants and their products, as printed by the oracle.
K_B = Fraction("1.380649e-23")
N_A = Fraction("6.02214076e23")
E_CH = Fraction("1.602176634e-19")
R_ORACLE = 8.31446261815324  # J/(mol K), N_A k_B
F_ORACLE = 96485.33212331001  # C/mol, N_A e


class _Base:
    formula: FormulaSpec
    base: dict

    def assert_close(self, actual, expected, rel=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=rel, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def assert_rejects(self, bad_inputs, error=ValueError):
        for name, value in bad_inputs:
            with self.subTest(**{name: value}):
                with self.assertRaises(error):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_references_are_well_formed(self):
        self.assertTrue(self.formula.references)
        for reference in self.formula.references:
            self.assertNotIn("openstax", (reference.url or "").lower())
            reference.format_ieee()

    def test_cites_codata_records_for_r_and_f(self):
        urls = {reference.url for reference in self.formula.references}
        self.assertIn("https://physics.nist.gov/cgi-bin/cuu/Value?r", urls)
        self.assertIn("https://physics.nist.gov/cgi-bin/cuu/Value?f", urls)


class ThermalVoltageTest(_Base, unittest.TestCase):
    formula = thermal_voltage
    base = {"T": 298.15}

    def test_id(self):
        self.assertEqual(self.formula.id, "electrochemistry.thermal_voltage")

    def test_oracle_values(self):
        for t, expected in (
            (298.15, 0.025692579121085846),
            (310.0, 0.02671373311265005),
            (1.0, 8.617333262145177e-05),
        ):
            with self.subTest(T=t):
                self.assert_close(self.formula.evaluate(T=t), expected)

    def test_domain_rules(self):
        self.assert_rejects([("T", v) for v in (0.0, -1.0, NAN, INF, -INF)])

    def test_boundary_tiny_temperature_is_proportional(self):
        self.assert_close(self.formula.evaluate(T=1e-6), 8.617333262145177e-11, rel=1e-12)

    def test_no_overflow_at_huge_temperature(self):
        # R * T alone overflows above about 2.2e307 K, but R T / F is about 8.6e-5 * T.
        for t in (1e308, 1.7e308):
            with self.subTest(T=t):
                got = self.formula.evaluate(T=t)
                self.assertTrue(math.isfinite(got))
                self.assert_close(got, K_B * Fraction(t) / E_CH)

    def test_independent_route_k_t_over_e(self):
        # R T / F = (N_A k) T / (N_A e) = k T / e with the exact defining constants.
        for t in (Fraction(5963, 20), Fraction(310), Fraction(77), Fraction(1500)):
            with self.subTest(T=t):
                self.assert_close(self.formula.evaluate(T=float(t)), K_B * t / E_CH)

    def test_independent_route_oracle_r_and_f(self):
        for t in (250.0, 298.15, 400.0):
            with self.subTest(T=t):
                self.assert_close(self.formula.evaluate(T=t), R_ORACLE * t / F_ORACLE)

    def test_exact_constants_product(self):
        self.assertEqual(float(N_A * K_B), R_ORACLE)
        self.assert_close(float(N_A * E_CH), F_ORACLE)

    def test_about_25_7_millivolt_at_room_temperature(self):
        self.assertAlmostEqual(self.formula.evaluate(T=298.15) * 1000.0, 25.7, delta=0.05)


class TafelCurrentDensityTest(_Base, unittest.TestCase):
    formula = tafel_current_density
    base = {"j0": 0.001, "alpha": 0.5, "n_e": 1.0, "eta": 0.1, "T": 298.15}

    def test_id(self):
        self.assertEqual(self.formula.id, "electrochemistry.tafel_current_density")

    def test_oracle_values(self):
        for inputs, expected in (
            (self.base, 0.0070012396400441195),
            ({"j0": 0.02, "alpha": 0.5, "n_e": 2.0, "eta": 0.0, "T": 333.15}, 0.02),
            (
                {"j0": 0.0005, "alpha": 0.3, "n_e": 2.0, "eta": 0.25, "T": 333.15},
                0.09292192950427813,
            ),
        ):
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected)

    def test_domain_rules(self):
        bad = (
            [("j0", v) for v in (0.0, -1e-3, NAN, INF)]
            + [("alpha", v) for v in (0.0, -0.5, NAN, INF)]
            + [("n_e", v) for v in (0.0, -1.0, 1.5, NAN, INF)]
            + [("eta", v) for v in (-0.01, NAN, INF, -INF)]
            + [("T", v) for v in (0.0, -300.0, NAN, INF)]
        )
        self.assert_rejects(bad)

    def test_boundary_zero_overpotential_returns_exchange_current(self):
        self.assertEqual(self.formula.evaluate(**{**self.base, "eta": 0.0}), self.base["j0"])

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(**{**self.base, "eta": 1e6})

    def test_integer_valued_float_electron_count_accepted(self):
        self.assertEqual(
            self.formula.evaluate(**{**self.base, "n_e": 1.0}),
            self.formula.evaluate(**{**self.base, "n_e": 1}),
        )

    def test_current_grows_with_overpotential_and_falls_with_temperature(self):
        low = self.formula.evaluate(**{**self.base, "eta": 0.1})
        high = self.formula.evaluate(**{**self.base, "eta": 0.2})
        hot = self.formula.evaluate(**{**self.base, "T": 400.0})
        self.assertGreater(high, low)
        self.assertLess(hot, low)

    def test_independent_route_printed_activation_polarization(self):
        # Printed eq. (2-20): eta = R T / (alpha n F) ln(j / j0). Applying it to the evaluator's
        # current density must give the overpotential back (R and F from the oracle).
        for j0, alpha, n_e, eta, t in (
            (1e-3, 0.5, 1, 0.1, 298.15),
            (5e-4, 0.3, 2, 0.25, 333.15),
            (2.0, 0.7, 4, 0.06, 353.15),
        ):
            with self.subTest(eta=eta, n_e=n_e):
                j = self.formula.evaluate(j0=j0, alpha=alpha, n_e=n_e, eta=eta, T=t)
                recovered = R_ORACLE * t / (alpha * n_e * F_ORACLE) * math.log(j / j0)
                self.assert_close(recovered, eta, rel=1e-9)

    def test_independent_route_printed_tafel_line(self):
        # Printed eq. (2-21): eta = a + b ln j with a = -(R T / (alpha n F)) ln j0 and
        # b = R T / (alpha n F), the Tafel slope. Evaluate the line at the evaluator's j.
        j0, alpha, n_e, t = 3e-4, 0.45, 2, 323.15
        b = R_ORACLE * t / (alpha * n_e * F_ORACLE)
        a = -b * math.log(j0)
        for eta in (0.08, 0.15, 0.3):
            with self.subTest(eta=eta):
                j = self.formula.evaluate(j0=j0, alpha=alpha, n_e=n_e, eta=eta, T=t)
                self.assert_close(a + b * math.log(j), eta, rel=1e-9)

    def test_independent_route_one_tafel_slope_gives_factor_e(self):
        # One Tafel slope b of extra overpotential multiplies the current density by e.
        alpha, n_e, t = 0.5, 1, 298.15
        slope = R_ORACLE * t / (alpha * n_e * F_ORACLE)
        j_a = self.formula.evaluate(j0=1e-3, alpha=alpha, n_e=n_e, eta=0.1, T=t)
        j_b = self.formula.evaluate(j0=1e-3, alpha=alpha, n_e=n_e, eta=0.1 + slope, T=t)
        self.assert_close(j_b / j_a, math.e, rel=1e-9)


if __name__ == "__main__":
    unittest.main()

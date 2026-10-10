"""Tests for the E2 rocket-equation final-mass formula.

Reference values come from the independent 50-digit oracle output (mpmath) and from hand
calculation. The formula is a derived result, so it is also checked through the inverse form
dv = u_e ln(m0 / m_f) and the propellant fraction of the source.
"""

import math
import unittest

from sciengformulary.catalog.propulsion.rocket_equation_final_mass import (
    rocket_equation_final_mass,
)

REL = 1e-12
NAN = math.nan
INF = math.inf


class RocketEquationFinalMassTest(unittest.TestCase):
    formula = rocket_equation_final_mass
    base = {"m0": 2000.0, "dv": 3000.0, "u_e": 3500.0}

    def assert_close(self, actual, expected, rel_tol=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=rel_tol, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def test_constructed(self):
        self.assertEqual(self.formula.id, "propulsion.rocket_equation_final_mass")

    def test_oracle_values(self):
        cases = [
            ({"m0": 1000.0, "dv": 0.0, "u_e": 3000.0}, 1000.0),
            ({"m0": 5000.0, "dv": 5860.0, "u_e": 29419.95}, 4096.9932273956065),
            ({"m0": 2000.0, "dv": 3000.0, "u_e": 3500.0}, 848.7456913538999),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected)

    def test_domain_rules(self):
        bad = [
            ("m0", 0.0),
            ("m0", -1.0),
            ("m0", NAN),
            ("m0", INF),
            ("dv", -1.0),
            ("dv", NAN),
            ("dv", INF),
            ("u_e", 0.0),
            ("u_e", -3000.0),
            ("u_e", NAN),
            ("u_e", INF),
        ]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_boundary_zero_delta_v(self):
        self.assertEqual(self.formula.evaluate(m0=123.0, dv=0.0, u_e=4000.0), 123.0)

    def test_boundary_underflow_raises(self):
        with self.assertRaises(ValueError):
            self.formula.evaluate(m0=1000.0, dv=800.0, u_e=1.0)

    def test_boundary_large_but_representable_ratio(self):
        self.assertGreater(self.formula.evaluate(m0=1.0, dv=700.0, u_e=1.0), 0.0)

    def test_independent_route_halving(self):
        # dv = u_e ln 2 halves the mass exactly.
        self.assert_close(
            self.formula.evaluate(m0=1000.0, dv=3000.0 * math.log(2), u_e=3000.0), 500.0
        )

    def test_independent_route_inverse_form(self):
        # u_e ln(m0 / m_f) must give back dv.
        m_f = self.formula.evaluate(**self.base)
        self.assert_close(
            self.base["u_e"] * math.log(self.base["m0"] / m_f), self.base["dv"], 1e-12
        )

    def test_independent_route_propellant_fraction(self):
        # The source's propellant fraction is 1 - exp(-dv / u_e) = 1 - m_f / m0.
        m_f = self.formula.evaluate(**self.base)
        fraction = -math.expm1(-self.base["dv"] / self.base["u_e"])
        self.assert_close(1 - m_f / self.base["m0"], fraction, 1e-12)

    def test_result_never_exceeds_initial_mass(self):
        for dv in (0.0, 1e-9, 1.0, 5e3):
            with self.subTest(dv=dv):
                self.assertLessEqual(self.formula.evaluate(m0=10.0, dv=dv, u_e=3000.0), 10.0)

    def test_scales_with_initial_mass(self):
        self.assert_close(
            self.formula.evaluate(m0=6000.0, dv=3000.0, u_e=3500.0),
            3 * self.formula.evaluate(**self.base),
        )


if __name__ == "__main__":
    unittest.main()

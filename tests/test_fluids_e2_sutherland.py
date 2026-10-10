"""Tests for the Sutherland viscosity of air (fluids.sutherland_viscosity_air).

Reference values are 50-digit mpmath evaluations of mu = beta T^(3/2) / (T + S) at the inputs
listed in each test (mpmath.mp.dps = 50) and the printed table value of the cited report, not
values from the evaluator under test.
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.fluids.sutherland_viscosity_air import sutherland_viscosity_air

BETA = 1.458e-06  # kg/(s m K^0.5), air constant of the 1976 Standard Atmosphere
S_AIR = 110.4  # K


class SutherlandViscosityAirTest(unittest.TestCase):
    formula = sutherland_viscosity_air

    def assert_close(self, actual, expected, rel_tol=1e-12):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=rel_tol),
            f"got {actual!r}, expected {expected!r}",
        )

    def test_constructed(self):
        self.assertEqual(self.formula.id, "fluids.sutherland_viscosity_air")
        self.assertTrue(self.formula.verification_cases)
        for ref in self.formula.references:
            self.assertEqual(ref.accessed, ENGINEERING_ACCESSED)
            self.assertIn("eq. (51)", ref.locator)

    def test_verification_cases_pass(self):
        self.formula.verify()

    def test_oracle(self):
        for T, expected in (
            (288.15, 1.7893802780775828e-05),
            (216.65, 1.4216130796413358e-05),
            (180.65, 1.2163172589607777e-05),
        ):
            with self.subTest(T=T):
                self.assert_close(self.formula.evaluate(T=T, beta=BETA, S=S_AIR), expected)

    def test_matches_printed_sea_level_value(self):
        # Table 10 of the cited report prints mu0 = 1.7894e-5 kg/(m s) at 288.15 K.
        got = self.formula.evaluate(T=288.15, beta=BETA, S=S_AIR)
        self.assert_close(got, 1.7894e-05, rel_tol=1e-4)

    def test_table_10_selects_s_110_4_over_110(self):
        # The cited report prints S = 110 K in Table 2B and p. 4 but 110.4 K in the text of
        # eq. (51); only 110.4 K reproduces the Table 10 value within its printed digits.
        printed = 1.7894e-05
        with_110_4 = self.formula.evaluate(T=288.15, beta=BETA, S=110.4)
        with_110 = self.formula.evaluate(T=288.15, beta=BETA, S=110.0)
        self.assertLess(abs(with_110_4 - printed) / printed, 1e-4)
        self.assertGreater(abs(with_110 - printed) / printed, 5e-4)
        text = " ".join(self.formula.assumptions)
        self.assertIn("110 K", text)

    def test_three_halves_power_form(self):
        # Independent route: T^(3/2) written with pow rather than T * sqrt(T).
        for T in (150.0, 250.0, 400.0, 1000.0):
            with self.subTest(T=T):
                expected = BETA * math.pow(T, 1.5) / (T + S_AIR)
                self.assert_close(self.formula.evaluate(T=T, beta=BETA, S=S_AIR), expected)

    def test_viscosity_of_gas_rises_with_temperature(self):
        values = [self.formula.evaluate(T=T, beta=BETA, S=S_AIR) for T in (200.0, 250.0, 300.0)]
        self.assertEqual(values, sorted(values))

    def test_constants_are_inputs_not_built_in(self):
        # Doubling beta doubles mu, and S changes it, so neither constant is fixed in the code.
        base = self.formula.evaluate(T=300.0, beta=BETA, S=S_AIR)
        self.assert_close(self.formula.evaluate(T=300.0, beta=2 * BETA, S=S_AIR), 2 * base)
        self.assertNotEqual(self.formula.evaluate(T=300.0, beta=BETA, S=120.0), base)

    def test_low_temperature_limit(self):
        # For T much less than S, mu tends to beta T^(3/2) / S.
        T = 1e-3
        self.assert_close(
            self.formula.evaluate(T=T, beta=BETA, S=S_AIR), BETA * T**1.5 / S_AIR, rel_tol=1e-4
        )

    def test_domain(self):
        base = {"T": 288.15, "beta": BETA, "S": S_AIR}
        for name in base:
            for bad in (0.0, -1.0, math.nan, math.inf):
                with self.subTest(name=name, bad=bad):
                    with self.assertRaises(ValueError):
                        self.formula.evaluate(**{**base, name: bad})

    def test_assumptions_state_constants_and_units(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("1.458e-6", text)
        self.assertIn("110.4", text)
        self.assertIn("Pa s", text)


if __name__ == "__main__":
    unittest.main()

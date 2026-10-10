"""Regression tests for the e2 review fixes of the propulsion formulas.

Expected values are 50-digit mpmath evaluations at the exact float inputs (script
`fix_oracles/oracles.py` in the review scratch directory).
"""

import math
import unittest

from sciengformulary.catalog.propulsion.burn_to_throat_area_ratio import burn_to_throat_area_ratio
from sciengformulary.catalog.propulsion.thrust_coefficient import thrust_coefficient
from sciengformulary.catalog.propulsion.tsiolkovsky_delta_v import tsiolkovsky_delta_v


class TsiolkovskyNearEqualMassesTest(unittest.TestCase):
    def test_matches_the_logarithm_near_and_away_from_unit_mass_ratio(self):
        cases = (
            (999.9999999999998, 6.821210263296963e-13),  # mf = m0 (1 - 2**-52)
            (999.999999, 2.999999993925728e-06),
            (600.0, 1532.4768712979721),
            (500.0000000000001, 2079.441541679835),
            (400.0, 2748.8721956224654),
        )
        for mf, expected in cases:
            value = tsiolkovsky_delta_v.evaluate(c=3000.0, m0=1000.0, mf=mf)
            self.assertTrue(math.isclose(value, expected, rel_tol=1e-13), f"{mf}: {value!r}")

    def test_equal_masses_give_zero(self):
        self.assertEqual(tsiolkovsky_delta_v.evaluate(c=3000.0, m0=1000.0, mf=1000.0), 0.0)


class ThrustCoefficientCriticalRatioTest(unittest.TestCase):
    CRITICAL_14 = 0.5282817877171742  # (2 / (gamma + 1))^(gamma / (gamma - 1)), gamma = 1.4

    def test_pressure_ratio_above_critical_is_rejected(self):
        for p_e in (0.9, 0.53, 0.5283):
            with self.assertRaises(ValueError):
                thrust_coefficient.evaluate(gamma=1.4, p_e=p_e, p_c=1.0, p_a=0.1, eps=1.0)

    def test_pressure_ratio_at_or_below_critical_is_accepted(self):
        # Just below the critical ratio and at a comfortable margin below it.
        thrust_coefficient.evaluate(
            gamma=1.4, p_e=self.CRITICAL_14 * (1.0 - 1e-9), p_c=1.0, p_a=0.1, eps=1.0
        )
        value = thrust_coefficient.evaluate(gamma=1.4, p_e=0.5, p_c=1.0, p_a=0.5, eps=1.0)
        self.assertTrue(math.isclose(value, 0.767892826108974, rel_tol=1e-12), repr(value))


class BurnToThroatMetadataTest(unittest.TestCase):
    def test_unverified_term_is_not_in_the_metadata(self):
        self.assertNotIn("klemmung", burn_to_throat_area_ratio.name.lower())
        self.assertNotIn("klemmung", " ".join(burn_to_throat_area_ratio.tags).lower())


class Sp125LocatorTest(unittest.TestCase):
    def test_thrust_coefficient_locator_uses_the_same_section_as_eqs_1_30_and_1_31(self):
        locators = [r.locator for r in thrust_coefficient.references]
        self.assertTrue(any(loc.startswith("sec. 1.3, eq. (1-33a)") for loc in locators), locators)


if __name__ == "__main__":
    unittest.main()

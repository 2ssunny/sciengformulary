"""Tests for the E3 chemistry formulas (air-fuel ratio and mixture fraction versus equivalence
ratio).

Reference values come from the independent oracle (exact rational arithmetic). Both relations
are derived from the definition of the equivalence ratio as a ratio of fuel-to-air mass ratios;
the tests rebuild them from explicit masses with ``fractions.Fraction``.
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.chemistry.air_fuel_ratio_from_equivalence_ratio import (
    air_fuel_ratio_from_equivalence_ratio,
)
from sciengformulary.catalog.chemistry.equivalence_ratio_from_mixture_fraction import (
    equivalence_ratio_from_mixture_fraction,
)

REL = 1e-12
NAN = math.nan
INF = math.inf


def close(actual, expected, rel=REL):
    return math.isclose(actual, expected, rel_tol=rel)


class AirFuelRatioFromEquivalenceRatioTest(unittest.TestCase):
    formula = air_fuel_ratio_from_equivalence_ratio
    base = {"AFR_st": 17.12, "phi": 0.8}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "chemistry.air_fuel_ratio_from_equivalence_ratio")

    def test_oracle_values(self):
        cases = [
            ({"AFR_st": 17.12, "phi": 0.8}, 21.4),
            ({"AFR_st": 17.12, "phi": 1.0}, 17.12),
            ({"AFR_st": 14.7, "phi": 2.0}, 7.35),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assertTrue(close(self.formula.evaluate(**inputs), expected))

    def test_domain_rules(self):
        bad = [
            ("AFR_st", 0.0),
            ("AFR_st", -14.7),
            ("AFR_st", NAN),
            ("AFR_st", INF),
            ("phi", 0.0),  # pure air: the air-fuel ratio is unbounded
            ("phi", -0.5),
            ("phi", NAN),
            ("phi", INF),
        ]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_very_lean_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(AFR_st=1e300, phi=1e-300)

    def test_stoichiometric_boundary(self):
        self.assertEqual(self.formula.evaluate(AFR_st=14.7, phi=1.0), 14.7)

    def test_matches_fuel_to_air_ratio_route(self):
        # Independent route: phi = (f/a) / (f/a)_st, so f/a = phi / AFR_st and AFR = 1 / (f/a).
        for afr_st, phi in [("17.12", "0.8"), ("14.7", "2"), ("3.5", "0.25")]:
            with self.subTest(AFR_st=afr_st, phi=phi):
                fuel_to_air = Fraction(phi) * (1 / Fraction(afr_st))
                expected = float(1 / fuel_to_air)
                actual = self.formula.evaluate(AFR_st=float(afr_st), phi=float(phi))
                self.assertTrue(close(actual, expected))


class EquivalenceRatioFromMixtureFractionTest(unittest.TestCase):
    formula = equivalence_ratio_from_mixture_fraction
    base = {"Z": 0.04, "Z_st": 0.055}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "chemistry.equivalence_ratio_from_mixture_fraction")

    def test_oracle_values(self):
        cases = [
            ({"Z": 0.04, "Z_st": 0.055}, 0.7159090909090909),
            ({"Z": 0.055, "Z_st": 0.055}, 1.0),
            ({"Z": 0.2, "Z_st": 0.0552}, 4.278985507246377),
        ]
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assertTrue(close(self.formula.evaluate(**inputs), expected))

    def test_domain_rules(self):
        bad = []
        for name in ("Z", "Z_st"):
            bad += [(name, v) for v in (0.0, 1.0, -0.1, 1.5, NAN, INF, -INF)]
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_stoichiometric_boundary(self):
        self.assertTrue(close(self.formula.evaluate(Z=0.3, Z_st=0.3), 1.0))

    def test_near_open_interval_edges_stay_finite(self):
        tiny = 1e-12
        self.assertTrue(math.isfinite(self.formula.evaluate(Z=tiny, Z_st=0.055)))
        self.assertTrue(math.isfinite(self.formula.evaluate(Z=1.0 - 1e-9, Z_st=0.055)))

    def test_matches_mass_ratio_route(self):
        # Independent route: build the fuel-to-air mass ratios from explicit stream masses and
        # divide them, then compare with the closed form.
        for z, z_st in [("0.04", "0.055"), ("0.2", "0.0552"), ("0.9", "0.5")]:
            with self.subTest(Z=z, Z_st=z_st):
                fuel, air = Fraction(z), 1 - Fraction(z)
                fuel_st, air_st = Fraction(z_st), 1 - Fraction(z_st)
                expected = float((fuel / air) / (fuel_st / air_st))
                actual = self.formula.evaluate(Z=float(z), Z_st=float(z_st))
                self.assertTrue(close(actual, expected))

    def test_composes_with_air_fuel_ratio(self):
        # Mixture of fuel and air: AFR = air mass / fuel mass = (1 - Z) / Z must equal
        # AFR_st / phi, with AFR_st = (1 - Z_st) / Z_st.
        z, z_st = 0.04, 0.055
        phi = self.formula.evaluate(Z=z, Z_st=z_st)
        afr = air_fuel_ratio_from_equivalence_ratio.evaluate(AFR_st=(1.0 - z_st) / z_st, phi=phi)
        self.assertTrue(close(afr, (1.0 - z) / z))


if __name__ == "__main__":
    unittest.main()

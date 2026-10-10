"""Regression tests for the corrected constants and reference metadata.

Expected values come from a 60-digit mpmath evaluation from the SI's exact h, k and c,
never from the catalog code under test.
"""

import math
import unittest

from sciengformulary import formulas
from sciengformulary.catalog import _constants

# 60-digit values (mpmath): sigma = 2 pi^5 k^4 / (15 h^3 c^2); b = h c / (k x), where x solves
# x = 5 (1 - exp(-x)).
SIGMA_EXACT = 5.6703744191844294e-08
WIEN_B_EXACT = 2.8977719551851727e-03
WIEN_X = 4.965114231744276


class ExactRadiationConstantsTest(unittest.TestCase):
    def test_stefan_boltzmann_is_the_exact_derived_value(self):
        self.assertEqual(_constants.STEFAN_BOLTZMANN_CONSTANT, SIGMA_EXACT)

    def test_wien_constant_is_the_exact_derived_value(self):
        self.assertEqual(_constants.WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT, WIEN_B_EXACT)

    def test_values_follow_from_the_defining_constants(self):
        h = _constants.PLANCK_CONSTANT
        k = _constants.BOLTZMANN_CONSTANT
        c = 299792458.0
        sigma = 2 * math.pi**5 * k**4 / (15 * h**3 * c**2)
        self.assertTrue(math.isclose(sigma, SIGMA_EXACT, rel_tol=1e-14))
        self.assertTrue(math.isclose(WIEN_X, 5 * (1 - math.exp(-WIEN_X)), rel_tol=1e-15))
        self.assertTrue(math.isclose(h * c / (k * WIEN_X), WIEN_B_EXACT, rel_tol=1e-14))

    def test_truncated_values_are_gone(self):
        # Versions up to 1.0.0 used the printed digits 5.670374419e-8 and 2.897771955e-3.
        self.assertNotEqual(_constants.STEFAN_BOLTZMANN_CONSTANT, 5.670374419e-8)
        self.assertNotEqual(_constants.WIEN_WAVELENGTH_DISPLACEMENT_CONSTANT, 2.897771955e-3)

    def test_blackbody_emissive_power_at_300_k(self):
        value = formulas.get("heat_transfer.blackbody_emissive_power").evaluate(T=300.0)
        self.assertTrue(math.isclose(value, 459.3003279539388, rel_tol=1e-15))

    def test_wien_peak_wavelength_at_5778_k(self):
        value = formulas.get("heat_transfer.wien_peak_wavelength").evaluate(T=5778.0)
        self.assertTrue(math.isclose(value, 5.015181646218714e-07, rel_tol=1e-15))


class ReferenceMetadataTest(unittest.TestCase):
    def test_lift_equation_page_year(self):
        # NASA Glenn "Lift Equation" page: Page Last Updated July 10, 2024.
        refs = formulas.get("aerodynamics.lift_force").references
        glenn = [r for r in refs if r.url and "lift-equation" in r.url]
        self.assertEqual([r.year for r in glenn], [2024])


if __name__ == "__main__":
    unittest.main()

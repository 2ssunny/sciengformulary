"""Tests for the e2 fluids formulas: laminar flat-plate mean skin friction and the wind power law.

Reference values are 50-digit mpmath evaluations of the cited equations at the inputs listed in
each test (mpmath.mp.dps = 50: 0.664 / sqrt(Re_x) integrated over the plate for the mean skin
friction, U_ref (z / z_ref)^alpha for the wind law) or exact hand arithmetic, rounded to a
double. None comes from the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.fluids.laminar_flat_plate_mean_skin_friction import (
    laminar_flat_plate_mean_skin_friction,
)
from sciengformulary.catalog.fluids.wind_shear_power_law import wind_shear_power_law
from sciengformulary.catalog.heat_transfer.laminar_flat_plate_skin_friction import (
    laminar_flat_plate_skin_friction,
)
from sciengformulary.core import FormulaSpec

REL = 1e-12


class _FormulaTest:
    formula: FormulaSpec
    formula_id: str

    def assert_close(self, actual, expected, rel_tol=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol),
            f"got {actual!r}, expected {expected!r}",
        )

    def assert_oracle(self, cases):
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, abs_tol=1e-15)

    def assert_rejected(self, **inputs):
        with self.subTest(**inputs):
            with self.assertRaises(ValueError):
                self.formula.evaluate(**inputs)

    def test_constructed(self):
        self.assertEqual(self.formula.id, self.formula_id)
        self.assertTrue(self.formula.references)
        self.assertTrue(self.formula.verification_cases)
        for ref in self.formula.references:
            self.assertEqual(ref.accessed, ENGINEERING_ACCESSED)

    def test_verification_cases_pass(self):
        self.formula.verify()

    def test_non_finite_inputs_rejected(self):
        base = dict(self.formula.verification_cases[0].inputs)
        for name in base:
            for bad in (math.nan, math.inf):
                with self.subTest(name=name, bad=bad):
                    with self.assertRaises(ValueError):
                        self.formula.evaluate(**{**base, name: bad})


class LaminarFlatPlateMeanSkinFrictionTest(_FormulaTest, unittest.TestCase):
    formula = laminar_flat_plate_mean_skin_friction
    formula_id = "fluids.laminar_flat_plate_mean_skin_friction"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re_L": 47619.0}, 0.006085663565733899),
                ({"Re_L": 10000.0}, 0.01328),
                ({"Re_L": 4.0}, 0.664),
                ({"Re_L": 300000.0}, 0.0024245851878895355),
            ]
        )

    def test_textbook_example_rounds(self):
        # Example 6.3 of the cited text prints C_f = 0.00609 for Re_L = 47 619.
        self.assertEqual(round(self.formula.evaluate(Re_L=47619.0), 5), 0.00609)

    def test_mean_is_twice_local_value_at_plate_end(self):
        # Independent route: integrating the local 0.664 / sqrt(Re_x) over the plate length
        # gives 2 * (local value at Re_x = Re_L); the local entry is a separate formula.
        for re in (1.0e3, 4.7619e4, 3.0e5):
            with self.subTest(Re_L=re):
                local = laminar_flat_plate_skin_friction.evaluate(Re_x=re)
                self.assert_close(self.formula.evaluate(Re_L=re), 2.0 * local)

    def test_domain_errors(self):
        for re in (0.0, -1.0, -4.7619e4):
            self.assert_rejected(Re_L=re)

    def test_boundary_tiny_reynolds_accepted(self):
        # No regime limit is enforced; only positivity is required.
        self.assert_close(self.formula.evaluate(Re_L=1e-6), 1328.0)


class WindShearPowerLawTest(_FormulaTest, unittest.TestCase):
    formula = wind_shear_power_law
    formula_id = "fluids.wind_shear_power_law"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"U_ref": 8.0, "z": 100.0, "z_ref": 10.0, "alpha": 1.0 / 7.0}, 11.115963954985101),
                ({"U_ref": 6.5, "z": 80.0, "z_ref": 50.0, "alpha": 0.2}, 7.140643531489766),
                ({"U_ref": 7.0, "z": 10.0, "z_ref": 10.0, "alpha": 0.14}, 7.0),
            ]
        )

    def test_exponent_one_is_linear_in_height(self):
        self.assert_close(self.formula.evaluate(U_ref=5.0, z=60.0, z_ref=20.0, alpha=1.0), 15.0)

    def test_zero_exponent_is_uniform(self):
        self.assertEqual(self.formula.evaluate(U_ref=5.0, z=300.0, z_ref=10.0, alpha=0.0), 5.0)

    def test_composes_between_heights(self):
        # Applying the law from z1 to z2 and then z2 to z3 equals going from z1 to z3.
        alpha = 0.22
        mid = self.formula.evaluate(U_ref=6.0, z=40.0, z_ref=10.0, alpha=alpha)
        self.assert_close(
            self.formula.evaluate(U_ref=mid, z=120.0, z_ref=40.0, alpha=alpha),
            self.formula.evaluate(U_ref=6.0, z=120.0, z_ref=10.0, alpha=alpha),
        )

    def test_negative_exponent_accepted(self):
        # The exponent is empirical; it is not restricted to a typical range.
        self.assert_close(self.formula.evaluate(U_ref=4.0, z=40.0, z_ref=10.0, alpha=-0.5), 2.0)

    def test_domain_errors(self):
        good = {"U_ref": 8.0, "z": 100.0, "z_ref": 10.0, "alpha": 0.14}
        for name, value in (
            ("U_ref", -0.1),
            ("z", 0.0),
            ("z", -10.0),
            ("z_ref", 0.0),
            ("z_ref", -10.0),
        ):
            self.assert_rejected(**{**good, name: value})

    def test_boundary_zero_reference_speed_accepted(self):
        self.assertEqual(self.formula.evaluate(U_ref=0.0, z=100.0, z_ref=10.0, alpha=0.14), 0.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(U_ref=1e300, z=1e300, z_ref=1e-300, alpha=2.0)

    def test_extreme_height_ratio_with_finite_result(self):
        # z / z_ref beyond the float range with a small exponent still has a finite result
        # (50-digit mpmath: (1e600)^1e-3 = 3.98107..., and (1e-600)^-0.5 = 1e300); the plain
        # power used to raise OverflowError or ZeroDivisionError.
        self.assert_close(
            self.formula.evaluate(U_ref=1.0, z=1e300, z_ref=1e-300, alpha=1e-3), 3.9810717055349727
        )
        self.assert_close(
            self.formula.evaluate(U_ref=1.0, z=1e-300, z_ref=1e300, alpha=-0.5), 1e300
        )

    def test_stated_dependence_matches_source_list(self):
        text = " ".join(self.formula.assumptions)
        self.assertNotIn("stability", text)
        for word in ("height", "time of day", "season", "terrain", "wind speed", "temperature"):
            self.assertIn(word, text)


if __name__ == "__main__":
    unittest.main()

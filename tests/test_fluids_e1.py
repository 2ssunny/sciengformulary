"""Tests for the e1 fluids formulas: friction factors, dimensionless groups, open-channel flow.

Reference values come from the phase-2 oracle (50-digit mpmath and exact hand arithmetic), not
from the evaluators under test. Derived formulas are also checked through an independent route
built from the source's original relations (for example the Chezy equation for Manning's
velocity, the Hagen-Poiseuille pressure drop for the laminar friction factor).
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.fluids.bond_number import bond_number
from sciengformulary.catalog.fluids.chezy_coefficient_from_manning import (
    chezy_coefficient_from_manning,
)
from sciengformulary.catalog.fluids.chezy_velocity import chezy_velocity
from sciengformulary.catalog.fluids.darcy_weisbach_pressure_drop import (
    darcy_weisbach_pressure_drop,
)
from sciengformulary.catalog.fluids.filonenko_smooth_pipe_friction_factor import (
    filonenko_smooth_pipe_friction_factor,
)
from sciengformulary.catalog.fluids.haaland_friction_factor import haaland_friction_factor
from sciengformulary.catalog.fluids.laminar_darcy_friction_factor import (
    laminar_darcy_friction_factor,
)
from sciengformulary.catalog.fluids.manning_velocity import manning_velocity
from sciengformulary.catalog.fluids.smooth_pipe_friction_factor_power_law import (
    smooth_pipe_friction_factor_power_law,
)
from sciengformulary.catalog.fluids.strouhal_number import strouhal_number
from sciengformulary.catalog.fluids.weber_number import weber_number
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


class FilonenkoTest(_FormulaTest, unittest.TestCase):
    formula = filonenko_smooth_pipe_friction_factor
    formula_id = "fluids.filonenko_smooth_pipe_friction_factor"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re": 412300.0}, 0.013584916790961722),
                ({"Re": 2300.0}, 0.04986145767700318),
                ({"Re": 5000000.0}, 0.008980905197987004),
            ]
        )

    def test_textbook_value_rounds(self):
        # Worked example on p. 372 of the cited text prints f = 0.0136.
        self.assertEqual(round(self.formula.evaluate(Re=412300.0), 4), 0.0136)

    def test_range_enforced(self):
        for re in (2299.999, 5.000001e6, 0.0, -1.0, 100.0):
            self.assert_rejected(Re=re)

    def test_boundaries_accepted(self):
        self.formula.evaluate(Re=2300.0)
        self.formula.evaluate(Re=5.0e6)


class SmoothPowerLawTest(_FormulaTest, unittest.TestCase):
    formula = smooth_pipe_friction_factor_power_law
    formula_id = "fluids.smooth_pipe_friction_factor_power_law"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re": 10000.0}, 0.02916203474128449),
                ({"Re": 100000.0}, 0.0184),
                ({"Re": 1000000.0}, 0.011609615138435557),
            ]
        )

    def test_derived_from_skin_friction_form(self):
        # Independent route: Darcy factor = 4 * C_f with C_f = 0.046 / Re^0.2 (eqs. 7.34, 7.38).
        for re in (1.0e4, 3.7e4, 2.5e5, 8.0e6):
            with self.subTest(Re=re):
                c_f = 0.046 / re**0.2
                self.assert_close(self.formula.evaluate(Re=re), 4.0 * c_f)

    def test_lower_limit_enforced(self):
        for re in (9999.999, 2300.0, 0.0, -5.0):
            self.assert_rejected(Re=re)

    def test_boundary_accepted(self):
        self.formula.evaluate(Re=10000.0)

    def test_no_upper_limit(self):
        self.formula.evaluate(Re=1.0e9)


class BondNumberTest(_FormulaTest, unittest.TestCase):
    formula = bond_number
    formula_id = "fluids.bond_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                (
                    {"g": 9.80665, "rho_l": 1000.0, "rho_g": 1.2, "L": 2.0, "sigma": 0.0589},
                    665187.2339558573,
                ),
                (
                    {"g": 9.80665, "rho_l": 1000.0, "rho_g": 0.0, "L": 0.001, "sigma": 0.072},
                    0.13620347222222223,
                ),
                (
                    {"g": 9.80665, "rho_l": 998.0, "rho_g": 1.0, "L": 0.0005, "sigma": 0.072},
                    0.03394871545138889,
                ),
            ]
        )

    def test_square_of_source_group(self):
        # Independent route: the source's group Pi_2 = L / sqrt(sigma / (g (rho_l - rho_g)))
        # is the square root of the Bond number.
        for g, rl, rg, length, sigma in (
            (9.80665, 1000.0, 1.2, 2.0, 0.0589),
            (1.62, 790.0, 3.0, 0.004, 0.022),
        ):
            with self.subTest(L=length):
                pi_2 = length / math.sqrt(sigma / (g * (rl - rg)))
                self.assert_close(
                    self.formula.evaluate(g=g, rho_l=rl, rho_g=rg, L=length, sigma=sigma),
                    pi_2**2,
                )

    def test_domain(self):
        ok = {"g": 9.8, "rho_l": 1000.0, "rho_g": 1.0, "L": 0.01, "sigma": 0.07}
        for name, bad in (
            ("g", 0.0),
            ("g", -9.8),
            ("rho_l", 0.0),
            ("rho_g", -1.0),
            ("L", 0.0),
            ("sigma", 0.0),
            ("sigma", -0.07),
            ("rho_g", 1000.0),
            ("rho_g", 2000.0),
        ):
            self.assert_rejected(**{**ok, name: bad})

    def test_equal_densities_boundary_rejected(self):
        self.assert_rejected(g=9.8, rho_l=5.0, rho_g=5.0, L=0.01, sigma=0.07)


class ChezyCoefficientTest(_FormulaTest, unittest.TestCase):
    formula = chezy_coefficient_from_manning
    formula_id = "fluids.chezy_coefficient_from_manning"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"n": 0.05, "R_h": 5.0}, 26.15320972023661),
                ({"n": 0.013, "R_h": 0.25}, 61.05388661416152),
                ({"n": 0.04, "R_h": 1.0}, 25.0),
            ]
        )

    def test_sixth_root(self):
        # Independent route: the sixth power of C n recovers the hydraulic radius.
        for n, rh in ((0.02, 3.0), (0.035, 0.4)):
            with self.subTest(n=n):
                c = self.formula.evaluate(n=n, R_h=rh)
                self.assert_close((c * n) ** 6, rh)

    def test_domain(self):
        for n, rh in ((0.0, 1.0), (-0.01, 1.0), (0.03, 0.0), (0.03, -1.0)):
            self.assert_rejected(n=n, R_h=rh)

    def test_si_only_stated(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("SI units only", text)


class ChezyVelocityTest(_FormulaTest, unittest.TestCase):
    formula = chezy_velocity
    formula_id = "fluids.chezy_velocity"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"C": 26.153, "R_h": 5.0, "S": 0.001}, 1.8492963648371776),
                ({"C": 50.0, "R_h": 2.5, "S": 0.0004}, 1.5811388300841898),
                ({"C": 26.153, "R_h": 5.0, "S": 0.0}, 0.0),
            ]
        )

    def test_squared_form(self):
        # Independent route: V^2 = C^2 R S.
        v = self.formula.evaluate(C=40.0, R_h=1.5, S=0.002)
        self.assert_close(v * v, 40.0**2 * 1.5 * 0.002)

    def test_zero_slope_boundary(self):
        self.assertEqual(self.formula.evaluate(C=40.0, R_h=1.5, S=0.0), 0.0)

    def test_domain(self):
        ok = {"C": 40.0, "R_h": 1.5, "S": 0.002}
        for name, bad in (("C", 0.0), ("C", -1.0), ("R_h", 0.0), ("R_h", -2.0), ("S", -1e-9)):
            self.assert_rejected(**{**ok, name: bad})


class ManningVelocityTest(_FormulaTest, unittest.TestCase):
    formula = manning_velocity
    formula_id = "fluids.manning_velocity"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"n": 0.03, "R_h": 0.2859, "S": 0.005236}, 1.046778195811897),
                ({"n": 0.013, "R_h": 0.5, "S": 0.001}, 1.5323923806378643),
                ({"n": 1.0, "R_h": 1.0, "S": 1.0}, 1.0),
                ({"n": 0.03, "R_h": 0.5, "S": 0.0}, 0.0),
            ]
        )

    def test_derived_from_chezy_substitution(self):
        # Independent route: the Chezy equation V = C sqrt(R S) with C = R^(1/6) / n.
        for n, rh, s in ((0.013, 0.5, 0.001), (0.045, 2.2, 0.0007), (0.03, 0.2859, 0.005236)):
            with self.subTest(n=n):
                c = rh ** (1.0 / 6.0) / n
                self.assert_close(
                    self.formula.evaluate(n=n, R_h=rh, S=s), c * math.sqrt(rh * s), rel_tol=1e-13
                )

    def test_english_constant_consistent_with_si(self):
        # The source prints V = 1.486 R^(2/3) S^(1/2) / n for feet and seconds. Converting the
        # SI evaluator output to those units must reproduce it: R in feet, V in feet per second
        # and n unchanged (the same number in s/m^(1/3)) with the constant 1 / 0.3048^(1/3).
        feet = 0.3048
        for n, r_m, s in ((0.013, 0.5, 0.001), (0.045, 2.2, 0.0007), (0.03, 0.2859, 0.005236)):
            with self.subTest(n=n):
                v_si = self.formula.evaluate(n=n, R_h=r_m, S=s)
                r_ft = r_m / feet
                v_english = 1.486 * r_ft ** (2.0 / 3.0) * math.sqrt(s) / n
                # The printed constant has four digits, so the agreement is to about 3e-4.
                self.assert_close(v_si / feet, v_english, rel_tol=3e-4)
                exact = (1.0 / feet ** (1.0 / 3.0)) * r_ft ** (2.0 / 3.0) * math.sqrt(s) / n
                self.assert_close(v_si / feet, exact, rel_tol=1e-12)

    def test_si_only_stated(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("SI units only", text)

    def test_domain(self):
        ok = {"n": 0.03, "R_h": 0.5, "S": 0.001}
        for name, bad in (("n", 0.0), ("n", -0.03), ("R_h", 0.0), ("R_h", -0.5), ("S", -1e-12)):
            self.assert_rejected(**{**ok, name: bad})


class DarcyPressureDropTest(_FormulaTest, unittest.TestCase):
    formula = darcy_weisbach_pressure_drop
    formula_id = "fluids.darcy_weisbach_pressure_drop"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"f_D": 0.018, "L": 100.0, "D": 0.3, "V": 3.0, "rho": 1000.0}, 27000.0),
                (
                    {"f_D": 0.0136, "L": 50.0, "D": 0.12, "V": 1.924, "rho": 988.0},
                    10362.504949333334,
                ),
                ({"f_D": 0.018, "L": 100.0, "D": 0.3, "V": 0.0, "rho": 1000.0}, 0.0),
            ]
        )

    def test_recovers_friction_factor_definition(self):
        # Independent route: the source's definition f = dp / ((L / D) rho V^2 / 2).
        for f, length, d, v, rho in ((0.02, 30.0, 0.05, 2.0, 998.0), (0.031, 7.0, 0.2, 0.4, 850.0)):
            with self.subTest(f=f):
                dp = self.formula.evaluate(f_D=f, L=length, D=d, V=v, rho=rho)
                self.assert_close(dp / ((length / d) * rho * v * v / 2.0), f)

    def test_domain(self):
        ok = {"f_D": 0.02, "L": 10.0, "D": 0.1, "V": 1.0, "rho": 1000.0}
        for name, bad in (
            ("f_D", 0.0),
            ("L", 0.0),
            ("D", 0.0),
            ("rho", 0.0),
            ("V", -0.1),
            ("D", -0.1),
        ):
            self.assert_rejected(**{**ok, name: bad})

    def test_zero_speed_boundary(self):
        self.assertEqual(
            self.formula.evaluate(f_D=0.02, L=10.0, D=0.1, V=0.0, rho=1000.0),
            0.0,
        )


class HaalandTest(_FormulaTest, unittest.TestCase):
    formula = haaland_friction_factor
    formula_id = "fluids.haaland_friction_factor"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re": 100000.0, "eD": 0.0001}, 0.01826505301479386),
                ({"Re": 25000.0, "eD": 0.002}, 0.028505893955530846),
                ({"Re": 4000.0, "eD": 0.05}, 0.07763488009595958),
                ({"Re": 100000000.0, "eD": 0.0}, 0.006018514872911013),
                ({"Re": 4000.0, "eD": 0.0}, 0.04042284932911364),
            ]
        )

    def test_range_enforced(self):
        for re, ed in (
            (3999.9, 0.001),
            (1.0000001e8, 0.001),
            (1.0e5, -1e-9),
            (1.0e5, 0.0500001),
            (0.0, 0.001),
        ):
            self.assert_rejected(Re=re, eD=ed)

    def test_boundaries_accepted(self):
        for re in (4000.0, 1.0e8):
            for ed in (0.0, 0.05):
                with self.subTest(Re=re, eD=ed):
                    self.formula.evaluate(Re=re, eD=ed)

    def test_rougher_pipe_has_larger_factor(self):
        smooth = self.formula.evaluate(Re=1.0e5, eD=0.0)
        rough = self.formula.evaluate(Re=1.0e5, eD=0.01)
        self.assertLess(smooth, rough)


class LaminarFrictionTest(_FormulaTest, unittest.TestCase):
    formula = laminar_darcy_friction_factor
    formula_id = "fluids.laminar_darcy_friction_factor"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re": 128.0}, 0.5),
                ({"Re": 2000.0}, 0.032),
                ({"Re": 2300.0}, 0.02782608695652174),
                ({"Re": 1.0}, 64.0),
            ]
        )

    def test_hagen_poiseuille_route(self):
        # Independent route: delta_p = 32 mu L u / D^2 (Hagen-Poiseuille) inserted in the
        # friction-factor definition f = delta_p / ((L / D) rho u^2 / 2).
        for mu, rho, u, d, length in (
            (1.0e-3, 998.0, 0.05, 0.02, 3.0),
            (0.2, 870.0, 0.3, 0.05, 9.0),
        ):
            with self.subTest(mu=mu):
                dp = 32.0 * mu * length * u / d**2
                f = dp / ((length / d) * rho * u * u / 2.0)
                re = rho * u * d / mu
                self.assert_close(self.formula.evaluate(Re=re), f)

    def test_convention_limit_enforced(self):
        for re in (2300.0000001, 5000.0, 1.0e6):
            self.assert_rejected(Re=re)

    def test_boundary_accepted(self):
        self.assertAlmostEqual(self.formula.evaluate(Re=2300.0), 64.0 / 2300.0)

    def test_domain(self):
        for re in (0.0, -10.0):
            self.assert_rejected(Re=re)

    def test_limit_documented_as_convention(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("convention", text)


class StrouhalTest(_FormulaTest, unittest.TestCase):
    formula = strouhal_number
    formula_id = "fluids.strouhal_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"f": 8.0, "L": 2.0, "V": 4.0}, 4.0),
                ({"f": 40.0, "L": 0.01, "V": 2.0}, 0.2),
                ({"f": 0.0, "L": 0.01, "V": 2.0}, 0.0),
            ]
        )

    def test_domain(self):
        ok = {"f": 10.0, "L": 0.02, "V": 3.0}
        for name, bad in (("f", -0.1), ("L", 0.0), ("L", -1.0), ("V", 0.0), ("V", -2.0)):
            self.assert_rejected(**{**ok, name: bad})

    def test_zero_frequency_boundary(self):
        self.assertEqual(self.formula.evaluate(f=0.0, L=0.02, V=3.0), 0.0)


class WeberTest(_FormulaTest, unittest.TestCase):
    formula = weber_number
    formula_id = "fluids.weber_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"rho": 900.0, "V": 0.18, "L": 0.001, "sigma": 0.01}, 2.916),
                ({"rho": 1000.0, "V": 5.0, "L": 0.002, "sigma": 0.072}, 694.4444444444445),
                ({"rho": 1000.0, "V": 0.0, "L": 0.002, "sigma": 0.072}, 0.0),
            ]
        )

    def test_mass_flux_form(self):
        # The source's second statement: G^2 L / (sigma rho) with G = rho V.
        rho, v, length, sigma = 780.0, 1.7, 0.003, 0.021
        g = rho * v
        self.assert_close(
            self.formula.evaluate(rho=rho, V=v, L=length, sigma=sigma),
            g * g * length / (sigma * rho),
        )

    def test_domain(self):
        ok = {"rho": 1000.0, "V": 1.0, "L": 0.01, "sigma": 0.07}
        for name, bad in (("rho", 0.0), ("V", -1.0), ("L", 0.0), ("sigma", 0.0), ("sigma", -0.07)):
            self.assert_rejected(**{**ok, name: bad})

    def test_zero_speed_boundary(self):
        self.assertEqual(self.formula.evaluate(rho=1000.0, V=0.0, L=0.01, sigma=0.07), 0.0)


if __name__ == "__main__":
    unittest.main()

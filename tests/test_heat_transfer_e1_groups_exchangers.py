"""Tests for the e1 heat-transfer dimensionless groups and exchanger effectiveness relations.

Reference values come from the phase-2 oracle (50-digit mpmath and exact hand arithmetic), not
from the evaluators under test. The values near the removable singularities (C_r close to 1,
C_r close to 0, NTU close to 0) were computed the same way, with 60-digit mpmath from the
published equations. Derived formulas are also checked through an independent route: the
energy balance with the log-mean temperature difference for the exchangers, the mass-flux
form of the Sherwood number, and the product forms of the Rayleigh, Peclet and Graetz numbers.
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.heat_transfer.counterflow_effectiveness import (
    counterflow_effectiveness,
)
from sciengformulary.catalog.heat_transfer.crossflow_cmax_mixed_effectiveness import (
    crossflow_cmax_mixed_effectiveness,
)
from sciengformulary.catalog.heat_transfer.crossflow_cmin_mixed_effectiveness import (
    crossflow_cmin_mixed_effectiveness,
)
from sciengformulary.catalog.heat_transfer.eckert_number import eckert_number
from sciengformulary.catalog.heat_transfer.graetz_number import graetz_number
from sciengformulary.catalog.heat_transfer.grashof_number import grashof_number
from sciengformulary.catalog.heat_transfer.jakob_number import jakob_number
from sciengformulary.catalog.heat_transfer.number_of_transfer_units import (
    number_of_transfer_units,
)
from sciengformulary.catalog.heat_transfer.parallel_flow_effectiveness import (
    parallel_flow_effectiveness,
)
from sciengformulary.catalog.heat_transfer.peclet_number import peclet_number
from sciengformulary.catalog.heat_transfer.rayleigh_number import rayleigh_number
from sciengformulary.catalog.heat_transfer.schmidt_number import schmidt_number
from sciengformulary.catalog.heat_transfer.shell_and_tube_one_shell_effectiveness import (
    shell_and_tube_one_shell_effectiveness,
)
from sciengformulary.catalog.heat_transfer.sherwood_number import sherwood_number
from sciengformulary.core import FormulaSpec

REL = 1e-12

# C_r values just below 1 (exactly representable): 1 - 2^-30, 1 - 2^-45, 1 - 2^-52.
C_NEAR_1 = (1 - 2.0**-30, 1 - 2.0**-45, 1 - 2.0**-52)


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
                abs_tol = 1e-15 if expected == 0 else 0.0
                self.assert_close(self.formula.evaluate(**inputs), expected, abs_tol=abs_tol)

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


class EckertNumberTest(_FormulaTest, unittest.TestCase):
    formula = eckert_number
    formula_id = "heat_transfer.eckert_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"u_inf": 10.0, "c_p": 2000.0, "T_w": 325.0, "T_inf": 300.0}, 0.002),
                (
                    {"u_inf": 15.0, "c_p": 1007.0, "T_w": 200.0, "T_inf": 290.0},
                    -0.0024826216484607746,
                ),
            ]
        )

    def test_sign_follows_temperature_difference(self):
        hot = self.formula.evaluate(u_inf=10.0, c_p=2000.0, T_w=325.0, T_inf=300.0)
        cold = self.formula.evaluate(u_inf=10.0, c_p=2000.0, T_w=275.0, T_inf=300.0)
        self.assertGreater(hot, 0)
        self.assert_close(cold, -hot)

    def test_speed_sign_irrelevant_and_zero_speed(self):
        a = self.formula.evaluate(u_inf=-10.0, c_p=2000.0, T_w=325.0, T_inf=300.0)
        self.assert_close(a, 0.002)
        self.assertEqual(self.formula.evaluate(u_inf=0.0, c_p=2000.0, T_w=325.0, T_inf=300.0), 0.0)

    def test_domain(self):
        self.assert_rejected(u_inf=10.0, c_p=0.0, T_w=325.0, T_inf=300.0)
        self.assert_rejected(u_inf=10.0, c_p=-5.0, T_w=325.0, T_inf=300.0)
        self.assert_rejected(u_inf=10.0, c_p=2000.0, T_w=300.0, T_inf=300.0)

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(u_inf=1e200, c_p=1.0, T_w=2.0, T_inf=1.0)


class GraetzNumberTest(_FormulaTest, unittest.TestCase):
    formula = graetz_number
    formula_id = "heat_transfer.graetz_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Re_D": 1000.0, "Pr": 7.0, "D": 0.01, "x": 0.5}, 140.0),
                ({"Re_D": 2000.0, "Pr": 0.7, "D": 0.02, "x": 0.02}, 1400.0),
            ]
        )

    def test_equivalent_velocity_form(self):
        # Independent route: with Re_D = u D / nu and Pr = nu / alpha, the group is
        # u D^2 / (x alpha).
        for u, d, x, nu, alpha in (
            (0.4, 0.025, 1.3, 1.0e-6, 1.4e-7),
            (12.0, 0.1, 0.07, 1.5e-5, 2.1e-5),
        ):
            with self.subTest(u=u, D=d, x=x):
                got = self.formula.evaluate(Re_D=u * d / nu, Pr=nu / alpha, D=d, x=x)
                self.assert_close(got, u * d * d / (x * alpha))

    def test_domain(self):
        base = {"Re_D": 1000.0, "Pr": 7.0, "D": 0.01, "x": 0.5}
        for name in base:
            for bad in (0.0, -1.0):
                self.assert_rejected(**{**base, name: bad})


class GrashofNumberTest(_FormulaTest, unittest.TestCase):
    formula = grashof_number
    formula_id = "heat_transfer.grashof_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                (
                    {
                        "g": 9.80665,
                        "beta": 0.000933,
                        "T_w": 378.2,
                        "T_inf": 200.0,
                        "L": 0.9144,
                        "nu": 1.636e-05,
                    },
                    4657491516.530312,
                ),
                (
                    {
                        "g": 9.80665,
                        "beta": 0.0033333333333333335,
                        "T_w": 280.0,
                        "T_inf": 300.0,
                        "L": 0.1,
                        "nu": 1.5e-05,
                    },
                    2905674.074074074,
                ),
                (
                    {
                        "g": 9.80665,
                        "beta": 0.0033333333333333335,
                        "T_w": 300.0,
                        "T_inf": 300.0,
                        "L": 0.1,
                        "nu": 1.5e-05,
                    },
                    0.0,
                ),
            ]
        )

    def test_absolute_temperature_difference(self):
        args = {"g": 9.80665, "beta": 3.0e-3, "L": 0.2, "nu": 1.6e-5}
        up = self.formula.evaluate(T_w=310.0, T_inf=290.0, **args)
        down = self.formula.evaluate(T_w=290.0, T_inf=310.0, **args)
        self.assertGreater(up, 0)
        self.assertEqual(up, down)

    def test_cubic_in_length(self):
        args = {"g": 9.80665, "beta": 3.0e-3, "T_w": 310.0, "T_inf": 290.0, "nu": 1.6e-5}
        small = self.formula.evaluate(L=0.1, **args)
        big = self.formula.evaluate(L=0.3, **args)
        self.assert_close(big / small, 27.0)

    def test_small_viscosity_does_not_underflow(self):
        # L^3 / nu^2 = 1e-300 / 1e-400 = 1e100, although nu^2 alone is not a float.
        got = self.formula.evaluate(g=1.0, beta=1.0, T_w=2.0, T_inf=1.0, L=1e-100, nu=1e-200)
        self.assert_close(got, 1e100)

    def test_domain(self):
        base = {"g": 9.80665, "beta": 3.0e-3, "T_w": 310.0, "T_inf": 290.0, "L": 0.2, "nu": 1.6e-5}
        for name in ("g", "beta", "L", "nu"):
            for bad in (0.0, -1.0):
                self.assert_rejected(**{**base, name: bad})

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(g=1e100, beta=1e100, T_w=1e100, T_inf=0.0, L=1e100, nu=1.0)


class JakobNumberTest(_FormulaTest, unittest.TestCase):
    formula = jakob_number
    formula_id = "heat_transfer.jakob_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"c_p": 4000.0, "T_sat": 373.15, "T_w": 363.15, "h_fg": 2000000.0}, 0.02),
                ({"c_p": 4000.0, "T_sat": 373.15, "T_w": 373.15, "h_fg": 2000000.0}, 0.0),
            ]
        )

    def test_wall_above_saturation_rejected(self):
        self.assert_rejected(c_p=4000.0, T_sat=373.15, T_w=373.16, h_fg=2000000.0)
        self.assert_rejected(c_p=4000.0, T_sat=373.15, T_w=400.0, h_fg=2000000.0)

    def test_wall_at_saturation_accepted(self):
        self.assertEqual(self.formula.evaluate(c_p=4000.0, T_sat=350.0, T_w=350.0, h_fg=1e6), 0.0)

    def test_domain(self):
        self.assert_rejected(c_p=0.0, T_sat=373.15, T_w=363.15, h_fg=2000000.0)
        self.assert_rejected(c_p=-4000.0, T_sat=373.15, T_w=363.15, h_fg=2000000.0)
        self.assert_rejected(c_p=4000.0, T_sat=373.15, T_w=363.15, h_fg=0.0)
        self.assert_rejected(c_p=4000.0, T_sat=373.15, T_w=363.15, h_fg=-1.0)


class PecletNumberTest(_FormulaTest, unittest.TestCase):
    formula = peclet_number
    formula_id = "heat_transfer.peclet_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"u": 1.5, "L": 2.0, "alpha": 1e-07}, 30000000.0),
                ({"u": 0.0, "L": 2.0, "alpha": 1e-07}, 0.0),
            ]
        )

    def test_equals_reynolds_times_prandtl(self):
        # Independent route: Re = u L / nu and Pr = nu / alpha multiply to u L / alpha.
        for u, length, nu, alpha in ((0.8, 0.05, 1.0e-6, 1.4e-7), (25.0, 1.2, 1.5e-5, 2.1e-5)):
            with self.subTest(u=u, L=length):
                re = u * length / nu
                pr = nu / alpha
                self.assert_close(self.formula.evaluate(u=u, L=length, alpha=alpha), re * pr)

    def test_domain(self):
        self.assert_rejected(u=-0.1, L=2.0, alpha=1e-07)
        for bad in (0.0, -1.0):
            self.assert_rejected(u=1.5, L=bad, alpha=1e-07)
            self.assert_rejected(u=1.5, L=2.0, alpha=bad)


class RayleighNumberTest(_FormulaTest, unittest.TestCase):
    formula = rayleigh_number
    formula_id = "heat_transfer.rayleigh_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"Gr_L": 4600000000.0, "Pr": 1.2}, 5520000000.0),
                ({"Gr_L": 0.0, "Pr": 0.7}, 0.0),
            ]
        )

    def test_matches_buoyancy_form(self):
        # Independent route from the source's equivalent form g beta dT L^3 / (alpha nu), with
        # alpha = nu / Pr, against the product of the Grashof formula and Pr.
        g, beta, dt, length, nu, pr = 9.80665, 3.1e-3, 22.0, 0.35, 1.6e-5, 0.71
        alpha = nu / pr
        gr = grashof_number.evaluate(g=g, beta=beta, T_w=300.0 + dt, T_inf=300.0, L=length, nu=nu)
        self.assert_close(
            self.formula.evaluate(Gr_L=gr, Pr=pr), g * beta * dt * length**3 / (alpha * nu)
        )

    def test_domain(self):
        self.assert_rejected(Gr_L=-1.0, Pr=0.7)
        self.assert_rejected(Gr_L=1e9, Pr=0.0)
        self.assert_rejected(Gr_L=1e9, Pr=-0.7)


class SchmidtNumberTest(_FormulaTest, unittest.TestCase):
    formula = schmidt_number
    formula_id = "heat_transfer.schmidt_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"nu": 6e-07, "D_AB": 1e-09}, 600.0),
                ({"nu": 1.5e-05, "D_AB": 2.5e-05}, 0.6),
            ]
        )

    def test_equal_diffusivities_give_one(self):
        self.assertEqual(self.formula.evaluate(nu=2.3e-5, D_AB=2.3e-5), 1.0)

    def test_domain(self):
        for bad in (0.0, -1e-6):
            self.assert_rejected(nu=bad, D_AB=1e-9)
            self.assert_rejected(nu=6e-7, D_AB=bad)

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(nu=1e300, D_AB=1e-300)


class SherwoodNumberTest(_FormulaTest, unittest.TestCase):
    formula = sherwood_number
    formula_id = "heat_transfer.sherwood_number"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"k_m": 0.01, "L": 0.05, "D_AB": 2e-05}, 25.0),
                ({"k_m": 0.0, "L": 0.05, "D_AB": 2e-05}, 0.0),
            ]
        )

    def test_derived_from_mass_flux_coefficient(self):
        # Independent route from the source's form: Sh = g_m L / (rho D_AB), where the mass-flux
        # coefficient g_m [kg/(m^2 s)] relates to the velocity-form coefficient by k_m = g_m / rho.
        for g_m, rho, length, d_ab in ((0.012, 1.2, 0.05, 2.0e-5), (0.4, 998.0, 0.01, 1.1e-9)):
            with self.subTest(g_m=g_m, rho=rho):
                got = self.formula.evaluate(k_m=g_m / rho, L=length, D_AB=d_ab)
                self.assert_close(got, g_m * length / (rho * d_ab))

    def test_domain(self):
        self.assert_rejected(k_m=-0.01, L=0.05, D_AB=2e-05)
        for bad in (0.0, -1.0):
            self.assert_rejected(k_m=0.01, L=bad, D_AB=2e-05)
            self.assert_rejected(k_m=0.01, L=0.05, D_AB=bad)


class NumberOfTransferUnitsTest(_FormulaTest, unittest.TestCase):
    formula = number_of_transfer_units
    formula_id = "heat_transfer.number_of_transfer_units"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"U": 500.0, "A": 30.0, "C_min": 10000.0}, 1.5),
                ({"U": 25.0, "A": 0.4, "C_min": 1000.0}, 0.01),
            ]
        )

    def test_zero_area_or_conductance_gives_zero(self):
        self.assertEqual(self.formula.evaluate(U=0.0, A=30.0, C_min=10000.0), 0.0)
        self.assertEqual(self.formula.evaluate(U=500.0, A=0.0, C_min=10000.0), 0.0)

    def test_domain(self):
        self.assert_rejected(U=-1.0, A=30.0, C_min=10000.0)
        self.assert_rejected(U=500.0, A=-1.0, C_min=10000.0)
        self.assert_rejected(U=500.0, A=30.0, C_min=0.0)
        self.assert_rejected(U=500.0, A=30.0, C_min=-10000.0)


class _EffectivenessTest(_FormulaTest):
    """Checks shared by the single-pass effectiveness-NTU relations."""

    def test_range_enforced(self):
        for bad_ntu in (-1e-9, -1.0):
            self.assert_rejected(NTU=bad_ntu, C_r=0.5)
        for bad_cr in (-1e-9, 1.0000000000000002, 2.0):
            self.assert_rejected(NTU=1.0, C_r=bad_cr)

    def test_zero_ntu_gives_zero(self):
        for c_r in (0.5, 1.0):
            with self.subTest(C_r=c_r):
                self.assertEqual(self.formula.evaluate(NTU=0.0, C_r=c_r), 0.0)

    def test_large_ntu_approaches_limit(self):
        got = self.formula.evaluate(NTU=1e6, C_r=0.5)
        self.assertTrue(0.0 < got <= 1.0)
        self.assertEqual(self.formula.evaluate(NTU=1e300, C_r=0.5), got)

    def test_monotonic_in_ntu(self):
        values = [self.formula.evaluate(NTU=n, C_r=0.6) for n in (0.1, 0.5, 1.0, 2.0, 5.0)]
        self.assertEqual(values, sorted(values))

    def _lmtd_balance_residual(self, ntu, c_r, counterflow):
        # Independent route: the effectiveness fixes the outlet temperatures through the energy
        # balance, and the heat rate must then equal U A times the log-mean temperature
        # difference. The hot stream is the C_min stream.
        c_min = 1000.0
        c_h, c_c = c_min, c_min / c_r
        th_in, tc_in = 400.0, 300.0
        eps = self.formula.evaluate(NTU=ntu, C_r=c_r)
        q = eps * c_min * (th_in - tc_in)
        th_out = th_in - q / c_h
        tc_out = tc_in + q / c_c
        if counterflow:
            d_a, d_b = th_in - tc_out, th_out - tc_in
        else:
            d_a, d_b = th_in - tc_in, th_out - tc_out
        lmtd = (d_a - d_b) / math.log(d_a / d_b)
        return q, ntu * c_min * lmtd


class ParallelFlowEffectivenessTest(_EffectivenessTest, unittest.TestCase):
    formula = parallel_flow_effectiveness
    formula_id = "heat_transfer.parallel_flow_effectiveness"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"NTU": 1.5, "C_r": 0.5}, 0.5964005169587571),
                ({"NTU": 5.0, "C_r": 0.7}, 0.5881156068417585),
                ({"NTU": 2.0, "C_r": 1.0}, 0.4908421805556329),
                ({"NTU": 0.0, "C_r": 0.5}, 0.0),
                ({"NTU": 1e-8, "C_r": 0.5}, 9.999999925e-09),
                ({"NTU": 1e-12, "C_r": 0.5}, 9.9999999999925e-13),
            ]
        )

    def test_textbook_example_rounds(self):
        # The worked example in the cited section prints 0.596.
        self.assertEqual(round(self.formula.evaluate(NTU=1.5, C_r=0.5), 3), 0.596)

    def test_c_r_zero_is_constant_temperature_stream(self):
        self.assert_close(self.formula.evaluate(NTU=1.5, C_r=0.0), -math.expm1(-1.5))

    def test_large_ntu_limit(self):
        self.assert_close(self.formula.evaluate(NTU=1e3, C_r=0.5), 1 / 1.5)

    def test_energy_balance_with_lmtd(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (2.0, 1.0), (0.3, 0.2)):
            with self.subTest(NTU=ntu, C_r=c_r):
                q, q_lmtd = self._lmtd_balance_residual(ntu, c_r, counterflow=False)
                self.assert_close(q, q_lmtd, rel_tol=1e-10)


class CounterflowEffectivenessTest(_EffectivenessTest, unittest.TestCase):
    formula = counterflow_effectiveness
    formula_id = "heat_transfer.counterflow_effectiveness"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"NTU": 5.0, "C_r": 0.7}, 0.9206703686051108),
                ({"NTU": 5.0, "C_r": 1.0}, 0.8333333333333334),
                ({"NTU": 1.5, "C_r": 0.0}, 0.7768698398515702),
                ({"NTU": 1e-8, "C_r": 0.7}, 9.999999915e-09),
                ({"NTU": 1e-12, "C_r": 0.7}, 9.9999999999915e-13),
            ]
        )

    def test_balanced_limit_exact_fraction(self):
        for ntu in (Fraction(5), Fraction(1, 2), Fraction(3, 1000)):
            with self.subTest(NTU=ntu):
                expected = float(ntu / (1 + ntu))
                self.assert_close(self.formula.evaluate(NTU=float(ntu), C_r=1.0), expected)

    def test_values_just_below_one_match_oracle(self):
        # 60-digit mpmath values of the stated form at C_r just below 1.
        expected = {
            5.0: (0.8333333336567093, 0.8333333333333433, 0.8333333333333334),
            0.5: (0.3333333333850735, 0.3333333333333349, 0.33333333333333337),
        }
        for ntu, values in expected.items():
            for c_r, value in zip(C_NEAR_1, values):
                with self.subTest(NTU=ntu, C_r=c_r):
                    self.assert_close(self.formula.evaluate(NTU=ntu, C_r=c_r), value)

    def test_continuous_at_one(self):
        for ntu in (0.5, 5.0, 40.0):
            limit = self.formula.evaluate(NTU=ntu, C_r=1.0)
            for c_r in C_NEAR_1:
                with self.subTest(NTU=ntu, C_r=c_r):
                    self.assert_close(self.formula.evaluate(NTU=ntu, C_r=c_r), limit, rel_tol=1e-8)

    def test_balanced_limit_from_energy_balance(self):
        # Independent route for the derived branch: with equal capacity rates the temperature
        # difference between the streams is uniform along a counterflow exchanger, so
        # Q = U A dT with dT = T_h,in - T_c,out. In effectiveness terms eps = NTU * (1 - eps).
        for ntu in (0.01, 0.5, 5.0, 123.0):
            with self.subTest(NTU=ntu):
                eps = self.formula.evaluate(NTU=ntu, C_r=1.0)
                self.assert_close(eps, ntu * (1 - eps))

    def test_c_r_zero_is_constant_temperature_stream(self):
        self.assert_close(self.formula.evaluate(NTU=1.5, C_r=0.0), -math.expm1(-1.5))

    def test_large_ntu_limits(self):
        self.assertEqual(self.formula.evaluate(NTU=1e3, C_r=0.7), 1.0)
        self.assert_close(self.formula.evaluate(NTU=1e9, C_r=1.0), 1.0, rel_tol=1e-8)

    def test_energy_balance_with_lmtd(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (0.3, 0.2), (2.0, 0.999)):
            with self.subTest(NTU=ntu, C_r=c_r):
                q, q_lmtd = self._lmtd_balance_residual(ntu, c_r, counterflow=True)
                self.assert_close(q, q_lmtd, rel_tol=1e-9)

    def test_exceeds_parallel_flow(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (2.0, 1.0)):
            with self.subTest(NTU=ntu, C_r=c_r):
                self.assertGreater(
                    self.formula.evaluate(NTU=ntu, C_r=c_r),
                    parallel_flow_effectiveness.evaluate(NTU=ntu, C_r=c_r),
                )


class CrossflowCmaxMixedEffectivenessTest(_EffectivenessTest, unittest.TestCase):
    formula = crossflow_cmax_mixed_effectiveness
    formula_id = "heat_transfer.crossflow_cmax_mixed_effectiveness"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"NTU": 5.0, "C_r": 0.7}, 0.7158099831204696),
                ({"NTU": 1.0, "C_r": 1.0}, 0.4685363946133843),
                ({"NTU": 1.0, "C_r": 1e-3}, 0.6319208127182021),
                ({"NTU": 1.0, "C_r": 1e-8}, 0.6321205568306757),
                ({"NTU": 1.0, "C_r": 1e-12}, 0.6321205588283579),
            ]
        )

    def test_zero_c_r_is_outside_range(self):
        self.assert_rejected(NTU=1.0, C_r=0.0)

    def test_tiny_c_r_is_stable(self):
        # As C_r tends to 0 the result tends to 1 - exp(-NTU), the constant-temperature limit.
        self.assert_close(
            self.formula.evaluate(NTU=1.0, C_r=1e-300), 0.6321205588285577, rel_tol=1e-12
        )
        self.assertTrue(0.0 < self.formula.evaluate(NTU=1.0, C_r=5e-324) < 1.0)

    def test_equals_cmin_mixed_at_balanced_flow(self):
        # Both mixed-stream assignments coincide when the capacity rates are equal.
        for ntu in (0.2, 1.0, 5.0):
            with self.subTest(NTU=ntu):
                self.assert_close(
                    self.formula.evaluate(NTU=ntu, C_r=1.0),
                    crossflow_cmin_mixed_effectiveness.evaluate(NTU=ntu, C_r=1.0),
                )

    def test_between_parallel_and_counterflow(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (2.0, 1.0)):
            with self.subTest(NTU=ntu, C_r=c_r):
                value = self.formula.evaluate(NTU=ntu, C_r=c_r)
                self.assertGreater(value, parallel_flow_effectiveness.evaluate(NTU=ntu, C_r=c_r))
                self.assertLess(value, counterflow_effectiveness.evaluate(NTU=ntu, C_r=c_r))


class CrossflowCminMixedEffectivenessTest(_EffectivenessTest, unittest.TestCase):
    formula = crossflow_cmin_mixed_effectiveness
    formula_id = "heat_transfer.crossflow_cmin_mixed_effectiveness"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"NTU": 5.0, "C_r": 0.7}, 0.7497843941508544),
                ({"NTU": 1.0, "C_r": 1.0}, 0.4685363946133843),
                ({"NTU": 1.0, "C_r": 0.0}, 0.6321205588285577),
                ({"NTU": 5.0, "C_r": 0.0}, 0.9932620530009145),
                ({"NTU": 1.0, "C_r": 1e-3}, 0.6319366344439432),
                ({"NTU": 1.0, "C_r": 1e-8}, 0.6321205569891605),
                ({"NTU": 1.0, "C_r": 1e-12}, 0.6321205588283737),
                ({"NTU": 5.0, "C_r": 1e-3}, 0.9931774420217113),
                ({"NTU": 5.0, "C_r": 1e-8}, 0.9932620521586711),
                ({"NTU": 5.0, "C_r": 1e-12}, 0.9932620530008303),
            ]
        )

    def test_zero_c_r_limit_is_constant_temperature_stream(self):
        # Independent route for the derived branch: a stream at constant temperature has
        # eps = 1 - exp(-NTU), and small C_r approaches it continuously.
        for ntu in (0.01, 1.0, 5.0, 30.0):
            with self.subTest(NTU=ntu):
                limit = self.formula.evaluate(NTU=ntu, C_r=0.0)
                self.assert_close(limit, -math.expm1(-ntu))
                self.assert_close(self.formula.evaluate(NTU=ntu, C_r=1e-10), limit, rel_tol=1e-8)

    def test_tiny_c_r_does_not_underflow(self):
        # NTU * C_r underflows to 0 here; the result must still be the limit, not 0.
        self.assert_close(self.formula.evaluate(NTU=0.5, C_r=5e-324), -math.expm1(-0.5))

    def test_between_parallel_and_counterflow(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (2.0, 1.0)):
            with self.subTest(NTU=ntu, C_r=c_r):
                value = self.formula.evaluate(NTU=ntu, C_r=c_r)
                self.assertGreater(value, parallel_flow_effectiveness.evaluate(NTU=ntu, C_r=c_r))
                self.assertLess(value, counterflow_effectiveness.evaluate(NTU=ntu, C_r=c_r))


class ShellAndTubeOneShellEffectivenessTest(_EffectivenessTest, unittest.TestCase):
    formula = shell_and_tube_one_shell_effectiveness
    formula_id = "heat_transfer.shell_and_tube_one_shell_effectiveness"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"NTU": 5.0, "C_r": 0.7}, 0.6834977044311439),
                ({"NTU": 1.0, "C_r": 0.0}, 0.6321205588285577),
                ({"NTU": 2.0, "C_r": 1.0}, 0.5568096679436695),
                ({"NTU": 1e-3, "C_r": 0.0}, 0.0009995001666250085),
                ({"NTU": 1e-8, "C_r": 0.0}, 9.999999950000001e-09),
                ({"NTU": 1e-12, "C_r": 0.0}, 9.999999999995e-13),
                ({"NTU": 1e-3, "C_r": 0.7}, 0.0009991505979305628),
                ({"NTU": 1e-8, "C_r": 0.7}, 9.999999915e-09),
                ({"NTU": 1e-12, "C_r": 0.7}, 9.9999999999915e-13),
                ({"NTU": 1e-3, "C_r": 1.0}, 0.0009990008326671996),
                ({"NTU": 1e-8, "C_r": 1.0}, 9.999999900000002e-09),
                ({"NTU": 1e-12, "C_r": 1.0}, 9.99999999999e-13),
            ]
        )

    def test_matches_exponential_form(self):
        # Independent route: the exponential form printed in the equation field, written with
        # math.exp, equals the tanh form the evaluator uses.
        for ntu in (0.05, 0.7, 2.0, 9.0):
            for c_r in (0.0, 0.3, 0.7, 1.0):
                with self.subTest(NTU=ntu, C_r=c_r):
                    s = math.sqrt(1 + c_r**2)
                    e = math.exp(-ntu * s)
                    expected = 2 / (1 + c_r + s * (1 + e) / (1 - e))
                    self.assert_close(self.formula.evaluate(NTU=ntu, C_r=c_r), expected)

    def test_zero_ntu_limit_from_small_ntu(self):
        # Independent route for the derived NTU = 0 branch: eps tends to 0 as NTU tends to 0
        # and is close to NTU * (1 - O(NTU)) for small values.
        for c_r in (0.0, 0.7, 1.0):
            with self.subTest(C_r=c_r):
                self.assertEqual(self.formula.evaluate(NTU=0.0, C_r=c_r), 0.0)
                self.assert_close(self.formula.evaluate(NTU=1e-12, C_r=c_r), 1e-12, rel_tol=1e-9)

    def test_denormal_ntu_does_not_divide_by_zero(self):
        value = self.formula.evaluate(NTU=5e-324, C_r=0.5)
        self.assertTrue(0.0 <= value <= 1e-300)

    def test_large_ntu_limit(self):
        # As NTU grows, tanh tends to 1 and eps tends to 2 / (1 + C_r + sqrt(1 + C_r^2)).
        for c_r in (0.0, 0.5, 1.0):
            with self.subTest(C_r=c_r):
                limit = 2 / (1 + c_r + math.sqrt(1 + c_r**2))
                self.assert_close(self.formula.evaluate(NTU=1e3, C_r=c_r), limit)

    def test_between_parallel_and_counterflow(self):
        for ntu, c_r in ((1.5, 0.5), (5.0, 0.7), (2.0, 1.0)):
            with self.subTest(NTU=ntu, C_r=c_r):
                value = self.formula.evaluate(NTU=ntu, C_r=c_r)
                self.assertGreater(value, parallel_flow_effectiveness.evaluate(NTU=ntu, C_r=c_r))
                self.assertLess(value, counterflow_effectiveness.evaluate(NTU=ntu, C_r=c_r))


if __name__ == "__main__":
    unittest.main()

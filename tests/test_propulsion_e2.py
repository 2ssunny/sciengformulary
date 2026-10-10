"""Tests for the e2 propulsion formulas: impulse relations, solid-motor ballistics, nozzle
performance and the rocket equation.

Reference values come from the phase-2 oracle (50-digit mpmath and exact hand arithmetic), not
from the evaluators under test. Derived formulas are also checked through an independent route
built from the source's original relations (the printed mass balance, the exit Mach number and
area-Mach relation, the product of exit velocity and mass-flow terms, the printed mass ratio).
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.propulsion.average_thrust import average_thrust
from sciengformulary.catalog.propulsion.burn_to_throat_area_ratio import burn_to_throat_area_ratio
from sciengformulary.catalog.propulsion.effective_exhaust_velocity import (
    effective_exhaust_velocity,
)
from sciengformulary.catalog.propulsion.effective_exhaust_velocity_from_impulse import (
    effective_exhaust_velocity_from_impulse,
)
from sciengformulary.catalog.propulsion.nozzle_expansion_ratio import nozzle_expansion_ratio
from sciengformulary.catalog.propulsion.regression_rate_from_mass_flow import (
    regression_rate_from_mass_flow,
)
from sciengformulary.catalog.propulsion.specific_impulse import specific_impulse
from sciengformulary.catalog.propulsion.thrust_coefficient import thrust_coefficient
from sciengformulary.catalog.propulsion.thrust_to_weight_ratio import thrust_to_weight_ratio
from sciengformulary.catalog.propulsion.tsiolkovsky_delta_v import tsiolkovsky_delta_v
from sciengformulary.core import FormulaSpec

REL = 1e-12
G0 = 9.80665


class _FormulaTest:
    formula: FormulaSpec
    formula_id: str

    def assert_close(self, actual, expected, rel_tol=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol),
            f"got {actual!r}, expected {expected!r}",
        )

    def assert_oracle(self, cases, rel_tol=REL):
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, rel_tol, 1e-15)

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


class EffectiveExhaustVelocityTest(_FormulaTest, unittest.TestCase):
    formula = effective_exhaust_velocity
    formula_id = "propulsion.effective_exhaust_velocity"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"I_sp": 300.0, "g0": G0}, 2941.995),
                ({"I_sp": 450.0, "g0": G0}, 4412.9925),
                ({"I_sp": 1.0, "g0": G0}, 9.80665),
            ]
        )

    def test_inverse_of_specific_impulse(self):
        # Independent route: F = mdot * v_e, so the existing I_sp = F / (mdot * g0) of the
        # catalog must return the specific impulse that was fed in.
        for isp in (1.0, 85.0, 300.0, 452.3):
            with self.subTest(I_sp=isp):
                v_e = self.formula.evaluate(I_sp=isp, g0=G0)
                mdot = 7.5
                self.assert_close(specific_impulse.evaluate(F=mdot * v_e, mdot=mdot), isp)

    def test_domain_errors(self):
        for isp, g0 in ((0.0, G0), (-1.0, G0), (300.0, 0.0), (300.0, -9.8)):
            self.assert_rejected(I_sp=isp, g0=g0)

    def test_boundary_just_above_zero_accepted(self):
        self.assert_close(self.formula.evaluate(I_sp=1e-300, g0=G0), 1e-300 * G0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(I_sp=1e308, g0=1e10)


class EffectiveExhaustVelocityFromImpulseTest(_FormulaTest, unittest.TestCase):
    formula = effective_exhaust_velocity_from_impulse
    formula_id = "propulsion.effective_exhaust_velocity_from_impulse"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"I_t": 2500000.0, "m_p": 1000.0}, 2500.0),
                ({"I_t": 3000.0, "m_p": 1.2}, 2500.0),
                ({"I_t": 9806.65, "m_p": 1.0}, 9806.65),
            ]
        )

    def test_consistent_with_specific_impulse_route(self):
        # I_t = F * t and m_p = mdot * t, so the result must equal g0 * I_sp for constant F.
        force, mdot, burn = 31500.0, 12.0, 41.0
        isp = specific_impulse.evaluate(F=force, mdot=mdot)
        self.assert_close(
            self.formula.evaluate(I_t=force * burn, m_p=mdot * burn),
            effective_exhaust_velocity.evaluate(I_sp=isp, g0=G0),
        )

    def test_domain_errors(self):
        for i_t, m_p in ((0.0, 1.0), (-5.0, 1.0), (1.0, 0.0), (1.0, -1.0)):
            self.assert_rejected(I_t=i_t, m_p=m_p)

    def test_boundary_tiny_mass_accepted(self):
        self.assert_close(self.formula.evaluate(I_t=1.0, m_p=1e-9), 1e9)


class AverageThrustTest(_FormulaTest, unittest.TestCase):
    formula = average_thrust
    formula_id = "propulsion.average_thrust"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"I_t": 10000.0, "t_b": 5.0}, 2000.0),
                ({"I_t": 2000000.0, "t_b": 80.0}, 25000.0),
                ({"I_t": 1.0, "t_b": 0.001}, 1000.0),
            ]
        )

    def test_constant_thrust_returns_thrust(self):
        # For a constant thrust F over time t the impulse is F * t, so the average is F.
        for force, burn in ((100.0, 3.0), (4.5e5, 120.0)):
            with self.subTest(F=force):
                self.assert_close(self.formula.evaluate(I_t=force * burn, t_b=burn), force)

    def test_domain_errors(self):
        for i_t, t_b in ((0.0, 1.0), (-1.0, 1.0), (1.0, 0.0), (1.0, -2.0)):
            self.assert_rejected(I_t=i_t, t_b=t_b)

    def test_boundary_short_burn_accepted(self):
        self.assert_close(self.formula.evaluate(I_t=1.0, t_b=1e-6), 1e6)


class ThrustToWeightRatioTest(_FormulaTest, unittest.TestCase):
    formula = thrust_to_weight_ratio
    formula_id = "propulsion.thrust_to_weight_ratio"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"F": 34000.0, "m": 1000.0, "g0": G0}, 3.467035124124956),
                ({"F": 9806.65, "m": 1000.0, "g0": G0}, 1.0),
                ({"F": 1200000.0, "m": 50000.0, "g0": G0}, 2.4473189111470277),
            ]
        )

    def test_acceleration_over_gravity_for_force_balance(self):
        # Independent route: with no other force, a = F / m and F/W = a / g0.
        force, mass = 85000.0, 4300.0
        accel = force / mass
        self.assert_close(self.formula.evaluate(F=force, m=mass, g0=G0), accel / G0)

    def test_domain_errors(self):
        for force, mass, g0 in (
            (0.0, 1.0, G0),
            (-1.0, 1.0, G0),
            (1.0, 0.0, G0),
            (1.0, -1.0, G0),
            (1.0, 1.0, 0.0),
            (1.0, 1.0, -9.8),
        ):
            self.assert_rejected(F=force, m=mass, g0=g0)

    def test_boundary_unity(self):
        self.assert_close(self.formula.evaluate(F=G0, m=1.0, g0=G0), 1.0)


class BurnToThroatAreaRatioTest(_FormulaTest, unittest.TestCase):
    formula = burn_to_throat_area_ratio
    formula_id = "propulsion.burn_to_throat_area_ratio"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"A_b": 0.5, "A_t": 0.001}, 500.0),
                ({"A_b": 0.01, "A_t": 0.01}, 1.0),
                ({"A_b": 0.123, "A_t": 0.00041}, 300.0),
            ]
        )

    def test_domain_errors(self):
        for a_b, a_t in ((0.0, 1.0), (-1.0, 1.0), (1.0, 0.0), (1.0, -1.0)):
            self.assert_rejected(A_b=a_b, A_t=a_t)

    def test_boundary_equal_areas(self):
        self.assertEqual(self.formula.evaluate(A_b=2.5, A_t=2.5), 1.0)


class RegressionRateFromMassFlowTest(_FormulaTest, unittest.TestCase):
    formula = regression_rate_from_mass_flow
    formula_id = "propulsion.regression_rate_from_mass_flow"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mdot": 2.0, "rho_p": 1800.0, "A_b": 0.1}, 0.01111111111111111),
                ({"mdot": 0.35, "rho_p": 1750.0, "A_b": 0.02}, 0.009999999999999998),
                ({"mdot": 0.0, "rho_p": 1800.0, "A_b": 0.1}, 0.0),
            ]
        )

    def test_derived_round_trip_through_printed_mass_balance(self):
        # Independent route: the source prints mdot = A_b * r_b * rho_p; feeding the result
        # back into that relation must reproduce the mass flow.
        for mdot, rho, area in ((2.0, 1800.0, 0.1), (13.7, 1650.0, 0.35), (0.04, 1920.0, 0.003)):
            with self.subTest(mdot=mdot):
                rate = self.formula.evaluate(mdot=mdot, rho_p=rho, A_b=area)
                self.assert_close(area * rate * rho, mdot)

    def test_domain_errors(self):
        for mdot, rho, area in (
            (-0.1, 1800.0, 0.1),
            (1.0, 0.0, 0.1),
            (1.0, -1800.0, 0.1),
            (1.0, 1800.0, 0.0),
            (1.0, 1800.0, -0.1),
        ):
            self.assert_rejected(mdot=mdot, rho_p=rho, A_b=area)

    def test_boundary_zero_flow_accepted(self):
        self.assertEqual(self.formula.evaluate(mdot=0.0, rho_p=1800.0, A_b=0.1), 0.0)


def _expansion_ratio_via_mach(gamma, ratio):
    """Area ratio from the exit Mach number and the isentropic area-Mach relation.

    Written from NACA Rep. 1135 (exit Mach number from p/p_t, then A/A*), not from the
    pressure-ratio form of the evaluator.
    """
    mach = math.sqrt(2.0 / (gamma - 1.0) * (ratio ** (-(gamma - 1.0) / gamma) - 1.0))
    base = (2.0 / (gamma + 1.0)) * (1.0 + (gamma - 1.0) / 2.0 * mach**2)
    return base ** ((gamma + 1.0) / (2.0 * (gamma - 1.0))) / mach


class NozzleExpansionRatioTest(_FormulaTest, unittest.TestCase):
    formula = nozzle_expansion_ratio
    formula_id = "propulsion.nozzle_expansion_ratio"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"gamma": 1.2, "p_e": 0.009852216748768473, "p_c": 1.0}, 12.006365875398286),
                ({"gamma": 1.4, "p_e": 0.01, "p_c": 1.0}, 8.116468977058233),
                ({"gamma": 1.25, "p_e": 0.0005, "p_c": 1.0}, 102.9617873957671),
            ],
            rel_tol=1e-10,
        )

    def test_derived_matches_mach_number_route(self):
        for gamma, ratio in ((1.1, 0.02), (1.2, 0.05), (1.33, 1e-3), (1.4, 0.2), (1.67, 0.1)):
            with self.subTest(gamma=gamma, ratio=ratio):
                self.assert_close(
                    self.formula.evaluate(gamma=gamma, p_e=ratio, p_c=1.0),
                    _expansion_ratio_via_mach(gamma, ratio),
                    rel_tol=1e-9,
                )

    def test_ratio_is_what_counts(self):
        self.assert_close(
            self.formula.evaluate(gamma=1.2, p_e=9.85, p_c=1000.0),
            self.formula.evaluate(gamma=1.2, p_e=9.85e5, p_c=1.0e8),
        )

    def test_critical_ratio_gives_one(self):
        for gamma in (1.1, 1.2, 1.4, 1.67):
            with self.subTest(gamma=gamma):
                critical = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
                self.assert_close(
                    self.formula.evaluate(gamma=gamma, p_e=critical, p_c=1.0), 1.0, rel_tol=1e-9
                )

    def test_domain_errors(self):
        for gamma, p_e, p_c in (
            (1.0, 0.1, 1.0),
            (0.9, 0.1, 1.0),
            (1.4, 0.0, 1.0),
            (1.4, -0.1, 1.0),
            (1.4, 0.1, 0.0),
            (1.4, 0.1, -1.0),
            (1.4, 1.0, 1.0),
            (1.4, 2.0, 1.0),
            (1.4, 0.6, 1.0),  # subsonic exit: above the critical ratio 0.5283
            (1.4, 0.53, 1.0),
        ):
            self.assert_rejected(gamma=gamma, p_e=p_e, p_c=p_c)

    def test_just_below_critical_ratio_accepted(self):
        self.assertGreater(self.formula.evaluate(gamma=1.4, p_e=0.5282, p_c=1.0), 1.0)


def _momentum_term_via_velocity_product(gamma, ratio):
    """Momentum part of C_F as (mass-flow term) * (exit-velocity term).

    mdot * sqrt(R * T_c) / (A_t * p_c) = sqrt(gamma * (2/(gamma+1))^((gamma+1)/(gamma-1))) and
    v_e / sqrt(R * T_c) = sqrt(2 * gamma / (gamma-1) * (1 - ratio^((gamma-1)/gamma))).
    """
    flow = math.sqrt(gamma * (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (gamma - 1.0)))
    speed = math.sqrt(2.0 * gamma / (gamma - 1.0) * (1.0 - ratio ** ((gamma - 1.0) / gamma)))
    return flow * speed


class ThrustCoefficientTest(_FormulaTest, unittest.TestCase):
    formula = thrust_coefficient
    formula_id = "propulsion.thrust_coefficient"

    EPS12 = 12.006365875398286

    def test_oracle(self):
        base = {"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "eps": self.EPS12}
        self.assert_oracle(
            [
                ({**base, "p_a": 1.0}, 1.6462855673870371),
                ({**base, "p_a": 0.0}, 1.7645748863564783),
                ({**base, "p_a": 2.0}, 1.527996248417596),
                (
                    {"gamma": 1.4, "p_e": 1.0, "p_c": 50.0, "p_a": 1.0, "eps": 5.158477790334015},
                    1.4861717353486505,
                ),
            ],
            rel_tol=1e-11,
        )

    def test_momentum_term_matches_velocity_product(self):
        # Independent route: with matched expansion (p_a = p_e) the pressure term is zero, so
        # the result is the momentum term alone, built here as flow term times velocity term.
        for gamma, ratio in ((1.15, 0.01), (1.2, 0.02), (1.4, 0.05), (1.67, 0.1)):
            with self.subTest(gamma=gamma, ratio=ratio):
                eps = _expansion_ratio_via_mach(gamma, ratio)
                self.assert_close(
                    self.formula.evaluate(gamma=gamma, p_e=ratio, p_c=1.0, p_a=ratio, eps=eps),
                    _momentum_term_via_velocity_product(gamma, ratio),
                    rel_tol=1e-9,
                )

    def test_pressure_term_is_linear_in_ambient_pressure(self):
        base = {"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "eps": self.EPS12}
        c0 = self.formula.evaluate(**base, p_a=0.0)
        c1 = self.formula.evaluate(**base, p_a=1.0)
        c3 = self.formula.evaluate(**base, p_a=3.0)
        self.assert_close(c0 - c1, self.EPS12 / 101.5, rel_tol=1e-10)
        self.assert_close(c0 - c3, 3.0 * (c0 - c1), rel_tol=1e-10)

    def test_domain_errors(self):
        good = {"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "p_a": 1.0, "eps": 12.0}
        for name, value in (
            ("gamma", 1.0),
            ("gamma", 0.5),
            ("p_e", 0.0),
            ("p_e", -1.0),
            ("p_e", 101.5),
            ("p_e", 200.0),
            ("p_c", 0.0),
            ("p_c", -1.0),
            ("p_a", -0.1),
            ("eps", 0.99),
            ("eps", -1.0),
        ):
            self.assert_rejected(**{**good, name: value})

    def test_boundaries_accepted(self):
        good = {"gamma": 1.2, "p_e": 1.0, "p_c": 101.5, "p_a": 0.0, "eps": 1.0}
        self.assertGreater(self.formula.evaluate(**good), 0.0)  # vacuum, p_a = 0 and eps = 1


class TsiolkovskyDeltaVTest(_FormulaTest, unittest.TestCase):
    formula = tsiolkovsky_delta_v
    formula_id = "propulsion.tsiolkovsky_delta_v"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"c": 3000.0, "m0": 1000.0, "mf": 500.0}, 2079.441541679836),
                ({"c": 4400.0, "m0": 5000.0, "mf": 1200.0}, 6279.311964816641),
                ({"c": 3000.0, "m0": 800.0, "mf": 800.0}, 0.0),
            ]
        )

    def test_derived_round_trip_through_printed_mass_ratio(self):
        # Independent route: the source prints final mass / initial mass = exp(-delta_v / c).
        for c, m0, mf in ((3000.0, 1000.0, 500.0), (4400.0, 5000.0, 1200.0), (310.0, 9.0, 8.5)):
            with self.subTest(c=c, m0=m0, mf=mf):
                delta_v = self.formula.evaluate(c=c, m0=m0, mf=mf)
                self.assert_close(m0 * math.exp(-delta_v / c), mf)

    def test_domain_errors(self):
        for c, m0, mf in (
            (0.0, 2.0, 1.0),
            (-3000.0, 2.0, 1.0),
            (3000.0, 0.0, 1.0),
            (3000.0, -2.0, 1.0),
            (3000.0, 2.0, 0.0),
            (3000.0, 2.0, -1.0),
            (3000.0, 1.0, 2.0),  # final mass above initial mass
        ):
            self.assert_rejected(c=c, m0=m0, mf=mf)

    def test_boundary_equal_masses_give_zero(self):
        self.assertEqual(self.formula.evaluate(c=3000.0, m0=7.0, mf=7.0), 0.0)

    def test_extreme_mass_ratio_uses_log_difference(self):
        # The ratio 1e308 / 1e-10 overflows; the logarithm is still 318 * ln 10.
        self.assert_close(
            self.formula.evaluate(c=1.0, m0=1e308, mf=1e-10), 318.0 * math.log(10.0), rel_tol=1e-12
        )


if __name__ == "__main__":
    unittest.main()

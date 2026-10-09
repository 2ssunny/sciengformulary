"""Tests for the E2 hyperbolic, parabolic, perturbation and transfer orbital formulas.

Reference values come from the independent 50-digit oracle output (mpmath) and from hand
calculation. Derived formulas are also checked by routes that do not reuse the evaluator's own
form: closed-form Hohmann burns, the cubic residual in exact rationals, finite differences and
algebraic identities.
"""

import math
import unittest
from decimal import Decimal, getcontext
from fractions import Fraction

from sciengformulary.catalog.orbital.barker_parabolic_anomaly_from_mean_anomaly import (
    barker_parabolic_anomaly_from_mean_anomaly,
)
from sciengformulary.catalog.orbital.barker_parabolic_mean_anomaly import (
    barker_parabolic_mean_anomaly,
)
from sciengformulary.catalog.orbital.bielliptic_total_delta_v import bielliptic_total_delta_v
from sciengformulary.catalog.orbital.edelbaum_delta_v import edelbaum_delta_v
from sciengformulary.catalog.orbital.hyperbolic_asymptote_true_anomaly import (
    hyperbolic_asymptote_true_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_eccentric_anomaly_from_true_anomaly import (
    hyperbolic_eccentric_anomaly_from_true_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_kepler_mean_anomaly import (
    hyperbolic_kepler_mean_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_true_anomaly_from_eccentric_anomaly import (
    hyperbolic_true_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.j2_nodal_precession_rate import j2_nodal_precession_rate
from sciengformulary.catalog.orbital.laplace_sphere_of_influence_radius import (
    laplace_sphere_of_influence_radius,
)
from sciengformulary.catalog.orbital.mean_motion_semi_major_axis_sensitivity import (
    mean_motion_semi_major_axis_sensitivity,
)

REL = 1e-12
NAN = math.nan
INF = math.inf
MU_EARTH = 398600441800000.0


class FormulaTestCase(unittest.TestCase):
    formula = None
    base = {}

    def assert_close(self, actual, expected, rel_tol=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=rel_tol, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def assert_rejects(self, bad, error=ValueError):
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(error):
                    self.formula.evaluate(**{**self.base, name: value})

    def test_oracle_values(self):
        if self.formula is None:
            self.skipTest("abstract base")
        for case in self.formula.verification_cases:
            with self.subTest(note=case.note):
                self.assert_close(
                    self.formula.evaluate(**case.inputs),
                    case.expected,
                    case.rel_tol,
                    case.abs_tol,
                )


class BiellipticTotalDeltaVTest(FormulaTestCase):
    formula = bielliptic_total_delta_v
    base = {"mu": MU_EARTH, "r1": 6678000.0, "rb": 100000000.0, "r2": 42164000.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.bielliptic_total_delta_v")

    def test_domain_rules(self):
        self.assert_rejects(
            [
                ("mu", 0.0),
                ("mu", -1.0),
                ("mu", NAN),
                ("mu", INF),
                ("r1", 0.0),
                ("r1", -5.0),
                ("r2", 0.0),
                ("r2", NAN),
                ("rb", 0.0),
                ("rb", NAN),
                ("rb", 42163999.0),  # below max(r1, r2)
            ]
        )

    def test_boundary_rb_equals_r2_is_hohmann(self):
        # With rb = r2 the third burn vanishes. The oracle's Hohmann burns for the same radii
        # (low orbit to geostationary radius) give the expected total.
        total = self.formula.evaluate(mu=MU_EARTH, r1=6678000.0, rb=42164000.0, r2=42164000.0)
        self.assert_close(total, 2425.769028306859 + 1466.8387152844527)

    def test_boundary_all_radii_equal(self):
        total = self.formula.evaluate(mu=MU_EARTH, r1=7e6, rb=7e6, r2=7e6)
        self.assertAlmostEqual(total, 0.0, places=9)

    def test_independent_route_closed_form_hohmann(self):
        # Textbook closed form of the two Hohmann burns for rb = r2 (not the vis-viva sums).
        mu, r1, r2 = MU_EARTH, 7.0e6, 1.4e8
        dv1 = math.sqrt(mu / r1) * (math.sqrt(2 * r2 / (r1 + r2)) - 1)
        dv2 = math.sqrt(mu / r2) * (1 - math.sqrt(2 * r1 / (r1 + r2)))
        self.assert_close(self.formula.evaluate(mu=mu, r1=r1, rb=r2, r2=r2), dv1 + dv2, 1e-11)

    def test_independent_route_vis_viva_with_semi_major_axes(self):
        # The equation as printed: vis-viva with a1 = (r1 + rb)/2 and a2 = (rb + r2)/2.
        mu, r1, rb, r2 = MU_EARTH, 7.0e6, 4.2e8, 1.4e8
        a1, a2 = (r1 + rb) / 2, (rb + r2) / 2
        expected = (
            abs(math.sqrt(2 * mu / r1 - mu / a1) - math.sqrt(mu / r1))
            + abs(math.sqrt(2 * mu / rb - mu / a2) - math.sqrt(2 * mu / rb - mu / a1))
            + abs(math.sqrt(mu / r2) - math.sqrt(2 * mu / r2 - mu / a2))
        )
        self.assert_close(self.formula.evaluate(mu=mu, r1=r1, rb=rb, r2=r2), expected, 1e-10)

    def test_symmetric_in_initial_and_final_radius(self):
        a = self.formula.evaluate(mu=MU_EARTH, r1=7e6, rb=4.2e8, r2=1.4e8)
        b = self.formula.evaluate(mu=MU_EARTH, r1=1.4e8, rb=4.2e8, r2=7e6)
        self.assert_close(a, b, 1e-12)

    def test_scales_with_sqrt_mu(self):
        a = self.formula.evaluate(mu=MU_EARTH, r1=7e6, rb=4.2e8, r2=1.4e8)
        b = self.formula.evaluate(mu=4 * MU_EARTH, r1=7e6, rb=4.2e8, r2=1.4e8)
        self.assert_close(b, 2 * a, 1e-12)


class LaplaceSphereOfInfluenceRadiusTest(FormulaTestCase):
    formula = laplace_sphere_of_influence_radius
    base = {"a": 149597870700.0, "m": 5.9722e24, "M": 1.98847e30}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.laplace_sphere_of_influence_radius")

    def test_domain_rules(self):
        self.assert_rejects(
            [
                ("a", 0.0),
                ("a", -1.0),
                ("a", NAN),
                ("a", INF),
                ("m", 0.0),
                ("m", -1.0),
                ("m", NAN),
                ("M", 0.0),
                ("M", NAN),
                ("m", 2.0e30),  # secondary heavier than the primary
            ]
        )

    def test_boundary_equal_masses(self):
        self.assert_close(self.formula.evaluate(a=384400000.0, m=3.0, M=3.0), 384400000.0)

    def test_independent_route_power_law(self):
        # (r / a)^(5/2) must give back the mass ratio.
        a, m, big_m = 3.844e8, 7.342e22, 5.972e24
        radius = self.formula.evaluate(a=a, m=m, M=big_m)
        self.assert_close((radius / a) ** 2.5, m / big_m, 1e-12)

    def test_masses_and_gravitational_parameters_agree(self):
        by_mass = self.formula.evaluate(a=1.0e9, m=7.342e22, M=5.972e24)
        by_mu = self.formula.evaluate(a=1.0e9, m=7.342e22 * 6.674e-11, M=5.972e24 * 6.674e-11)
        self.assert_close(by_mass, by_mu, 1e-12)

    def test_scales_with_distance(self):
        one = self.formula.evaluate(a=1.0e9, m=1.0, M=100.0)
        self.assert_close(self.formula.evaluate(a=3.0e9, m=1.0, M=100.0), 3 * one)


class HyperbolicKeplerMeanAnomalyTest(FormulaTestCase):
    formula = hyperbolic_kepler_mean_anomaly
    base = {"e": 2.0, "H": 1.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.hyperbolic_kepler_mean_anomaly")

    def test_domain_rules(self):
        self.assert_rejects(
            [("e", 1.0), ("e", 0.5), ("e", 0.0), ("e", -2.0), ("e", NAN), ("e", INF)]
            + [("H", NAN), ("H", INF), ("H", -INF)]
        )

    def test_boundary_periapsis(self):
        self.assertEqual(self.formula.evaluate(e=3.0, H=0.0), 0.0)

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(e=2.0, H=800.0)
        with self.assertRaises(OverflowError):
            self.formula.evaluate(e=1e308, H=700.0)

    def test_odd_in_H(self):
        self.assert_close(
            self.formula.evaluate(e=1.7, H=-0.9), -self.formula.evaluate(e=1.7, H=0.9)
        )

    def test_slope_is_e_cosh_minus_one(self):
        # dM/dH = e cosh H - 1, by central difference.
        e, h, step = 1.8, 0.7, 1e-5
        slope = (
            self.formula.evaluate(e=e, H=h + step) - self.formula.evaluate(e=e, H=h - step)
        ) / (2 * step)
        self.assert_close(slope, e * math.cosh(h) - 1, 1e-8)


class HyperbolicAsymptoteTrueAnomalyTest(FormulaTestCase):
    formula = hyperbolic_asymptote_true_anomaly
    base = {"e": 2.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.hyperbolic_asymptote_true_anomaly")

    def test_domain_rules(self):
        self.assert_rejects([("e", 1.0), ("e", 0.99), ("e", 0.0), ("e", -3.0), ("e", NAN)])
        self.assert_rejects([("e", INF), ("e", -INF)])

    def test_boundary_just_above_one(self):
        # e -> 1+ approaches 180 degrees; e -> infinity approaches 90 degrees.
        self.assertLess(self.formula.evaluate(e=1.0 + 1e-12), math.pi)
        self.assertGreater(self.formula.evaluate(e=1e12), math.pi / 2)

    def test_independent_route_two_pi_over_three(self):
        self.assert_close(self.formula.evaluate(e=2.0), 2 * math.pi / 3)

    def test_independent_route_conic_has_no_finite_radius(self):
        # At nu_inf the conic denominator 1 + e cos(nu) of r = p / (1 + e cos nu) vanishes.
        for e in (1.01, 1.5, 3.0, 40.0):
            with self.subTest(e=e):
                nu = self.formula.evaluate(e=e)
                self.assertAlmostEqual(1 + e * math.cos(nu), 0.0, places=12)
                self.assertTrue(math.pi / 2 < nu < math.pi)


class HyperbolicEccentricAnomalyFromTrueAnomalyTest(FormulaTestCase):
    formula = hyperbolic_eccentric_anomaly_from_true_anomaly
    base = {"e": 2.0, "nu": 1.35}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.hyperbolic_eccentric_anomaly_from_true_anomaly")

    def test_domain_rules(self):
        nu_inf = math.acos(-1 / 2.0)
        self.assert_rejects(
            [("e", 1.0), ("e", 0.5), ("e", NAN), ("e", INF)]
            + [("nu", NAN), ("nu", INF), ("nu", nu_inf), ("nu", -nu_inf), ("nu", 2.5)]
            + [("nu", math.pi), ("nu", 2 * math.pi + 0.5)]
        )

    def test_boundary_just_inside_asymptote(self):
        nu_inf = math.acos(-1 / 2.0)
        self.assertGreater(self.formula.evaluate(e=2.0, nu=nu_inf * (1 - 1e-9)), 5.0)

    def test_boundary_periapsis(self):
        self.assertEqual(self.formula.evaluate(e=2.0, nu=0.0), 0.0)

    def test_odd_in_nu(self):
        self.assert_close(
            self.formula.evaluate(e=1.5, nu=-0.8), -self.formula.evaluate(e=1.5, nu=0.8)
        )

    def test_independent_route_inverse_with_oracle_value(self):
        # The oracle's nu(e=2, H=1.0000213593109137) is 1.35 (inverse relation).
        inverse = hyperbolic_true_anomaly_from_eccentric_anomaly.evaluate(
            e=2.0, H=1.0000213593109137
        )
        self.assert_close(inverse, 1.35, 1e-11)

    def test_independent_route_cosh_identity(self):
        # cosh H = (e + cos nu) / (1 + e cos nu) for the true-anomaly to H relation.
        for e, nu in ((2.0, 1.35), (1.5, -1.9), (3.0, 0.4), (1.1, 2.0)):
            with self.subTest(e=e, nu=nu):
                h = self.formula.evaluate(e=e, nu=nu)
                self.assert_close(math.cosh(h), (e + math.cos(nu)) / (1 + e * math.cos(nu)), 1e-10)

    def test_independent_route_areal_law(self):
        # Kepler's equation must advance at (e^2 - 1)^(3/2) / (1 + e cos nu)^2 per unit of true
        # anomaly, which follows from r^2 dnu/dt = sqrt(mu p) and p = |a| (e^2 - 1).
        e, nu, step = 2.0, 0.9, 1e-6
        rate = (
            hyperbolic_kepler_mean_anomaly.evaluate(e=e, H=self.formula.evaluate(e=e, nu=nu + step))
            - hyperbolic_kepler_mean_anomaly.evaluate(
                e=e, H=self.formula.evaluate(e=e, nu=nu - step)
            )
        ) / (2 * step)
        self.assert_close(rate, (e * e - 1) ** 1.5 / (1 + e * math.cos(nu)) ** 2, 1e-7)

    def test_near_one_eccentricity_is_accurate(self):
        # Small angle: H ~ sqrt(e^2 - 1) nu / (1 + e) for nu -> 0 (first-order expansion).
        e = 1.0 + 1e-9
        self.assert_close(self.formula.evaluate(e=e, nu=1e-6), math.sqrt(2e-9) * 1e-6 / 2, 1e-6)


class HyperbolicTrueAnomalyFromEccentricAnomalyTest(FormulaTestCase):
    formula = hyperbolic_true_anomaly_from_eccentric_anomaly
    base = {"e": 2.0, "H": 1.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.hyperbolic_true_anomaly_from_eccentric_anomaly")

    def test_domain_rules(self):
        self.assert_rejects(
            [("e", 1.0), ("e", 0.5), ("e", NAN), ("e", INF), ("H", NAN), ("H", INF)]
        )

    def test_boundary_periapsis(self):
        self.assertEqual(self.formula.evaluate(e=2.0, H=0.0), 0.0)

    def test_boundary_saturates_at_asymptote(self):
        # tanh saturates: huge H gives the asymptote true anomaly without overflow.
        nu_inf = hyperbolic_asymptote_true_anomaly.evaluate(e=2.0)
        self.assert_close(self.formula.evaluate(e=2.0, H=1e6), nu_inf, 1e-12)
        self.assertLess(abs(self.formula.evaluate(e=2.0, H=-1e6)), nu_inf + 1e-12)

    def test_independent_route_inverse_with_oracle_value(self):
        # The oracle's H(e=1.5, nu=-1.9) is -1.4675706294660553; the inverse returns nu = -1.9.
        self.assert_close(self.formula.evaluate(e=1.5, H=-1.4675706294660553), -1.9, 1e-11)

    def test_independent_route_cosine_identity(self):
        # cos nu = (e - cosh H) / (e cosh H - 1) follows from the conic and r = |a|(e cosh H - 1).
        for e, h in ((2.0, 1.0), (1.5, -1.4), (3.0, 0.3), (1.1, 4.0)):
            with self.subTest(e=e, H=h):
                nu = self.formula.evaluate(e=e, H=h)
                self.assert_close(math.cos(nu), (e - math.cosh(h)) / (e * math.cosh(h) - 1), 1e-10)

    def test_stays_inside_the_asymptotes(self):
        for e in (1.01, 2.0, 10.0):
            nu_inf = math.acos(-1 / e)
            for h in (-30.0, -2.0, 0.5, 8.0):
                with self.subTest(e=e, H=h):
                    self.assertLess(abs(self.formula.evaluate(e=e, H=h)), nu_inf + 1e-12)


class J2NodalPrecessionRateTest(FormulaTestCase):
    formula = j2_nodal_precession_rate
    base = {
        "mu": MU_EARTH,
        "a": 7078000.0,
        "e": 0.01,
        "i": 1.0,
        "R_e": 6378137.0,
        "J2": 0.00108263,
    }

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.j2_nodal_precession_rate")

    def test_domain_rules(self):
        self.assert_rejects(
            [("mu", 0.0), ("mu", -1.0), ("mu", NAN), ("a", 0.0), ("a", -7e6), ("a", INF)]
            + [("e", -0.1), ("e", 1.0), ("e", 1.5), ("e", NAN)]
            + [("i", -0.1), ("i", math.pi + 0.01), ("i", NAN), ("i", INF)]
            + [("R_e", 0.0), ("R_e", -1.0), ("J2", 0.0), ("J2", -0.001), ("J2", NAN)]
        )

    def test_boundary_inclinations(self):
        prograde = self.formula.evaluate(**{**self.base, "i": 0.0})
        retrograde = self.formula.evaluate(**{**self.base, "i": math.pi})
        self.assertLess(prograde, 0.0)
        self.assert_close(retrograde, -prograde)
        self.assertAlmostEqual(self.formula.evaluate(**{**self.base, "i": math.pi / 2}), 0.0)

    def test_boundary_circular_orbit(self):
        self.assertTrue(math.isfinite(self.formula.evaluate(**{**self.base, "e": 0.0})))

    def test_independent_route_decimal_closed_form(self):
        # Same law in the form -(3/2) J2 R_e^2 sqrt(mu) a^(-7/2) (1 - e^2)^(-2) cos(i), evaluated
        # with 40-digit decimals so no step reuses the evaluator's n and p variables.
        getcontext().prec = 40
        mu, a, e, i = Decimal("398600441800000"), Decimal("8500000"), Decimal("0.3"), 0.9
        r_e, j2 = Decimal("6378137"), Decimal("0.00108263")
        expected = (
            Decimal("-1.5")
            * j2
            * r_e**2
            * mu.sqrt()
            / (a**3 * a.sqrt())
            / (1 - e * e) ** 2
            * Decimal(math.cos(i))
        )
        actual = self.formula.evaluate(
            mu=float(mu), a=float(a), e=float(e), i=i, R_e=float(r_e), J2=float(j2)
        )
        self.assert_close(actual, float(expected), 1e-12)

    def test_independent_route_semi_major_axis_power_law(self):
        # For a circular orbit the rate scales as a^(-7/2).
        near = self.formula.evaluate(**{**self.base, "e": 0.0})
        far = self.formula.evaluate(**{**self.base, "e": 0.0, "a": 4 * 7078000.0})
        self.assert_close(far, near / 4**3.5, 1e-12)

    def test_independent_route_sun_synchronous_rate(self):
        # A sun-synchronous orbit turns its node at 360 deg per tropical year (365.2422 days),
        # about 1.99096871e-7 rad/s; the oracle's near-sun-synchronous case (+1.9941e-7 rad/s)
        # is within 0.2 percent of it.
        tropical_year_rate = 2 * math.pi / (365.2422 * 86400)
        value = self.formula.evaluate(
            mu=MU_EARTH, a=7078000.0, e=0.0, i=1.7139133254584316, R_e=6378137.0, J2=0.00108263
        )
        self.assertLess(abs(value / tropical_year_rate - 1), 2e-3)

    def test_independent_route_published_regression_rate(self):
        # NASA TN D-1045 prints +0.9856 deg/day for its 600 n.mi. orbit at i = 99.89 deg.
        printed = 0.9856 * math.pi / 180 / 86400
        value = self.formula.evaluate(
            mu=398632900000000.0,
            a=7483200.0,
            e=0.0,
            i=1.743409389817136,
            R_e=6378388.0,
            J2=0.0010913333333333333,
        )
        self.assert_close(value, printed, 2e-3)


class MeanMotionSemiMajorAxisSensitivityTest(FormulaTestCase):
    formula = mean_motion_semi_major_axis_sensitivity
    base = {"n": 0.001078007612872506, "a": 7000000.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.mean_motion_semi_major_axis_sensitivity")

    def test_domain_rules(self):
        self.assert_rejects(
            [("n", 0.0), ("n", -1e-3), ("n", NAN), ("n", INF)]
            + [("a", 0.0), ("a", -7e6), ("a", NAN), ("a", INF)]
        )

    def test_boundary_always_negative(self):
        self.assertLess(self.formula.evaluate(n=1e-3, a=1e300), 0.0)

    def test_independent_route_exact_power_law(self):
        # mu = 1, a = 4: n = 4^(-3/2) = 1/8 and d/da a^(-3/2) = -(3/2) a^(-5/2) = -3/64.
        self.assert_close(self.formula.evaluate(n=0.125, a=4.0), float(Fraction(-3, 64)))

    def test_independent_route_finite_difference(self):
        mu = MU_EARTH
        for a in (7.0e6, 4.2164e7):
            with self.subTest(a=a):
                step = a * 1e-5
                slope = (math.sqrt(mu / (a + step) ** 3) - math.sqrt(mu / (a - step) ** 3)) / (
                    2 * step
                )
                n = math.sqrt(mu / a**3)
                self.assert_close(self.formula.evaluate(n=n, a=a), slope, 1e-8)


class BarkerParabolicMeanAnomalyTest(FormulaTestCase):
    formula = barker_parabolic_mean_anomaly
    base = {"nu": 1.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.barker_parabolic_mean_anomaly")

    def test_domain_rules(self):
        self.assert_rejects(
            [("nu", math.pi), ("nu", -math.pi), ("nu", 3.5), ("nu", 2 * math.pi)]
            + [("nu", NAN), ("nu", INF), ("nu", -INF)]
        )

    def test_boundary_close_to_asymptote(self):
        self.assertGreater(self.formula.evaluate(nu=math.pi - 1e-9), 1e20)
        self.assertLess(self.formula.evaluate(nu=-(math.pi - 1e-9)), -1e20)

    def test_independent_route_exact_rational(self):
        # tan(nu/2) = 1/2 gives M_p = 1/2 + (1/8)/3 = 13/24 (exact rationals).
        nu = 2 * math.atan(0.5)
        expected = Fraction(1, 2) + Fraction(1, 8) / 3
        self.assert_close(self.formula.evaluate(nu=nu), float(expected), 1e-12)

    def test_independent_route_round_trip_with_inverse(self):
        # The inverse's oracle value D(M_p=-10) = -2.7866708131026976 is tan(nu/2); so the forward
        # relation at nu = 2 atan(D) must return -10.
        nu = 2 * math.atan(-2.7866708131026976)
        self.assert_close(self.formula.evaluate(nu=nu), -10.0, 1e-11)

    def test_independent_route_tangent_half_angle(self):
        nu = -2.0
        d = math.tan(-1.0)
        self.assert_close(self.formula.evaluate(nu=nu), d + d**3 / 3, 1e-12)


class BarkerParabolicAnomalyFromMeanAnomalyTest(FormulaTestCase):
    formula = barker_parabolic_anomaly_from_mean_anomaly
    base = {"M_p": 1.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.barker_parabolic_anomaly_from_mean_anomaly")

    def test_domain_rules(self):
        self.assert_rejects([("M_p", NAN), ("M_p", INF), ("M_p", -INF)])

    def test_boundary_overflow_of_huge_input(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(M_p=1.7e308)
        with self.assertRaises(OverflowError):
            self.formula.evaluate(M_p=-1.7e308)

    def test_boundary_huge_but_representable(self):
        d = self.formula.evaluate(M_p=1e300)
        self.assertTrue(math.isfinite(d))
        self.assert_close(d**3 / 3, 1e300, 1e-9)

    def test_boundary_tiny_input_keeps_relative_accuracy(self):
        # D = M_p - M_p^3/3 + ... so for M_p = 1e-8 the result is 1e-8 to the last digits.
        self.assert_close(self.formula.evaluate(M_p=1e-8), 1e-8, 1e-12)
        self.assert_close(self.formula.evaluate(M_p=-1e-8), -1e-8, 1e-12)

    def test_independent_route_cubic_residual(self):
        # D must satisfy D^3 + 3 D - 3 M_p = 0; checked in exact rational arithmetic.
        for m in (-1e6, -10.0, -0.7, 0.1, 1.0 / 3.0, 5.0, 37.5, 1e6):
            with self.subTest(M_p=m):
                d = Fraction(self.formula.evaluate(M_p=m))
                residual = d**3 + 3 * d - 3 * Fraction(m)
                self.assertLess(abs(float(residual)), 1e-12 * (3 * abs(m) + 1))

    def test_independent_route_cardano(self):
        for m in (-10.0, -0.7, 0.4, 37.5):
            with self.subTest(M_p=m):
                b = 1.5 * m
                u = math.copysign(abs(b + math.sqrt(1 + b * b)) ** (1 / 3), 1)
                self.assert_close(self.formula.evaluate(M_p=m), u - 1 / u, 1e-9, 1e-12)

    def test_independent_route_round_trip_with_forward(self):
        for nu in (-2.5, -0.3, 0.9, 3.0):
            with self.subTest(nu=nu):
                m = barker_parabolic_mean_anomaly.evaluate(nu=nu)
                self.assert_close(2 * math.atan(self.formula.evaluate(M_p=m)), nu, 1e-11)

    def test_odd_symmetry(self):
        self.assertEqual(self.formula.evaluate(M_p=-3.7), -self.formula.evaluate(M_p=3.7))


class EdelbaumDeltaVTest(FormulaTestCase):
    formula = edelbaum_delta_v
    base = {"mu": MU_EARTH, "a0": 6878137.0, "a1": 42061137.0, "di": 0.5}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "orbital.edelbaum_delta_v")

    def test_domain_rules(self):
        self.assert_rejects(
            [("mu", 0.0), ("mu", -1.0), ("mu", NAN), ("a0", 0.0), ("a0", -7e6), ("a0", NAN)]
            + [("a1", 0.0), ("a1", -7e6), ("a1", INF), ("di", -0.1), ("di", NAN), ("di", INF)]
        )

    def test_boundary_no_change_gives_zero(self):
        self.assertEqual(self.formula.evaluate(mu=MU_EARTH, a0=7e6, a1=7e6, di=0.0), 0.0)

    def test_boundary_plane_change_of_two_radians(self):
        # cos(pi) = -1, so dV = V0 + V1.
        v0, v1 = math.sqrt(MU_EARTH / 7e6), math.sqrt(MU_EARTH / 4.2164e7)
        self.assert_close(self.formula.evaluate(mu=MU_EARTH, a0=7e6, a1=4.2164e7, di=2.0), v0 + v1)

    def test_independent_route_law_of_cosines(self):
        # The report's printed form, evaluated directly.
        for a0, a1, di in ((6878137.0, 42061137.0, 0.5009094953223726), (9e6, 7e6, 1.3)):
            with self.subTest(a0=a0, a1=a1, di=di):
                v0, v1 = math.sqrt(MU_EARTH / a0), math.sqrt(MU_EARTH / a1)
                expected = math.sqrt(v0**2 + v1**2 - 2 * v0 * v1 * math.cos(math.pi * di / 2))
                self.assert_close(
                    self.formula.evaluate(mu=MU_EARTH, a0=a0, a1=a1, di=di), expected, 1e-11
                )

    def test_independent_route_published_example(self):
        # The report prints 5.86 km/s for LEO (500 km, 28.7 deg) to GEO (35683 km altitude).
        value = self.formula.evaluate(
            mu=MU_EARTH, a0=6878137.0, a1=42061137.0, di=math.radians(28.7)
        )
        self.assert_close(value, 5860.0, 1e-3)

    def test_independent_route_pure_plane_change(self):
        v = math.sqrt(MU_EARTH / 7e6)
        self.assert_close(
            self.formula.evaluate(mu=MU_EARTH, a0=7e6, a1=7e6, di=0.5),
            2 * v * math.sin(math.pi * 0.5 / 4),
        )

    def test_nearly_equal_orbits_keep_accuracy(self):
        # No cancellation for very small changes: dV ~ pi V di / 2 for a0 = a1, di -> 0.
        v = math.sqrt(MU_EARTH / 7e6)
        self.assert_close(
            self.formula.evaluate(mu=MU_EARTH, a0=7e6, a1=7e6, di=1e-9),
            math.pi * v * 1e-9 / 2,
            1e-9,
        )


if __name__ == "__main__":
    unittest.main()

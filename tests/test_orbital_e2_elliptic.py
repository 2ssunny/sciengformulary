"""Tests for the e2 elliptic-orbit formulas: speeds, conic geometry, anomalies, Hohmann transfer.

Reference values come from the phase-2 oracle (50-digit mpmath, exact hand arithmetic) rather
than from the evaluators under test. Every derived formula is also checked through an independent
route built from the source's original relations, written out in the tests themselves.
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.orbital.circular_orbit_speed import circular_orbit_speed
from sciengformulary.catalog.orbital.conic_orbit_radius import conic_orbit_radius
from sciengformulary.catalog.orbital.eccentric_anomaly_from_true_anomaly import (
    eccentric_anomaly_from_true_anomaly,
)
from sciengformulary.catalog.orbital.flight_path_angle import flight_path_angle
from sciengformulary.catalog.orbital.hohmann_first_impulse import hohmann_first_impulse
from sciengformulary.catalog.orbital.hohmann_second_impulse import hohmann_second_impulse
from sciengformulary.catalog.orbital.hohmann_transfer_time import hohmann_transfer_time
from sciengformulary.catalog.orbital.kepler_mean_anomaly_from_eccentric_anomaly import (
    kepler_mean_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.keplerian_mean_motion import keplerian_mean_motion
from sciengformulary.catalog.orbital.semi_latus_rectum import semi_latus_rectum
from sciengformulary.catalog.orbital.specific_angular_momentum import specific_angular_momentum
from sciengformulary.catalog.orbital.true_anomaly_from_eccentric_anomaly import (
    true_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.vis_viva_speed import vis_viva_speed
from sciengformulary.core import FormulaSpec

REL = 1e-12
MU = 398600441800000.0  # Earth, m^3/s^2, as used by the oracle
PI = math.pi


class _FormulaTest:
    formula: FormulaSpec
    formula_id: str
    derived = False

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
            self.assertEqual(ref.source_type, "technical_report")
            self.assertNotIn("openstax", (ref.url or "").lower())
            self.assertIsNotNone(ref.locator)

    def test_derived_marker(self):
        marked = any(text.startswith("Derived result:") for text in self.formula.assumptions)
        self.assertEqual(marked, self.derived)

    def test_verification_cases_pass(self):
        self.formula.verify()

    def test_non_finite_inputs_rejected(self):
        base = dict(self.formula.verification_cases[0].inputs)
        for name in base:
            for bad in (math.nan, math.inf):
                with self.subTest(name=name, bad=bad):
                    with self.assertRaises(ValueError):
                        self.formula.evaluate(**{**base, name: bad})


class KeplerianMeanMotionTest(_FormulaTest, unittest.TestCase):
    formula = keplerian_mean_motion
    formula_id = "orbital.keplerian_mean_motion"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "a": 7000000.0}, 0.001078007612872506),
                ({"mu": MU, "a": 42164000.0}, 7.292159861796045e-05),
                ({"mu": MU, "a": -7000000.0}, 0.001078007612872506),
            ]
        )

    def test_domain(self):
        self.assert_rejected(mu=0.0, a=7.0e6)
        self.assert_rejected(mu=-MU, a=7.0e6)
        self.assert_rejected(mu=MU, a=0.0)
        self.assert_rejected(mu=True, a=7.0e6)

    def test_boundary_unit_values(self):
        self.assert_close(self.formula.evaluate(mu=1.0, a=1.0), 1.0)
        self.assert_close(self.formula.evaluate(mu=4.0, a=-1.0), 2.0)

    def test_extreme_lengths(self):
        # |a|^3 would overflow (or underflow) as a float, the result itself is representable.
        self.assert_close(self.formula.evaluate(mu=1.0e300, a=1.0e100), 1.0)
        with self.assertRaises(OverflowError):
            self.formula.evaluate(mu=1.0e10, a=1.0e-250)

    def test_period_route(self):
        # n T = 2 pi with T = 2 pi sqrt(a^3 / mu), written out here rather than reused.
        for a in (6.8e6, 4.2164e7, 3.844e8):
            with self.subTest(a=a):
                period = 2.0 * PI * math.sqrt(a**3 / MU)
                self.assert_close(self.formula.evaluate(mu=MU, a=a) * period, 2.0 * PI)

    def test_gauss_form_route(self):
        # Preprint form: sqrt(mu) (t - T) = q^(3/2) (1 - e)^(-3/2) (E - e sin E) (ellipse) and
        # q^(3/2) (e - 1)^(-3/2) (e sinh H - H) (hyperbola); the bracket's coefficient is
        # sqrt(mu) / n.
        a, e = 7.0e6, 0.3
        q = a * (1.0 - e)
        coefficient = q**1.5 * (1.0 - e) ** -1.5
        self.assert_close(self.formula.evaluate(mu=MU, a=a), math.sqrt(MU) / coefficient)
        a, e = -1.0e7, 2.0
        q = abs(a) * (e - 1.0)
        coefficient = q**1.5 * (e - 1.0) ** -1.5
        self.assert_close(self.formula.evaluate(mu=MU, a=a), math.sqrt(MU) / coefficient)

    def test_hyperbolic_branch_uses_magnitude(self):
        self.assert_close(
            self.formula.evaluate(mu=MU, a=-2.0e7), self.formula.evaluate(mu=MU, a=2.0e7)
        )


class CircularOrbitSpeedTest(_FormulaTest, unittest.TestCase):
    formula = circular_orbit_speed
    formula_id = "orbital.circular_orbit_speed"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "r": 6778000.0}, 7668.635675197651),
                ({"mu": MU, "r": 42164000.0}, 3074.6662841276843),
            ]
        )

    def test_domain(self):
        self.assert_rejected(mu=0.0, r=7.0e6)
        self.assert_rejected(mu=-1.0, r=7.0e6)
        self.assert_rejected(mu=MU, r=0.0)
        self.assert_rejected(mu=MU, r=-7.0e6)

    def test_boundary_unit_values(self):
        self.assert_close(self.formula.evaluate(mu=1.0, r=1.0), 1.0)
        self.assert_close(self.formula.evaluate(mu=9.0, r=4.0), 1.5)

    def test_force_balance_and_period_routes(self):
        # Centripetal balance v^2 / r = mu / r^2, and circumference / period = speed.
        for r in (6.778e6, 4.2164e7):
            with self.subTest(r=r):
                v = self.formula.evaluate(mu=MU, r=r)
                self.assert_close(v * v / r, MU / (r * r))
                period = 2.0 * PI * math.sqrt(r**3 / MU)
                self.assert_close(2.0 * PI * r / period, v)


class VisVivaSpeedTest(_FormulaTest, unittest.TestCase):
    formula = vis_viva_speed
    formula_id = "orbital.vis_viva_speed"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "r": 6678000.0, "a": 24421000.0}, 10151.608507443249),
                ({"mu": MU, "r": 42164000.0, "a": 24421000.0}, 1607.8275688432316),
                ({"mu": MU, "r": 7000000.0, "a": 7000000.0}, 7546.053290107542),
                ({"mu": MU, "r": 7000000.0, "a": -20000000.0}, 11567.880644451934),
            ]
        )

    def test_domain(self):
        self.assert_rejected(mu=0.0, r=7.0e6, a=7.0e6)
        self.assert_rejected(mu=MU, r=0.0, a=7.0e6)
        self.assert_rejected(mu=MU, r=-7.0e6, a=7.0e6)
        self.assert_rejected(mu=MU, r=7.0e6, a=0.0)
        # r beyond 2 a: the radicand is negative and must not be clamped.
        self.assert_rejected(mu=MU, r=3.0e7, a=1.0e7)

    def test_boundary_r_equals_two_a(self):
        # Largest distance an ellipse of semi-major axis a can reach: speed vanishes.
        self.assertEqual(self.formula.evaluate(mu=1.0, r=2.0, a=1.0), 0.0)

    def test_energy_route(self):
        # v^2 / 2 - mu / r = -mu / (2 a) (energy), for an ellipse and a hyperbola.
        for r, a in ((6.678e6, 2.4421e7), (7.0e6, -2.0e7)):
            with self.subTest(r=r, a=a):
                v = self.formula.evaluate(mu=MU, r=r, a=a)
                self.assert_close(0.5 * v * v - MU / r, -MU / (2.0 * a), rel_tol=1e-9)

    def test_orbit_equation_route(self):
        # v^2 = (mu / p) (1 + 2 e cos(nu) + e^2) with p = a (1 - e^2), r = p / (1 + e cos nu).
        a, e, nu = 1.2e7, 0.35, 1.1
        p = a * (1.0 - e * e)
        r = p / (1.0 + e * math.cos(nu))
        expected = math.sqrt(MU / p * (1.0 + 2.0 * e * math.cos(nu) + e * e))
        self.assert_close(self.formula.evaluate(mu=MU, r=r, a=a), expected)

    def test_circular_special_case(self):
        self.assert_close(self.formula.evaluate(mu=MU, r=7.0e6, a=7.0e6), math.sqrt(MU / 7.0e6))


class ConicOrbitRadiusTest(_FormulaTest, unittest.TestCase):
    formula = conic_orbit_radius
    formula_id = "orbital.conic_orbit_radius"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"p": 6930000.0, "e": 0.1, "nu": 0.0}, 6300000.0),
                ({"p": 6930000.0, "e": 0.1, "nu": PI}, 7700000.0),
                ({"p": 1.0e7, "e": 2.0, "nu": 1.0}, 4806295.219952881),
                ({"p": 1.0e7, "e": 1.0, "nu": PI / 2.0}, 1.0e7),
                ({"p": 7.0e6, "e": 0.0, "nu": 2.2}, 7.0e6),
            ]
        )

    def test_domain(self):
        self.assert_rejected(p=0.0, e=0.1, nu=0.0)
        self.assert_rejected(p=-1.0, e=0.1, nu=0.0)
        self.assert_rejected(p=1.0e7, e=-0.1, nu=0.0)
        self.assert_rejected(p=1.0e7, e=1.0, nu=PI)  # parabola at its asymptote direction
        self.assert_rejected(p=1.0e7, e=2.0, nu=PI)  # hyperbola outside the asymptotes
        self.assert_rejected(p=1.0e7, e=2.0, nu=2.5)  # 1 + 2 cos(2.5) < 0

    def test_boundary_just_inside_asymptote(self):
        e = 2.0
        nu = math.acos(-1.0 / e) - 1.0e-6
        r = self.formula.evaluate(p=1.0e7, e=e, nu=nu)
        self.assertGreater(r, 1.0e12)

    def test_inverse_relation_route(self):
        # The report's relation cos(nu) = (p - r) / (e r), recovered from the evaluator's r.
        for e, nu in ((0.2, 0.7), (0.6, -2.0), (3.0, 1.0)):
            with self.subTest(e=e, nu=nu):
                r = self.formula.evaluate(p=9.0e6, e=e, nu=nu)
                self.assert_close((9.0e6 - r) / (e * r), math.cos(nu), rel_tol=1e-9)

    def test_apsis_route(self):
        a, e = 1.5e7, 0.4
        p = a * (1.0 - e * e)
        self.assert_close(self.formula.evaluate(p=p, e=e, nu=0.0), a * (1.0 - e))
        self.assert_close(self.formula.evaluate(p=p, e=e, nu=PI), a * (1.0 + e))
        # Semi-major-axis form a (1 - e^2) / (1 + e cos nu) at an arbitrary angle.
        nu = 2.4
        self.assert_close(
            self.formula.evaluate(p=p, e=e, nu=nu), a * (1.0 - e * e) / (1.0 + e * math.cos(nu))
        )


class SemiLatusRectumTest(_FormulaTest, unittest.TestCase):
    formula = semi_latus_rectum
    formula_id = "orbital.semi_latus_rectum"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"a": 7.0e6, "e": 0.1}, 6930000.0),
                ({"a": 7.0e6, "e": 0.0}, 7.0e6),
                ({"a": -1.0e7, "e": 2.0}, 3.0e7),
            ]
        )

    def test_domain(self):
        self.assert_rejected(a=0.0, e=0.1)
        self.assert_rejected(a=7.0e6, e=-0.1)
        self.assert_rejected(a=7.0e6, e=1.0)  # parabola
        self.assert_rejected(a=-7.0e6, e=0.5)  # hyperbola needs e > 1
        self.assert_rejected(a=7.0e6, e=1.5)  # ellipse needs e < 1

    def test_boundary_near_parabola(self):
        p = self.formula.evaluate(a=1.0e9, e=0.999999)
        # Exact rational arithmetic on the float inputs: 1 - e^2 is computed without rounding.
        exact = Fraction(1.0e9) * (1 - Fraction(0.999999) ** 2)
        self.assert_close(p, float(exact), rel_tol=1e-15)
        self.assertGreater(p, 0.0)

    def test_eccentricity_route(self):
        # The report's e = sqrt(1 - p / a), recovered from the evaluator's p.
        for a, e in ((7.0e6, 0.25), (2.4421e7, 0.73)):
            with self.subTest(a=a, e=e):
                p = self.formula.evaluate(a=a, e=e)
                self.assert_close(math.sqrt(1.0 - p / a), e)

    def test_apsis_route(self):
        # p is the harmonic mean of the apsis radii, 2 r_p r_a / (r_p + r_a).
        a, e = 1.3e7, 0.55
        r_p, r_a = a * (1.0 - e), a * (1.0 + e)
        self.assert_close(self.formula.evaluate(a=a, e=e), 2.0 * r_p * r_a / (r_p + r_a))
        # Hyperbola: p = q (1 + e) with periapsis distance q = |a| (e - 1).
        a, e = -9.0e6, 1.8
        q = abs(a) * (e - 1.0)
        self.assert_close(self.formula.evaluate(a=a, e=e), q * (1.0 + e))


class SpecificAngularMomentumTest(_FormulaTest, unittest.TestCase):
    formula = specific_angular_momentum
    formula_id = "orbital.specific_angular_momentum"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "p": 7.0e6}, 52822373030.75279),
                ({"mu": MU, "p": 6930000.0}, 52557597563.75856),
                ({"mu": MU, "p": 0.0}, 0.0),
            ]
        )

    def test_domain(self):
        self.assert_rejected(mu=0.0, p=7.0e6)
        self.assert_rejected(mu=-MU, p=7.0e6)
        self.assert_rejected(mu=MU, p=-1.0)

    def test_boundary_zero_and_overflow(self):
        self.assertEqual(self.formula.evaluate(mu=MU, p=0.0), 0.0)
        with self.assertRaises(OverflowError):
            self.formula.evaluate(mu=1.0e200, p=1.0e200)

    def test_area_law_route(self):
        # h = 2 pi a b / T for an ellipse with b = a sqrt(1 - e^2) and T = 2 pi sqrt(a^3 / mu).
        a, e = 1.1e7, 0.4
        b = a * math.sqrt(1.0 - e * e)
        period = 2.0 * PI * math.sqrt(a**3 / MU)
        p = a * (1.0 - e * e)
        self.assert_close(self.formula.evaluate(mu=MU, p=p), 2.0 * PI * a * b / period)

    def test_periapsis_and_flight_path_routes(self):
        a, e = 1.1e7, 0.4
        p = a * (1.0 - e * e)
        h = self.formula.evaluate(mu=MU, p=p)
        # h = r_p v_p at periapsis, with v_p from the vis-viva equation.
        r_p = a * (1.0 - e)
        v_p = math.sqrt(MU * (2.0 / r_p - 1.0 / a))
        self.assert_close(h, r_p * v_p)
        # h = r v cos(gamma) at a general point.
        nu = 1.3
        r = p / (1.0 + e * math.cos(nu))
        v = math.sqrt(MU * (2.0 / r - 1.0 / a))
        gamma = math.atan2(e * math.sin(nu), 1.0 + e * math.cos(nu))
        self.assert_close(h, r * v * math.cos(gamma), rel_tol=1e-11)


class FlightPathAngleTest(_FormulaTest, unittest.TestCase):
    formula = flight_path_angle
    formula_id = "orbital.flight_path_angle"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"e": 0.0, "nu": 1.3}, 0.0),
                ({"e": 0.5, "nu": PI / 2.0}, 0.4636476090008061),
                ({"e": 0.3, "nu": -2.0}, -0.3021591249043568),
                ({"e": 2.0, "nu": 2.0}, 1.478838878440151),
                ({"e": 0.3, "nu": PI}, 5.248486282060085e-17),
            ]
        )

    def test_domain(self):
        self.assert_rejected(e=-0.1, nu=0.5)
        self.assert_rejected(e=1.0, nu=PI)  # parabola, asymptote direction
        self.assert_rejected(e=2.0, nu=PI)  # outside the hyperbola's asymptotes
        self.assert_rejected(e=2.0, nu=2.5)

    def test_boundary_range_and_symmetry(self):
        # Close to an asymptote the angle approaches, but never reaches, +/- pi/2.
        e = 10.0
        nu = math.acos(-1.0 / e) - 1.0e-9
        gamma = self.formula.evaluate(e=e, nu=nu)
        self.assertLess(gamma, PI / 2.0)
        self.assertGreater(gamma, 1.5)
        # Odd in nu.
        self.assert_close(
            self.formula.evaluate(e=0.4, nu=-1.2), -self.formula.evaluate(e=0.4, nu=1.2)
        )
        # Zero at periapsis.
        self.assertEqual(self.formula.evaluate(e=0.7, nu=0.0), 0.0)

    def test_momentum_route(self):
        # cos(gamma) = h / (r v) built from h = sqrt(mu p), the orbit equation and vis-viva.
        a, e = 1.2e7, 0.4
        p = a * (1.0 - e * e)
        for nu in (0.3, 1.1, 2.1, 2.9):
            with self.subTest(nu=nu):
                r = p / (1.0 + e * math.cos(nu))
                v = math.sqrt(MU * (2.0 / r - 1.0 / a))
                h = math.sqrt(MU * p)
                gamma = self.formula.evaluate(e=e, nu=nu)
                self.assert_close(math.cos(gamma), h / (r * v), rel_tol=1e-11)
                self.assertGreater(gamma, 0.0)  # outbound leg
                self.assert_close(
                    self.formula.evaluate(e=e, nu=-nu), -gamma
                )  # inbound leg mirrors it

    def test_tangent_route(self):
        for e, nu in ((0.2, 0.9), (0.9, 2.0), (1.5, 0.5)):
            with self.subTest(e=e, nu=nu):
                gamma = self.formula.evaluate(e=e, nu=nu)
                self.assert_close(
                    math.tan(gamma), e * math.sin(nu) / (1.0 + e * math.cos(nu)), rel_tol=1e-11
                )


class KeplerMeanAnomalyTest(_FormulaTest, unittest.TestCase):
    formula = kepler_mean_anomaly_from_eccentric_anomaly
    formula_id = "orbital.kepler_mean_anomaly_from_eccentric_anomaly"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"e": 0.5, "E": PI / 2.0}, 1.0707963267948966),
                ({"e": 0.0, "E": 1.7}, 1.7),
                ({"e": 0.9, "E": 3.5}, 3.8157049049206577),
                ({"e": 0.3, "E": 0.0}, 0.0),
            ]
        )

    def test_domain(self):
        self.assert_rejected(e=-0.01, E=1.0)
        self.assert_rejected(e=1.0, E=1.0)  # parabola is not an ellipse
        self.assert_rejected(e=1.5, E=1.0)

    def test_boundary_apsides_and_high_eccentricity(self):
        # M = E at E = 0 and E = pi for every e (sin vanishes there).
        self.assertEqual(self.formula.evaluate(e=0.8, E=0.0), 0.0)
        self.assert_close(self.formula.evaluate(e=0.8, E=PI), PI, abs_tol=1e-15)
        self.assert_close(self.formula.evaluate(e=0.999999, E=2.0), 2.0 - 0.999999 * math.sin(2.0))

    def test_no_wrapping_and_periodic_shift(self):
        for e, big_e in ((0.3, 1.0), (0.7, 4.0), (0.95, -2.5)):
            with self.subTest(e=e, E=big_e):
                shifted = self.formula.evaluate(e=e, E=big_e + 2.0 * PI)
                self.assert_close(shifted, self.formula.evaluate(e=e, E=big_e) + 2.0 * PI)

    def test_inverse_by_bisection(self):
        # Solve E - e sin E = M independently by bisection; the root must be the input E.
        for e, big_e in ((0.2, 0.8), (0.6, 2.5), (0.9, -1.3)):
            with self.subTest(e=e, E=big_e):
                m = self.formula.evaluate(e=e, E=big_e)
                lo, hi = -4.0, 4.0
                for _ in range(200):
                    mid = 0.5 * (lo + hi)
                    if mid - e * math.sin(mid) < m:
                        lo = mid
                    else:
                        hi = mid
                self.assert_close(0.5 * (lo + hi), big_e, rel_tol=1e-12)


def _beta_form_true_anomaly(e, big_e):
    """nu = E + 2 atan(beta sin E / (1 - beta cos E)), beta = e / (1 + sqrt(1 - e^2))."""
    beta = e / (1.0 + math.sqrt(1.0 - e * e))
    return big_e + 2.0 * math.atan(beta * math.sin(big_e) / (1.0 - beta * math.cos(big_e)))


class TrueAnomalyFromEccentricAnomalyTest(_FormulaTest, unittest.TestCase):
    formula = true_anomaly_from_eccentric_anomaly
    formula_id = "orbital.true_anomaly_from_eccentric_anomaly"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"e": 0.5, "E": PI / 2.0}, 2.0943951023931953),
                ({"e": 0.0, "E": 2.4}, 2.4),
                ({"e": 0.3, "E": 4.0}, 3.7895822925603033),
                ({"e": 0.8, "E": PI}, PI),
            ]
        )

    def test_domain(self):
        self.assert_rejected(e=-0.1, E=1.0)
        self.assert_rejected(e=1.0, E=1.0)
        self.assert_rejected(e=1.2, E=1.0)

    def test_boundary_revolution_ends(self):
        for e in (0.0, 0.5, 0.95):
            with self.subTest(e=e):
                self.assertEqual(self.formula.evaluate(e=e, E=0.0), 0.0)
                self.assert_close(self.formula.evaluate(e=e, E=2.0 * PI), 2.0 * PI)
                self.assert_close(self.formula.evaluate(e=e, E=-2.0 * PI), -2.0 * PI)
                self.assert_close(self.formula.evaluate(e=e, E=PI), PI)
                self.assert_close(self.formula.evaluate(e=e, E=-PI), -PI)

    def test_continuous_branch_and_extra_revolutions(self):
        # The result follows the input revolution, also beyond |E| = 2 pi.
        for e in (0.1, 0.6, 0.99):
            for k in (-3, -1, 0, 2, 5):
                for base in (0.4, 1.9, 3.3, 5.8):
                    big_e = base + 2.0 * PI * k
                    with self.subTest(e=e, E=big_e):
                        nu = self.formula.evaluate(e=e, E=big_e)
                        self.assert_close(
                            nu, self.formula.evaluate(e=e, E=base) + 2.0 * PI * k, rel_tol=1e-12
                        )
                        self.assertLess(abs(nu - big_e), PI)

    def test_monotone_without_jumps(self):
        previous = self.formula.evaluate(e=0.7, E=-13.0)
        for i in range(1, 2600):
            current = self.formula.evaluate(e=0.7, E=-13.0 + i * 0.01)
            self.assertGreater(current, previous)
            self.assertLess(current - previous, 0.2)
            previous = current

    def test_tangent_route(self):
        # R-158 relation tan(nu / 2) = sqrt((1 + e) / (1 - e)) tan(E / 2).
        for e, big_e in ((0.3, 0.7), (0.8, 2.5), (0.5, -1.2), (0.2, 5.5)):
            with self.subTest(e=e, E=big_e):
                nu = self.formula.evaluate(e=e, E=big_e)
                self.assert_close(
                    math.tan(0.5 * nu),
                    math.sqrt((1.0 + e) / (1.0 - e)) * math.tan(0.5 * big_e),
                    rel_tol=1e-11,
                )

    def test_cosine_and_beta_routes(self):
        for e in (0.15, 0.6, 0.92):
            for big_e in (-5.0, -2.0, 0.5, 1.5, 3.0, 4.5, 7.0, 10.0):
                with self.subTest(e=e, E=big_e):
                    nu = self.formula.evaluate(e=e, E=big_e)
                    self.assert_close(
                        math.cos(nu),
                        (math.cos(big_e) - e) / (1.0 - e * math.cos(big_e)),
                        abs_tol=1e-12,
                    )
                    self.assert_close(nu, _beta_form_true_anomaly(e, big_e), rel_tol=1e-11)


class EccentricAnomalyFromTrueAnomalyTest(_FormulaTest, unittest.TestCase):
    formula = eccentric_anomaly_from_true_anomaly
    formula_id = "orbital.eccentric_anomaly_from_true_anomaly"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"e": 0.5, "nu": 2.0943951023931953}, 1.5707963267948963),
                ({"e": 0.0, "nu": 2.4}, 2.4),
                ({"e": 0.3, "nu": 5.0}, 5.280319491381671),
                ({"e": 0.9, "nu": 0.1}, 0.02295970185248208),
            ]
        )

    def test_domain(self):
        self.assert_rejected(e=-0.1, nu=1.0)
        self.assert_rejected(e=1.0, nu=1.0)
        self.assert_rejected(e=1.2, nu=1.0)

    def test_boundary_revolution_ends(self):
        for e in (0.0, 0.5, 0.95):
            with self.subTest(e=e):
                self.assertEqual(self.formula.evaluate(e=e, nu=0.0), 0.0)
                self.assert_close(self.formula.evaluate(e=e, nu=2.0 * PI), 2.0 * PI)
                self.assert_close(self.formula.evaluate(e=e, nu=-2.0 * PI), -2.0 * PI)
                self.assert_close(self.formula.evaluate(e=e, nu=PI), PI)

    def test_round_trip_with_forward_conversion(self):
        for e in (0.1, 0.6, 0.97):
            for nu in (-8.0, -3.0, 0.2, 2.0, 3.5, 6.0, 9.5):
                with self.subTest(e=e, nu=nu):
                    big_e = self.formula.evaluate(e=e, nu=nu)
                    self.assert_close(
                        true_anomaly_from_eccentric_anomaly.evaluate(e=e, E=big_e),
                        nu,
                        rel_tol=1e-11,
                    )

    def test_cosine_sine_and_tangent_routes(self):
        # cos E = (e + cos nu) / (1 + e cos nu), sin E = sqrt(1 - e^2) sin nu / (1 + e cos nu),
        # whose quotient is the report's tan E = sqrt(1 - e^2) sin(nu) / (e + cos(nu)).
        for e in (0.15, 0.6, 0.92):
            for nu in (-5.0, -2.0, 0.5, 1.5, 3.0, 4.5, 7.0):
                with self.subTest(e=e, nu=nu):
                    big_e = self.formula.evaluate(e=e, nu=nu)
                    denominator = 1.0 + e * math.cos(nu)
                    self.assert_close(
                        math.cos(big_e), (e + math.cos(nu)) / denominator, abs_tol=1e-12
                    )
                    self.assert_close(
                        math.sin(big_e),
                        math.sqrt(1.0 - e * e) * math.sin(nu) / denominator,
                        abs_tol=1e-12,
                    )
                    self.assertLess(abs(big_e - nu), PI)

    def test_kepler_equation_consistency(self):
        # The mean anomaly of the converted angle matches a time-of-flight reading: at nu = pi
        # the body is at apoapsis, so M = pi.
        e = 0.4
        big_e = self.formula.evaluate(e=e, nu=PI)
        self.assert_close(big_e - e * math.sin(big_e), PI, abs_tol=1e-12)


class _HohmannTest(_FormulaTest):
    def test_domain(self):
        self.assert_rejected(mu=0.0, r1=7.0e6, r2=4.2e7)
        self.assert_rejected(mu=-MU, r1=7.0e6, r2=4.2e7)
        self.assert_rejected(mu=MU, r1=0.0, r2=4.2e7)
        self.assert_rejected(mu=MU, r1=-7.0e6, r2=4.2e7)
        self.assert_rejected(mu=MU, r1=7.0e6, r2=0.0)
        self.assert_rejected(mu=MU, r1=7.0e6, r2=-4.2e7)

    def test_overflow_of_radius_sum(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(mu=MU, r1=1.0e308, r2=1.0e308)


class HohmannFirstImpulseTest(_HohmannTest, unittest.TestCase):
    formula = hohmann_first_impulse
    formula_id = "orbital.hohmann_first_impulse"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "r1": 6678000.0, "r2": 42164000.0}, 2425.769028306859),
                ({"mu": MU, "r1": 7.0e6, "r2": 7.0e6}, 0.0),
                ({"mu": MU, "r1": 42164000.0, "r2": 6678000.0}, -1466.8387152844527),
            ]
        )

    def test_boundary_equal_radii_and_large_ratio(self):
        self.assertEqual(self.formula.evaluate(mu=MU, r1=9.0e6, r2=9.0e6), 0.0)
        # r2 >> r1: the transfer ellipse tends to a parabola, dv1 -> (sqrt(2) - 1) v_circular.
        v_c = math.sqrt(MU / 7.0e6)
        self.assert_close(
            self.formula.evaluate(mu=MU, r1=7.0e6, r2=1.0e18), (math.sqrt(2.0) - 1.0) * v_c, 1e-8
        )

    def test_vis_viva_route(self):
        # dv1 = v at the transfer ellipse's initial apse (vis-viva, a = (r1 + r2) / 2) minus the
        # circular speed.
        for r1, r2 in ((6.678e6, 4.2164e7), (4.2164e7, 6.678e6), (7.0e6, 1.2e7)):
            with self.subTest(r1=r1, r2=r2):
                a_trans = 0.5 * (r1 + r2)
                expected = math.sqrt(MU * (2.0 / r1 - 1.0 / a_trans)) - math.sqrt(MU / r1)
                self.assert_close(self.formula.evaluate(mu=MU, r1=r1, r2=r2), expected, 1e-11)

    def test_sign_and_reversal_identity(self):
        raising = self.formula.evaluate(mu=MU, r1=7.0e6, r2=2.0e7)
        lowering = self.formula.evaluate(mu=MU, r1=2.0e7, r2=7.0e6)
        self.assertGreater(raising, 0.0)
        self.assertLess(lowering, 0.0)
        # Running the transfer backwards swaps the burns: dv1(r1, r2) = -dv2(r2, r1).
        self.assert_close(
            self.formula.evaluate(mu=MU, r1=7.0e6, r2=2.0e7),
            -hohmann_second_impulse.evaluate(mu=MU, r1=2.0e7, r2=7.0e6),
        )


class HohmannSecondImpulseTest(_HohmannTest, unittest.TestCase):
    formula = hohmann_second_impulse
    formula_id = "orbital.hohmann_second_impulse"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "r1": 6678000.0, "r2": 42164000.0}, 1466.8387152844527),
                ({"mu": MU, "r1": 7.0e6, "r2": 7.0e6}, 0.0),
                ({"mu": MU, "r1": 42164000.0, "r2": 6678000.0}, -2425.769028306859),
            ]
        )

    def test_boundary_equal_radii_and_large_ratio(self):
        self.assertEqual(self.formula.evaluate(mu=MU, r1=9.0e6, r2=9.0e6), 0.0)
        # r2 >> r1: the transfer speed at the far apse tends to zero, so dv2 -> v_circular(r2).
        self.assert_close(
            self.formula.evaluate(mu=MU, r1=7.0e6, r2=1.0e18), math.sqrt(MU / 1.0e18), 1e-5
        )

    def test_vis_viva_route(self):
        # dv2 = circular speed at the final orbit minus the transfer ellipse's speed there.
        for r1, r2 in ((6.678e6, 4.2164e7), (4.2164e7, 6.678e6), (7.0e6, 1.2e7)):
            with self.subTest(r1=r1, r2=r2):
                a_trans = 0.5 * (r1 + r2)
                expected = math.sqrt(MU / r2) - math.sqrt(MU * (2.0 / r2 - 1.0 / a_trans))
                self.assert_close(self.formula.evaluate(mu=MU, r1=r1, r2=r2), expected, 1e-11)

    def test_total_delta_v_matches_sum(self):
        # Total of a raising transfer, summed from the two oracle burn values.
        total = hohmann_first_impulse.evaluate(
            mu=MU, r1=6678000.0, r2=42164000.0
        ) + self.formula.evaluate(mu=MU, r1=6678000.0, r2=42164000.0)
        self.assert_close(total, 2425.769028306859 + 1466.8387152844527)


class HohmannTransferTimeTest(_HohmannTest, unittest.TestCase):
    formula = hohmann_transfer_time
    formula_id = "orbital.hohmann_transfer_time"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"mu": MU, "r1": 6678000.0, "r2": 42164000.0}, 18990.051838481286),
                ({"mu": MU, "r1": 7.0e6, "r2": 7.0e6}, 2914.2583188430076),
                ({"mu": MU, "r1": 42164000.0, "r2": 6678000.0}, 18990.051838481286),
            ]
        )

    def test_boundary_equal_radii_is_half_circular_period(self):
        r = 8.0e6
        half_period = PI * math.sqrt(r**3 / MU)
        self.assert_close(self.formula.evaluate(mu=MU, r1=r, r2=r), half_period)

    def test_large_radii_do_not_overflow_the_cube(self):
        # The cube of the semi-major axis (1e309) is past the float range; the time is not.
        t = self.formula.evaluate(mu=1.0e200, r1=1.0e103, r2=1.0e103)
        self.assert_close(t, PI * 1.0e103 * math.sqrt(1.0e103 / 1.0e200))

    def test_half_period_and_kepler_equation_routes(self):
        r1, r2 = 6.678e6, 4.2164e7
        a_trans = 0.5 * (r1 + r2)
        t = self.formula.evaluate(mu=MU, r1=r1, r2=r2)
        # Half of the transfer ellipse's period 2 pi sqrt(a^3 / mu).
        self.assert_close(t, 0.5 * 2.0 * PI * math.sqrt(a_trans**3 / MU))
        # Kepler's equation from periapsis (E = 0) to apoapsis (E = pi): t = (E - e sin E) / n.
        e = (r2 - r1) / (r2 + r1)
        n = math.sqrt(MU / a_trans**3)
        self.assert_close(t, (PI - e * math.sin(PI)) / n, abs_tol=1e-9)

    def test_symmetric_in_radii(self):
        self.assert_close(
            self.formula.evaluate(mu=MU, r1=7.0e6, r2=2.0e7),
            self.formula.evaluate(mu=MU, r1=2.0e7, r2=7.0e6),
        )


if __name__ == "__main__":
    unittest.main()

"""Regression tests for the e2 review fixes of the orbital formulas.

Expected values are 50-digit mpmath evaluations of the plain, unrearranged equations at the exact
float inputs (script `fix_oracles/oracles.py` in the review scratch directory), so they do not
depend on the evaluators' cancellation-free rewrites. The J2 cases also reproduce the nodal-rate
expression printed in NASA TM X-73433, eq. (1), written in terms of the semilatus rectum p.
"""

import math
import unittest

from sciengformulary.catalog.orbital.bielliptic_total_delta_v import bielliptic_total_delta_v
from sciengformulary.catalog.orbital.circular_orbit_speed import circular_orbit_speed
from sciengformulary.catalog.orbital.conic_orbit_radius import conic_orbit_radius
from sciengformulary.catalog.orbital.edelbaum_delta_v import edelbaum_delta_v
from sciengformulary.catalog.orbital.flight_path_angle import flight_path_angle
from sciengformulary.catalog.orbital.hohmann_first_impulse import hohmann_first_impulse
from sciengformulary.catalog.orbital.hohmann_second_impulse import hohmann_second_impulse
from sciengformulary.catalog.orbital.hohmann_transfer_time import hohmann_transfer_time
from sciengformulary.catalog.orbital.hyperbolic_asymptote_true_anomaly import (
    hyperbolic_asymptote_true_anomaly,
)
from sciengformulary.catalog.orbital.hyperbolic_kepler_mean_anomaly import (
    hyperbolic_kepler_mean_anomaly,
)
from sciengformulary.catalog.orbital.j2_nodal_precession_rate import j2_nodal_precession_rate
from sciengformulary.catalog.orbital.kepler_mean_anomaly_from_eccentric_anomaly import (
    kepler_mean_anomaly_from_eccentric_anomaly,
)
from sciengformulary.catalog.orbital.keplerian_mean_motion import keplerian_mean_motion
from sciengformulary.catalog.orbital.laplace_sphere_of_influence_radius import (
    laplace_sphere_of_influence_radius,
)
from sciengformulary.catalog.orbital.semi_latus_rectum import semi_latus_rectum
from sciengformulary.catalog.orbital.specific_angular_momentum import specific_angular_momentum
from sciengformulary.catalog.orbital.vis_viva_speed import vis_viva_speed

MU = 398600441800000.0


class _Close:
    def assert_close(self, actual, expected, rel_tol=1e-13):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=rel_tol),
            f"got {actual!r}, expected {expected!r}",
        )


class J2ReferenceAndRangeTest(_Close, unittest.TestCase):
    def test_reference_is_nasa_report_not_conference_paper(self):
        numbers = [r.report_number for r in j2_nodal_precession_rate.references]
        self.assertIn("NASA TM X-73433", numbers)
        self.assertIn("NASA TN D-1045", numbers)
        for ref in j2_nodal_precession_rate.references:
            self.assertNotIn("Leonardo", ref.title)
            self.assertNotIn("20090013858", ref.url or "")

    def test_borsody_semilatus_rectum_form(self):
        # rate = -J sqrt(mu) R^2 p^(-7/2) (1 - e^2)^(3/2) cos i with J = 1.5 J2 and p = a (1 - e^2).
        rate = j2_nodal_precession_rate.evaluate(
            mu=MU, a=26554000.0, e=0.7, i=1.106538745764405, R_e=6378137.0, J2=0.00108263
        )
        self.assert_close(rate, -2.3532990527964748e-08)
        rate = j2_nodal_precession_rate.evaluate(
            mu=MU, a=7.0e6, e=0.999, i=0.5, R_e=6378137.0, J2=0.00108263
        )
        self.assert_close(rate, -0.3191884353931042)

    def test_extreme_semi_major_axis_raises_the_documented_errors(self):
        for a in (1e-110, 1e-120, 1e-160):
            with self.assertRaises((ValueError, OverflowError)) as ctx:
                j2_nodal_precession_rate.evaluate(
                    mu=MU, a=a, e=0.1, i=0.5, R_e=6378137.0, J2=0.00108263
                )
            self.assertNotIsInstance(ctx.exception, ZeroDivisionError)

    def test_large_semi_major_axis_does_not_overflow_in_the_cube(self):
        rate = j2_nodal_precession_rate.evaluate(
            mu=MU, a=1e120, e=0.1, i=0.5, R_e=6378137.0, J2=0.00108263
        )
        self.assertTrue(math.isfinite(rate))
        self.assertLessEqual(abs(rate), 1e-300)


class CancellationFreeFormsTest(_Close, unittest.TestCase):
    def test_semi_latus_rectum_near_parabola(self):
        self.assert_close(semi_latus_rectum.evaluate(a=1.0e9, e=1.0 - 1e-9), 1.9999999424361372)
        self.assert_close(
            semi_latus_rectum.evaluate(a=7.0e6, e=1.0 - 2.0**-50), 1.2434497875801748e-08
        )

    def test_vis_viva_near_twice_the_semi_major_axis(self):
        r = 13999999.999999994  # 2 a (1 - 3 * 2**-53) for a = 7e6
        self.assert_close(vis_viva_speed.evaluate(mu=MU, r=r, a=7.0e6), 0.00015075840715719335)
        self.assert_close(vis_viva_speed.evaluate(mu=MU, r=1.0e7, a=-3.0e7), 9644.001749965277)

    def test_hohmann_impulses_for_nearly_equal_radii(self):
        r1 = 7.0e6
        cases = (
            (7000000.0007, 1.8865126276597834e-07, 1.8865126276126203e-07),
            (7000000.000000001, 2.509932063688771e-13, 2.5099320636887703e-13),
            (6999999.9993, -1.8865126278955973e-07, -1.8865126279427601e-07),
        )
        for r2, dv1, dv2 in cases:
            self.assert_close(hohmann_first_impulse.evaluate(mu=MU, r1=r1, r2=r2), dv1)
            self.assert_close(hohmann_second_impulse.evaluate(mu=MU, r1=r1, r2=r2), dv2)

    def test_hohmann_equal_radii_stay_zero(self):
        self.assertEqual(hohmann_first_impulse.evaluate(mu=MU, r1=7.0e6, r2=7.0e6), 0.0)
        self.assertEqual(hohmann_second_impulse.evaluate(mu=MU, r1=7.0e6, r2=7.0e6), 0.0)

    def test_edelbaum_close_radii(self):
        a1 = 7000000.000007001
        self.assert_close(
            edelbaum_delta_v.evaluate(mu=MU, a0=7.0e6, a1=a1, di=0.0), 3.773431864546867e-09
        )
        self.assert_close(
            edelbaum_delta_v.evaluate(mu=MU, a0=7.0e6, a1=a1, di=0.3), 3523.1823119695337
        )

    def test_kepler_equation_near_the_parabola(self):
        f = kepler_mean_anomaly_from_eccentric_anomaly.evaluate
        self.assert_close(f(e=0.999999, E=1e-3), 1.1666664916954309e-09)
        self.assert_close(f(e=1.0 - 2.0**-40, E=1e-5), 1.7576161368341107e-16)
        self.assert_close(f(e=0.3, E=0.4999), 0.35609866661469025)
        self.assert_close(f(e=0.9, E=-0.2), -0.021197602284444905)
        self.assert_close(f(e=0.5, E=0.5), 0.2602872306978985)

    def test_hyperbolic_kepler_equation_near_the_parabola(self):
        f = hyperbolic_kepler_mean_anomaly.evaluate
        self.assert_close(f(e=1 + 1e-10, H=1e-4), 1.766666675940704e-13)
        self.assert_close(f(e=1 + 2.0**-40, H=1e-5), 1.757616136853809e-16)
        self.assert_close(f(e=1.5, H=0.3), 0.1567804401707139)
        self.assert_close(f(e=2.0, H=-0.2), -0.202672005082188)
        self.assert_close(f(e=1.2, H=0.5), 0.1253143665924968)


class EdelbaumRangeTest(_Close, unittest.TestCase):
    def test_plane_change_above_pi_is_rejected(self):
        for di in (math.nextafter(math.pi, 10.0), 4.0, 1e300):
            with self.assertRaises(ValueError):
                edelbaum_delta_v.evaluate(mu=MU, a0=7.0e6, a1=4.2164e7, di=di)

    def test_plane_change_of_pi_is_accepted(self):
        value = edelbaum_delta_v.evaluate(mu=MU, a0=7.0e6, a1=4.2164e7, di=math.pi)
        self.assert_close(value, 7494.043607050908)


class UnderflowTest(_Close, unittest.TestCase):
    def test_sphere_of_influence_extreme_mass_ratio_is_not_zero(self):
        f = laplace_sphere_of_influence_radius.evaluate
        self.assert_close(f(a=1.0, m=1e-300, M=1e300), 1e-240)
        self.assert_close(f(a=1e5, m=1e-300, M=1e300), 1e-235)

    def test_sphere_of_influence_underflowing_result_raises(self):
        with self.assertRaises(OverflowError):
            laplace_sphere_of_influence_radius.evaluate(a=1e-200, m=1e-300, M=1e300)

    def test_mean_motion_underflowing_result_raises(self):
        with self.assertRaises(OverflowError):
            keplerian_mean_motion.evaluate(mu=1e-300, a=1e300)


class SecondSourceTest(unittest.TestCase):
    def test_former_single_brunner_formulas_have_a_second_nasa_report(self):
        second = {
            "NASA SP-325": (
                circular_orbit_speed,
                vis_viva_speed,
                hohmann_first_impulse,
                hohmann_second_impulse,
                hohmann_transfer_time,
                bielliptic_total_delta_v,
                conic_orbit_radius,
                flight_path_angle,
                semi_latus_rectum,
                specific_angular_momentum,
                hyperbolic_asymptote_true_anomaly,
            ),
            "NASA TM X-53485": (laplace_sphere_of_influence_radius,),
        }
        for number, formulas in second.items():
            for formula in formulas:
                numbers = [r.report_number for r in formula.references]
                self.assertIn(number, numbers, formula.id)
                self.assertIn("NASA/CR-2005-213034", numbers, formula.id)
                for ref in formula.references:
                    if ref.report_number == number:
                        self.assertTrue(ref.locator, formula.id)
                        self.assertTrue(ref.url.startswith("https://ntrs.nasa.gov/"), formula.id)


if __name__ == "__main__":
    unittest.main()

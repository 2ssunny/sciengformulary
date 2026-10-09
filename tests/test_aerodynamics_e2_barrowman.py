"""Tests for the e2 Barrowman-method formulas (fins, noses, transitions, body center of pressure).

Reference values are 50-digit mpmath evaluations of the cited equations at the inputs listed in
each test (mpmath.mp.dps = 50; mpmath.quad of the defining integrals of the mean aerodynamic
chord, the body area and volume integrals, and exact arithmetic), rounded to a double. The
independent-route checks for the derived formulas use a plain Simpson quadrature written here,
not the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED
from sciengformulary.catalog.aerodynamics.conical_transition_center_of_pressure import (
    conical_transition_center_of_pressure,
)
from sciengformulary.catalog.aerodynamics.conical_transition_normal_force_slope import (
    conical_transition_normal_force_slope,
)
from sciengformulary.catalog.aerodynamics.nose_normal_force_slope import nose_normal_force_slope
from sciengformulary.catalog.aerodynamics.power_series_nose_center_of_pressure import (
    power_series_nose_center_of_pressure,
)
from sciengformulary.catalog.aerodynamics.single_fin_normal_force_slope import (
    single_fin_normal_force_slope,
)
from sciengformulary.catalog.aerodynamics.slender_body_center_of_pressure_from_volume import (
    slender_body_center_of_pressure_from_volume,
)
from sciengformulary.catalog.aerodynamics.trapezoid_mac_spanwise_location import (
    trapezoid_mac_spanwise_location,
)
from sciengformulary.catalog.aerodynamics.trapezoidal_fin_center_of_pressure import (
    trapezoidal_fin_center_of_pressure,
)
from sciengformulary.core import FormulaSpec

REL = 1e-11
REPORT_NUMBER = "NASA/TM-2001-209983"
SOURCE_URL = "https://ntrs.nasa.gov/citations/20010047838"


def simpson(function, a, b, panels=2000):
    """Composite Simpson rule on [a, b] with an even number of panels."""
    step = (b - a) / panels
    total = function(a) + function(b)
    for index in range(1, panels):
        total += function(a + index * step) * (4 if index % 2 else 2)
    return total * step / 3.0


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
                self.assert_close(
                    self.formula.evaluate(**inputs), expected, rel_tol=rel_tol, abs_tol=1e-15
                )

    def assert_rejected(self, **inputs):
        with self.subTest(**inputs):
            with self.assertRaises(ValueError):
                self.formula.evaluate(**inputs)

    def test_constructed(self):
        self.assertEqual(self.formula.id, self.formula_id)
        self.assertTrue(self.formula.verification_cases)
        self.assertEqual(len(self.formula.references), 1)
        reference = self.formula.references[0]
        self.assertEqual(reference.report_number, REPORT_NUMBER)
        self.assertEqual(reference.url, SOURCE_URL)
        self.assertEqual(reference.accessed, ENGINEERING_ACCESSED)
        self.assertEqual(reference.authors, ("J. S. Barrowman",))
        self.assertTrue(reference.locator)

    def test_verification_cases_pass(self):
        self.formula.verify()

    def test_non_finite_inputs_rejected(self):
        base = dict(self.formula.verification_cases[0].inputs)
        for name in base:
            for bad in (math.nan, math.inf, -math.inf):
                with self.subTest(name=name, bad=bad):
                    with self.assertRaises(ValueError):
                        self.formula.evaluate(**{**base, name: bad})

    def test_states_method_assumptions(self):
        text = " ".join(self.formula.assumptions).lower()
        self.assertIn("subsonic", text)
        self.assertIn("consistent", text)


class SingleFinNormalForceSlopeTest(_FormulaTest, unittest.TestCase):
    formula = single_fin_normal_force_slope
    formula_id = "aerodynamics.single_fin_normal_force_slope"

    def test_oracle(self):
        self.assert_oracle(
            [
                (
                    {
                        "Cla": 6.283185307179586,
                        "AR": 2.2222222222222228,
                        "Gc": 0.2914567944778671,
                        "A_f": 0.009,
                        "A_ref": 0.012667686977437444,
                    },
                    1.959269389119581,
                ),
                (
                    {"Cla": 7.255197456936872, "AR": 1.0, "Gc": 0.3, "A_f": 0.004, "A_ref": 0.0125},
                    0.479192122133112,
                ),
                (
                    {"Cla": 6.283185307179586, "AR": 0.01, "Gc": 0.0, "A_f": 0.001, "A_ref": 0.01},
                    0.0015707865094405707,
                ),
            ]
        )

    def test_matches_substituted_form(self):
        # Eq. (3-6) is (3-1) with beta = 2 pi / Cla substituted: written out independently here.
        for beta, aspect, sweep, fin_area, ref_area in (
            (1.0, 2.0, 0.3, 0.004, 0.0125),
            (0.8, 1.5, -0.4, 0.01, 0.02),
            (0.5, 0.7, 1.0, 0.002, 0.03),
        ):
            with self.subTest(beta=beta, aspect=aspect, sweep=sweep):
                expected = (
                    2.0
                    * math.pi
                    * aspect
                    * (fin_area / ref_area)
                    / (2.0 + math.sqrt(4.0 + (beta * aspect / math.cos(sweep)) ** 2))
                )
                actual = self.formula.evaluate(
                    Cla=2.0 * math.pi / beta,
                    AR=aspect,
                    Gc=sweep,
                    A_f=fin_area,
                    A_ref=ref_area,
                )
                self.assert_close(actual, expected, rel_tol=1e-13)

    def test_sweep_is_symmetric(self):
        inputs = {"Cla": 6.0, "AR": 1.2, "A_f": 0.004, "A_ref": 0.0125}
        self.assert_close(
            self.formula.evaluate(Gc=0.5, **inputs), self.formula.evaluate(Gc=-0.5, **inputs)
        )

    def test_scales_with_area_ratio(self):
        inputs = {"Cla": 6.0, "AR": 1.2, "Gc": 0.2, "A_ref": 0.0125}
        self.assert_close(
            self.formula.evaluate(A_f=0.008, **inputs),
            2.0 * self.formula.evaluate(A_f=0.004, **inputs),
        )

    def test_invalid_inputs_rejected(self):
        good = {"Cla": 6.0, "AR": 1.2, "Gc": 0.2, "A_f": 0.004, "A_ref": 0.0125}
        for name in ("Cla", "AR", "A_f", "A_ref"):
            for bad in (0.0, -1.0):
                self.assert_rejected(**{**good, name: bad})
        for bad in (math.pi / 2, -math.pi / 2, 2.0):
            self.assert_rejected(**{**good, "Gc": bad})
        self.assert_rejected(**{**good, "Gc": True})

    def test_sweep_just_inside_limit_accepted(self):
        value = self.formula.evaluate(Cla=6.0, AR=1.2, Gc=1.5, A_f=0.004, A_ref=0.0125)
        self.assertGreater(value, 0.0)

    def test_tiny_aspect_ratio_has_no_false_overflow(self):
        # (2 / F_D)^2 overflowed for AR below about 1e-154 although the slope is finite and
        # tends to Cla F_D (A_f / A_ref) cos(Gc) / 4. 50-digit mpmath value of eq. (3-6).
        got = self.formula.evaluate(
            Cla=6.283185307179586, AR=1e-300, Gc=0.3, A_f=0.004, A_ref=0.0125
        )
        self.assert_close(got, 5.026548245743669e-301, rel_tol=1e-12)

    def test_aspect_ratio_convention_is_stated_plainly(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("prints no formula", text)
        self.assertIn("AR = 2 s^2 / A_f", text)
        self.assertIn("AR = s^2 / A_f", text)
        for case in self.formula.verification_cases:
            self.assertIn("AR", case.note)
        # Halving AR (the other convention) changes this case's slope by a factor of 1.70.
        first = self.formula.verification_cases[0].inputs
        full = self.formula.evaluate(**first)
        half = self.formula.evaluate(**{**first, "AR": first["AR"] / 2.0})
        self.assertGreater(full / half, 1.5)
        self.assertLess(full / half, 2.0)


class TrapezoidalFinCenterOfPressureTest(_FormulaTest, unittest.TestCase):
    formula = trapezoidal_fin_center_of_pressure
    formula_id = "aerodynamics.trapezoidal_fin_center_of_pressure"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"c_r": 0.12, "c_t": 0.06, "x_t": 0.06}, 0.049999999999999996),
                ({"c_r": 0.2, "c_t": 0.2, "x_t": 0.0}, 0.05),
                ({"c_r": 0.1, "c_t": 0.0, "x_t": 0.1}, 0.05),
                ({"c_r": 0.3, "c_t": 0.1, "x_t": 0.25}, 0.15833333333333333),
            ]
        )

    def test_matches_mean_chord_quadrature(self):
        # Independent route: integrate c^2 over the span for the mean chord (3-13), find where
        # the chord equals it by bisection, and take the quarter-chord point behind the leading
        # edge at that station.
        for c_r, c_t, span, x_t in (
            (0.12, 0.06, 0.1, 0.06),
            (0.3, 0.1, 0.12, 0.25),
            (0.1, 0.0, 0.05, 0.1),
            (0.25, 0.2, 0.08, -0.03),
        ):
            with self.subTest(c_r=c_r, c_t=c_t, x_t=x_t):

                def chord(y, c_r=c_r, c_t=c_t, span=span):
                    return c_r + (c_t - c_r) * y / span

                area = (c_r + c_t) * span / 2.0
                mean_chord = simpson(lambda y: chord(y) ** 2, 0.0, span) / area
                low, high = 0.0, span
                for _ in range(200):
                    mid = (low + high) / 2.0
                    if (chord(mid) - mean_chord) * (chord(low) - mean_chord) <= 0:
                        high = mid
                    else:
                        low = mid
                station = (low + high) / 2.0
                expected = x_t * station / span + mean_chord / 4.0
                actual = self.formula.evaluate(x_t=x_t, c_r=c_r, c_t=c_t)
                self.assert_close(actual, expected, rel_tol=1e-9)

    def test_rectangular_fin_is_quarter_chord(self):
        self.assert_close(self.formula.evaluate(x_t=0.0, c_r=0.4, c_t=0.4), 0.1)

    def test_offset_adds_linearly_with_sweep(self):
        base = self.formula.evaluate(x_t=0.0, c_r=0.3, c_t=0.1)
        shifted = self.formula.evaluate(x_t=0.12, c_r=0.3, c_t=0.1)
        self.assert_close(shifted - base, 0.12 * (0.3 + 0.2) / (3.0 * 0.4))

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(x_t=0.0, c_r=-0.1, c_t=0.1)
        self.assert_rejected(x_t=0.0, c_r=0.1, c_t=-0.1)
        self.assert_rejected(x_t=0.0, c_r=0.0, c_t=0.0)

    def test_tiny_lengths_do_not_lose_the_result(self):
        # With c_r = c_t = x_t = 1e-200 the products x_t * (c_r + 2 c_t) and c_r * c_t
        # underflowed, giving 3.33e-201 instead of the 50-digit mpmath value 7.5e-201.
        self.assert_close(
            self.formula.evaluate(x_t=1e-200, c_r=1e-200, c_t=1e-200), 7.5e-201, rel_tol=1e-12
        )

    def test_zero_root_chord_accepted(self):
        # c_r = 0 with c_t > 0 is a degenerate but defined planform (inverted delta).
        self.assertTrue(math.isfinite(self.formula.evaluate(x_t=0.0, c_r=0.0, c_t=0.1)))


class TrapezoidMacSpanwiseLocationTest(_FormulaTest, unittest.TestCase):
    formula = trapezoid_mac_spanwise_location
    formula_id = "aerodynamics.trapezoid_mac_spanwise_location"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"c_r": 0.12, "c_t": 0.06, "s": 0.1}, 0.044444444444444446),
                ({"c_r": 0.2, "c_t": 0.2, "s": 0.15}, 0.075),
                ({"c_r": 0.1, "c_t": 0.0, "s": 0.05}, 0.016666666666666666),
                ({"c_r": 0.3, "c_t": 0.1, "s": 0.12}, 0.049999999999999996),
            ]
        )

    def test_chord_there_equals_mean_chord(self):
        # The defining property: the local chord at Y_mac equals the mean aerodynamic chord.
        for c_r, c_t, span in ((0.12, 0.06, 0.1), (0.3, 0.1, 0.12), (0.05, 0.4, 0.2)):
            with self.subTest(c_r=c_r, c_t=c_t):
                station = self.formula.evaluate(c_r=c_r, c_t=c_t, s=span)
                local_chord = c_r + (c_t - c_r) * station / span
                area = (c_r + c_t) * span / 2.0
                mean_chord = simpson(lambda y: (c_r + (c_t - c_r) * y / span) ** 2, 0, span) / area
                self.assert_close(local_chord, mean_chord, rel_tol=1e-9)

    def test_lies_within_span(self):
        for c_r, c_t in ((1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.3, 0.2)):
            value = self.formula.evaluate(c_r=c_r, c_t=c_t, s=2.0)
            self.assertTrue(0.0 <= value <= 2.0)

    def test_scales_with_span(self):
        self.assert_close(
            self.formula.evaluate(c_r=0.3, c_t=0.1, s=0.24),
            2.0 * self.formula.evaluate(c_r=0.3, c_t=0.1, s=0.12),
        )

    def test_tiny_lengths_do_not_underflow_to_zero(self):
        # 50-digit mpmath value of (s/3)(c_r + 2 c_t)/(c_r + c_t) at s = 1e-200, c_r = 3e-200,
        # c_t = 1e-200 is 4.1666...e-201; the product used to underflow to 0.0.
        self.assert_close(
            self.formula.evaluate(s=1e-200, c_r=3e-200, c_t=1e-200), 4.166666666666666e-201
        )

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(c_r=0.1, c_t=0.1, s=0.0)
        self.assert_rejected(c_r=0.1, c_t=0.1, s=-0.1)
        self.assert_rejected(c_r=-0.1, c_t=0.1, s=0.1)
        self.assert_rejected(c_r=0.1, c_t=-0.1, s=0.1)
        self.assert_rejected(c_r=0.0, c_t=0.0, s=0.1)


class NoseNormalForceSlopeTest(_FormulaTest, unittest.TestCase):
    formula = nose_normal_force_slope
    formula_id = "aerodynamics.nose_normal_force_slope"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"r_base": 0.05, "r_ref": 0.05}, 2.0),
                ({"r_base": 0.03, "r_ref": 0.0635}, 0.4464008928017856),
                ({"r_base": 0.0, "r_ref": 0.05}, 0.0),
            ],
            rel_tol=1e-12,
        )

    def test_matches_area_ratio_form(self):
        # Eq. (3-66) as printed: 2 A_BN / A_r with circular areas.
        for r_base, r_ref in ((0.03, 0.0635), (0.1, 0.05), (0.02, 0.02)):
            with self.subTest(r_base=r_base, r_ref=r_ref):
                expected = 2.0 * (math.pi * r_base**2) / (math.pi * r_ref**2)
                self.assert_close(
                    self.formula.evaluate(r_base=r_base, r_ref=r_ref), expected, rel_tol=1e-13
                )

    def test_is_conical_transition_from_a_point(self):
        for r_aft, r_ref in ((0.03, 0.0635), (0.05, 0.05)):
            self.assert_close(
                self.formula.evaluate(r_base=r_aft, r_ref=r_ref),
                conical_transition_normal_force_slope.evaluate(r_fwd=0.0, r_aft=r_aft, r_ref=r_ref),
                rel_tol=1e-13,
            )

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(r_base=-0.01, r_ref=0.05)
        self.assert_rejected(r_base=0.01, r_ref=0.0)
        self.assert_rejected(r_base=0.01, r_ref=-0.05)


class ConicalTransitionNormalForceSlopeTest(_FormulaTest, unittest.TestCase):
    formula = conical_transition_normal_force_slope
    formula_id = "aerodynamics.conical_transition_normal_force_slope"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"r_fwd": 0.05, "r_aft": 0.04, "r_ref": 0.05}, -0.72),
                ({"r_fwd": 0.03, "r_aft": 0.05, "r_ref": 0.05}, 1.28),
                ({"r_fwd": 0.05, "r_aft": 0.05, "r_ref": 0.05}, 0.0),
            ],
            rel_tol=1e-12,
        )

    def test_matches_end_area_difference(self):
        # Eq. (3-65): 2 [A(l_0) - A(0)] / A_r with circular end areas.
        for r_fwd, r_aft, r_ref in ((0.03, 0.05, 0.05), (0.06, 0.02, 0.0635), (0.0, 0.04, 0.04)):
            with self.subTest(r_fwd=r_fwd, r_aft=r_aft):
                expected = 2.0 * (math.pi * r_aft**2 - math.pi * r_fwd**2) / (math.pi * r_ref**2)
                self.assert_close(
                    self.formula.evaluate(r_fwd=r_fwd, r_aft=r_aft, r_ref=r_ref),
                    expected,
                    rel_tol=1e-12,
                    abs_tol=1e-15,
                )

    def test_sign_follows_taper_direction(self):
        self.assertGreater(self.formula.evaluate(r_fwd=0.02, r_aft=0.04, r_ref=0.05), 0.0)
        self.assertLess(self.formula.evaluate(r_fwd=0.04, r_aft=0.02, r_ref=0.05), 0.0)

    def test_contributions_telescope(self):
        # Two transitions in series add to one from the first start to the last end.
        first = self.formula.evaluate(r_fwd=0.02, r_aft=0.04, r_ref=0.05)
        second = self.formula.evaluate(r_fwd=0.04, r_aft=0.03, r_ref=0.05)
        whole = self.formula.evaluate(r_fwd=0.02, r_aft=0.03, r_ref=0.05)
        self.assert_close(first + second, whole, rel_tol=1e-12)

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(r_fwd=-0.01, r_aft=0.04, r_ref=0.05)
        self.assert_rejected(r_fwd=0.01, r_aft=-0.04, r_ref=0.05)
        self.assert_rejected(r_fwd=0.01, r_aft=0.04, r_ref=0.0)
        self.assert_rejected(r_fwd=0.01, r_aft=0.04, r_ref=-0.05)


class ConicalTransitionCenterOfPressureTest(_FormulaTest, unittest.TestCase):
    formula = conical_transition_center_of_pressure
    formula_id = "aerodynamics.conical_transition_center_of_pressure"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"L": 0.1, "r_fwd": 0.03, "r_aft": 0.05}, 0.05416666666666667),
                ({"L": 0.1, "r_fwd": 0.05, "r_aft": 0.04}, 0.04814814814814815),
                ({"L": 0.2, "r_fwd": 0.0, "r_aft": 0.05}, 0.13333333333333333),
            ]
        )

    def test_matches_area_moment_quadrature(self):
        # Independent route: x_cp = integral of x dA/dx over the frustum divided by the area
        # change (eqs. 3-83, 3-65), with A = pi r(x)^2 and a linear radius profile.
        for length, r_fwd, r_aft in ((0.1, 0.03, 0.05), (0.1, 0.05, 0.04), (0.3, 0.0, 0.06)):
            with self.subTest(length=length, r_fwd=r_fwd, r_aft=r_aft):
                slope = (r_aft - r_fwd) / length

                def area_rate(x, r_fwd=r_fwd, slope=slope):
                    return 2.0 * math.pi * (r_fwd + slope * x) * slope

                moment = simpson(lambda x, f=area_rate: x * f(x), 0.0, length)
                area_change = math.pi * (r_aft**2 - r_fwd**2)
                actual = self.formula.evaluate(L=length, r_fwd=r_fwd, r_aft=r_aft)
                self.assert_close(actual, moment / area_change, rel_tol=1e-9)

    def test_matches_volume_form(self):
        # x_cp = (L A(L) - V) / (A(L) - A(0)) with the frustum volume written out.
        for length, r_fwd, r_aft in ((0.1, 0.03, 0.05), (0.2, 0.06, 0.02)):
            with self.subTest(length=length, r_fwd=r_fwd, r_aft=r_aft):
                volume = math.pi * length / 3.0 * (r_fwd**2 + r_fwd * r_aft + r_aft**2)
                expected = (length * math.pi * r_aft**2 - volume) / (
                    math.pi * r_aft**2 - math.pi * r_fwd**2
                )
                actual = self.formula.evaluate(L=length, r_fwd=r_fwd, r_aft=r_aft)
                self.assert_close(actual, expected, rel_tol=1e-12)

    def test_matches_ratio_form(self):
        length, r_fwd, r_aft = 0.15, 0.02, 0.05
        ratio = r_fwd / r_aft
        expected = (length / 3.0) * (1.0 + (1.0 - ratio) / (1.0 - ratio**2))
        actual = self.formula.evaluate(L=length, r_fwd=r_fwd, r_aft=r_aft)
        self.assert_close(actual, expected, rel_tol=1e-12)

    def test_cone_from_a_point_matches_power_series_nose(self):
        self.assert_close(
            self.formula.evaluate(L=0.4, r_fwd=0.0, r_aft=0.05),
            power_series_nose_center_of_pressure.evaluate(L=0.4, n=1.0),
            rel_tol=1e-13,
        )

    def test_cylinder_rejected(self):
        self.assert_rejected(L=0.1, r_fwd=0.05, r_aft=0.05)

    def test_nearly_cylindrical_transition_is_finite(self):
        value = self.formula.evaluate(L=0.1, r_fwd=0.05, r_aft=0.05 * (1 + 1e-9))
        self.assert_close(value, 0.05, rel_tol=1e-8)

    def test_tiny_lengths_do_not_underflow_to_zero(self):
        # 50-digit mpmath value at L = 1e-200, r_fwd = 3e-201, r_aft = 5e-201 is 5.41666...e-201;
        # the product (L/3)(2 r_aft + r_fwd) used to underflow to a silent 0.0.
        self.assert_close(
            self.formula.evaluate(L=1e-200, r_fwd=3e-201, r_aft=5e-201), 5.416666666666666e-201
        )

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(L=0.0, r_fwd=0.03, r_aft=0.05)
        self.assert_rejected(L=-0.1, r_fwd=0.03, r_aft=0.05)
        self.assert_rejected(L=0.1, r_fwd=-0.03, r_aft=0.05)
        self.assert_rejected(L=0.1, r_fwd=0.03, r_aft=-0.05)
        self.assert_rejected(L=0.1, r_fwd=0.0, r_aft=0.0)


class PowerSeriesNoseCenterOfPressureTest(_FormulaTest, unittest.TestCase):
    formula = power_series_nose_center_of_pressure
    formula_id = "aerodynamics.power_series_nose_center_of_pressure"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"L": 1.0, "n": 1.0}, 0.6666666666666666),
                ({"L": 0.4, "n": 0.75}, 0.24000000000000002),
                ({"L": 2.0, "n": 0.5}, 1.0),
                ({"L": 1.0, "n": 0.001}, 0.001996007984031936),
            ]
        )

    def test_matches_volume_quadrature(self):
        # Independent route: x_cp = L - V / A_B (eq. 3-89), with the volume integrated
        # numerically from A(x) = A_B (x / L)^(2n) instead of using V = A_B L / (2n + 1).
        for length, exponent in ((1.0, 1.0), (0.4, 0.75), (2.0, 0.5), (0.7, 1.3)):
            with self.subTest(length=length, exponent=exponent):
                volume = simpson(
                    lambda x, n=exponent, L=length: (x / L) ** (2.0 * n), 0.0, length, panels=4000
                )
                actual = self.formula.evaluate(L=length, n=exponent)
                # The integrand has a cusp at the tip for n < 1/2; here n >= 1/2.
                self.assert_close(actual, length - volume, rel_tol=1e-7)

    def test_matches_general_volume_form(self):
        length, exponent, base_area = 0.6, 0.75, 0.01
        volume = base_area * length / (2.0 * exponent + 1.0)
        self.assert_close(
            self.formula.evaluate(L=length, n=exponent),
            slender_body_center_of_pressure_from_volume.evaluate(
                L=length, V=volume, A_base=base_area
            ),
            rel_tol=1e-12,
        )

    def test_known_profiles(self):
        self.assert_close(self.formula.evaluate(L=3.0, n=1.0), 2.0)
        self.assert_close(self.formula.evaluate(L=3.0, n=0.5), 1.5)

    def test_stays_between_tip_and_base(self):
        for exponent in (0.01, 0.5, 1.0, 5.0, 100.0):
            value = self.formula.evaluate(L=1.0, n=exponent)
            self.assertTrue(0.0 < value < 1.0)

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(L=0.0, n=1.0)
        self.assert_rejected(L=-1.0, n=1.0)
        self.assert_rejected(L=1.0, n=0.0)
        self.assert_rejected(L=1.0, n=-0.5)


class SlenderBodyCenterOfPressureFromVolumeTest(_FormulaTest, unittest.TestCase):
    formula = slender_body_center_of_pressure_from_volume
    formula_id = "aerodynamics.slender_body_center_of_pressure_from_volume"

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"L": 1.0, "V": 0.2617993877991493, "A_base": 0.785398163397448}, 2.0 / 3.0),
                ({"L": 2.0, "V": 0.75, "A_base": 0.75}, 1.0),
                ({"L": 1.0, "V": 0.2, "A_base": 0.2}, 0.0),
            ],
            rel_tol=1e-12,
        )

    def test_cone_volume_gives_two_thirds_length(self):
        radius, length = 0.04, 0.5
        volume = math.pi * radius**2 * length / 3.0
        value = self.formula.evaluate(L=length, V=volume, A_base=math.pi * radius**2)
        self.assert_close(value, 2.0 * length / 3.0)

    def test_zero_volume_puts_center_of_pressure_at_base(self):
        self.assert_close(self.formula.evaluate(L=1.5, V=0.0, A_base=0.2), 1.5)

    def test_invalid_inputs_rejected(self):
        self.assert_rejected(L=0.0, V=0.1, A_base=0.2)
        self.assert_rejected(L=-1.0, V=0.1, A_base=0.2)
        self.assert_rejected(L=1.0, V=-0.1, A_base=0.2)
        self.assert_rejected(L=1.0, V=0.1, A_base=0.0)
        self.assert_rejected(L=1.0, V=0.1, A_base=-0.2)


if __name__ == "__main__":
    unittest.main()

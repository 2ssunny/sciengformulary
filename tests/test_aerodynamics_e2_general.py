"""Tests for the e2 atmosphere and general aerodynamics formulas.

Reference values are 50-digit mpmath evaluations of the cited equations at the inputs listed in
each test (mpmath.mp.dps = 50; the standard-atmosphere constants R* = 8.31432e3 N m/(kmol K),
M0 = 28.9644 kg/kmol and g0 = 9.80665 m/s^2; root finding with mpmath.findroot for the implicit
cases such as density altitude, stall speed, terminal-velocity drag area and parachute radius;
the mass-flux ratio for A/A*), rounded to a double. The independent-route tests use routes
written out in this file. No value comes from the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, MATH_ACCESSED
from sciengformulary.catalog.aerodynamics.barometric_pressure_gradient_layer import (
    barometric_pressure_gradient_layer,
)
from sciengformulary.catalog.aerodynamics.barometric_pressure_isothermal_layer import (
    barometric_pressure_isothermal_layer,
)
from sciengformulary.catalog.aerodynamics.climb_gradient import climb_gradient
from sciengformulary.catalog.aerodynamics.density_altitude import density_altitude
from sciengformulary.catalog.aerodynamics.energy_height import energy_height
from sciengformulary.catalog.aerodynamics.geopotential_height import geopotential_height
from sciengformulary.catalog.aerodynamics.induced_drag_force import induced_drag_force
from sciengformulary.catalog.aerodynamics.isentropic_area_mach_ratio import (
    isentropic_area_mach_ratio,
)
from sciengformulary.catalog.aerodynamics.isentropic_mass_flow_rate import (
    isentropic_mass_flow_rate,
)
from sciengformulary.catalog.aerodynamics.parachute_radius_from_drag_area import (
    parachute_radius_from_drag_area,
)
from sciengformulary.catalog.aerodynamics.sears_haack_wave_drag_area import (
    sears_haack_wave_drag_area,
)
from sciengformulary.catalog.aerodynamics.stall_speed import stall_speed
from sciengformulary.catalog.aerodynamics.terminal_velocity_drag_area import (
    terminal_velocity_drag_area,
)
from sciengformulary.core import FormulaSpec

REL = 1e-12

# 1976 Standard Atmosphere constants, written out here independently of the evaluators.
G0 = 9.80665
R_STAR = 8.31432e3
M0 = 28.9644
R_AIR = 287.0530720470647  # R*/M0 = 8.31432e3 / 28.9644 in J/(kg K), evaluated at 50 digits


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
        self.assertTrue(self.formula.references)
        self.assertTrue(self.formula.verification_cases)
        for ref in self.formula.references:
            if "mathlib" in ref.title:
                self.assertEqual(ref.accessed, MATH_ACCESSED)
            else:
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

    def test_derived_formulas_say_so(self):
        text = " ".join(self.formula.assumptions)
        if self.derived:
            self.assertIn("Derived result:", text)
        else:
            self.assertNotIn("Derived result:", text)


def _rk4(rate, x0, y0, x1, steps=2000):
    """Classical Runge-Kutta integration of dy/dx = rate(x, y) from x0 to x1."""
    h = (x1 - x0) / steps
    x, y = x0, y0
    for _ in range(steps):
        k1 = rate(x, y)
        k2 = rate(x + h / 2, y + h * k1 / 2)
        k3 = rate(x + h / 2, y + h * k2 / 2)
        k4 = rate(x + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
    return y


class BarometricPressureGradientLayerTest(_FormulaTest, unittest.TestCase):
    formula = barometric_pressure_gradient_layer
    formula_id = "aerodynamics.barometric_pressure_gradient_layer"
    derived = True
    base = {
        "p_b": 101325.0,
        "T_b": 288.15,
        "L": -0.0065,
        "h": 5000.0,
        "h_b": 0.0,
        "g0": G0,
        "R": R_AIR,
    }

    def test_oracle(self):
        self.assert_oracle(
            [
                (self.base, 54019.91210376207),
                ({**self.base, "h": 11000.0}, 22632.06397346293),
                (
                    {**self.base, "p_b": 5474.88866967778, "T_b": 216.65, "L": 0.001}
                    | {"h": 25000.0, "h_b": 20000.0},
                    2511.023353252595,
                ),
            ]
        )

    def test_matches_printed_form_with_universal_constants(self):
        # Independent route: the printed eq. (33a) with T_M, M0 and R* written out, base of the
        # bracket T_b / (T_b + L dh) and exponent g0 M0 / (R* L).
        T_b, p_b = 250.0, 90000.0
        for L, h_b, h in (
            (-0.0065, 0.0, 8000.0),
            (0.001, 20000.0, 30000.0),
            (0.0028, 32000.0, 40000.0),
            (-0.002, 47000.0, 70000.0),
        ):
            expected = p_b * (T_b / (T_b + L * (h - h_b))) ** (G0 * M0 / (R_STAR * L))
            with self.subTest(L=L, h=h):
                got = self.formula.evaluate(
                    p_b=p_b, T_b=T_b, L=L, h=h, h_b=h_b, g0=G0, R=R_STAR / M0
                )
                self.assert_close(got, expected, rel_tol=1e-11)

    def test_matches_numerical_hydrostatic_integration(self):
        # Independent route: integrate dp/dh = -p g0 / (R T(h)) with T = T_b + L (h - h_b).
        T_b, L, p_b = 288.15, -0.0065, 101325.0

        def rate(h, p):
            return -p * G0 / (R_AIR * (T_b + L * h))

        for h in (1000.0, 5000.0, 11000.0):
            with self.subTest(h=h):
                got = self.formula.evaluate(p_b=p_b, T_b=T_b, L=L, h=h, h_b=0.0, g0=G0, R=R_AIR)
                self.assert_close(got, _rk4(rate, 0.0, p_b, h), rel_tol=1e-10)

    def test_small_gradient_approaches_isothermal(self):
        iso = barometric_pressure_isothermal_layer.evaluate(
            p_b=22632.0, T_b=216.65, h=15000.0, h_b=11000.0, g0=G0, R=R_AIR
        )
        got = self.formula.evaluate(
            p_b=22632.0, T_b=216.65, L=1e-9, h=15000.0, h_b=11000.0, g0=G0, R=R_AIR
        )
        self.assert_close(got, iso, rel_tol=1e-6)

    def test_below_base_gives_higher_pressure(self):
        got = self.formula.evaluate(**{**self.base, "h": -1000.0})
        self.assertGreater(got, self.base["p_b"])

    def test_domain(self):
        self.assert_rejected(**{**self.base, "L": 0.0})
        self.assert_rejected(**{**self.base, "p_b": 0.0})
        self.assert_rejected(**{**self.base, "T_b": -1.0})
        self.assert_rejected(**{**self.base, "g0": 0.0})
        self.assert_rejected(**{**self.base, "R": -287.0})
        # Temperature reaches zero at dh = T_b / -L = 44330.8 m.
        self.assert_rejected(**{**self.base, "h": 44330.8})
        self.assert_rejected(**{**self.base, "h": 60000.0})


class BarometricPressureIsothermalLayerTest(_FormulaTest, unittest.TestCase):
    formula = barometric_pressure_isothermal_layer
    formula_id = "aerodynamics.barometric_pressure_isothermal_layer"
    derived = True
    base = {
        "p_b": 22632.06397346293,
        "T_b": 216.65,
        "h": 15000.0,
        "h_b": 11000.0,
        "g0": G0,
        "R": R_AIR,
    }

    def test_oracle(self):
        self.assert_oracle(
            [
                (self.base, 12044.570862423208),
                ({**self.base, "h": 20000.0}, 5474.88866967778),
            ]
        )

    def test_matches_printed_form_with_universal_constants(self):
        # Independent route: eq. (33b) with g0' M0 / (R* T_M,b) written out.
        expected = 22632.06397346293 * math.exp(-G0 * M0 * 4000.0 / (R_STAR * 216.65))
        got = self.formula.evaluate(**{**self.base, "R": R_STAR / M0})
        self.assert_close(got, expected, rel_tol=1e-11)

    def test_matches_numerical_hydrostatic_integration(self):
        def rate(h, p):
            return -p * G0 / (R_AIR * 216.65)

        got = self.formula.evaluate(**self.base)
        self.assert_close(got, _rk4(rate, 11000.0, 22632.06397346293, 15000.0), rel_tol=1e-10)

    def test_composes_across_two_steps(self):
        mid = self.formula.evaluate(**{**self.base, "h": 13000.0})
        top = self.formula.evaluate(**{**self.base, "p_b": mid, "h_b": 13000.0})
        self.assert_close(top, self.formula.evaluate(**self.base), rel_tol=1e-12)

    def test_domain(self):
        self.assert_rejected(**{**self.base, "p_b": -1.0})
        self.assert_rejected(**{**self.base, "T_b": 0.0})
        self.assert_rejected(**{**self.base, "g0": -9.8})
        self.assert_rejected(**{**self.base, "R": 0.0})

    def test_overflow_is_an_error(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(**{**self.base, "h": -1e9})

    def test_printed_table_row_is_truncated_not_rounded(self):
        # Table I prints 121.11 mb at 14965 m'; the computed value is 121.118 mb, which would
        # round to 121.12, so the table truncates on this row (the case note says so).
        got = self.formula.evaluate(**{**self.base, "h": 14964.687968767215})
        self.assertGreater(got, 12111.5)
        self.assertLess(got, 12112.5)
        self.assertGreater(got / 100.0, 121.115)


class GeopotentialHeightTest(_FormulaTest, unittest.TestCase):
    formula = geopotential_height
    formula_id = "aerodynamics.geopotential_height"
    derived = False

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"R_E": 6356766.0, "h": 11000.0}, 10980.99804546838),
                ({"R_E": 6356766.0, "h": 5000.0}, 4996.070273568692),
                ({"R_E": 6356766.0, "h": -5000.0}, -5003.93591325625),
                ({"R_E": 6371000.0, "h": 100000.0}, 98454.64379539483),
            ]
        )

    def test_table_rows_round_to_printed_values(self):
        # Table I of the cited report prints 4996 and -5004 for Z = 5000 and -5000 m.
        self.assertEqual(round(self.formula.evaluate(R_E=6356766.0, h=5000.0)), 4996)
        self.assertEqual(round(self.formula.evaluate(R_E=6356766.0, h=-5000.0)), -5004)

    def test_matches_integral_of_inverse_square_gravity(self):
        # Independent route: H = integral of (r0 / (r0 + z))^2 dz by the composite Simpson rule.
        r0, Z, n = 6356766.0, 80000.0, 2000
        step = Z / n
        total = 0.0
        for i in range(n + 1):
            weight = 1 if i in (0, n) else (4 if i % 2 else 2)
            total += weight * (r0 / (r0 + i * step)) ** 2
        simpson = total * step / 3
        self.assert_close(self.formula.evaluate(R_E=r0, h=Z), simpson, rel_tol=1e-12)

    def test_inverse_relation_recovers_geometric_height(self):
        # The source's inverse, Z = r0 H / (r0 - H), returns the input.
        r0 = 6356766.0
        for h in (-5000.0, 1234.5, 86000.0):
            H = self.formula.evaluate(R_E=r0, h=h)
            self.assert_close(r0 * H / (r0 - H), h, rel_tol=1e-10)

    def test_extreme_inputs_keep_finite_results(self):
        # 50-digit mpmath values of R h / (R + h); the product R * h or the sum R + h used to
        # overflow although the result is finite.
        cases = (
            ({"R_E": 6356766.0, "h": 1e305}, 6356766.0),
            ({"R_E": 1e308, "h": 1e308}, 5e307),
            ({"R_E": 1e200, "h": -0.5e200}, -1e200),
        )
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected)

    def test_domain(self):
        self.assert_rejected(R_E=0.0, h=1000.0)
        self.assert_rejected(R_E=-6356766.0, h=1000.0)
        self.assert_rejected(R_E=6356766.0, h=-6356766.0)
        self.assert_rejected(R_E=6356766.0, h=-7e6)


class DensityAltitudeTest(_FormulaTest, unittest.TestCase):
    formula = density_altitude
    formula_id = "aerodynamics.density_altitude"
    derived = True
    std = {"p0": 101325.0, "T0": 288.15, "Gamma": 0.0065, "g0": G0, "R": R_AIR}

    @staticmethod
    def _standard_density(h):
        # Forward ISA troposphere model from eqs. (23), (33a) and (42) of the source.
        T = 288.15 - 0.0065 * h
        p = 101325.0 * (T / 288.15) ** (G0 / (R_AIR * 0.0065))
        return p / (R_AIR * T)

    def _bisect(self, rho, low=-5000.0, high=11000.0):
        for _ in range(200):
            mid = 0.5 * (low + high)
            if self._standard_density(mid) > rho:
                low = mid
            else:
                high = mid
        return 0.5 * (low + high)

    def test_oracle(self):
        self.assert_oracle(
            [
                ({**self.std, "p": 101325.0, "T": 303.15}, 525.4557961194042),
                ({**self.std, "p": 54048.0, "T": 255.676}, 4996.13571767492),
                ({**self.std, "p": 70000.0, "T": 270.0}, 3063.677290652884),
            ],
            rel_tol=1e-11,
        )

    def test_standard_sea_level_gives_zero(self):
        self.assertAlmostEqual(self.formula.evaluate(p=101325.0, T=288.15, **self.std), 0.0, 8)

    def test_matches_bisection_of_forward_model(self):
        for p, T in ((101325.0, 303.15), (70000.0, 270.0), (90000.0, 260.0), (50000.0, 230.0)):
            rho = p / (R_AIR * T)
            with self.subTest(p=p, T=T):
                self.assertAlmostEqual(
                    self.formula.evaluate(p=p, T=T, **self.std), self._bisect(rho), 6
                )

    def test_round_trip_on_standard_states(self):
        for h in (-3000.0, 0.0, 2500.0, 8000.0, 10900.0):
            T = 288.15 - 0.0065 * h
            p = 101325.0 * (T / 288.15) ** (G0 / (R_AIR * 0.0065))
            with self.subTest(h=h):
                self.assertAlmostEqual(self.formula.evaluate(p=p, T=T, **self.std), h, 6)

    def test_hotter_air_has_higher_density_altitude(self):
        cool = self.formula.evaluate(p=95000.0, T=280.0, **self.std)
        hot = self.formula.evaluate(p=95000.0, T=300.0, **self.std)
        self.assertGreater(hot, cool)

    def test_domain(self):
        base = {"p": 90000.0, "T": 280.0, **self.std}
        for name in base:
            self.assert_rejected(**{**base, name: 0.0})
            self.assert_rejected(**{**base, name: -1.0})
        # g0 / (R Gamma) = 1 makes the exponent undefined.
        self.assert_rejected(**{**base, "Gamma": G0 / R_AIR})

    def test_outside_troposphere_branch_is_an_error(self):
        # Pressures and temperatures whose density altitude would lie far outside the
        # troposphere used to return implausible numbers (-2.08e6 m and 43.7 km).
        self.assert_rejected(p=1e12, T=200.0, **self.std)
        self.assert_rejected(p=1e-3, T=216.65, **self.std)
        # Standard states just beyond the branch limits (-5004 m' and 11 km') are rejected too.
        for h in (-5200.0, 11300.0):
            T = 288.15 - 0.0065 * h
            p = 101325.0 * (T / 288.15) ** (G0 / (R_AIR * 0.0065))
            self.assert_rejected(p=p, T=T, **self.std)

    def test_branch_limits_are_stated(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("raises ValueError", text)
        self.assertNotIn("not restricted", text)


class IsentropicAreaMachRatioTest(_FormulaTest, unittest.TestCase):
    formula = isentropic_area_mach_ratio
    formula_id = "aerodynamics.isentropic_area_mach_ratio"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"M": 2.0, "gamma": 1.4}, 1.6875),
                ({"M": 0.5, "gamma": 1.4}, 1.33984375),
                ({"M": 3.0, "gamma": 1.4}, 4.234567901234569),
                ({"M": 2.0, "gamma": 1.2}, 1.8837116867500996),
            ]
        )

    def test_is_reciprocal_of_printed_eq_80(self):
        # Independent route: eq. (80) as printed, A*/A, inverted.
        for M, g in ((0.3, 1.4), (1.7, 1.3), (4.0, 1.67), (10.0, 1.1)):
            printed = (
                ((g + 1) / 2) ** ((g + 1) / (2 * (g - 1)))
                * M
                * (1 + (g - 1) / 2 * M**2) ** (-(g + 1) / (2 * (g - 1)))
            )
            with self.subTest(M=M, gamma=g):
                self.assert_close(self.formula.evaluate(M=M, gamma=g), 1.0 / printed, rel_tol=1e-11)

    def test_equals_ratio_of_mass_fluxes(self):
        # Independent route: A / A* is the sonic mass flux over the local mass flux, with each
        # flux built from rho V = (p / R T) M sqrt(gamma R T) and the total-to-static ratios.
        g = 1.4

        def flux(M):
            # Mass flux rho V = p M sqrt(gamma / (R T)) in units where p0 = T0 = R = 1.
            t = 1 + (g - 1) / 2 * M**2  # T0 / T
            return t ** (-g / (g - 1)) * M * math.sqrt(g * t)

        for M in (0.4, 2.2, 3.5):
            with self.subTest(M=M):
                self.assert_close(
                    self.formula.evaluate(M=M, gamma=g), flux(1.0) / flux(M), rel_tol=1e-11
                )

    def test_minimum_at_sonic_and_two_branches(self):
        self.assertGreater(self.formula.evaluate(M=0.9, gamma=1.4), 1.0)
        self.assertGreater(self.formula.evaluate(M=1.1, gamma=1.4), 1.0)

    def test_domain(self):
        self.assert_rejected(M=0.0, gamma=1.4)
        self.assert_rejected(M=-1.0, gamma=1.4)
        self.assert_rejected(M=2.0, gamma=1.0)
        self.assert_rejected(M=2.0, gamma=0.9)


class IsentropicMassFlowRateTest(_FormulaTest, unittest.TestCase):
    formula = isentropic_mass_flow_rate
    formula_id = "aerodynamics.isentropic_mass_flow_rate"
    derived = True
    base = {"A": 0.01, "p0": 500000.0, "T0": 300.0, "gamma": 1.4, "R": R_AIR, "M": 1.0}

    def test_oracle(self):
        self.assert_oracle(
            [
                (self.base, 11.66671414836129),
                ({**self.base, "M": 0.5}, 8.70751843143),
                (
                    {**self.base, "A": 0.002, "p0": 101325.0, "T0": 288.15, "M": 2.0},
                    0.28591220493316727,
                ),
                ({**self.base, "M": 0.0}, 0.0),
            ],
            rel_tol=1e-11,
        )

    def test_matches_density_velocity_area_product(self):
        # Independent route: rho V A with rho = p / (R T), V = M sqrt(gamma R T), and the static
        # state from the total-to-static relations (43) and (44).
        for M in (0.2, 0.9, 1.0, 1.8, 3.0):
            g, R, p0, T0, A = 1.4, R_AIR, 700000.0, 450.0, 0.05
            T = T0 / (1 + (g - 1) / 2 * M**2)
            p = p0 * (1 + (g - 1) / 2 * M**2) ** (-g / (g - 1))
            expected = (p / (R * T)) * (M * math.sqrt(g * R * T)) * A
            with self.subTest(M=M):
                got = self.formula.evaluate(A=A, p0=p0, T0=T0, gamma=g, R=R, M=M)
                self.assert_close(got, expected, rel_tol=1e-11)

    def test_choked_flow_coefficient(self):
        # For air (gamma 1.4, R 287.05) the choked flow is about 0.0404 p0 A / sqrt(T0).
        got = self.formula.evaluate(**{**self.base, "T0": 400.0, "A": 1.0, "p0": 1.0})
        self.assertAlmostEqual(got * math.sqrt(400.0), 0.0404, 4)

    def test_choked_flow_is_the_maximum(self):
        flows = [self.formula.evaluate(**{**self.base, "M": m}) for m in (0.5, 0.9, 1.0, 1.1, 2.0)]
        self.assertEqual(max(flows), flows[2])

    def test_domain(self):
        for name in ("A", "p0", "T0", "R"):
            self.assert_rejected(**{**self.base, name: 0.0})
        self.assert_rejected(**{**self.base, "gamma": 1.0})
        self.assert_rejected(**{**self.base, "M": -0.1})


class ClimbGradientTest(_FormulaTest, unittest.TestCase):
    formula = climb_gradient
    formula_id = "aerodynamics.climb_gradient"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"T_W": 0.3, "L_D": 12.0}, 0.21666666666666667),
                ({"T_W": 0.1, "L_D": 10.0}, 0.0),
                ({"T_W": 0.0, "L_D": 15.0}, -0.06666666666666667),
            ]
        )

    @staticmethod
    def _exact_angle(T_W, L_D):
        # Independent route: solve sin(c) = T/W - cos(c) / (L/D) by bisection.
        def f(c):
            return math.sin(c) - T_W + math.cos(c) / L_D

        low, high = -math.pi / 2, math.pi / 2
        for _ in range(200):
            mid = 0.5 * (low + high)
            if f(mid) > 0:
                high = mid
            else:
                low = mid
        return 0.5 * (low + high)

    def test_small_angle_error_is_documented_size(self):
        # The exact angle for T/W 0.3 and L/D 12 is 0.220465 rad; the small-angle result
        # 0.216667 rad is about 0.0038 rad (1.7 percent) too SMALL, and the metadata says so.
        approx = self.formula.evaluate(T_W=0.3, L_D=12.0)
        exact = self._exact_angle(0.3, 12.0)
        self.assertLess(approx, exact)
        self.assertLess(abs(approx - exact), 5e-3)
        self.assertGreater(abs(approx - exact), 3e-3)
        self.assert_close((exact - approx) / exact, 0.0172, rel_tol=2e-2)
        text = " ".join(self.formula.assumptions)
        self.assertIn("too small", text)
        self.assertNotIn("too large", text)

    def test_converges_to_exact_angle_for_shallow_climbs(self):
        approx = self.formula.evaluate(T_W=0.1005, L_D=20.0)
        self.assert_close(approx, self._exact_angle(0.1005, 20.0), rel_tol=2e-2)
        approx = self.formula.evaluate(T_W=0.0505, L_D=20.0)
        self.assert_close(approx, self._exact_angle(0.0505, 20.0), rel_tol=5e-3)

    def test_domain(self):
        self.assert_rejected(T_W=-0.1, L_D=10.0)
        self.assert_rejected(T_W=0.1, L_D=0.0)
        self.assert_rejected(T_W=0.1, L_D=-10.0)


class InducedDragForceTest(_FormulaTest, unittest.TestCase):
    formula = induced_drag_force
    formula_id = "aerodynamics.induced_drag_force"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"L": 20000.0, "q": 5000.0, "b": 10.0, "e": 1.0}, 254.64790894703253),
                ({"L": 50000.0, "q": 2000.0, "b": 12.0, "e": 0.8}, 3453.8833136262006),
                ({"L": 0.0, "q": 2000.0, "b": 12.0, "e": 0.8}, 0.0),
            ]
        )

    def test_matches_coefficient_route_for_any_wing_area(self):
        # Independent route: C_di = C_l^2 / (pi AR e) with C_l = L / (q S), AR = b^2 / S and
        # D_i = C_di q S, for several arbitrary wing areas S.
        L, q, b, e = 30000.0, 3000.0, 14.0, 0.85
        for S in (5.0, 20.0, 77.0):
            C_l = L / (q * S)
            AR = b**2 / S
            expected = C_l**2 / (math.pi * AR * e) * q * S
            with self.subTest(S=S):
                self.assert_close(
                    self.formula.evaluate(L=L, q=q, b=b, e=e), expected, rel_tol=1e-12
                )

    def test_sign_of_lift_does_not_matter(self):
        pos = self.formula.evaluate(L=1000.0, q=500.0, b=8.0, e=0.9)
        neg = self.formula.evaluate(L=-1000.0, q=500.0, b=8.0, e=0.9)
        self.assertEqual(pos, neg)

    def test_boundary_efficiency_one_allowed(self):
        self.assertGreater(self.formula.evaluate(L=1.0, q=1.0, b=1.0, e=1.0), 0.0)

    def test_domain(self):
        base = {"L": 1000.0, "q": 500.0, "b": 8.0, "e": 0.9}
        self.assert_rejected(**{**base, "q": 0.0})
        self.assert_rejected(**{**base, "b": -1.0})
        self.assert_rejected(**{**base, "e": 0.0})
        self.assert_rejected(**{**base, "e": 1.0000001})


class StallSpeedTest(_FormulaTest, unittest.TestCase):
    formula = stall_speed
    formula_id = "aerodynamics.stall_speed"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"W": 10000.0, "rho": 1.225, "S": 16.2, "CL_max": 1.6}, 25.097441747368087),
                ({"W": 60000.0, "rho": 0.9093, "S": 30.0, "CL_max": 2.2}, 44.71621748063751),
                ({"W": 1.0, "rho": 1.0, "S": 1.0, "CL_max": 1.0}, 1.4142135623730951),
            ],
            rel_tol=1e-11,
        )

    def test_lift_at_stall_speed_equals_weight(self):
        # Independent route: the lift equation L = C_L (rho V^2 / 2) S at V_s and C_L,max.
        W, rho, S, CL = 25000.0, 1.1, 22.0, 1.9
        V = self.formula.evaluate(W=W, rho=rho, S=S, CL_max=CL)
        self.assert_close(CL * 0.5 * rho * V**2 * S, W, rel_tol=1e-12)

    def test_scaling(self):
        base = {"W": 8000.0, "rho": 1.0, "S": 10.0, "CL_max": 1.5}
        v = self.formula.evaluate(**base)
        self.assert_close(self.formula.evaluate(**{**base, "W": 4 * 8000.0}), 2 * v)
        self.assert_close(self.formula.evaluate(**{**base, "rho": 4.0}), v / 2)

    def test_convention_is_stated(self):
        text = " ".join(self.formula.assumptions)
        self.assertIn("1 g speed at maximum lift coefficient", text)
        self.assertIn("do not define stall speed", text)

    def test_domain(self):
        base = {"W": 8000.0, "rho": 1.0, "S": 10.0, "CL_max": 1.5}
        for name in base:
            self.assert_rejected(**{**base, name: 0.0})
            self.assert_rejected(**{**base, name: -1.0})


class TerminalVelocityDragAreaTest(_FormulaTest, unittest.TestCase):
    formula = terminal_velocity_drag_area
    formula_id = "aerodynamics.terminal_velocity_drag_area"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"m": 10.0, "g": G0, "rho": 1.225, "v_t": 5.0}, 6.404342857142856),
                ({"m": 1.0, "g": G0, "rho": 1.225, "v_t": 6.0}, 0.44474603174603167),
                ({"m": 80.0, "g": G0, "rho": 1.0, "v_t": 1.0}, 1569.0639999999999),
            ],
            rel_tol=1e-11,
        )

    def test_recovers_the_printed_terminal_velocity(self):
        # Independent route: the page's V = sqrt(2 W / (C_d rho A)) returns the input speed.
        m, g, rho, v = 85.0, G0, 1.1, 6.5
        CdS = self.formula.evaluate(m=m, g=g, rho=rho, v_t=v)
        self.assert_close(math.sqrt(2 * m * g / (CdS * rho)), v, rel_tol=1e-12)

    def test_drag_equals_weight(self):
        m, g, rho, v = 12.0, G0, 1.2, 8.0
        CdS = self.formula.evaluate(m=m, g=g, rho=rho, v_t=v)
        self.assert_close(CdS * 0.5 * rho * v**2, m * g, rel_tol=1e-12)

    def test_domain(self):
        base = {"m": 10.0, "g": G0, "rho": 1.225, "v_t": 5.0}
        for name in base:
            self.assert_rejected(**{**base, name: 0.0})
            self.assert_rejected(**{**base, name: -1.0})


class ParachuteRadiusFromDragAreaTest(_FormulaTest, unittest.TestCase):
    formula = parachute_radius_from_drag_area
    formula_id = "aerodynamics.parachute_radius_from_drag_area"
    derived = True

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"CdS": 1.0, "C_D": 1.5}, 0.46065886596178063),
                ({"CdS": 2.5, "C_D": 0.75}, 1.0300645387285055),
                ({"CdS": 0.04, "C_D": 1.0}, 0.11283791670955126),
            ],
            rel_tol=1e-11,
        )

    def test_projected_area_times_drag_coefficient_is_drag_area(self):
        for CdS, C_D in ((3.0, 1.2), (0.5, 0.8), (12.0, 1.75)):
            R = self.formula.evaluate(CdS=CdS, C_D=C_D)
            with self.subTest(CdS=CdS, C_D=C_D):
                self.assert_close(C_D * math.pi * R**2, CdS, rel_tol=1e-12)

    def test_zero_drag_area_gives_zero_radius(self):
        self.assertEqual(self.formula.evaluate(CdS=0.0, C_D=1.5), 0.0)

    def test_domain(self):
        self.assert_rejected(CdS=-0.1, C_D=1.5)
        self.assert_rejected(CdS=1.0, C_D=0.0)
        self.assert_rejected(CdS=1.0, C_D=-1.5)


class SearsHaackWaveDragAreaTest(_FormulaTest, unittest.TestCase):
    formula = sears_haack_wave_drag_area
    formula_id = "aerodynamics.sears_haack_wave_drag_area"
    derived = False

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"V": 0.0002, "L": 1.0}, 1.6297466172610084e-06),
                ({"V": 0.05, "L": 3.0}, 0.0012575205380100374),
                ({"V": 0.0, "L": 2.0}, 0.0),
            ]
        )

    def test_agrees_with_coefficient_on_maximum_cross_section(self):
        # Independent route: the printed eq. (16), C_Dw = 24 V / L^3 on A_max, with the maximum
        # cross-section A_max = 16 V / (3 pi L) of the Sears-Haack area distribution.
        V, L = 0.12, 2.5
        A_max = 16 * V / (3 * math.pi * L)
        D_over_q = 24 * V / L**3 * A_max
        self.assert_close(self.formula.evaluate(V=V, L=L), D_over_q, rel_tol=1e-12)

    def test_maximum_cross_section_matches_area_distribution_volume(self):
        # The volume of S(x) = A_max (4 x (L - x) / L^2)^(3/2) is 3 pi A_max L / 16 (midpoint rule).
        L, A_max, n = 2.0, 0.01, 200000
        volume = sum(
            A_max * (4 * (i + 0.5) / n * (1 - (i + 0.5) / n)) ** 1.5 * L / n for i in range(n)
        )
        self.assert_close(volume, 3 * math.pi * A_max * L / 16, rel_tol=1e-6)

    def test_scaling(self):
        base = self.formula.evaluate(V=0.1, L=2.0)
        self.assert_close(self.formula.evaluate(V=0.2, L=2.0), 4 * base)
        self.assert_close(self.formula.evaluate(V=0.1, L=4.0), base / 16)

    def test_domain(self):
        self.assert_rejected(V=-0.1, L=2.0)
        self.assert_rejected(V=0.1, L=0.0)
        self.assert_rejected(V=0.1, L=-2.0)


class EnergyHeightTest(_FormulaTest, unittest.TestCase):
    formula = energy_height
    formula_id = "aerodynamics.energy_height"
    derived = False

    def test_oracle(self):
        self.assert_oracle(
            [
                ({"h": 10000.0, "V": 250.0, "g": G0}, 13186.613165556026),
                ({"h": 0.0, "V": 100.0, "g": G0}, 509.8581064889641),
                ({"h": 3000.0, "V": 0.0, "g": G0}, 3000.0),
            ]
        )

    def test_constant_along_a_ballistic_climb(self):
        # Independent route: energy conservation, V^2 = V0^2 - 2 g (h - h0) at constant energy.
        h0, V0 = 2000.0, 300.0
        E0 = self.formula.evaluate(h=h0, V=V0, g=G0)
        for h in (3000.0, 4000.0, 4500.0):
            V = math.sqrt(V0**2 - 2 * G0 * (h - h0))
            with self.subTest(h=h):
                self.assert_close(self.formula.evaluate(h=h, V=V, g=G0), E0, rel_tol=1e-12)

    def test_negative_altitude_and_speed_sign(self):
        self.assertEqual(
            self.formula.evaluate(h=100.0, V=30.0, g=G0),
            self.formula.evaluate(h=100.0, V=-30.0, g=G0),
        )
        self.assertLess(self.formula.evaluate(h=-100.0, V=0.0, g=G0), 0.0)

    def test_domain(self):
        self.assert_rejected(h=100.0, V=30.0, g=0.0)
        self.assert_rejected(h=100.0, V=30.0, g=-9.8)


if __name__ == "__main__":
    unittest.main()

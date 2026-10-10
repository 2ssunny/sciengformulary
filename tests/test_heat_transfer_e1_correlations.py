"""Tests for the E1 heat-transfer correlations and radiation, resistance and shape-factor formulas.

Reference values come from the independent 50-digit oracle (mpmath) and from hand calculation.
The derived formulas (parallel-plate and concentric-cylinder radiation, and the rearranged
horizontal-cylinder form) and the zero-ratio effectiveness are also checked through
independent routes that do not reuse the evaluator's own expression.
"""

import math
import unittest

from sciengformulary.catalog.heat_transfer.churchill_bernstein_cylinder_nusselt import (
    churchill_bernstein_cylinder_nusselt,
)
from sciengformulary.catalog.heat_transfer.churchill_chu_horizontal_cylinder_nusselt import (
    churchill_chu_horizontal_cylinder_nusselt,
)
from sciengformulary.catalog.heat_transfer.churchill_chu_vertical_plate_nusselt import (
    churchill_chu_vertical_plate_nusselt,
)
from sciengformulary.catalog.heat_transfer.colburn_pipe_nusselt import colburn_pipe_nusselt
from sciengformulary.catalog.heat_transfer.concentric_cylinder_radiation_exchange import (
    concentric_cylinder_radiation_exchange,
)
from sciengformulary.catalog.heat_transfer.cylindrical_wall_thermal_resistance import (
    cylindrical_wall_thermal_resistance,
)
from sciengformulary.catalog.heat_transfer.gnielinski_nusselt import gnielinski_nusselt
from sciengformulary.catalog.heat_transfer.gnielinski_smooth_tube_nusselt import (
    gnielinski_smooth_tube_nusselt,
)
from sciengformulary.catalog.heat_transfer.laminar_flat_plate_uniform_flux_local_nusselt import (
    laminar_flat_plate_uniform_flux_local_nusselt,
)
from sciengformulary.catalog.heat_transfer.laminar_flat_plate_local_nusselt import (
    laminar_flat_plate_local_nusselt,
)
from sciengformulary.catalog.heat_transfer.parallel_plate_radiation_exchange import (
    parallel_plate_radiation_exchange,
)
from sciengformulary.catalog.heat_transfer.phase_change_exchanger_effectiveness import (
    phase_change_exchanger_effectiveness,
)
from sciengformulary.catalog.heat_transfer.shape_factor_buried_sphere import (
    shape_factor_buried_sphere,
)
from sciengformulary.catalog.heat_transfer.sieder_tate_turbulent_nusselt import (
    sieder_tate_turbulent_nusselt,
)

REL = 1e-12
NAN = math.nan
INF = math.inf
# W/(m^2 K^4), CODATA 2022: exact, derived from the SI's exact h, k and c (2 pi^5 k^4 /
# (15 h^3 c^2)), typed here for the independent routes.
SIGMA = 5.6703744191844294e-8


class FormulaTestCase(unittest.TestCase):
    """Shared helpers: ``formula`` and ``base`` are set by each subclass."""

    formula = None
    base: dict = {}

    def assert_close(self, actual, expected, rel_tol=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol),
            f"got {actual!r}, expected {expected!r}",
        )

    def check_oracle(self, cases, abs_tol=0.0):
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, abs_tol=abs_tol)

    def check_rejected(self, bad):
        for name, value in bad:
            with self.subTest(**{name: value}):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**{**self.base, name: value})

    def check_accepted(self, good):
        for name, value in good:
            with self.subTest(**{name: value}):
                result = self.formula.evaluate(**{**self.base, name: value})
                self.assertTrue(math.isfinite(result))


class PhaseChangeExchangerEffectivenessTest(FormulaTestCase):
    formula = phase_change_exchanger_effectiveness
    base = {"NTU": 1.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.phase_change_exchanger_effectiveness")

    def test_oracle_values(self):
        self.check_oracle(
            [
                ({"NTU": 1.0}, 0.6321205588285577),
                ({"NTU": 5.0}, 0.9932620530009145),
                ({"NTU": 0.0}, 0.0),
            ],
            abs_tol=1e-15,
        )

    def test_domain_rules(self):
        self.check_rejected(
            [("NTU", -1e-9), ("NTU", -1.0), ("NTU", NAN), ("NTU", INF), ("NTU", True)]
        )

    def test_boundary_zero_is_accepted(self):
        self.assertEqual(self.formula.evaluate(NTU=0.0), 0.0)
        self.assertEqual(self.formula.evaluate(NTU=0), 0.0)

    def test_small_and_large_ntu(self):
        # 1 - exp(-x) = x - x^2/2 + ... for tiny x; the large-NTU limit is 1.
        self.assert_close(self.formula.evaluate(NTU=1e-12), 1e-12 * (1 - 0.5e-12))
        self.assertEqual(self.formula.evaluate(NTU=1e6), 1.0)

    def test_independent_route_from_general_relations_at_zero_ratio(self):
        # The parallel-flow and counterflow relations with C_r = 0 give the same expression.
        def parallel(ntu, c_r):
            return (1.0 - math.exp(-ntu * (1.0 + c_r))) / (1.0 + c_r)

        def counter(ntu, c_r):
            e = math.exp(-ntu * (1.0 - c_r))
            return (1.0 - e) / (1.0 - c_r * e)

        for ntu in (0.1, 0.5, 1.0, 2.5, 5.0):
            with self.subTest(NTU=ntu):
                value = self.formula.evaluate(NTU=ntu)
                self.assert_close(value, parallel(ntu, 0.0))
                self.assert_close(value, counter(ntu, 0.0))


class CylindricalWallThermalResistanceTest(FormulaTestCase):
    formula = cylindrical_wall_thermal_resistance
    base = {"r_o": 0.5, "r_i": 0.45, "k": 20.0, "L": 10.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.cylindrical_wall_thermal_resistance")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 8.384323436827047e-05),
                ({"r_o": 1.001, "r_i": 1.0, "k": 1.0, "L": 1.0}, 0.00015907541863224015),
                ({"r_o": 0.0058, "r_i": 0.0025, "k": 0.074, "L": 1.0}, 1.8099942911435594),
            ]
        )

    def test_thin_wall_keeps_full_precision(self):
        # Constants are 50-digit mpmath values of ln(r_o / r_i) / (2 pi k L) for the float
        # inputs (fix_oracles/thin_close_oracle.py); ln(r_o / r_i) alone loses about 7 digits
        # at a relative wall thickness of 1e-9.
        self.check_oracle(
            [
                ({"r_o": 1.0 + 1e-9, "r_i": 1.0, "k": 1.0, "L": 1.0}, 1.591549561808569e-10),
                ({"r_o": 0.0100001, "r_i": 0.01, "k": 40.0, "L": 3.0}, 1.3262845610128319e-08),
                ({"r_o": 5.0 + 5e-7, "r_i": 5.0, "k": 2.0, "L": 1.0}, 7.957746750751855e-09),
            ]
        )

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("r_i", 0.0),
                ("r_i", -0.1),
                ("r_o", 0.45),
                ("r_o", 0.4),
                ("r_o", NAN),
                ("k", 0.0),
                ("k", -1.0),
                ("L", 0.0),
                ("L", INF),
            ]
        )

    def test_boundary_just_above_inner_radius(self):
        self.check_accepted([("r_o", 0.45 * (1.0 + 1e-9))])

    def test_series_layers_add(self):
        whole = self.formula.evaluate(r_o=0.9, r_i=0.3, k=2.0, L=3.0)
        inner = self.formula.evaluate(r_o=0.5, r_i=0.3, k=2.0, L=3.0)
        outer = self.formula.evaluate(r_o=0.9, r_i=0.5, k=2.0, L=3.0)
        self.assert_close(whole, inner + outer)

    def test_shape_factor_route(self):
        # Table 5.4 item 2: S = 2 pi L / ln(r_o / r_i) and R_t = 1 / (k S).
        r_o, r_i, k, length = 0.07, 0.05, 45.0, 2.0
        shape = 2.0 * math.pi * length / math.log(r_o / r_i)
        self.assert_close(self.formula.evaluate(r_o=r_o, r_i=r_i, k=k, L=length), 1.0 / (k * shape))

    def test_thin_wall_approaches_plane_wall(self):
        r_i, thickness, k, length = 1.0, 1e-6, 3.0, 2.0
        mean_area = 2.0 * math.pi * (r_i + thickness / 2.0) * length
        plane = thickness / (k * mean_area)
        self.assert_close(
            self.formula.evaluate(r_o=r_i + thickness, r_i=r_i, k=k, L=length), plane, rel_tol=1e-6
        )


class ShapeFactorBuriedSphereTest(FormulaTestCase):
    formula = shape_factor_buried_sphere
    base = {"R": 0.5, "h": 100.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.shape_factor_buried_sphere")

    def test_oracle_values(self):
        self.check_oracle(
            [(self.base, 6.298932638776527), ({"R": 0.79, "h": 1.0}, 16.408979810485533)]
        )

    def test_first_order_approximation_against_exact_series(self):
        # Exact sphere-plane shape factor 4 pi R sinh(a) sum 1/sinh(n a), cosh(a) = h / R, from
        # 40-digit mpmath (fix_oracles/sphere_oracle.py), for h = 1. The tabulated expression
        # is low, by about 0.06 % at R = 0.3, 0.6 % at 0.5, 3 % at 0.7 and 6 % at 0.79.
        exact = {0.3: 4.4379128864993561, 0.5: 8.4261273135833954}
        exact |= {0.7: 13.947308984865633, 0.79: 17.424534937354727}
        for radius, bound in ((0.3, 0.0007), (0.5, 0.0065), (0.7, 0.031), (0.79, 0.060)):
            with self.subTest(R=radius):
                ratio = self.formula.evaluate(R=radius, h=1.0) / exact[radius] - 1.0
                self.assertLess(ratio, 0.0)
                self.assertGreater(ratio, -bound)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("R", 0.0),
                ("R", -1.0),
                ("R", NAN),
                ("h", 0.0),
                ("h", -100.0),
                ("h", INF),
            ]
        )

    def test_radius_ratio_limit(self):
        # The stated range is R / h < 0.8, so 0.8 itself and anything above is rejected.
        for ratio in (0.8, 0.8001, 1.0, 2.0):
            with self.subTest(ratio=ratio):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(R=ratio, h=1.0)
        self.assertTrue(math.isfinite(self.formula.evaluate(R=0.7999, h=1.0)))

    def test_deep_burial_limit(self):
        self.assert_close(self.formula.evaluate(R=2.0, h=1e9), 4.0 * math.pi * 2.0, rel_tol=1e-8)

    def test_diameter_form_route(self):
        # The same factor written with D = 2 R and Z = h: 2 pi D / (1 - D / (4 Z)).
        diameter, depth = 0.6, 2.0
        expected = 2.0 * math.pi * diameter / (1.0 - diameter / (4.0 * depth))
        self.assert_close(self.formula.evaluate(R=diameter / 2.0, h=depth), expected)


class ParallelPlateRadiationExchangeTest(FormulaTestCase):
    formula = parallel_plate_radiation_exchange
    base = {"A": 1.0, "T1": 500.0, "T2": 300.0, "eps1": 0.8, "eps2": 0.6}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.parallel_plate_radiation_exchange")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 1609.4001829754764),
                (
                    {"A": 2.0, "T1": 400.0, "T2": 300.0, "eps1": 1.0, "eps2": 1.0},
                    1984.6310467145504,
                ),
                ({"A": 1.0, "T1": 350.0, "T2": 350.0, "eps1": 0.5, "eps2": 0.5}, 0.0),
            ],
            abs_tol=1e-15,
        )

    def test_close_temperatures_keep_full_precision(self):
        # 50-digit mpmath values of sigma A (T1^4 - T2^4) / (1/eps1 + 1/eps2 - 1) for the float
        # inputs (fix_oracles/thin_close_oracle.py); T1^4 - T2^4 as a difference of fourth
        # powers loses about 8 digits at T1 - T2 = 1e-9 K.
        self.check_oracle(
            [
                (
                    {"A": 1.0, "T1": 300.01, "T2": 300.0, "eps1": 0.8, "eps2": 0.5},
                    0.027219158132163357,
                ),
                (
                    {"A": 2.0, "T1": 400.0 + 1e-6, "T2": 400.0, "eps1": 0.9, "eps2": 0.9},
                    2.37537139596512e-05,
                ),
                (
                    {"A": 1.5, "T1": 300.0, "T2": 300.0 - 1e-9, "eps1": 0.7, "eps2": 0.4},
                    3.136651994796624e-09,
                ),
            ]
        )

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("A", 0.0),
                ("A", -1.0),
                ("T1", 0.0),
                ("T1", -300.0),
                ("T2", 0.0),
                ("T2", NAN),
                ("eps1", 0.0),
                ("eps1", -0.1),
                ("eps1", 1.0000001),
                ("eps2", 0.0),
                ("eps2", 1.5),
                ("eps2", INF),
            ]
        )

    def test_emissivity_upper_bound_is_accepted(self):
        self.check_accepted([("eps1", 1.0), ("eps2", 1.0)])

    def test_antisymmetric_under_swapping_plates(self):
        forward = self.formula.evaluate(**self.base)
        swapped = {"A": 1.0, "T1": 300.0, "T2": 500.0, "eps1": 0.6, "eps2": 0.8}
        self.assert_close(self.formula.evaluate(**swapped), -forward)

    def test_derived_route_surface_resistance_circuit(self):
        # Derived result: net rate from the two-surface circuit of the source with F12 = 1,
        # Q = (Eb1 - Eb2) / [(1 - e1)/(e1 A) + 1/A + (1 - e2)/(e2 A)], Eb = sigma T^4.
        for area, t1, t2, e1, e2 in [
            (1.0, 500.0, 300.0, 0.8, 0.6),
            (3.5, 900.0, 400.0, 0.25, 0.9),
            (0.2, 320.0, 700.0, 0.05, 0.05),
        ]:
            with self.subTest(A=area, T1=t1, T2=t2):
                resistance = (1.0 - e1) / (e1 * area) + 1.0 / area + (1.0 - e2) / (e2 * area)
                expected = SIGMA * (t1**4 - t2**4) / resistance
                value = self.formula.evaluate(A=area, T1=t1, T2=t2, eps1=e1, eps2=e2)
                self.assert_close(value, expected)


class ConcentricCylinderRadiationExchangeTest(FormulaTestCase):
    formula = concentric_cylinder_radiation_exchange
    base = {"r1": 0.05, "r2": 0.1, "L": 1.0, "T1": 600.0, "T2": 300.0, "eps1": 0.5, "eps2": 0.5}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.concentric_cylinder_radiation_exchange")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 865.7607216548861),
                (
                    {
                        "r1": 0.05,
                        "r2": 0.1,
                        "L": 2.0,
                        "T1": 800.0,
                        "T2": 300.0,
                        "eps1": 0.3,
                        "eps2": 1.0,
                    },
                    4291.394194375762,
                ),
            ]
        )

    def test_close_temperatures_keep_full_precision(self):
        # 50-digit mpmath values for the float inputs (fix_oracles/thin_close_oracle.py).
        self.check_oracle(
            [
                (
                    {
                        "r1": 0.1,
                        "r2": 0.2,
                        "L": 2.0,
                        "T1": 300.01,
                        "T2": 300.0,
                        "eps1": 0.8,
                        "eps2": 0.5,
                    },
                    0.043977346572807406,
                ),
                (
                    {
                        "r1": 0.05,
                        "r2": 0.1,
                        "L": 1.0,
                        "T1": 500.0,
                        "T2": 500.0 - 1e-6,
                        "eps1": 0.9,
                        "eps2": 0.6,
                    },
                    6.166386872306042e-06,
                ),
            ]
        )

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("r1", 0.0),
                ("r1", -0.05),
                ("r2", 0.05),
                ("r2", 0.04),
                ("r2", NAN),
                ("L", 0.0),
                ("L", -1.0),
                ("T1", 0.0),
                ("T2", -1.0),
                ("eps1", 0.0),
                ("eps1", 1.1),
                ("eps2", 0.0),
                ("eps2", 1.1),
                ("eps2", NAN),
            ]
        )

    def test_boundary_outer_radius_just_above_inner(self):
        self.check_accepted([("r2", 0.05 * (1.0 + 1e-9)), ("eps1", 1.0), ("eps2", 1.0)])

    def test_derived_route_enclosure_resistance_circuit(self):
        # Derived result: the enclosure circuit with F12 = 1 and the areas of the two
        # cylinders written out, Q = (Eb1 - Eb2) / [(1-e1)/(e1 A1) + 1/A1 + (1-e2)/(e2 A2)].
        for r1, r2, length, t1, t2, e1, e2 in [
            (0.05, 0.1, 1.0, 600.0, 300.0, 0.5, 0.5),
            (0.02, 0.15, 4.0, 450.0, 320.0, 0.9, 0.2),
            (0.3, 0.31, 0.5, 280.0, 350.0, 0.1, 0.7),
        ]:
            with self.subTest(r1=r1, r2=r2):
                a1 = 2.0 * math.pi * r1 * length
                a2 = 2.0 * math.pi * r2 * length
                resistance = (1.0 - e1) / (e1 * a1) + 1.0 / a1 + (1.0 - e2) / (e2 * a2)
                expected = SIGMA * (t1**4 - t2**4) / resistance
                value = self.formula.evaluate(
                    r1=r1, r2=r2, L=length, T1=t1, T2=t2, eps1=e1, eps2=e2
                )
                self.assert_close(value, expected)

    def test_large_enclosure_limit(self):
        # r1 / r2 -> 0 gives exchange with large surroundings, eps1 A1 sigma (T1^4 - T2^4).
        value = self.formula.evaluate(**{**self.base, "r2": 5e7, "eps2": 0.3})
        area = 2.0 * math.pi * 0.05 * 1.0
        self.assert_close(value, 0.5 * SIGMA * area * (600.0**4 - 300.0**4), rel_tol=1e-6)

    def test_close_spacing_limit_matches_parallel_plates(self):
        # r2 -> r1 gives the parallel-plate expression with plate area A1.
        value = self.formula.evaluate(**{**self.base, "r2": 0.05 * (1.0 + 1e-9)})
        area = 2.0 * math.pi * 0.05 * 1.0
        plates = SIGMA * area * (600.0**4 - 300.0**4) / (1 / 0.5 + 1 / 0.5 - 1)
        self.assert_close(value, plates, rel_tol=1e-6)


class ColburnPipeNusseltTest(FormulaTestCase):
    formula = colburn_pipe_nusselt
    base = {"Re_D": 100000.0, "Pr": 1.2}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.colburn_pipe_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [(self.base, 244.41147091200054), ({"Re_D": 10000.0, "Pr": 0.67}, 31.89721533251494)]
        )

    def test_hand_value(self):
        # Pr = 1 and Re_D = 1e5: Re^0.8 = 1e4, so Nu = 0.023 * 1e4 = 230.
        self.assert_close(self.formula.evaluate(Re_D=1e5, Pr=1.0), 230.0)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_D", 9999.999),
                ("Re_D", 0.0),
                ("Re_D", -1e5),
                ("Re_D", NAN),
                ("Re_D", INF),
                ("Pr", 0.6699),
                ("Pr", 0.0),
                ("Pr", -1.0),
                ("Pr", 100.001),
                ("Pr", NAN),
            ]
        )

    def test_range_boundaries_are_accepted(self):
        self.check_accepted([("Re_D", 1e4), ("Pr", 0.67), ("Pr", 100.0)])


class GnielinskiNusseltTest(FormulaTestCase):
    formula = gnielinski_nusselt
    base = {"Re_D": 100000.0, "Pr": 1.2, "f": 0.0185}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.gnielinski_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                ({"Re_D": 412000.0, "Pr": 3.61, "f": 0.0136}, 1476.2264696347459),
                (self.base, 254.62682749359632),
                ({"Re_D": 2300.0, "Pr": 0.6, "f": 0.05}, 6.864094528152871),
            ]
        )

    def test_hand_value_at_unit_prandtl(self):
        # Pr = 1 removes the denominator correction: Nu = (f/8)(Re - 1000) = 0.005 * 1300.
        self.assert_close(self.formula.evaluate(Re_D=2300.0, Pr=1.0, f=0.04), 6.5)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_D", 2299.999),
                ("Re_D", 5.0000001e6),
                ("Re_D", 1000.0),
                ("Re_D", NAN),
                ("Pr", 0.5999),
                ("Pr", 100001.0),
                ("Pr", 0.0),
                ("Pr", NAN),
                ("f", 0.0),
                ("f", -0.02),
                ("f", NAN),
                ("f", INF),
            ]
        )

    def test_range_boundaries_are_accepted(self):
        self.check_accepted([("Re_D", 2300.0), ("Re_D", 5e6), ("Pr", 0.6), ("Pr", 1e5)])

    def test_non_positive_denominator_is_rejected(self):
        # At Pr = 0.6 the denominator is 1 + 12.7 * sqrt(f/8) * (0.6^(2/3) - 1), and the last
        # factor is -0.28862. By hand it is 0.0836 at f = 0.5 (1 - 12.7 * 0.25 * 0.28862), so Nu
        # stays positive there, while it is negative at f = 0.7, 1.0 and 4.0, where the
        # formula would give a negative Nu.
        low_pr = {"Re_D": 100000.0, "Pr": 0.6}
        self.assertGreater(self.formula.evaluate(**low_pr, f=0.5), 0.0)
        for f in (0.7, 1.0, 4.0):
            with self.subTest(f=f):
                with self.assertRaises(ValueError):
                    self.formula.evaluate(**low_pr, f=f)
        # Pr >= 1 can never make the denominator non-positive.
        self.assertGreater(self.formula.evaluate(Re_D=1e5, Pr=1.0, f=4.0), 0.0)


class GnielinskiSmoothTubeNusseltTest(FormulaTestCase):
    formula = gnielinski_smooth_tube_nusselt
    base = {"Re_D": 100000.0, "Pr": 1.2}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.gnielinski_smooth_tube_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 227.8880049437343),
                ({"Re_D": 2300.0, "Pr": 0.6}, 6.787598638783551),
                ({"Re_D": 5000000.0, "Pr": 1.5}, 5752.230790481048),
            ]
        )

    def test_hand_value(self):
        # Pr = 1, Re_D = 1e5: Re^0.8 = 1e4, so Nu = 0.0214 * (1e4 - 100) = 211.86.
        self.assert_close(self.formula.evaluate(Re_D=1e5, Pr=1.0), 211.86)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_D", 2299.9),
                ("Re_D", 5.01e6),
                ("Re_D", 0.0),
                ("Re_D", NAN),
                ("Pr", 0.5999),
                ("Pr", 1.5001),
                ("Pr", 0.0),
                ("Pr", INF),
            ]
        )

    def test_range_boundaries_are_accepted(self):
        self.check_accepted([("Re_D", 2300.0), ("Re_D", 5e6), ("Pr", 0.6), ("Pr", 1.5)])


class SiederTateTurbulentNusseltTest(FormulaTestCase):
    formula = sieder_tate_turbulent_nusselt
    base = {"Re_D": 100000.0, "Pr": 5.0, "mu_b": 0.000554, "mu_w": 0.000316}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.sieder_tate_turbulent_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 425.45439365112526),
                ({"Re_D": 10000.0, "Pr": 0.67, "mu_b": 0.001, "mu_w": 0.001}, 31.89721533251494),
            ]
        )

    def test_uses_textbook_coefficient(self):
        # Equal viscosities, Pr = 1, Re_D = 1e5: Nu = 0.023 * 1e4 = 230 (not 0.027 * 1e4).
        value = self.formula.evaluate(Re_D=1e5, Pr=1.0, mu_b=1.0, mu_w=1.0)
        self.assert_close(value, 230.0)

    def test_viscosity_ratio_exponent(self):
        # A viscosity ratio of 2^(1/0.14) doubles the result.
        ratio = 2.0 ** (1.0 / 0.14)
        value = self.formula.evaluate(Re_D=1e5, Pr=1.0, mu_b=ratio, mu_w=1.0)
        self.assert_close(value, 460.0)

    def test_reduces_to_colburn_for_equal_viscosities(self):
        for re_d, pr in [(1e4, 0.67), (3e4, 2.0), (5e5, 100.0)]:
            with self.subTest(Re_D=re_d, Pr=pr):
                colburn = colburn_pipe_nusselt.evaluate(Re_D=re_d, Pr=pr)
                value = self.formula.evaluate(Re_D=re_d, Pr=pr, mu_b=0.003, mu_w=0.003)
                self.assert_close(value, colburn)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_D", 9999.9),
                ("Re_D", NAN),
                ("Pr", 0.6699),
                ("Pr", 100.5),
                ("Pr", 0.0),
                ("mu_b", 0.0),
                ("mu_b", -1e-3),
                ("mu_b", INF),
                ("mu_w", 0.0),
                ("mu_w", -1e-3),
                ("mu_w", NAN),
            ]
        )

    def test_range_boundaries_are_accepted(self):
        self.check_accepted([("Re_D", 1e4), ("Pr", 0.67), ("Pr", 100.0)])


class ChurchillBernsteinCylinderNusseltTest(FormulaTestCase):
    formula = churchill_bernstein_cylinder_nusselt
    base = {"Re_D": 6071.0, "Pr": 0.7}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.churchill_bernstein_cylinder_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 40.637085941249744),
                ({"Re_D": 100000.0, "Pr": 7.0}, 507.5910225632826),
                ({"Re_D": 0.28571428571428575, "Pr": 0.7}, 0.5581686439080673),
            ]
        )

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_D", 0.0),
                ("Re_D", -100.0),
                ("Re_D", NAN),
                ("Pr", 0.0),
                ("Pr", -0.7),
                ("Pr", INF),
            ]
        )

    def test_peclet_lower_limit(self):
        # Re_D * Pr = 0.2 is accepted (oracle case); just below it is rejected.
        with self.assertRaises(ValueError):
            self.formula.evaluate(Re_D=0.28, Pr=0.7)
        with self.assertRaises(ValueError):
            self.formula.evaluate(Re_D=1e-3, Pr=100.0)
        self.assertTrue(math.isfinite(self.formula.evaluate(Re_D=0.2, Pr=1.0)))

    def test_increases_with_reynolds_number(self):
        values = [self.formula.evaluate(Re_D=re, Pr=0.7) for re in (1.0, 10.0, 1e3, 1e5, 1e6)]
        self.assertEqual(values, sorted(values))

    def test_conduction_floor(self):
        # The constant 0.3 is the lower bound of the correlation.
        self.assertGreater(self.formula.evaluate(Re_D=0.2, Pr=1.0), 0.3)


class LaminarFlatPlateUniformFluxLocalNusseltTest(FormulaTestCase):
    formula = laminar_flat_plate_uniform_flux_local_nusselt
    base = {"Re_x": 100000.0, "Pr": 0.7}

    def test_constructed(self):
        self.assertEqual(
            self.formula.id, "heat_transfer.laminar_flat_plate_uniform_flux_local_nusselt"
        )

    def test_oracle_values(self):
        self.check_oracle(
            [(self.base, 128.79373962931666), ({"Re_x": 200000.0, "Pr": 7.0}, 392.41272732629943)]
        )

    def test_hand_value(self):
        # Re_x = 1e4 and Pr = 1: Nu = 0.4587 * 100 = 45.87.
        self.assert_close(self.formula.evaluate(Re_x=1e4, Pr=1.0), 45.87)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Re_x", 0.0),
                ("Re_x", -1.0),
                ("Re_x", NAN),
                ("Pr", 0.6999),
                ("Pr", 0.0),
                ("Pr", -1.0),
                ("Pr", NAN),
                ("Pr", True),
            ]
        )

    def test_lower_prandtl_boundary_is_accepted(self):
        self.check_accepted([("Pr", 0.7)])

    def test_ratio_to_isothermal_plate_coefficient(self):
        for re_x, pr in [(1e3, 0.7), (1e5, 7.0), (3e5, 100.0)]:
            with self.subTest(Re_x=re_x, Pr=pr):
                flux = self.formula.evaluate(Re_x=re_x, Pr=pr)
                wall = laminar_flat_plate_local_nusselt.evaluate(Re_x=re_x, Pr=pr)
                self.assert_close(flux / wall, 0.4587 / 0.332)


class ChurchillChuVerticalPlateNusseltTest(FormulaTestCase):
    formula = churchill_chu_vertical_plate_nusselt
    base = {"Ra_L": 1814700000.0, "Pr": 0.69}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.churchill_chu_vertical_plate_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                (self.base, 147.16185223770617),
                ({"Ra_L": 1e12, "Pr": 7.0}, 1389.0728802931085),
                ({"Ra_L": 1.0, "Pr": 0.71}, 1.3211667381810492),
            ]
        )

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Ra_L", 0.0),
                ("Ra_L", -1.0),
                ("Ra_L", NAN),
                ("Ra_L", INF),
                ("Pr", 0.0),
                ("Pr", -0.7),
                ("Pr", NAN),
            ]
        )

    def test_small_positive_rayleigh_is_accepted(self):
        # The source states no lower limit, so tiny positive values are evaluated.
        value = churchill_chu_vertical_plate_nusselt.evaluate(Ra_L=1e-12, Pr=0.7)
        self.assertGreater(value, 0.825**2)

    def test_increases_with_rayleigh_number(self):
        values = [self.formula.evaluate(Ra_L=ra, Pr=0.7) for ra in (1.0, 1e3, 1e6, 1e9, 1e12)]
        self.assertEqual(values, sorted(values))

    def test_large_prandtl_limit(self):
        # For Pr -> infinity the Prandtl factor tends to 1: Nu = (0.825 + 0.387 Ra^(1/6))^2.
        value = self.formula.evaluate(Ra_L=1e9, Pr=1e12)
        expected = (0.825 + 0.387 * 1e9 ** (1.0 / 6.0)) ** 2
        self.assert_close(value, expected, rel_tol=1e-6)


class ChurchillChuHorizontalCylinderNusseltTest(FormulaTestCase):
    formula = churchill_chu_horizontal_cylinder_nusselt
    base = {"Ra_D": 5.762, "Pr": 0.707}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "heat_transfer.churchill_chu_horizontal_cylinder_nusselt")

    def test_oracle_values(self):
        self.check_oracle(
            [
                ({"Ra_D": 0.0005762, "Pr": 0.707}, 0.4797602017289283),
                (self.base, 1.0609626321876542),
                ({"Ra_D": 1e-06, "Pr": 0.7}, 0.39954060545245246),
                ({"Ra_D": 1814700000.0, "Pr": 0.69}, 139.13493970073606),
            ]
        )

    def test_textbook_printed_example_values(self):
        # Example 8.4 prints 0.480 and 1.061 (three decimals).
        low = self.formula.evaluate(Ra_D=0.0005762, Pr=0.707)
        self.assertEqual(round(low, 3), 0.480)
        self.assertEqual(round(self.formula.evaluate(**self.base), 3), 1.061)

    def test_domain_rules(self):
        self.check_rejected(
            [
                ("Ra_D", 9.99e-7),
                ("Ra_D", 0.0),
                ("Ra_D", -1.0),
                ("Ra_D", NAN),
                ("Ra_D", INF),
                ("Pr", 0.0),
                ("Pr", -0.7),
                ("Pr", NAN),
            ]
        )

    def test_lower_rayleigh_boundary_is_accepted(self):
        self.check_accepted([("Ra_D", 1e-6)])

    def test_derived_route_source_bracket_form(self):
        # Derived result: the source prints {0.60 + 0.387 [Ra / psi^(16/9)]^(1/6)}^2 with
        # psi = 1 + (0.559/Pr)^(9/16); the evaluator uses Ra^(1/6) / psi^(8/27).
        for ra, pr in [(1e-6, 0.7), (5.762, 0.707), (1e4, 7.0), (1.8147e9, 0.69), (1e12, 0.02)]:
            with self.subTest(Ra_D=ra, Pr=pr):
                psi = 1.0 + (0.559 / pr) ** (9.0 / 16.0)
                expected = (0.60 + 0.387 * (ra / psi ** (16.0 / 9.0)) ** (1.0 / 6.0)) ** 2
                self.assert_close(self.formula.evaluate(Ra_D=ra, Pr=pr), expected)


if __name__ == "__main__":
    unittest.main()

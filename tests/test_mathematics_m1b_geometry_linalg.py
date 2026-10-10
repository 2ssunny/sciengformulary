"""Tests for the m1b geometry and linear-algebra formulas in the mathematics domain.

Extra numeric expectations come from the independent oracle used to verify these formulas
(exact fractions, 50-digit mpmath, sympy) or from hand calculations stated next to them; none
is produced by the evaluators under test. Derived formulas are also checked against the
source's original form evaluated separately: a Leibniz determinant in exact fractions for
Cramer's rule and the characteristic polynomial, the projection procedure and a numerical
minimisation for the point-to-line distance, and enumeration of integer triples or an explicit
coordinate construction for the right-triangle results.
"""

import itertools
import math
import random
import unittest
from fractions import Fraction

from sciengformulary.catalog.mathematics.characteristic_polynomial_2x2 import (
    characteristic_polynomial_2x2,
)
from sciengformulary.catalog.mathematics.circle_area import circle_area
from sciengformulary.catalog.mathematics.cramer_rule_3x3_x import cramer_rule_3x3_x
from sciengformulary.catalog.mathematics.cramer_rule_3x3_y import cramer_rule_3x3_y
from sciengformulary.catalog.mathematics.cramer_rule_3x3_z import cramer_rule_3x3_z
from sciengformulary.catalog.mathematics.distance_between_points_2d import (
    distance_between_points_2d,
)
from sciengformulary.catalog.mathematics.distance_point_to_line_3d import (
    distance_point_to_line_3d,
)
from sciengformulary.catalog.mathematics.dot_product_3d import dot_product_3d
from sciengformulary.catalog.mathematics.dot_product_from_magnitudes_and_angle import (
    dot_product_from_magnitudes_and_angle,
)
from sciengformulary.catalog.mathematics.parallelogram_area_3d_vectors import (
    parallelogram_area_3d_vectors,
)
from sciengformulary.catalog.mathematics.parallelogram_area_from_sides_and_angle import (
    parallelogram_area_from_sides_and_angle,
)
from sciengformulary.catalog.mathematics.pythagorean_hypotenuse import pythagorean_hypotenuse
from sciengformulary.catalog.mathematics.right_triangle_altitude_geometric_mean import (
    right_triangle_altitude_geometric_mean,
)
from sciengformulary.catalog.mathematics.right_triangle_angle_from_legs import (
    right_triangle_angle_from_legs,
)
from sciengformulary.catalog.mathematics.scalar_projection_3d import scalar_projection_3d
from sciengformulary.catalog.mathematics.vector_magnitude_3d import vector_magnitude_3d

EXPECTED_NAMES = (
    "characteristic_polynomial_2x2",
    "circle_area",
    "cramer_rule_3x3_x",
    "cramer_rule_3x3_y",
    "cramer_rule_3x3_z",
    "distance_between_points_2d",
    "distance_point_to_line_3d",
    "dot_product_3d",
    "dot_product_from_magnitudes_and_angle",
    "parallelogram_area_3d_vectors",
    "parallelogram_area_from_sides_and_angle",
    "pythagorean_hypotenuse",
    "right_triangle_altitude_geometric_mean",
    "right_triangle_angle_from_legs",
    "scalar_projection_3d",
    "vector_magnitude_3d",
)

ALL_FORMULAS = (
    characteristic_polynomial_2x2,
    circle_area,
    cramer_rule_3x3_x,
    cramer_rule_3x3_y,
    cramer_rule_3x3_z,
    distance_between_points_2d,
    distance_point_to_line_3d,
    dot_product_3d,
    dot_product_from_magnitudes_and_angle,
    parallelogram_area_3d_vectors,
    parallelogram_area_from_sides_and_angle,
    pythagorean_hypotenuse,
    right_triangle_altitude_geometric_mean,
    right_triangle_angle_from_legs,
    scalar_projection_3d,
    vector_magnitude_3d,
)

CRAMER = (cramer_rule_3x3_x, cramer_rule_3x3_y, cramer_rule_3x3_z)
NON_FINITE = (math.nan, math.inf, -math.inf)
UV = ("ux", "uy", "uz", "vx", "vy", "vz")


def _close(actual, expected, rel_tol=1e-12, abs_tol=0.0):
    return math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol)


def _det(matrix):
    """Determinant by the Leibniz formula in exact fractions (independent of the evaluators)."""
    size = len(matrix)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            1 for i in range(size) for j in range(i + 1, size) if permutation[i] > permutation[j]
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= Fraction(matrix[row][column])
        total += term
    return total


def _system3(matrix, rhs):
    values = {f"a{i + 1}{j + 1}": matrix[i][j] for i in range(3) for j in range(3)}
    values.update({f"b{i + 1}": rhs[i] for i in range(3)})
    return values


def _cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def _uv(u, v):
    return dict(zip(UV, (*u, *v)))


def _line(point, base, direction):
    names = ("x0", "y0", "z0", "x1", "y1", "z1", "dx", "dy", "dz")
    return dict(zip(names, (*point, *base, *direction)))


class ConstructionTest(unittest.TestCase):
    def test_ids_match_module_names(self):
        self.assertEqual(
            tuple(formula.id for formula in ALL_FORMULAS),
            tuple(f"mathematics.{name}" for name in EXPECTED_NAMES),
        )

    def test_validate_and_verify_pass(self):
        for formula in ALL_FORMULAS:
            with self.subTest(formula=formula.id):
                formula.validate()
                formula.verify()

    def test_every_input_rejects_non_finite_values(self):
        for formula in ALL_FORMULAS:
            base = dict(formula.verification_cases[0].inputs)
            for name in formula.input_names:
                for bad in (*NON_FINITE, True, "1"):
                    with self.subTest(formula=formula.id, input=name, value=bad):
                        with self.assertRaises(ValueError):
                            formula.evaluate(**{**base, name: bad})

    def test_results_are_floats(self):
        for formula in ALL_FORMULAS:
            for case in formula.verification_cases:
                with self.subTest(formula=formula.id):
                    self.assertIsInstance(formula.evaluate(**case.inputs), float)

    def test_derived_formulas_say_so(self):
        derived = (
            characteristic_polynomial_2x2,
            cramer_rule_3x3_x,
            cramer_rule_3x3_y,
            cramer_rule_3x3_z,
            distance_point_to_line_3d,
            parallelogram_area_3d_vectors,
            pythagorean_hypotenuse,
            right_triangle_altitude_geometric_mean,
            scalar_projection_3d,
        )
        for formula in derived:
            with self.subTest(formula=formula.id):
                self.assertTrue(
                    any(text.startswith("Derived result:") for text in formula.assumptions)
                )


class CharacteristicPolynomialTest(unittest.TestCase):
    A = {"a11": -5, "a12": 2, "a21": -7, "a22": 4}

    def test_eigenvalues_are_roots(self):
        # Oracle cases charpoly_Aex_root_2 and charpoly_Aex_root_minus3: lambda^2 + lambda - 6.
        for lam in (2, -3):
            self.assertEqual(characteristic_polynomial_2x2.evaluate(**self.A, lam=lam), 0.0)

    def test_matches_leibniz_determinant_of_shifted_matrix(self):
        # The source's definition det(A - lam I), evaluated separately in exact fractions.
        rng = random.Random(20261009)
        for _ in range(60):
            a11, a12, a21, a22 = (rng.randint(-20, 20) for _ in range(4))
            lam = rng.randint(-20, 20) / 4
            shifted = ((a11 - Fraction(lam), a12), (a21, a22 - Fraction(lam)))
            expected = float(_det(shifted))
            result = characteristic_polynomial_2x2.evaluate(
                a11=a11, a12=a12, a21=a21, a22=a22, lam=lam
            )
            self.assertEqual(result, expected)

    def test_trace_determinant_form(self):
        # Hand check of lam^2 - trace * lam + det for [[3, 1.5], [-0.25, 2]], lam = 2.75:
        # 7.5625 - 13.75 + 6.375 = 0.1875 (oracle charpoly_general).
        result = characteristic_polynomial_2x2.evaluate(a11=3, a12=1.5, a21=-0.25, a22=2, lam=2.75)
        self.assertEqual(result, 0.1875)

    def test_value_at_zero_is_determinant(self):
        # Oracle case charpoly_Aex_lam0_det: det A = -20 + 14 = -6.
        self.assertEqual(characteristic_polynomial_2x2.evaluate(**self.A, lam=0), -6.0)

    def test_no_real_eigenvalue_example_has_no_root(self):
        # Rotation matrix: p = lam^2 + 1 > 0 for every real lam (oracle charpoly_rot_lam0).
        for lam in (0, 1.5, -3):
            result = characteristic_polynomial_2x2.evaluate(a11=0, a12=-1, a21=1, a22=0, lam=lam)
            self.assertEqual(result, lam * lam + 1)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            characteristic_polynomial_2x2.evaluate(a11=1e200, a12=0, a21=0, a22=1e200, lam=-1e200)


class CircleAreaTest(unittest.TestCase):
    def test_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            circle_area.evaluate(r=-1.0)

    def test_zero_radius_gives_zero(self):
        self.assertEqual(circle_area.evaluate(r=0), 0.0)

    def test_hand_values(self):
        # Hand calculation: 100 * pi for r = 10 and (1/2)^2 * pi for r = 0.5.
        self.assertTrue(_close(circle_area.evaluate(r=10), 314.1592653589793))
        self.assertTrue(_close(circle_area.evaluate(r=0.5), 0.7853981633974483))

    def test_area_scales_with_radius_squared(self):
        self.assertTrue(_close(circle_area.evaluate(r=3.0), 9 * circle_area.evaluate(r=1.0)))

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            circle_area.evaluate(r=1e200)


class CramerRule3x3Test(unittest.TestCase):
    SYSTEMS = {
        # Oracle systems cramer3_*: exact fraction solutions.
        "selinger": (((1, 2, 1), (3, 2, 1), (1, 4, 1)), (3, 5, 6), (1, Fraction(3, 2), -1)),
        "classic": (((2, 1, -1), (-3, -1, 2), (-2, 1, 2)), (8, -11, -3), (2, 3, -1)),
        "fractional": (((4, -2, 1), (-2, 4, -2), (1, -2, 4)), (11, -16, 17), (1, -2, 3)),
    }

    def test_oracle_systems(self):
        for name, (matrix, rhs, solution) in self.SYSTEMS.items():
            for formula, expected in zip(CRAMER, solution):
                with self.subTest(system=name, formula=formula.id):
                    result = formula.evaluate(**_system3(matrix, rhs))
                    self.assertEqual(result, float(expected))

    def test_decimal_system_matches_exact_fractions(self):
        # Oracle cramer3_decimal_*: solution (252/263, 272/263, 90/263).
        matrix = ((0.5, 1, -1.5), (2, -0.25, 1), (-1, 3, 2.5))
        values = _system3(matrix, (1, 2, 3))
        for formula, expected in zip(CRAMER, (252, 272, 90)):
            with self.subTest(formula=formula.id):
                self.assertTrue(_close(formula.evaluate(**values), expected / 263))

    def test_matches_ratio_of_leibniz_determinants(self):
        # The source's form x_i = det(A_i) / det(A), evaluated separately in exact fractions.
        rng = random.Random(1234)
        checked = 0
        while checked < 40:
            matrix = [[rng.randint(-9, 9) for _ in range(3)] for _ in range(3)]
            rhs = [rng.randint(-9, 9) for _ in range(3)]
            det = _det(matrix)
            if det == 0:
                continue
            checked += 1
            for column, formula in enumerate(CRAMER):
                replaced = [
                    [rhs[row] if col == column else matrix[row][col] for col in range(3)]
                    for row in range(3)
                ]
                expected = float(_det(replaced) / det)
                with self.subTest(formula=formula.id, matrix=matrix, rhs=rhs):
                    self.assertEqual(formula.evaluate(**_system3(matrix, rhs)), expected)

    def test_solution_satisfies_the_equations(self):
        matrix = ((3.5, -1, 2), (0.5, 4, -1.25), (2, 0.75, 5))
        rhs = (1.5, -2, 4)
        values = _system3(matrix, rhs)
        solution = [formula.evaluate(**values) for formula in CRAMER]
        for row in range(3):
            residual = sum(matrix[row][col] * solution[col] for col in range(3)) - rhs[row]
            self.assertAlmostEqual(residual, 0.0, places=12)

    def test_identity_matrix_returns_right_hand_side(self):
        identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        values = _system3(identity, (7, -2, 0.5))
        for formula, expected in zip(CRAMER, (7.0, -2.0, 0.5)):
            self.assertEqual(formula.evaluate(**values), expected)

    def test_singular_matrix_raises(self):
        # Rows 1, 2, 3 = (1, 2, 3), (4, 5, 6), (7, 8, 9): determinant exactly 0.
        values = _system3(((1, 2, 3), (4, 5, 6), (7, 8, 9)), (1, 2, 3))
        for formula in CRAMER:
            with self.subTest(formula=formula.id):
                with self.assertRaises(ValueError):
                    formula.evaluate(**values)

    def test_zero_row_raises(self):
        values = _system3(((1, 2, 3), (0, 0, 0), (7, 8, 10)), (1, 2, 3))
        for formula in CRAMER:
            with self.subTest(formula=formula.id):
                with self.assertRaises(ValueError):
                    formula.evaluate(**values)

    def test_unit_triangular_system(self):
        # Hand calculation: the matrix is unit upper triangular (determinant 1), so
        # z = 1, y = 1 and x = 1e3 - 1e3 * y = 0.
        values = _system3(((1, 1e3, 0), (0, 1, 0), (0, 0, 1)), (1e3, 1, 1))
        self.assertEqual(cramer_rule_3x3_x.evaluate(**values), 0.0)

    def test_overflow_raises(self):
        values = _system3(((1e200, 0, 0), (0, 1e200, 0), (0, 0, 1e200)), (1, 0, 0))
        with self.assertRaises(OverflowError):
            cramer_rule_3x3_x.evaluate(**values)


class DistanceBetweenPoints2dTest(unittest.TestCase):
    def test_triples(self):
        # Hand calculation: 5-12-13 and 8-15-17 right triangles.
        self.assertEqual(distance_between_points_2d.evaluate(x1=0, y1=0, x2=5, y2=12), 13.0)
        self.assertEqual(distance_between_points_2d.evaluate(x1=1, y1=1, x2=-7, y2=-14), 17.0)

    def test_symmetric(self):
        forward = distance_between_points_2d.evaluate(x1=-1.5, y1=2.25, x2=3.0, y2=-0.75)
        backward = distance_between_points_2d.evaluate(x1=3.0, y1=-0.75, x2=-1.5, y2=2.25)
        self.assertEqual(forward, backward)

    def test_coincident_points_give_zero(self):
        # Oracle case dist2d_same.
        self.assertEqual(distance_between_points_2d.evaluate(x1=2.5, y1=-1, x2=2.5, y2=-1), 0.0)

    def test_difference_overflow_raises(self):
        with self.assertRaises(OverflowError):
            distance_between_points_2d.evaluate(x1=-1.7e308, y1=0, x2=1.7e308, y2=0)


class DistancePointToLineTest(unittest.TestCase):
    def test_zero_direction_raises(self):
        with self.assertRaises(ValueError):
            distance_point_to_line_3d.evaluate(**_line((1, 2, 3), (0, 0, 0), (0, 0, 0)))

    @staticmethod
    def _projection_squared(point, base, direction):
        """Selinger's procedure: |w - proj_d(w)|^2 in exact fractions, w = point - base."""
        w = [Fraction(p) - Fraction(b) for p, b in zip(point, base)]
        d = [Fraction(c) for c in direction]
        t = _dot(d, w) / _dot(d, d)
        return _dot([wi - t * di for wi, di in zip(w, d)], [wi - t * di for wi, di in zip(w, d)])

    def test_oracle_squared_distances(self):
        # Oracle pointline_*: exact squared distances 26, 26, 25, 2225/144 and 0.
        cases = (
            (((1, 3, 5), (0, 4, -2), (2, 1, 2)), Fraction(26)),
            (((1, 3, 5), (0, 4, -2), (-4, -2, -4)), Fraction(26)),
            (((5, 3, 4), (-7, 0, 0), (0.5, 0, 0)), Fraction(25)),
            (((1.5, -2, 0.25), (-1, 0.5, 2), (1, 2, -2)), Fraction(2225, 144)),
            (((4, 6, 2), (0, 4, -2), (2, 1, 2)), Fraction(0)),
        )
        for (point, base, direction), squared in cases:
            with self.subTest(point=point, direction=direction):
                result = distance_point_to_line_3d.evaluate(**_line(point, base, direction))
                self.assertTrue(_close(result**2, float(squared), abs_tol=1e-12))

    def test_matches_projection_procedure_on_random_lines(self):
        # Derived closed form versus the source's projection procedure (exact fractions).
        rng = random.Random(77)
        for _ in range(60):
            point = [rng.randint(-15, 15) for _ in range(3)]
            base = [rng.randint(-15, 15) for _ in range(3)]
            direction = [rng.randint(-6, 6) for _ in range(3)]
            if not any(direction):
                continue
            squared = self._projection_squared(point, base, direction)
            result = distance_point_to_line_3d.evaluate(**_line(point, base, direction))
            with self.subTest(point=point, base=base, direction=direction):
                self.assertTrue(_close(result, math.sqrt(float(squared)), abs_tol=1e-12))

    def test_matches_numerical_minimisation(self):
        # Independent route: minimise |base + t d - point| over t by ternary search.
        point, base, direction = (1.5, -2, 0.25), (-1, 0.5, 2), (1, 2, -2)

        def gap(t):
            return math.dist(point, [b + t * d for b, d in zip(base, direction)])

        low, high = -100.0, 100.0
        for _ in range(200):
            first, second = low + (high - low) / 3, high - (high - low) / 3
            if gap(first) < gap(second):
                high = second
            else:
                low = first
        result = distance_point_to_line_3d.evaluate(**_line(point, base, direction))
        self.assertTrue(_close(result, gap((low + high) / 2), rel_tol=1e-9))

    def test_direction_scale_does_not_matter(self):
        # Hand check: the x-axis through the origin and the point (0, 3, 4) are 5 apart.
        for scale in (1, -1, 2.5, 1e-200, 1e200, -3e150):
            direction = (scale, 0, 0)
            result = distance_point_to_line_3d.evaluate(**_line((0, 3, 4), (0, 0, 0), direction))
            with self.subTest(scale=scale):
                self.assertTrue(_close(result, 5.0))

    def test_tiny_and_huge_geometry_does_not_underflow_or_overflow(self):
        tiny = distance_point_to_line_3d.evaluate(
            **_line((0, 3e-170, 4e-170), (0, 0, 0), (1e-170, 0, 0))
        )
        huge = distance_point_to_line_3d.evaluate(
            **_line((0, 3e200, 4e200), (0, 0, 0), (1e200, 0, 0))
        )
        self.assertTrue(_close(tiny, 5e-170))
        self.assertTrue(_close(huge, 5e200))

    def test_point_on_line_gives_zero(self):
        # Oracle pointline_on_line: P + 2d lies on the line.
        result = distance_point_to_line_3d.evaluate(**_line((4, 6, 2), (0, 4, -2), (2, 1, 2)))
        self.assertEqual(result, 0.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            distance_point_to_line_3d.evaluate(
                **_line((0, 1.7e308, 0), (0, -1.7e308, 0), (1, 0, 0))
            )


class DotProductTest(unittest.TestCase):
    def test_orthogonal_and_zero(self):
        self.assertEqual(dot_product_3d.evaluate(**_uv((1, 0, 0), (0, 1, 0))), 0.0)
        self.assertEqual(dot_product_3d.evaluate(**_uv((0, 0, 0), (7.5, -3, 2))), 0.0)

    def test_symmetric_and_bilinear(self):
        u, v = (2, 3, -4), (1, -2, 1)
        forward = dot_product_3d.evaluate(**_uv(u, v))
        self.assertEqual(forward, dot_product_3d.evaluate(**_uv(v, u)))
        # Hand calculation: 2 - 6 - 4 = -8 (Selinger sec. 2.6 prints -8); doubling u doubles it.
        self.assertEqual(forward, -8.0)
        self.assertEqual(dot_product_3d.evaluate(**_uv((4, 6, -8), v)), 2 * forward)

    def test_self_product_is_squared_length(self):
        # Hand calculation: 2^2 + 3^2 + 6^2 = 49.
        self.assertEqual(dot_product_3d.evaluate(**_uv((2, 3, 6), (2, 3, 6))), 49.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            dot_product_3d.evaluate(**_uv((1e200, 0, 0), (1e200, 0, 0)))


class DotProductFromAngleTest(unittest.TestCase):
    NAMES = ("u_norm", "v_norm", "theta")

    def test_negative_length_raises(self):
        for name in ("u_norm", "v_norm"):
            values = {"u_norm": 1.0, "v_norm": 1.0, "theta": 1.0, name: -1.0}
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    dot_product_from_magnitudes_and_angle.evaluate(**values)

    def test_angle_outside_range_raises(self):
        for theta in (-1e-9, -1.0, math.pi * (1 + 1e-12), 4.0, 2 * math.pi):
            with self.subTest(theta=theta):
                with self.assertRaises(ValueError):
                    dot_product_from_magnitudes_and_angle.evaluate(
                        u_norm=1.0, v_norm=1.0, theta=theta
                    )

    def test_boundaries_are_accepted(self):
        # Oracle dotang_parallel and dotang_antiparallel.
        edge = dot_product_from_magnitudes_and_angle
        self.assertEqual(edge.evaluate(u_norm=2.5, v_norm=4, theta=0), 10.0)
        self.assertTrue(_close(edge.evaluate(u_norm=2, v_norm=5, theta=math.pi), -10.0))

    def test_matches_explicit_vectors(self):
        # Independent route: dot product of explicit vectors at the given included angle.
        for theta in (0.3, 1.0, 2.0, 3.0):
            u = (1.5, 0.0, 0.0)
            v = (0.4 * math.cos(theta), 0.4 * math.sin(theta), 0.0)
            result = dot_product_from_magnitudes_and_angle.evaluate(
                u_norm=1.5, v_norm=0.4, theta=theta
            )
            with self.subTest(theta=theta):
                self.assertTrue(_close(result, _dot(u, v), abs_tol=1e-15))

    def test_zero_length_gives_zero_for_any_angle(self):
        # Oracle dotang_zero_length.
        for theta in (0.0, 1.0, math.pi):
            result = dot_product_from_magnitudes_and_angle.evaluate(u_norm=0, v_norm=7, theta=theta)
            self.assertEqual(result, 0.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            dot_product_from_magnitudes_and_angle.evaluate(u_norm=1e200, v_norm=1e200, theta=0)


class ParallelogramAreaTest(unittest.TestCase):
    def test_oracle_squared_areas_by_lagrange_identity(self):
        # Oracle pgram3d_*: exact squared areas 35, 65, 144, 225/16 and 0.
        cases = (
            (((1, -1, 2), (3, -2, 1)), 35.0),
            (((1, 2, 2), (-2, 1, 2)), 65.0),
            (((3, 0, 0), (0, 4, 0)), 144.0),
            (((0.5, -1.5, 2.0), (1.25, 0.75, -1)), 225 / 16),
            (((1, 2, 3), (-2, -4, -6)), 0.0),
        )
        for (u, v), squared in cases:
            with self.subTest(u=u, v=v):
                result = parallelogram_area_3d_vectors.evaluate(**_uv(u, v))
                self.assertTrue(_close(result**2, squared, abs_tol=1e-12))

    def test_matches_lagrange_identity_on_random_vectors(self):
        # Derived length of the cross product versus |u|^2 |v|^2 - (u . v)^2 in exact fractions.
        rng = random.Random(5)
        for _ in range(60):
            u = [rng.randint(-12, 12) for _ in range(3)]
            v = [rng.randint(-12, 12) for _ in range(3)]
            squared = _dot(u, u) * _dot(v, v) - _dot(u, v) ** 2
            result = parallelogram_area_3d_vectors.evaluate(**_uv(u, v))
            with self.subTest(u=u, v=v):
                self.assertTrue(_close(result, math.sqrt(squared), abs_tol=1e-12))

    def test_swapping_sides_keeps_the_area(self):
        u, v = (1, -1, 2), (3, -2, 1)
        forward = parallelogram_area_3d_vectors.evaluate(**_uv(u, v))
        self.assertEqual(forward, parallelogram_area_3d_vectors.evaluate(**_uv(v, u)))

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            parallelogram_area_3d_vectors.evaluate(**_uv((1e200, 0, 0), (0, 1e200, 0)))

    def test_angle_form_negative_side_raises(self):
        for name in ("a", "b"):
            values = {"a": 1.0, "b": 1.0, "theta": 1.0, name: -1.0}
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    parallelogram_area_from_sides_and_angle.evaluate(**values)

    def test_angle_form_angle_outside_range_raises(self):
        for theta in (-1e-9, math.pi * (1 + 1e-12), 4.0):
            with self.subTest(theta=theta):
                with self.assertRaises(ValueError):
                    parallelogram_area_from_sides_and_angle.evaluate(a=1.0, b=1.0, theta=theta)

    def test_angle_form_boundaries(self):
        form = parallelogram_area_from_sides_and_angle
        self.assertEqual(form.evaluate(a=4, b=5, theta=0), 0.0)
        self.assertEqual(form.evaluate(a=0, b=5, theta=1.0), 0.0)
        # sin of the float nearest pi is about 1.2e-16, so the area is about 3e-16.
        self.assertLess(form.evaluate(a=2.5, b=4, theta=math.pi), 1e-12)

    def test_angle_form_matches_cross_product_of_explicit_sides(self):
        # Independent route: |u x v| for explicit vectors at the included angle.
        for theta in (0.4, 1.3, 2.0944, 3.0):
            u = (3.0, 0.0, 0.0)
            v = (4.0 * math.cos(theta), 4.0 * math.sin(theta), 0.0)
            expected = math.hypot(*_cross(u, v))
            result = parallelogram_area_from_sides_and_angle.evaluate(a=3, b=4, theta=theta)
            with self.subTest(theta=theta):
                self.assertTrue(_close(result, expected))

    def test_angle_form_overflow_raises(self):
        with self.assertRaises(OverflowError):
            parallelogram_area_from_sides_and_angle.evaluate(a=1e200, b=1e200, theta=1.0)


class RightTriangleTest(unittest.TestCase):
    def test_pythagorean_domain(self):
        for values in ({"a": 0, "b": 1}, {"a": 1, "b": 0}, {"a": -3, "b": 4}, {"a": 3, "b": -4}):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    pythagorean_hypotenuse.evaluate(**values)

    def test_pythagorean_matches_integer_triples(self):
        # Independent route: enumerate integer legs whose squared sum is a perfect square.
        found = 0
        for a in range(1, 61):
            for b in range(a, 61):
                root = math.isqrt(a * a + b * b)
                if root * root == a * a + b * b:
                    found += 1
                    with self.subTest(a=a, b=b):
                        self.assertEqual(pythagorean_hypotenuse.evaluate(a=a, b=b), float(root))
                        self.assertEqual(pythagorean_hypotenuse.evaluate(a=b, b=a), float(root))
        self.assertGreater(found, 15)

    def test_pythagorean_matches_coordinate_distance(self):
        rng = random.Random(9)
        for _ in range(40):
            a, b = rng.uniform(0.01, 100), rng.uniform(0.01, 100)
            with self.subTest(a=a, b=b):
                result = pythagorean_hypotenuse.evaluate(a=a, b=b)
                self.assertTrue(_close(result, math.dist((a, 0.0), (0.0, b))))
                self.assertTrue(_close(result * result, a * a + b * b))

    def test_pythagorean_overflow_raises(self):
        with self.assertRaises(OverflowError):
            pythagorean_hypotenuse.evaluate(a=1.7e308, b=1.7e308)

    def test_altitude_domain(self):
        for values in ({"p": 0, "q": 1}, {"p": 1, "q": 0}, {"p": -1, "q": 4}, {"p": 1, "q": -4}):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    right_triangle_altitude_geometric_mean.evaluate(**values)

    def test_altitude_matches_integer_products(self):
        # Independent route: enumerate integer segments whose product is a perfect square.
        found = 0
        for p in range(1, 61):
            for q in range(1, 61):
                root = math.isqrt(p * q)
                if root * root == p * q:
                    found += 1
                    with self.subTest(p=p, q=q):
                        result = right_triangle_altitude_geometric_mean.evaluate(p=p, q=q)
                        self.assertEqual(result, float(root))
        self.assertGreater(found, 100)

    def test_altitude_gives_a_right_angle_in_coordinates(self):
        # Independent route: A = (-p, 0), B = (q, 0), C = (0, h) has a right angle at C
        # exactly when (A - C) . (B - C) = h^2 - p q vanishes (oracle altitude_* construction).
        rng = random.Random(3)
        for _ in range(40):
            p, q = rng.uniform(0.05, 50), rng.uniform(0.05, 50)
            h = right_triangle_altitude_geometric_mean.evaluate(p=p, q=q)
            dot = (-p - 0.0) * (q - 0.0) + (0.0 - h) * (0.0 - h)
            with self.subTest(p=p, q=q):
                self.assertLess(abs(dot), 1e-12 * p * q)
                self.assertTrue(_close(math.hypot(p, h) ** 2, (p + q) * p))

    def test_altitude_is_symmetric_and_stays_in_range(self):
        # p = 1e-300, q = 1e300 has product 1: forming p * q directly would be fine, but the
        # extreme magnitudes of the factors must not matter.
        form = right_triangle_altitude_geometric_mean
        self.assertEqual(form.evaluate(p=2, q=3), form.evaluate(p=3, q=2))
        self.assertTrue(_close(form.evaluate(p=1e-300, q=1e300), 1.0))
        self.assertTrue(_close(form.evaluate(p=1e200, q=1e-200), 1.0))

    def test_angle_domain(self):
        for values in (
            {"opposite": 0, "adjacent": 1},
            {"opposite": 1, "adjacent": 0},
            {"opposite": -1, "adjacent": 1},
            {"opposite": 1, "adjacent": -1},
        ):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    right_triangle_angle_from_legs.evaluate(**values)

    def test_angle_matches_arccos_and_arcsin_routes(self):
        # Mathlib's sibling theorems: the same angle from adjacent/hypotenuse and
        # opposite/hypotenuse (oracle rtangle_345: arctan(3/4) = arccos(4/5) = arcsin(3/5)).
        for opposite, adjacent in ((3, 4), (1, 1), (2.5, 0.5), (0.2, 7), (5, 12)):
            hypotenuse = math.hypot(opposite, adjacent)
            result = right_triangle_angle_from_legs.evaluate(opposite=opposite, adjacent=adjacent)
            with self.subTest(opposite=opposite, adjacent=adjacent):
                self.assertTrue(_close(result, math.acos(adjacent / hypotenuse), rel_tol=1e-12))
                self.assertTrue(_close(result, math.asin(opposite / hypotenuse), rel_tol=1e-12))
                self.assertTrue(_close(math.tan(result), opposite / adjacent, rel_tol=1e-12))

    def test_angle_range_and_complement(self):
        for opposite, adjacent in ((3, 4), (1e-9, 1), (1, 1e-9), (12, 5)):
            forward = right_triangle_angle_from_legs.evaluate(opposite=opposite, adjacent=adjacent)
            other = right_triangle_angle_from_legs.evaluate(opposite=adjacent, adjacent=opposite)
            with self.subTest(opposite=opposite, adjacent=adjacent):
                self.assertGreater(forward, 0.0)
                self.assertLess(forward, math.pi / 2)
                self.assertTrue(_close(forward + other, math.pi / 2))

    def test_angle_extreme_ratio_stays_finite(self):
        result = right_triangle_angle_from_legs.evaluate(opposite=1e300, adjacent=1e-300)
        self.assertTrue(_close(result, math.pi / 2))


class VectorTest(unittest.TestCase):
    def test_magnitude_pythagorean_quadruples(self):
        # Hand calculation: 1 + 16 + 64 = 81 and 16 + 16 + 49 = 81, both 9.
        self.assertEqual(vector_magnitude_3d.evaluate(ux=1, uy=4, uz=8), 9.0)
        self.assertEqual(vector_magnitude_3d.evaluate(ux=4, uy=-4, uz=7), 9.0)

    def test_magnitude_is_symmetric_in_components_and_sign(self):
        values = (2.0, 3.0, 6.0)
        for permutation in itertools.permutations(values):
            result = vector_magnitude_3d.evaluate(
                ux=permutation[0], uy=-permutation[1], uz=permutation[2]
            )
            self.assertEqual(result, 7.0)

    def test_magnitude_scales_linearly(self):
        base = vector_magnitude_3d.evaluate(ux=0.1, uy=0.2, uz=-0.3)
        self.assertTrue(_close(vector_magnitude_3d.evaluate(ux=1e5, uy=2e5, uz=-3e5), 1e6 * base))

    def test_magnitude_overflow_raises(self):
        with self.assertRaises(OverflowError):
            vector_magnitude_3d.evaluate(ux=1.7e308, uy=1.7e308, uz=1.7e308)

    def test_scalar_projection_zero_u_raises(self):
        with self.assertRaises(ValueError):
            scalar_projection_3d.evaluate(**_uv((0, 0, 0), (1, 2, 3)))

    def test_scalar_projection_matches_dot_over_length_in_exact_fractions(self):
        # Derived form versus c^2 = (u . v)^2 / (u . u) with the sign of u . v (exact fractions).
        rng = random.Random(41)
        for _ in range(60):
            u = [rng.randint(-9, 9) for _ in range(3)]
            v = [rng.randint(-9, 9) for _ in range(3)]
            if not any(u):
                continue
            dot = _dot(u, v)
            squared = Fraction(dot * dot, _dot(u, u))
            expected = math.copysign(math.sqrt(float(squared)), dot)
            result = scalar_projection_3d.evaluate(**_uv(u, v))
            with self.subTest(u=u, v=v):
                self.assertTrue(_close(result, expected, abs_tol=1e-12))

    def test_scalar_projection_matches_length_times_cosine_of_angle(self):
        # Independent route: |v| cos(theta) with theta = atan2(|u x v|, u . v) (oracle
        # scalproj_*: the |v| cos(theta) route agrees).
        for u, v in (
            ((2, 3, -4), (1, -2, 1)),
            ((1, 2, -2), (2, 1, 3)),
            ((0.5, -1, 2), (3, 0.25, -1.5)),
        ):
            theta = math.atan2(math.hypot(*_cross(u, v)), _dot(u, v))
            expected = math.hypot(*v) * math.cos(theta)
            with self.subTest(u=u, v=v):
                self.assertTrue(_close(scalar_projection_3d.evaluate(**_uv(u, v)), expected))

    def test_scalar_projection_scaling_of_u(self):
        u, v = (2, 3, -4), (1, -2, 1)
        base = scalar_projection_3d.evaluate(**_uv(u, v))
        self.assertTrue(_close(scalar_projection_3d.evaluate(**_uv((4, 6, -8), v)), base))
        self.assertTrue(_close(scalar_projection_3d.evaluate(**_uv((-2, -3, 4), v)), -base))

    def test_scalar_projection_tiny_and_huge_vectors(self):
        # u along x, so c is the x component of v (hand value); a naive u . v would underflow
        # to 0 or overflow to inf here.
        tiny = scalar_projection_3d.evaluate(**_uv((1e-200, 0, 0), (3e-200, 5e-200, 0)))
        huge = scalar_projection_3d.evaluate(**_uv((1e200, 0, 0), (1e200, 5, 0)))
        self.assertTrue(_close(tiny, 3e-200))
        self.assertTrue(_close(huge, 1e200))


class ParallelogramAreaCancellationTest(unittest.TestCase):
    """Cross-product components whose products overflow but cancel (review fix)."""

    def test_overflowing_products_that_cancel_do_not_raise(self):
        # 900-digit mpmath (oracle script oracles.py): the exact area is sqrt(2) in both cases;
        # the unscaled products 1e200 * 1e200 used to give inf - inf = nan.
        cases = (
            ((1e200, 1e200, 0), (1e200, 1e200, 1e-200), 1.414213562373095),
            ((1e-200, 1e-200, 0), (1e-200, 1e-200, 1e200), 1.414213562373095),
        )
        for u, v, expected in cases:
            with self.subTest(u=u, v=v):
                actual = parallelogram_area_3d_vectors.evaluate(**_uv(u, v))
                self.assertTrue(_close(actual, expected, 1e-15), actual)

    def test_area_beyond_the_float_range_still_raises(self):
        u = (3e307, 3e307, 1.0)
        v = (3e307, 3e307 * (1 + 2**-52), 0.0)  # c_z is about 2e599
        with self.assertRaises(OverflowError):
            parallelogram_area_3d_vectors.evaluate(**_uv(u, v))


class VectorDimensionPolicyTest(unittest.TestCase):
    """Components of position and displacement vectors are lengths, as in the committed
    parallelepiped_volume and in parallelogram_area_3d_vectors."""

    def test_vector_components_are_lengths_and_the_outputs_follow(self):
        expected = {
            vector_magnitude_3d: ("L", "m"),
            dot_product_3d: ("L^2", "m^2"),
            scalar_projection_3d: ("L", "m"),
            parallelogram_area_3d_vectors: ("L^2", "m^2"),
        }
        for formula, (dimension, unit) in expected.items():
            with self.subTest(formula=formula.id):
                for variable in formula.inputs:
                    self.assertEqual((variable.dimension, variable.si_unit), ("L", "m"))
                self.assertEqual(
                    (formula.output.dimension, formula.output.si_unit), (dimension, unit)
                )

    def test_assumptions_state_any_consistent_length_unit(self):
        for formula in (vector_magnitude_3d, dot_product_3d, scalar_projection_3d):
            with self.subTest(formula=formula.id):
                self.assertTrue(
                    any("any consistent length unit" in text for text in formula.assumptions)
                )


if __name__ == "__main__":
    unittest.main()

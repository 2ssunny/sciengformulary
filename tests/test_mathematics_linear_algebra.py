"""Tests for the linear-algebra and vector-geometry formulas in the mathematics domain.

Extra numeric expectations come from the independent oracle used to verify these formulas
(exact fractions, 50-digit mpmath, sympy) or from hand calculations stated next to them; none
is produced by the evaluators under test.
"""

import math
import unittest

from sciengformulary.catalog.mathematics.angle_between_vectors_3d import (
    angle_between_vectors_3d,
)
from sciengformulary.catalog.mathematics.cramer_rule_2x2_x import cramer_rule_2x2_x
from sciengformulary.catalog.mathematics.cramer_rule_2x2_y import cramer_rule_2x2_y
from sciengformulary.catalog.mathematics.determinant_2x2 import determinant_2x2
from sciengformulary.catalog.mathematics.determinant_3x3 import determinant_3x3
from sciengformulary.catalog.mathematics.distance_between_points_3d import (
    distance_between_points_3d,
)
from sciengformulary.catalog.mathematics.distance_point_to_plane import distance_point_to_plane
from sciengformulary.catalog.mathematics.parallelepiped_volume import parallelepiped_volume
from sciengformulary.catalog.mathematics.triangle_area_from_vertices_3d import (
    triangle_area_from_vertices_3d,
)

ALL_FORMULAS = (
    determinant_2x2,
    determinant_3x3,
    cramer_rule_2x2_x,
    cramer_rule_2x2_y,
    distance_between_points_3d,
    angle_between_vectors_3d,
    distance_point_to_plane,
    parallelepiped_volume,
    triangle_area_from_vertices_3d,
)

NON_FINITE = (math.nan, math.inf, -math.inf)


def _matrix3(rows):
    return {f"a{i + 1}{j + 1}": rows[i][j] for i in range(3) for j in range(3)}


def _vectors(names, *vectors):
    values = [component for vector in vectors for component in vector]
    return dict(zip(names, values))


class ConstructionTest(unittest.TestCase):
    def test_ids_match_module_names(self):
        expected = (
            "determinant_2x2",
            "determinant_3x3",
            "cramer_rule_2x2_x",
            "cramer_rule_2x2_y",
            "distance_between_points_3d",
            "angle_between_vectors_3d",
            "distance_point_to_plane",
            "parallelepiped_volume",
            "triangle_area_from_vertices_3d",
        )
        self.assertEqual(
            tuple(formula.id for formula in ALL_FORMULAS),
            tuple(f"mathematics.{name}" for name in expected),
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


class DeterminantTest(unittest.TestCase):
    def test_identity_2x2(self):
        # Oracle case det2_identity: exact value 1.
        result = determinant_2x2.evaluate(a11=1, a12=0, a21=0, a22=1)
        self.assertEqual(result, 1.0)

    def test_selinger_cramer_column_determinants(self):
        # Oracle checks of the printed Selinger sec. 7.7 values det(A_1) = 4, det(A_3) = -4.
        a1 = _matrix3(((3, 2, 1), (5, 2, 1), (6, 4, 1)))
        a3 = _matrix3(((1, 2, 3), (3, 2, 5), (1, 4, 6)))
        self.assertEqual(determinant_3x3.evaluate(**a1), 4.0)
        self.assertEqual(determinant_3x3.evaluate(**a3), -4.0)

    def test_returns_float(self):
        self.assertIsInstance(determinant_2x2.evaluate(a11=2, a12=4, a21=-1, a22=6), float)
        self.assertIsInstance(determinant_3x3.evaluate(**_matrix3(((1,) * 3,) * 3)), float)

    def test_singular_matrices_give_exactly_zero(self):
        self.assertEqual(determinant_2x2.evaluate(a11=1, a12=2, a21=2, a22=4), 0.0)
        rows = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
        self.assertEqual(determinant_3x3.evaluate(**_matrix3(rows)), 0.0)


class CramerRuleTest(unittest.TestCase):
    def test_singular_matrix_raises(self):
        singular = {"a11": 1, "a12": 2, "a21": 2, "a22": 4, "b1": 3, "b2": 6}
        for formula in (cramer_rule_2x2_x, cramer_rule_2x2_y):
            with self.subTest(formula=formula.id):
                with self.assertRaises(ValueError):
                    formula.evaluate(**singular)

    def test_solution_satisfies_both_equations(self):
        # Independent check by substitution: the pair (x, y) must reproduce b1 and b2.
        system = {"a11": 4, "a12": -3, "a21": 2, "a22": 7, "b1": 11, "b2": -1}
        x = cramer_rule_2x2_x.evaluate(**system)
        y = cramer_rule_2x2_y.evaluate(**system)
        self.assertAlmostEqual(system["a11"] * x + system["a12"] * y, system["b1"], places=12)
        self.assertAlmostEqual(system["a21"] * x + system["a22"] * y, system["b2"], places=12)

    def test_nearly_singular_matrix_is_not_rejected(self):
        # Oracle case cramer_ill_conditioned: det = 2^-20, exact solution (1, 1).
        system = {"a11": 1, "a12": 1, "a21": 1, "a22": 1 + 2**-20, "b1": 2, "b2": 2 + 2**-20}
        self.assertEqual(cramer_rule_2x2_x.evaluate(**system), 1.0)
        self.assertEqual(cramer_rule_2x2_y.evaluate(**system), 1.0)


class DistanceBetweenPointsTest(unittest.TestCase):
    def test_pythagorean_quadruple(self):
        # Hand calculation: 3^2 + 4^2 + 12^2 = 169, distance 13.
        result = distance_between_points_3d.evaluate(x1=1, y1=-1, z1=2, x2=4, y2=3, z2=14)
        self.assertEqual(result, 13.0)

    def test_coincident_points_give_zero(self):
        result = distance_between_points_3d.evaluate(x1=2.5, y1=-1, z1=7, x2=2.5, y2=-1, z2=7)
        self.assertEqual(result, 0.0)

    def test_large_coordinates_do_not_overflow(self):
        # Hand value: differences (3e200, 4e200, 0) give 5e200; naive squaring overflows.
        result = distance_between_points_3d.evaluate(
            x1=0.0, y1=0.0, z1=0.0, x2=3e200, y2=4e200, z2=0.0
        )
        self.assertTrue(math.isclose(result, 5e200, rel_tol=1e-12))


class AngleBetweenVectorsTest(unittest.TestCase):
    NAMES = ("ux", "uy", "uz", "vx", "vy", "vz")

    def test_zero_u_raises(self):
        with self.assertRaises(ValueError):
            angle_between_vectors_3d.evaluate(**_vectors(self.NAMES, (0, 0, 0), (1, 2, 3)))

    def test_zero_v_raises(self):
        with self.assertRaises(ValueError):
            angle_between_vectors_3d.evaluate(**_vectors(self.NAMES, (1, 2, 3), (0, 0, 0)))

    def test_orthogonal_vectors(self):
        # Oracle case angle_orthogonal: pi / 2 to 50 digits.
        result = angle_between_vectors_3d.evaluate(**_vectors(self.NAMES, (1, 0, 0), (0, 1, 0)))
        self.assertTrue(math.isclose(result, 1.5707963267948966, rel_tol=1e-12))

    def test_range_and_symmetry(self):
        cases = (((-1, 1, 2), (2, 1, -1)), ((1, 2, 3), (-2, -4, -6)), ((7, -1, 0), (4, 3, 5)))
        for u, v in cases:
            with self.subTest(u=u, v=v):
                forward = angle_between_vectors_3d.evaluate(**_vectors(self.NAMES, u, v))
                backward = angle_between_vectors_3d.evaluate(**_vectors(self.NAMES, v, u))
                self.assertGreaterEqual(forward, 0.0)
                self.assertLessEqual(forward, math.pi)
                self.assertEqual(forward, backward)


class DistancePointToPlaneTest(unittest.TestCase):
    def test_zero_normal_raises(self):
        with self.assertRaises(ValueError):
            distance_point_to_plane.evaluate(a=0, b=0, c=0, d=1, x0=1, y0=2, z0=3)

    def test_scaled_plane_equation(self):
        # Oracle case plane_scaled_x2: textbook plane doubled, distance still 4.
        result = distance_point_to_plane.evaluate(a=4, b=2, c=4, d=4, x0=3, y0=2, z0=3)
        self.assertEqual(result, 4.0)

    def test_distance_is_unsigned(self):
        # Hand calculation: plane z = 0, points at z = 5 and z = -5 are both 5 away.
        above = distance_point_to_plane.evaluate(a=0, b=0, c=1, d=0, x0=1, y0=1, z0=5)
        below = distance_point_to_plane.evaluate(a=0, b=0, c=1, d=0, x0=1, y0=1, z0=-5)
        self.assertEqual(above, 5.0)
        self.assertEqual(below, 5.0)


class ParallelepipedVolumeTest(unittest.TestCase):
    NAMES = ("ux", "uy", "uz", "vx", "vy", "vz", "wx", "wy", "wz")

    def test_unit_cube(self):
        # Oracle case box_unit_cube: volume 1.
        values = _vectors(self.NAMES, (1, 0, 0), (0, 1, 0), (0, 0, 1))
        self.assertEqual(parallelepiped_volume.evaluate(**values), 1.0)

    def test_order_independent_and_non_negative(self):
        # Selinger sec. 2.7 worked example (volume 14) under every ordering of u, v, w.
        u, v, w = (1, 2, -5), (1, 3, -6), (3, 2, 3)
        for order in ((u, v, w), (v, u, w), (w, v, u), (u, w, v), (v, w, u), (w, u, v)):
            with self.subTest(order=order):
                result = parallelepiped_volume.evaluate(**_vectors(self.NAMES, *order))
                self.assertEqual(result, 14.0)

    def test_coplanar_vectors_give_zero(self):
        values = _vectors(self.NAMES, (0, 1, 2), (1, 2, 2), (1, 1, 0))
        self.assertEqual(parallelepiped_volume.evaluate(**values), 0.0)


class TriangleAreaTest(unittest.TestCase):
    NAMES = ("x1", "y1", "z1", "x2", "y2", "z2", "x3", "y3", "z3")

    def test_base_vertex_does_not_matter(self):
        # Oracle: the cross product is the same for every cyclic choice of base vertex, so
        # each rotation of the Selinger example gives (3/2) sqrt(6) to 50 digits.
        p, q, r = (1, 2, 3), (0, 2, 5), (5, 1, 2)
        for vertices in ((p, q, r), (q, r, p), (r, p, q)):
            with self.subTest(vertices=vertices):
                result = triangle_area_from_vertices_3d.evaluate(**_vectors(self.NAMES, *vertices))
                self.assertTrue(math.isclose(result, 3.6742346141747673, rel_tol=1e-12))

    def test_degenerate_triangles_give_zero(self):
        collinear = _vectors(self.NAMES, (0, 0, 0), (1, 1, 1), (2, 2, 2))
        coincident = _vectors(self.NAMES, (1, 2, 3), (1, 2, 3), (1, 2, 3))
        self.assertEqual(triangle_area_from_vertices_3d.evaluate(**collinear), 0.0)
        self.assertEqual(triangle_area_from_vertices_3d.evaluate(**coincident), 0.0)


if __name__ == "__main__":
    unittest.main()

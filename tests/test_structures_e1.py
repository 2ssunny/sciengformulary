"""Tests for the E1 structures formulas (beam stiffness, fixed-end loads, bars, plates).

Every formula here is a derived result, so each class checks the closed form by a route that
does not call the evaluator: exact Fraction arithmetic on the integration or superposition
procedure of the source. Reference numbers for the plain cases come from the independent
oracle (exact rationals and sympy, with 50-digit mpmath).
"""

import math
import unittest
from fractions import Fraction

from sciengformulary.catalog.structures.beam_rotational_stiffness_far_end_fixed import (
    beam_rotational_stiffness_far_end_fixed,
)
from sciengformulary.catalog.structures.fixed_bar_axial_reaction_linear_load import (
    fixed_bar_axial_reaction_linear_load,
)
from sciengformulary.catalog.structures.fixed_bar_axial_reaction_point_load import (
    fixed_bar_axial_reaction_point_load,
)
from sciengformulary.catalog.structures.fixed_end_moment_applied_couple import (
    fixed_end_moment_applied_couple,
)
from sciengformulary.catalog.structures.fixed_end_moment_partial_linear_load import (
    fixed_end_moment_partial_linear_load,
)
from sciengformulary.catalog.structures.fixed_end_moment_point_load import (
    fixed_end_moment_point_load,
)
from sciengformulary.catalog.structures.fixed_end_reaction_point_load import (
    fixed_end_reaction_point_load,
)
from sciengformulary.catalog.structures.fixed_guided_beam_lateral_stiffness import (
    fixed_guided_beam_lateral_stiffness,
)
from sciengformulary.catalog.structures.plate_flexural_rigidity import plate_flexural_rigidity
from sciengformulary.core import FormulaSpec

REL = 1e-12
NAN = math.nan
INF = math.inf


def _solve_2x2(a11, a12, a21, a22, b1, b2):
    """Solve a 2x2 linear system exactly (Cramer's rule)."""
    det = a11 * a22 - a12 * a21
    return (b1 * a22 - a12 * b2) / det, (a11 * b2 - b1 * a21) / det


def _cantilever_fix_tip(P, a, L):
    """Tip force R and tip couple M that cancel the tip deflection and slope of a cantilever.

    Uses the cantilever curve for a point load P at x = a (E I = 1): tip deflection
    P a^2 (3 L - a) / 6 and tip slope P a^2 / 2. A tip force R (opposing P) and a tip couple M
    (positive when it reduces both) contribute R L^3 / 3 + M L^2 / 2 and R L^2 / 2 + M L.
    """
    deflection = P * a**2 * (3 * L - a) / 6
    slope = P * a**2 / 2
    return _solve_2x2(L**3 / 3, L**2 / 2, L**2 / 2, L, deflection, slope)


def _poly_derivative(coefficients):
    return [n * c for n, c in enumerate(coefficients)][1:] or [Fraction(0)]


def _poly_value(coefficients, x):
    return sum(c * x**n for n, c in enumerate(coefficients))


class _Base:
    formula: FormulaSpec

    def assert_close(self, actual, expected, rel=REL, abs_tol=0.0):
        self.assertTrue(
            math.isclose(actual, float(expected), rel_tol=rel, abs_tol=abs_tol),
            f"got {actual!r}, expected {float(expected)!r}",
        )

    def assert_cases(self, cases, rel=REL):
        for inputs, expected in cases:
            with self.subTest(**inputs):
                self.assert_close(self.formula.evaluate(**inputs), expected, rel, 1e-9)

    def assert_rejects(self, bad_inputs, base, error=ValueError):
        for name, value in bad_inputs:
            with self.subTest(**{name: value}):
                with self.assertRaises(error):
                    self.formula.evaluate(**{**base, name: value})


class BeamRotationalStiffnessTest(_Base, unittest.TestCase):
    formula = beam_rotational_stiffness_far_end_fixed
    base = {"E": 2.0e11, "I": 8.0e-6, "L": 4.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.beam_rotational_stiffness_far_end_fixed")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"E": 2.0e11, "I": 8.0e-6, "L": 4.0}, 1600000.0),
                ({"E": 7.0e10, "I": 1.2e-6, "L": 0.5}, 672000.0),
            ]
        )

    def test_domain_rules(self):
        bad = [(n, v) for n in self.base for v in (0.0, -1.0, NAN, INF)]
        self.assert_rejects(bad, self.base)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(E=1e300, I=1e300, L=1.0)

    def test_independent_route_cantilever_superposition(self):
        # Cantilever clamped at the far end; a tip force R and tip couple M give zero tip
        # deflection and a tip rotation theta (E I = 1): R L^3 / 3 + M L^2 / 2 = 0 and
        # R L^2 / 2 + M L = theta. M is the moment needed at the rotated end.
        for L in (Fraction(3, 2), Fraction(4), Fraction(1, 3)):
            with self.subTest(L=L):
                _, moment = _solve_2x2(L**3 / 3, L**2 / 2, L**2 / 2, L, 0, 1)
                got = self.formula.evaluate(E=1.0, I=1.0, L=float(L))
                self.assert_close(got, moment)

    def test_independent_route_assumed_curve(self):
        # v = theta x (1 - x / L)^2 meets v(0) = 0, v'(0) = theta, v(L) = 0, v'(L) = 0;
        # the moment at x = 0 has magnitude E I v''(0).
        L = Fraction(5, 2)
        theta = Fraction(1, 1)
        v = [0, theta, -2 * theta / L, theta / L**2]
        slope = _poly_derivative(v)
        curvature = _poly_derivative(slope)
        self.assertEqual(_poly_value(v, 0), 0)
        self.assertEqual(_poly_value(slope, 0), theta)
        self.assertEqual(_poly_value(v, L), 0)
        self.assertEqual(_poly_value(slope, L), 0)
        got = self.formula.evaluate(E=1.0, I=1.0, L=float(L)) * float(theta)
        self.assert_close(got, abs(_poly_value(curvature, 0)))
        # Carry-over: the far-end moment is half of the near-end moment.
        self.assertEqual(abs(_poly_value(curvature, L)) * 2, abs(_poly_value(curvature, 0)))


class FixedGuidedLateralStiffnessTest(_Base, unittest.TestCase):
    formula = fixed_guided_beam_lateral_stiffness
    base = {"E": 2.0e11, "I": 8.0e-6, "L": 4.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_guided_beam_lateral_stiffness")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"E": 2.0e11, "I": 8.0e-6, "L": 4.0}, 300000.0),
                ({"E": 7.0e10, "I": 1.2e-6, "L": 0.5}, 8064000.0),
            ]
        )

    def test_domain_rules(self):
        bad = [(n, v) for n in self.base for v in (0.0, -1.0, NAN, INF)]
        self.assert_rejects(bad, self.base)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(E=1e300, I=1e300, L=1.0)

    def test_independent_route_cantilever_superposition(self):
        # Tip force R and tip couple M on a cantilever (E I = 1) with zero tip slope and tip
        # deflection Delta = 1: R L^3 / 3 + M L^2 / 2 = 1 and R L^2 / 2 + M L = 0.
        for L in (Fraction(3, 2), Fraction(4), Fraction(1, 3)):
            with self.subTest(L=L):
                force, _ = _solve_2x2(L**3 / 3, L**2 / 2, L**2 / 2, L, 1, 0)
                self.assert_close(self.formula.evaluate(E=1.0, I=1.0, L=float(L)), force)

    def test_independent_route_assumed_curve(self):
        # v = Delta (3 x^2 / L^2 - 2 x^3 / L^3) meets v(0) = v'(0) = 0, v(L) = Delta, v'(L) = 0;
        # the shear force is E I v'''.
        L = Fraction(7, 3)
        v = [0, 0, 3 / L**2, -2 / L**3]
        slope = _poly_derivative(v)
        third = _poly_derivative(_poly_derivative(slope))
        self.assertEqual(_poly_value(v, 0), 0)
        self.assertEqual(_poly_value(slope, 0), 0)
        self.assertEqual(_poly_value(v, L), 1)
        self.assertEqual(_poly_value(slope, L), 0)
        self.assert_close(self.formula.evaluate(E=1.0, I=1.0, L=float(L)), abs(third[0]))


class _PointLoadBase(_Base):
    """Shared checks for the three point-load formulas on a beam fixed at both ends."""

    base = {"P": 10000.0, "a": 2.0, "L": 6.0}

    def test_domain_rules(self):
        bad = [
            ("L", 0.0),
            ("L", -6.0),
            ("L", NAN),
            ("L", INF),
            ("a", -0.1),
            ("a", 6.1),
            ("a", NAN),
            ("a", INF),
            ("P", NAN),
            ("P", INF),
        ]
        self.assert_rejects(bad, self.base)

    def test_boundary_inclusive(self):
        for a in (0.0, 6.0):
            with self.subTest(a=a):
                self.formula.evaluate(P=1.0, a=a, L=6.0)

    def test_extreme_magnitudes(self):
        # The result never exceeds the load in size, so huge inputs must not overflow.
        load_name = "M0" if "M0" in self.base else "P"
        value = self.formula.evaluate(**{**self.base, load_name: 1e308, "L": 1e150, "a": 4e149})
        self.assertTrue(math.isfinite(value))


class FixedEndReactionPointLoadTest(_PointLoadBase, unittest.TestCase):
    formula = fixed_end_reaction_point_load

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_end_reaction_point_load")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"P": 10000.0, "a": 2.0, "L": 6.0}, 7407.407407407408),
                ({"P": 10000.0, "a": 0.0, "L": 6.0}, 10000.0),
                ({"P": 10000.0, "a": 6.0, "L": 6.0}, 0.0),
                ({"P": 8000.0, "a": 2.0, "L": 4.0}, 4000.0),
            ]
        )

    def test_independent_route_superposition(self):
        # Far-end reaction from the cantilever superposition, then R_A = P - R_B.
        P, L = Fraction(10000), Fraction(6)
        for a in (Fraction(1, 2), Fraction(2), Fraction(9, 2), Fraction(6)):
            with self.subTest(a=a):
                far_reaction, _ = _cantilever_fix_tip(P, a, L)
                got = self.formula.evaluate(P=float(P), a=float(a), L=float(L))
                self.assert_close(got, P - far_reaction, abs_tol=1e-9)
        # Load at the near clamp: nothing to cancel at the far end, so the near end takes all.
        self.assert_close(self.formula.evaluate(P=1.0, a=0.0, L=3.0), 1)

    def test_reactions_sum_to_load(self):
        P, L = 10000.0, 6.0
        for a in (0.5, 2.0, 4.5):
            with self.subTest(a=a):
                near = self.formula.evaluate(P=P, a=a, L=L)
                far = self.formula.evaluate(P=P, a=L - a, L=L)  # mirror image
                self.assert_close(near + far, P)


class FixedEndMomentPointLoadTest(_PointLoadBase, unittest.TestCase):
    formula = fixed_end_moment_point_load

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_end_moment_point_load")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"P": 10000.0, "a": 2.0, "L": 6.0}, 8888.888888888889),
                ({"P": 10000.0, "a": 0.0, "L": 6.0}, 0.0),
                ({"P": 10000.0, "a": 6.0, "L": 6.0}, 0.0),
                ({"P": 8000.0, "a": 2.0, "L": 4.0}, 4000.0),
            ]
        )

    def test_independent_route_superposition(self):
        # The cantilever superposition gives the far-end moment P a^2 b / L^2 (the magnitude of
        # the fixing couple) and the far-end reaction R_B. Moment equilibrium about the near
        # end then gives the near-end moment, M_A = P a - R_B L - M_fix.
        P, L = Fraction(10000), Fraction(6)
        for a in (Fraction(1, 2), Fraction(2), Fraction(3), Fraction(9, 2), Fraction(11, 2)):
            with self.subTest(a=a):
                far_reaction, couple = _cantilever_fix_tip(P, a, L)
                near_moment = P * a - far_reaction * L - couple
                got = self.formula.evaluate(P=float(P), a=float(a), L=float(L))
                self.assert_close(got, near_moment)
                # Far-end moment is the same formula with a replaced by L - a.
                mirrored = self.formula.evaluate(P=float(P), a=float(L - a), L=float(L))
                self.assert_close(mirrored, -couple)

    def test_extreme_magnitudes(self):
        # Unlike the reactions, the moment grows with the span, so a huge product overflows.
        with self.assertRaises(OverflowError):
            self.formula.evaluate(P=1e308, a=10.0, L=20.0)

    def test_midspan_is_pl_over_eight(self):
        self.assert_close(self.formula.evaluate(P=3.0, a=1.5, L=3.0), Fraction(3 * 3, 8))


class FixedEndMomentAppliedCoupleTest(_PointLoadBase, unittest.TestCase):
    formula = fixed_end_moment_applied_couple
    base = {"M0": 5000.0, "a": 1.5, "L": 6.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_end_moment_applied_couple")

    def test_domain_rules(self):
        bad = [
            ("L", 0.0),
            ("L", -6.0),
            ("L", NAN),
            ("a", -0.1),
            ("a", 6.1),
            ("a", NAN),
            ("a", INF),
            ("M0", NAN),
            ("M0", INF),
        ]
        self.assert_rejects(bad, self.base)

    def test_boundary_inclusive(self):
        for a in (0.0, 6.0):
            with self.subTest(a=a):
                self.formula.evaluate(M0=1.0, a=a, L=6.0)

    def test_oracle_values_and_sign_convention(self):
        self.assert_cases(
            [
                ({"M0": 5000.0, "a": 1.5, "L": 6.0}, -937.5),
                ({"M0": 5000.0, "a": 2.0, "L": 6.0}, 0.0),
                ({"M0": 5000.0, "a": 0.0, "L": 6.0}, -5000.0),
                ({"M0": 5000.0, "a": 6.0, "L": 6.0}, 0.0),
                ({"M0": 5000.0, "a": 4.0, "L": 6.0}, Fraction(5000 * 2 * 6, 36)),
            ]
        )
        # Counterclockwise couple, counterclockwise clamp moment: the sign flips with M0, is
        # negative for a < L/3 and positive for a > L/3.
        evaluate = self.formula.evaluate
        self.assertLess(evaluate(M0=1.0, a=1.0, L=6.0), 0)
        self.assertGreater(evaluate(M0=1.0, a=3.0, L=6.0), 0)
        self.assertEqual(evaluate(M0=-2.0, a=1.0, L=6.0), -evaluate(M0=2.0, a=1.0, L=6.0))

    def test_independent_route_limit_of_two_point_loads(self):
        # A couple M0 is the limit of two opposite point loads a distance d apart. With the
        # counterclockwise near-end moment of a downward point load P a b^2 / L^2, the couple
        # result is -M0 d/da [a (L - a)^2 / L^2]. The derivative of this cubic is taken
        # exactly with a five-point stencil.
        L, M0 = Fraction(6), Fraction(5000)

        def per_unit_load(a):
            return a * (L - a) ** 2 / L**2

        h = Fraction(1, 64)
        for a in (Fraction(1, 2), Fraction(3, 2), Fraction(2), Fraction(5), Fraction(11, 2)):
            with self.subTest(a=a):
                derivative = (
                    -per_unit_load(a + 2 * h)
                    + 8 * per_unit_load(a + h)
                    - 8 * per_unit_load(a - h)
                    + per_unit_load(a - 2 * h)
                ) / (12 * h)
                got = self.formula.evaluate(M0=float(M0), a=float(a), L=float(L))
                self.assert_close(got, -M0 * derivative, abs_tol=1e-9)

    def test_independent_route_equilibrium_and_slope_conditions(self):
        # Closed-form check of the clamped-clamped solution: for a couple M0 at a, the near
        # reaction R_A = 6 M0 a b / L^3 and moment M_A together make the beam slope zero at the
        # far end. With E I = 1, the slope at L of M(x) = R_A x - M_A - M0 <x - a>^0 integrated
        # once and the deflection at L integrated twice must vanish:
        #   R_A L^2 / 2 - M_A L - M0 b = 0 and R_A L^3 / 6 - M_A L^2 / 2 - M0 b^2 / 2 = 0.
        L, M0 = Fraction(6), Fraction(5000)
        for a in (Fraction(1), Fraction(2), Fraction(7, 2), Fraction(5)):
            with self.subTest(a=a):
                b = L - a
                reaction, moment = _solve_2x2(
                    L**2 / 2, -L, L**3 / 6, -(L**2) / 2, M0 * b, M0 * b**2 / 2
                )
                self.assertEqual(reaction, 6 * M0 * a * b / L**3)
                got = self.formula.evaluate(M0=float(M0), a=float(a), L=float(L))
                self.assert_close(got, moment)


class FixedEndMomentPartialLinearLoadTest(_Base, unittest.TestCase):
    formula = fixed_end_moment_partial_linear_load
    base = {"w1": 1000.0, "w2": 2500.0, "x1": 1.0, "x2": 3.5, "L": 6.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_end_moment_partial_linear_load")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"w1": 2000.0, "w2": 2000.0, "x1": 0.0, "x2": 6.0, "L": 6.0}, 6000.0),
                ({"w1": 0.0, "w2": 3000.0, "x1": 0.0, "x2": 5.0, "L": 5.0}, 2500.0),
                ({"w1": 3000.0, "w2": 0.0, "x1": 0.0, "x2": 5.0, "L": 5.0}, 3750.0),
                (self.base, 3472.222222222222),
                ({"w1": 1000.0, "w2": 1000.0, "x1": 2.0, "x2": 2.0, "L": 6.0}, 0.0),
            ]
        )

    def test_domain_rules(self):
        bad = [
            ("L", 0.0),
            ("L", -6.0),
            ("L", NAN),
            ("x1", -0.5),
            ("x1", 3.6),  # x1 > x2
            ("x2", 0.5),  # x2 < x1
            ("x2", 6.5),  # x2 > L
            ("x1", NAN),
            ("x2", INF),
            ("w1", NAN),
            ("w2", INF),
        ]
        self.assert_rejects(bad, self.base)

    def test_boundary_inclusive(self):
        ends = {"w1": 1.0, "w2": 1.0, "x1": 0.0, "x2": 6.0, "L": 6.0}
        self.assert_close(self.formula.evaluate(**ends), Fraction(36, 12))
        self.assertEqual(self.formula.evaluate(w1=1.0, w2=5.0, x1=6.0, x2=6.0, L=6.0), 0.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(w1=1e308, w2=1e308, x1=0.0, x2=6.0, L=6.0)

    def test_independent_route_exact_integral_of_point_load_moment(self):
        # M_A = (1 / L^2) integral of w(s) s (L - s)^2 ds on [x1, x2]; the integrand is a
        # polynomial of degree 4, so Boole's five-point rule is exact (Fractions throughout).
        cases = [
            (1000, 2500, 1, Fraction(7, 2), 6),
            (1000, 2500, Fraction(59, 10), 6, 6),
            (-1500, 2000, Fraction(1, 10), Fraction(59, 10), 6),
            (7, 3, 2, Fraction(20000001, 10000000), 6),
            (500, 0, 3, 5, 8),
        ]
        for w1, w2, x1, x2, L in cases:
            with self.subTest(w1=w1, w2=w2, x1=x1, x2=x2, L=L):
                # The evaluator receives floats, so the exact integral uses those same values.
                w1, w2, x1, x2, L = (Fraction(float(Fraction(v))) for v in (w1, w2, x1, x2, L))
                h = (x2 - x1) / 4

                def integrand(s):
                    load = w1 + (w2 - w1) * (s - x1) / (x2 - x1)
                    return load * s * (L - s) ** 2

                nodes = [x1 + i * h for i in range(5)]
                weights = (7, 32, 12, 32, 7)
                exact = (2 * h / 45) * sum(w * integrand(s) for w, s in zip(weights, nodes))
                exact /= L**2
                got = self.formula.evaluate(
                    w1=float(w1), w2=float(w2), x1=float(x1), x2=float(x2), L=float(L)
                )
                self.assert_close(got, exact, rel=1e-12)

    def test_near_far_clamp_has_no_cancellation(self):
        # Loads next to the far clamp (x2 -> L). The values are 60-digit mpmath integrals of
        # w(s) s (L - s)^2 / L^2 for the float inputs, computed in the scratch script
        # fix_oracles/fem_oracle.py; an expanded polynomial loses most digits here.
        cases = [
            ((1.0, 1.0, 1 - 1e-6, 1.0, 1.0), 3.3333308336208895e-19),
            ((1.0, 1.0, 1 - 2e-6, 1 - 1e-6, 1.0), 2.3333295830905342e-18),
            ((1.0, 1.0, 1 - 1e-9, 1.0, 1.0), 3.333333048014027e-28),
            ((2.0, 3.0, 1 - 1e-8, 1.0, 1.0), 7.500000058057083e-25),
            ((1000.0, 500.0, 5.0 - 1e-5, 5.0, 5.0), 5.833324332670825e-14),
        ]
        for (w1, w2, x1, x2, L), expected in cases:
            with self.subTest(x1=x1, x2=x2):
                got = self.formula.evaluate(w1=w1, w2=w2, x1=x1, x2=x2, L=L)
                self.assertGreater(got, 0.0)
                self.assert_close(got, expected, rel=1e-14)

    def test_same_sign_load_never_gives_wrong_sign(self):
        # Every term of the quadrature is non-negative for a downward load, so the magnitude
        # stays positive however thin the loaded strip at the clamp is.
        for gap in (1e-3, 1e-6, 1e-9, 1e-12, 1e-15):
            with self.subTest(gap=gap):
                value = self.formula.evaluate(w1=1.0, w2=2.0, x1=1.0 - gap, x2=1.0, L=1.0)
                self.assertGreater(value, 0.0)

    def test_superposition_of_point_loads_limit(self):
        # A uniform load on [x1, x2] is a fine row of point loads; the exact Riemann sum of
        # the point-load moment P a b^2 / L^2 with the midpoint rule converges to the closed
        # form as the row is refined (error ~ 1/n^2).
        w, x1, x2, L = 1000.0, 1.0, 4.0, 6.0
        exact = self.formula.evaluate(w1=w, w2=w, x1=x1, x2=x2, L=L)
        for n, tolerance in ((50, 1e-3), (500, 1e-5)):
            step = (x2 - x1) / n
            total = 0.0
            for i in range(n):
                a = x1 + (i + 0.5) * step
                total += w * step * a * (L - a) ** 2 / L**2
            self.assertTrue(math.isclose(total, exact, rel_tol=tolerance))

    def test_special_case_limits(self):
        for L in (3.0, 7.5):
            w = 200.0
            uniform = self.formula.evaluate(w1=w, w2=w, x1=0.0, x2=L, L=L)
            rising = self.formula.evaluate(w1=0.0, w2=w, x1=0.0, x2=L, L=L)
            falling = self.formula.evaluate(w1=w, w2=0.0, x1=0.0, x2=L, L=L)
            self.assert_close(uniform, Fraction(w) * Fraction(L) ** 2 / 12)
            self.assert_close(rising, Fraction(w) * Fraction(L) ** 2 / 30)
            self.assert_close(falling, Fraction(w) * Fraction(L) ** 2 / 20)


class FixedBarAxialReactionPointLoadTest(_PointLoadBase, unittest.TestCase):
    formula = fixed_bar_axial_reaction_point_load

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_bar_axial_reaction_point_load")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"P": 9000.0, "a": 2.0, "L": 6.0}, 6000.0),
                ({"P": 9000.0, "a": 0.0, "L": 6.0}, 9000.0),
                ({"P": 9000.0, "a": 6.0, "L": 6.0}, 0.0),
            ]
        )

    def test_independent_route_compatibility_and_equilibrium(self):
        # Segment elongations must cancel (R_A a / A E = R_B b / A E) and the reactions sum
        # to P; solve the 2x2 system exactly (A E = 1) and compare.
        P, L = Fraction(9000), Fraction(6)
        for a in (Fraction(1, 2), Fraction(2), Fraction(3), Fraction(11, 2)):
            with self.subTest(a=a):
                b = L - a
                near, far = _solve_2x2(a, -b, 1, 1, 0, P)
                self.assertEqual(near + far, P)
                got = self.formula.evaluate(P=float(P), a=float(a), L=float(L))
                self.assert_close(got, near)


class FixedBarAxialReactionLinearLoadTest(_Base, unittest.TestCase):
    formula = fixed_bar_axial_reaction_linear_load
    base = {"p1": 400.0, "p2": 1200.0, "x1": 2.0, "x2": 4.0, "L": 6.0}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.fixed_bar_axial_reaction_linear_load")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"p1": 1000.0, "p2": 1000.0, "x1": 0.0, "x2": 6.0, "L": 6.0}, 3000.0),
                ({"p1": 0.0, "p2": 900.0, "x1": 0.0, "x2": 6.0, "L": 6.0}, 1800.0),
                (self.base, 844.4444444444445),
                ({"p1": 400.0, "p2": 400.0, "x1": 3.0, "x2": 3.0, "L": 6.0}, 0.0),
            ]
        )

    def test_domain_rules(self):
        bad = [
            ("L", 0.0),
            ("L", -6.0),
            ("L", NAN),
            ("x1", -0.5),
            ("x1", 4.5),
            ("x2", 1.0),
            ("x2", 6.5),
            ("x1", NAN),
            ("x2", INF),
            ("p1", NAN),
            ("p2", INF),
        ]
        self.assert_rejects(bad, self.base)

    def test_boundary_inclusive(self):
        self.assert_close(self.formula.evaluate(p1=1.0, p2=1.0, x1=0.0, x2=6.0, L=6.0), 3)
        self.assertEqual(self.formula.evaluate(p1=5.0, p2=5.0, x1=0.0, x2=0.0, L=6.0), 0.0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(p1=1e308, p2=1e308, x1=0.0, x2=1e10, L=1e10)

    def test_independent_route_integral_of_point_load_reaction(self):
        # R_B = (1 / L) integral of p(s) s ds on [x1, x2]; the integrand has degree 2, so
        # Simpson's rule is exact (Fractions throughout).
        cases = [
            (400, 1200, 2, 4, 6),
            (0, 900, 0, 6, 6),
            (-300, 800, Fraction(1, 2), Fraction(11, 2), 6),
            (50, 20, Fraction(3, 2), Fraction(5, 2), 10),
        ]
        for p1, p2, x1, x2, L in cases:
            with self.subTest(p1=p1, p2=p2, x1=x1, x2=x2, L=L):
                p1, p2, x1, x2, L = (Fraction(float(Fraction(v))) for v in (p1, p2, x1, x2, L))

                def integrand(s):
                    return (p1 + (p2 - p1) * (s - x1) / (x2 - x1)) * s

                mid = (x1 + x2) / 2
                exact = (x2 - x1) / 6 * (integrand(x1) + 4 * integrand(mid) + integrand(x2)) / L
                got = self.formula.evaluate(
                    p1=float(p1), p2=float(p2), x1=float(x1), x2=float(x2), L=float(L)
                )
                self.assert_close(got, exact)

    def test_matches_point_load_reaction_for_narrow_load(self):
        # A very narrow load of total resultant Q at position s acts like a point load Q.
        s, width, total, L = 2.5, 1e-6, 800.0, 6.0
        intensity = total / width
        got = self.formula.evaluate(
            p1=intensity, p2=intensity, x1=s - width / 2, x2=s + width / 2, L=L
        )
        point_far = total * s / L
        self.assertTrue(math.isclose(got, point_far, rel_tol=1e-9))


class PlateFlexuralRigidityTest(_Base, unittest.TestCase):
    formula = plate_flexural_rigidity
    base = {"E": 2.0e11, "t": 0.01, "nu": 0.3}

    def test_constructed(self):
        self.assertEqual(self.formula.id, "structures.plate_flexural_rigidity")

    def test_oracle_values(self):
        self.assert_cases(
            [
                ({"E": 2.0e11, "t": 0.01, "nu": 0.3}, 18315.018315018315),
                ({"E": 1.0e9, "t": 0.1, "nu": 0.0}, 83333.33333333333),
                ({"E": 5.0e6, "t": 0.02, "nu": -0.5}, 4.444444444444445),
            ]
        )

    def test_domain_rules(self):
        bad = [
            ("E", 0.0),
            ("E", -1.0),
            ("E", NAN),
            ("t", 0.0),
            ("t", -0.01),
            ("t", INF),
            ("nu", 0.5),
            ("nu", 0.6),
            ("nu", -1.0),
            ("nu", -1.5),
            ("nu", NAN),
            ("nu", INF),
        ]
        self.assert_rejects(bad, self.base)

    def test_boundary_values_just_inside(self):
        self.assertGreater(self.formula.evaluate(E=1.0, t=1.0, nu=0.4999999), 0)
        self.assertGreater(self.formula.evaluate(E=1.0, t=1.0, nu=-0.9999999), 0)

    def test_overflow_raises(self):
        with self.assertRaises(OverflowError):
            self.formula.evaluate(E=1e300, t=1e100, nu=0.0)

    def test_independent_route_laminate_bending_stiffness(self):
        # Eq. (24) of the source for one ply: D_b = (1/3) Q (z2^3 - z1^3) with z from -t/2 to
        # t/2 and the plane-stress entry Q = E / (1 - nu^2) of eq. (2). Exact Fractions.
        for E, t, nu in (
            (Fraction(200), Fraction(1, 10), Fraction(3, 10)),
            (Fraction(5), Fraction(1, 50), Fraction(-1, 2)),
            (Fraction(1), Fraction(2), Fraction(0)),
        ):
            with self.subTest(E=E, t=t, nu=nu):
                q11 = E / (1 - nu**2)
                bending = q11 * ((t / 2) ** 3 - (-t / 2) ** 3) / 3
                got = self.formula.evaluate(E=float(E), t=float(t), nu=float(nu))
                self.assert_close(got, bending)

    def test_additive_over_identical_plies(self):
        # Four plies of thickness t / 4 stacked through the thickness sum to the single plate.
        E, t, nu = Fraction(200), Fraction(1, 10), Fraction(3, 10)
        q11 = E / (1 - nu**2)
        edges = [-t / 2 + i * t / 4 for i in range(5)]
        total = sum(q11 * (edges[i + 1] ** 3 - edges[i] ** 3) / 3 for i in range(4))
        got = self.formula.evaluate(E=float(E), t=float(t), nu=float(nu))
        self.assert_close(got, total)


if __name__ == "__main__":
    unittest.main()

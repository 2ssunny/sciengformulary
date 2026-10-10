"""Pythagorean Theorem (Hypotenuse): c = sqrt(a^2 + b^2)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float) -> float:
    positive("a", a)
    positive("b", b)
    # math.hypot scales internally, so large legs do not overflow when squared.
    return finite_result(math.hypot(a, b))


pythagorean_hypotenuse = FormulaSpec(
    id="mathematics.pythagorean_hypotenuse",
    name="Pythagorean Theorem (Hypotenuse)",
    equation="c = sqrt(a^2 + b^2)",
    description=("Length of the hypotenuse of a right triangle from the lengths of its two legs."),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Length of one leg",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Length of the other leg",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="c",
        symbol="c",
        description="Length of the hypotenuse",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states, for points p1, p2, p3 of a Euclidean affine space, that
        # d(p1, p3)^2 = d(p1, p2)^2 + d(p3, p2)^2 if and only if the angle p1 p2 p3 is pi/2.
        # Derived step: with legs a = d(p1, p2) and b = d(p3, p2) and hypotenuse
        # c = d(p1, p3) >= 0, take the non-negative square root of c^2 = a^2 + b^2. Mathlib's
        # angle is pi/2 by convention when p1 = p2 or p3 = p2; both legs are required to be
        # positive here, so the triangle is genuine.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/RightAngle.lean#L327",
            "theorem EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two",
        ),
        # Selinger applies the theorem to a right triangle with legs |p1 - q1| and |p2 - q2| to
        # get the distance as the square root of the sum of squares. Secondary: the theorem is
        # used there, not proved.
        selinger_linear_algebra(
            "sec. 2.5, definition of the distance between points "
            "(source label def:distance-between-points)"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 3, "b": 4},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="3-4-5 triple: 5.",
        ),
        VerificationCase(
            inputs={"a": 5, "b": 12},
            expected=13.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="5-12-13 triple: 13.",
        ),
        VerificationCase(
            inputs={"a": 1, "b": 1},
            expected=1.4142135623730951,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Isosceles right triangle: sqrt(2), mpmath.",
        ),
        VerificationCase(
            inputs={"a": 1.5, "b": 2},
            expected=2.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact squared hypotenuse 25/4: 2.5.",
        ),
        VerificationCase(
            inputs={"a": 3e200, "b": 4e200},
            expected=5e200,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Huge legs: 5e200; naive a*a overflows to inf.",
        ),
        VerificationCase(
            inputs={"a": 1, "b": 1e-08},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Closest valid edge (very thin triangle): sqrt(1 + 1e-16) rounds to 1.0.",
        ),
    ),
    assumptions=(
        "Plane right triangle with the right angle between legs a and b.",
        "Non-degenerate triangle: a > 0 and b > 0; a zero or negative leg raises ValueError.",
        "Both legs in one length unit; the hypotenuse is in the same unit.",
        "Derived result: the cited theorem states c^2 = a^2 + b^2 for the hypotenuse c; the "
        "formula solves it for c >= 0 with the square root. The solving step was checked "
        "numerically against the coordinate distance between (a, 0) and (0, b).",
        "A hypotenuse outside the floating-point range raises OverflowError.",
    ),
    tags=("Pythagorean theorem", "right triangle", "hypotenuse", "geometry", "trigonometry"),
)

"""Law of Cosines (Third Side): c = sqrt(a^2 + b^2 - 2*a*b*cos(gamma))."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, gamma: float) -> float:
    positive("a", a)
    positive("b", b)
    if not 0 < finite("gamma", gamma) < math.pi:
        raise ValueError(f"gamma must lie strictly between 0 and pi radians, got {gamma!r}.")
    # Same value as a^2 + b^2 - 2ab cos(gamma), written as (a - b)^2 + 4ab sin^2(gamma/2) so
    # that small angles do not lose accuracy to cancellation.
    half_sine = math.sin(gamma / 2.0)
    return math.sqrt((a - b) ** 2 + 4.0 * a * b * half_sine * half_sine)


law_of_cosines_side = FormulaSpec(
    id="mathematics.law_of_cosines_side",
    name="Law of Cosines (Third Side)",
    equation="c = sqrt(a^2 + b^2 - 2*a*b*cos(gamma))",
    description=(
        "Length of the side of a triangle opposite the angle gamma, from the two sides a and b "
        "that enclose that angle."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="One side adjacent to the angle gamma",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Other side adjacent to the angle gamma",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Included angle between sides a and b, at their common vertex, in radians",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="c",
        symbol="c",
        description="Side opposite the angle gamma",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: dist(p1,p3)^2 = dist(p1,p2)^2 + dist(p3,p2)^2
        #   - 2 dist(p1,p2) dist(p3,p2) cos(angle p1 p2 p3).
        # With a = dist(p1,p2), b = dist(p3,p2), gamma = angle at p2 and c = dist(p1,p3) this is
        # c^2 = a^2 + b^2 - 2ab cos(gamma); c >= 0 gives the square root.
        mathlib(
            "Mathlib/Geometry/Euclidean/Triangle.lean#L239",
            "theorem EuclideanGeometry"
            ".dist_sq_eq_dist_sq_add_dist_sq_sub_two_mul_dist_mul_dist_mul_cos_angle",
        ),
        # Fixes the angle convention: unoriented angle at the middle point, in [0, pi] radians.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/Affine.lean#L41",
            "def EuclideanGeometry.angle",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 3.0, "b": 4.0, "gamma": 1.5707963267948966},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "3-4-5 right triangle at gamma = float(pi/2): mpmath 50-digit value "
                "4.9999999999999998530..., matched by the distance between constructed "
                "vertices."
            ),
        ),
        VerificationCase(
            inputs={"a": 1.0, "b": 1.0, "gamma": 1.0471975511965976},
            expected=0.9999999999999999,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Equilateral case at gamma = float(pi/3): mpmath 50-digit value "
                "0.99999999999999990054..., matched by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"a": 2.0, "b": 3.0, "gamma": 3.0},
            expected=4.9879765395604405,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Obtuse angle near pi: mpmath 50-digit value 4.98797653956044038..., matched "
                "by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"a": 1.0, "b": 1.0, "gamma": 0.01},
            expected=0.009999958333385416,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Small angle with equal sides, c = 2 sin(0.005): mpmath 50-digit value "
                "0.0099999583333854168..., matched by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"a": 5.0, "b": 3.0, "gamma": 0.001},
            expected=2.000003749996172,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Small angle with unequal sides (c just above |a - b|): mpmath 50-digit value "
                "2.00000374999617188..., matched by a coordinate construction."
            ),
        ),
    ),
    assumptions=(
        "Non-degenerate plane (Euclidean) triangle: a > 0, b > 0 and 0 < gamma < pi; "
        "degenerate inputs raise ValueError.",
        "gamma is the interior, unoriented angle between a and b at their shared vertex, in "
        "radians. Because the float math.pi is slightly below the real pi, math.pi itself is "
        "rejected.",
        "a and b share one length unit; c is returned in that unit.",
        "gamma = pi/2 reduces to the Pythagorean theorem.",
    ),
    tags=("law of cosines", "cosine rule", "triangle", "trigonometry", "geometry"),
)

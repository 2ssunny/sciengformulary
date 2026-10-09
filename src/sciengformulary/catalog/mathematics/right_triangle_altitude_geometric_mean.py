"""Altitude to the Hypotenuse (Geometric Mean Theorem): h = sqrt(p * q)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p: float, q: float) -> float:
    positive("p", p)
    positive("q", q)
    product = p * q
    if 1e-290 < product < 1e290:
        return math.sqrt(product)
    # For extreme magnitudes the product could overflow or lose precision to underflow, so
    # take the roots separately.
    return finite_result(math.sqrt(p) * math.sqrt(q))


right_triangle_altitude_geometric_mean = FormulaSpec(
    id="mathematics.right_triangle_altitude_geometric_mean",
    name="Altitude to the Hypotenuse (Geometric Mean Theorem)",
    equation="h = sqrt(p * q)",
    description=(
        "Altitude from the right-angle vertex to the hypotenuse of a right triangle, as the "
        "geometric mean of the two segments into which its foot divides the hypotenuse."
    ),
    inputs=(
        VariableSpec(
            name="p",
            symbol="p",
            description="Length of one hypotenuse segment (from a vertex to the altitude foot)",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="q",
            symbol="q",
            description="Length of the other hypotenuse segment",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="h",
        symbol="h",
        description="Altitude from the right-angle vertex to the hypotenuse",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: if p4 lies strictly between p1 and p3, the angle p1 p4 p2 is pi/2 (p4 is the
        # foot of the altitude from p2) and the angle p1 p2 p3 is pi/2, then
        # d(p2, p4)^2 = d(p1, p4) * d(p3, p4). Derived step: with h = d(p2, p4) >= 0,
        # p = d(p1, p4) and q = d(p3, p4), take the non-negative square root of h^2 = p * q.
        # Strict betweenness gives p > 0 and q > 0, which the evaluator enforces.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/RightAngle.lean#L505",
            "theorem EuclideanGeometry.dist_sq_eq_dist_mul_dist_of_angle_eq_pi_div_two",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p": 1, "q": 4},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "sqrt(4) = 2; construction check: apex (0, 2) over (-1,0)-(4,0) has a right "
                "angle exactly."
            ),
        ),
        VerificationCase(
            inputs={"p": 9, "q": 16},
            expected=12.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="3-4-5 triangle scaled by 5 (legs 15, 20, hypotenuse 25): altitude 12.",
        ),
        VerificationCase(
            inputs={"p": 2, "q": 3},
            expected=2.449489742783178,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="sqrt(6), mpmath 50 digits.",
        ),
        VerificationCase(
            inputs={"p": 0.25, "q": 0.36},
            expected=0.3,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact product 9/100: 0.3.",
        ),
        VerificationCase(
            inputs={"p": 1e-06, "q": 1000000.0},
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Very lopsided (closest valid edge to a degenerate foot): exact product 1, h = 1."
            ),
        ),
    ),
    assumptions=(
        "Plane right triangle; the altitude is dropped from the right-angle vertex, so its "
        "foot lies strictly inside the hypotenuse.",
        "p > 0 and q > 0 (strict betweenness); a zero or negative segment raises ValueError.",
        "p and q in one length unit; the hypotenuse is p + q and h is in the same unit.",
        "Derived result: the cited theorem states h^2 = p * q; the formula solves it for "
        "h >= 0 with the square root. The solving step was checked numerically with a "
        "coordinate construction in which the apex angle is exactly right.",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("geometric mean theorem", "right triangle", "altitude", "hypotenuse", "geometry"),
)

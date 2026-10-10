"""Triangle Median Length: m_a = sqrt(2*b^2 + 2*c^2 - a^2) / 2."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, c: float) -> float:
    positive("a", a)
    positive("b", b)
    positive("c", c)
    if not (a < b + c and b < a + c and c < a + b):
        raise ValueError(
            f"Sides {a!r}, {b!r}, {c!r} violate the strict triangle inequality "
            "(each side must be shorter than the sum of the other two)."
        )
    return finite_result(math.sqrt(2.0 * b * b + 2.0 * c * c - a * a) / 2.0)


triangle_median_length = FormulaSpec(
    id="mathematics.triangle_median_length",
    name="Triangle Median Length",
    equation="m_a = sqrt(2*b^2 + 2*c^2 - a^2) / 2",
    description=(
        "Length of the median from a triangle's vertex to the midpoint of the opposite side a, "
        "from the three side lengths (Apollonius's theorem)."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Side opposite the vertex; the median ends at its midpoint",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="One side meeting at the vertex",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Other side meeting at the vertex",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="m_a",
        symbol="m_a",
        description="Median from the vertex opposite side a to the midpoint of a",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib (points a b c, any position): d(a,b)^2 + d(a,c)^2
        #   = 2 (d(a, midpoint b c)^2 + (d(b,c)/2)^2).
        # Our side a is d(b,c), sides b and c are d(a,c) and d(a,b), and m_a = d(a, midpoint b c),
        # so b^2 + c^2 = 2 m_a^2 + a^2/2, i.e. m_a = sqrt(2b^2 + 2c^2 - a^2) / 2.
        mathlib(
            "Mathlib/Geometry/Euclidean/Triangle.lean#L390",
            "theorem EuclideanGeometry"
            ".dist_sq_add_dist_sq_eq_two_mul_dist_midpoint_sq_add_half_dist_sq",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 5.0, "b": 3.0, "c": 4.0},
            expected=2.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "3-4-5 triangle, median to the hypotenuse: exact radicand 25, so m_a = 2.5; "
                "matched by the vertex-to-midpoint distance of a constructed triangle."
            ),
        ),
        VerificationCase(
            inputs={"a": 2.0, "b": 2.0, "c": 2.0},
            expected=1.7320508075688772,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Equilateral side 2: exact radicand 12, m_a = sqrt(3) to 50 digits; matched by a "
                "coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"a": 1.9375, "b": 1.0, "c": 1.0},
            expected=0.24803918541230538,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Near-flat triangle: exact radicand 63/256, mpmath 50-digit value "
                "0.24803918541230536785...; matched by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"a": 0.5, "b": 3.0, "c": 3.25},
            expected=3.1174909783349816,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Short base: exact radicand 311/8, mpmath 50-digit value "
                "3.11749097833498148521...; matched by a coordinate construction."
            ),
        ),
    ),
    assumptions=(
        "Plane triangle with positive sides satisfying the strict triangle inequality; "
        "degenerate triangles and impossible side sets raise ValueError.",
        "b and c are the sides that meet at the vertex the median starts from; the formula is "
        "symmetric in b and c.",
        "All sides in one length unit; m_a is returned in that unit.",
    ),
    tags=("median", "Apollonius", "triangle", "geometry"),
)

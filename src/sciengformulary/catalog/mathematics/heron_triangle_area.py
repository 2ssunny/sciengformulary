"""Heron's Formula (Triangle Area): A = sqrt(s*(s - a)*(s - b)*(s - c)), s = (a + b + c)/2."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import finite_result, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, c: float) -> float:
    positive("a", a)
    positive("b", b)
    positive("c", c)
    # Kahan's arrangement of the same radicand: with x >= y >= z,
    # 16 A^2 = (x + (y + z)) (z - (x - y)) (z + (x - y)) (x + (y - z)), which stays accurate
    # for needle-shaped triangles. Once sorted, the strict triangle inequality reduces to
    # z > x - y, which is also the factor that would otherwise vanish or go negative.
    x, y, z = sorted((a, b, c), reverse=True)
    if not z - (x - y) > 0:
        raise ValueError(
            f"Sides {a!r}, {b!r}, {c!r} violate the strict triangle inequality "
            "(each side must be shorter than the sum of the other two)."
        )
    return finite_result(
        math.sqrt((x + (y + z)) * (z - (x - y)) * (z + (x - y)) * (x + (y - z))) / 4.0
    )


heron_triangle_area = FormulaSpec(
    id="mathematics.heron_triangle_area",
    name="Heron's Formula (Triangle Area)",
    equation="A = sqrt(s*(s - a)*(s - b)*(s - c)), s = (a + b + c)/2",
    description="Area of a triangle from its three side lengths, through the semiperimeter s.",
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="First side length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Second side length",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Third side length",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="A",
        symbol="A",
        description="Triangle area",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib Archive (100 theorems list): (1/2) a b sin(angle) = sqrt(s(s-a)(s-b)(s-c)),
        # where the left side is the triangle area (two sides times the sine of the included
        # angle, halved). The Heron expression is symmetric, so the side labels are free.
        mathlib("Archive/Wiedijk100Theorems/HeronsFormula.lean#L35", "theorem Theorems100.heron"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 3.0, "b": 4.0, "c": 5.0},
            expected=6.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact radicand 6*3*2*1 = 36, so A = 6; matched by the shoelace area of the "
                "constructed triangle."
            ),
        ),
        VerificationCase(
            inputs={"a": 2.0, "b": 2.0, "c": 2.0},
            expected=1.7320508075688772,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Equilateral side 2: exact radicand 3, mpmath 50-digit sqrt(3); matched by the "
                "shoelace area."
            ),
        ),
        VerificationCase(
            inputs={"a": 1.0, "b": 1.0, "c": 1.9375},
            expected=0.24028796086817084,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Near-flat triangle: exact radicand 60543/1048576, mpmath 50-digit square root "
                "0.24028796086817082511...; matched by the shoelace area."
            ),
        ),
        VerificationCase(
            inputs={"a": 7.0, "b": 8.0, "c": 9.0},
            expected=26.832815729997478,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Scalene 7-8-9: s = 12, exact radicand 720, mpmath 50-digit 12 sqrt(5); matched "
                "by the shoelace area."
            ),
        ),
    ),
    assumptions=(
        "Plane triangle with positive sides satisfying the strict triangle inequality (each "
        "side shorter than the sum of the other two); degenerate (flat) triangles and "
        "impossible side sets raise ValueError.",
        "All sides in one length unit; the area is in that unit squared.",
        "Evaluated in Kahan's rearranged form of the same radicand, which keeps nearly flat "
        "triangles accurate.",
    ),
    tags=("Heron", "triangle area", "semiperimeter", "geometry"),
)

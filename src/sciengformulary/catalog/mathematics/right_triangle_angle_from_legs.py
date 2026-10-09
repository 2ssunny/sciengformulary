"""Acute Angle of a Right Triangle from Its Legs: theta = arctan(opposite / adjacent)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(opposite: float, adjacent: float) -> float:
    positive("opposite", opposite)
    positive("adjacent", adjacent)
    # atan2 equals atan(opposite / adjacent) for positive legs and does not form the quotient,
    # so it cannot overflow.
    return math.atan2(opposite, adjacent)


right_triangle_angle_from_legs = FormulaSpec(
    id="mathematics.right_triangle_angle_from_legs",
    name="Acute Angle of a Right Triangle from Its Legs",
    equation="theta = arctan(opposite / adjacent)",
    description=(
        "Acute angle at one vertex of a right triangle from the leg opposite it and the leg "
        "adjacent to it, in radians."
    ),
    inputs=(
        VariableSpec(
            name="opposite",
            symbol="a",
            description="Length of the leg opposite the angle",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="adjacent",
            symbol="b",
            description="Length of the leg adjacent to the angle (not the hypotenuse)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="theta",
        symbol=r"\theta",
        description="Acute angle at the vertex, in radians",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib: if the angle p1 p2 p3 is pi/2 and p3 != p2, the angle at p3 (angle p2 p3 p1)
        # equals arctan (dist p1 p2 / dist p3 p2). At p3 the opposite leg is d(p1, p2) and the
        # adjacent leg is d(p3, p2) > 0, so only the symbols are renamed. The sibling theorems
        # for arccos (adjacent / hypotenuse) and arcsin (opposite / hypotenuse) give the same
        # value.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/RightAngle.lean#L363",
            "theorem EuclideanGeometry.angle_eq_arctan_of_angle_eq_pi_div_two",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"opposite": 1, "adjacent": 1},
            expected=0.7853981633974483,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="pi/4 (mpmath).",
        ),
        VerificationCase(
            inputs={"opposite": 3, "adjacent": 4},
            expected=0.6435011087932844,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="atan(3/4); arccos(4/5) and arcsin(3/5) agree to 1e-25 (mpmath).",
        ),
        VerificationCase(
            inputs={"opposite": 2.5, "adjacent": 0.5},
            expected=1.373400766945016,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="atan(5), mpmath.",
        ),
        VerificationCase(
            inputs={"opposite": 1e-09, "adjacent": 1},
            expected=1e-09,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Near the lower edge: atan(1e-9) = 1e-9 to 18 digits.",
        ),
        VerificationCase(
            inputs={"opposite": 1, "adjacent": 1e-09},
            expected=1.5707963257948967,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Near the upper edge: pi/2 - 1e-9 (mpmath).",
        ),
    ),
    assumptions=(
        "Plane right triangle; theta is one of the two acute angles.",
        "Both legs are strictly positive; a zero or negative leg raises ValueError (a zero "
        "opposite leg is a degenerate triangle, although the cited statement needs only a "
        "non-zero adjacent leg).",
        "Both legs in one length unit; theta does not depend on the unit.",
        "The angle lies strictly between 0 and pi/2 mathematically; for a leg ratio below about "
        "5e-324 the float result underflows to 0, and above about 1e16 it rounds to the float "
        "nearest pi/2.",
    ),
    tags=("right triangle", "arctangent", "angle", "trigonometry", "legs"),
)

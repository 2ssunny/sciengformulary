"""Distance Between Two Points in 2-D: d = sqrt((x2 - x1)^2 + (y2 - y1)^2)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x1: float, y1: float, x2: float, y2: float) -> float:
    for name, value in (("x1", x1), ("y1", y1), ("x2", x2), ("y2", y2)):
        finite(name, value)
    # math.hypot scales internally, so large or tiny differences do not overflow or underflow
    # when squared. A difference that itself leaves the float range gives inf, which is
    # reported as OverflowError.
    return finite_result(math.hypot(x2 - x1, y2 - y1))


def _coordinate(axis: str, point: int, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{axis}{point}",
        symbol=f"{axis}_{point}",
        description=f"{axis} coordinate of the {which} point",
        dimension="L",
        si_unit="m",
    )


distance_between_points_2d = FormulaSpec(
    id="mathematics.distance_between_points_2d",
    name="Distance Between Two Points in 2-D",
    equation="d = sqrt((x2 - x1)^2 + (y2 - y1)^2)",
    description=(
        "Straight-line (Euclidean) distance between two points in the plane given by their "
        "Cartesian coordinates."
    ),
    inputs=(
        _coordinate("x", 1, "first"),
        _coordinate("y", 1, "first"),
        _coordinate("x", 2, "second"),
        _coordinate("y", 2, "second"),
    ),
    output=VariableSpec(
        name="d",
        symbol="d",
        description="Euclidean distance between the two points",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger defines the distance between points of R^n as the square root of the sum
        # of the squared coordinate differences and draws the planar case as the hypotenuse
        # of a right triangle. Here n = 2 is written out and the points are renamed
        # (p1, p2) -> (x1, y1) and (q1, q2) -> (x2, y2); the squares do not depend on the
        # sign of the differences.
        selinger_linear_algebra(
            "sec. 2.5, definition of the distance between points "
            "(source label def:distance-between-points)"
        ),
        # Mathlib: dist x y = sqrt (sum_i dist (x i) (y i) ^ 2) in Euclidean space over a
        # finite index type; secondary support (index type Fin 2).
        mathlib(
            "Mathlib/Analysis/InnerProductSpace/PiL2.lean#L178", "theorem EuclideanSpace.dist_eq"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x1": 0, "y1": 0, "x2": 3, "y2": 4},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="3-4-5 triangle: exactly 5.",
        ),
        VerificationCase(
            inputs={"x1": 1, "y1": 2, "x2": -2, "y2": -2},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Negative differences (-3, -4): exactly 5.",
        ),
        VerificationCase(
            inputs={"x1": -1.5, "y1": 2.25, "x2": 3.0, "y2": -0.75},
            expected=5.408326913195984,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=("Exact squared distance 117/4; mpmath 50-digit square root; math.hypot agrees."),
        ),
        VerificationCase(
            inputs={"x1": 1e200, "y1": 0, "x2": 4e200, "y2": 4e200},
            expected=5e200,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Differences (3e200, 4e200): 5e200. Guards against naive squaring, which "
                "overflows to inf."
            ),
        ),
        VerificationCase(
            inputs={"x1": 2.5, "y1": -1, "x2": 2.5, "y2": -1},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Coincident points: distance 0.",
        ),
    ),
    assumptions=(
        "Cartesian coordinates in an orthonormal frame, all in one length unit.",
        "Flat (Euclidean) plane: this is not a geodesic or great-circle distance.",
        "Coincident points give a distance of 0.",
        "Coordinate differences that leave the floating-point range (for example points near "
        "+1.7e308 and -1.7e308) raise OverflowError.",
    ),
    tags=("distance formula", "Euclidean distance", "2D", "coordinate geometry", "points"),
)

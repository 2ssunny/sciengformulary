"""Distance Between Two Points in 3-D: d = sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    values = (("x1", x1), ("y1", y1), ("z1", z1), ("x2", x2), ("y2", y2), ("z2", z2))
    for name, value in values:
        finite(name, value)
    # math.dist scales internally, so large or tiny coordinates do not overflow when squared.
    return math.dist((x1, y1, z1), (x2, y2, z2))


def _coordinate(axis: str, point: int, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{axis}{point}",
        symbol=f"{axis}_{point}",
        description=f"{axis} coordinate of the {which} point",
        dimension="L",
        si_unit="m",
    )


distance_between_points_3d = FormulaSpec(
    id="mathematics.distance_between_points_3d",
    name="Distance Between Two Points in 3-D",
    equation="d = sqrt((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)",
    description=(
        "Straight-line (Euclidean) distance between two points in three-dimensional space "
        "given by their Cartesian coordinates."
    ),
    inputs=(
        _coordinate("x", 1, "first"),
        _coordinate("y", 1, "first"),
        _coordinate("z", 1, "first"),
        _coordinate("x", 2, "second"),
        _coordinate("y", 2, "second"),
        _coordinate("z", 2, "second"),
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
        # Selinger writes the points as P = (p1, p2, p3) and Q = (q1, q2, q3) and states the
        # general R^n definition; here n = 3 and p, q -> (x1, y1, z1), (x2, y2, z2).
        selinger_linear_algebra(
            "sec. 2.5, definition of the distance between points "
            "(source label def:distance-between-points)"
        ),
        # Mathlib: dist x y = sqrt(sum_i dist(x i, y i)^2); for real coordinates
        # dist(a, b) = |a - b|, so each term is the squared coordinate difference.
        mathlib(
            "Mathlib/Analysis/InnerProductSpace/PiL2.lean#L178", "theorem EuclideanSpace.dist_eq"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x1": 0, "y1": 0, "z1": 0, "x2": 1, "y2": -3, "z2": 4},
            expected=5.0990195135927845,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.5 example: the vector (1, -3, 4) has length sqrt(26), its "
                "distance from the origin; sqrt(26) to 50 digits with mpmath."
            ),
        ),
        VerificationCase(
            inputs={"x1": 1, "y1": 2, "z1": 3, "x2": 4, "y2": 6, "z2": 3},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation: differences (3, 4, 0), squared sum 25, distance 5.",
        ),
        VerificationCase(
            inputs={"x1": -1.5, "y1": 2.25, "z1": 0.5, "x2": 3.0, "y2": -0.75, "z2": -2.5},
            expected=6.18465843842649,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact squared distance 153/4 by fraction arithmetic, square root to 50 digits "
                "with mpmath."
            ),
        ),
        VerificationCase(
            inputs={"x1": 2.5, "y1": -1, "z1": 7, "x2": 2.5, "y2": -1, "z2": 7},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Coincident points: distance 0 by inspection.",
        ),
    ),
    assumptions=(
        "Cartesian coordinates in an orthonormal frame, all six in the same length unit.",
        "Flat Euclidean space: this is not a great-circle or other geodesic distance.",
        "Coincident points give 0; the result is never negative.",
    ),
    tags=("distance formula", "Euclidean distance", "3D", "coordinate geometry", "points"),
)

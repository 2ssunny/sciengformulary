"""Distance from a Point to a Plane: D = |a*x0 + b*y0 + c*z0 - d| / sqrt(a^2 + b^2 + c^2)."""

import math

from sciengformulary.catalog._sources import selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, c: float, d: float, x0: float, y0: float, z0: float) -> float:
    values = (("a", a), ("b", b), ("c", c), ("d", d), ("x0", x0), ("y0", y0), ("z0", z0))
    for name, value in values:
        finite(name, value)
    if a == b == c == 0:
        raise ValueError(
            "The normal (a, b, c) must be non-zero; with a = b = c = 0 the equation does not "
            "describe a plane."
        )
    return finite_result(abs(a * x0 + b * y0 + c * z0 - d) / math.hypot(a, b, c))


def _normal(name: str, axis: str, extra: str = "") -> VariableSpec:
    return VariableSpec(
        name=name,
        symbol=name,
        description=f"{axis} component of the plane normal{extra}",
        dimension="1",
        si_unit="-",
    )


def _point(name: str, axis: str) -> VariableSpec:
    return VariableSpec(
        name=name,
        symbol=f"{name[0]}_0",
        description=f"{axis} coordinate of the point",
        dimension="L",
        si_unit="m",
    )


distance_point_to_plane = FormulaSpec(
    id="mathematics.distance_point_to_plane",
    name="Distance from a Point to a Plane",
    equation="D = |a*x0 + b*y0 + c*z0 - d| / sqrt(a^2 + b^2 + c^2)",
    description=(
        "Shortest (perpendicular) distance from the point (x0, y0, z0) to the plane "
        "a*x + b*y + c*z = d in three-dimensional space. The normal (a, b, c) does not have to "
        "be a unit vector."
    ),
    inputs=(
        _normal("a", "x", " in a*x + b*y + c*z = d"),
        _normal("b", "y"),
        _normal("c", "z"),
        VariableSpec(
            name="d",
            symbol="d",
            description="Constant term of the plane equation a*x + b*y + c*z = d",
            dimension="L",
            si_unit="m",
        ),
        _point("x0", "x"),
        _point("y0", "y"),
        _point("z0", "z"),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Shortest distance from the point to the plane",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source gives a procedure, not this closed form: pick any point R on the plane;
        # the distance is the length of the projection of R->P onto the normal n. With
        # n = (a, b, c) and n . r = d this length is |n . p - d| / |n| for every R on the
        # plane, which is the equation above (our derivation, checked symbolically).
        selinger_linear_algebra(
            "sec. 3.2, worked example on the shortest distance to a plane "
            "(source label exa:shortest-distance-plane)"
        ),
        # Fixes the form a*x + b*y + c*z = d with a non-zero normal. Selinger's (x_0, y_0, z_0)
        # is a point ON the plane; here x0, y0, z0 is the query point.
        selinger_linear_algebra(
            "sec. 3.2, definition of the standard equation of a plane "
            "(source label def:standard-equation-plane)"
        ),
        # proj_u(v) = (u . v / |u|^2) u, used in the derivation above.
        selinger_linear_algebra(
            "sec. 2.6, definition of the projection (source label def:projection)"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 2, "b": 1, "c": 2, "d": 2, "x0": 3, "y0": 2, "z0": 3},
            expected=4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example in Selinger sec. 3.2 (shortest distance to a plane), value 4; "
                "the projection procedure and the closed form both give squared distance 16 "
                "exactly, and a scipy minimisation agrees."
            ),
        ),
        VerificationCase(
            inputs={"a": 1, "b": 3, "c": -2, "d": 7, "x0": 1, "y0": 1, "z0": 1},
            expected=1.3363062095621219,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Plane x + 3y - 2z = 7 and point (1, 1, 1): exact squared distance 25/14, "
                "square root to 50 digits with mpmath; a scipy minimisation agrees."
            ),
        ),
        VerificationCase(
            inputs={"a": -2, "b": -1, "c": -2, "d": -2, "x0": 3, "y0": 2, "z0": 3},
            expected=4.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Textbook plane with every coefficient negated describes the same plane: "
                "distance still 4."
            ),
        ),
        VerificationCase(
            inputs={"a": 5, "b": -1, "c": 4, "d": 11, "x0": 2, "y0": -1, "z0": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "The point lies on the plane 5x - y + 4z = 11 (10 + 1 + 0 = 11 by hand), so the "
                "distance is 0."
            ),
        ),
    ),
    assumptions=(
        "Plane given as a*x + b*y + c*z = d with a non-zero normal (a, b, c); a = b = c = 0 "
        "raises ValueError. Scaling a, b, c and d by the same non-zero factor describes the "
        "same plane and gives the same distance.",
        "Cartesian coordinates in an orthonormal frame; x0, y0, z0 and d share one length unit "
        "when (a, b, c) is dimensionless.",
        "Unsigned distance: which side of the plane the point lies on is not reported.",
        "The closed form is derived here from the cited projection procedure (checked "
        "symbolically); the cited text works the procedure rather than printing this formula.",
    ),
    tags=(
        "point to plane distance",
        "plane",
        "normal vector",
        "projection",
        "3D",
        "analytic geometry",
    ),
)

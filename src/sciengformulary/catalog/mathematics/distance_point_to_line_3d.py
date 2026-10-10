"""Distance from a Point to a Line in 3-D: D = |(P0 - P1) x d| / |d|."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    x0: float,
    y0: float,
    z0: float,
    x1: float,
    y1: float,
    z1: float,
    dx: float,
    dy: float,
    dz: float,
) -> float:
    values = (
        ("x0", x0),
        ("y0", y0),
        ("z0", z0),
        ("x1", x1),
        ("y1", y1),
        ("z1", z1),
        ("dx", dx),
        ("dy", dy),
        ("dz", dz),
    )
    for name, value in values:
        finite(name, value)
    if dx == dy == dz == 0:
        raise ValueError(
            "The direction (dx, dy, dz) must be non-zero; with a zero direction there is no line."
        )
    # The distance does not depend on the length of d, so scale d by a power of two (exact)
    # until its largest component lies in [0.5, 1): products with tiny or huge direction
    # components then neither underflow nor overflow.
    _, exponent = math.frexp(max(abs(dx), abs(dy), abs(dz)))
    dx, dy, dz = math.ldexp(dx, -exponent), math.ldexp(dy, -exponent), math.ldexp(dz, -exponent)
    # w = P0 - P1 and c = w x d. The cross-product form is used instead of |w - proj_d(w)|,
    # which would subtract nearly equal numbers for points far along the line.
    wx, wy, wz = x0 - x1, y0 - y1, z0 - z1
    cx = wy * dz - wz * dy
    cy = wz * dx - wx * dz
    cz = wx * dy - wy * dx
    return finite_result(math.hypot(cx, cy, cz) / math.hypot(dx, dy, dz))


def _point(axis: str, index: int, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{axis}{index}",
        symbol=f"{axis}_{index}",
        description=f"{axis} coordinate of {which}",
        dimension="L",
        si_unit="m",
    )


def _direction(axis: str) -> VariableSpec:
    return VariableSpec(
        name=f"d{axis}",
        symbol=f"d_{axis}",
        description=f"{axis} component of the line direction vector",
        dimension="1",
        si_unit="-",
    )


distance_point_to_line_3d = FormulaSpec(
    id="mathematics.distance_point_to_line_3d",
    name="Distance from a Point to a Line in 3-D",
    equation=(
        "D = sqrt(cx^2 + cy^2 + cz^2) / sqrt(dx^2 + dy^2 + dz^2), where (cx, cy, cz) = "
        "(x0 - x1, y0 - y1, z0 - z1) x (dx, dy, dz)"
    ),
    description=(
        "Shortest (perpendicular) distance from the point (x0, y0, z0) to the line through "
        "(x1, y1, z1) with direction (dx, dy, dz) in three-dimensional space. The direction "
        "does not have to be a unit vector."
    ),
    inputs=(
        _point("x", 0, "the point"),
        _point("y", 0, "the point"),
        _point("z", 0, "the point"),
        _point("x", 1, "a point on the line"),
        _point("y", 1, "a point on the line"),
        _point("z", 1, "a point on the line"),
        _direction("x"),
        _direction("y"),
        _direction("z"),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Shortest distance from the point to the line",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # The source works a procedure, not this closed form. With P on the line, direction d
        # and external point Q, the closest point R satisfies PR = proj_d(PQ) and the distance
        # is |PQ - proj_d(PQ)|. Derived step: with w = Q - P the Lagrange identity gives
        # |w - ((d . w) / (d . d)) d|^2 = (|w|^2 |d|^2 - (d . w)^2) / |d|^2 = |w x d|^2 / |d|^2,
        # which is the equation above (checked symbolically). Selinger's P is (x1, y1, z1)
        # and his Q is (x0, y0, z0), as in distance_point_to_plane.
        selinger_linear_algebra(
            "sec. 3.1, worked example on the shortest distance from a point to a line "
            "(source label exa:shortest-point-line)"
        ),
        # proj_u(v) = (u . v / u . u) u for non-zero u, used in the derivation above.
        selinger_linear_algebra(
            "sec. 2.6, definition of the projection (source label def:projection)"
        ),
        # Mathlib: (u x v) . (w x x) = (u . w)(v . x) - (u . x)(v . w). With u = w = w and
        # v = x = d this is |w x d|^2 = |w|^2 |d|^2 - (w . d)^2, the step from the projection
        # form to the cross-product form.
        mathlib("Mathlib/LinearAlgebra/CrossProduct.lean#L109", "theorem cross_dot_cross"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "x0": 1,
                "y0": 3,
                "z0": 5,
                "x1": 0,
                "y1": 4,
                "z1": -2,
                "dx": 2,
                "dy": 1,
                "dz": 2,
            },
            expected=5.0990195135927845,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 3.1 exa:shortest-point-line: t = 5/3, squared distance 26 "
                "exactly by both the projection procedure and the cross form (Fractions), "
                "printed sqrt(26); scipy minimisation along the line agrees."
            ),
        ),
        VerificationCase(
            inputs={
                "x0": 1,
                "y0": 3,
                "z0": 5,
                "x1": 0,
                "y1": 4,
                "z1": -2,
                "dx": -4,
                "dy": -2,
                "dz": -4,
            },
            expected=5.0990195135927845,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Same line with direction scaled by -2: distance unchanged, sqrt(26).",
        ),
        VerificationCase(
            inputs={
                "x0": 5,
                "y0": 3,
                "z0": 4,
                "x1": -7,
                "y1": 0,
                "z1": 0,
                "dx": 0.5,
                "dy": 0,
                "dz": 0,
            },
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Line = x-axis: distance sqrt(3^2 + 4^2) = 5 by hand.",
        ),
        VerificationCase(
            inputs={
                "x0": 1.5,
                "y0": -2,
                "z0": 0.25,
                "x1": -1,
                "y1": 0.5,
                "z1": 2,
                "dx": 1,
                "dy": 2,
                "dz": -2,
            },
            expected=3.9308254716902518,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Decimal coordinates: exact squared distance (Fraction) then mpmath sqrt; "
                "both routes and scipy agree."
            ),
        ),
        VerificationCase(
            inputs={
                "x0": 4,
                "y0": 6,
                "z0": 2,
                "x1": 0,
                "y1": 4,
                "z1": -2,
                "dx": 2,
                "dy": 1,
                "dz": 2,
            },
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Point P + 2d lies on the line: distance 0.",
        ),
    ),
    assumptions=(
        "Line given by a point and a non-zero direction vector; (dx, dy, dz) = (0, 0, 0) raises "
        "ValueError because it does not define a line.",
        "Cartesian coordinates in an orthonormal frame; the point coordinates share one length "
        "unit. Only the direction of d matters: any non-zero multiple, positive or negative, "
        "gives the same distance.",
        "Unsigned distance; the foot of the perpendicular is not returned.",
        "Derived result: the closed form is worked out from the cited projection procedure "
        "(squared distance as |w x d|^2 / |d|^2 by the Lagrange identity), checked "
        "symbolically (sympy) and numerically against the projection procedure in exact "
        "fractions; the cited text works the procedure rather than printing this formula.",
        "Coordinate differences or cross-product components that leave the floating-point "
        "range raise OverflowError.",
    ),
    tags=(
        "point to line distance",
        "line",
        "direction vector",
        "cross product",
        "projection",
        "3D",
        "analytic geometry",
    ),
)

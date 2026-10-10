"""Area of a Triangle from 3-D Vertices: S = 0.5 * |(P2 - P1) x (P3 - P1)|."""

import math

from sciengformulary.catalog._sources import selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_NAMES = ("x1", "y1", "z1", "x2", "y2", "z2", "x3", "y3", "z3")


def _evaluate(
    x1: float,
    y1: float,
    z1: float,
    x2: float,
    y2: float,
    z2: float,
    x3: float,
    y3: float,
    z3: float,
) -> float:
    for name, value in zip(_NAMES, (x1, y1, z1, x2, y2, z2, x3, y3, z3)):
        finite(name, value)
    # Edge vectors from the first vertex, then their cross product.
    px, py, pz = x2 - x1, y2 - y1, z2 - z1
    qx, qy, qz = x3 - x1, y3 - y1, z3 - z1
    cx = py * qz - pz * qy
    cy = pz * qx - px * qz
    cz = px * qy - py * qx
    return finite_result(0.5 * math.hypot(cx, cy, cz))


def _coordinate(axis: str, vertex: int, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{axis}{vertex}",
        symbol=f"{axis}_{vertex}",
        description=f"{axis} coordinate of the {which} vertex",
        dimension="L",
        si_unit="m",
    )


triangle_area_from_vertices_3d = FormulaSpec(
    id="mathematics.triangle_area_from_vertices_3d",
    name="Area of a Triangle from 3-D Vertices",
    equation=(
        "S = 0.5 * sqrt(cx^2 + cy^2 + cz^2), where (cx, cy, cz) = "
        "((x2-x1, y2-y1, z2-z1) x (x3-x1, y3-y1, z3-z1))"
    ),
    description=(
        "Area of the triangle with vertices (x1, y1, z1), (x2, y2, z2) and (x3, y3, z3) in "
        "three-dimensional space: half the length of the cross product of the two edge vectors "
        "leaving the first vertex. For the area from three side lengths instead, see "
        "heron_triangle_area."
    ),
    inputs=tuple(
        _coordinate(axis, vertex, which)
        for vertex, which in ((1, "first"), (2, "second"), (3, "third"))
        for axis in "xyz"
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Area of the triangle",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger names the vertices P, Q, R; here P -> (x1, y1, z1), Q -> (x2, y2, z2),
        # R -> (x3, y3, z3), and |PQ x PR| is expanded with the coordinate cross product.
        selinger_linear_algebra(
            "sec. 2.7, worked example on the area of a triangle (source label exa:area-triangle)"
        ),
        # |u x v| is the area of the parallelogram on u and v; the triangle is half of it.
        selinger_linear_algebra(
            "sec. 2.7, geometric definition of the cross product "
            "(source label def:cross-product-geometric)"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "x1": 1,
                "y1": 2,
                "z1": 3,
                "x2": 0,
                "y2": 2,
                "z2": 5,
                "x3": 5,
                "y3": 1,
                "z3": 2,
            },
            expected=3.6742346141747673,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example in Selinger sec. 2.7 (area of a triangle): (3/2) sqrt(6) from "
                "the cross product (2, 7, 1), evaluated to 50 digits with mpmath; an exact "
                "squared-side-length identity agrees."
            ),
        ),
        VerificationCase(
            inputs={
                "x1": 1,
                "y1": 0,
                "z1": 1,
                "x2": 2,
                "y2": 2,
                "z2": 3,
                "x3": -1,
                "y3": 1,
                "z3": 3,
            },
            expected=4.031128874149275,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Half of the parallelogram area sqrt(65) printed in a Selinger sec. 2.7 example "
                "(cross product (2, -6, 5)); sqrt(65) / 2 to 50 digits with mpmath."
            ),
        ),
        VerificationCase(
            inputs={
                "x1": 0,
                "y1": 0,
                "z1": 0,
                "x2": 3,
                "y2": 0,
                "z2": 0,
                "x3": 0,
                "y3": 4,
                "z3": 0,
            },
            expected=6.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Right triangle with legs 3 and 4: area 3 * 4 / 2 = 6 by hand.",
        ),
        VerificationCase(
            inputs={
                "x1": 0,
                "y1": 0,
                "z1": 0,
                "x2": 1,
                "y2": 1,
                "z2": 1,
                "x3": 2,
                "y3": 2,
                "z3": 2,
            },
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Collinear vertices give a degenerate triangle: area 0 by inspection.",
        ),
    ),
    assumptions=(
        "Cartesian coordinates in an orthonormal frame, all nine in one length unit.",
        "The area does not depend on which vertex the edge vectors start from or on the "
        "vertex order.",
        "Collinear or coincident vertices give a degenerate triangle of area 0.",
    ),
    tags=(
        "triangle area",
        "cross product",
        "vertices",
        "3D",
        "coordinate geometry",
        "parallelogram",
    ),
)

"""Volume of a Parallelepiped: V = |(u x v) . w|."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase

_NAMES = ("ux", "uy", "uz", "vx", "vy", "vz", "wx", "wy", "wz")


def _evaluate(
    ux: float,
    uy: float,
    uz: float,
    vx: float,
    vy: float,
    vz: float,
    wx: float,
    wy: float,
    wz: float,
) -> float:
    for name, value in zip(_NAMES, (ux, uy, uz, vx, vy, vz, wx, wy, wz)):
        finite(name, value)
    # Integer inputs stay exact until the final conversion.
    box = (uy * vz - uz * vy) * wx + (uz * vx - ux * vz) * wy + (ux * vy - uy * vx) * wz
    return finite_result(float(abs(box)))


def _component(vector: str, axis: str) -> VariableSpec:
    return VariableSpec(
        name=f"{vector}{axis}",
        symbol=f"{vector}_{axis}",
        description=f"{axis} component of edge vector {vector}",
        dimension="L",
        si_unit="m",
    )


parallelepiped_volume = FormulaSpec(
    id="mathematics.parallelepiped_volume",
    name="Volume of a Parallelepiped",
    equation="V = |(uy*vz - uz*vy)*wx + (uz*vx - ux*vz)*wy + (ux*vy - uy*vx)*wz|",
    description=(
        "Volume of the parallelepiped spanned by three edge vectors u, v, w from one vertex in "
        "three-dimensional space: the absolute value of the box (scalar triple) product "
        "(u x v) . w, which also equals |det| of the matrix with rows u, v, w."
    ),
    inputs=tuple(_component(vector, axis) for vector in "uvw" for axis in "xyz"),
    output=VariableSpec(
        name="V",
        symbol="V",
        description="Volume of the parallelepiped",
        dimension="L^3",
        si_unit="m^3",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger defines the volume as the absolute value of the box product (u x v) . w;
        # the equation expands it with the coordinate cross and dot products.
        selinger_linear_algebra(
            "sec. 2.7, proposition on the box product and volume (source label prop:box-product)"
        ),
        # Mathlib: u . (v x w) = det of the matrix with rows u, v, w. With
        # (u x v) . w = u . (v x w) this gives V = |det[u; v; w]| (algebraic identity only).
        mathlib("Mathlib/LinearAlgebra/CrossProduct.lean#L103", "theorem triple_product_eq_det"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "ux": 1,
                "uy": 2,
                "uz": -5,
                "vx": 1,
                "vy": 3,
                "vz": -6,
                "wx": 3,
                "wy": 2,
                "wz": 3,
            },
            expected=14.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Worked example in Selinger sec. 2.7 (parallelepiped volume), value 14; equals "
                "the determinant of the rows by an exact Leibniz sum."
            ),
        ),
        VerificationCase(
            inputs={
                "ux": 1,
                "uy": 1,
                "uz": 1,
                "vx": 1,
                "vy": 2,
                "vz": 3,
                "wx": 0,
                "wy": 1,
                "wz": 1,
            },
            expected=1.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.7 handedness example (b): box product printed as -1 (left-"
                "handed triple), so the volume is 1; checks the absolute value."
            ),
        ),
        VerificationCase(
            inputs={
                "ux": 0.5,
                "uy": -1.5,
                "uz": 2.25,
                "vx": 3.0,
                "vy": 0.75,
                "vz": -1.0,
                "wx": -2.5,
                "wy": 4.0,
                "wz": 1.5,
            },
            expected=36.78125,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Dyadic components, so exact fraction arithmetic gives the box product 1177/32.",
        ),
        VerificationCase(
            inputs={
                "ux": 0,
                "uy": 1,
                "uz": 2,
                "vx": 1,
                "vy": 2,
                "vz": 2,
                "wx": 1,
                "wy": 1,
                "wz": 0,
            },
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "Selinger sec. 2.7 handedness example (c): box product printed as 0 for these "
                "coplanar vectors, so the volume is 0."
            ),
        ),
    ),
    assumptions=(
        "u, v and w are edge vectors leaving one common vertex, given as Cartesian components "
        "in one length unit.",
        "The absolute value drops the handedness sign, so any ordering of u, v, w gives the "
        "same volume.",
        "Coplanar (linearly dependent) edge vectors span a flat parallelepiped of volume 0.",
        "Integer components are multiplied exactly; with floats, nearly coplanar vectors lose "
        "relative accuracy to cancellation.",
    ),
    tags=(
        "parallelepiped",
        "volume",
        "box product",
        "scalar triple product",
        "cross product",
        "determinant",
        "3D",
    ),
)

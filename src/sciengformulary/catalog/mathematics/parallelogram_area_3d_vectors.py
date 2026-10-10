"""Area of a Parallelogram from Two 3-D Side Vectors: S = |u x v|."""

from fractions import Fraction

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite
from sciengformulary.catalog.mathematics._exact_roots import fraction_to_float, sqrt_as_fraction
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> float:
    values = (("ux", ux), ("uy", uy), ("uz", uz), ("vx", vx), ("vy", vy), ("vz", vz))
    ux, uy, uz, vx, vy, vz = (Fraction(finite(name, value)) for name, value in values)
    # The cross product and the sum of its squares are exact Fractions, so a component product
    # that would overflow in floating point (and cancel against another) cannot make the
    # result inf or nan; only the final square root and the conversion to float round.
    cx = uy * vz - uz * vy
    cy = uz * vx - ux * vz
    cz = ux * vy - uy * vx
    return fraction_to_float(sqrt_as_fraction(cx * cx + cy * cy + cz * cz))


def _component(vector: str, axis: str, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{vector}{axis}",
        symbol=f"{vector}_{axis}",
        description=f"{axis} component of the {which} side vector {vector}",
        dimension="L",
        si_unit="m",
    )


parallelogram_area_3d_vectors = FormulaSpec(
    id="mathematics.parallelogram_area_3d_vectors",
    name="Area of a Parallelogram from Two 3-D Side Vectors",
    equation=(
        "S = sqrt(cx^2 + cy^2 + cz^2), where (cx, cy, cz) = "
        "(uy*vz - uz*vy, uz*vx - ux*vz, ux*vy - uy*vx)"
    ),
    description=(
        "Area of the parallelogram spanned by two edge vectors u and v drawn from a common "
        "vertex in three-dimensional space: the length of their cross product."
    ),
    inputs=(
        _component("u", "x", "first"),
        _component("u", "y", "first"),
        _component("u", "z", "first"),
        _component("v", "x", "second"),
        _component("v", "y", "second"),
        _component("v", "z", "second"),
    ),
    output=VariableSpec(
        name="S",
        symbol="S",
        description="Area of the parallelogram",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger prints the cross-product components u x v = (u2 v3 - u3 v2, u3 v1 - u1 v3,
        # u1 v2 - u2 v1) and states that the parallelogram determined by u and v has area
        # |u x v|. Derived step: |u x v| is written out with the length formula of sec. 2.5,
        # sqrt(cx^2 + cy^2 + cz^2); the components are renamed (1, 2, 3) -> (x, y, z).
        selinger_linear_algebra(
            "sec. 2.7, worked example on the area of a parallelogram "
            "(source label exa:area-parallelogram)"
        ),
        # |u x v| = |u| |v| sin(theta), the area of the parallelogram spanned by u and v.
        selinger_linear_algebra(
            "sec. 2.7, geometric definition of the cross product "
            "(source label def:cross-product-geometric)"
        ),
        # Mathlib: a x b = ![a 1 * b 2 - a 2 * b 1, a 2 * b 0 - a 0 * b 2, a 0 * b 1 - a 1 * b 0]
        # (0-based indices); with 0, 1, 2 -> x, y, z these are the three components above. It
        # supports the component formula only, not the area interpretation.
        mathlib("Mathlib/LinearAlgebra/CrossProduct.lean#L63", "theorem cross_apply"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": 1, "uy": -1, "uz": 2, "vx": 3, "vy": -2, "vz": 1},
            expected=5.916079783099616,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.7 exa:area-parallelogram: u x v = (3, 5, 1), area sqrt(35); "
                "the Lagrange identity gives the same squared area 35 exactly."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 2, "vx": -2, "vy": 1, "vz": 2},
            expected=8.06225774829855,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Selinger exa:area-parallelogram2 edges PQ and PR: sqrt(65).",
        ),
        VerificationCase(
            inputs={"ux": 3, "uy": 0, "uz": 0, "vx": 0, "vy": 4, "vz": 0},
            expected=12.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="3-by-4 rectangle: 12.",
        ),
        VerificationCase(
            inputs={"ux": 0.5, "uy": -1.5, "uz": 2.0, "vx": 1.25, "vy": 0.75, "vz": -1},
            expected=3.75,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Decimal components: exact squared area 225/16 (cross components and Lagrange "
                "identity agree), area 3.75."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": -2, "vy": -4, "vz": -6},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Antiparallel edges: degenerate, area 0.",
        ),
    ),
    assumptions=(
        "u and v are two adjacent edges drawn from the same vertex, in one orthonormal "
        "Cartesian frame and one length unit.",
        "Parallel, antiparallel or zero vectors give area 0 (degenerate parallelogram); no "
        "such input raises.",
        "Unsigned area: the orientation of the cross product is discarded.",
        "Derived result: the area |u x v| from the source is written with the component "
        "formula for the cross product and the length formula. It was checked symbolically "
        "(sympy, Lagrange identity |u x v|^2 = |u|^2 |v|^2 - (u . v)^2) and numerically.",
        "The cross product is formed exactly from the given floating-point values, so only an "
        "area outside the floating-point range raises OverflowError (never an intermediate "
        "product that cancels).",
    ),
    tags=("parallelogram", "area", "cross product", "3D", "vector geometry"),
)

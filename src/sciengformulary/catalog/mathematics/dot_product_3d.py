"""Dot Product of Two 3-D Vectors: s = ux*vx + uy*vy + uz*vz."""

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> float:
    values = (("ux", ux), ("uy", uy), ("uz", uz), ("vx", vx), ("vy", vy), ("vz", vz))
    for name, value in values:
        finite(name, value)
    # Integer inputs stay exact until the final conversion.
    return finite_result(float(ux * vx + uy * vy + uz * vz))


def _component(vector: str, axis: str, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{vector}{axis}",
        symbol=f"{vector}_{axis}",
        description=f"{axis} component of the {which} vector {vector}",
        dimension="L",
        si_unit="m",
    )


dot_product_3d = FormulaSpec(
    id="mathematics.dot_product_3d",
    name="Dot Product of Two 3-D Vectors",
    equation="s = ux*vx + uy*vy + uz*vz",
    description=(
        "Scalar (dot) product of two vectors in three-dimensional space from their Cartesian "
        "components: the sum of the products of matching components."
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
        name="s",
        symbol=r"\mathbf{u} \cdot \mathbf{v}",
        description="Dot product of u and v",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger: u . v = u1 v1 + u2 v2 + ... + un vn for u, v in R^n. Here n = 3 is written
        # out and the components are renamed (u1, u2, u3) -> (ux, uy, uz), likewise for v.
        selinger_linear_algebra(
            "sec. 2.6, definition of the dot product (source label def:dot-product)"
        ),
        # Mathlib: <x, y> = sum_i <x i, y i> in the L2 product space; index type Fin 3, and the
        # real inner product of two reals is their product.
        mathlib("Mathlib/Analysis/InnerProductSpace/PiL2.lean#L104", "theorem PiLp.inner_apply"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": 4, "vy": 5, "vz": 6},
            expected=32.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Hand calculation 4 + 10 + 18 = 32.",
        ),
        VerificationCase(
            inputs={"ux": 2, "uy": 3, "uz": -4, "vx": 1, "vy": -2, "vz": 1},
            expected=-8.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Selinger sec. 2.6 exa:vector-projection prints u.v = -8 for these vectors.",
        ),
        VerificationCase(
            inputs={"ux": 0.5, "uy": -1.25, "uz": 2, "vx": 4, "vy": 0.8, "vz": -0.75},
            expected=-0.5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact Fractions: 2 - 1 - 1.5 = -0.5; numpy agrees.",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 0, "uz": 0, "vx": 0, "vy": 1, "vz": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Orthogonal unit vectors: 0.",
        ),
        VerificationCase(
            inputs={"ux": 0, "uy": 0, "uz": 0, "vx": 7.5, "vy": -3, "vz": 2},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Zero vector: 0.",
        ),
    ),
    assumptions=(
        "Components in one orthonormal Cartesian frame (the standard Euclidean inner product).",
        "Components are lengths in any consistent length unit, so s carries the square of that "
        "unit (the components are listed as lengths and s as an area-type L^2 quantity, as in "
        "parallelogram_area_3d_vectors).",
        "Zero vectors are allowed and give s = 0.",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("dot product", "scalar product", "inner product", "3D", "vectors"),
)

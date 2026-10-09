"""Magnitude of a 3-D Vector: u_norm = sqrt(ux^2 + uy^2 + uz^2)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(ux: float, uy: float, uz: float) -> float:
    for name, value in (("ux", ux), ("uy", uy), ("uz", uz)):
        finite(name, value)
    # math.hypot scales internally, so large components do not overflow when squared.
    return finite_result(math.hypot(ux, uy, uz))


def _component(axis: str) -> VariableSpec:
    return VariableSpec(
        name=f"u{axis}",
        symbol=f"u_{axis}",
        description=f"{axis} component of the vector u",
        dimension="L",
        si_unit="m",
    )


vector_magnitude_3d = FormulaSpec(
    id="mathematics.vector_magnitude_3d",
    name="Magnitude of a 3-D Vector",
    equation="u_norm = sqrt(ux^2 + uy^2 + uz^2)",
    description=(
        "Length (Euclidean norm, magnitude) of a vector in three-dimensional space from its "
        "Cartesian components."
    ),
    inputs=(_component("x"), _component("y"), _component("z")),
    output=VariableSpec(
        name="u_norm",
        symbol=r"\lVert\mathbf{u}\rVert",
        description="Length of u",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger: |u| = sqrt(u1^2 + ... + un^2) for u in R^n, also called the magnitude or
        # norm. Here n = 3 is written out and the components are renamed
        # (u1, u2, u3) -> (ux, uy, uz).
        selinger_linear_algebra(
            "sec. 2.5, definition of the length of a vector (source label def:length-of-vector)"
        ),
        # Mathlib: |x| = sqrt (sum_i |x i| ^ 2) in Euclidean space over a finite index type;
        # index type Fin 3, and |t|^2 = t^2 for real t.
        mathlib(
            "Mathlib/Analysis/InnerProductSpace/PiL2.lean#L159", "theorem EuclideanSpace.norm_eq"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": 1, "uy": -3, "uz": 4},
            expected=5.0990195135927845,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Selinger sec. 2.5 exa:unit-vector: sqrt(26), mpmath 50 digits.",
        ),
        VerificationCase(
            inputs={"ux": 2, "uy": 3, "uz": 6},
            expected=7.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Exact: 49 -> 7.",
        ),
        VerificationCase(
            inputs={"ux": 0.1, "uy": 0.2, "uz": -0.3},
            expected=0.37416573867739417,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Decimal components: sqrt(0.14) from exact Fraction 7/50.",
        ),
        VerificationCase(
            inputs={"ux": 3e200, "uy": -4e200, "uz": 0},
            expected=5e200,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="5e200; naive squaring overflows to inf.",
        ),
        VerificationCase(
            inputs={"ux": 0, "uy": 0, "uz": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Zero vector: 0.",
        ),
    ),
    assumptions=(
        "Components in one orthonormal Cartesian frame and any consistent length unit; the "
        "length is in that same unit (the components are listed as lengths, as in "
        "parallelogram_area_3d_vectors).",
        "The zero vector has length 0.",
        "A length outside the floating-point range (all three components near 1e308) raises "
        "OverflowError.",
    ),
    tags=("vector magnitude", "norm", "length", "3D", "vectors"),
)

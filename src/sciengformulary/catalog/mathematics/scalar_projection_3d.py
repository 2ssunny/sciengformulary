"""Scalar Projection of a 3-D Vector: c = (u . v) / |u|."""

import math

from sciengformulary.catalog._sources import selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> float:
    values = (("ux", ux), ("uy", uy), ("uz", uz), ("vx", vx), ("vy", vy), ("vz", vz))
    for name, value in values:
        finite(name, value)
    if ux == uy == uz == 0:
        raise ValueError("u must be a non-zero vector; the scalar projection needs a direction.")
    # (u . v) / |u| is unchanged when u is multiplied by a positive number, so scale u by a
    # power of two (exact) until its largest component lies in [0.5, 1): a tiny or huge u then
    # neither underflows nor overflows in the dot product and the length.
    _, exponent = math.frexp(max(abs(ux), abs(uy), abs(uz)))
    ux, uy, uz = math.ldexp(ux, -exponent), math.ldexp(uy, -exponent), math.ldexp(uz, -exponent)
    return finite_result((ux * vx + uy * vy + uz * vz) / math.hypot(ux, uy, uz))


def _component(vector: str, axis: str, role: str) -> VariableSpec:
    return VariableSpec(
        name=f"{vector}{axis}",
        symbol=f"{vector}_{axis}",
        description=f"{axis} component of the {role} {vector}",
        dimension="L",
        si_unit="m",
    )


scalar_projection_3d = FormulaSpec(
    id="mathematics.scalar_projection_3d",
    name="Scalar Projection of a 3-D Vector",
    equation="c = (ux*vx + uy*vy + uz*vz) / sqrt(ux^2 + uy^2 + uz^2)",
    description=(
        "Signed component of a vector v along the direction of a non-zero vector u in "
        "three-dimensional space (the scalar projection of v onto u). It is negative when the "
        "angle between the two vectors is obtuse."
    ),
    inputs=(
        _component("u", "x", "direction vector"),
        _component("u", "y", "direction vector"),
        _component("u", "z", "direction vector"),
        _component("v", "x", "projected vector"),
        _component("v", "y", "projected vector"),
        _component("v", "z", "projected vector"),
    ),
    output=VariableSpec(
        name="c",
        symbol=r"\mathrm{comp}_{\mathbf{u}}(\mathbf{v})",
        description="Signed length of the projection of v onto the direction of u",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger defines, for non-zero u, the component of v in the direction of u as
        # comp_u(v) = u . v / |u|. Derived step: u . v and |u| are written out in the three
        # Cartesian components (sec. 2.6 dot product, sec. 2.5 length), which gives the
        # equation above (checked symbolically).
        selinger_linear_algebra(
            "sec. 2.6, definition of the projection (source label def:projection)"
        ),
        # |u| = sqrt(u1^2 + ... + un^2); here n = 3.
        selinger_linear_algebra(
            "sec. 2.5, definition of the length of a vector (source label def:length-of-vector)"
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": 2, "uy": 3, "uz": -4, "vx": 1, "vy": -2, "vz": 1},
            expected=-1.4855627054164149,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.6 exa:vector-projection data (u.v = -8, u.u = 29 printed): "
                "-8/sqrt(29); |v| cos(theta) route agrees (mpmath)."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": -2, "vx": 2, "vy": 1, "vz": 3},
            expected=-0.6666666666666666,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="|u| = 3, u.v = -2: -2/3.",
        ),
        VerificationCase(
            inputs={"ux": 0, "uy": 0, "uz": 2, "vx": 1, "vy": 1, "vz": 5},
            expected=5.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="u along z: picks vz = 5.",
        ),
        VerificationCase(
            inputs={"ux": 0.5, "uy": -1, "uz": 2, "vx": 3, "vy": 0.25, "vz": -1.5},
            expected=-0.7637626158259734,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Decimal components: exact u.v and u.u (Fractions), mpmath sqrt.",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 1, "uz": 0, "vx": 1, "vy": -1, "vz": 7},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Orthogonal: 0.",
        ),
    ),
    assumptions=(
        "u must be non-zero; u = (0, 0, 0) raises ValueError because it has no direction.",
        "Only the direction of u matters: positive scaling of u leaves c unchanged and "
        "negating u flips its sign.",
        "All components are lengths in one orthonormal Cartesian frame and any consistent length "
        "unit; c is in that same unit (the unit of v).",
        "Derived result: the source's scalar projection u . v / |u| is written out in "
        "three-dimensional components using the dot-product and length formulas. The "
        "expansion was checked symbolically and numerically (|v| cos(theta) route).",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("scalar projection", "vector component", "dot product", "projection", "3D"),
)

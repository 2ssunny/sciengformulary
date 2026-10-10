"""Angle Between Two 3-D Vectors: theta = arccos(u . v / (|u| |v|))."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(ux: float, uy: float, uz: float, vx: float, vy: float, vz: float) -> float:
    values = (("ux", ux), ("uy", uy), ("uz", uz), ("vx", vx), ("vy", vy), ("vz", vz))
    for name, value in values:
        finite(name, value)
    if ux == uy == uz == 0:
        raise ValueError("u must be a non-zero vector; the angle is undefined for u = 0.")
    if vx == vy == vz == 0:
        raise ValueError("v must be a non-zero vector; the angle is undefined for v = 0.")
    # The angle does not depend on the vectors' lengths, so scale each by its largest
    # component first: products of very small or very large components would otherwise
    # underflow to 0 or overflow to inf and give a wrong angle without an error.
    u_scale = max(abs(ux), abs(uy), abs(uz))
    v_scale = max(abs(vx), abs(vy), abs(vz))
    ux, uy, uz = ux / u_scale, uy / u_scale, uz / u_scale
    vx, vy, vz = vx / v_scale, vy / v_scale, vz / v_scale
    # For non-zero u, v: |u x v| = |u| |v| sin(theta) and u . v = |u| |v| cos(theta) with
    # sin(theta) >= 0 on [0, pi], so atan2 returns the same angle as the arccos form. It stays
    # accurate near 0 and pi, where arccos of a rounded cosine loses about half the digits.
    cx = uy * vz - uz * vy
    cy = uz * vx - ux * vz
    cz = ux * vy - uy * vx
    dot = ux * vx + uy * vy + uz * vz
    return math.atan2(math.hypot(cx, cy, cz), dot)


def _component(vector: str, axis: str, which: str) -> VariableSpec:
    return VariableSpec(
        name=f"{vector}{axis}",
        symbol=f"{vector}_{axis}",
        description=f"{axis} component of the {which} vector {vector}",
        dimension="1",
        si_unit="-",
    )


angle_between_vectors_3d = FormulaSpec(
    id="mathematics.angle_between_vectors_3d",
    name="Angle Between Two 3-D Vectors",
    equation=(
        "theta = arccos((ux*vx + uy*vy + uz*vz) / (sqrt(ux^2 + uy^2 + uz^2) * "
        "sqrt(vx^2 + vy^2 + vz^2)))"
    ),
    description=(
        "Included (unoriented) angle between two non-zero vectors in three-dimensional space: "
        "the angle whose cosine is their dot product divided by the product of their lengths. "
        "The result is in radians, from 0 to pi."
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
        name="theta",
        symbol=r"\theta",
        description="Included angle between u and v, in radians",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger: u . v = |u| |v| cos(theta) with 0 <= theta <= pi; dividing by the non-zero
        # lengths and taking arccos gives the equation above.
        selinger_linear_algebra(
            "sec. 2.6, proposition relating the dot product to the angle "
            "(source label prop:dot-product-angle)"
        ),
        # |u x v| = |u| |v| sin(theta): justifies the atan2 form used by the evaluator.
        selinger_linear_algebra(
            "sec. 2.7, geometric definition of the cross product "
            "(source label def:cross-product-geometric)"
        ),
        # Mathlib defines the angle as arccos(<x, y> / (|x| |y|)) in any real inner product
        # space. Its value pi/2 when a vector is zero is a totalisation convention and is not
        # adopted here: zero vectors raise ValueError.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/Basic.lean#L41",
            "def InnerProductGeometry.angle",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"ux": -1, "uy": 1, "uz": 2, "vx": 2, "vy": 1, "vz": -1},
            expected=2.0943951023931957,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Direction vectors of the Selinger sec. 3.1 angle-between-lines example: "
                "cos = -1/2, theta = 2 pi / 3, evaluated to 50 digits with mpmath."
            ),
        ),
        VerificationCase(
            inputs={"ux": 7, "uy": -1, "uz": 0, "vx": 4, "vy": 3, "vz": 5},
            expected=1.0471975511965979,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Plane normals of the Selinger sec. 3.2 angle-between-planes example: "
                "cos = 25/50, theta = pi / 3, evaluated to 50 digits with mpmath."
            ),
        ),
        VerificationCase(
            inputs={"ux": 2, "uy": 2, "uz": 0, "vx": 0, "vy": 3, "vz": 0},
            expected=0.7853981633974483,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.6 worked example in the plane, embedded with z = 0 (dot "
                "product and lengths unchanged): theta = pi / 4."
            ),
        ),
        VerificationCase(
            inputs={"ux": 2, "uy": -1, "uz": -2, "vx": 2, "vy": 2, "vz": -1},
            expected=1.1102423351135742,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 3.2 line-plane example, printed as about 1.11 rad: "
                "arccos(4/9) evaluated to 50 digits with mpmath."
            ),
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": -2, "vy": -4, "vz": -6},
            expected=3.141592653589793,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Antiparallel vectors (v = -2 u): upper end of the range, theta = pi.",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 2, "uz": 3, "vx": 2, "vy": 4, "vz": 6},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Parallel vectors (v = 2 u): lower end of the range, theta = 0.",
        ),
        VerificationCase(
            inputs={"ux": 1, "uy": 0, "uz": 0, "vx": 1, "vy": 1e-09, "vz": 0},
            expected=1e-09,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Nearly parallel: exact angle atan(1e-9) = 1e-9 to 18 digits (mpmath). Guards "
                "against an arccos evaluator, which returns 0.0 here."
            ),
        ),
    ),
    assumptions=(
        "Both vectors must be non-zero; a zero vector raises ValueError because the angle is "
        "undefined.",
        "Unoriented angle in [0, pi]: swapping u and v gives the same value, and no sense of "
        "rotation is reported.",
        "The components of u share one unit and those of v share one unit; the angle does not "
        "change under positive scaling of either vector.",
        "Evaluated as atan2(|u x v|, u . v), which equals the arccos form for non-zero vectors "
        "and keeps full precision for nearly parallel or antiparallel vectors.",
    ),
    tags=(
        "angle between vectors",
        "dot product",
        "included angle",
        "3D",
        "vector geometry",
        "arccos",
    ),
)

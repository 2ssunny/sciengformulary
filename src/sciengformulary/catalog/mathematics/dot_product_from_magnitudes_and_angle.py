"""Dot Product from Lengths and Included Angle: s = u_norm * v_norm * cos(theta)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog.mathematics._domain import finite, finite_result, non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(u_norm: float, v_norm: float, theta: float) -> float:
    non_negative("u_norm", u_norm)
    non_negative("v_norm", v_norm)
    finite("theta", theta)
    if not 0 <= theta <= math.pi:
        raise ValueError(
            f"theta must be the included angle in [0, pi] radians, got {theta!r}; cos would "
            "accept other values, but they are not included angles."
        )
    # Multiplying by cos(theta) first keeps the intermediate value no larger than u_norm.
    return finite_result((u_norm * math.cos(theta)) * v_norm)


dot_product_from_magnitudes_and_angle = FormulaSpec(
    id="mathematics.dot_product_from_magnitudes_and_angle",
    name="Dot Product from Lengths and Included Angle",
    equation="s = u_norm * v_norm * cos(theta)",
    description=(
        "Dot product of two vectors from their lengths and the included angle between them. "
        "The result is negative when the angle is obtuse."
    ),
    inputs=(
        VariableSpec(
            name="u_norm",
            symbol=r"\lVert\mathbf{u}\rVert",
            description="Length of the first vector u",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="v_norm",
            symbol=r"\lVert\mathbf{v}\rVert",
            description="Length of the second vector v",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="theta",
            symbol=r"\theta",
            description="Included angle between u and v, in radians",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="s",
        symbol=r"\mathbf{u} \cdot \mathbf{v}",
        description="Dot product of u and v",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Selinger: for the included angle theta, 0 <= theta <= pi, u . v = |u| |v| cos(theta).
        # Only the symbols are renamed: |u| -> u_norm and |v| -> v_norm.
        selinger_linear_algebra(
            "sec. 2.6, proposition relating the dot product to the angle "
            "(source label prop:dot-product-angle)"
        ),
        # Mathlib: cos (angle x y) * (|x| * |y|) = <x, y> in a real inner product space, with
        # angle defined as arccos (<x, y> / (|x| * |y|)) in [0, pi]. The product is commuted.
        # It also holds for zero vectors (both sides 0), so zero lengths are admissible.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/Basic.lean#L158",
            "theorem InnerProductGeometry.cos_angle_mul_norm_mul_norm",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"u_norm": 3, "v_norm": 4, "theta": 1.0471975511965976},
            expected=6.000000000000001,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Selinger sec. 2.6 exa:geometric-dot-product: 3*4*cos(pi/3) = 6 (printed). "
                "Expected is mpmath cos of the binary float math.pi/3, 6.000000000000001."
            ),
        ),
        VerificationCase(
            inputs={"u_norm": 1.5, "v_norm": 0.4, "theta": 2.0},
            expected=-0.24968810192828544,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Obtuse angle 2 rad: 0.6*cos(2) < 0; mpmath 50 digits; explicit-vector numpy "
                "dot agrees."
            ),
        ),
        VerificationCase(
            inputs={"u_norm": 2, "v_norm": 5, "theta": 3.141592653589793},
            expected=-10.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Upper domain edge theta = math.pi: -10 (cos of float pi is -1 to 1e-32).",
        ),
        VerificationCase(
            inputs={"u_norm": 2.5, "v_norm": 4, "theta": 0},
            expected=10.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Lower domain edge theta = 0: 10.",
        ),
        VerificationCase(
            inputs={"u_norm": 1, "v_norm": 1, "theta": 1.5707963267948966},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "theta = math.pi/2: exact value 6.1e-17 (float pi/2), checked against 0 with "
                "abs_tol."
            ),
        ),
        VerificationCase(
            inputs={"u_norm": 0, "v_norm": 7, "theta": 1.0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Zero length: 0.",
        ),
    ),
    assumptions=(
        "theta is the unoriented included angle in [0, pi]; values outside raise ValueError.",
        "Lengths are non-negative; a negative length raises ValueError. A zero length gives "
        "s = 0 for any theta.",
        "Because the float nearest pi/2 is not exactly pi/2, perpendicular inputs return about "
        "1e-16 times the lengths rather than exactly 0.",
        "The lengths are listed as dimensionless; if they carry a unit, s carries its square.",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("dot product", "included angle", "cosine", "vectors", "geometry"),
)

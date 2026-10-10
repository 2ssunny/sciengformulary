"""Law of Sines (Side): a = b * sin(alpha) / sin(beta)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite, positive
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(b: float, alpha: float, beta: float) -> float:
    positive("b", b)
    for name, angle in (("alpha", alpha), ("beta", beta)):
        if not 0 < finite(name, angle) < math.pi:
            raise ValueError(f"{name} must lie strictly between 0 and pi radians, got {angle!r}.")
    if alpha + beta >= math.pi:
        raise ValueError(
            f"alpha + beta must be less than pi for a triangle, got {alpha!r} + {beta!r}."
        )
    return b * math.sin(alpha) / math.sin(beta)


law_of_sines_side = FormulaSpec(
    id="mathematics.law_of_sines_side",
    name="Law of Sines (Side)",
    equation="a = b * sin(alpha) / sin(beta)",
    description=(
        "Length of the side a of a triangle from a known side b and the interior angles alpha "
        "(opposite a) and beta (opposite b)."
    ),
    inputs=(
        VariableSpec(
            name="b",
            symbol="b",
            description="Known side, opposite the angle beta",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="alpha",
            symbol=r"\alpha",
            description="Interior angle opposite the unknown side a, in radians",
            dimension="1",
            si_unit="rad",
        ),
        VariableSpec(
            name="beta",
            symbol=r"\beta",
            description="Interior angle opposite the known side b, in radians",
            dimension="1",
            si_unit="rad",
        ),
    ),
    output=VariableSpec(
        name="a",
        symbol="a",
        description="Side opposite the angle alpha",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib (p1, p2, p3 not collinear): dist(p1,p2) = dist(p3,p1) sin(angle p2 p3 p1)
        #   / sin(angle p1 p2 p3). Side p1p2 is opposite p3 and side p3p1 is opposite p2, so
        # a = dist(p1,p2), alpha = angle at p3, b = dist(p3,p1), beta = angle at p2.
        mathlib(
            "Mathlib/Geometry/Euclidean/Triangle.lean#L272",
            "theorem EuclideanGeometry.dist_eq_dist_mul_sin_angle_div_sin_angle",
        ),
        # Product form sin(beta) a = sin(alpha) b; dividing by sin(beta) > 0 (non-degenerate
        # triangle) gives the quotient form above.
        mathlib(
            "Mathlib/Geometry/Euclidean/Triangle.lean#L253",
            "theorem EuclideanGeometry.sin_angle_mul_dist_eq_sin_angle_mul_dist",
        ),
        # Fixes the angle convention: unoriented angle at the middle point, in [0, pi] radians.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/Affine.lean#L41",
            "def EuclideanGeometry.angle",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"b": 1.0, "alpha": 1.5707963267948966, "beta": 0.5235987755982988},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "30-60-90 triangle with float angles: mpmath 50-digit value "
                "2.00000000000000019890..., matched by the side length of a constructed "
                "triangle."
            ),
        ),
        VerificationCase(
            inputs={"b": 2.0, "alpha": 1.0471975511965976, "beta": 1.0471975511965976},
            expected=2.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Equal angles give a = b = 2 exactly; confirmed by a coordinate construction.",
        ),
        VerificationCase(
            inputs={"b": 5.0, "alpha": 0.3, "beta": 2.8},
            expected=4.410905378650007,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "alpha + beta = 3.1 rad, close to pi: mpmath 50-digit value "
                "4.41090537865000668..., matched by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"b": 1.0, "alpha": 1.0, "beta": 0.001},
            expected=841.471125053077,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Tiny beta = 0.001 rad: mpmath 50-digit value 841.471125053076985..., matched "
                "by a coordinate construction."
            ),
        ),
        VerificationCase(
            inputs={"b": 4.0, "alpha": 2.0, "beta": 0.7},
            expected=5.645901656159817,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Obtuse alpha = 2 rad: mpmath 50-digit value 5.64590165615981707..., matched "
                "by a coordinate construction."
            ),
        ),
    ),
    assumptions=(
        "Non-degenerate plane triangle: b > 0, 0 < alpha < pi, 0 < beta < pi and "
        "alpha + beta < pi (the third angle is positive); other inputs raise ValueError.",
        "Each angle is the interior angle opposite the side of the same letter, in radians.",
        "a is returned in the length unit of b.",
    ),
    tags=("law of sines", "sine rule", "triangle", "trigonometry", "geometry"),
)

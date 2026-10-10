"""Area of a Parallelogram from Two Sides and the Included Angle: S = a * b * sin(theta)."""

import math

from sciengformulary.catalog._sources import mathlib, selinger_linear_algebra
from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a: float, b: float, theta: float) -> float:
    non_negative("a", a)
    non_negative("b", b)
    finite("theta", theta)
    if not 0 <= theta <= math.pi:
        raise ValueError(
            f"theta must be the included angle in [0, pi] radians, got {theta!r}; sin would "
            "turn negative beyond pi."
        )
    # Multiplying by sin(theta) first keeps the intermediate value no larger than a.
    return finite_result((a * math.sin(theta)) * b)


parallelogram_area_from_sides_and_angle = FormulaSpec(
    id="mathematics.parallelogram_area_from_sides_and_angle",
    name="Area of a Parallelogram from Two Sides and the Included Angle",
    equation="S = a * b * sin(theta)",
    description=(
        "Area of a parallelogram from the lengths of two adjacent sides and the angle between "
        "them, equal to the base times the height b*sin(theta) over the base a."
    ),
    inputs=(
        VariableSpec(
            name="a",
            symbol="a",
            description="Length of one side",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Length of the adjacent side",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="theta",
            symbol=r"\theta",
            description="Included angle between the two sides, in radians",
            dimension="1",
            si_unit="rad",
        ),
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
        # Selinger: |u x v| = |u| |v| sin(theta) with theta the included angle in [0, pi], and
        # this length is the area of the parallelogram determined by u and v (height
        # |v| sin(theta) over base |u|). Only the symbols are renamed: |u| -> a, |v| -> b.
        selinger_linear_algebra(
            "sec. 2.7, geometric definition of the cross product "
            "(source label def:cross-product-geometric)"
        ),
        # Mathlib: sin (angle x y) * (|x| * |y|) = sqrt (<x, x> * <y, y> - <x, y> ^ 2); with
        # the Lagrange identity (cross_dot_cross) this is |x x y| in R^3. It supports the
        # relation; the area interpretation comes from Selinger.
        mathlib(
            "Mathlib/Geometry/Euclidean/Angle/Unoriented/Basic.lean#L164",
            "theorem InnerProductGeometry.sin_angle_mul_norm_mul_norm",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a": 2, "b": 3, "theta": 1.5707963267948966},
            expected=6.0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Rectangle: 6 (sin of float pi/2 rounds to 1).",
        ),
        VerificationCase(
            inputs={"a": 3, "b": 4, "theta": 2.0943951023931953},
            expected=10.392304845413266,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "theta = 2*math.pi/3: 12*sin = 6*sqrt(3); mpmath of the float angle; numpy |u "
                "x v| of explicit vectors agrees."
            ),
        ),
        VerificationCase(
            inputs={"a": 1, "b": 1, "theta": 0.5235987755982988},
            expected=0.49999999999999994,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="theta = math.pi/6: 0.49999999999999994 (mpmath sin of the float).",
        ),
        VerificationCase(
            inputs={"a": 4, "b": 5, "theta": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Lower domain edge theta = 0: degenerate, 0.",
        ),
        VerificationCase(
            inputs={"a": 2.5, "b": 4, "theta": 3.141592653589793},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note=(
                "Upper domain edge theta = math.pi: exact value 1.2e-15 (sin of float pi), "
                "checked against 0 with abs_tol 1e-12."
            ),
        ),
    ),
    assumptions=(
        "theta is the interior angle between the two sides, in [0, pi]; values outside raise "
        "ValueError.",
        "Side lengths are non-negative; theta = 0, theta = pi or a zero side gives the "
        "degenerate area 0 (at theta = pi the float nearest pi gives about 1e-16 times a*b "
        "rather than exactly 0).",
        "Plane (Euclidean) parallelogram with both sides in one length unit.",
        "A result outside the floating-point range raises OverflowError.",
    ),
    tags=("parallelogram", "area", "sine", "included angle", "plane geometry"),
)

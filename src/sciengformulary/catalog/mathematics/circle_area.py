"""Area of a Circle: A = pi * r^2."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float) -> float:
    non_negative("r", r)
    return finite_result(math.pi * r * r)


circle_area = FormulaSpec(
    id="mathematics.circle_area",
    name="Area of a Circle",
    equation="A = pi * r^2",
    description=(
        "Area enclosed by a circle of radius r in the Euclidean plane, that is the area of the "
        "disc of that radius."
    ),
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description="Radius of the circle",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="A",
        symbol="A",
        description="Area of the disc",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states that the open ball of radius r in the Euclidean plane has Lebesgue
        # volume ofReal(r)^2 * ofReal(pi). For r >= 0 this is pi * r^2. For r < 0 Lean's
        # ofReal truncates to 0; that totalisation is not adopted, a negative r raises.
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L395",
            "lemma EuclideanSpace.volume_ball_fin_two",
        ),
        # Independent second statement (Freek Wiedijk's 100-theorems archive in the same
        # repository): for r : NNReal the Lebesgue measure of {x^2 + y^2 < r^2} is pi * r^2.
        mathlib(
            "Archive/Wiedijk100Theorems/AreaOfACircle.lean#L85",
            "theorem Theorems100.area_disc",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 1},
            expected=3.141592653589793,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Unit circle: pi (mpmath 50 digits).",
        ),
        VerificationCase(
            inputs={"r": 2.5},
            expected=19.634954084936208,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "6.25 pi; mpmath 50-digit value, confirmed by mpmath.quad of the chord length "
                "2*sqrt(r^2 - x^2) over [-r, r]."
            ),
        ),
        VerificationCase(
            inputs={"r": 0.001},
            expected=3.1415926535897933e-06,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Small radius: pi * 1e-6.",
        ),
        VerificationCase(
            inputs={"r": 0},
            expected=0.0,
            rel_tol=0.0,
            abs_tol=1e-12,
            note="Lower domain edge r = 0: area 0.",
        ),
    ),
    assumptions=(
        "Flat (Euclidean) plane. The radius must satisfy r >= 0; a negative radius raises "
        "ValueError.",
        "r = 0 is accepted and gives the degenerate disc of area 0.",
        "Open and closed discs have the same area, so the result applies to both.",
        "A radius above about 7.5e153 makes the area exceed the largest float and raises "
        "OverflowError.",
    ),
    tags=("circle", "disc", "area", "pi", "plane geometry"),
)

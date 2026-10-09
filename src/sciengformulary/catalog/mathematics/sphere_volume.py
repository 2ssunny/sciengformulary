"""Volume of a Sphere: V = (4/3) * pi * r^3."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import non_negative
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float) -> float:
    non_negative("r", r)
    return 4.0 / 3.0 * math.pi * r**3


sphere_volume = FormulaSpec(
    id="mathematics.sphere_volume",
    name="Volume of a Sphere",
    equation="V = (4/3) * pi * r^3",
    description=(
        "Volume enclosed by a sphere of radius r (the solid ball) in three-dimensional space. "
        "This is the d = 3 case of mathematics.n_ball_volume."
    ),
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description="Radius of the sphere",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="V",
        symbol="V",
        description="Enclosed volume",
        dimension="L^3",
        si_unit="m^3",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib (EuclideanSpace R (Fin 3)): volume(ball x r) = r^3 * (4 pi / 3) for r >= 0.
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L405",
            "lemma EuclideanSpace.volume_ball_fin_three",
        ),
        # General Gamma form; at d = 3, sqrt(pi)^3 / Gamma(5/2) = 4 pi / 3.
        mathlib(
            "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean#L308",
            "theorem EuclideanSpace.volume_ball",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 1.0},
            expected=4.188790204786391,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Unit sphere: 4 pi / 3 = 4.18879020478639098...; mpmath, slice integral of "
                "pi (r^2 - z^2) and the d = 3 Gamma form agree."
            ),
        ),
        VerificationCase(
            inputs={"r": 3.0},
            expected=113.09733552923255,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "r = 3: 36 pi = 113.0973355292325565...; mpmath, slice integral and Gamma form "
                "agree."
            ),
        ),
        VerificationCase(
            inputs={"r": 0.1},
            expected=0.004188790204786391,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Small radius, using the exact binary value of 0.1: mpmath value "
                "0.00418879020478639168...; slice integral and Gamma form agree."
            ),
        ),
        VerificationCase(
            inputs={"r": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="r = 0 gives volume 0 exactly.",
        ),
        VerificationCase(
            inputs={"r": 2.5},
            expected=65.44984694978736,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "r = 2.5: 125 pi / 6 = 65.4498469497873591...; mpmath, slice integral and Gamma "
                "form agree."
            ),
        ),
    ),
    assumptions=(
        "Ordinary three-dimensional Euclidean space; V is the volume of the solid ball bounded "
        "by the sphere, not its surface area.",
        "r >= 0; a negative radius raises ValueError. V is in the radius unit cubed.",
        "Special case d = 3 of mathematics.n_ball_volume, which gives the same value.",
    ),
    tags=("sphere", "ball", "volume", "geometry"),
)

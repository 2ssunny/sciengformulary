"""Period of Uniform Circular Motion: T = 2 * pi * r / v."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float, v: float) -> float:
    return 2.0 * math.pi * r / v


circular_motion_period = FormulaSpec(
    id="mechanics.circular_motion_period",
    name="Period of Uniform Circular Motion",
    equation="T = 2 * pi * r / v",
    description="Time for one revolution at constant speed around a circle of radius r.",
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description="Radius of the circular path",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="v",
            symbol="v",
            description="Constant speed along the path",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="T",
        symbol="T",
        description="Period of one revolution",
        dimension="T",
        si_unit="s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated in the section text as v = 2 pi r / T.
        openstax_university_physics(1, "4-4-uniform-and-nonuniform-circular-motion", "sec. 4.4"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 0.175, "v": 5000000.0},
            expected=2.1991148575128554e-07,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation of 2 pi 0.175 / 5.0e6 (the section's "
                "worked example rounds it to 2.20e-7 s)."
            ),
        ),
    ),
    assumptions=(
        "Uniform circular motion: constant speed and radius.",
    ),
    tags=("circular motion", "period", "revolution", "orbit"),
)

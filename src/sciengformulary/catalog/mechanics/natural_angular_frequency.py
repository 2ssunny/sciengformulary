"""Undamped Natural Angular Frequency: omega_n = sqrt(k / m)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, m: float) -> float:
    return math.sqrt(k / m)


natural_angular_frequency = FormulaSpec(
    id="mechanics.natural_angular_frequency",
    name="Undamped Natural Angular Frequency",
    equation="omega_n = sqrt(k / m)",
    description="Angular frequency of free oscillation of a mass on a linear spring.",
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Linear spring stiffness",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="omega_n",
        symbol=r"\omega_n",
        description="Natural angular frequency",
        dimension="T^-1",
        si_unit="rad/s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes omega_0.
        openstax_university_physics(1, "15-1-simple-harmonic-motion", "sec. 15.1, eq. (15.9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 200.0, "m": 2.0},
            expected=10.0,
            rel_tol=1e-12,
            note="Hand calculation: sqrt(200 / 2) = 10 rad/s.",
        ),
    ),
    assumptions=(
        "Linear spring and no damping; small damping lowers the frequency only slightly (see "
        "the damped angular frequency).",
        "Frequency in hertz is omega_n / (2 pi).",
    ),
    tags=("natural frequency", "vibration", "simple harmonic motion", "spring-mass"),
)

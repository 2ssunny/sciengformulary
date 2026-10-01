"""Mean Molecular Speed: v_mean = sqrt(8 * k_B * T / (pi * m))."""

import math

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
    BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float, m: float) -> float:  # noqa: N803 - symbols as written in the source
    return math.sqrt(8.0 * BOLTZMANN_CONSTANT * T / (math.pi * m))


mean_molecular_speed = FormulaSpec(
    id="thermodynamics.mean_molecular_speed",
    name="Mean Molecular Speed",
    equation="v_mean = sqrt(8 * k_B * T / (pi * m))",
    description="Average molecular speed in a gas at equilibrium.",
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of one molecule",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="v_mean",
        symbol=r"\bar{v}",
        description="Mean molecular speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            2,
            "2-4-distribution-of-molecular-speeds",
            "sec. 2.4, eq. (2.16)",
        ),
        BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 300.0, "m": 4.65e-26},
            expected=476.2619100803956,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation.",
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
        "Not the bulk flow speed; differs from the rms and most probable speeds.",
    ),
    tags=("mean speed", "kinetic theory", "molecular speed"),
)

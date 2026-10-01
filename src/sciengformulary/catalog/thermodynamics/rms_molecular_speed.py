"""Root-Mean-Square Molecular Speed: v_rms = sqrt(3 * k_B * T / m)."""

import math

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
    BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float, m: float) -> float:  # noqa: N803 - symbols as written in the source
    return math.sqrt(3.0 * BOLTZMANN_CONSTANT * T / m)


rms_molecular_speed = FormulaSpec(
    id="thermodynamics.rms_molecular_speed",
    name="Root-Mean-Square Molecular Speed",
    equation="v_rms = sqrt(3 * k_B * T / m)",
    description="Root-mean-square molecular speed in a gas at equilibrium.",
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
        name="v_rms",
        symbol="v_{rms}",
        description="Root-mean-square molecular speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            2,
            "2-2-pressure-temperature-and-rms-speed",
            "sec. 2.2, eq. (2.8)",
        ),
        BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 300.0, "m": 4.65e-26},
            expected=516.9355734487366,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation.",
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
    ),
    tags=("rms speed", "kinetic theory", "molecular speed"),
)

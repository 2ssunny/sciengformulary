"""Speed of Sound in an Ideal Gas: a = sqrt(gamma * R * T)."""

import math

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    gamma: float,
    R: float,  # noqa: N803
    T: float,  # noqa: N803
) -> float:
    return math.sqrt(gamma * R * T)


speed_of_sound_ideal_gas = FormulaSpec(
    id="aerodynamics.speed_of_sound_ideal_gas",
    name="Speed of Sound in an Ideal Gas",
    equation="a = sqrt(gamma * R * T)",
    description=(
        "Speed at which small pressure disturbances travel through a thermally perfect gas. It "
        "depends only on the gas and its absolute temperature, not on pressure."
    ),
    inputs=(
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v of the gas",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant of the gas (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute static temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="a",
        symbol="a",
        description="Speed of sound",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        naca_report_1135("eq. (29b)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"gamma": 1.4, "R": 287.0, "T": 288.15},
            expected=340.2626485525557,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of sqrt(1.4 * 287 * 288.15).",
        ),
    ),
    assumptions=(
        "Thermally perfect gas (p = rho R T); R is the specific gas constant, not the "
        "universal constant.",
        "T is absolute (kelvin); Celsius gives a wrong result.",
    ),
    tags=("speed of sound", "acoustic speed", "a", "compressible flow", "gas dynamics"),
)

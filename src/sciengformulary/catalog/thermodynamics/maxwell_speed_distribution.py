"""Maxwell-Boltzmann Speed Distribution."""

import math

from sciengformulary.catalog._constants import (
    BOLTZMANN_CONSTANT,
    BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    v: float,
    m: float,
    T: float,  # noqa: N803
) -> float:
    thermal_energy = BOLTZMANN_CONSTANT * T
    return (
        4.0 * math.pi * v**2 * (m / (2.0 * math.pi * thermal_energy)) ** 1.5
        * math.exp(-m * v**2 / (2.0 * thermal_energy))
    )


maxwell_speed_distribution = FormulaSpec(
    id="thermodynamics.maxwell_speed_distribution",
    name="Maxwell-Boltzmann Speed Distribution",
    equation="f(v) = 4 pi v^2 (m / (2 pi k_B T))^(3/2) exp(-m v^2 / (2 k_B T))",
    description=(
        "Probability density of molecular speed in a gas at equilibrium; f(v) dv is the fraction "
        "of molecules with speeds between v and v + dv."
    ),
    inputs=(
        VariableSpec(
            name="v",
            symbol="v",
            description="Molecular speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of one molecule",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="f",
        symbol="f(v)",
        description="Probability density per unit speed",
        dimension="L^-1 T",
        si_unit="s/m",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes the prefactor as (4 / sqrt(pi)) (m / 2 k_B T)^(3/2), equal to 4 pi (m /
        # 2 pi k_B T)^(3/2).
        openstax_university_physics(
            2,
            "2-4-distribution-of-molecular-speeds",
            "sec. 2.4, eq. (2.15)",
        ),
        BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v": 500.0, "m": 4.65e-26, "T": 300.0},
            expected=0.0018441496315446217,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation for a nitrogen-like molecule mass at 300 "
                "K and 500 m/s."
            ),
        ),
    ),
    assumptions=(
        "Dilute ideal gas in thermal equilibrium (kinetic theory); T must be absolute.",
        "Gas at rest overall; speeds are relative to the bulk flow.",
    ),
    tags=("Maxwell-Boltzmann", "speed distribution", "kinetic theory", "probability density"),
)

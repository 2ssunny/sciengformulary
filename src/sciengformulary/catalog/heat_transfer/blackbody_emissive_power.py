"""Blackbody Emissive Power (Stefan-Boltzmann Law): q_b = sigma * T^4."""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import (
    lienhard_heat_transfer,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T: float) -> float:  # noqa: N803 - symbols as written in the source
    return STEFAN_BOLTZMANN_CONSTANT * T**4


blackbody_emissive_power = FormulaSpec(
    id="heat_transfer.blackbody_emissive_power",
    name="Blackbody Emissive Power (Stefan-Boltzmann Law)",
    equation="q_b = sigma * T^4",
    description="Total radiant power emitted per unit area by a black surface.",
    inputs=(
        VariableSpec(
            name="T",
            symbol="T",
            description="Absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="q_b",
        symbol="q_b",
        description="Emissive power per unit area",
        dimension="M T^-3",
        si_unit="W/m^2",
    ),
    evaluator=_evaluate,
    references=(
        # The source gives the total power P = sigma A T^4; this is per unit area.
        openstax_university_physics(3, "6-1-blackbody-radiation", "sec. 6.1, eq. (6.4)"),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
        lienhard_heat_transfer("sec. 1.3, eq. (1.28), p. 30"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 300.0},
            expected=459.3003279539388,
            rel_tol=1e-12,
            note=(
                "60-digit evaluation of sigma * 300^4 with sigma = 2 pi^5 k^4 / (15 h^3 c^2) "
                "from the exact SI constants."
            ),
        ),
    ),
    assumptions=(
        "Ideal black surface; real surfaces emit eps times this value.",
        "Absolute temperature.",
    ),
    tags=("Stefan-Boltzmann", "blackbody", "thermal radiation", "emissive power"),
)

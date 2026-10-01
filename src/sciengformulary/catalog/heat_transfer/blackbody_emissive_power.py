"""Blackbody Emissive Power (Stefan-Boltzmann Law): q_b = sigma * T^4."""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import openstax_university_physics
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
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T": 300.0},
            expected=459.300327939,
            rel_tol=1e-12,
            note="Exact arithmetic: 5.670374419e-8 * 300^4.",
        ),
    ),
    assumptions=(
        "Ideal black surface; real surfaces emit eps times this value.",
        "Absolute temperature.",
    ),
    tags=("Stefan-Boltzmann", "blackbody", "thermal radiation", "emissive power"),
)

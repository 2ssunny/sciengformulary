"""Linearised Radiation Heat Transfer Coefficient: h_rad = 4 * eps * sigma * T_m^3."""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(eps: float, T_m: float) -> float:  # noqa: N803 - symbols as written in the source
    return 4.0 * eps * STEFAN_BOLTZMANN_CONSTANT * T_m**3


linearized_radiation_heat_transfer_coefficient = FormulaSpec(
    id="heat_transfer.linearized_radiation_heat_transfer_coefficient",
    name="Linearised Radiation Heat Transfer Coefficient",
    equation="h_rad = 4 * eps * sigma * T_m^3",
    description=(
        "Approximate radiation heat transfer coefficient when the two temperatures are close, "
        "using their mean temperature."
    ),
    inputs=(
        VariableSpec(
            name="eps",
            symbol=r"\varepsilon",
            description="Emittance of the small body",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="T_m",
            symbol="T_m",
            description="Mean absolute temperature (T1 + T2) / 2",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="h_rad",
        symbol="h_{rad}",
        description="Radiation heat transfer coefficient",
        dimension="M T^-3 Theta^-1",
        si_unit="W/(m^2*K)",
    ),
    evaluator=_evaluate,
    references=(
        # The sheet evaluates T at the plate temperature; the source uses the mean temperature.
        lienhard_heat_transfer("sec. 2.3, eq. (2.31)"),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"eps": 0.8, "T_m": 325.0},
            expected=6.228906299474096,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 4 * 0.8 * sigma * 325^3.",
        ),
    ),
    assumptions=(
        "Only when (delta T / T_m)^2 / 4 is much less than 1; otherwise use the exact "
        "radiation coefficient.",
        "Small grey body in large surroundings.",
    ),
    tags=("radiation", "linearised", "heat transfer coefficient", "grey body"),
)

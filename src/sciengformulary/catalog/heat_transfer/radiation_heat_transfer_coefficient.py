"""Radiation Heat Transfer Coefficient: h_rad = eps * sigma * (T1 + T2) * (T1^2 + T2^2)."""

from sciengformulary.catalog._constants import (
    STEFAN_BOLTZMANN_CONSTANT,
    STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
)
from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    eps: float,
    T1: float,  # noqa: N803
    T2: float,  # noqa: N803
) -> float:
    return eps * STEFAN_BOLTZMANN_CONSTANT * (T1 + T2) * (T1**2 + T2**2)


radiation_heat_transfer_coefficient = FormulaSpec(
    id="heat_transfer.radiation_heat_transfer_coefficient",
    name="Radiation Heat Transfer Coefficient",
    equation="h_rad = eps * sigma * (T1 + T2) * (T1^2 + T2^2)",
    description=(
        "Coefficient that writes net radiation between a small grey body and large surroundings as "
        "h_rad (T1 - T2), like convection."
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
            name="T1",
            symbol="T_1",
            description="Absolute temperature of the body",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T_2",
            description="Absolute temperature of the surroundings",
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
        # Eq. (2.28) factorises T1^4 - T2^4 with transfer factor F_1-2; eq. (1.35) gives F_1-2 =
        # eps for a small body in large surroundings.
        lienhard_heat_transfer("sec. 2.3, eq. (2.28); sec. 1.3, eq. (1.35)"),
        STEFAN_BOLTZMANN_CONSTANT_REFERENCE,
    ),
    verification_cases=(
        VerificationCase(
            inputs={"eps": 0.8, "T1": 350.0, "T2": 300.0},
            expected=6.265763732995,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation.",
        ),
    ),
    assumptions=(
        "Grey, diffuse small body in large isothermal surroundings (black-like enclosure).",
        "Absolute temperatures; non-participating medium between them.",
    ),
    tags=("radiation", "heat transfer coefficient", "grey body", "Stefan-Boltzmann"),
)

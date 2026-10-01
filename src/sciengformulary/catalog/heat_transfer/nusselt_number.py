"""Nusselt Number: Nu = h * L / k."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    h: float,
    L: float,  # noqa: N803
    k: float,
) -> float:
    return h * L / k


nusselt_number = FormulaSpec(
    id="heat_transfer.nusselt_number",
    name="Nusselt Number",
    equation="Nu = h * L / k",
    description="Dimensionless convective heat transfer coefficient.",
    inputs=(
        VariableSpec(
            name="h",
            symbol="h",
            description="Convective heat transfer coefficient",
            dimension="M T^-3 Theta^-1",
            si_unit="W/(m^2*K)",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description="Characteristic length used by the correlation",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Thermal conductivity of the fluid",
            dimension="M L T^-3 Theta^-1",
            si_unit="W/(m*K)",
        ),
    ),
    output=VariableSpec(
        name="Nu",
        symbol="Nu",
        description="Nusselt number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 1.3; sec. 8.1, eq. (8.9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"h": 50.0, "L": 0.5, "k": 0.025},
            expected=1000.0,
            rel_tol=1e-12,
            note="Hand calculation: 50 * 0.5 / 0.025 = 1000.",
        ),
    ),
    assumptions=(
        "k is the fluid's conductivity (the Biot number uses the solid's).",
        "L must match the correlation being used (diameter, plate length, x).",
    ),
    tags=("Nusselt number", "dimensionless group", "convection"),
)

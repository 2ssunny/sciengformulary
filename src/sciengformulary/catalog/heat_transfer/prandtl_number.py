"""Prandtl Number: Pr = c_p * mu / k."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c_p: float, mu: float, k: float) -> float:
    return c_p * mu / k


prandtl_number = FormulaSpec(
    id="heat_transfer.prandtl_number",
    name="Prandtl Number",
    equation="Pr = c_p * mu / k",
    description=(
        "Ratio of momentum diffusivity to thermal diffusivity of a fluid; a fluid property."
    ),
    inputs=(
        VariableSpec(
            name="c_p",
            symbol="c_p",
            description="Specific heat at constant pressure",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
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
        name="Pr",
        symbol="Pr",
        description="Prandtl number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source also writes it as nu / alpha.
        lienhard_heat_transfer("App. C, nomenclature"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c_p": 1007.0, "mu": 1.846e-05, "k": 0.02625},
            expected=0.708160761904762,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation (air near 300 K gives about 0.71).",
        ),
    ),
    assumptions=(
        "All three properties at the same temperature.",
    ),
    tags=("Prandtl number", "dimensionless group", "fluid property", "convection"),
)

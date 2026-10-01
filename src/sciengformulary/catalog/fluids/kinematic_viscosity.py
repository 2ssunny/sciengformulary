"""Kinematic Viscosity: nu = mu / rho."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, rho: float) -> float:
    return mu / rho


kinematic_viscosity = FormulaSpec(
    id="fluids.kinematic_viscosity",
    name="Kinematic Viscosity",
    equation="nu = mu / rho",
    description="Dynamic viscosity divided by density: the diffusivity of momentum.",
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity of the fluid",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Fluid density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
    ),
    output=VariableSpec(
        name="nu",
        symbol=r"\nu",
        description="Kinematic viscosity",
        dimension="L^2 T^-1",
        si_unit="m^2/s",
    ),
    evaluator=_evaluate,
    references=(
        lienhard_heat_transfer("sec. 6.2; App. C nomenclature"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 1.81e-05, "rho": 1.204},
            expected=1.5033222591362126e-05,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1.81e-5 / 1.204.",
        ),
    ),
    assumptions=(
        "mu and rho at the same temperature and pressure.",
    ),
    tags=("kinematic viscosity", "nu", "momentum diffusivity", "viscosity"),
)

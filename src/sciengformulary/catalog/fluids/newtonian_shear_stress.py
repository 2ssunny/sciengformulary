"""Newtonian Shear Stress: tau = mu * du/dy."""

from sciengformulary.catalog._sources import lienhard_heat_transfer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(mu: float, dudy: float) -> float:
    return mu * dudy


newtonian_shear_stress = FormulaSpec(
    id="fluids.newtonian_shear_stress",
    name="Newtonian Shear Stress",
    equation="tau = mu * du/dy",
    description=(
        "Viscous shear stress in a Newtonian fluid, proportional to the velocity gradient normal "
        "to the flow direction."
    ),
    inputs=(
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity of the fluid",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
        VariableSpec(
            name="dudy",
            symbol=r"\partial u/\partial y",
            description="Gradient of the flow-direction velocity normal to the surface or layer",
            dimension="T^-1",
            si_unit="1/s",
        ),
    ),
    output=VariableSpec(
        name="tau",
        symbol=r"\tau",
        description="Shear stress on planes normal to y",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        # The source states Newton's law of viscous shear at a wall, tau_w = mu du/dy at y = 0.
        lienhard_heat_transfer("sec. 6.2"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"mu": 1.8e-05, "dudy": 1000.0},
            expected=0.018,
            rel_tol=1e-12,
            note="Hand calculation: 1.8e-5 * 1000 = 0.018 Pa.",
        ),
    ),
    assumptions=(
        "Newtonian fluid: viscosity independent of shear rate (air, water; not paints, blood "
        "or polymer melts).",
        "Simple shear flow in which u varies only with y; general flows need the full "
        "strain-rate tensor.",
    ),
    tags=("viscosity", "shear stress", "Newtonian fluid", "wall shear"),
)

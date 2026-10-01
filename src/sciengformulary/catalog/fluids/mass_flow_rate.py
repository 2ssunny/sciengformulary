"""Mass Flow Rate: mdot = rho * V * A."""

from sciengformulary.catalog._sources import nasa_glenn, openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho: float,
    V: float,  # noqa: N803
    A: float,  # noqa: N803
) -> float:
    return rho * V * A


mass_flow_rate = FormulaSpec(
    id="fluids.mass_flow_rate",
    name="Mass Flow Rate",
    equation="mdot = rho * V * A",
    description="Mass of fluid crossing a section per unit time for a uniform flow.",
    inputs=(
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Fluid density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Flow velocity normal to the section",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="A",
            symbol="A",
            description="Flow cross-sectional area",
            dimension="L^2",
            si_unit="m^2",
        ),
    ),
    output=VariableSpec(
        name="mdot",
        symbol=r"\dot{m}",
        description="Mass flow rate",
        dimension="M T^-1",
        si_unit="kg/s",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Mass Flow Rate", "mass-flow-rate", 2024),
        openstax_university_physics(1, "14-5-fluid-dynamics", "sec. 14.5, eq. (14.15)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 1.225, "V": 20.0, "A": 0.5},
            expected=12.25,
            rel_tol=1e-12,
            note="Hand calculation: 1.225 * 20 * 0.5 = 12.25 kg/s.",
        ),
    ),
    assumptions=(
        "Density and velocity uniform over the section (or V taken as the area-mean speed and "
        "rho as its matching mean); V is the component normal to A.",
        "In steady flow with no other inlets or outlets, mdot is the same at every section "
        "(continuity).",
    ),
    tags=("mass flow", "continuity", "mdot", "flow rate"),
)

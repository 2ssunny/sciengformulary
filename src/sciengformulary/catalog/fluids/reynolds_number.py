"""Reynolds Number: Re = rho * V * L / mu."""

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    rho: float,
    V: float,  # noqa: N803
    L: float,  # noqa: N803
    mu: float,
) -> float:
    return rho * V * L / mu


reynolds_number = FormulaSpec(
    id="fluids.reynolds_number",
    name="Reynolds Number",
    equation="Re = rho * V * L / mu",
    description=(
        "Ratio of inertial to viscous forces in a flow. Its value, with a stated length scale, "
        "indicates whether flow is likely laminar or turbulent."
    ),
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
            description="Characteristic flow speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="L",
            symbol="L",
            description=(
                "Characteristic length (chord, diameter, distance from a leading edge, ...)"
            ),
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="mu",
            symbol=r"\mu",
            description="Dynamic viscosity of the fluid",
            dimension="M L^-1 T^-1",
            si_unit="Pa*s",
        ),
    ),
    output=VariableSpec(
        name="Re",
        symbol="Re",
        description="Reynolds number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Similarity Parameters", "similarity-parameters", 2024),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"rho": 1.225, "V": 10.0, "L": 2.0, "mu": 1.8e-05},
            expected=1361111.111111111,
            rel_tol=1e-12,
            note="Independent 40-digit decimal evaluation of 1.225 * 10 * 2 / 1.8e-5.",
        ),
    ),
    assumptions=(
        "The length scale must be the one used by whatever correlation or transition criterion "
        "the value is compared with (pipe diameter, plate distance x, chord).",
        "Transition thresholds are not universal; they depend on geometry and disturbance level.",
    ),
    tags=("Reynolds number", "Re", "similarity", "laminar", "turbulent"),
)

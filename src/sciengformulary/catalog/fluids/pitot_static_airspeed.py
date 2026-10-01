"""Pitot-Static Airspeed: V = sqrt(2 * (p_t - p_s) / rho)."""

import math

from sciengformulary.catalog._sources import nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(p_t: float, p_s: float, rho: float) -> float:
    return math.sqrt(2.0 * (p_t - p_s) / rho)


pitot_static_airspeed = FormulaSpec(
    id="fluids.pitot_static_airspeed",
    name="Pitot-Static Airspeed",
    equation="V = sqrt(2 * (p_t - p_s) / rho)",
    description=(
        "Flow speed inferred from the difference between total and static pressure measured by a "
        "Pitot-static probe."
    ),
    inputs=(
        VariableSpec(
            name="p_t",
            symbol="p_t",
            description="Total (stagnation) pressure sensed by the forward port",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
        VariableSpec(
            name="p_s",
            symbol="p_s",
            description="Static pressure sensed by the side ports",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
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
        name="V",
        symbol="V",
        description="Flow speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Pitot - Static Tube - Speedometer", "pitot-static-tube-speedometer", 2025),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"p_t": 101825.0, "p_s": 101325.0, "rho": 1.225},
            expected=28.571428571428573,
            rel_tol=1e-12,
            note="Hand calculation: sqrt(2 * 500 / 1.225) = sqrt(816.33) = 28.571 m/s.",
        ),
    ),
    assumptions=(
        "Steady, incompressible, inviscid flow along a streamline (Bernoulli); at high "
        "subsonic and supersonic speeds compressibility makes it inaccurate.",
        "rho is the density of the fluid at the measurement point.",
        "p_t must not be less than p_s.",
    ),
    tags=("pitot tube", "airspeed", "Bernoulli", "dynamic pressure", "velocity measurement"),
)

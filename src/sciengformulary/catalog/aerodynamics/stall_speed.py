"""Stall Speed in Steady Level Flight: V_s = sqrt(2 * W / (rho * S * CL_max))."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    W: float,  # noqa: N803
    rho: float,
    S: float,  # noqa: N803
    CL_max: float,  # noqa: N803
) -> float:
    positive("W", W)
    positive("rho", rho)
    positive("S", S)
    positive("CL_max", CL_max)
    return finite_result(math.sqrt(2.0 * W / (rho * S * CL_max)))


stall_speed = FormulaSpec(
    id="aerodynamics.stall_speed",
    name="Stall Speed in Steady Level Flight",
    equation="V_s = sqrt(2 * W / (rho * S * CL_max))",
    description=(
        "Lowest speed of steady, level, unaccelerated flight at which the lift equation can "
        "carry the weight, reached when the lift coefficient is at its maximum value. It is "
        "aerodynamics.lift_force solved for the speed with the lift set equal to the weight "
        "and the lift coefficient set to C_L,max."
    ),
    inputs=(
        VariableSpec(
            name="W",
            symbol="W",
            description="Aircraft weight",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Air density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="S",
            symbol="S",
            description="Wing reference area on which C_L,max is based",
            dimension="L^2",
            si_unit="m^2",
        ),
        VariableSpec(
            name="CL_max",
            symbol="C_{L,max}",
            description="Maximum lift coefficient (depends on the configuration)",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="V_s",
        symbol="V_s",
        description="Stall speed in 1 g level flight",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the lift equation L = C_L (rho V^2 / 2) A with A the wing area S, and the
        # small-angle vertical equation L - W = m a_v, which gives L = W when a_v = 0. Setting
        # L = W and C_L = CL_max and solving for V gives the shipped form. The two pages define
        # neither "stall speed" nor C_L,max; stall speed is taken here to be the 1 g speed at
        # C_L,max, which is a convention of this formula and not a statement of the sources.
        nasa_glenn(
            "Lift Equation",
            "lift-equation",
            2024,
            "Lift Equation",
            accessed=ENGINEERING_ACCESSED,
        ),
        nasa_glenn(
            "Forces in a Climb",
            "forces-in-a-climb",
            2024,
            "small-angle reduction",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"W": 10000.0, "rho": 1.225, "S": 16.2, "CL_max": 1.6},
            expected=25.097441747368087,
            rel_tol=1e-11,
            note=(
                "Light aircraft at sea level; mpmath root of C_L,max (rho V^2 / 2) S = W "
                "taken from the lift equation."
            ),
        ),
        VerificationCase(
            inputs={"W": 60000.0, "rho": 0.9093, "S": 30.0, "CL_max": 2.2},
            expected=44.71621748063751,
            rel_tol=1e-11,
            note="Air density at about 3000 m with flaps; same mpmath root of L(V) = W.",
        ),
        VerificationCase(
            inputs={"W": 1.0, "rho": 1.0, "S": 1.0, "CL_max": 1.0},
            expected=1.4142135623730951,
            rel_tol=1e-11,
            note="Boundary case with unit values: V_s = sqrt(2).",
        ),
    ),
    assumptions=(
        "Derived result: in steady level flight L = W (the printed component equations with "
        "zero acceleration); the lift equation L = C_L (rho V^2 / 2) S evaluated at C_L = "
        "C_L,max gives the shipped V_s.",
        "Convention of this formula: stall speed is the 1 g speed at maximum lift coefficient. "
        "The cited NASA pages do not define stall speed or give a C_L,max, so this definition "
        "is an assumption, not a statement of the sources.",
        "Load factor 1, subsonic flight; the vertical component of thrust and any pitch angle "
        "are ignored. C_L,max depends on configuration (flaps, slats) and must be supplied.",
        "Any consistent unit system works; SI is documented.",
    ),
    tags=("stall", "flight performance", "lift equation", "level flight"),
)

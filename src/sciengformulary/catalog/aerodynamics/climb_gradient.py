"""Small-Angle Climb Gradient of a Steady Climb."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T_W: float, L_D: float) -> float:  # noqa: N803
    non_negative("T_W", T_W)
    positive("L_D", L_D)
    return finite_result(T_W - 1.0 / L_D)


climb_gradient = FormulaSpec(
    id="aerodynamics.climb_gradient",
    name="Small-Angle Climb Gradient of a Steady Climb",
    equation="gamma = T_W - 1 / L_D",
    description=(
        "Climb flight-path angle, in radians and in the small-angle approximation, of an "
        "aircraft in a steady climb with its thrust along the flight path, from its "
        "thrust-to-weight ratio and its lift-to-drag ratio. The exact angle satisfies "
        "sin(gamma) = T/W - cos(gamma) / (L/D); this is the first-order form and is not exact "
        "for steep climbs."
    ),
    inputs=(
        VariableSpec(
            name="T_W",
            symbol="T/W",
            description="Thrust-to-weight ratio",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="L_D",
            symbol="L/D",
            description="Lift-to-drag ratio at the flight condition",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="gamma",
        symbol=r"\gamma",
        description="Climb flight-path angle, small-angle approximation (negative in a descent)",
        dimension="1",
        si_unit="rad",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the page prints the component equations along the vertical and horizontal
        # axes, F_ex sin c + L cos c - W = m a_v and F_ex cos c - L sin c = m a_h with
        # F_ex = F - D. With zero acceleration they give F_ex = W sin c and L = W cos c, hence
        # sin c = T/W - cos c / (L/D) with D = L / (L/D); sin c ~ c and cos c ~ 1 for small
        # angles give the shipped form. Symbols: c -> gamma, F -> T.
        nasa_glenn(
            "Forces in a Climb",
            "forces-in-a-climb",
            2024,
            "Vertical and horizontal component equations",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T_W": 0.3, "L_D": 12.0},
            expected=0.21666666666666667,
            rel_tol=1e-12,
            note="Hand calculation: 0.3 - 1/12 = 0.2166667 rad (50-digit mpmath check).",
        ),
        VerificationCase(
            inputs={"T_W": 0.1, "L_D": 10.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-15,
            note="Boundary case: thrust equal to drag gives level flight, 0.1 - 0.1 = 0.",
        ),
        VerificationCase(
            inputs={"T_W": 0.0, "L_D": 15.0},
            expected=-0.06666666666666667,
            rel_tol=1e-12,
            note="No thrust: a glide with angle -1/15 rad.",
        ),
    ),
    assumptions=(
        "Derived result: for a steady climb with thrust along the flight path the printed "
        "component equations give sin(gamma) = T/W - cos(gamma) / (L/D); taking sin(gamma) ~ "
        "gamma and cos(gamma) ~ 1 gives gamma = T/W - 1/(L/D).",
        "Small-angle approximation: at gamma near 0.22 rad (T/W = 0.3, L/D = 12) the result is "
        "about 1.7 percent too small (0.2167 rad against the exact 0.2205 rad); the "
        "error grows with the angle. The angle is not checked.",
        "Steady (unaccelerated) flight, thrust aligned with the flight path, no wind. T/W is "
        "not negative; L/D is positive.",
        "The result is the first-order climb angle in radians, not the exact angle.",
    ),
    tags=("climb", "flight path angle", "performance"),
)

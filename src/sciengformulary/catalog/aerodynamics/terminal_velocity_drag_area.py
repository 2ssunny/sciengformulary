"""Drag Area from Terminal Descent: CdS = 2 * m * g / (rho * v_t^2)."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, g: float, rho: float, v_t: float) -> float:
    positive("m", m)
    positive("g", g)
    positive("rho", rho)
    positive("v_t", v_t)
    return finite_result(2.0 * m * g / (rho * v_t**2))


terminal_velocity_drag_area = FormulaSpec(
    id="aerodynamics.terminal_velocity_drag_area",
    name="Drag Area from Terminal Descent",
    equation="CdS = 2 * m * g / (rho * v_t^2)",
    description=(
        "Drag area, the drag coefficient times the reference area, of a body that falls at a "
        "constant speed, found by setting its drag equal to its weight. It is "
        "aerodynamics.drag_force rearranged for C_d S at D = m g, and it needs no separate "
        "drag coefficient or area."
    ),
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the falling body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="g",
            symbol="g",
            description="Gravitational acceleration",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="rho",
            symbol=r"\rho",
            description="Air density",
            dimension="M L^-3",
            si_unit="kg/m^3",
        ),
        VariableSpec(
            name="v_t",
            symbol="v_t",
            description="Terminal (steady descent) speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="CdS",
        symbol="C_d S",
        description="Drag area, drag coefficient times reference area",
        dimension="L^2",
        si_unit="m^2",
    ),
    evaluator=_evaluate,
    references=(
        # Derived: the page sets D = W with D = C_d rho V^2 A / 2 and solves for the speed,
        # V = sqrt(2 W / (C_d rho A)). Solving the same balance for C_d A with W = m g gives the
        # shipped form. Symbols: V -> v_t, A -> S.
        nasa_glenn(
            "Terminal Velocity Interactive",
            "termvel",
            2024,
            "Terminal Velocity Interactive",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 10.0, "g": 9.80665, "rho": 1.225, "v_t": 5.0},
            expected=6.404342857142856,
            rel_tol=1e-11,
            note="10 kg at 5 m/s; mpmath root of C_d S rho v^2 / 2 = m g (drag equation).",
        ),
        VerificationCase(
            inputs={"m": 1.0, "g": 9.80665, "rho": 1.225, "v_t": 6.0},
            expected=0.44474603174603167,
            rel_tol=1e-11,
            note="1 kg at 6 m/s; same mpmath root of the drag-weight balance.",
        ),
        VerificationCase(
            inputs={"m": 80.0, "g": 9.80665, "rho": 1.0, "v_t": 1.0},
            expected=1569.0639999999999,
            rel_tol=1e-11,
            note="Boundary case with unit speed and density: 2 * 80 * 9.80665 = 1569.064.",
        ),
    ),
    assumptions=(
        "Derived result: the printed drag equation D = C_d rho V^2 A / 2 with D = W = m g "
        "solved for C_d A gives CdS = 2 m g / (rho v_t^2).",
        "Steady vertical descent with drag equal to weight; buoyancy and added mass are "
        "neglected and the density is constant along the fall.",
        "Any consistent unit system works; SI is documented, with CdS in square metres.",
    ),
    tags=("terminal velocity", "drag area", "parachute", "drag equation"),
)

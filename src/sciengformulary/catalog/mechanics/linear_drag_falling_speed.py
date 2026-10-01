"""Falling Speed with Linear Drag: v = (m * g / c) * (1 - exp(-c * t / m))."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, g: float, c: float, t: float) -> float:
    return m * g / c * (1.0 - math.exp(-c * t / m))


linear_drag_falling_speed = FormulaSpec(
    id="mechanics.linear_drag_falling_speed",
    name="Falling Speed with Linear Drag",
    equation="v = (m * g / c) * (1 - exp(-c * t / m))",
    description=(
        "Downward speed of a body released from rest under gravity when air resistance is "
        "proportional to speed; it approaches the terminal speed m g / c."
    ),
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="g",
            symbol="g",
            description="Local gravitational acceleration (about 9.81 m/s^2 near Earth's surface)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Linear drag coefficient (drag force = c times speed)",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
        VariableSpec(
            name="t",
            symbol="t",
            description="Elapsed time since t = 0",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="v",
        symbol="v",
        description="Downward speed at time t",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Derived in the section text with drag coefficient b: v = (m g / b)(1 - e^(-b t / m)).
        openstax_university_physics(1, "6-4-drag-force-and-terminal-speed", "sec. 6.4"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 80.0, "g": 9.81, "c": 12.5, "t": 6.4},
            expected=39.68705716549216,
            rel_tol=1e-12,
            note=(
                "Independent 40-digit decimal evaluation; t = m / c, so v = (80 * 9.81 / 12.5)(1 - "
                "1/e)."
            ),
        ),
        VerificationCase(
            inputs={"m": 80.0, "g": 9.81, "c": 12.5, "t": 0.0},
            expected=0.0,
            abs_tol=1e-12,
            note="Released from rest: v = 0 at t = 0.",
        ),
    ),
    assumptions=(
        "Drag force proportional to speed. This holds for slow, small or viscous-dominated "
        "motion; most falling bodies in air have drag closer to proportional to speed squared.",
        "Starts from rest at t = 0; constant m, g and c.",
    ),
    tags=("terminal velocity", "linear drag", "falling body", "air resistance", "parachute"),
)

"""Damped Angular Frequency: omega_d = sqrt(k / m - (b / (2 * m))^2)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, m: float, b: float) -> float:
    return math.sqrt(k / m - (b / (2.0 * m)) ** 2)


damped_angular_frequency = FormulaSpec(
    id="mechanics.damped_angular_frequency",
    name="Damped Angular Frequency",
    equation="omega_d = sqrt(k / m - (b / (2 * m))^2)",
    description=(
        "Angular frequency of free oscillation of an underdamped mass-spring-damper; slightly "
        "below the undamped natural frequency."
    ),
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Linear spring stiffness",
            dimension="M T^-2",
            si_unit="N/m",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Viscous damping coefficient (damping force = -b times velocity)",
            dimension="M T^-1",
            si_unit="kg/s",
        ),
    ),
    output=VariableSpec(
        name="omega_d",
        symbol=r"\omega_d",
        description="Damped angular frequency",
        dimension="T^-1",
        si_unit="rad/s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes omega = sqrt(omega_0^2 - (b/2m)^2). With damping ratio zeta = b / (2 m
        # omega_0) this equals the sheet's omega_n sqrt(1 - zeta^2).
        openstax_university_physics(1, "15-5-damped-oscillations", "sec. 15.5, eq. (15.26)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 200.0, "m": 2.0, "b": 8.0},
            expected=9.797958971132712,
            rel_tol=1e-12,
            note="Hand calculation: sqrt(100 - (8/4)^2) = sqrt(96).",
        ),
    ),
    assumptions=(
        "Single-degree-of-freedom mass-spring-damper with linear spring and viscous damping; "
        "the damping force is proportional to velocity.",
        "Underdamped only: b must be below the critical value 2 sqrt(k m); at or above it "
        "there is no oscillation and the square root is invalid.",
    ),
    tags=("damped vibration", "damped frequency", "underdamped", "oscillation"),
)

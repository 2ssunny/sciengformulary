"""Critical Damping Coefficient: c_c = 2 * sqrt(k * m)."""

import math

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k: float, m: float) -> float:
    return 2.0 * math.sqrt(k * m)


critical_damping_coefficient = FormulaSpec(
    id="mechanics.critical_damping_coefficient",
    name="Critical Damping Coefficient",
    equation="c_c = 2 * sqrt(k * m)",
    description=(
        "Viscous damping coefficient at which a mass-spring system returns to equilibrium fastest "
        "without oscillating."
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
    ),
    output=VariableSpec(
        name="c_c",
        symbol="c_c",
        description="Critical damping coefficient",
        dimension="M T^-1",
        si_unit="kg/s",
    ),
    evaluator=_evaluate,
    references=(
        # The section text gives critical damping at b = sqrt(4 m k) = 2 sqrt(k m).
        openstax_university_physics(1, "15-5-damped-oscillations", "sec. 15.5"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 200.0, "m": 2.0},
            expected=40.0,
            rel_tol=1e-12,
            note="Hand calculation: 2 * sqrt(200 * 2) = 40 kg/s.",
        ),
    ),
    assumptions=(
        "Single-degree-of-freedom mass-spring-damper with linear spring and viscous damping; "
        "the damping force is proportional to velocity.",
        "Damping below c_c gives decaying oscillation (underdamped); above it, slow "
        "non-oscillatory return (overdamped).",
    ),
    tags=("critical damping", "damping", "vibration", "overdamped", "underdamped"),
)

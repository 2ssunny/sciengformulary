"""Weight: W = m * g."""

from sciengformulary.catalog._sources import (
    ACCESSED_AUDIT,
    doe_fundamentals_handbook,
    nasa_glenn,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, g: float) -> float:
    return m * g


weight = FormulaSpec(
    id="mechanics.weight",
    name="Weight",
    equation="W = m * g",
    description="Gravitational force on a body of mass m near a planet's surface.",
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
    ),
    output=VariableSpec(
        name="W",
        symbol="W",
        description="Weight (magnitude of the gravitational force)",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(1, "5-4-mass-and-weight", "sec. 5.4, eq. (5.9)"),
        # The handbook writes W = m g / g_c with g_c = 1 in SI.
        doe_fundamentals_handbook(
            "DOE-HDBK-1010-92",
            "Module 4 'Application of Newton's Laws', Force and Weight, eq. (4-2), p. 2 (CP-04)",
        ),
        nasa_glenn(
            "Free Falling Objects",
            "free-falling-objects",
            2023,
            "Falling through Vacuum, weight equation",
            accessed=ACCESSED_AUDIT,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 1.0, "g": 9.8},
            expected=9.8,
            rel_tol=1e-12,
            note="Worked example in the cited section: w = 1.00 kg * 9.80 m/s^2 = 9.80 N.",
        ),
    ),
    assumptions=(
        "g is the local gravitational acceleration, which varies with location and altitude. "
        "Far from a planet's surface use Newton's law of gravitation.",
    ),
    tags=("weight", "gravity", "mass", "force"),
)

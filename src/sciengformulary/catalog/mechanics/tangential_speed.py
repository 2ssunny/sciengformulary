"""Tangential Speed in Rotation: v_t = r * omega."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float, omega: float) -> float:
    return r * omega


tangential_speed = FormulaSpec(
    id="mechanics.tangential_speed",
    name="Tangential Speed in Rotation",
    equation="v_t = r * omega",
    description="Speed of a point at radius r on a body rotating at angular speed omega.",
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description="Distance from the rotation axis",
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="omega",
            symbol=r"\omega",
            description="Angular speed",
            dimension="T^-1",
            si_unit="rad/s",
        ),
    ),
    output=VariableSpec(
        name="v_t",
        symbol="v_t",
        description="Tangential speed",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        # Stated in the section text as v_t = r omega.
        openstax_university_physics(
            1,
            "10-3-relating-angular-and-translational-quantities",
            "sec. 10.3",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 0.2, "omega": 35.0},
            expected=7.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.2 * 35 = 7.0 m/s.",
        ),
    ),
    assumptions=(
        "omega in radians per second (not rpm or degrees per second).",
        "Rotation about a fixed axis; r is the perpendicular distance to that axis.",
    ),
    tags=("rotation", "tangential speed", "angular velocity", "circular motion"),
)

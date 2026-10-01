"""Speed Squared Under Constant Acceleration: v^2 = v0^2 + 2 * a * (x - x0)."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(v0: float, a: float, displacement: float) -> float:
    return v0**2 + 2.0 * a * displacement


constant_acceleration_speed_squared = FormulaSpec(
    id="mechanics.constant_acceleration_speed_squared",
    name="Speed Squared Under Constant Acceleration",
    equation="v^2 = v0^2 + 2 * a * (x - x0)",
    description=(
        "Square of the velocity after a displacement, for straight-line motion with constant "
        "acceleration (time eliminated)."
    ),
    inputs=(
        VariableSpec(
            name="v0",
            symbol="v_0",
            description="Velocity at t = 0 (signed, along the line of motion)",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="a",
            symbol="a",
            description="Constant acceleration (signed, along the line of motion)",
            dimension="L T^-2",
            si_unit="m/s^2",
        ),
        VariableSpec(
            name="displacement",
            symbol="x - x_0",
            description="Displacement x - x0 along the line of motion (signed)",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="v_squared",
        symbol="v^2",
        description="Square of the velocity at the end of the displacement",
        dimension="L^2 T^-2",
        si_unit="m^2/s^2",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "3-4-motion-with-constant-acceleration",
            "sec. 3.4, eq. (3.14)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v0": 0.0, "a": 26.0, "displacement": 402.0},
            expected=20904.0,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: 0 + 2 * 26.0 * 402 = 2.09e4 m^2/s^2 (exactly "
                "20904 before rounding)."
            ),
        ),
    ),
    assumptions=(
        "Straight-line motion with constant acceleration over the whole interval; for varying "
        "acceleration integrate a(t) instead.",
        "Returns v^2; the sign of v must come from the physical situation. A negative result "
        "means the displacement is not reachable.",
    ),
    tags=("kinematics", "constant acceleration", "SUVAT", "speed"),
)

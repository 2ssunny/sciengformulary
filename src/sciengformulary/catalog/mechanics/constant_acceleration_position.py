"""Position Under Constant Acceleration: x = x0 + v0 * t + a * t^2 / 2."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(x0: float, v0: float, a: float, t: float) -> float:
    return x0 + v0 * t + 0.5 * a * t**2


constant_acceleration_position = FormulaSpec(
    id="mechanics.constant_acceleration_position",
    name="Position Under Constant Acceleration",
    equation="x = x0 + v0 * t + a * t^2 / 2",
    description="Position after time t for straight-line motion with constant acceleration.",
    inputs=(
        VariableSpec(
            name="x0",
            symbol="x_0",
            description="Position at t = 0",
            dimension="L",
            si_unit="m",
        ),
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
            name="t",
            symbol="t",
            description="Elapsed time since t = 0",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="x",
        symbol="x",
        description="Position at time t",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "3-4-motion-with-constant-acceleration",
            "sec. 3.4, eq. (3.13)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x0": 2.0, "v0": 3.0, "a": 4.0, "t": 5.0},
            expected=67.0,
            rel_tol=1e-12,
            note="Hand calculation: 2 + 3 * 5 + 4 * 25 / 2 = 67 m.",
        ),
    ),
    assumptions=(
        "Straight-line motion with constant acceleration over the whole interval; for varying "
        "acceleration integrate a(t) instead.",
        "For projectiles use it separately for each axis (a = -g vertically, a = 0 "
        "horizontally) when air resistance is negligible.",
    ),
    tags=("kinematics", "constant acceleration", "SUVAT", "displacement", "projectile"),
)

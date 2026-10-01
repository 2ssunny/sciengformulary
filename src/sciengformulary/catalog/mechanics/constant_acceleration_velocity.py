"""Velocity Under Constant Acceleration: v = v0 + a * t."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(v0: float, a: float, t: float) -> float:
    return v0 + a * t


constant_acceleration_velocity = FormulaSpec(
    id="mechanics.constant_acceleration_velocity",
    name="Velocity Under Constant Acceleration",
    equation="v = v0 + a * t",
    description="Velocity after time t for straight-line motion with constant acceleration.",
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
        description="Velocity at time t (signed)",
        dimension="L T^-1",
        si_unit="m/s",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "3-4-motion-with-constant-acceleration",
            "sec. 3.4, eq. (3.12)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v0": 70.0, "a": -1.5, "t": 40.0},
            expected=10.0,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: 70.0 m/s + (-1.50 m/s^2)(40.0 s) = 10.0 m/s."
            ),
        ),
    ),
    assumptions=(
        "Straight-line motion with constant acceleration over the whole interval; for varying "
        "acceleration integrate a(t) instead.",
    ),
    tags=("kinematics", "constant acceleration", "SUVAT", "velocity"),
)

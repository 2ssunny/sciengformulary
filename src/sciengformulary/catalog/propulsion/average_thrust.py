"""Average Thrust from Total Impulse: F_avg = I_t / t_b."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(I_t: float, t_b: float) -> float:  # noqa: N803 - symbols as in the source
    positive("I_t", I_t)
    positive("t_b", t_b)
    return finite_result(I_t / t_b)


average_thrust = FormulaSpec(
    id="propulsion.average_thrust",
    name="Average Thrust from Total Impulse",
    equation="F_avg = I_t / t_b",
    description=(
        "Time-averaged thrust of a rocket firing from its total impulse and burn time. It is "
        "a property of the whole burn; the instantaneous thrust of an engine at one operating "
        "point is given by propulsion.rocket_thrust."
    ),
    inputs=(
        VariableSpec(
            name="I_t",
            symbol="I",
            description="Total impulse of the burn",
            dimension="M L T^-1",
            si_unit="N s",
        ),
        VariableSpec(
            name="t_b",
            symbol=r"\Delta t",
            description="Burn time (total firing time)",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="F_avg",
        symbol="F_{avg}",
        description="Average thrust over the burn",
        dimension="M L T^-2",
        si_unit="N",
    ),
    evaluator=_evaluate,
    references=(
        # Stated: the page defines total impulse as average thrust times total firing time,
        # I = F * delta_t; solved here for the average thrust F.
        nasa_glenn(
            "Specific Impulse",
            "specific-impulse",
            2024,
            locator="Specific Impulse",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I_t": 10000.0, "t_b": 5.0},
            expected=2000.0,
            rel_tol=1e-12,
            note="Hand calculation: 10 000 N s / 5 s = 2000 N.",
        ),
        VerificationCase(
            inputs={"I_t": 2000000.0, "t_b": 80.0},
            expected=25000.0,
            rel_tol=1e-12,
            note="Hand calculation: 2e6 / 80 = 25 000 N (large motor).",
        ),
        VerificationCase(
            inputs={"I_t": 1.0, "t_b": 0.001},
            expected=1000.0,
            rel_tol=1e-12,
            note="Edge case, very short burn: 1 / 0.001 = 1000 N.",
        ),
    ),
    assumptions=(
        "The average is taken over the whole burn time and holds for any thrust history.",
        "I_t and t_b must be positive and refer to the same burn.",
    ),
    tags=("average thrust", "total impulse", "rocket motor", "propulsion"),
)

"""Impulse of a Constant Force: J = F * delta_t."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(F: float, delta_t: float) -> float:  # noqa: N803 - symbols as written in the source
    return F * delta_t


impulse_of_constant_force = FormulaSpec(
    id="mechanics.impulse_of_constant_force",
    name="Impulse of a Constant Force",
    equation="J = F * delta_t",
    description=(
        "Impulse delivered by a force that is constant (or replaced by its time average) over a "
        "time interval; it equals the change in momentum."
    ),
    inputs=(
        VariableSpec(
            name="F",
            symbol="F",
            description="Constant (or time-averaged) force component",
            dimension="M L T^-2",
            si_unit="N",
        ),
        VariableSpec(
            name="delta_t",
            symbol=r"\Delta t",
            description="Duration over which the force acts",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="J",
        symbol="J",
        description="Impulse component",
        dimension="M L T^-1",
        si_unit="N*s",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes J = F_ave delta_t with F_ave the time-averaged force.
        openstax_university_physics(1, "9-2-impulse-and-collisions", "sec. 9.2, eq. (9.5)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"F": 500.0, "delta_t": 0.2},
            expected=100.0,
            rel_tol=1e-12,
            note="Hand calculation: 500 * 0.2 = 100 N s.",
        ),
    ),
    assumptions=(
        "F is constant over delta_t, or is its time average.",
        "Apply per component for forces in more than one direction.",
    ),
    tags=("impulse", "momentum", "collision", "force"),
)

"""Translational Kinetic Energy: K = m * v^2 / 2."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, v: float) -> float:
    return 0.5 * m * v**2


translational_kinetic_energy = FormulaSpec(
    id="mechanics.translational_kinetic_energy",
    name="Translational Kinetic Energy",
    equation="K = m * v^2 / 2",
    description="Kinetic energy of a mass moving at speed v.",
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="v",
            symbol="v",
            description="Speed",
            dimension="L T^-1",
            si_unit="m/s",
        ),
    ),
    output=VariableSpec(
        name="K",
        symbol="K",
        description="Kinetic energy",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(1, "7-2-kinetic-energy", "sec. 7.2, eq. (7.6)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 75.0, "v": 13.5},
            expected=6834.375,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: 0.5 * 75.0 kg * (13.5 m/s)^2 = 6.83 kJ "
                "(exactly 6834.375 J before rounding)."
            ),
        ),
    ),
    assumptions=(
        "Non-relativistic speed (v much less than the speed of light).",
        "For a rigid body this is the energy of its centre-of-mass motion only; add the "
        "rotational part separately.",
    ),
    tags=("kinetic energy", "energy", "work-energy"),
)

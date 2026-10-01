"""Rotational Kinetic Energy: K = I * omega^2 / 2."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    I: float,  # noqa: N803, E741
    omega: float,
) -> float:
    return 0.5 * I * omega**2


rotational_kinetic_energy = FormulaSpec(
    id="mechanics.rotational_kinetic_energy",
    name="Rotational Kinetic Energy",
    equation="K = I * omega^2 / 2",
    description="Kinetic energy of a rigid body rotating about a fixed axis.",
    inputs=(
        VariableSpec(
            name="I",
            symbol="I",
            description="Moment of inertia about the rotation axis",
            dimension="M L^2",
            si_unit="kg*m^2",
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
        name="K",
        symbol="K",
        description="Rotational kinetic energy",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "10-4-moment-of-inertia-and-rotational-kinetic-energy",
            "sec. 10.4, eq. (10.18)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I": 1067.0, "omega": 31.4},
            expected=526009.66,
            rel_tol=1e-12,
            note=(
                "Worked example in the cited section: 0.5 * 1067 kg m^2 * (31.4 rad/s)^2 = 5.26e5 "
                "J (526009.66 J before rounding)."
            ),
        ),
    ),
    assumptions=(
        "omega in rad/s.",
        "For rolling or general motion, add the translational kinetic energy of the centre of "
        "mass and use I about the centre of mass.",
    ),
    tags=("rotational energy", "kinetic energy", "flywheel", "rigid body"),
)

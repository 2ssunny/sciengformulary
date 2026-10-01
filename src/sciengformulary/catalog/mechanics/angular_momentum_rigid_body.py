"""Angular Momentum of a Rotating Rigid Body: L = I * omega."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    I: float,  # noqa: N803, E741
    omega: float,
) -> float:
    return I * omega


angular_momentum_rigid_body = FormulaSpec(
    id="mechanics.angular_momentum_rigid_body",
    name="Angular Momentum of a Rotating Rigid Body",
    equation="L = I * omega",
    description="Angular momentum of a rigid body spinning about a fixed axis.",
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
            description="Angular speed about that axis",
            dimension="T^-1",
            si_unit="rad/s",
        ),
    ),
    output=VariableSpec(
        name="L",
        symbol="L",
        description="Angular momentum about the axis",
        dimension="M L^2 T^-1",
        si_unit="kg*m^2/s",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(1, "11-2-angular-momentum", "sec. 11.2, eq. (11.9)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I": 2.5, "omega": 4.0},
            expected=10.0,
            rel_tol=1e-12,
            note="Hand calculation: 2.5 * 4 = 10 kg m^2/s.",
        ),
    ),
    assumptions=(
        "Rotation about a fixed axis (or a principal axis through the centre of mass); "
        "otherwise angular momentum and angular velocity need not be parallel.",
    ),
    tags=("angular momentum", "rotation", "rigid body", "spin"),
)

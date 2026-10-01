"""Parallel-Axis Theorem (Mass): I = I_cm + m * d^2."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    I_cm: float,  # noqa: N803
    m: float,
    d: float,
) -> float:
    return I_cm + m * d**2


parallel_axis_moment_of_inertia = FormulaSpec(
    id="mechanics.parallel_axis_moment_of_inertia",
    name="Parallel-Axis Theorem (Mass)",
    equation="I = I_cm + m * d^2",
    description="Mass moment of inertia about an axis parallel to one through the centre of mass.",
    inputs=(
        VariableSpec(
            name="I_cm",
            symbol="I_{cm}",
            description="Moment of inertia about the parallel axis through the centre of mass",
            dimension="M L^2",
            si_unit="kg*m^2",
        ),
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the body",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="d",
            symbol="d",
            description="Distance between the two parallel axes",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="I",
        symbol="I",
        description="Moment of inertia about the shifted axis",
        dimension="M L^2",
        si_unit="kg*m^2",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "10-5-calculating-moments-of-inertia",
            "sec. 10.5, eq. (10.20)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"I_cm": 2.0, "m": 3.0, "d": 0.5},
            expected=2.75,
            rel_tol=1e-12,
            note="Hand calculation: 2.0 + 3.0 * 0.25 = 2.75 kg m^2.",
        ),
    ),
    assumptions=(
        "The reference axis must pass through the centre of mass; shifting between two "
        "non-centroidal axes needs two steps.",
        "Mass moment of inertia; the area (second) moment used for beam bending has its own "
        "version of the theorem.",
    ),
    tags=("moment of inertia", "parallel axis", "Steiner", "rigid body"),
)

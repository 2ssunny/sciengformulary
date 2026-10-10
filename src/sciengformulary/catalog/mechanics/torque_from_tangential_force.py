"""Torque from a Tangential Force: tau = r * F."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.catalog._sources import ENGINEERING_ACCESSED, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(r: float, F: float) -> float:  # noqa: N803
    non_negative("r", r)
    finite("F", F)
    return finite_result(r * F)


torque_from_tangential_force = FormulaSpec(
    id="mechanics.torque_from_tangential_force",
    name="Torque from a Tangential Force",
    equation="tau = r * F",
    description=(
        "Torque about a pivot or axle produced by a force applied perpendicular to the lever "
        "arm, for example a force tangent to a wheel rim."
    ),
    inputs=(
        VariableSpec(
            name="r",
            symbol="r",
            description=(
                "Perpendicular distance from the axis to the line of action of the force "
                "(for example the wheel radius), not negative"
            ),
            dimension="L",
            si_unit="m",
        ),
        VariableSpec(
            name="F",
            symbol="F",
            description=(
                "Force perpendicular to the arm (tangent to the rim); its sign gives the sense "
                "of rotation"
            ),
            dimension="M L T^-2",
            si_unit="N",
        ),
    ),
    output=VariableSpec(
        name="tau",
        symbol=r"\tau",
        description="Torque about the axis",
        dimension="M L^2 T^-2",
        si_unit="N*m",
    ),
    evaluator=_evaluate,
    references=(
        # The page defines torque as force times the perpendicular distance from the pivot and
        # works T = F * L for a force perpendicular to the arm; only the symbols are renamed
        # (T -> tau, L -> r).
        nasa_glenn(
            "Torque (Moment)",
            "torque-moment",
            2023,
            "Example 1",
            accessed=ENGINEERING_ACCESSED,
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"r": 0.3, "F": 500.0},
            expected=150.0,
            rel_tol=1e-12,
            note="Hand calculation: 0.3 m * 500 N = 150 N*m.",
        ),
        VerificationCase(
            inputs={"r": 0.3, "F": 0.0},
            expected=0.0,
            rel_tol=1e-12,
            abs_tol=1e-09,
            note="Zero tangential force gives zero torque.",
        ),
        VerificationCase(
            inputs={"r": 0.05, "F": -12.5},
            expected=-0.625,
            rel_tol=1e-12,
            note="Hand calculation: 0.05 * (-12.5) = -0.625 N*m; the sign follows the force.",
        ),
    ),
    assumptions=(
        "The force is perpendicular to the lever arm (tangent to the rim). For another angle "
        "the source gives a cosine factor, so this item covers only the perpendicular case.",
        "Torque is taken about a fixed pivot or axle; r = 0 is allowed and gives zero torque.",
        "Sign convention: the sign of F carries the sense of rotation. No friction, inertia or "
        "rolling resistance is included.",
        "r must not be negative, and r and F must be finite; otherwise ValueError is raised.",
        "Homogeneous in any consistent unit set (torque = force * length).",
    ),
    tags=("torque", "moment", "lever arm", "wheel"),
)

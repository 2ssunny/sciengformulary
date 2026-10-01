"""Centripetal Acceleration: a_c = v^2 / r."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(v: float, r: float) -> float:
    return v**2 / r


centripetal_acceleration = FormulaSpec(
    id="mechanics.centripetal_acceleration",
    name="Centripetal Acceleration",
    equation="a_c = v^2 / r",
    description=(
        "Acceleration toward the centre needed to keep a body on a circular path of radius r at "
        "speed v."
    ),
    inputs=(
        VariableSpec(
            name="v",
            symbol="v",
            description="Speed along the path",
            dimension="L T^-1",
            si_unit="m/s",
        ),
        VariableSpec(
            name="r",
            symbol="r",
            description="Radius of curvature of the path",
            dimension="L",
            si_unit="m",
        ),
    ),
    output=VariableSpec(
        name="a_c",
        symbol="a_c",
        description="Centripetal acceleration (directed toward the centre)",
        dimension="L T^-2",
        si_unit="m/s^2",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            1,
            "4-4-uniform-and-nonuniform-circular-motion",
            "sec. 4.4, eq. (4.27)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"v": 10.0, "r": 5.0},
            expected=20.0,
            rel_tol=1e-12,
            note="Hand calculation: 10^2 / 5 = 20 m/s^2.",
        ),
    ),
    assumptions=(
        "Gives only the radial component; if the speed is changing there is also a tangential "
        "component.",
        "Equivalent to r * omega^2 with v = r * omega.",
    ),
    tags=("centripetal acceleration", "circular motion", "radial acceleration"),
)

"""Sensible Heat: Q = m * c * delta_T."""

from sciengformulary.catalog._sources import openstax_university_physics
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    m: float,
    c: float,
    delta_T: float,  # noqa: N803
) -> float:
    return m * c * delta_T


sensible_heat = FormulaSpec(
    id="thermodynamics.sensible_heat",
    name="Sensible Heat",
    equation="Q = m * c * delta_T",
    description="Heat needed to change the temperature of a mass without a phase change.",
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Specific heat capacity of the substance",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="delta_T",
            symbol=r"\Delta T",
            description="Temperature change",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Heat transferred",
        dimension="M L^2 T^-2",
        si_unit="J",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(
            2,
            "1-4-heat-transfer-specific-heat-and-calorimetry",
            "sec. 1.4, eq. (1.5)",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 2.0, "c": 4186.0, "delta_T": 10.0},
            expected=83720.0,
            rel_tol=1e-12,
            note="Hand calculation: 2 * 4186 * 10 = 83720 J.",
        ),
    ),
    assumptions=(
        "No phase change within the temperature range.",
        "c constant over the range (use the mean value otherwise); for gases use c_p or c_v "
        "according to the process.",
    ),
    tags=("specific heat", "sensible heat", "calorimetry", "heat capacity"),
)

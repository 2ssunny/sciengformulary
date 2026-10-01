"""Specific Heat at Constant Volume from Gamma: c_v = R / (gamma - 1)."""

from sciengformulary.catalog._sources import naca_report_1135
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(R: float, gamma: float) -> float:  # noqa: N803 - symbols as written in the source
    return R / (gamma - 1.0)


specific_heat_at_constant_volume_from_gamma = FormulaSpec(
    id="thermodynamics.specific_heat_at_constant_volume_from_gamma",
    name="Specific Heat at Constant Volume from Gamma",
    equation="c_v = R / (gamma - 1)",
    description="Specific heat at constant volume of an ideal gas from R and gamma.",
    inputs=(
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="gamma",
            symbol=r"\gamma",
            description="Ratio of specific heats c_p / c_v",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="c_v",
        symbol="c_v",
        description="Specific heat at constant volume",
        dimension="L^2 T^-2 Theta^-1",
        si_unit="J/(kg*K)",
    ),
    evaluator=_evaluate,
    references=(
        naca_report_1135("eq. (17)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"R": 287.0, "gamma": 1.4},
            expected=717.5,
            rel_tol=1e-12,
            note="Hand calculation: 287 / 0.4 = 717.5 J/(kg K).",
        ),
    ),
    assumptions=(
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "gamma must exceed 1.",
    ),
    tags=("specific heat", "cv", "ratio of specific heats", "ideal gas"),
)

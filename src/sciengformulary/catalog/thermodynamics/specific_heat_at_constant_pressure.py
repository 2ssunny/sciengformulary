"""Mayer's Relation (Specific Heats): c_p = c_v + R."""

from sciengformulary.catalog._sources import naca_report_1135, nasa_glenn
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c_v: float, R: float) -> float:  # noqa: N803 - symbols as written in the source
    return c_v + R


specific_heat_at_constant_pressure = FormulaSpec(
    id="thermodynamics.specific_heat_at_constant_pressure",
    name="Mayer's Relation (Specific Heats)",
    equation="c_p = c_v + R",
    description="Specific heat at constant pressure of an ideal gas from c_v and R.",
    inputs=(
        VariableSpec(
            name="c_v",
            symbol="c_v",
            description="Specific heat at constant volume",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
        VariableSpec(
            name="R",
            symbol="R",
            description="Specific gas constant (287 J/(kg K) for dry air)",
            dimension="L^2 T^-2 Theta^-1",
            si_unit="J/(kg*K)",
        ),
    ),
    output=VariableSpec(
        name="c_p",
        symbol="c_p",
        description="Specific heat at constant pressure",
        dimension="L^2 T^-2 Theta^-1",
        si_unit="J/(kg*K)",
    ),
    evaluator=_evaluate,
    references=(
        nasa_glenn("Specific Heats", "specific-heat-cp-cv", 2025),
        naca_report_1135("eq. (13b)"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c_v": 717.5, "R": 287.0},
            expected=1004.5,
            rel_tol=1e-12,
            note="Hand calculation: 717.5 + 287 = 1004.5 J/(kg K).",
        ),
    ),
    assumptions=(
        "Ideal (thermally perfect) gas: p = rho R T holds; not near condensation or at very "
        "high pressure.",
        "Per-unit-mass values; with molar values use the universal gas constant instead.",
    ),
    tags=("specific heat", "Mayer relation", "cp", "cv", "ideal gas"),
)

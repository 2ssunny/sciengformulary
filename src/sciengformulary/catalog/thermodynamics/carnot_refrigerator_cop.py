"""Carnot Refrigerator Coefficient of Performance: COP_R = T_C / (T_H - T_C)."""

from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    nasa_technical_report,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T_C: float, T_H: float) -> float:  # noqa: N803 - symbols as written in the source
    return T_C / (T_H - T_C)


carnot_refrigerator_cop = FormulaSpec(
    id="thermodynamics.carnot_refrigerator_cop",
    name="Carnot Refrigerator Coefficient of Performance",
    equation="COP_R = T_C / (T_H - T_C)",
    description=(
        "Highest possible coefficient of performance of a refrigerator moving heat from a cold to "
        "a hot reservoir."
    ),
    inputs=(
        VariableSpec(
            name="T_C",
            symbol="T_C",
            description="Cold reservoir absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T_H",
            symbol="T_H",
            description="Hot reservoir absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
    ),
    output=VariableSpec(
        name="COP_R",
        symbol="K_R",
        description="Coefficient of performance (heat removed per unit work)",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # The source writes K_R.
        openstax_university_physics(2, "4-5-the-carnot-cycle", "sec. 4.5, eq. (4.6)"),
        # The report's design worksheet gives the ideal cooling COP as T_cold / (T_hot - T_cold) (an
        # engineering report, not a textbook). The handbook prints Q_C / Q_H = T_C / T_H for a
        # reversible engine; running it backwards gives the same COP.
        nasa_technical_report(
            title="Lunar Base Heat Pump, Phase I Final Report",
            authors=("J. H. Goldman", "A. Harvey", "T. Lovell", "D. H. Walker"),
            report_number="NASA-CR-188300",
            year=1994,
            url="https://ntrs.nasa.gov/citations/19950011696",
            locator="p. 57",
        ),
        doe_fundamentals_handbook(
            "DOE-HDBK-1012/1-92",
            "Module 1, eq. (1-23), p. 73 plus reversal argument",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T_C": 270.0, "T_H": 300.0},
            expected=9.0,
            rel_tol=1e-12,
            note="Hand calculation: 270 / 30 = 9.",
        ),
    ),
    assumptions=(
        "Reversible refrigerator between two reservoirs; an upper bound for real machines.",
        "Absolute temperatures; T_H > T_C.",
    ),
    tags=("refrigerator", "coefficient of performance", "COP", "Carnot", "heat pump"),
)

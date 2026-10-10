"""Carnot Efficiency: eta_C = 1 - T_C / T_H."""

from sciengformulary.catalog._sources import (
    doe_fundamentals_handbook,
    openstax_university_physics,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(T_C: float, T_H: float) -> float:  # noqa: N803 - symbols as written in the source
    return 1.0 - T_C / T_H


carnot_efficiency = FormulaSpec(
    id="thermodynamics.carnot_efficiency",
    name="Carnot Efficiency",
    equation="eta_C = 1 - T_C / T_H",
    description="Highest possible efficiency of a heat engine operating between two reservoirs.",
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
        name="eta_C",
        symbol=r"\eta_C",
        description="Carnot efficiency",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_university_physics(2, "4-5-the-carnot-cycle", "sec. 4.5, eq. (4.5)"),
        doe_fundamentals_handbook(
            "DOE-HDBK-1012/1-92",
            "Module 1, 'Carnot Cycle', eq. (1-23), p. 73",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"T_C": 300.0, "T_H": 600.0},
            expected=0.5,
            rel_tol=1e-12,
            note="Hand calculation: 1 - 300/600 = 0.5.",
        ),
    ),
    assumptions=(
        "Reversible engine between two fixed-temperature reservoirs; real engines are always "
        "less efficient.",
        "Absolute temperatures (kelvin).",
    ),
    tags=("Carnot", "efficiency", "second law", "heat engine", "upper bound"),
)

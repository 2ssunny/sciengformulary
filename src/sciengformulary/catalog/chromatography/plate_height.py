"""Theoretical plate height."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(L: float, N: float) -> float:
    positive("L", L)
    positive("N", N)
    return finite_result(L / N)


plate_height = FormulaSpec(
    id="chromatography.plate_height",
    name="Plate Height",
    equation="H = L/N",
    description="Theoretical plate height.",
    inputs=(
        VariableSpec(name="L", symbol="L", description="Column length", dimension="L", si_unit="m"),
        VariableSpec(
            name="N", symbol="N", description="Theoretical plate number", dimension="1", si_unit="-"
        ),
    ),
    output=VariableSpec(
        name="H",
        symbol="H",
        description="Height equivalent to a theoretical plate",
        dimension="L",
        si_unit="m",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            (
                "12%3A_Chromatographic_and_Electrophoretic_Methods/12.02%3A_General_Theory_of_Col"
                "umn_Chromatography"
            ),
            "12.2: General Theory of Column Chromatography",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"L": 1, "N": 10000},
            expected=0.0001,
            note="One metre / 10000 = 0.1 mm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"L": 2, "N": 10000},
            expected=0.0002,
            note="Two metres / 10000 = 0.2 mm.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "N is measured for the same column, analyte and operating conditions.",
        "Theoretical plates are a model, not physical plates.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "plate height"),
)

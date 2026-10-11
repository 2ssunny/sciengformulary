"""Theoretical plate number from baseline width."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(t_R: float, w_baseline: float) -> float:
    positive("t_R", t_R)
    positive("w_baseline", w_baseline)
    return finite_result(16 * (t_R / w_baseline) ** 2)


baseline_plate_number = FormulaSpec(
    id="chromatography.baseline_plate_number",
    name="Baseline Plate Number",
    equation="N = 16*(t_R/w_baseline)^2",
    description="Theoretical plate number from baseline width.",
    inputs=(
        VariableSpec(
            name="t_R", symbol="t_R", description="Total retention time", dimension="T", si_unit="s"
        ),
        VariableSpec(
            name="w_baseline",
            symbol="w_baseline",
            description="Peak baseline width",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="N", symbol="N", description="Theoretical plate number", dimension="1", si_unit="-"
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
            inputs={"t_R": 100, "w_baseline": 10},
            expected=1600,
            note="16 times 10 squared = 1600.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"t_R": 200, "w_baseline": 10},
            expected=6400,
            note="Doubling retention time at fixed width quadruples N.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Approximately Gaussian peak with its tangent-defined baseline width.",
        "Use total retention time, not adjusted retention time; this is not effective plate number.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "baseline plate number"),
)

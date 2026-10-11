"""Resolution from baseline peak widths."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(t_R1: float, t_R2: float, w1: float, w2: float) -> float:
    non_negative("t_R1", t_R1)
    non_negative("t_R2", t_R2)
    positive("w1", w1)
    positive("w2", w2)
    return finite_result(2 * abs(t_R2 - t_R1) / (w1 + w2))


baseline_peak_resolution = FormulaSpec(
    id="chromatography.baseline_peak_resolution",
    name="Baseline Peak Resolution",
    equation="Rs = 2*abs(t_R2-t_R1)/(w1+w2)",
    description="Resolution from baseline peak widths.",
    inputs=(
        VariableSpec(
            name="t_R1",
            symbol="t_R1",
            description="Retention time of peak 1",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="t_R2",
            symbol="t_R2",
            description="Retention time of peak 2",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="w1",
            symbol="w1",
            description="Baseline width of peak 1",
            dimension="T",
            si_unit="s",
        ),
        VariableSpec(
            name="w2",
            symbol="w2",
            description="Baseline width of peak 2",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="Rs",
        symbol="Rs",
        description="Baseline-width peak resolution",
        dimension="1",
        si_unit="-",
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
            inputs={"t_R1": 100, "t_R2": 130, "w1": 20, "w2": 20},
            expected=1.5,
            note="Twice 30 divided by 40 is 1.5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"t_R1": 100, "t_R2": 100, "w1": 20, "w2": 20},
            expected=0,
            note="Coincident peaks have zero resolution.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "w1 and w2 are widths at the baseline, not full widths at half maximum.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "baseline peak resolution"),
)

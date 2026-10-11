"""Column chromatography retention factor."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(t_R: float, t_M: float) -> float:
    positive("t_R", t_R)
    positive("t_M", t_M)
    if t_R < t_M:
        raise ValueError("retention time cannot precede hold-up time in this model")
    return finite_result((t_R - t_M) / t_M)


retention_factor = FormulaSpec(
    id="chromatography.retention_factor",
    name="Retention Factor",
    equation="k = (t_R-t_M)/t_M",
    description="Column chromatography retention factor.",
    inputs=(
        VariableSpec(
            name="t_R", symbol="t_R", description="Total retention time", dimension="T", si_unit="s"
        ),
        VariableSpec(
            name="t_M",
            symbol="t_M",
            description="Unretained hold-up time",
            dimension="T",
            si_unit="s",
        ),
    ),
    output=VariableSpec(
        name="k", symbol="k", description="Column retention factor", dimension="1", si_unit="-"
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
            inputs={"t_R": 300, "t_M": 100},
            expected=2,
            note="(300-100)/100=2.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"t_R": 100, "t_M": 100},
            expected=0,
            note="Unretained analyte gives k=0.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Compatible retention and hold-up times from the same conditions.",
        "This column k is different from the planar TLC Rf.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "retention factor"),
)

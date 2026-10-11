"""Chromatographic selectivity between two retained species."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(k_later: float, k_earlier: float) -> float:
    positive("k_later", k_later)
    positive("k_earlier", k_earlier)
    if k_later < k_earlier:
        raise ValueError("k_later must not be smaller than k_earlier")
    return finite_result(k_later / k_earlier)


separation_factor = FormulaSpec(
    id="chromatography.separation_factor",
    name="Separation Factor",
    equation="alpha = k_later/k_earlier",
    description="Chromatographic selectivity between two retained species.",
    inputs=(
        VariableSpec(
            name="k_later",
            symbol="k_later",
            description="Retention factor of later peak",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k_earlier",
            symbol="k_earlier",
            description="Retention factor of earlier peak",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="alpha",
        symbol="alpha",
        description="Selectivity or separation factor",
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
            inputs={"k_later": 3, "k_earlier": 2},
            expected=1.5,
            note="3/2=1.5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"k_later": 2, "k_earlier": 2},
            expected=1,
            note="Co-retention gives limiting selectivity one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Same separation conditions and peak order; alpha >= 1.",
        "Equal factors represent the unseparated limiting case.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chromatography", "separation factor"),
)

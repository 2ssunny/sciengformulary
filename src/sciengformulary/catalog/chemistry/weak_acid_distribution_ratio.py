"""pH-dependent extraction ratio of a neutral weak acid."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(K_D: float, Ka: float, a_H: float) -> float:
    non_negative("K_D", K_D)
    positive("Ka", Ka)
    positive("a_H", a_H)
    return finite_result(K_D / (1 + Ka / a_H))


weak_acid_distribution_ratio = FormulaSpec(
    id="chemistry.weak_acid_distribution_ratio",
    name="Weak Acid Distribution Ratio",
    equation="D = K_D/(1 + Ka/a_H)",
    description="pH-dependent extraction ratio of a neutral weak acid.",
    inputs=(
        VariableSpec(
            name="K_D",
            symbol="K_D",
            description="Neutral-acid organic/aqueous concentration partition ratio",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Ka",
            symbol="Ka",
            description="Dimensionless acid dissociation constant",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_H",
            symbol="a_H",
            description="Dimensionless hydrogen-ion activity",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Total acid organic/aqueous distribution ratio",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "07%3A_Obtaining_and_Preparing_Samples_for_Analysis/7.07%3A_Liquid-Liquid_Extractions",
            "7.7: Liquid-Liquid Extractions",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"K_D": 10, "Ka": 1e-05, "a_H": 1e-05},
            expected=5,
            note="At equal Ka and hydrogen activity, half the aqueous acid is neutral.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"K_D": 0, "Ka": 1e-05, "a_H": 1e-05},
            expected=0,
            note="Zero neutral partition gives zero total distribution.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Derived result: Normalize the source concentration-form Ka and hydrogen concentration by the same standard concentration.",
        "Only neutral monoprotic acid enters the organic phase; aqueous acid-base equilibrium is maintained.",
        "Dilute aqueous concentration ratios approximate activity ratios with compatible standard states.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "weak acid distribution ratio"),
)

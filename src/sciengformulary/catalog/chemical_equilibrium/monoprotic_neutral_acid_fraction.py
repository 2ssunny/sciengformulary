"""Neutral fraction of a monoprotic acid."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Ka: float, a_H: float) -> float:
    positive("Ka", Ka)
    positive("a_H", a_H)
    return finite_result(1 / (1 + Ka / a_H))


monoprotic_neutral_acid_fraction = FormulaSpec(
    id="chemical_equilibrium.monoprotic_neutral_acid_fraction",
    name="Monoprotic Neutral Acid Fraction",
    equation="alpha_HA = 1/(1+Ka/a_H)",
    description="Neutral fraction of a monoprotic acid.",
    inputs=(
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
        name="alpha_HA",
        symbol="alpha_HA",
        description="Fraction of acid present as neutral HA",
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
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Ka": 1e-05, "a_H": 1e-05},
            expected=0.5,
            note="At pH=pKa, neutral and conjugate forms are equally populated.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Ka": 1e-05, "a_H": 9e-05},
            expected=0.9,
            note="Conjugate/neutral ratio 1/9 gives neutral fraction 9/10.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Combine acid dissociation with C_total=[HA]+[A-] to solve for [HA]/C_total.",
        "Only HA and A- are relevant acid forms; aqueous equilibrium is maintained.",
        "Concentration fractions use the ideal dilute approximation for the HA/A- activity-coefficient ratio.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "monoprotic neutral acid fraction"),
)

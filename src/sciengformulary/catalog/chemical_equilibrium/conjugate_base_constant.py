"""Conjugate acid-base equilibrium relation."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Kw: float, Ka: float) -> float:
    positive("Kw", Kw)
    positive("Ka", Ka)
    return finite_result(Kw / Ka)


conjugate_base_constant = FormulaSpec(
    id="chemical_equilibrium.conjugate_base_constant",
    name="Conjugate Base Constant",
    equation="Kb = Kw / Ka",
    description="Conjugate acid-base equilibrium relation.",
    inputs=(
        VariableSpec(
            name="Kw",
            symbol="Kw",
            description="Water ion product at the chosen temperature",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="Ka",
            symbol="Ka",
            description="Acid dissociation constant of the conjugate acid",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Kb",
        symbol="Kb",
        description="Conjugate base dissociation constant",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "14-3-relative-strengths-of-acids-and-bases",
            "14.3 Relative Strengths of Acids and Bases",
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
            inputs={"Kw": 1e-14, "Ka": 1e-05},
            expected=1e-09,
            note="1e-14 / 1e-5 = 1e-9.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Kw": 1e-14, "Ka": 1e-09},
            expected=1e-05,
            note="1e-14 / 1e-9 = 1e-5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Ka, Kb and Kw use compatible activity conventions and the same temperature.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "conjugate base constant"),
)

"""Fraction remaining after equal-volume repeated liquid-liquid extraction."""

from sciengformulary.catalog._domain import (
    finite_result,
    integer,
    non_negative,
    positive,
)
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(V_aq: float, V_org: float, D: float, n: float) -> float:
    positive("V_aq", V_aq)
    positive("V_org", V_org)
    non_negative("D", D)
    n = integer("n", n, minimum=0)
    return finite_result((V_aq / (D * V_org + V_aq)) ** n)


repeated_extraction_remaining_fraction = FormulaSpec(
    id="chemistry.repeated_extraction_remaining_fraction",
    name="Repeated Extraction Remaining Fraction",
    equation="f_remaining = [V_aq/(D*V_org+V_aq)]^n",
    description="Fraction remaining after equal-volume repeated liquid-liquid extraction.",
    inputs=(
        VariableSpec(
            name="V_aq",
            symbol="V_aq",
            description="Aqueous phase volume",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="V_org",
            symbol="V_org",
            description="Fresh organic solvent volume in each extraction",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="D",
            symbol="D",
            description="Constant organic-to-aqueous distribution ratio",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of equal-volume extractions",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="f_remaining",
        symbol="f_remaining",
        description="Fraction of initial analyte remaining in the aqueous phase",
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
            inputs={"V_aq": 5e-05, "V_org": 1.5e-05, "D": 5, "n": 2},
            expected=0.16,
            note="Single-step fraction 50/(5*15+50)=0.4; two steps leave 0.16.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"V_aq": 5e-05, "V_org": 1.5e-05, "D": 5, "n": 0},
            expected=1,
            note="No extraction leaves the entire initial analyte.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Each step reaches equilibrium with fresh solvent; D and phase volumes remain constant.",
        "V_org is volume per extraction, not total solvent volume; losses and mutual phase-volume changes excluded.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "repeated extraction remaining fraction"),
)

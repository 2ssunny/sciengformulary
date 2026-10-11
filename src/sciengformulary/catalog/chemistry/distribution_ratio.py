"""Analytical distribution ratio between two liquid phases."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c_organic_total: float, c_aqueous_total: float) -> float:
    non_negative("c_organic_total", c_organic_total)
    positive("c_aqueous_total", c_aqueous_total)
    return finite_result(c_organic_total / c_aqueous_total)


distribution_ratio = FormulaSpec(
    id="chemistry.distribution_ratio",
    name="Distribution Ratio",
    equation="D = c_organic_total/c_aqueous_total",
    description="Analytical distribution ratio between two liquid phases.",
    inputs=(
        VariableSpec(
            name="c_organic_total",
            symbol="c_organic_total",
            description="Total analytical solute concentration in organic phase",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="c_aqueous_total",
            symbol="c_aqueous_total",
            description="Total analytical solute concentration in aqueous phase",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="D",
        description="Organic-to-aqueous distribution ratio",
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
            inputs={"c_organic_total": 10, "c_aqueous_total": 2},
            expected=5,
            note="10/2=5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c_organic_total": 0, "c_aqueous_total": 2},
            expected=0,
            note="No organic-phase solute gives zero ratio.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Phases are at distribution equilibrium; concentrations count all forms of the analyte.",
        "D can depend on pH and differs from the partition constant of a single chemical form.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "distribution ratio"),
)

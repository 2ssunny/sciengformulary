"""Logarithmic acid dissociation constant."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(Ka: float) -> float:
    positive("Ka", Ka)
    return finite_result(-math.log10(Ka))


acid_dissociation_pka = FormulaSpec(
    id="chemical_equilibrium.acid_dissociation_pka",
    name="Acid Dissociation Pka",
    equation="pKa = -log10(Ka)",
    description="Logarithmic acid dissociation constant.",
    inputs=(
        VariableSpec(
            name="Ka",
            symbol="Ka",
            description="Dimensionless thermodynamic acid dissociation constant",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="pKa", symbol="pKa", description="Acid dissociation pKa", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "14-6-buffers",
            "14.6 Buffers",
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
            inputs={"Ka": 1e-05},
            expected=5,
            note="Ka = 1e-5 gives pKa = 5.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Ka": 1},
            expected=0,
            note="Unit dissociation constant gives pKa zero.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Ka is a dimensionless activity-based equilibrium constant at the specified temperature.",
        "This differs from pH: it is a property of an equilibrium, not the current hydrogen-ion activity.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "acid dissociation pka"),
)

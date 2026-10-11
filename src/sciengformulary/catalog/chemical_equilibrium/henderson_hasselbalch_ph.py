"""Henderson-Hasselbalch relation using activities."""

import math

from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(pKa: float, a_base: float, a_acid: float) -> float:
    finite("pKa", pKa)
    positive("a_base", a_base)
    positive("a_acid", a_acid)
    return finite_result(pKa + math.log10(a_base) - math.log10(a_acid))


henderson_hasselbalch_ph = FormulaSpec(
    id="chemical_equilibrium.henderson_hasselbalch_ph",
    name="Henderson Hasselbalch Ph",
    equation="pH = pKa + log10(a_base / a_acid)",
    description="Henderson-Hasselbalch relation using activities.",
    inputs=(
        VariableSpec(
            name="pKa",
            symbol="pKa",
            description="Activity-based acid dissociation pKa",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_base",
            symbol="a_base",
            description="Conjugate-base activity",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_acid",
            symbol="a_acid",
            description="Undissociated-acid activity",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="pH", symbol="pH", description="Buffer pH", dimension="1", si_unit="-"
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
            inputs={"pKa": 5, "a_base": 0.01, "a_acid": 0.01},
            expected=5,
            note="Equal activities give pH = pKa.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"pKa": 5, "a_base": 0.1, "a_acid": 0.01},
            expected=6,
            note="Tenfold base/acid activity ratio raises pH by one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Acid and conjugate base at equilibrium under a common standard-state convention.",
        "Replacing activities by concentrations requires appropriate dilute-solution/activity-coefficient approximations.",
        "Near equivalence, in very dilute solutions or after large acid/base additions, calculate the actual equilibrium composition first.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "henderson hasselbalch ph"),
)

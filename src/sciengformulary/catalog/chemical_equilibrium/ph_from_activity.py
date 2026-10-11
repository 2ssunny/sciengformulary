"""Thermodynamic pH from hydrogen-ion activity."""

import math

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(a_H: float) -> float:
    positive("a_H", a_H)
    return finite_result(-math.log10(a_H))


ph_from_activity = FormulaSpec(
    id="chemical_equilibrium.ph_from_activity",
    name="Ph From Activity",
    equation="pH = -log10(a_H)",
    description="Thermodynamic pH from hydrogen-ion activity.",
    inputs=(
        VariableSpec(
            name="a_H",
            symbol="a_H",
            description="Dimensionless hydrogen-ion activity",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="pH", symbol="pH", description="Activity-based pH", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"a_H": 1e-07},
            expected=7,
            note="Negative base-ten logarithm of 1e-7 is seven.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"a_H": 10},
            expected=-1,
            note="Activity ten gives pH -1; pH is not restricted to 0--14.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "a_H is dimensionless activity relative to the chosen standard state.",
        "Do not substitute concentration in mol/m^3 without normalization and an activity coefficient.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "ph from activity"),
)

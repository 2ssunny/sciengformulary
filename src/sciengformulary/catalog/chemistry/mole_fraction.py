"""Mole fraction of one mixture component."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n_component: float, n_total: float) -> float:
    non_negative("n_component", n_component)
    positive("n_total", n_total)
    if n_component > n_total:
        raise ValueError("n_component cannot exceed n_total")
    return finite_result(n_component / n_total)


mole_fraction = FormulaSpec(
    id="chemistry.mole_fraction",
    name="Mole Fraction",
    equation="x = n_component / n_total",
    description="Mole fraction of one mixture component.",
    inputs=(
        VariableSpec(
            name="n_component",
            symbol="n_component",
            description="Amount of the selected component",
            dimension="N",
            si_unit="mol",
        ),
        VariableSpec(
            name="n_total",
            symbol="n_total",
            description="Total amount of all mixture components",
            dimension="N",
            si_unit="mol",
        ),
    ),
    output=VariableSpec(
        name="x", symbol="x", description="Mole fraction", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "11-4-colligative-properties",
            "11.4 Colligative Properties",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n_component": 2, "n_total": 5},
            expected=0.4,
            note="Two moles out of five gives 0.4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n_component": 1, "n_total": 1},
            expected=1,
            note="A pure component has mole fraction one.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "The component amount cannot exceed the total.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "mole fraction"),
)

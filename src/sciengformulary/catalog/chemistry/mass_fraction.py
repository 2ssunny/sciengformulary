"""Mass fraction of a solution component."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m_component: float, m_solution: float) -> float:
    non_negative("m_component", m_component)
    positive("m_solution", m_solution)
    if m_component > m_solution:
        raise ValueError("m_component cannot exceed m_solution")
    return finite_result(m_component / m_solution)


mass_fraction = FormulaSpec(
    id="chemistry.mass_fraction",
    name="Mass Fraction",
    equation="w = m_component / m_solution",
    description="Mass fraction of a solution component.",
    inputs=(
        VariableSpec(
            name="m_component",
            symbol="m_component",
            description="Mass of selected component",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="m_solution",
            symbol="m_solution",
            description="Total mass of solution",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="w", symbol="w", description="Mass fraction, not percent", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "3-4-other-units-for-solution-concentrations",
            "3.4 Other Units for Solution Concentrations",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m_component": 0.005, "m_solution": 0.1},
            expected=0.05,
            note="5 g in 100 g gives 0.05, or 5 percent.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m_component": 0, "m_solution": 1},
            expected=0,
            note="No component gives zero fraction.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Multiply the returned fraction by 100 to obtain mass percent.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "mass fraction"),
)

"""Partial pressure in an ideal gas mixture."""

from sciengformulary.catalog._domain import finite, finite_result, non_negative
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(x_i: float, p_total: float) -> float:
    finite("x_i", x_i)
    if not 0 <= x_i <= 1:
        raise ValueError("x_i must be between zero and one")
    non_negative("p_total", p_total)
    return finite_result(x_i * p_total)


dalton_partial_pressure = FormulaSpec(
    id="chemistry.dalton_partial_pressure",
    name="Dalton Partial Pressure",
    equation="p_i = x_i * p_total",
    description="Partial pressure in an ideal gas mixture.",
    inputs=(
        VariableSpec(
            name="x_i",
            symbol="x_i",
            description="Gas-phase mole fraction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p_total",
            symbol="p_total",
            description="Total pressure of the gas mixture",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="p_i",
        symbol="p_i",
        description="Gas component partial pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="9.3 Stoichiometry of Gaseous Substances, Mixtures, and Reactions",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/9-3-stoichiometry-of-gaseous-substances-mixtures-and-reactions",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"x_i": 0.2, "p_total": 100000},
            expected=20000,
            note="0.2 of 100000 Pa = 20000 Pa.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"x_i": 0, "p_total": 100000},
            expected=0,
            note="Absent component has zero partial pressure.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Ideal gas mixture; gas-phase mole fraction is used.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "dalton partial pressure"),
)

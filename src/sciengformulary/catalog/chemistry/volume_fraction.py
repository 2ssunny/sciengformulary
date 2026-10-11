"""Volume percentage expressed as a fraction."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(V_component: float, V_solution: float) -> float:
    non_negative("V_component", V_component)
    positive("V_solution", V_solution)
    if V_component > V_solution:
        raise ValueError("V_component cannot exceed V_solution in this preparation definition")
    return finite_result(V_component / V_solution)


volume_fraction = FormulaSpec(
    id="chemistry.volume_fraction",
    name="Volume Fraction",
    equation="phi = V_component / V_solution",
    description="Volume percentage expressed as a fraction.",
    inputs=(
        VariableSpec(
            name="V_component",
            symbol="V_component",
            description="Volume of selected pure component used in preparation",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="V_solution",
            symbol="V_solution",
            description="Final volume of solution",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="phi",
        symbol="phi",
        description="Preparation volume fraction, not percent",
        dimension="1",
        si_unit="-",
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
            inputs={"V_component": 0.0001, "V_solution": 0.001},
            expected=0.1,
            note="100 mL made up to 1 L gives 0.1.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"V_component": 0, "V_solution": 1},
            expected=0,
            note="No component gives zero preparation fraction.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Use the final measured solution volume; volumes need not be additive.",
        "Multiply by 100 for volume percent.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "volume fraction"),
)

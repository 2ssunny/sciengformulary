"""Isolated yield in percent."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(actual: float, theoretical: float) -> float:
    non_negative("actual", actual)
    positive("theoretical", theoretical)
    return finite_result(100 * (actual / theoretical))


percent_yield = FormulaSpec(
    id="chemistry.percent_yield",
    name="Percent Yield",
    equation="yield_percent = 100 * actual / theoretical",
    description="Isolated yield in percent.",
    inputs=(
        VariableSpec(
            name="actual",
            symbol="actual",
            description="Actual isolated amount of product",
            dimension="N",
            si_unit="mol",
        ),
        VariableSpec(
            name="theoretical",
            symbol="theoretical",
            description="Theoretical amount from the limiting reagent",
            dimension="N",
            si_unit="mol",
        ),
    ),
    output=VariableSpec(
        name="yield_percent",
        symbol="yield_percent",
        description="Numerical percent yield",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="4.4 Reaction Yields",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/4-4-reaction-yields",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"actual": 0.008, "theoretical": 0.01},
            expected=80,
            note="0.008 / 0.01 times 100 = 80 percent.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"actual": 0, "theoretical": 0.01},
            expected=0,
            note="No isolated product gives zero percent.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Use the same product and amount basis in numerator and denominator.",
        "Values above 100 are reported, not rejected; investigate purity, retained solvent and measurement errors.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "percent yield"),
)

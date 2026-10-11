"""Theoretical product amount from balanced stoichiometry."""

from sciengformulary.catalog._domain import finite_result, integer, non_negative
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(n_limiting: float, nu_product: float, nu_limiting: float) -> float:
    non_negative("n_limiting", n_limiting)
    nu_product = integer("nu_product", nu_product, minimum=1)
    nu_limiting = integer("nu_limiting", nu_limiting, minimum=1)
    return finite_result(n_limiting * (nu_product / nu_limiting))


stoichiometric_product_amount = FormulaSpec(
    id="chemistry.stoichiometric_product_amount",
    name="Stoichiometric Product Amount",
    equation="n_product = n_limiting * nu_product / nu_limiting",
    description="Theoretical product amount from balanced stoichiometry.",
    inputs=(
        VariableSpec(
            name="n_limiting",
            symbol="n_limiting",
            description="Amount of the already identified limiting reagent",
            dimension="N",
            si_unit="mol",
        ),
        VariableSpec(
            name="nu_product",
            symbol="nu_product",
            description="Product coefficient in the balanced reaction",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_limiting",
            symbol="nu_limiting",
            description="Limiting reagent coefficient in the balanced reaction",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="n_product",
        symbol="n_product",
        description="Theoretical amount of product",
        dimension="N",
        si_unit="mol",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="4.3 Reaction Stoichiometry",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/4-3-reaction-stoichiometry",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n_limiting": 2, "nu_product": 2, "nu_limiting": 1},
            expected=4,
            note="Stoichiometric ratio 2/1 converts two moles into four.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n_limiting": 0.3, "nu_product": 1, "nu_limiting": 2},
            expected=0.15,
            note="0.3 times 1/2 = 0.15 mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "The reaction is balanced and n_limiting is the available limiting-reagent amount.",
        "This does not identify the limiting reagent or predict practical yield.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "stoichiometric product amount"),
)

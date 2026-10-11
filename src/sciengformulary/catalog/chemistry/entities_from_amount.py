"""Count of specified elementary entities."""

from sciengformulary.catalog._constants import (
    AVOGADRO_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> float:
    non_negative("n", n)
    return finite_result(n * AVOGADRO_CONSTANT)


entities_from_amount = FormulaSpec(
    id="chemistry.entities_from_amount",
    name="Entities From Amount",
    equation="N_entities = n * N_A",
    description="Count of specified elementary entities.",
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Amount of specified elementary entities",
            dimension="N",
            si_unit="mol",
        ),
    ),
    output=VariableSpec(
        name="N_entities",
        symbol="N_entities",
        description="Number of specified entities",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "3-1-formula-mass-and-the-mole-concept",
            "3.1 Formula Mass and the Mole Concept",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 1},
            expected=6.02214076e23,
            note="The SI definition gives exactly 6.02214076e23 entities per mole.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n": 0.5},
            expected=3.01107038e23,
            note="Half a mole contains half the Avogadro number.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Specify whether the entities are atoms, molecules, ions or formula units.",
        "The returned float is not an exact integer count for very large samples.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "entities from amount"),
)

"""Amount of a specified substance from its mass."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(m: float, M: float) -> float:
    non_negative("m", m)
    positive("M", M)
    return finite_result(m / M)


amount_from_mass = FormulaSpec(
    id="chemistry.amount_from_mass",
    name="Amount From Mass",
    equation="n = m / M",
    description="Amount of a specified substance from its mass.",
    inputs=(
        VariableSpec(
            name="m",
            symbol="m",
            description="Mass of the specified substance",
            dimension="M",
            si_unit="kg",
        ),
        VariableSpec(
            name="M",
            symbol="M",
            description="Molar mass of the substance",
            dimension="M N^-1",
            si_unit="kg/mol",
        ),
    ),
    output=VariableSpec(
        name="n", symbol="n", description="Amount of substance", dimension="N", si_unit="mol"
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "3-1-formula-mass-and-the-mole-concept",
            "3.1 Formula Mass and the Mole Concept",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"m": 0.018, "M": 0.018},
            expected=1,
            note="Hand check: equal mass and molar mass give one mole.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"m": 0, "M": 0.05844},
            expected=0,
            note="Zero sample contains zero moles.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Use the molar mass of the actual chemical form, including hydration when applicable.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "amount from mass"),
)

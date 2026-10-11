"""Amount of solute per mass of solvent."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, m_solvent: float) -> float:
    non_negative("n", n)
    positive("m_solvent", m_solvent)
    return finite_result(n / m_solvent)


molality = FormulaSpec(
    id="chemistry.molality",
    name="Molality",
    equation="b = n / m_solvent",
    description="Amount of solute per mass of solvent.",
    inputs=(
        VariableSpec(
            name="n", symbol="n", description="Amount of solute", dimension="N", si_unit="mol"
        ),
        VariableSpec(
            name="m_solvent",
            symbol="m_solvent",
            description="Mass of solvent",
            dimension="M",
            si_unit="kg",
        ),
    ),
    output=VariableSpec(
        name="b", symbol="b", description="Molality", dimension="N M^-1", si_unit="mol/kg"
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
            inputs={"n": 0.2, "m_solvent": 0.1},
            expected=2,
            note="0.2 mol / 0.1 kg = 2 mol/kg.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n": 0, "m_solvent": 1},
            expected=0,
            note="No solute gives zero molality.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "The denominator is solvent mass, not solution mass.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "molality"),
)

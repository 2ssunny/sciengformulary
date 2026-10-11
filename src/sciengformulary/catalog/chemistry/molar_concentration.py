"""Molar concentration with SI reference units."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, V: float) -> float:
    non_negative("n", n)
    positive("V", V)
    return finite_result(n / V)


molar_concentration = FormulaSpec(
    id="chemistry.molar_concentration",
    name="Molar Concentration",
    equation="c = n / V",
    description="Molar concentration with SI reference units.",
    inputs=(
        VariableSpec(
            name="n", symbol="n", description="Amount of solute", dimension="N", si_unit="mol"
        ),
        VariableSpec(
            name="V",
            symbol="V",
            description="Final volume of solution",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="c",
        symbol="c",
        description="Amount concentration",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "3-3-molarity",
            "3.3 Molarity",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0.01, "V": 0.0002},
            expected=50,
            note="0.01 mol / 0.0002 m^3 = 50 mol/m^3 (0.05 mol/L).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"n": 0, "V": 0.001},
            expected=0,
            note="A solution with no solute has zero concentration.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "V is solution volume, not the volume of solvent before mixing.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "molar concentration"),
)

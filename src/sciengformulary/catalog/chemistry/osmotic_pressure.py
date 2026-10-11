"""Ideal dilute-solution osmotic pressure."""

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    bipm_si_defining_constants,
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(i: float, c: float, T: float) -> float:
    positive("i", i)
    non_negative("c", c)
    positive("T", T)
    return finite_result(i * c * MOLAR_GAS_CONSTANT * T)


osmotic_pressure = FormulaSpec(
    id="chemistry.osmotic_pressure",
    name="Osmotic Pressure",
    equation="Pi = i * c * R_u * T",
    description="Ideal dilute-solution osmotic pressure.",
    inputs=(
        VariableSpec(
            name="i",
            symbol="i",
            description="Effective van t Hoff particle factor",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="c",
            symbol="c",
            description="Formal solute concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="T", symbol="T", description="Absolute temperature", dimension="Theta", si_unit="K"
        ),
    ),
    output=VariableSpec(
        name="Pi",
        symbol="Pi",
        description="Osmotic pressure",
        dimension="M L^-1 T^-2",
        si_unit="Pa",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "11-4-colligative-properties",
            "11.4 Colligative Properties",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"i": 1, "c": 1, "T": 300},
            expected=2494.338785445972,
            note="Decimal check: exact R_u times 300 for one mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"i": 2, "c": 0, "T": 300},
            expected=0,
            note="No solute gives zero osmotic pressure.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Dilute solution separated from solvent by an ideal semipermeable membrane.",
        "Inputs must use SI because R_u is built in.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "osmotic pressure"),
)

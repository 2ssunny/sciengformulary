"""Boiling-point elevation."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(i: float, K_solvent: float, b: float) -> float:
    positive("i", i)
    positive("K_solvent", K_solvent)
    non_negative("b", b)
    return finite_result(i * K_solvent * b)


boiling_point_elevation = FormulaSpec(
    id="chemistry.boiling_point_elevation",
    name="Boiling Point Elevation",
    equation="delta_T = i * K_solvent * b",
    description="Boiling-point elevation.",
    inputs=(
        VariableSpec(
            name="i",
            symbol="i",
            description="Effective van t Hoff particle factor",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="K_solvent",
            symbol="K_solvent",
            description="Solvent constant for this specific phase transition",
            dimension="Theta M N^-1",
            si_unit="K*kg/mol",
        ),
        VariableSpec(
            name="b",
            symbol="b",
            description="Molality of dissolved solute",
            dimension="N M^-1",
            si_unit="mol/kg",
        ),
    ),
    output=VariableSpec(
        name="delta_T",
        symbol="delta_T",
        description="Positive magnitude of transition-temperature shift",
        dimension="Theta",
        si_unit="K",
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
            inputs={"i": 2, "K_solvent": 1.5, "b": 0.2},
            expected=0.6,
            note="2 times 1.5 times 0.2 = 0.6 K.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"i": 1, "K_solvent": 2, "b": 0},
            expected=0,
            note="Pure solvent gives zero shift.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Dilute solution with a nonvolatile solute in the colligative regime.",
        "Use K_b for boiling or K_f for freezing; add the result to boiling temperature and subtract it from freezing temperature.",
        "i is an effective particle factor, not necessarily the integer dissociation count.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "boiling point elevation"),
)

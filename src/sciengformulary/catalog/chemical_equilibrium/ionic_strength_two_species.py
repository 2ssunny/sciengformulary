"""Ionic strength for a two-ion composition."""

from sciengformulary.catalog._domain import finite_result, integer, non_negative
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c1: float, z1: float, c2: float, z2: float) -> float:
    non_negative("c1", c1)
    z1 = integer("z1", z1)
    non_negative("c2", c2)
    z2 = integer("z2", z2)
    return finite_result((c1 * z1**2 + c2 * z2**2) / 2)


ionic_strength_two_species = FormulaSpec(
    id="chemical_equilibrium.ionic_strength_two_species",
    name="Ionic Strength Two Species",
    equation="I = (c1*z1^2 + c2*z2^2) / 2",
    description="Ionic strength for a two-ion composition.",
    inputs=(
        VariableSpec(
            name="c1",
            symbol="c1",
            description="Concentration of ion species 1",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="z1",
            symbol="z1",
            description="Charge number of species 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="c2",
            symbol="c2",
            description="Concentration of ion species 2",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="z2",
            symbol="z2",
            description="Charge number of species 2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="I",
        symbol="I",
        description="Concentration-based ionic strength",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c1": 100, "z1": 1, "c2": 100, "z2": -1},
            expected=100,
            note="0.1 M NaCl has ionic strength 0.1 M = 100 mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c1": 200, "z1": 1, "c2": 100, "z2": -2},
            expected=300,
            note="0.1 M Na2SO4: (200+400)/2 = 300 mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Exactly two ionic species or a two-species contribution to a larger sum.",
        "For more species sum one half of c_i*z_i^2 over all ions; electroneutrality is the caller responsibility.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "ionic strength two species"),
)

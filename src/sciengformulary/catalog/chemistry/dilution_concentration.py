"""Final concentration after dilution."""

from sciengformulary.catalog._domain import finite_result, non_negative, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c_initial: float, V_initial: float, V_final: float) -> float:
    non_negative("c_initial", c_initial)
    positive("V_initial", V_initial)
    positive("V_final", V_final)
    if V_final < V_initial:
        raise ValueError("V_final must be at least V_initial for dilution")
    return finite_result(c_initial * (V_initial / V_final))


dilution_concentration = FormulaSpec(
    id="chemistry.dilution_concentration",
    name="Dilution Concentration",
    equation="c_final = c_initial * V_initial / V_final",
    description="Final concentration after dilution.",
    inputs=(
        VariableSpec(
            name="c_initial",
            symbol="c_initial",
            description="Initial solute concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="V_initial",
            symbol="V_initial",
            description="Volume of initial solution transferred",
            dimension="L^3",
            si_unit="m^3",
        ),
        VariableSpec(
            name="V_final",
            symbol="V_final",
            description="Final volume after dilution",
            dimension="L^3",
            si_unit="m^3",
        ),
    ),
    output=VariableSpec(
        name="c_final",
        symbol="c_final",
        description="Final solute concentration",
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
            inputs={"c_initial": 1000, "V_initial": 1e-05, "V_final": 0.0001},
            expected=100,
            note="Tenfold volume increase gives 100 mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c_initial": 200, "V_initial": 0.001, "V_final": 0.001},
            expected=200,
            note="No volume change preserves concentration.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Solute amount is conserved; no reaction, precipitation or solute loss.",
        "This evaluator models dilution only, so V_final >= V_initial.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "dilution concentration"),
)

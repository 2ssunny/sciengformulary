"""Integrated zero-order consumption law."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c0: float, k: float, t: float) -> float:
    non_negative("c0", c0)
    non_negative("k", k)
    non_negative("t", t)
    if k * t > c0:
        raise ValueError("zero-order model has passed reactant depletion")
    return finite_result(c0 - k * t)


zero_order_concentration = FormulaSpec(
    id="chemical_kinetics.zero_order_concentration",
    name="Zero Order Concentration",
    equation="c = c0 - k*t",
    description="Integrated zero-order consumption law.",
    inputs=(
        VariableSpec(
            name="c0",
            symbol="c0",
            description="Initial reactant concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Zero-order consumption rate constant",
            dimension="N L^-3 T^-1",
            si_unit="mol/(m^3*s)",
        ),
        VariableSpec(name="t", symbol="t", description="Elapsed time", dimension="T", si_unit="s"),
    ),
    output=VariableSpec(
        name="c",
        symbol="c",
        description="Remaining reactant concentration",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "12-4-integrated-rate-laws",
            "12.4 Integrated Rate Laws",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"c0": 10, "k": 2, "t": 3},
            expected=4,
            note="10 - 2 times 3 = 4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c0": 10, "k": 2, "t": 5},
            expected=0,
            note="At depletion time concentration reaches zero.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Single-species zero-order consumption with constant k and fixed volume.",
        "Valid only until depletion; negative concentrations are rejected.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "zero order concentration"),
)

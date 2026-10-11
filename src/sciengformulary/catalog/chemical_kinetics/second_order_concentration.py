"""Integrated second-order single-species disappearance law."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c0: float, k: float, t: float) -> float:
    non_negative("c0", c0)
    non_negative("k", k)
    non_negative("t", t)
    return finite_result(c0 / (1 + k * c0 * t))


second_order_concentration = FormulaSpec(
    id="chemical_kinetics.second_order_concentration",
    name="Second Order Concentration",
    equation="c = c0 / (1 + k*c0*t)",
    description="Integrated second-order single-species disappearance law.",
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
            description="Rate constant for -dc/dt = k*c^2",
            dimension="L^3 N^-1 T^-1",
            si_unit="m^3/(mol*s)",
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
            inputs={"c0": 2, "k": 0.5, "t": 1},
            expected=1,
            note="1/c = 1/2 + 0.5 times 1 = 1.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c0": 2, "k": 0.5, "t": 0},
            expected=2,
            note="At t=0 recover initial concentration.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Single-species differential consumption law -dc/dt=k*c^2 with constant k and fixed volume.",
        "If reaction rate is normalized for 2A -> products, distinguish its rate constant from the disappearance constant used here.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "second order concentration"),
)

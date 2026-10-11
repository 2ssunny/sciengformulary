"""Half-life for second-order consumption."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c0: float, k: float) -> float:
    positive("c0", c0)
    positive("k", k)
    return finite_result(1 / (k * c0))


second_order_half_life = FormulaSpec(
    id="chemical_kinetics.second_order_half_life",
    name="Second Order Half Life",
    equation="t_half = 1 / (k*c0)",
    description="Half-life for second-order consumption.",
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
            description="Disappearance constant for -dc/dt=k*c^2",
            dimension="L^3 N^-1 T^-1",
            si_unit="m^3/(mol*s)",
        ),
    ),
    output=VariableSpec(
        name="t_half",
        symbol="t_half",
        description="Second-order half-life",
        dimension="T",
        si_unit="s",
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
            inputs={"c0": 2, "k": 0.5},
            expected=1,
            note="1/(0.5 times 2)=1 s.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c0": 4, "k": 0.5},
            expected=0.5,
            note="Doubling concentration halves this half-life.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Single-species second-order disappearance law with constant k.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "second order half life"),
)

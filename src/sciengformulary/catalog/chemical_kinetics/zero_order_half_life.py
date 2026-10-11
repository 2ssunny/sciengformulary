"""Half-life for zero-order consumption."""

from sciengformulary.catalog._domain import finite_result, positive
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(c0: float, k: float) -> float:
    positive("c0", c0)
    positive("k", k)
    return finite_result(c0 / (2 * k))


zero_order_half_life = FormulaSpec(
    id="chemical_kinetics.zero_order_half_life",
    name="Zero Order Half Life",
    equation="t_half = c0 / (2*k)",
    description="Half-life for zero-order consumption.",
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
            description="Zero-order disappearance constant",
            dimension="N L^-3 T^-1",
            si_unit="mol/(m^3*s)",
        ),
    ),
    output=VariableSpec(
        name="t_half",
        symbol="t_half",
        description="Zero-order half-life",
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
            inputs={"c0": 10, "k": 2},
            expected=2.5,
            note="Half of ten consumed at two per second takes 2.5 s.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"c0": 20, "k": 2},
            expected=5,
            note="Doubling initial concentration doubles zero-order half-life.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Zero-order single-species consumption under constant conditions.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "zero order half life"),
)

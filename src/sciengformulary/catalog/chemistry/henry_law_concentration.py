"""Henry law dissolved concentration."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(k_H: float, p: float) -> float:
    non_negative("k_H", k_H)
    non_negative("p", p)
    return finite_result(k_H * p)


henry_law_concentration = FormulaSpec(
    id="chemistry.henry_law_concentration",
    name="Henry Law Concentration",
    equation="c = k_H * p",
    description="Henry law dissolved concentration.",
    inputs=(
        VariableSpec(
            name="k_H",
            symbol="k_H",
            description="Henry coefficient in the concentration-over-pressure convention",
            dimension="N M^-1 L^-2 T^2",
            si_unit="mol/(m^3*Pa)",
        ),
        VariableSpec(
            name="p",
            symbol="p",
            description="Partial pressure of the dissolved gas above the liquid",
            dimension="M L^-1 T^-2",
            si_unit="Pa",
        ),
    ),
    output=VariableSpec(
        name="c",
        symbol="c",
        description="Equilibrium dissolved gas concentration",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="11.3 Solubility",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/11-3-solubility",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k_H": 1e-05, "p": 100000},
            expected=1,
            note="1e-5 times 1e5 = 1 mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"k_H": 2e-05, "p": 0},
            expected=0,
            note="Zero partial pressure gives zero dissolved concentration in this model.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Dilute dissolved gas at equilibrium; coefficient appropriate to the gas, solvent and temperature.",
        "k_H uses c/p, not the inverse p/c convention.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "henry law concentration"),
)

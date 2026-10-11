"""Reaction enthalpy estimate from average bond energies."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(D_broken_total: float, D_formed_total: float) -> float:
    non_negative("D_broken_total", D_broken_total)
    non_negative("D_formed_total", D_formed_total)
    return finite_result(D_broken_total - D_formed_total)


bond_enthalpy_reaction_estimate = FormulaSpec(
    id="thermodynamics.bond_enthalpy_reaction_estimate",
    name="Bond Enthalpy Reaction Estimate",
    equation="delta_H_estimate = D_broken_total - D_formed_total",
    description="Reaction enthalpy estimate from average bond energies.",
    inputs=(
        VariableSpec(
            name="D_broken_total",
            symbol="D_broken_total",
            description="Sum of gas-phase average bond enthalpies for bonds broken per mole of reaction",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="D_formed_total",
            symbol="D_formed_total",
            description="Sum of gas-phase average bond enthalpies for bonds formed per mole of reaction",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
    ),
    output=VariableSpec(
        name="delta_H_estimate",
        symbol="delta_H_estimate",
        description="Estimated molar reaction enthalpy",
        dimension="M L^2 T^-2 N^-1",
        si_unit="J/mol",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="7.5 Strengths of Ionic and Covalent Bonds",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/7-5-strengths-of-ionic-and-covalent-bonds",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"D_broken_total": 500000, "D_formed_total": 700000},
            expected=-200000,
            note="Breaking costs 500 kJ/mol and forming releases 700 kJ/mol: net -200 kJ/mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"D_broken_total": 500000, "D_formed_total": 500000},
            expected=0,
            note="Equal bond-energy sums cancel.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Use average gas-phase bond enthalpies with all broken/formed bond counts included.",
        "Approximate molecular-environment-dependent estimate; condensed-phase transitions require additional corrections.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "bond enthalpy reaction estimate"),
)

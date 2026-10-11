"""Hess-law standard reaction enthalpy from formation data."""

from sciengformulary.catalog._domain import finite, finite_result, integer
from sciengformulary.catalog._sources import (
    openstax_section,
)
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(
    Hf_P1: float,
    Hf_P2: float,
    Hf_R1: float,
    Hf_R2: float,
    nu_P1: float,
    nu_P2: float,
    nu_R1: float,
    nu_R2: float,
) -> float:
    finite("Hf_P1", Hf_P1)
    finite("Hf_P2", Hf_P2)
    finite("Hf_R1", Hf_R1)
    finite("Hf_R2", Hf_R2)
    nu_P1 = integer("nu_P1", nu_P1, minimum=0)
    nu_P2 = integer("nu_P2", nu_P2, minimum=0)
    nu_R1 = integer("nu_R1", nu_R1, minimum=0)
    nu_R2 = integer("nu_R2", nu_R2, minimum=0)
    if nu_P1 + nu_P2 == 0 or nu_R1 + nu_R2 == 0:
        raise ValueError("include at least one product and one reactant")
    return finite_result(nu_P1 * Hf_P1 + nu_P2 * Hf_P2 - nu_R1 * Hf_R1 - nu_R2 * Hf_R2)


reaction_enthalpy_from_formation = FormulaSpec(
    id="thermodynamics.reaction_enthalpy_from_formation",
    name="Reaction Enthalpy From Formation",
    equation="delta_H = nu_P1*Hf_P1 + nu_P2*Hf_P2 - nu_R1*Hf_R1 - nu_R2*Hf_R2",
    description="Hess-law standard reaction enthalpy from formation data.",
    inputs=(
        VariableSpec(
            name="Hf_P1",
            symbol="Hf_P1",
            description="Standard formation enthalpy of product 1",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="Hf_P2",
            symbol="Hf_P2",
            description="Standard formation enthalpy of product 2",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="Hf_R1",
            symbol="Hf_R1",
            description="Standard formation enthalpy of reactant 1",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="Hf_R2",
            symbol="Hf_R2",
            description="Standard formation enthalpy of reactant 2",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
        VariableSpec(
            name="nu_P1",
            symbol="nu_P1",
            description="Coefficient of product 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_P2",
            symbol="nu_P2",
            description="Coefficient of product 2",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_R1",
            symbol="nu_R1",
            description="Coefficient of reactant 1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_R2",
            symbol="nu_R2",
            description="Coefficient of reactant 2",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="delta_H",
        symbol="delta_H",
        description="Standard molar enthalpy of the reaction as written",
        dimension="M L^2 T^-2 N^-1",
        si_unit="J/mol",
    ),
    evaluator=_evaluate,
    references=(
        openstax_section(
            "chemistry-2e",
            "5-3-enthalpy",
            "5.3 Enthalpy",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={
                "Hf_P1": -200000,
                "Hf_P2": 0,
                "Hf_R1": -50000,
                "Hf_R2": 0,
                "nu_P1": 1,
                "nu_P2": 0,
                "nu_R1": 1,
                "nu_R2": 0,
            },
            expected=-150000,
            note="Products -200 kJ minus reactants -50 kJ gives -150 kJ/mol.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={
                "Hf_P1": -200000,
                "Hf_P2": 0,
                "Hf_R1": -50000,
                "Hf_R2": 0,
                "nu_P1": 2,
                "nu_P2": 0,
                "nu_R1": 2,
                "nu_R2": 0,
            },
            expected=-300000,
            note="Doubling the balanced reaction doubles its reaction enthalpy.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Same temperature, standard-state convention and correct physical phases for all formation enthalpies.",
        "Balanced reaction with at most two product and two reactant species; coefficient zero omits a slot.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "thermodynamics", "reaction enthalpy from formation"),
)

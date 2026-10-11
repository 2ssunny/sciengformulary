"""Temperature dependence of chemical equilibrium."""

import math

from sciengformulary.catalog._constants import (
    MOLAR_GAS_CONSTANT,
)
from sciengformulary.catalog._domain import finite, finite_result, positive
from sciengformulary.catalog._sources import bipm_si_defining_constants
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(K1: float, T1: float, T2: float, delta_H_standard: float) -> float:
    positive("K1", K1)
    positive("T1", T1)
    positive("T2", T2)
    finite("delta_H_standard", delta_H_standard)
    return finite_result(K1 * math.exp(-delta_H_standard / MOLAR_GAS_CONSTANT * (1 / T2 - 1 / T1)))


van_t_hoff_equilibrium_constant = FormulaSpec(
    id="chemical_equilibrium.van_t_hoff_equilibrium_constant",
    name="Van T Hoff Equilibrium Constant",
    equation="K2 = K1 * exp[-delta_H_standard/R_u * (1/T2 - 1/T1)]",
    description="Temperature dependence of chemical equilibrium.",
    inputs=(
        VariableSpec(
            name="K1",
            symbol="K1",
            description="Dimensionless equilibrium constant at T1",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="T1",
            symbol="T1",
            description="First absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="T2",
            symbol="T2",
            description="Second absolute temperature",
            dimension="Theta",
            si_unit="K",
        ),
        VariableSpec(
            name="delta_H_standard",
            symbol="delta_H_standard",
            description="Standard molar reaction enthalpy",
            dimension="M L^2 T^-2 N^-1",
            si_unit="J/mol",
        ),
    ),
    output=VariableSpec(
        name="K2",
        symbol="K2",
        description="Dimensionless equilibrium constant at T2",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="9.6: Temperature Dependence of Equilibrium Constants - the van ’t Hoff Equation",
            organization="Millersville University",
            url="https://chem.libretexts.org/Courses/Millersville_University/CHEM_341-_Physical_Chemistry_I/09%3A_Chemical_Equilibria/9.06%3A_Temperature_Dependence_of_Equilibrium_Constants_-_the_van_t_Hoff_Equation",
            accessed="2026-10-10",
        ),
        bipm_si_defining_constants(),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"K1": 2, "T1": 300, "T2": 300, "delta_H_standard": 10000},
            expected=2,
            note="Equal temperatures preserve K.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"K1": 2, "T1": 300, "T2": 600, "delta_H_standard": 4988.677570891944},
            expected=5.43656365691809,
            note="Exponent equals one; independent Decimal result 2 exp(1).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Rearrange the integrated van t Hoff equation to solve for K2.",
        "Standard reaction enthalpy approximately constant over the temperature interval.",
        "Keep the same balanced reaction and standard-state convention.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "van t hoff equilibrium constant"),
)

"""Molar solubility of a binary salt in the ideal dilute limit."""

import math

from sciengformulary.catalog._domain import finite_result, integer, positive
from sciengformulary.catalog._sources import (
    harvey_analytical_chemistry,
)
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(Ksp: float, p: float, q: float, c_standard: float) -> float:
    positive("Ksp", Ksp)
    p = integer("p", p, minimum=1)
    q = integer("q", q, minimum=1)
    positive("c_standard", c_standard)
    return finite_result(
        c_standard * math.exp((math.log(Ksp) - p * math.log(p) - q * math.log(q)) / (p + q))
    )


salt_molar_solubility = FormulaSpec(
    id="chemical_equilibrium.salt_molar_solubility",
    name="Salt Molar Solubility",
    equation="s = c_standard * [Ksp/(p^p*q^q)]^(1/(p+q))",
    description="Molar solubility of a binary salt in the ideal dilute limit.",
    inputs=(
        VariableSpec(
            name="Ksp",
            symbol="Ksp",
            description="Dimensionless activity-based solubility product",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="p",
            symbol="p",
            description="Number of cations released per formula unit",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="q",
            symbol="q",
            description="Number of anions released per formula unit",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="c_standard",
            symbol="c_standard",
            description="Standard-state amount concentration",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="s",
        symbol="s",
        description="Formal molar solubility",
        dimension="N L^-3",
        si_unit="mol/m^3",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="15.1 Precipitation and Dissolution",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/15-1-precipitation-and-dissolution",
            accessed="2026-10-10",
        ),
        harvey_analytical_chemistry(
            "06%3A_Equilibrium_Chemistry/6.09%3A_Activity_Effects",
            "6.9: Activity Effects",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"Ksp": 1e-08, "p": 1, "q": 1, "c_standard": 1000},
            expected=0.1,
            note="AB: sqrt(1e-8) times 1000 = 0.1 mol/m^3.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"Ksp": 4e-12, "p": 1, "q": 2, "c_standard": 1000},
            expected=0.1,
            note="AB2: Ksp=4(s/c_standard)^3 gives s/c_standard=1e-4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "Derived result: Substitute a_cation=p*s/c_standard and a_anion=q*s/c_standard into Ksp.",
        "Salt releases p cations and q anions; only these ions contribute to Ksp.",
        "Pure solvent with no common ions, complexation or acid-base reactions; activity coefficients approximated as one.",
        "A common concentration standard is 1000 mol/m^3 (1 mol/L).",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "salt molar solubility"),
)

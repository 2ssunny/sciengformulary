"""Activity quotient for reactions with up to two reactant and two product species."""

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


def _evaluate(
    a_A: float,
    a_B: float,
    a_C: float,
    a_D: float,
    nu_A: float,
    nu_B: float,
    nu_C: float,
    nu_D: float,
) -> float:
    positive("a_A", a_A)
    positive("a_B", a_B)
    positive("a_C", a_C)
    positive("a_D", a_D)
    nu_A = integer("nu_A", nu_A, minimum=0)
    nu_B = integer("nu_B", nu_B, minimum=0)
    nu_C = integer("nu_C", nu_C, minimum=0)
    nu_D = integer("nu_D", nu_D, minimum=0)
    if nu_A + nu_B == 0 or nu_C + nu_D == 0:
        raise ValueError("include at least one reactant and one product")
    return finite_result(
        math.exp(
            nu_C * math.log(a_C)
            + nu_D * math.log(a_D)
            - nu_A * math.log(a_A)
            - nu_B * math.log(a_B)
        )
    )


reaction_quotient = FormulaSpec(
    id="chemical_equilibrium.reaction_quotient",
    name="Reaction Quotient",
    equation="Q = a_C^nu_C * a_D^nu_D / (a_A^nu_A * a_B^nu_B)",
    description="Activity quotient for reactions with up to two reactant and two product species.",
    inputs=(
        VariableSpec(
            name="a_A",
            symbol="a_A",
            description="Dimensionless activity of reactant A",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_B",
            symbol="a_B",
            description="Dimensionless activity of reactant B",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_C",
            symbol="a_C",
            description="Dimensionless activity of product C",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="a_D",
            symbol="a_D",
            description="Dimensionless activity of product D",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_A",
            symbol="nu_A",
            description="Stoichiometric coefficient of A",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_B",
            symbol="nu_B",
            description="Stoichiometric coefficient of B",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_C",
            symbol="nu_C",
            description="Stoichiometric coefficient of C",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="nu_D",
            symbol="nu_D",
            description="Stoichiometric coefficient of D",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="Q",
        symbol="Q",
        description="Dimensionless reaction quotient",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="13.2 Equilibrium Constants",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants",
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
            inputs={
                "a_A": 2,
                "a_B": 1,
                "a_C": 4,
                "a_D": 1,
                "nu_A": 1,
                "nu_B": 0,
                "nu_C": 1,
                "nu_D": 0,
            },
            expected=2,
            note="One product/reactant ratio: 4/2 = 2.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={
                "a_A": 1,
                "a_B": 1,
                "a_C": 1,
                "a_D": 1,
                "nu_A": 1,
                "nu_B": 2,
                "nu_C": 1,
                "nu_D": 1,
            },
            expected=1,
            note="Unit activities give unit quotient.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
    ),
    assumptions=(
        "For nu_A A + nu_B B <=> nu_C C + nu_D D; use activity 1 and coefficient 0 for an omitted slot.",
        "At least one reactant and one product coefficient must be positive.",
        "Pure solids and liquids have unit activity in their appropriate standard state; this is Q, and equals K only at equilibrium.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical equilibrium", "reaction quotient"),
)

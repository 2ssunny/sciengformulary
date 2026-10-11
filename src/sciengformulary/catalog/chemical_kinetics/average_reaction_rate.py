"""Average reaction rate from reactant consumption."""

from sciengformulary.catalog._domain import finite, finite_result, integer, positive
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(delta_c_reactant: float, nu: float, delta_t: float) -> float:
    finite("delta_c_reactant", delta_c_reactant)
    nu = integer("nu", nu, minimum=1)
    positive("delta_t", delta_t)
    return finite_result(-delta_c_reactant / (nu * delta_t))


average_reaction_rate = FormulaSpec(
    id="chemical_kinetics.average_reaction_rate",
    name="Average Reaction Rate",
    equation="r = -delta_c_reactant / (nu * delta_t)",
    description="Average reaction rate from reactant consumption.",
    inputs=(
        VariableSpec(
            name="delta_c_reactant",
            symbol="delta_c_reactant",
            description="Final minus initial concentration of a reactant",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="nu",
            symbol="nu",
            description="Reactant coefficient in the balanced equation",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="delta_t", symbol="delta_t", description="Elapsed time", dimension="T", si_unit="s"
        ),
    ),
    output=VariableSpec(
        name="r",
        symbol="r",
        description="Stoichiometrically normalized average forward rate",
        dimension="N L^-3 T^-1",
        si_unit="mol/(m^3*s)",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="12.1 Chemical Reaction Rates",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/12-1-chemical-reaction-rates",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"delta_c_reactant": -20, "nu": 2, "delta_t": 5},
            expected=2,
            note="Consumption: 20/(2 times 5) = 2 mol/(m^3 s).",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"delta_c_reactant": 0, "nu": 1, "delta_t": 5},
            expected=0,
            note="No concentration change gives zero average rate.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Fixed-volume concentration basis and a single balanced reaction.",
        "A positive result corresponds to net reactant consumption; reverse change may give a negative rate.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "average reaction rate"),
)

"""Second-order two-species rate law."""

from sciengformulary.catalog._domain import finite_result, non_negative
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(k: float, c_A: float, c_B: float) -> float:
    non_negative("k", k)
    non_negative("c_A", c_A)
    non_negative("c_B", c_B)
    return finite_result(k * c_A * c_B)


bimolecular_rate = FormulaSpec(
    id="chemical_kinetics.bimolecular_rate",
    name="Bimolecular Rate",
    equation="r = k * c_A * c_B",
    description="Second-order two-species rate law.",
    inputs=(
        VariableSpec(
            name="k",
            symbol="k",
            description="Second-order rate constant",
            dimension="L^3 N^-1 T^-1",
            si_unit="m^3/(mol*s)",
        ),
        VariableSpec(
            name="c_A",
            symbol="c_A",
            description="Concentration of species A",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
        VariableSpec(
            name="c_B",
            symbol="c_B",
            description="Concentration of species B",
            dimension="N L^-3",
            si_unit="mol/m^3",
        ),
    ),
    output=VariableSpec(
        name="r",
        symbol="r",
        description="Rate governed by the specified law",
        dimension="N L^-3 T^-1",
        si_unit="mol/(m^3*s)",
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="12.3 Rate Laws",
            organization="OpenStax",
            url="https://openstax.org/books/chemistry-2e/pages/12-3-rate-laws",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"k": 0.01, "c_A": 2, "c_B": 3},
            expected=0.06,
            note="0.01 times 2 times 3 = 0.06.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"k": 0.01, "c_A": 0, "c_B": 3},
            expected=0,
            note="Absent reactant makes the model rate zero.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Rate is first order in each of the two species; rate law is established experimentally or for an elementary step.",
        "Do not infer reaction orders from overall reaction coefficients.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemical kinetics", "bimolecular rate"),
)

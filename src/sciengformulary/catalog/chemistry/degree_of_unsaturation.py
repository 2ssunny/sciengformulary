"""Degree of unsaturation for ordinary neutral organic formulas."""

from sciengformulary.catalog._domain import finite_result, integer
from sciengformulary.core import (
    FormulaSpec,
    ReferenceSpec,
    VariableSpec,
    VerificationCase,
)


def _evaluate(C: float, H: float, N: float, X: float) -> float:
    C = integer("C", C, minimum=0)
    H = integer("H", H, minimum=0)
    N = integer("N", N, minimum=0)
    X = integer("X", X, minimum=0)
    dbe = (2 * C + 2 + N - H - X) / 2
    if dbe < 0 or not dbe.is_integer():
        raise ValueError("formula is incompatible with this neutral closed-shell DBE model")
    return finite_result((2 * C + 2 + N - H - X) / 2)


degree_of_unsaturation = FormulaSpec(
    id="chemistry.degree_of_unsaturation",
    name="Degree Of Unsaturation",
    equation="DBE = (2*C + 2 + N - H - X) / 2",
    description="Degree of unsaturation for ordinary neutral organic formulas.",
    inputs=(
        VariableSpec(
            name="C", symbol="C", description="Number of carbon atoms", dimension="1", si_unit="-"
        ),
        VariableSpec(
            name="H", symbol="H", description="Number of hydrogen atoms", dimension="1", si_unit="-"
        ),
        VariableSpec(
            name="N", symbol="N", description="Number of nitrogen atoms", dimension="1", si_unit="-"
        ),
        VariableSpec(
            name="X",
            symbol="X",
            description="Total number of monovalent halogen atoms",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="DBE", symbol="DBE", description="Double bond equivalents", dimension="1", si_unit="-"
    ),
    evaluator=_evaluate,
    references=(
        ReferenceSpec(
            source_type="official_web",
            title="7.2 Calculating the Degree of Unsaturation",
            organization="OpenStax",
            url="https://openstax.org/books/organic-chemistry/pages/7-2-calculating-the-degree-of-unsaturation",
            accessed="2026-10-10",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"C": 6, "H": 6, "N": 0, "X": 0},
            expected=4,
            note="C6H6 gives (12 + 2 - 6)/2 = 4.",
            rel_tol=1e-12,
            abs_tol=0.0,
        ),
        VerificationCase(
            inputs={"C": 2, "H": 6, "N": 0, "X": 0},
            expected=0,
            note="C2H6 gives no unsaturation.",
            rel_tol=1e-12,
            abs_tol=1e-300,
        ),
    ),
    assumptions=(
        "Derived result: Apply the stated hydrogen/halogen/nitrogen correction to the saturated acyclic formula.",
        "For neutral closed-shell formulas with ordinary C(4), N(3), H(1), halogen(1), O(2) and divalent S valences.",
        "O and ordinary divalent S do not enter this expression.",
        "Charged ions, radicals and unusual valences require a different treatment; a whole non-negative result is necessary but does not prove a valid structure.",
        "No automatic unit conversion; si_unit documents the reference system.",
    ),
    tags=("chemistry", "chemistry", "degree of unsaturation"),
)

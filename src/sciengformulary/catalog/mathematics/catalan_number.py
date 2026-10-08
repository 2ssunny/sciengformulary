"""Catalan Number: C_n = (2 n)! / ((n + 1)! * n!)."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    # C(2n, n) is always divisible by n + 1, so the floor division is exact.
    return math.comb(2 * n, n) // (n + 1)


catalan_number = FormulaSpec(
    id="mathematics.catalan_number",
    name="Catalan Number",
    equation="C_n = (2 n)! / ((n + 1)! * n!)",
    description=(
        "The n-th Catalan number, equal to C(2n, n) / (n + 1) with C_0 = 1; one thing it counts "
        "is the binary trees with n internal nodes."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Index (number of internal nodes of the binary trees counted), integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="C_n",
        symbol="C_n",
        description="n-th Catalan number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states (n + 1) * catalan n = centralBinom n = choose (2n) n. Dividing by n + 1
        # and writing choose (2n) n = (2n)! / (n! n!) gives (2n)! / ((n + 1)! n!), because
        # (n + 1) n! = (n + 1)!.
        mathlib(
            "Mathlib/Combinatorics/Enumerative/Catalan/Basic.lean#L126",
            "theorem succ_mul_catalan_eq_centralBinom",
        ),
        mathlib("Mathlib/Data/Nat/Choose/Central.lean#L37", "def Nat.centralBinom"),
        # Counting meaning and the indexing C_0 = 1 (the empty tree).
        mathlib(
            "Mathlib/Combinatorics/Enumerative/Catalan/Tree.lean#L74",
            "theorem treesOfNumNodesEq_card_eq_catalan",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 3},
            expected=5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Explicit enumeration of binary trees with 3 nodes; Dyck-word count and the "
                "Segner recurrence agree."
            ),
        ),
        VerificationCase(
            inputs={"n": 10},
            expected=16796,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Binary-tree enumeration, a scan of all 2^20 up/down words and the Segner "
                "recurrence agree with the exact ratio 20!/(11! 10!)."
            ),
        ),
        VerificationCase(
            inputs={"n": 15},
            expected=9694845,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact integer Segner recurrence (the defining recurrence in the source), equal "
                "to the exact factorial ratio."
            ),
        ),
        VerificationCase(
            inputs={"n": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 0: tree enumeration yields only the empty tree.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: tree enumeration yields one single-node tree.",
        ),
    ),
    assumptions=(
        "n is a non-negative whole number.",
        "Indexing starts at C_0 = 1, so the sequence runs 1, 1, 2, 5, 14, ...",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=(
        "Catalan number",
        "central binomial coefficient",
        "binary trees",
        "Dyck paths",
        "combinatorics",
        "counting",
    ),
)

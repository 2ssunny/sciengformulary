"""k-Permutations of n Items: P = n! / (n - k)!."""

import math

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, k: float) -> int:
    n = integer("n", n, minimum=0)
    k = integer("k", k, minimum=0)
    if k > n:
        raise ValueError(f"k must not exceed n, got n={n!r}, k={k!r}.")
    return math.perm(n, k)


k_permutations = FormulaSpec(
    id="mathematics.k_permutations",
    name="k-Permutations of n Items",
    equation="P = n! / (n - k)!",
    description=(
        "Count of the ordered selections of k distinct items out of n distinct items, which is "
        "the falling factorial n (n - 1) ... (n - k + 1)."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of distinct items, integer",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of positions to fill (items arranged), integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="P",
        symbol="P(n, k)",
        description="Number of ordered selections of k distinct items",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib's descFactorial n k is the product n (n - 1) ... (n - k + 1).
        mathlib("Mathlib/Data/Nat/Factorial/Basic.lean#L424", "theorem Nat.descFactorial_eq_div"),
        # An injection from a k-set into an n-set is an ordered choice of k distinct items, so
        # its count n.descFactorial k is the number of k-permutations.
        mathlib("Mathlib/Data/Fintype/CardEmbedding.lean#L40", "theorem Fintype.card_embedding_eq"),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 5, "k": 2},
            expected=20,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force count of ordered pairs of distinct items from 5; equals 5!/3!.",
        ),
        VerificationCase(
            inputs={"n": 10, "k": 3},
            expected=720,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force count of length-3 tuples of distinct items from 10 (10 * 9 * 8).",
        ),
        VerificationCase(
            inputs={"n": 6, "k": 6},
            expected=720,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = n: brute-force count of all orderings of 6 items (6!).",
        ),
        VerificationCase(
            inputs={"n": 7, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0: brute force finds only the empty arrangement.",
        ),
        VerificationCase(
            inputs={"n": 0, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = k = 0: brute force finds one empty arrangement.",
        ),
    ),
    assumptions=(
        "n and k are whole numbers with 0 <= k <= n; k > n is rejected (no such arrangement "
        "exists and the factorial form is undefined).",
        "Order matters and each item is used at most once.",
        "Computed exactly in integer arithmetic; the result is a Python int of any size.",
    ),
    tags=(
        "permutations",
        "k-permutations",
        "nPr",
        "falling factorial",
        "arrangements",
        "combinatorics",
        "counting",
    ),
)

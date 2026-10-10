"""Number of Derangements: D = n! * sum_{k=0}^{n} (-1)^k / k!."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    # Exact integer form of n! * sum (-1)^k / k!: each term n!/k! = (k + 1)(k + 2)...n is a
    # whole number, built here from k = n down to k = 0.
    total = 0
    term = 1  # n!/n!
    for k in range(n, -1, -1):
        total += term if k % 2 == 0 else -term
        term *= k  # n!/(k - 1)! = (n!/k!) * k
    return total


derangement_count = FormulaSpec(
    id="mathematics.derangement_count",
    name="Number of Derangements",
    equation="D = n! * sum_{k=0}^{n} (-1)^k / k!",
    description=(
        "Count of the permutations of n distinct items that leave no item in its original "
        "position (the subfactorial !n)."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of items, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="D",
        symbol="!n",
        description="Number of fixed-point-free permutations of n items",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib states numDerangements n = sum over k = 0..n of (-1)^k ascFactorial (k + 1)
        # (n - k) over the integers. For k <= n, ascFactorial (k + 1) (n - k) = (k + 1)...n
        # = n!/k! (Nat.ascFactorial_eq_div), so the sum is n! * sum (-1)^k / k!.
        mathlib(
            "Mathlib/Combinatorics/Derangements/Finite.lean#L106", "theorem numDerangements_sum"
        ),
        # Counting meaning (permutations without fixed points) and numDerangements 0 = 1.
        mathlib(
            "Mathlib/Combinatorics/Derangements/Finite.lean#L101",
            "theorem card_derangements_eq_numDerangements",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 4},
            expected=9,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force count of the fixed-point-free permutations among all 4! orderings.",
        ),
        VerificationCase(
            inputs={"n": 10},
            expected=1334961,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Brute force over all 10! permutations, equal to the exact rational alternating "
                "sum."
            ),
        ),
        VerificationCase(
            inputs={"n": 20},
            expected=895014631192902121,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact Fraction alternating sum, cross-checked with the integer recurrence "
                "D_m = (m - 1)(D_{m-1} + D_{m-2})."
            ),
        ),
        VerificationCase(
            inputs={"n": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 0: brute force sees one empty permutation, which fixes nothing.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=0,
            rel_tol=1e-12,
            abs_tol=1e-12,
            note="Edge n = 1: brute force; the only permutation fixes its single item.",
        ),
    ),
    assumptions=(
        "n is a non-negative whole number; D_0 = 1 (the empty permutation has no fixed point) "
        "and D_1 = 0.",
        "Computed exactly in integer arithmetic, not with the rounding shortcut n!/e; the result "
        "is a Python int of any size.",
    ),
    tags=(
        "derangement",
        "subfactorial",
        "permutations without fixed points",
        "hat-check problem",
        "combinatorics",
        "counting",
    ),
)

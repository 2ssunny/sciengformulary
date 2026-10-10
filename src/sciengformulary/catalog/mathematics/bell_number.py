"""Bell Number: B(n) = sum_{i=0}^{n-1} binom(n - 1, i) * B(n - 1 - i), B(0) = 1."""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog.mathematics._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float) -> int:
    n = integer("n", n, minimum=0)
    bells = [1]
    # Row m of Pascal's triangle, kept up to date so no binomial is recomputed from scratch.
    row = [1]
    for m in range(n):
        bells.append(sum(row[i] * bells[m - i] for i in range(m + 1)))
        row = [1, *(row[i] + row[i + 1] for i in range(m)), 1]
    return bells[n]


bell_number = FormulaSpec(
    id="mathematics.bell_number",
    name="Bell Number",
    equation="B(n) = sum_{i=0}^{n-1} binom(n - 1, i) * B(n - 1 - i), B(0) = 1",
    description=(
        "The n-th Bell number, defined by the binomial recurrence B(0) = 1, "
        "B(n) = sum of binom(n - 1, i) B(n - 1 - i). It counts the ways to split a set of n "
        "distinct elements into non-empty, unordered blocks."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Size of the set, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="B",
        symbol="B_n",
        description="n-th Bell number",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines Nat.bell by B(0) = 1 and B(n + 1) = sum over i <= n of
        # choose(n, i) * B(n - i). Replacing n + 1 by n (n >= 1) gives the equation above.
        mathlib("Mathlib/Combinatorics/Enumerative/Bell.lean#L201", "def Nat.bell"),
        mathlib("Mathlib/Combinatorics/Enumerative/Bell.lean#L205", "theorem Nat.bell_succ"),
        mathlib(
            "Mathlib/Combinatorics/Enumerative/Bell.lean#L256",
            "theorem Nat.bell_eq_sum_partition",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 0: brute-force enumeration finds the single partition of the empty set.",
        ),
        VerificationCase(
            inputs={"n": 1},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = 1: brute-force enumeration.",
        ),
        VerificationCase(
            inputs={"n": 3},
            expected=5,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of the set partitions of a 3-element set.",
        ),
        VerificationCase(
            inputs={"n": 5},
            expected=52,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force enumeration of restricted growth strings of length 5.",
        ),
        VerificationCase(
            inputs={"n": 10},
            expected=115975,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact-integer run of the Mathlib recurrence; Dobinski's series in 50-digit "
                "mpmath agrees."
            ),
        ),
    ),
    assumptions=(
        "n is a non-negative whole number; B(0) = 1.",
        "Derived result: the cited recurrence is stated for B(n + 1); the equation here is the "
        "same recurrence with n + 1 replaced by n (an index shift). It was checked numerically "
        "in exact integers against the re-indexed form sum binom(n - 1, k) B(k) for n <= 20.",
        "The counting meaning (set partitions with unlabelled, non-empty blocks) was checked "
        "by brute-force enumeration for n <= 8; it is not what the cited Mathlib declarations "
        "formally prove, which is the recurrence (the counting meaning appears only in their "
        "documentation).",
        "Computed exactly in integer arithmetic (a Python int of any size); the work grows "
        "roughly with n^2 big-integer operations.",
    ),
    tags=(
        "Bell number",
        "set partitions",
        "combinatorics",
        "counting",
        "recurrence",
    ),
)

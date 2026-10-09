"""Unsigned Stirling Number of the First Kind:
c(n, k) = (n - 1) * c(n - 1, k) + c(n - 1, k - 1) for n, k >= 1; c(0, 0) = 1; c(n, 0) = c(0, k) = 0.
"""

from sciengformulary.catalog._sources import mathlib
from sciengformulary.catalog._domain import integer
from sciengformulary.core import FormulaSpec, VariableSpec, VerificationCase


def _evaluate(n: float, k: float) -> int:
    n = integer("n", n, minimum=0)
    k = integer("k", k, minimum=0)
    if k > n:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    # row[j] holds c(m, j) for the current m; update from the right so c(m - 1, j - 1) is
    # still the previous row's value when it is used.
    row = [1] + [0] * k
    for m in range(1, n + 1):
        for j in range(k, 0, -1):
            row[j] = (m - 1) * row[j] + row[j - 1]
        row[0] = 0
    return row[k]


stirling_number_first_kind_unsigned = FormulaSpec(
    id="mathematics.stirling_number_first_kind_unsigned",
    name="Unsigned Stirling Number of the First Kind",
    equation=(
        "c(n, k) = (n - 1) * c(n - 1, k) + c(n - 1, k - 1) for n, k >= 1; c(0, 0) = 1; "
        "c(n, 0) = c(0, k) = 0 for n, k >= 1"
    ),
    description=(
        "Unsigned Stirling number of the first kind, defined by the recurrence above (all "
        "values non-negative). It counts the permutations of n distinct elements that consist "
        "of exactly k disjoint cycles."
    ),
    inputs=(
        VariableSpec(
            name="n",
            symbol="n",
            description="Number of elements permuted, integer",
            dimension="1",
            si_unit="-",
        ),
        VariableSpec(
            name="k",
            symbol="k",
            description="Number of cycles, integer",
            dimension="1",
            si_unit="-",
        ),
    ),
    output=VariableSpec(
        name="c",
        symbol="c(n, k)",
        description="Unsigned Stirling number of the first kind",
        dimension="1",
        si_unit="-",
    ),
    evaluator=_evaluate,
    references=(
        # Mathlib defines c(n + 1, k + 1) = n c(n, k + 1) + c(n, k) with c(0, 0) = 1,
        # c(0, k + 1) = 0 and c(n + 1, 0) = 0. Replacing n + 1 by n and k + 1 by k (n, k >= 1)
        # gives the recurrence above.
        mathlib("Mathlib/Combinatorics/Enumerative/Stirling.lean#L54", "def Nat.stirlingFirst"),
        mathlib(
            "Mathlib/Combinatorics/Enumerative/Stirling.lean#L105",
            "theorem Nat.stirlingFirst_one_right",
        ),
    ),
    verification_cases=(
        VerificationCase(
            inputs={"n": 5, "k": 2},
            expected=50,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force cycle count over all 120 permutations of 5 items.",
        ),
        VerificationCase(
            inputs={"n": 4, "k": 2},
            expected=11,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force cycle count over the permutations of 4 items.",
        ),
        VerificationCase(
            inputs={"n": 6, "k": 3},
            expected=225,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Brute-force cycle count over all 720 permutations of 6 items.",
        ),
        VerificationCase(
            inputs={"n": 10, "k": 3},
            expected=1172700,
            rel_tol=1e-12,
            abs_tol=0.0,
            note=(
                "Exact-integer recurrence and the coefficient of x^3 in x (x + 1) ... (x + 9) "
                "(symbolic expansion) agree."
            ),
        ),
        VerificationCase(
            inputs={"n": 0, "k": 0},
            expected=1,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge n = k = 0: the empty permutation, with no cycles.",
        ),
        VerificationCase(
            inputs={"n": 7, "k": 1},
            expected=720,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 1: (n - 1)! = 6! = 720 cyclic permutations (stirlingFirst_one_right).",
        ),
        VerificationCase(
            inputs={"n": 5, "k": 0},
            expected=0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k = 0 < n: a permutation of a non-empty set has at least one cycle.",
        ),
        VerificationCase(
            inputs={"n": 3, "k": 4},
            expected=0,
            rel_tol=1e-12,
            abs_tol=0.0,
            note="Edge k > n: more cycles than elements is impossible.",
        ),
    ),
    assumptions=(
        "Unsigned convention, all values >= 0. The signed numbers s(n, k) = (-1)^(n - k) c(n, k) "
        "are not provided by this formula.",
        "n and k are non-negative whole numbers. k > n, and k = 0 < n, give the genuine count "
        "0 rather than an error.",
        "Derived result: the cited definition is stated for c(n + 1, k + 1); the recurrence "
        "here is the same one with n + 1 replaced by n and k + 1 by k (an index shift). It was "
        "checked numerically against the expansion x (x + 1) ... (x + n - 1) = "
        "sum_k c(n, k) x^k for n <= 9.",
        "The counting meaning (permutations with exactly k cycles) was checked by brute-force "
        "enumeration for n <= 7; it is not what the cited Mathlib declarations formally prove "
        "(it appears only in their documentation).",
        "Summing c(n, k) over k gives n!. Computed exactly in integer arithmetic; the work "
        "grows roughly with n * k big-integer operations.",
    ),
    tags=(
        "Stirling numbers",
        "first kind",
        "unsigned",
        "permutations",
        "cycles",
        "combinatorics",
    ),
)
